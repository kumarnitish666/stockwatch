"""
Database operations for StockWatch.

High-level functions that the rest of the app uses to read and write data.
Anything that touches the database goes through here.
"""
from typing import Optional
from sqlalchemy import select, desc
from sqlalchemy.orm import Session

from db.models import Stock, Price


def add_stock(session: Session, ticker: str, name: str) -> Stock:
    """
    Add a stock to the watchlist. Idempotent — if it already exists, return it.
    """
    existing = session.execute(
        select(Stock).where(Stock.ticker == ticker)
    ).scalar_one_or_none()

    if existing:
        return existing

    stock = Stock(ticker=ticker, name=name)
    session.add(stock)
    session.commit()
    session.refresh(stock)
    return stock


def list_stocks(session: Session) -> list[Stock]:
    """Return all stocks in the watchlist, ordered by ticker."""
    return list(session.execute(select(Stock).order_by(Stock.ticker)).scalars())


def save_prices(session: Session, stock_id: int, price_rows: list[dict]) -> int:
    """
    Save many prices at once. Skips duplicates (same stock_id + date).

    Returns the number of new rows inserted.
    """
    existing_dates = set(session.execute(
        select(Price.date).where(Price.stock_id == stock_id)
    ).scalars())

    new_rows = [
        Price(stock_id=stock_id, date=row["date"], close_price=row["close_price"])
        for row in price_rows
        if row["date"] not in existing_dates
    ]

    if not new_rows:
        return 0

    session.add_all(new_rows)
    session.commit()
    return len(new_rows)


def get_recent_prices(session: Session, stock_id: int, days: int = 30) -> list[Price]:
    """
    Fetch the most recent N prices for a stock, newest first.
    """
    return list(session.execute(
        select(Price)
        .where(Price.stock_id == stock_id)
        .order_by(desc(Price.date))
        .limit(days)
    ).scalars())


def get_stock_by_ticker(session: Session, ticker: str) -> Optional[Stock]:
    """Look up a stock by ticker. Returns None if not found."""
    return session.execute(
        select(Stock).where(Stock.ticker == ticker)
    ).scalar_one_or_none()