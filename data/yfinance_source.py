"""
Data source module for fetching stock data from Yahoo Finance via yfinance.

Exposes one main function: get_watchlist_summary(tickers).
"""
import yfinance as yf
import pandas as pd


def get_watchlist_summary(tickers: list[str], period: str = "1y") -> pd.DataFrame:
    """
    Fetch price data for a list of tickers and compute a summary table.

    For each ticker, returns:
      - current price (latest close)
      - 52-week high and low (within the given period)
      - 52-week position (0-100% along the range)
      - 7-day percent change
      - 30-day percent change

    Args:
        tickers: list of yfinance-compatible tickers, e.g. ["RELIANCE.NS", "TCS.NS"]
        period: how far back to fetch. Default "1y" for 52-week computations.

    Returns:
        pandas DataFrame indexed by ticker, one row per stock.
    """
    if not tickers:
        return pd.DataFrame()

    # Bulk fetch
    data = yf.download(tickers, period=period, auto_adjust=True, progress=False)

    if data.empty:
        return pd.DataFrame()

    # yfinance returns slightly different shape for single vs multi-ticker;
    # normalize so we always have a column-per-ticker frame.
    if len(tickers) == 1:
        close = data[["Close"]].rename(columns={"Close": tickers[0]})
    else:
        close = data["Close"]

    current = close.iloc[-1]
    high_52w = close.max()
    low_52w = close.min()
    position_pct = ((current - low_52w) / (high_52w - low_52w) * 100).round(1)

    # Need at least 31 rows for 30-day change. Guard against shorter history.
    change_7d = ((current - close.iloc[-8]) / close.iloc[-8] * 100).round(2) if len(close) >= 8 else None
    change_30d = ((current - close.iloc[-31]) / close.iloc[-31] * 100).round(2) if len(close) >= 31 else None

    summary = pd.DataFrame({
        "current_price": current.round(2),
        "high_52w": high_52w.round(2),
        "low_52w": low_52w.round(2),
        "position_52w_pct": position_pct,
        "change_7d_pct": change_7d,
        "change_30d_pct": change_30d,
    })

    return summary


if __name__ == "__main__":
    # Quick smoke test: run this file directly to see if it works
    tickers = ["RELIANCE.NS", "INDIGO.NS", "HINDUNILVR.NS", "ASIANPAINT.NS", "HDFCBANK.NS"]
    result = get_watchlist_summary(tickers)
    print(result)