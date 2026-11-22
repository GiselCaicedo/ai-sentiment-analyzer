"""Build the project presentation (10 slides) with MckEngine + native PowerPoint charts.

Run: python presentation/build_deck.py   (needs python-pptx and ~/deckkit/mck)
All numbers come from the model run on the original 80 reviews in data/sample_reviews.csv.
"""

import os
import re
import sys
from pathlib import Path

sys.path.insert(0, os.path.expanduser("~/deckkit/mck"))

from mck_ppt import MckEngine  # noqa: E402
from mck_ppt.constants import (  # noqa: E402
    ACCENT_RED,
    BG_GRAY,
    BODY_SIZE,
    CONTENT_TOP,
    CW,
    DARK_GRAY,
    LINE_GRAY,
    LM,
    NAVY,
    SUB_HEADER_SIZE,
)
from mck_ppt.core import add_action_title, add_rect, add_text  # noqa: E402
from pptx.chart.data import CategoryChartData  # noqa: E402
from pptx.dml.color import RGBColor  # noqa: E402
from pptx.enum.chart import XL_CHART_TYPE, XL_LABEL_POSITION, XL_LEGEND_POSITION  # noqa: E402
from pptx.enum.text import MSO_ANCHOR  # noqa: E402
from pptx.util import Inches, Pt  # noqa: E402

HERE = Path(__file__).resolve().parent
OUT = HERE / "AI_Sentiment_Analyzer.pptx"
SCREENSHOT = HERE / "app_screenshot.png"
LIGHT_GRAY = RGBColor(0xC8, 0xC8, 0xC8)
MID_GRAY = RGBColor(0x8C, 0x8C, 0x8C)
DATA_SRC = "Source: model run on data/sample_reviews.csv (80 reviews, Aug–Nov 2026)"

eng = MckEngine(total_slides=10)


def script_sections(path):
    """Read SCRIPT.md: the text under '## Slide N' becomes the notes of slide N."""
    sections, current = {}, None
    for line in path.read_text(encoding="utf-8").splitlines():
        match = re.match(r"## Slide (\d+)", line)
        if match:
            current = int(match.group(1))
            sections[current] = []
        elif line.startswith("## ") or line.startswith("---"):
            current = None
        elif current is not None:
            sections[current].append(re.sub(r"[*>]", "", line).strip())
    return {n: "\n".join(lines).strip() for n, lines in sections.items()}


def style_chart(chart):
    chart.font.size = Pt(12)
    chart.font.name = "Arial"
    chart.font.color.rgb = DARK_GRAY


def insight_panel(slide, x, y, w, h, heading, bullets):
    add_rect(slide, x, y, w, h, BG_GRAY)
    add_text(
        slide,
        x + Inches(0.25),
        y + Inches(0.2),
        w - Inches(0.5),
        Inches(0.4),
        heading,
        font_size=SUB_HEADER_SIZE,
        font_color=NAVY,
        bold=True,
    )
    add_text(
        slide,
        x + Inches(0.25),
        y + Inches(0.75),
        w - Inches(0.5),
        h - Inches(0.9),
        bullets,
        font_size=BODY_SIZE,
        font_color=DARK_GRAY,
        line_spacing=Pt(10),
    )


# 1. Cover: the thesis as the title -------------------------------------------
s = eng.cover(
    title="A pretrained model turns\ncafé reviews into a feedback\nreport in seconds",
    subtitle="AI Sentiment Analyzer · Gen AI Bootcamp, Project 19",
    author="Gisel Caicedo",
    date="November 2026",
)

# 2. Problem --------------------------------------------------------------------
s = eng.three_stat(
    title="Reviews hold the answer, but nobody can read them all by hand",
    stats=[
        ("80", "English reviews, Aug–Nov 2026", True),
        ("8", "café products, 10 reviews each", False),
        ("3", "labels: positive, neutral, negative", False),
    ],
    detail_items=[
        "Bean & Leaf (a fictional café chain) wants to know how customers feel about each product",
        "Reading by hand is slow and inconsistent, and it hides patterns by product or month",
        "Goal: classify every review automatically, count the results and deliver a report",
        "Each sample review also has a human label, so we can check the model",
    ],
    source="Source: Project 19 brief (Gen AI Bootcamp); data/DATA_SOURCE.md",
)

# 3. Objectives -------------------------------------------------------------------
s = eng.four_column(
    title="Four tasks turn raw reviews into a report the business can use",
    items=[
        (
            "1",
            "Load reviews",
            ["Read the sample CSV", "Trim spaces", "Drop empty and repeated reviews"],
        ),
        (
            "2",
            "Pretrained model",
            [
                "RoBERTa from Hugging Face",
                "Already trained for sentiment",
                "No training, no API key",
            ],
        ),
        (
            "3",
            "Classify reviews",
            ["Positive, neutral or negative", "Confidence from 0 to 1", "All reviews in one call"],
        ),
        (
            "4",
            "Count with Pandas",
            ["Totals and percentages", "Breakdown by product", "Feedback report (.md)"],
        ),
    ],
    source="Source: Project 19 student tasks and expected output (Gen AI Bootcamp)",
)

# 4. Technologies -----------------------------------------------------------------
s = eng.table_insight(
    title="Open-source tools cover the whole pipeline, with no paid API",
    headers=["Tool", "Role in the project"],
    rows=[
        ["Python 3.11", "Runs the analysis and the small local web server"],
        ["Hugging Face Transformers", "Loads the pretrained RoBERTa sentiment model"],
        ["Pandas", "Reads the CSV, cleans it and counts sentiments"],
        ["HTML · CSS · JavaScript", "Web page: review field, cards, bars and tables"],
        ["GitHub Pages + Actions", "Publishes the page on every push to main"],
        ["pytest", "8 tests with a fake model, no download needed"],
    ],
    insights=[
        "Model: cardiffnlp/twitter-roberta-base-sentiment-latest (3 labels)",
        "Runs on a normal laptop CPU: ~4 s to load, ~1–2 s for 80 reviews",
        "No API keys, so nothing secret is in GitHub",
    ],
    col_widths=[Inches(2.9), Inches(4.2)],
    insight_title="Why this stack",
    source="Source: requirements.txt; timings measured on the author's laptop (CPU)",
)

# 5. Implementation: the pipeline -------------------------------------------------
s = eng.process_chevron(
    title="Five small functions in one Python file go from CSV to report",
    steps=[
        ("1", "Load", "load_reviews(): read_csv, drop_duplicates"),
        ("2", "Model", "get_model(): Hugging Face pipeline"),
        ("3", "Classify", "classify(): sentiment + confidence"),
        ("4", "Count", "summarize(): value_counts, crosstab"),
        ("5", "Report", "to_markdown(): writes the report"),
    ],
    bottom_bar=("Result", "analyzer.py is ~130 lines; the model loads once and is reused"),
    source="Source: src/sentiment_analyzer/analyzer.py",
)
code_y = Inches(3.9)
add_text(
    s,
    LM,
    code_y,
    CW,
    Inches(0.4),
    "The Pandas part, inside summarize()",
    font_size=BODY_SIZE,
    font_color=NAVY,
    bold=True,
)
add_rect(s, LM, code_y + Inches(0.45), CW, Inches(1.55), NAVY)
add_text(
    s,
    LM + Inches(0.3),
    code_y + Inches(0.55),
    CW - Inches(0.6),
    Inches(1.4),
    [
        'counts = scored["sentiment"].value_counts().reindex(LABELS, fill_value=0)',
        "percentages = (counts / len(scored) * 100).round(1)",
        'by_product = pd.crosstab(scored["product"], scored["sentiment"])',
    ],
    font_size=BODY_SIZE,
    font_name="Consolas",
    font_color=RGBColor(0xFF, 0xFF, 0xFF),
    line_spacing=Pt(8),
)

# 6. Web app and deployment (real screenshot) -------------------------------------
s = eng._ns()
add_action_title(s, "The deployed page classifies reviews with the model on my PC")
img_h = Inches(5.0)
img_w = int(img_h * 1280 / 900)
img_x = LM + CW - img_w
left_w = img_x - LM - Inches(0.35)
add_text(
    s,
    LM,
    CONTENT_TOP,
    left_w,
    Inches(0.4),
    "How the demo works",
    font_size=SUB_HEADER_SIZE,
    font_color=NAVY,
    bold=True,
)
add_text(
    s,
    LM,
    CONTENT_TOP + Inches(0.55),
    left_w,
    Inches(3.0),
    [
        "GitHub Pages hosts the page (deploy requirement)",
        "server.py runs the model on my PC, port 8000",
        "The page calls /api/report, /api/classify and /api/add",
        "Without the server, it shows the last saved report",
    ],
    font_size=BODY_SIZE,
    line_spacing=Pt(10),
)
add_rect(s, LM, CONTENT_TOP + Inches(3.9), left_w, Inches(1.1), BG_GRAY)
add_text(
    s,
    LM + Inches(0.2),
    CONTENT_TOP + Inches(3.9),
    left_w - Inches(0.4),
    Inches(1.1),
    ["Live page:", "giselcaicedo.github.io/", "ai-sentiment-analyzer"],
    font_size=BODY_SIZE,
    font_color=NAVY,
    bold=True,
    anchor=MSO_ANCHOR.MIDDLE,
)
pic = s.shapes.add_picture(str(SCREENSHOT), img_x, CONTENT_TOP, img_w, img_h)
pic.line.color.rgb = LINE_GRAY
eng._footer(s, "Source: screenshot of the running app (localhost, original 80 reviews)")

# 7. Results by product (native stacked bar) --------------------------------------
products = ["Sandwich", "Croissant", "Cold Brew", "Espresso", "Latte", "Bagel", "Matcha", "Muffin"]
counts = {  # positive, neutral, negative per product (model output)
    "Sandwich": (2, 2, 6),
    "Croissant": (5, 2, 3),
    "Cold Brew": (6, 2, 2),
    "Espresso": (5, 3, 2),
    "Latte": (5, 3, 2),
    "Bagel": (6, 3, 1),
    "Matcha": (7, 2, 1),
    "Muffin": (5, 4, 1),
}
s = eng._ns()
add_action_title(s, "Sandwiches get 6 of 18 negative reviews: the first thing to fix")
cd = CategoryChartData()
order = list(reversed(products))  # bar charts draw bottom-up
cd.categories = order
for i, name in enumerate(["Negative", "Neutral", "Positive"]):
    idx = {"Negative": 2, "Neutral": 1, "Positive": 0}[name]
    cd.add_series(name, [counts[p][idx] for p in order])
chart_w = Inches(7.6)
gf = s.shapes.add_chart(XL_CHART_TYPE.BAR_STACKED, LM, CONTENT_TOP, chart_w, Inches(5.1), cd)
chart = gf.chart
style_chart(chart)
chart.has_legend = True
chart.legend.position = XL_LEGEND_POSITION.TOP
chart.legend.include_in_layout = False
for series, color in zip(chart.series, [ACCENT_RED, MID_GRAY, LIGHT_GRAY]):
    series.format.fill.solid()
    series.format.fill.fore_color.rgb = color
    series.data_labels.show_value = True
    series.data_labels.font.size = Pt(11)
    series.data_labels.font.color.rgb = (
        RGBColor(0xFF, 0xFF, 0xFF) if color != LIGHT_GRAY else DARK_GRAY
    )
chart.plots[0].gap_width = 60
chart.value_axis.visible = False
chart.value_axis.has_major_gridlines = False
insight_panel(
    s,
    LM + chart_w + Inches(0.3),
    CONTENT_TOP,
    CW - chart_w - Inches(0.3),
    Inches(5.1),
    "What the counts say",
    [
        "Overall: 51% positive, 26% neutral, 23% negative",
        "Sandwich is the only product with more negative than positive reviews",
        "Matcha and Bagel lead on positive reviews",
        "Each product has 10 reviews",
    ],
)
eng._footer(s, DATA_SRC + "; counts by product with pd.crosstab")

# 8. Results by month (native column chart, October highlighted) ------------------
s = eng._ns()
add_action_title(s, "Negative reviews jumped to 13 in October, from 2 a month before")
months = ["Aug 2026", "Sep 2026", "Oct 2026", "Nov 2026"]
negatives = [2, 2, 13, 1]
cd = CategoryChartData()
cd.categories = months
cd.add_series("Negative reviews", negatives)
gf = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, LM, CONTENT_TOP, chart_w, Inches(5.1), cd)
chart = gf.chart
style_chart(chart)
chart.has_legend = False
plot = chart.plots[0]
plot.gap_width = 70
plot.has_data_labels = True
plot.data_labels.show_value = True
plot.data_labels.position = XL_LABEL_POSITION.OUTSIDE_END
plot.data_labels.font.size = Pt(14)
plot.data_labels.font.bold = True
for i, point in enumerate(plot.series[0].points):
    point.format.fill.solid()
    point.format.fill.fore_color.rgb = ACCENT_RED if months[i].startswith("Oct") else LIGHT_GRAY
chart.value_axis.visible = False
chart.value_axis.has_major_gridlines = False
chart.value_axis.maximum_scale = 15
insight_panel(
    s,
    LM + chart_w + Inches(0.3),
    CONTENT_TOP,
    CW - chart_w - Inches(0.3),
    Inches(5.1),
    "Inside October",
    [
        "13 of the 18 negative reviews (72%) are from October",
        "6 of them are sandwiches",
        "Several mention the “new staff” or the “new kitchen crew”",
        "November is back to 1 negative review",
    ],
)
eng._footer(s, DATA_SRC + "; counts by month with pd.crosstab")

# 9. Model evaluation ---------------------------------------------------------------
s = eng.table_insight(
    title="The model agrees with humans on 69 of 80 reviews; sarcasm fools it",
    headers=["Human label ↓  /  Model →", "Positive", "Neutral", "Negative"],
    rows=[
        ["Positive (37)", "35", "2", "0"],
        ["Neutral (20)", "4", "16", "0"],
        ["Negative (23)", "2", "3", "18"],
    ],
    insights=[
        "Accuracy: 86.2% (69 of 80)",
        "Both negatives called positive are sarcasm, at 98% confidence: “Great, a lovely green "
        "drink that tastes just like dishwater”",
        "Mixed reviews (“a bit dense, but the topping was nice”) lean positive",
    ],
    col_widths=[Inches(2.9), Inches(1.4), Inches(1.4), Inches(1.4)],
    insight_title="What we learn",
    source="Source: model predictions vs. human labels in data/sample_reviews.csv (80 reviews)",
)

# 10. Limitations and next steps (closing = next step, no 'thank you') -------------
s = eng.numbered_list_panel(
    title="Next: real reviews, more languages and sentiment per aspect",
    items=[
        ("Test on real reviews", "The sample is small and written by hand; accuracy is indicative"),
        ("Support Spanish", "The model only reads English; switch to a multilingual model"),
        ("Catch sarcasm", "Flag 1–2 star reviews predicted positive for a human to check"),
        ("Sentiment per aspect", "Separate coffee, food, service and wait time in one review"),
    ],
    panel={
        "big_number": "86.2%",
        "big_label": "accuracy on 80 reviews",
        "metrics": [("Tests", "8 passing"), ("Deploy", "GitHub Pages"), ("Model RAM", "~880 MB")],
    },
    source="Source: project README and evaluation above; RAM measured on the author's laptop",
)

for number, text in script_sections(HERE / "SCRIPT.md").items():
    eng.prs.slides[number - 1].notes_slide.notes_text_frame.text = text

eng.save(str(OUT))
print("saved", OUT)
