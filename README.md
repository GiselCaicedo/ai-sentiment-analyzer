# AI Sentiment Analyzer — Project 19

Saved report online: https://giselcaicedo.github.io/ai-sentiment-analyzer/
(the buttons need the local server, see **Run it**).

Classifies customer reviews of a coffee shop (Bean & Leaf) as **positive, neutral or negative** with a
pretrained Hugging Face model, counts the results with **Pandas**, and writes a feedback report.

- **Model:** [`cardiffnlp/twitter-roberta-base-sentiment-latest`](https://huggingface.co/cardiffnlp/twitter-roberta-base-sentiment-latest), runs on CPU, no API keys.
- **Data:** 80 sample reviews in [`data/sample_reviews.csv`](data/sample_reviews.csv), each with a human label.
- **Result:** 41 positive · 21 neutral · 18 negative · 86.2 % accuracy against the human labels.

## The code (two files)

| File | What it does |
|------|--------------|
| [`analyzer.py`](src/sentiment_analyzer/analyzer.py) | The four tasks: `load_reviews` → `get_model` → `classify` → `summarize`, plus `to_markdown` for the report and `add_review` |
| [`server.py`](src/sentiment_analyzer/server.py) | Serves the web page: `GET /api/report`, `POST /api/classify`, `POST /api/add` |
| [`web/`](web/) | The page: the dataset report, plus a free field to **Classify** one review or **Add to dataset** |

## Run it

```bash
python -m venv .venv && .venv\Scripts\activate      # macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt

python -m sentiment_analyzer.server     # web app → http://localhost:8000
python -m sentiment_analyzer.analyzer   # rebuild web/data/report.json and reports/feedback_report.md
pytest                                  # tests (use a fake model, no download)
```

Step by step with outputs: [`notebooks/sentiment_analysis.ipynb`](notebooks/sentiment_analysis.ipynb).
With Docker: `docker compose up --build`, then open http://localhost:8000.
The first run downloads the model (~500 MB).

On GitHub Pages the page shows the saved report; the buttons need the local server.
Reviews added from the page are appended to `data/sample_reviews.csv` (`git checkout data/sample_reviews.csv` restores it).

## Limitations

- The 80 reviews are a small, fictional sample ([source details](data/DATA_SOURCE.md)).
- The model only understands English, and it misses sarcasm ("Amazing croissant, if you enjoy chewing cardboard" → positive, 98 %).
- One sentiment per review, even when a review talks about several things.
- The model needs ~880 MB of memory, so it runs on a laptop, not on a free cloud server.
