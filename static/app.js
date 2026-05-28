// Find the table body element
const tbody = document.getElementById("watchlist-body");
const statusEl = document.getElementById("status");

// Format a percent number like "+3.44%" or "-7.06%"
function formatPct(value) {
  if (value === null || value === undefined) return "—";
  const sign = value >= 0 ? "+" : "";
  return sign + value.toFixed(2) + "%";
}

// Build one <tr> row from a stock object
function buildRow(stock) {
  return `
    <tr>
      <td>${stock.ticker}</td>
      <td>${stock.name}</td>
      <td>₹${stock.current_price.toFixed(2)}</td>
      <td>₹${stock.low_52w.toFixed(2)}</td>
      <td>₹${stock.high_52w.toFixed(2)}</td>
      <td>${stock.position_52w_pct.toFixed(1)}%</td>
      <td>${formatPct(stock.change_7d_pct)}</td>
      <td>${formatPct(stock.change_30d_pct)}</td>
    </tr>
  `;
}

// Main: fetch the summary and render the table
fetch("/api/summary")
  .then(response => response.json())
  .then(stocks => {
    tbody.innerHTML = stocks.map(buildRow).join("");
    statusEl.textContent = "Last refreshed: " + new Date().toLocaleString();
  })
  .catch(error => {
    tbody.innerHTML = `<tr><td colspan="8">Failed to load: ${error.message}</td></tr>`;
  });