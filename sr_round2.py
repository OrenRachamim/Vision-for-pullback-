"""
sr_round2.py - סבב שני: לטובות מכל אסטרטגיה (לפי אימון) מוסיפים מסנן מצב שוק (SPY מעל SMA200)
ומשנים את מספר המשבצות K. בוחרים לפי אימון בלבד, ומדווחים בדיקה (2022+, ו-S&P 600).
מוסיף בסיסי השוואה: כניסה אקראית במגמה (אותו K ואותה החזקה) ו-SPY.

הרצה:  python sr_round2.py results_sr_opt results_sr_opt_lim --out results_sr_round2
"""
import argparse
import json
import os
import sys
from concurrent.futures import ProcessPoolExecutor

import pandas as pd

import sr_optimize as O
import sr_strategies as S


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("dirs", nargs="+")
    ap.add_argument("--top", type=int, default=2)
    ap.add_argument("--out", default="results_sr_round2")
    args = ap.parse_args(argv)
    # תיקייה מאוחרת מחליפה את התוצאות של אותן אסטרטגיות בתיקיות קודמות (למשל אחרי תיקון הלימיט)
    srch = pd.DataFrame()
    for d in args.dirs:
        new = pd.read_csv(f"{d}/train_search.csv")
        srch = pd.concat([srch[~srch.strategy.isin(set(new.strategy))] if len(srch) else srch, new])
    srch = srch[srch.tr_trades >= 300]
    best = srch.sort_values("tr_Sharpe", ascending=False).groupby("strategy").head(args.top)
    u900 = O.universe("universes/sp500.txt", "universes/sp400.txt")
    u600 = O.universe("universes/sp600.txt")
    rows = []
    cand = [(r.strategy, json.loads(r.params)) for r in best.itertuples()]
    cand += [("random", dict(q=0.03, hold=h, trend="200up")) for h in (5, 10)]
    with ProcessPoolExecutor(4) as pool:
        for name, p0 in cand:
            for regime in (None, "up200"):
                p = dict(p0, regime=regime) if regime else dict(p0)
                t9 = S.trades(pool, u900, name, p)
                t6 = S.trades(pool, u600, name, p)
                for K in (5, 10, 20):
                    r = dict(strategy=name, params=json.dumps(p), K=K)
                    for lab, tr, u, (a, b) in [("tr900", t9, u900, O.TRAIN), ("te900", t9, u900, O.TEST),
                                               ("tr600", t6, u600, O.TRAIN), ("te600", t6, u600, O.TEST)]:
                        _, m, _ = S.portfolio(tr, u, a, b, K=K)
                        r.update({f"{lab}_{k}": m.get(k) for k in ("CAGR", "MaxDD", "Sharpe", "win", "avg", "per_year")})
                    rows.append(r)
                    print(name, p, K, {k: round(v, 3) for k, v in r.items() if k.endswith(("CAGR", "Sharpe"))},
                          flush=True)
    df = pd.DataFrame(rows)
    os.makedirs(args.out, exist_ok=True)
    df.to_csv(os.path.join(args.out, "round2.csv"), index=False)
    spy = {lab: S.bench("SPY", a, b) for lab, (a, b) in [("train", O.TRAIN), ("test", O.TEST)]}
    print("SPY", spy)
    json.dump({k: {kk: float(vv) for kk, vv in v.items()} for k, v in spy.items()},
              open(os.path.join(args.out, "spy.json"), "w"))


if __name__ == "__main__":
    sys.exit(main())
