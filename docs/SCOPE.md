# StockWatch — Scope

## In for this weekend
- yfinance for price data (NSE/BSE via .NS/.BO suffixes)
- SQLite storage of historical prices
- Pattern detection: near 52-week high/low, X-day % change
- Daily background job: fetch + check patterns + log alerts
- Console alert when pattern triggers
- Minimal HTML+JS dashboard: watchlist, current prices, streaks
- Deployed live to Railway or Render

## Out (deferred)
- Real email/SMS notifications (console only for v1)
- Moneycontrol scraping for news/extras (Sunday stretch goal)
- User accounts / multi-user
- Intraday tracking (closing prices only for v1)
- Complex technical indicators (RSI, MACD, moving averages)
- Charts and graphs (numeric display only for v1)
- Mobile-responsive UI beyond "doesn't break"
- "Stock Story" — natural-language interpretation of the data per stock (e.g.,
  "Reliance dropped 7% this week and is near 52-week low"). Could be
  rule-based (cheap) or AI-generated (richer). Adds an insight layer on top
  of the raw numbers.