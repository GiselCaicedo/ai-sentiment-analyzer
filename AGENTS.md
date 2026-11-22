# AGENTS.md – AI Sentiment Analyzer (Gen AI Bootcamp, Project 19)

Read `docs/PLAN.md` before writing code. It is the source of truth. Run **all phases in order without asking for confirmation**. After each phase, check its acceptance criteria, commit (`git commit -m "Phase N: ..."`) and move on. If something fails, try to fix it; if it stays blocked, write it in `PENDING.md` (what failed and what you tried) and continue with whatever does not depend on it. At the end, write a summary in `PENDING.md`: what is done, what is missing and what Gisel must review.

**Deployment:** if there is no GitHub remote or authentication fails, leave the workflow ready and write the publishing steps in `PENDING.md`. Do not stop because of it.

**Model download:** the first run downloads ~500 MB. If the download fails, finish everything that works with `FakeClassifier`, and note it in `PENDING.md`.
 The course is in English: **all code, comments, README, UI text and the dataset are in English.**

## Fixed stack

- Python 3.11, `pandas`, `transformers`, `torch` (CPU), `pytest`. Keep the code small: `analyzer.py` + `server.py`.
- Static report site: plain HTML + CSS + vanilla JavaScript (ES modules), no framework and no build step. Deployed to GitHub Pages.
- Model: `cardiffnlp/twitter-roberta-base-sentiment-latest` (3 labels: negative, neutral, positive).

## Python code style (clean, solid, not over-engineered)

- `src/` layout, package `sentiment_analyzer`. Type hints on every public function. `pathlib.Path` for paths. `logging`, not `print`, outside the CLI.
- Small modules with one job each (see the plan). Pure functions for the analysis so they can be tested without the model.
- Use a `@dataclass` for config/results where it makes the code clearer. No abstract base classes, no plugin systems, no metaclasses.
- `classify(reviews, model=None)` takes the model as an optional argument. Tests pass a small `fake_model` function, so they never download the model.
- Short docstrings (one line, plus `Args/Returns` only when not obvious). Run `ruff check` and `ruff format`.
- No API keys are needed. If one is ever added, it goes in `.env` (git-ignored) and `.env.example`.

## Web code style

- Semantic HTML, CSS custom properties, `fetch('data/report.json')`. Charts drawn with inline SVG generated in JS (no chart library).
- Use **modern-web-guidance** before building tables, filters, forms, dialogs, dark mode or accessibility details.
- Use **unslop** in the polish phase on the finished page.

## Commands

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scriptsctivate
pip install -r requirements.txt
python -m sentiment_analyzer.server                 # web app with live analysis (localhost:8000)
python -m sentiment_analyzer.analyzer               # rebuild web/data/report.json and the Markdown report
pytest
```

## Definition of done

- `pytest` and `ruff check` pass.
- `python -m sentiment_analyzer.analyzer` regenerates `web/data/report.json` and `reports/feedback_report.md` without errors.
- The static site works when opened through `http.server` and on GitHub Pages.

## Do not

- Do not commit the model weights, `.venv` or `__pycache__`.
- Do not call paid APIs; everything runs locally with the pretrained model.
- Do not add a backend to the deployed site: GitHub Pages only serves static files.
