// Find the table body, status text, and refresh button
const tbody = document.getElementById("watchlist-body");
const statusEl = document.getElementById("status");
const refreshBtn = document.getElementById("refresh-btn");

// Format Indian rupees like "₹1,336.40"
function formatINR(n) {
  return new Intl.NumberFormat("en-IN", { maximumFractionDigits: 2 }).format(n);
}

// Color class based on whether the % change is positive, negative, or null
function pctClass(value) {
  if (value === null || value === undefined) return "text-slate-400";
  return value >= 0 ? "text-green-600" : "text-red-600";
}

// Format a percent like "+3.44%" or "-7.06%" with a sign
function pctText(value) {
  if (value === null || value === undefined) return "—";
  const sign = value >= 0 ? "+" : "";
  return `${sign}${value.toFixed(2)}%`;
}

// A tiny visual bar showing where current price sits in the 52-week range
function positionBar(pct) {
  const clamped = Math.max(0, Math.min(100, pct));
  const color = pct < 25 ? "bg-red-500" : pct > 75 ? "bg-green-500" : "bg-slate-400";
  return `
    <div class="flex items-center gap-2 justify-end">
      <span class="text-slate-600 w-12 text-right">${pct.toFixed(1)}%</span>
      <div class="w-20 h-1.5 bg-slate-200 rounded overflow-hidden">
        <div class="h-full ${color}" style="width: ${clamped}%"></div>
      </div>
    </div>
  `;
}

// Build one table row from a stock object
function buildRow(stock) {
  return `
    <tr class="hover:bg-slate-50">
      <td class="px-4 py-3">
        <div class="font-medium">${stock.ticker}</div>
        <div class="text-slate-500 text-xs">${stock.name}</div>
        <div class="text-slate-600 text-xs mt-1 italic">${stock.story || ""}</div>
      </td>
      <td class="px-4 py-3 text-right font-medium">₹${formatINR(stock.current_price)}</td>
      <td class="px-4 py-3 text-right text-slate-500">₹${formatINR(stock.low_52w)}</td>
      <td class="px-4 py-3 text-right text-slate-500">₹${formatINR(stock.high_52w)}</td>
      <td class="px-4 py-3 text-right">${positionBar(stock.position_52w_pct)}</td>
      <td class="px-4 py-3 text-right ${pctClass(stock.change_7d_pct)}">${pctText(stock.change_7d_pct)}</td>
      <td class="px-4 py-3 text-right ${pctClass(stock.change_30d_pct)}">${pctText(stock.change_30d_pct)}</td>
    </tr>
  `;
}

// Main load function — separated so the Refresh button can call it
async function loadSummary() {
  statusEl.textContent = "Fetching latest data…";
  refreshBtn.disabled = true;
  refreshBtn.classList.add("opacity-50");

  try {
    const res = await fetch("/api/summary");
    if (!res.ok) throw new Error(`API returned ${res.status}`);
    const stocks = await res.json();

    if (stocks.length === 0) {
      tbody.innerHTML = `<tr><td colspan="7" class="text-center text-slate-400 py-8">Watchlist is empty.</td></tr>`;
    } else {
      tbody.innerHTML = stocks.map(buildRow).join("");
    }

    statusEl.textContent = `Last refreshed: ${new Date().toLocaleString("en-IN")}`;
  } catch (err) {
    tbody.innerHTML = `<tr><td colspan="7" class="text-center text-red-500 py-8">Failed to load: ${err.message}</td></tr>`;
    statusEl.textContent = "";
  } finally {
    refreshBtn.disabled = false;
    refreshBtn.classList.remove("opacity-50");
  }
}

// Wire the refresh button
refreshBtn.addEventListener("click", loadSummary);

// First load on page load
loadSummary();