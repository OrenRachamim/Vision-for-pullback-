"""
index_control.py - בדיקות חוסן לאיתות מניה + מדד (backtest.py --index-combo):
  1. CONTROL "מדד דרוך": כניסה אקראית רק בימים שבהם המדד של המניה באיתות (אותו חלון ואותו ביטול),
     עם אותן יציאות. אם האיתות לא טוב ממנו - כל היתרון הוא תזמון של המדד, לא הדפוס במניה.
  2. מובהקות עם קיבוץ לפי תאריך: עסקאות שנפתחות באותו יום תלויות זו בזו, ולכן bootstrap על
     תאריכים (ולא על עסקאות בודדות) נותן רווח סמך אמיתי יותר.

הרצה (אחרי backtest.py --index-combo ... --out DIR):
    python index_control.py DIR --universe universes/sp600.txt --index-combo market --trail-atr 3 --max-hold 60
"""
import argparse
import os

import numpy as np
import pandas as pd

import backtest as bt


def armed_days(idf, ihits, window):
    """מערך bool לפי תאריכי המדד: המדד באיתות (עד window ימים אחרי איתות, ולא נסגר מתחת ל-base_lo)."""
    armed = np.zeros(len(idf), bool)
    close = idf["Close"].values
    for h in ihits:
        if not h["daily"]:
            continue
        lo = h["daily"]["base_lo"]
        for k in range(h["t"], min(h["t"] + window + 1, len(idf))):
            if close[h["t"]:k + 1].min() < lo:
                break
            armed[k] = True
    return armed


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("results_dir")
    ap.add_argument("--universe", nargs="+", required=True)
    ap.add_argument("--index-combo", choices=["market", "sector"], required=True)
    ap.add_argument("--index-window", type=int, default=5)
    ap.add_argument("--trail-atr", type=float, default=None)
    ap.add_argument("--max-hold", type=int, default=20)
    ap.add_argument("--target-r", type=float, default=2.0)
    ap.add_argument("--start", default="2016-01-01")
    ap.add_argument("--end", default=None)
    ap.add_argument("--stride", type=int, default=2)
    ap.add_argument("--cache-dir", default="data")
    args = ap.parse_args(argv)
    bt.use_scanner("pullback_scanner")

    sig = pd.read_csv(os.path.join(args.results_dir, "signals.csv"))
    combo = sig[(sig.kind == "combo") & (sig.exit_reason != "open")]
    daily = sig[(sig.kind == "daily") & (sig.exit_reason != "open")]
    risks = combo["risk_pct"].dropna().values
    rng = np.random.default_rng(0)

    tickers = [ln.strip().upper() for p in args.universe for ln in open(p) if ln.strip()]
    armed_cache, ctrl = {}, []
    for tk in tickers:
        etf = bt.index_for(tk, args.index_combo)
        path = os.path.join(args.cache_dir, f"{tk}.csv")
        if not etf or not os.path.exists(path):
            continue
        if etf not in armed_cache:
            idf, ihits = bt.index_hits(etf, args)
            armed_cache[etf] = pd.Series(armed_days(idf, ihits, args.index_window), index=idf.index)
        df = bt.load_history(tk, args.cache_dir)
        if len(df) < bt.DAILY_WARMUP + 2:
            continue
        arm = armed_cache[etf].reindex(df.index, fill_value=False).values
        lo = bt.bt_lo(df, args.start)
        hi = df.index.searchsorted(pd.Timestamp(args.end), side="right") if args.end else len(df)
        atr = bt.atr14(df) if args.trail_atr else None
        o = df["Open"].values
        for t in np.where(arm[lo:hi - 1])[0][::args.stride] + lo:
            r = bt.simulate_trade(df, t, o[t + 1] * (1 - rng.choice(risks)), args.target_r,
                                  args.max_hold, args.trail_atr, atr)
            if r and r["exit_reason"] != "open":
                ctrl.append(r["R"])
    ctrl = np.array([x for x in ctrl if x == x])

    def by_date_ci(g, n=4000):
        per = g.groupby("date")["R"].agg(["sum", "count"])
        s, c = per["sum"].values, per["count"].values
        idx = rng.integers(0, len(per), (n, len(per)))
        boots = s[idx].sum(1) / c[idx].sum(1)
        return len(per), np.percentile(boots, 2.5), np.percentile(boots, 97.5)

    print(f"results: {args.results_dir}  ({args.index_combo}, window {args.index_window},"
          f" exit {'trail ' + str(args.trail_atr) + 'xATR' if args.trail_atr else str(args.target_r) + 'R'}"
          f" / {args.max_hold}d)")
    print(f"  CONTROL index-armed days: n={len(ctrl):,}  avg_R={ctrl.mean():+.3f}")
    for name, g in (("stock+index", combo), ("stock alone", daily)):
        nd, lo_, hi_ = by_date_ci(g)
        print(f"  {name:12s} n={len(g):5d} on {nd:4d} dates  avg_R={g.R.mean():+.3f}"
              f"  date-clustered 95% CI [{lo_:+.3f}, {hi_:+.3f}]"
              f"  vs index-armed control {g.R.mean() - ctrl.mean():+.3f}R")


if __name__ == "__main__":
    main()
