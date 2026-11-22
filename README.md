# AI Sentiment Analyzer — Project 19

A coffee shop (Bean & Leaf) wants to know whether its customer reviews are positive, negative or neutral.
This project classifies them with a **pretrained Hugging Face Transformers model** and summarizes the
results with **Pandas** into a customer feedback analysis report.

- **Model:** [`cardiffnlp/twitter-roberta-base-sentiment-latest`](https://huggingface.co/cardiffnlp/twitter-roberta-base-sentiment-latest) (RoBERTa, 3 classes), run locally on CPU. No API keys.
- **Data:** 80 English reviews of 8 products in [`data/sample_reviews.csv`](data/sample_reviews.csv), each with a human label to measure accuracy.
- **Result:** 41 positive · 21 neutral · 18 negative, 86.2 % accuracy vs. human labels.

## Where each student task happens

| Task | Code | Also shown in |
|------|------|---------------|
| Load sample reviews | [`data_loader.py`](src/sentiment_analyzer/data_loader.py) | Notebook § 1 |
| Use a pretrained sentiment model | [`classifier.py`](src/sentiment_analyzer/classifier.py) (`transformers.pipeline`) | Notebook § 2 |
| Classify each review | [`classifier.py`](src/sentiment_analyzer/classifier.py) (`score_reviews`) | Notebook § 3 |
| Calculate sentiment counts with Pandas | [`analysis.py`](src/sentiment_analyzer/analysis.py) (`value_counts`, `crosstab`, `groupby`) | Notebook § 4 |
| **Expected output:** feedback report | [`report.py`](src/sentiment_analyzer/report.py) → [`reports/feedback_report.md`](reports/feedback_report.md) | Notebook, web site |

## Four ways to see it run

1. **Notebook (step by step, with outputs):** [`notebooks/sentiment_analysis.ipynb`](notebooks/sentiment_analysis.ipynb).
   It is saved already executed, so it can be read on GitHub without running anything.
2. **Full pipeline:** scores every review with the model and regenerates the report, JSON, CSV and charts.
   ```bash
   python -m sentiment_analyzer.cli --input data/sample_reviews.csv --out web/data
   ```
3. **One review from the terminal:**
   ```bash
   python -m sentiment_analyzer.classify_cli "The coffee was cold and the staff ignored me."
   ```
4. **Live demo (Streamlit):** type a review or upload a CSV and the model classifies it in real time.
   ```bash
   streamlit run app/streamlit_app.py
   ```

The static site in [`web/`](web/) is the published report: it shows the results the model produced
(`web/data/report.json`). GitHub Pages only serves static files, so the model itself runs in the
pipeline, the notebook and the Streamlit app.

## Setup

```bash
python -m venv .venv && .venv\Scripts\activate      # macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
pytest
```

The first run downloads the model (~500 MB); after that it is cached. With Docker:
`docker compose up --build` (site on http://localhost:8090, Streamlit on http://localhost:8501).
