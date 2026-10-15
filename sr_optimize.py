"""
sr_optimize.py - חיפוש פרמטרים לאסטרטגיות sr_strategies על תקופת אימון בלבד, ובדיקה על נתונים שלא נראו.

  אימון   : S&P 500 + S&P 400 (900 מניות), 2016-2021  - כאן בוחרים פרמטרים.
  בדיקה 1 : אותן מניות, 2022 -> היום                   - תקופה שלא נראתה.
  בדיקה 2 : S&P 600 (600 מניות), 2016 -> היום           - מניות שלא נראו.
מדד הבחירה: Sharpe של התיק באימון (עם תנאי מינימום לעסקאות). מספר התצורות שנבדקו מדווח (ריבוי השוואות).

הרצה:  python sr_optimize.py --n 40 --out results_sr_opt
"""
import argparse
import itertools
import json
import os
from concurrent.futures import ProcessPoolExecutor

import numpy as np
import pandas as pd

import sr_strategies as S

TRAIN = ("2016-01-01", "2021-12-31")
TEST = ("2022-01-01", None)

COMMON = dict(hold=[2, 3, 5, 10], exit_sma5=[False, True], trend=["200", "200up", "50"])
GRIDS = dict(
    support_bounce=dict(near=[0.0, 0.25, 0.5], touches=[2, 3, 4], green=[False, True], rsi2=[0, 10, 30],
                        target=["res", "1.5", "3", "none"], stop_atr=[0.25, 0.5, 1.0], min_rr=[0, 1.5]),
    spring=dict(pierce=[0.0, 0.1, 0.3, 0.6], touches=[2, 3], green=[False, True],
                target=["res", "1.5", "3", "none"], stop_atr=[0.1, 0.3, 0.6]),
    break_retest=dict(near=[0.0, 0.25, 0.5], min_age=[1, 3], max_age=[10, 20], green=[False, True],
                      target=["hh", "res", "2", "none"], stop_atr=[0.25, 0.5, 1.0]),
    breakout=dict(vol=[0, 1.5, 2.0], target=["res", "2", "4", "none"], stop_atr=[0.25, 0.5, 1.0]),
    pivot=dict(level=["S1", "S2"], target=["P", "2", "none"], stop_atr=[0.5, 1.0, 2.0]),
    fib=dict(fib=[0.382, 0.5, 0.618], min_swing=[3, 5, 8], max_age=[10, 30], stop_fib=[0.786, 1.0],
             target=["hi", "2"]),
    ma_support=dict(ma=[20, 50], near=[0.0, 0.1, 0.3], target=["res", "2", "none"], stop_atr=[0.5, 1.0, 2.0]),
    nday_low=dict(rsi2=[0, 5, 10, 20], below_low=[False, True], at_support=[False, True],
                  stop_atr=[0, 2, 3]),
)


def configs(name, n, seed=0):
    grid = {**COMMON, **GRIDS[name]}
    keys = list(grid)
    allc = list(itertools.product(*grid.values()))
    rng = np.random.default_rng(seed)
    pick = rng.choice(len(allc), min(n, len(allc)), replace=False)
    out = []
    for i in pick:
        p = {k: (v.item() if hasattr(v, "item") else v) for k, v in zip(keys, allc[i])}
        if name == "nday_low" and not p["rsi2"] and not p["below_low"]:
            p["rsi2"] = 10
        out.append(p)
    return out


def universe(*paths):
    tk = [ln.strip().upper() for p in paths for ln in open(p) if ln.strip()]
    return [t for t in dict.fromkeys(tk) if os.path.exists(f"{S.sf.CACHE}/{t}.pkl")]


def evaluate(pool, tickers, name, p, periods, K):
    tr = S.trades(pool, tickers, name, p)
    out = {}
    for lab, (a, b) in periods.items():
        _, m, _ = S.portfolio(tr, tickers, a, b, K=K)
        sub = tr[(tr.entry >= a) & ((tr.entry <= b) if b else True)]
        m.update(all_trades=len(sub), all_avg=sub.ret.mean(), all_win=(sub.ret > 0).mean())
        out[lab] = m
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=40, help="configs per strategy (random search)")
    ap.add_argument("--K", type=int, default=10)
    ap.add_argument("--top", type=int, default=3)
    ap.add_argument("--strats", nargs="*", default=list(GRIDS))
    ap.add_argument("--out", default="results_sr_opt")
    args = ap.parse_args(argv)
    os.makedirs(args.out, exist_ok=True)
    u900 = universe("universes/sp500.txt", "universes/sp400.txt")
    u600 = universe("universes/sp600.txt")
    rows = []
    with ProcessPoolExecutor(4) as pool:
        for name in args.strats:
            for p in configs(name, args.n):
                r = evaluate(pool, u900, name, p, {"train": TRAIN}, args.K)["train"]
                rows.append(dict(strategy=name, params=json.dumps(p), **{f"tr_{k}": v for k, v in r.items()}))
                print(name, p, {k: round(float(v), 3) for k, v in r.items()}, flush=True)
            pd.DataFrame(rows).to_csv(os.path.join(args.out, "train_search.csv"), index=False)
        res = pd.DataFrame(rows)
        res = res[res.tr_trades >= 300]
        best = res.sort_values("tr_Sharpe", ascending=False).groupby("strategy").head(args.top)
        final = []
        for r in best.itertuples():
            p = json.loads(r.params)
            a = evaluate(pool, u900, r.strategy, p, {"test": TEST}, args.K)["test"]
            b = evaluate(pool, u600, r.strategy, p, {"train": TRAIN, "test": TEST}, args.K)
            final.append(dict(strategy=r.strategy, params=r.params,
                              train_CAGR=r.tr_CAGR, train_DD=r.tr_MaxDD, train_Sharpe=r.tr_Sharpe,
                              train_trades=r.tr_trades, train_win=r.tr_win, train_avg=r.tr_avg,
                              test_CAGR=a["CAGR"], test_DD=a["MaxDD"], test_Sharpe=a["Sharpe"], test_win=a.get("win"),
                              test_avg=a.get("avg"),
                              sc600_train_CAGR=b["train"]["CAGR"], sc600_test_CAGR=b["test"]["CAGR"],
                              sc600_test_DD=b["test"]["MaxDD"]))
            print("FINAL", final[-1], flush=True)
    fin = pd.DataFrame(final)
    fin.to_csv(os.path.join(args.out, "final.csv"), index=False)
    print(fin.to_string())


if __name__ == "__main__":
    main()
