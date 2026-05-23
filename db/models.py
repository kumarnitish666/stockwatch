"""
Database models for StockWatch.

Defines the tables (Stock, Price) as Python classes using SQLAlchemy ORM.
Each class corresponds to a table; each class attribute corresponds to a column.
"""
from datetime import datetime, date
from sqlalchemy import String, Float, DateTime, Date, ForeignKey, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Base class all our models inherit from. SQLAlchemy convention."""
    pass


class Stock(Base):
    __tablename__ = "stocks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ticker: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    added_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationship: one Stock has many Prices
    prices: Mapped[list["Price"]] = relationship(back_populates="stock", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Stock {self.ticker} ({self.name})>"


class Price(Base):
    __tablename__ = "prices"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    stock_id: Mapped[int] = mapped_column(ForeignKey("stocks.id"), nullable=False)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    close_price: Mapped[float] = mapped_column(Float, nullable=False)

    # Reverse of the relationship above
    stock: Mapped["Stock"] = relationship(back_populates="prices")

    def __repr__(self) -> str:
        return f"<Price {self.stock.ticker if self.stock else '?'} {self.date}: {self.close_price}>"