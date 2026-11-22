// The page shows the report of the dataset (data/sample_reviews.csv)
// and has a free field to classify one review or add it to the dataset.

const LABELS = ["positive", "neutral", "negative"];
const NO_SERVER = "Saved report. To classify reviews, start the server on this PC: python -m sentiment_analyzer.server";
// On GitHub Pages the model is not there, so the page talks to the server running on my PC.
const API = location.hostname.endsWith("github.io") ? "http://localhost:8000/" : "";
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

// A bar with three colored parts. Works with percentages or counts (flex-grow keeps the proportion).
function splitBar(values) {
  const bar = document.createElement("div");
  bar.className = "split";
  for (const label of LABELS) {
    const part = document.createElement("i");
    part.className = label;
    part.style.flexGrow = values[label];
    bar.append(part);
  }
  return bar;
}

// Draw the dataset report sent by the server (same shape as data/report.json).
function show(report) {
  current = report;

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

  // One bar split in three: the width of each part is its percentage.
  const legend = document.createElement("div");
  legend.className = "legend";
  for (const label of LABELS) {
    const item = document.createElement("span");
    item.className = label;
    item.textContent = label + " · " + report.counts[label];
    legend.append(item);
  }
  $("bars").replaceChildren(splitBar(report.percentages), legend);

  // Table by product (with a small bar per product), and the product list for the free field.
  const products = report.by_product.map((p) => p.product);
  fillTable($("products"), ["Product", "", "Positive", "Neutral", "Negative"],
    report.by_product.map((p) => [p.product, "", p.positive, p.neutral, p.negative]));
  for (const [i, p] of report.by_product.entries()) {
    $("products").rows[i + 1].cells[1].append(splitBar(p));
  }
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
  const response = await fetch(API + url, { method: "POST", body: JSON.stringify(data) });
  const answer = await response.json();
  if (!response.ok) throw new Error(answer.error);
  return answer;
}

// Without the Python server (e.g. GitHub Pages) the model cannot run.
function showNoServer() {
  $("status").textContent = NO_SERVER;
}

function showError(error) {
  if (error instanceof TypeError || error instanceof SyntaxError) showNoServer();
  else $("status").textContent = error.message;
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
fetch(API + "api/report")
  .then((response) => response.json())
  .then((report) => {
    $("status").textContent = "Connected: the model is running on this PC.";
    return report;
  })
  .catch(() => {
    showNoServer();
    return fetch("data/report.json").then((response) => response.json());
  })
  .then(show)
  .catch(showNoServer);
