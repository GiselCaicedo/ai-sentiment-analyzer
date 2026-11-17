import pandas as pd

from sentiment_analyzer import evaluation


def test_evaluation(reviews: pd.DataFrame) -> None:
    assert evaluation.accuracy(reviews) == 0.75
    assert evaluation.confusion_matrix(reviews).values.tolist() == [
        [1, 0, 0],
        [0, 1, 0],
        [0, 1, 1],
    ]
    assert evaluation.misclassified(reviews)["review_id"].tolist() == [2]
    assert evaluation.rating_mismatch_pct(reviews) == 50
    assert evaluation.rating_mismatch_pct(reviews.iloc[:1]) == 0
