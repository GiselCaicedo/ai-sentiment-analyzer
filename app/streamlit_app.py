"""Run live CPU inference on a review or a CSV."""

import hashlib
from io import BytesIO
from time import perf_counter

import streamlit as st

from sentiment_analyzer.classifier import SentimentClassifier, score_reviews
from sentiment_analyzer.data_loader import load_reviews


@st.cache_resource
def load_classifier() -> SentimentClassifier:
    """Reuse the loaded model across Streamlit reruns."""
    return SentimentClassifier()


def single_review() -> None:
    """Show the single-review form and its prediction."""
    with st.form("single-review"):
        text = st.text_area("Review text", placeholder="The espresso tasted burnt.")
        submitted = st.form_submit_button("Classify review", type="primary")

    if not submitted:
        return
    if not text.strip():
        st.warning("Enter an English review before classifying.")
        return

    try:
        with st.spinner("Classifying the review…"):
            classifier = load_classifier()
            start = perf_counter()
            prediction = classifier.predict([text.strip()])[0]
            elapsed = perf_counter() - start
    except (OSError, ValueError, RuntimeError) as error:
        st.error(f"Classification failed. {error}")
        return

    sentiment, confidence = st.columns(2)
    sentiment.metric("Predicted sentiment", prediction.sentiment.title())
    confidence.metric("Model confidence", f"{prediction.confidence:.1%}")
    st.caption(f"CPU inference took {elapsed:.2f} seconds after model loading.")


def csv_reviews() -> None:
    """Validate and classify an upload and offer a scored CSV."""
    uploaded = st.file_uploader(
        "Review CSV",
        type=["csv"],
        help="Required columns: review_id, date, product, rating, review_text, true_label.",
    )
    if uploaded is None:
        st.session_state.pop("scored_csv", None)
        return

    content = uploaded.getvalue()
    digest = hashlib.sha256(content).hexdigest()
    previous = st.session_state.get("scored_csv")
    if previous is not None and previous[0] != digest:
        st.session_state.pop("scored_csv")

    if st.button("Classify CSV", type="primary"):
        try:
            reviews = load_reviews(BytesIO(content))
            with st.spinner("Classifying reviews on CPU…"):
                scored = score_reviews(reviews, load_classifier())
        except (OSError, ValueError, RuntimeError) as error:
            st.session_state.pop("scored_csv", None)
            st.error(f"The upload could not be scored. {error}")
            return
        st.session_state["scored_csv"] = (digest, scored)

    result = st.session_state.get("scored_csv")
    if result is not None:
        scored = result[1]
        dropped = scored.attrs["rows_dropped"]
        st.success(f"Scored {len(scored)} reviews. Dropped {dropped} blank or duplicate rows.")
        st.dataframe(scored, hide_index=True)
        st.download_button(
            "Download scored CSV",
            scored.to_csv(index=False, date_format="%Y-%m-%d").encode("utf-8"),
            file_name="reviews_scored.csv",
            mime="text/csv",
            on_click="ignore",
        )


st.set_page_config(page_title="Bean & Leaf sentiment demo", page_icon=None)
st.title("Bean & Leaf sentiment demo")
st.write("Classify English café reviews with the same RoBERTa model used in the report.")
st.caption(
    "The first prediction may take longer while the model loads. Confidence is the model score."
)
review_tab, csv_tab = st.tabs(["Single review", "Upload CSV"])
with review_tab:
    single_review()
with csv_tab:
    csv_reviews()
