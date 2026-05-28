"""
FastAPI application for StockWatch.

Exposes the watchlist and price data over HTTP.
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

from db.session import get_session, init_db
from db.operations import list_stocks, get_stock_by_ticker, get_recent_prices
from data.yfinance_source import get_watchlist_summary

from pathlib import Path
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Runs once when the API starts. Make sure the database schema exists."""
    init_db()
    yield
    # Anything after yield runs on shutdown (nothing for now)


app = FastAPI(
    title="StockWatch API",
    description="Watchlist with 52-week extremes and X-day percent changes.",
    version="0.1.0",
    lifespan=lifespan,
)


def db_session():
    """Dependency that yields a session per request and closes it after."""
    session = get_session()
    try:
        yield session
    finally:
        session.close()


@app.get("/api/health")
def health():
    """Health check. Confirms the API is alive."""
    return {"status": "ok", "service": "StockWatch", "version": "0.1.0"}

@app.get("/api/stocks")
def get_stocks(session: Session = Depends(db_session)):
    """List all stocks in the watchlist."""
    stocks = list_stocks(session)
    return [
        {"id": s.id, "ticker": s.ticker, "name": s.name}
        for s in stocks
    ]


@app.get("/api/summary")
def get_summary(session: Session = Depends(db_session)):
    """
    Live watchlist summary with 52-week position and recent percent changes.

    Pulls fresh data from yfinance for each stock and computes patterns.
    """
    stocks = list_stocks(session)
    if not stocks:
        return []

    tickers = [s.ticker for s in stocks]
    summary_df = get_watchlist_summary(tickers)

    # Build response: ticker -> name mapping for friendly output
    name_by_ticker = {s.ticker: s.name for s in stocks}

    rows = []
    for ticker, row in summary_df.iterrows():
        rows.append({
            "ticker": ticker,
            "name": name_by_ticker.get(ticker, ticker),
            "current_price": float(row["current_price"]),
            "high_52w": float(row["high_52w"]),
            "low_52w": float(row["low_52w"]),
            "position_52w_pct": float(row["position_52w_pct"]),
            "change_7d_pct": float(row["change_7d_pct"]) if row["change_7d_pct"] is not None else None,
            "change_30d_pct": float(row["change_30d_pct"]) if row["change_30d_pct"] is not None else None,
        })
    return rows


@app.get("/api/stocks/{ticker}/history")
def get_history(
    ticker: str,
    days: int = 30,
    session: Session = Depends(db_session),
):
    """
    Get the last N days of stored prices for a stock.

    Uses the database (no live fetch). Returns 404 if the ticker is not in watchlist.
    """
    stock = get_stock_by_ticker(session, ticker)
    if not stock:
        raise HTTPException(status_code=404, detail=f"Ticker '{ticker}' not in watchlist")

    prices = get_recent_prices(session, stock.id, days=days)
    return {
        "ticker": stock.ticker,
        "name": stock.name,
        "history": [
            {"date": p.date.isoformat(), "close_price": p.close_price}
            for p in prices
        ],
    }

PROJECT_ROOT = Path(__file__).resolve().parent.parent
STATIC_DIR = PROJECT_ROOT / "static"


@app.get("/")
def index():
    """Serve the dashboard HTML."""
    return FileResponse(STATIC_DIR / "index.html")

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")