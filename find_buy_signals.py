"""
find_buy_signals.py - מוצא בהיסטוריה ימים שבהם גם הקריטריון היומי וגם השבועי מתקיימים
(BUY SIGNAL של הסורק), ומצייר לכל אחד גרף יומי + גרף שבועי של אותו יום, אחד מעל השני.

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
import matplotlib.pyplot as plt
import pandas as pd

import backtest as bt
import pullback_scanner as ps


def find(ticker, start, end, cache_dir):
    df = bt.load_history(ticker, cache_dir)
    hits = bt.scan_history(df, start, end)
    return ticker, [h for h in hits if h["daily"] and h["weekly"]], df


def draw(ticker, df, hit, out_dir, after=20):
    tmp = [os.path.join(out_dir, f"_{ticker}_{k}.png") for k in ("daily", "weekly")]
    bt.signal_chart(df, hit, "daily", ticker, tmp[0], after=after)
    bt.signal_chart(df, hit, "weekly", ticker, tmp[1], after=after)
    imgs = [plt.imread(p) for p in tmp]
    fig, axes = plt.subplots(2, 1, figsize=(12, 14))
    for ax, img in zip(axes, imgs):
        ax.imshow(img)
        ax.axis("off")
    fig.tight_layout()
    path = os.path.join(out_dir, f"{ticker}_{df.index[hit['t']].date()}.png")
    fig.savefig(path, dpi=100)
    plt.close(fig)
    for p in tmp:
        os.remove(p)
    return path


def main(argv=None):
    ap = argparse.ArgumentParser(description="Find days where daily AND weekly criteria both hold")
    ap.add_argument("tickers", nargs="*")
    ap.add_argument("--universe", nargs="+", default=[])
    ap.add_argument("--start", default="2016-01-01")
    ap.add_argument("--end", default=None)
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
        futs = [ex.submit(find, tk, args.start, args.end, args.cache_dir) for tk in tickers]
        for fu in futs:
            try:
                tk, hits, df = fu.result()
            except Exception as e:
                print("error:", e)
                continue
            found += [(tk, h, df) for h in hits]

    rows = []
    for tk, h, df in found:
        t, d, w = h["t"], h["daily"], h["weekly"]
        fwd = bt.forward_returns(df).iloc[t]
        tr = bt.simulate_trade(df, t, d["base_lo"]) or {}
        rows.append(dict(ticker=tk, date=df.index[t].date(), close=df["Close"].iloc[t],
                         daily_score=int(d["score"]), weekly_score=int(w["score"]),
                         daily_drop=d["drop"], weekly_drop=w["drop"],
                         entry=d["base_hi"], stop=d["base_lo"],
                         fwd20=fwd["fwd20"], fwd60=fwd["fwd60"],
                         trade_R=tr.get("R"), exit_reason=tr.get("exit_reason")))
    table = pd.DataFrame(rows).sort_values("date", ascending=False) if rows else pd.DataFrame()
    table.to_csv(os.path.join(args.out, "buy_signals.csv"), index=False)
    print(f"{len(table)} days with daily AND weekly signal")
    if len(table):
        print(table.head(args.max).to_string(index=False))
    by_key = {(tk, df.index[h["t"]].date()): (tk, h, df) for tk, h, df in found}
    for _, r in table.head(args.max).iterrows():
        tk, h, df = by_key[(r["ticker"], r["date"])]
        print("chart:", draw(tk, df, h, args.out))


if __name__ == "__main__":
    main()
