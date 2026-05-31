"""
Daily update: fetch the latest prices for each stock and append to the database.

Runs once a day via Render Cron. Idempotent — running it twice in one day
does nothing on the second run because save_prices() deduplicates by date.
"""
import yfinance as yf
from datetime import datetime, timezone

from db.session import get_session, init_db
from db.operations import list_stocks, save_prices


def fetch_recent_prices(ticker: str, days_back: int = 5) -> list[dict]:
    """
    Fetch the last few days of prices for a ticker.
    Asks for more than 1 day so we catch weekends/holidays.
    """
    history = yf.Ticker(ticker).history(period=f"{days_back}d", auto_adjust=True)
    if history.empty:
        return []
    return [
        {"date": idx.date(), "close_price": float(row["Close"])}
        for idx, row in history.iterrows()
    ]


def update_one_stock(session, stock) -> int:
    """Update one stock's prices. Returns number of new rows inserted."""
    print(f"Updating {stock.ticker}...", end=" ")
    rows = fetch_recent_prices(stock.ticker, days_back=5)
    if not rows:
        print("no data from yfinance")
        return 0
    inserted = save_prices(session, stock_id=stock.id, price_rows=rows)
    print(f"{inserted} new row(s) inserted")
    return inserted


def main():
    init_db()
    session = get_session()
    total_inserted = 0
    try:
        stocks = list_stocks(session)
        if not stocks:
            print("Watchlist is empty. Run backfill.py first.")
            return
        print(f"Daily update started at {datetime.now(timezone.utc).isoformat()}")
        print(f"Updating {len(stocks)} stocks...\n")
        for stock in stocks:
            total_inserted += update_one_stock(session, stock)
        print(f"\nDaily update complete. {total_inserted} new row(s) added.")
    finally:
        session.close()


if __name__ == "__main__":
    main()