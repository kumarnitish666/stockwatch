# StockWatch — Product Requirements

## Problem
Retail investors watch 10-30 stocks but no consumer app surfaces multi-day pattern signals — "this is down 5 days in a row" or "near 52-week high." You have to manually click into each ticker, check the chart, eyeball trends. Slow, repetitive, easy to miss.

## Target user
Indian retail investor who maintains a watchlist of 10-30 stocks (NSE/BSE listed) and wants alerts for multi-day patterns, not just point-in-time prices.

## Core user journey
1. User adds tickers to watchlist (e.g. RELIANCE.NS, TCS.NS, INFY.NS)
2. System silently fetches daily closing prices and stores history
3. Daily, system computes patterns: "down N days", "% change over X days", "near 52-week high/low"
4. When a configured alert condition fires, an alert is logged (console for v1, email later)
5. Dashboard shows watchlist + current streaks + recent alerts

## Must-have features for v1
- Add/remove stocks from a watchlist
- Daily price fetch + storage (background job)
- Pattern detection: near 52-week high/low, X-day % change
- Configurable thresholds per stock (or global default)
- Alert log + console output when triggered

## Success metric
I (the builder) use this dashboard before opening any actual trading app for two weeks.