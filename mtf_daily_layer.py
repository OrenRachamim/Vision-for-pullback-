"""
mtf_daily_layer.py - בדיקת השכבה היומית לבד על 10 שנים: מה קורה אחרי שהמחיר נסגר לראשונה מעל
ממוצעים נעים מתכנסים (SMA 10..200)? תשואה מפתיחת מחר ל-1/3/5/10/20 ימים, מול ימים אקראיים במגמה
עולה (מעל SMA200) ומול כל הימים, באותן מניות. גם: כמה איתותים ביום, וכמה מניות "חמושות" בממוצע.

הרצה:  python mtf_daily_layer.py --out results_mtf
"""
import argparse
import os
from concurrent.futures import ProcessPoolExecutor

import numpy as np
import pandas as pd

import backtest as bt
import mtf_strategy as ms

H = (1, 3, 5, 10, 20)


def run(args):
    tk, start, spread, hold = args
    try:
        d = bt.load_history(tk)
    except Exception:  # noqa: BLE001
        return None
    if len(d) < 300:
        return None
    ds = ms.daily_signals(d, dict(ms.P, D_SPREAD=spread, D_HOLD=hold))
    o, c = d["Open"].values, d["Close"].values
    sma200 = d["Close"].rolling(200).mean().values
    lo = d.index.searchsorted(pd.Timestamp(start))
    n = len(d)
    fw = {}
    for h in H:                                   # fw[h][t] = סגירה ב-t+h / פתיחה ב-t+1 - 1
        x = np.full(n, np.nan)
        x[:n - h] = c[h:] / np.r_[o[1:], np.nan][:n - h] - 1
        fw[h] = x
    sig = ds["signal"].values.copy()
    sig[:lo] = False
    up = (c > sma200)
    up[:lo] = False
    allv = np.zeros(n, bool)
    allv[lo:] = True
    out = {}
    for name, m in [("signal", sig), ("uptrend", up), ("all", allv)]:
        out[name] = pd.DataFrame({f"r{h}": fw[h][m] for h in H}).assign(date=d.index[m])
    return tk, out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--universe", nargs="+", default=["universes/sp500.txt", "universes/sp400.txt",
                                                      "universes/sp600.txt"])
    ap.add_argument("--start", default="2016-01-01")
    ap.add_argument("--out", default="results_mtf")
    ap.add_argument("--spreads", nargs="+", type=float, default=[0.03, 0.05, 0.08])
    ap.add_argument("--holds", nargs="+", type=int, default=[1])
    ap.add_argument("--name", default="daily_layer.md")
    args = ap.parse_args(argv)
    tk = list(dict.fromkeys(ln.strip().upper() for f in args.universe for ln in open(f) if ln.strip()))
    tk = [t for t in tk if os.path.exists(f"data/{t}.csv")]
    L = [f"# Daily layer alone - {len(tk)} stocks, {args.start} -> today", "",
         "Signal = first close above all of SMA10/20/50/100/150/200 (none in prior 20 days) after the MAs converged "
         "(max-min spread <= X of price in the last 10 days). Return = next open -> close after N days.", ""]
    for spread, hold in [(s, h) for s in args.spreads for h in args.holds]:
        res = {"signal": [], "uptrend": [], "all": []}
        with ProcessPoolExecutor(4) as ex:
            for r in ex.map(run, [(t, args.start, spread, hold) for t in tk], chunksize=16):
                if r:
                    for k, v in r[1].items():
                        res[k].append(v)
        res = {k: pd.concat(v) for k, v in res.items()}
        days = res["all"].date.nunique()
        per_day = res["signal"].groupby("date").size()
        L += [f"## convergence spread <= {spread:.0%}, wait {hold} day(s) above the MAs", "",
              f"signals: {len(res['signal']):,} ({len(res['signal']) / days:.1f} per trading day; "
              f"days with none: {1 - len(per_day) / days:.0%})", "",
              "| | n | " + " | ".join(f"avg {h}d" for h in H) + " | up after 5d | up after 20d |",
              "|---|---|" + "---|" * (len(H) + 2)]
        for name in ("signal", "uptrend", "all"):
            g = res[name]
            L.append(f"| {name} | {len(g):,} | " + " | ".join(f"{g[f'r{h}'].mean():+.2%}" for h in H)
                     + f" | {(g.r5 > 0).mean():.0%} | {(g.r20 > 0).mean():.0%} |")
        s, u = res["signal"], res["uptrend"]
        L += ["", f"signal - uptrend (20d): {s.r20.mean() - u.r20.mean():+.2%}; by year (20d avg, signal vs uptrend): "
              + ", ".join(f"{y}: {s[s.date.dt.year == y].r20.mean():+.1%}/{u[u.date.dt.year == y].r20.mean():+.1%}"
                          for y in sorted(s.date.dt.year.unique())), ""]
    text = "\n".join(L)
    os.makedirs(args.out, exist_ok=True)
    open(os.path.join(args.out, args.name), "w", encoding="utf-8").write(text + "\n")
    print(text)


if __name__ == "__main__":
    main()
