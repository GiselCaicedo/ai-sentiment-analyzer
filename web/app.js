// The page shows the report of the dataset (data/sample_reviews.csv)
// and has a free field to classify one review or add it to the dataset.

const LABELS = ["positive", "neutral", "negative"];
const NO_SERVER = "Start the server first: python -m sentiment_analyzer.server";
const $ = (id) => document.getElementById(id);
let current = null; // the report on screen, to show what changed after "Add to dataset"

// Build an HTML table from a header row and data rows (textContent avoids injecting HTML).
function fillTable(table, header, rows) {
  table.replaceChildren();
  for (const [i, values] of [header, ...rows].entries()) {
    const tr = table.insertRow();
    for (const value of values) {
      const cell = document.createElement(i === 0 ? "th" : "td");
      cell.textContent = value;
      tr.append(cell);
    }
  }
}

// Draw the dataset report sent by the server (same shape as data/report.json).
function show(report) {
  current = report;
  $("source").textContent = "Dataset: data/sample_reviews.csv · " + report.total + " reviews";

  // Number cards: total, % per sentiment, accuracy.
  const cards = [["Reviews", report.total, ""]];
  for (const label of LABELS) cards.push([label, report.percentages[label] + "%", label]);
  cards.push(["Accuracy", report.accuracy + "%", ""]);
  $("stats").replaceChildren();
  for (const [name, value, color] of cards) {
    const card = document.createElement("div");
    card.className = "stat " + color;
    card.innerHTML = "<strong></strong><span></span>";
    card.querySelector("strong").textContent = value;
    card.querySelector("span").textContent = name;
    $("stats").append(card);
  }

  // Bars: the width of each bar is its percentage.
  $("bars").replaceChildren();
  for (const label of LABELS) {
    const row = document.createElement("div");
    row.className = "bar " + label;
    row.innerHTML = "<span></span><div><i></i></div><b></b>";
    row.querySelector("span").textContent = label;
    row.querySelector("i").style.width = report.percentages[label] + "%";
    row.querySelector("b").textContent = report.counts[label];
    $("bars").append(row);
  }

  // Table by product, and the product list for the free field.
  const products = report.by_product.map((p) => p.product);
  fillTable($("products"), ["Product", "Positive", "Neutral", "Negative"],
    report.by_product.map((p) => [p.product, p.positive, p.neutral, p.negative]));
  $("product").replaceChildren(...products.map((name) => new Option(name)));

  // Every review with the model's answer, newest first.
  const rows = report.reviews.toReversed().map((r) => [
    r.review_text, r.product, r.sentiment, Math.round(r.confidence * 100) + "%",
  ]);
  fillTable($("table"), ["Review", "Product", "Sentiment", "Confidence"], rows);
  for (const tr of $("table").rows) tr.cells[2].className = tr.cells[2].textContent;

  // Download button: turns the Markdown text into a file.
  $("download").href = URL.createObjectURL(new Blob([report.markdown], { type: "text/markdown" }));
  $("results").hidden = false;
}

// Send JSON to the server and return its answer (or throw its error message).
async function post(url, data) {
  const response = await fetch(url, { method: "POST", body: JSON.stringify(data) });
  const answer = await response.json();
  if (!response.ok) throw new Error(answer.error);
  return answer;
}

function showError(error) {
  $("status").textContent = error instanceof TypeError || error instanceof SyntaxError
    ? NO_SERVER
    : error.message;
}

// "Classify": only ask the model about this one review.
$("form").addEventListener("submit", async (event) => {
  event.preventDefault();
  $("status").textContent = "Classifying…";
  try {
    const result = await post("api/classify", { text: $("review").value });
    $("status").innerHTML = "<b></b> · <span></span> confidence";
    $("status").querySelector("b").textContent = result.sentiment;
    $("status").querySelector("b").className = result.sentiment;
    $("status").querySelector("span").textContent = Math.round(result.confidence * 100) + "%";
  } catch (error) {
    showError(error);
  }
});

// "Add to dataset": save it in the CSV and redraw the whole report.
$("add").addEventListener("click", async () => {
  $("status").textContent = "Adding and re-analyzing the dataset…";
  try {
    const report = await post("api/add", { text: $("review").value, product: $("product").value });
    const label = report.reviews.at(-1).sentiment; // the new review is the last row
    const before = current.percentages[label];
    show(report);
    $("status").textContent = "Added as " + label + ". " + label + " " + before + "% → "
      + report.percentages[label] + "% (" + report.total + " reviews).";
    $("review").value = "";
  } catch (error) {
    showError(error);
  }
});

// On page load: the server analyzes the dataset in data/.
// Without a server (GitHub Pages) show the last saved report instead.
fetch("api/report")
  .then((response) => response.json())
  .catch(() => {
    $("status").textContent = NO_SERVER;
    return fetch("data/report.json").then((response) => response.json());
  })
  .then(show)
  .catch(() => ($("status").textContent = NO_SERVER));
