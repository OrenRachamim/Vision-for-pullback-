"""
find_buy_signals.py - מוצא בהיסטוריה איתותי קנייה משולבים: איתות שבועי "דורך" את המניה,
ואחריו (באותו יום או עד arm_days ימי מסחר) איתות יומי מפעיל קנייה.
לכל איתות מצייר גרף יומי ביום הקנייה + גרף שבועי ביום האיתות השבועי, אחד מעל השני.

הרצה:
    python find_buy_signals.py AAPL MSFT NVDA
    python find_buy_signals.py --universe universes/sp500.txt universes/sp400.txt --max 10
תוצרים: buy_signals/buy_signals.csv ו-buy_signals/<TICKER>_<DATE>.png
"""
import argparse
import os
from concurrent.futures import ProcessPoolExecutor

import matplotlib
matplotlib.use("Agg")
import pandas as pd

import backtest as bt


def find(ticker, start, end, cache_dir, arm_days):
    df = bt.load_history(ticker, cache_dir)
    hits = bt.scan_history(df, start, end)
    return ticker, bt.combo_signals(df, hits, arm_days), df


def main(argv=None):
    ap = argparse.ArgumentParser(description="Find weekly-then-daily combined buy signals")
    ap.add_argument("tickers", nargs="*")
    ap.add_argument("--universe", nargs="+", default=[])
    ap.add_argument("--start", default="2016-01-01")
    ap.add_argument("--end", default=None)
    ap.add_argument("--arm-days", type=int, default=15,
                    help="trading days after the weekly signal in which a daily signal counts")
    ap.add_argument("--max-hold", type=int, default=10, help="time exit for the trade column")
    ap.add_argument("--target-r", type=float, default=2.0)
    ap.add_argument("--max", type=int, default=10, help="how many charts to draw (newest first)")
    ap.add_argument("--out", default="buy_signals")
    ap.add_argument("--cache-dir", default="data")
    ap.add_argument("--jobs", type=int, default=os.cpu_count() or 1)
    args = ap.parse_args(argv)
    tickers = [t.upper() for t in args.tickers]
    for path in args.universe:
        tickers += [ln.strip().upper() for ln in open(path, encoding="utf-8") if ln.strip()]
    tickers = list(dict.fromkeys(tickers)) or bt.DEFAULT_UNIVERSE
    os.makedirs(args.out, exist_ok=True)
    bt.prefetch(tickers, args.cache_dir)

    found = []
    with ProcessPoolExecutor(max_workers=max(1, args.jobs)) as ex:
        futs = [ex.submit(find, tk, args.start, args.end, args.cache_dir, args.arm_days)
                for tk in tickers]
        for fu in futs:
            try:
                tk, combos, df = fu.result()
            except Exception as e:
                print("error:", e)
                continue
            found += [(tk, c, df) for c in combos]

    rows = []
    for tk, c, df in found:
        t, d, w = c["t"], c["daily_hit"]["daily"], c["weekly_hit"]["weekly"]
        fwd = bt.forward_returns(df).iloc[t]
        tr = bt.simulate_trade(df, t, d["base_lo"], args.target_r, args.max_hold) or {}
        rows.append(dict(ticker=tk, date=df.index[t].date(),
                         weekly_date=df.index[c["weekly_hit"]["t"]].date(),
                         days_after_weekly=t - c["weekly_hit"]["t"], close=df["Close"].iloc[t],
                         daily_score=int(d["score"]), weekly_score=int(w["score"]),
                         entry=d["base_hi"], stop=d["base_lo"],
                         fwd5=fwd["fwd5"], fwd10=fwd["fwd10"], fwd20=fwd["fwd20"],
                         trade_R=tr.get("R"), exit_reason=tr.get("exit_reason")))
    table = pd.DataFrame(rows).sort_values("date", ascending=False) if rows else pd.DataFrame()
    table.to_csv(os.path.join(args.out, "buy_signals.csv"), index=False)
    print(f"{len(table)} combined buy signals (weekly, then daily within {args.arm_days} days)")
    if len(table):
        print(table.head(args.max).to_string(index=False))
    by_key = {(tk, df.index[c["t"]].date()): (tk, c, df) for tk, c, df in found}
    for _, r in table.head(args.max).iterrows():
        tk, c, df = by_key[(r["ticker"], r["date"])]
        path = os.path.join(args.out, f"{tk}_{r['date']}.png")
        bt.stacked_chart(df, c["daily_hit"], c["weekly_hit"], tk, path)
        print("chart:", path)


if __name__ == "__main__":
    main()
