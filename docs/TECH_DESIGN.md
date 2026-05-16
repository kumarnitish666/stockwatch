# StockWatch — Technical Design

## Architecture
Python backend with FastAPI exposing REST endpoints. A data module (`data/yfinance_source.py`) fetches prices via the yfinance library. SQLite + SQLAlchemy stores stocks, prices (time-series), and alerts. A pattern module computes 52-week extremes and X-day % changes. APScheduler runs a daily job: fetch latest prices, recompute patterns, fire alerts. A vanilla HTML+JS frontend calls the API. Deployed on Railway or Render.

## Components
- `data/yfinance_source.py` — fetch prices from yfinance
- `data/moneycontrol_scraper.py` — Sunday stretch, scrapes news/peer info
- `db/` — SQLAlchemy models (stocks, prices, alerts, watch_config)
- `patterns/` — pattern detection logic
- `api/` — FastAPI routes
- `static/` — HTML + JS frontend
- `scheduler/` — daily background job

## Data model
- stocks (id, ticker, name, added_at)
- prices (id, stock_id, date, close_price, volume)
- watch_config (id, stock_id, pattern_type, threshold)
- alerts (id, stock_id, pattern_type, triggered_at, value)

## Key decisions
- yfinance over Moneycontrol scraping: right tool, free, works on any network, gives history in one call.
- SQLite for v1: zero setup, sufficient for one user. Switch to Postgres on deploy if writes are needed.
- Closing prices only for v1: drastically simpler and matches the pattern-detection use case.
- FastAPI: modern, async-friendly, auto-generates docs.
- Vanilla JS over React: one new thing at a time.