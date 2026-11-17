import { labels, renderMonthlyChart, renderProductChart, renderSentimentChart } from "./charts.js";

const id = name => document.getElementById(name);
const titleCase = label => label[0].toUpperCase() + label.slice(1);
const pct = new Intl.NumberFormat("en", { style: "percent", maximumFractionDigits: 2 });
const monthFormat = new Intl.DateTimeFormat("en", { month: "short", year: "numeric", timeZone: "UTC" });
const monthName = month => monthFormat.format(new Date(month + "-01T00:00:00Z"));

function element(tag, text, className) {
  const node = document.createElement(tag);
  if (text !== undefined) node.textContent = text;
  if (className) node.className = className;
  return node;
}

function tableRow(values, headers = false) {
  const row = document.createElement("tr");
  values.forEach((value, i) => {
    const cell = element(headers || i === 0 ? "th" : "td", value);
    if (headers) cell.scope = "col";
    else if (i === 0) cell.scope = "row";
    row.append(cell);
  });
  return row;
}

function renderSummary(report) {
  const stats = [
    ["Reviews analyzed", report.total_reviews, ""],
    ...labels.map(label => [
      titleCase(label), pct.format(report.percentages[label] / 100), label,
    ]),
    ["Model accuracy", pct.format(report.evaluation.accuracy), ""],
  ];
  for (const [label, value, sentiment] of stats) {
    const group = element("div", undefined, sentiment ? "stat " + sentiment : "stat");
    group.append(element("dt", label), element("dd", value));
    id("summary").append(group);
  }
}

function renderQuotes(report, sentiment) {
  const group = id("quotes-" + sentiment);
  const reviews = new Map(report.reviews.map(review => [review.review_id, review]));
  const quotes = report["top_" + sentiment];
  if (!quotes.length) group.append(element("p", "No reviews in this class.", "muted"));
  for (const item of quotes) {
    const record = reviews.get(item.review_id);
    const quote = element("figure", undefined, "quote");
    quote.append(element("blockquote", "“" + item.text + "”"));
    const disagreement = record.true_label !== sentiment ? " · Hand label: " + record.true_label : "";
    quote.append(element("figcaption",
      record.product + " · " + pct.format(item.confidence) + " confidence" + disagreement,
    ));
    group.append(quote);
  }
}

function renderEvaluation(report) {
  const evaluation = report.evaluation;
  const mistakes = evaluation.misclassified;
  const correct = report.total_reviews - mistakes.length;
  id("evaluation-line").textContent = correct + " of " + report.total_reviews + " predictions matched the hand labels.";
  const low = report.reviews.filter(review => review.rating <= 2).length;
  id("rating-insight").textContent = low
    ? pct.format(report.rating_mismatch_pct / 100) + " of 1–2 star reviews were predicted positive or neutral."
    : "This sample has no 1–2 star reviews.";

  const matrix = evaluation.confusion_matrix;
  id("matrix").tHead.append(tableRow(["Hand label", ...matrix.labels.map(titleCase)], true));
  matrix.matrix.forEach((values, i) => {
    const row = tableRow([titleCase(matrix.labels[i]), ...values]);
    row.cells[i + 1].classList.add("match");
    id("matrix").tBodies[0].append(row);
  });
  if (!mistakes.length) id("misclassified").append(element("li", "Every prediction matched its hand label."));
  for (const review of mistakes) {
    const item = element("li");
    item.append(
      element("p", "“" + review.text + "”"),
      element("span", review.product + " · " + titleCase(review.true_label) + " → " + titleCase(review.sentiment), "muted"),
    );
    id("misclassified").append(item);
  }
}

function renderReviews(report) {
  const query = id("filter-query");
  const sentiment = id("filter-sentiment");
  const product = id("filter-product");
  const form = id("filters");

  for (const label of labels) sentiment.add(new Option(titleCase(label), label));
  for (const row of report.by_product) product.add(new Option(row.product, row.product));

  function update() {
    const term = query.value.trim().toLowerCase();
    const filtered = report.reviews.filter(review =>
      (!sentiment.value || review.sentiment === sentiment.value)
      && (!product.value || review.product === product.value)
      && review.text.toLowerCase().includes(term),
    );
    const rows = filtered.map(review => {
      const row = tableRow([
        review.text, review.product, review.rating + "/5", titleCase(review.sentiment),
        pct.format(review.confidence), titleCase(review.true_label), review.date,
      ]);
      row.cells[3].classList.add("sentiment-text", review.sentiment);
      return row;
    });
    id("reviews-body").replaceChildren(...rows);
    id("review-status").textContent = filtered.length
      ? filtered.length + " of " + report.total_reviews + " reviews"
      : "No reviews match these filters.";
  }
  query.addEventListener("input", update);
  product.addEventListener("change", update);
  sentiment.addEventListener("change", update);
  form.addEventListener("submit", event => event.preventDefault());
  form.addEventListener("reset", () => {
    requestAnimationFrame(() => {
      update();
      query.focus();
    });
  });
  update();
}

function render(report) {
  renderSummary(report);
  renderSentimentChart(id("sentiment-chart"), report.counts);
  const products = [...report.by_product].sort((a, b) => b.negative - a.negative || a.product.localeCompare(b.product));
  renderProductChart(id("product-chart"), products);
  const mostNegative = products[0];
  if (mostNegative?.negative) {
    const total = labels.reduce((sum, label) => sum + mostNegative[label], 0);
    id("product-insight").textContent =
      mostNegative.negative + " of " + total + " reviews for " + mostNegative.product + " were classified as negative.";
  } else {
    id("product-insight").textContent = "No reviews were classified as negative.";
  }

  const months = report.monthly;
  renderMonthlyChart(id("monthly-chart"), months);
  const peak = months.reduce((best, row) => row.negative > best.negative ? row : best);
  id("trend-insight").textContent = peak.negative
    ? monthName(peak.month) + " had " + peak.negative + " negative reviews, the most in the sample."
    : "No negative reviews across the months shown.";
  for (const row of months) {
    id("months").tBodies[0].append(tableRow([monthName(row.month), ...labels.map(label => row[label])]));
  }
  const first = monthName(months[0].month);
  const last = monthName(months.at(-1).month);
  id("period").textContent = first === last ? first : first + " – " + last;

  renderQuotes(report, "positive");
  renderQuotes(report, "negative");
  renderEvaluation(report);
  renderReviews(report);
  id("model-link").textContent = report.model.split("/").at(-1);
  id("generated").textContent = "Generated " + new Intl.DateTimeFormat("en", {
    dateStyle: "long", timeZone: "UTC",
  }).format(new Date(report.generated_at)) + " (UTC)";
}

try {
  const response = await fetch("data/report.json");
  if (!response.ok) throw new Error("Report request returned " + response.status);
  render(await response.json());
  id("report").hidden = false;
} catch {
  id("load-error").textContent = "The report could not be loaded. Refresh the page to try again.";
} finally {
  id("loading").hidden = true;
}
