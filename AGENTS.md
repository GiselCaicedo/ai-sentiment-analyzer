# AGENTS.md – AI Sentiment Analyzer (Gen AI Bootcamp, Project 19)

Gisel has to study and explain this code in class, so **keep it as small and simple as possible**.
The course is in English: code, comments, README, UI text and the dataset are in English.

## What is here

- `src/sentiment_analyzer/analyzer.py` – the four tasks: `load_reviews` → `get_model` → `classify` → `summarize`, plus `to_markdown` (the report) and `add_review`.
- `src/sentiment_analyzer/server.py` – stdlib web server: serves `web/` and the routes `GET /api/report`, `POST /api/classify`, `POST /api/add`. Sends CORS headers so the GitHub Pages page can call it on `localhost:8000`.
- `web/` – plain HTML + CSS + vanilla JS, no framework and no build step. Deployed to GitHub Pages (`.github/workflows/pages.yml`); without the server it shows `web/data/report.json`.
- `data/sample_reviews.csv` – 80 fictional reviews with a human label (`true_label`).
- `notebooks/` step by step · `docs/COMO_FUNCIONA.md` study guide (Spanish) · `presentation/` the class deck and script.

## Stack

Python 3.11, `pandas`, `transformers`, `torch` (CPU), `pytest`, `ruff`.
Model: `cardiffnlp/twitter-roberta-base-sentiment-latest` (positive / neutral / negative). No API keys.

## Commands

```bash
python -m venv .venv && .venv\Scripts\activate     # macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python -m sentiment_analyzer.server                 # web app with live analysis (localhost:8000)
python -m sentiment_analyzer.analyzer               # rebuild web/data/report.json and reports/feedback_report.md
pytest                                              # uses a fake model, no download
ruff check . && ruff format .
```

## Rules

- Tests pass a small `fake_model` to `classify(reviews, model)`, so they never download the model.
- Reviews added from the page are appended to the CSV: restore it with `git checkout data/sample_reviews.csv` before committing.
- Do not commit the model weights, `.venv` or `__pycache__`. Do not call paid APIs.
