# StockWatch

A weekend project to track multi-day patterns in a stock watchlist — 52-week highs/lows, X-day % changes — and alert when conditions hit.

See `docs/` for the PRD, scope, and technical design.

## Stack
- Python + FastAPI
- yfinance (price data)
- SQLite + SQLAlchemy
- APScheduler (daily jobs)
- Vanilla HTML + JS frontend
- Deployed on Railway / Render