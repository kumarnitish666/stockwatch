"""
Backfill script: fetch one year of history for the watchlist and store it.

Run once to populate the database. After that, the daily scheduler picks up from here.
"""
import yfinance as yf

from db.session import get_session, init_db
from db.operations import add_stock, save_prices


WATCHLIST = {
    "RELIANCE.NS": "Reliance Industries",
    "INDIGO.NS": "InterGlobe Aviation",
    "HINDUNILVR.NS": "Hindustan Unilever",
    "ASIANPAINT.NS": "Asian Paints",
    "HDFCBANK.NS": "HDFC Bank",
}


def backfill_one_stock(session, ticker: str, name: str) -> None:
    """Fetch a year of prices for one ticker and store them."""
    stock = add_stock(session, ticker=ticker, name=name)

    print(f"Fetching {ticker}...", end=" ")
    history = yf.Ticker(ticker).history(period="1y", auto_adjust=True)

    if history.empty:
        print("no data")
        return

    price_rows = [
        {"date": idx.date(), "close_price": float(row["Close"])}
        for idx, row in history.iterrows()
    ]

    inserted = save_prices(session, stock_id=stock.id, price_rows=price_rows)
    print(f"saved {inserted} new prices ({len(price_rows)} total in API response)")


def main():
    init_db()
    session = get_session()
    try:
        for ticker, name in WATCHLIST.items():
            backfill_one_stock(session, ticker, name)
        print("\nBackfill complete.")
    finally:
        session.close()


if __name__ == "__main__":
    main()