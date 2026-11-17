export const labels = ["positive", "neutral", "negative"];

const svgNS = "http://www.w3.org/2000/svg";
const monthFormat = new Intl.DateTimeFormat("en", { month: "short", timeZone: "UTC" });
const titleCase = value => value[0].toUpperCase() + value.slice(1);

function svgElement(tag, attrs = {}, text = "") {
  const node = document.createElementNS(svgNS, tag);
  for (const [key, value] of Object.entries(attrs)) node.setAttribute(key, value);
  if (text) node.textContent = text;
  return node;
}

function barRow(name, segments, maximum, description) {
  const row = document.createElement("div");
  row.className = "bar-row";
  const label = document.createElement("span");
  label.className = "bar-label";
  label.textContent = name;
  const bar = svgElement("svg", {
    viewBox: "0 0 " + maximum + " 14",
    preserveAspectRatio: "none",
    role: "img",
    "aria-label": description,
  });
  bar.append(svgElement("rect", { width: maximum, height: 14, class: "bar-track" }));
  let start = 0;
  for (const [sentiment, count] of segments) {
    if (count) bar.append(svgElement("rect", {
      x: start, width: count, height: 14, class: "bar " + sentiment,
    }));
    start += count;
  }
  const count = document.createElement("span");
  count.className = "bar-total";
  count.textContent = start;
  count.setAttribute("aria-hidden", "true");
  row.append(label, bar, count);
  return row;
}

export function renderSentimentChart(container, counts) {
  const max = Math.max(1, ...Object.values(counts));
  for (const label of labels) {
    const row = barRow(titleCase(label), [[label, counts[label]]], max, counts[label] + " reviews");
    container.append(row);
  }
}

export function renderProductChart(container, products) {
  const max = Math.max(1, ...products.map(row => labels.reduce((total, label) => total + row[label], 0)));
  for (const row of products) {
    const segments = labels.map(label => [label, row[label]]);
    const description = segments.map(([label, value]) => value + " " + label).join(", ");
    const bar = barRow(row.product, segments, max, description);
    const breakdown = document.createElement("span");
    breakdown.className = "bar-breakdown";
    breakdown.setAttribute("aria-hidden", "true");
    for (const [label, value] of segments) {
      const valueNode = document.createElement("span");
      valueNode.className = label;
      valueNode.textContent = value;
      breakdown.append(valueNode);
    }
    bar.append(breakdown);
    container.append(bar);
  }
}

export function renderMonthlyChart(container, rows) {
  const width = 416;
  const height = 192;
  const left = 38;
  const right = width - 30;
  const top = 18;
  const bottom = height - 32;
  const largestCount = Math.max(1, ...rows.flatMap(row => labels.map(label => row[label])));
  const step = Math.max(1, Math.ceil(largestCount / 4));
  const max = Math.ceil(largestCount / step) * step;
  const x = index => rows.length === 1 ? (left + right) / 2 : left + index * (right - left) / (rows.length - 1);
  const y = count => bottom - count * (bottom - top) / max;
  const chart = svgElement("svg", {
    viewBox: "0 0 " + width + " " + height,
    role: "img",
    "aria-label": "Monthly review counts by sentiment. Exact counts are available below.",
  });
  for (let count = 0; count <= max; count += step) {
    const rowY = y(count);
    chart.append(
      svgElement("line", { x1: left, y1: rowY, x2: right, y2: rowY, class: "grid-line" }),
      svgElement("text", { x: left - 8, y: rowY + 4, "text-anchor": "end" }, count.toString()),
    );
  }
  const labelEvery = Math.ceil(rows.length / 6);
  rows.forEach((row, index) => {
    if (index % labelEvery !== 0) return;
    const month = monthFormat.format(new Date(row.month + "-01T00:00:00Z"));
    const label = rows.length > 12 ? row.month : month;
    chart.append(svgElement("text", { x: x(index), y: height - 8, "text-anchor": "middle" }, label));
  });
  for (const sentiment of labels) {
    const points = rows.map((row, index) => [x(index), y(row[sentiment])]);
    chart.append(svgElement("polyline", {
      points: points.map(point => point.join(",")).join(" "),
      class: "series " + sentiment,
    }));
    points.forEach(([cx, cy]) => chart.append(svgElement("circle", {
      cx, cy, r: 3, class: "point " + sentiment,
    })));
  }
  container.append(chart);
}
