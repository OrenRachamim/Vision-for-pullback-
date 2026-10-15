"""
sr_followthrough.py - כמה פריצות יש ביום מסחר, וכמה מהמניות עולות לפחות X% מיד אחרי הפריצה.

לכל פריצה (מתוך signals.csv של sr_backtest.py): כניסה בפתיחה למחרת, ובודקים אם תוך N ימים
  * השיא (High) הגיע ל-+X% מהכניסה  ("touched")
  * או הסגירה של יום N מעל +X%        ("closed")
השוואה: ימים אקראיים שבהם המניה במגמה עולה (מעל SMA50 ו-SMA200), אותה מדידה.

הרצה:  python sr_followthrough.py results_sr_margin0.1_900 results_sr_margin0.1_600
"""
import sys

import numpy as np
import pandas as pd

import backtest as bt

HORIZONS = (1, 2, 3, 5)
LEVELS = (0.02, 0.03)


def measure(df, ts):
    """לכל t: כניסה בפתיחת t+1; מחזיר מערכים של max-high ו-close אחרי N ימים, ביחס לכניסה."""
    o, h, c = df["Open"].values, df["High"].values, df["Close"].values
    out = {}
    ts = np.asarray([t for t in ts if t + max(HORIZONS) < len(df)])
    e = o[ts + 1]
    for n in HORIZONS:
        mh = np.max([h[ts + k] for k in range(1, n + 1)], axis=0)
        out[f"hi{n}"] = mh / e - 1
        out[f"cl{n}"] = c[ts + n] / e - 1
    return pd.DataFrame(out)


def main(dirs):
    sig = pd.concat([pd.read_csv(f"{d}/signals.csv") for d in dirs])
    sig["date"] = pd.to_datetime(sig["date"])
    days = bt.load_history("SPY").loc["2016-01-01":].index
    per_day = sig.groupby("date").size().reindex(days, fill_value=0)
    print(f"# {', '.join(dirs)}")
    print(f"breakouts: {len(sig):,} on {sig.ticker.nunique():,} stocks | per trading day: "
          f"avg {per_day.mean():.1f}, median {per_day.median():.0f}, "
          f"days with none {(per_day == 0).mean():.0%}, days with 1-5 {per_day.between(1, 5).mean():.0%}, "
          f"days with >10 {(per_day > 10).mean():.0%}, max {per_day.max()} ({per_day.idxmax().date()})")

    rng = np.random.default_rng(0)
    res, base = [], []
    for tk, g in sig.groupby("ticker"):
        df = bt.load_history(tk)
        ts = df.index.get_indexer(g["date"])
        res.append(measure(df, ts[ts >= 0]))
        c = df["Close"]
        up = ((c > c.rolling(50).mean()) & (c > c.rolling(200).mean())).values
        lo = df.index.searchsorted(pd.Timestamp("2016-01-01"))
        cand = np.where(up[lo:len(df) - 6])[0] + lo
        if len(cand):
            base.append(measure(df, rng.choice(cand, min(len(cand), 60), replace=False)))
    r, b = pd.concat(res), pd.concat(base)
    rows = []
    for x in LEVELS:
        for n in HORIZONS:
            rows.append(dict(rise=f"+{x:.0%}", days=n,
                             breakout_touched=(r[f"hi{n}"] >= x).mean(), random_uptrend_touched=(b[f"hi{n}"] >= x).mean(),
                             breakout_closed=(r[f"cl{n}"] >= x).mean(), random_uptrend_closed=(b[f"cl{n}"] >= x).mean()))
    t = pd.DataFrame(rows)
    for col in t.columns[2:]:
        t[col] = (t[col] * 100).round(1).astype(str) + "%"
    print(t.to_string(index=False))
    print(f"(breakouts measured: {len(r):,}; random uptrend days: {len(b):,})\n")


if __name__ == "__main__":
    main(sys.argv[1:])
