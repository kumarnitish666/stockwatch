"""
Generate one-sentence stock stories from numeric signals.

Pure function: takes the same fields the API already computes, returns
a short English description. No external calls, no DB, no side effects.
This makes it trivially testable and reusable.
"""


def generate_story(
    position_52w_pct: float | None,
    change_7d_pct: float | None,
    change_30d_pct: float | None,
) -> str:
    """
    Pick the most meaningful one-sentence description for this stock.

    Rules are checked in priority order. The first match wins, so the
    most "interesting" patterns come first.
    """
    # Guard: if we don't have enough data, say so honestly
    if position_52w_pct is None:
        return "Not enough data yet."

    pos = position_52w_pct
    d7 = change_7d_pct
    d30 = change_30d_pct

    # 1. Near extremes — these dominate any other signal
    if pos < 15:
        return "Trading near 52-week low."
    if pos > 85:
        return "Trading near 52-week high."

    # 2. Divergence: bouncing this week after a bad month
    if d7 is not None and d30 is not None and d7 > 2 and d30 < -5:
        return "Bouncing this week, but still down for the month."

    # 3. Strong rally or sharp dip
    if d7 is not None and d30 is not None:
        if d7 > 3 and d30 > 5:
            return "Up sharply this week and month."
        if d7 < -3 and d30 < -5:
            return "Down sharply this week and month."

    # 4. Quiet/stagnant
    if (d7 is None or abs(d7) < 1.5) and (d30 is None or abs(d30) < 2):
        return "Quiet month — minimal movement."

    # 5. Default fallback
    return "Trading mid-range — mixed signals."


if __name__ == "__main__":
    # Quick smoke test — run this file directly to verify the rules
    test_cases = [
        # (label, pos_52w, change_7d, change_30d, expected_keyword)
        ("Near low", 9.6, -1.30, -6.33, "low"),
        ("Near high", 92.0, 1.0, 3.0, "high"),
        ("Rally", 60.0, 4.5, 8.0, "Up sharply"),
        ("Sharp dip", 50.0, -4.0, -7.0, "Down sharply"),
        ("Bouncing", 30.0, 3.5, -6.0, "Bouncing"),
        ("Flat", 50.0, 0.5, 1.0, "Quiet"),
        ("Mid mixed", 50.0, 2.0, -3.0, "mid-range"),
        ("Insufficient", None, None, None, "Not enough"),
    ]
    print("Story rules smoke test:\n")
    for label, pos, d7, d30, expected in test_cases:
        story = generate_story(pos, d7, d30)
        ok = "✅" if expected.lower() in story.lower() else "❌"
        print(f"  {ok}  {label:18s} → {story}")