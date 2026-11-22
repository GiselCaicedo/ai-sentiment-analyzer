"""Tests use a fake model and a temporary copy of the dataset: fast, no download, no changes."""

import json
import threading
from urllib.error import HTTPError
from urllib.request import Request, urlopen

import pandas as pd
import pytest

from sentiment_analyzer import analyzer, server


def fake_model(texts, **options):
    """Pretend to be the Hugging Face pipeline: 'good' is positive, 'bad' is negative."""
    results = []
    for text in texts:
        text = text.lower()
        label = "positive" if "good" in text else "negative" if "bad" in text else "neutral"
        results.append({"label": label, "score": 0.9})
    return results


CSV = """review_id,date,product,rating,review_text,true_label
1,2026-08-01,Latte,5,Very good latte,positive
2,2026-08-02,Latte,1,Bad and cold,negative
3,2026-08-03,Bagel,3,It was a bagel,negative
4,2026-08-04,Bagel,3,  ,neutral
5,2026-08-05,Bagel,5,Very good latte,positive
"""


@pytest.fixture
def dataset(tmp_path):
    path = tmp_path / "reviews.csv"
    path.write_text(CSV, encoding="utf-8")
    return path


def test_load_reviews_drops_empty_and_repeated_rows(dataset):
    reviews = analyzer.load_reviews(dataset)
    assert reviews["review_text"].tolist() == ["Very good latte", "Bad and cold", "It was a bagel"]


def test_classify_adds_sentiment_and_confidence(dataset):
    scored = analyzer.classify(analyzer.load_reviews(dataset), fake_model)
    assert scored["sentiment"].tolist() == ["positive", "negative", "neutral"]
    assert scored["confidence"].tolist() == [0.9, 0.9, 0.9]


def test_analyze_counts_products_and_accuracy(dataset):
    report = analyzer.analyze(dataset, fake_model)
    assert report["total"] == 3
    assert report["counts"] == {"positive": 1, "neutral": 1, "negative": 1}
    assert report["percentages"]["positive"] == 33.3
    assert report["by_product"][0] == {
        "product": "Bagel",
        "positive": 0,
        "neutral": 1,
        "negative": 0,
    }
    assert report["accuracy"] == 66.7  # the bagel review was labelled negative by a human
    assert "| Positive | 1 | 33.3% |" in report["markdown"]


def test_classify_text_does_not_save_anything(dataset):
    result = analyzer.classify_text("  So good!  ", fake_model)
    assert result == {"review_text": "So good!", "sentiment": "positive", "confidence": 0.9}
    assert len(pd.read_csv(dataset)) == 5


def test_add_review_appends_a_row_without_a_human_label(dataset):
    analyzer.add_review("Good   muffin", "Muffin", dataset)
    last = pd.read_csv(dataset, keep_default_na=False).iloc[-1]
    assert (last["review_id"], last["product"], last["review_text"]) == (6, "Muffin", "Good muffin")
    assert last["true_label"] == ""
    report = analyzer.analyze(dataset, fake_model)
    assert report["total"] == 4
    assert report["accuracy"] == 66.7  # the new review has no label, so accuracy is unchanged


@pytest.mark.parametrize(
    ("text", "error"), [("   ", "Write a review"), ("Bad and cold", "already")]
)
def test_add_review_rejects_empty_or_repeated(dataset, text, error):
    with pytest.raises(ValueError, match=error):
        analyzer.add_review(text, "Latte", dataset)


def post(url, data):
    request = Request(url, data=json.dumps(data).encode(), method="POST")
    try:
        with urlopen(request, timeout=5) as response:
            return response.status, json.load(response)
    except HTTPError as error:  # 4xx answers still have a JSON body
        return error.code, json.load(error)


def test_server_routes(dataset, monkeypatch):
    monkeypatch.setattr(analyzer, "_model", fake_model)
    monkeypatch.setattr(analyzer, "DATASET", dataset)
    httpd = server.make_server(port=0)  # port 0 = any free port
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    url = f"http://127.0.0.1:{httpd.server_address[1]}"
    try:
        with urlopen(url + "/api/report", timeout=5) as response:
            assert json.load(response)["total"] == 3

        assert post(url + "/api/classify", {"text": "bad toast"})[1]["sentiment"] == "negative"

        status, report = post(url + "/api/add", {"text": "good toast", "product": "Bagel"})
        assert (status, report["total"]) == (200, 4)

        status, answer = post(url + "/api/add", {"text": ""})
        assert (status, answer["error"]) == (400, "Write a review first.")
    finally:
        httpd.shutdown()
        httpd.server_close()
