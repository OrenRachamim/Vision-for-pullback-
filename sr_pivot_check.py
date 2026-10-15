"""
sr_pivot_check.py - בדיקות עמידות לאסטרטגיית נקודות הציר (לימיט קנייה ב-S2 של אתמול, החזקה 2 ימים).

  * מילוי שמרני: הלימיט "מתמלא" רק אם השפל ירד מתחתיו ב-pen (0 / 0.1% / 0.3%).
  * עלויות: 5 / 10 / 20 נקודות בסיס לכל צד.
  * דירוג: לפי RSI2 (ברירת מחדל) מול אקראי - האם הבחירה בין איתותים היא שעושה את התוצאה.
  * מספר משבצות K, מסנן מצב שוק, ותשואה לפי שנה.
הרצה:  python sr_pivot_check.py --out results_sr_pivot
"""
import argparse
import json
import os
from concurrent.futures import ProcessPoolExecutor

import numpy as np
import pandas as pd

import sr_optimize as O
import sr_strategies as S

BASE = dict(hold=2, exit_sma5=False, trend="200", level="S2", target="none", stop_atr=1.0)


def run(pool, u, p, cost=None, K=10, rand_score=False):
    tr = S.trades(pool, u, "pivot", p, cost=cost)
    if rand_score:
        tr["score"] = np.random.default_rng(1).random(len(tr))
    out = {}
    for lab, (a, b) in [("train", O.TRAIN), ("test", O.TEST)]:
        eq, m, tk = S.portfolio(tr, u, a, b, K=K)
        out[lab] = m
        out[lab + "_eq"] = eq
    return tr, out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="results_sr_pivot")
    args = ap.parse_args(argv)
    os.makedirs(args.out, exist_ok=True)
    U = {"900": O.universe("universes/sp500.txt", "universes/sp400.txt"), "600": O.universe("universes/sp600.txt")}
    rows = []
    variants = [("base", {}, None, 10, False)]
    variants += [(f"pen {x:.1%}", dict(pen=x), None, 10, False) for x in (0.001, 0.003)]
    variants += [(f"cost {c * 1e4:.0f}bp/side", {}, c, 10, False) for c in (0.001, 0.002)]
    variants += [("pen 0.1% + cost 10bp", dict(pen=0.001), 0.001, 10, False)]
    variants += [("random ranking", {}, None, 10, True)]
    variants += [(f"K={k}", {}, None, k, False) for k in (5, 20)]
    variants += [("SPY > SMA200 filter", dict(regime="up200"), None, 10, False)]
    variants += [(f"hold {h}", dict(hold=h), None, 10, False) for h in (1, 3, 5)]
    variants += [("S1 instead of S2", dict(level="S1"), None, 10, False)]
    yearly = {}
    with ProcessPoolExecutor(4) as pool:
        for name, dp, cost, K, rs in variants:
            p = dict(BASE, **dp)
            for un, u in U.items():
                tr, r = run(pool, u, p, cost, K, rs)
                rows.append(dict(variant=name, universe=un,
                                 **{f"{lab}_{k}": r[lab].get(k) for lab in ("train", "test")
                                    for k in ("CAGR", "MaxDD", "Sharpe", "win", "avg", "per_year")}))
                print(rows[-1], flush=True)
                if name == "base":
                    eq = pd.concat([r["train_eq"], r["test_eq"] * r["train_eq"].iloc[-1]])
                    ye = eq.groupby(eq.index.year).last()
                    yearly[un] = (ye / ye.shift(1).fillna(1.0) - 1)
                    fills = tr[(tr.entry >= O.TRAIN[0])]
                    print(un, "trades", len(fills), "exit reasons", fills.reason.value_counts(normalize=True).round(3).to_dict())
    df = pd.DataFrame(rows)
    df.to_csv(os.path.join(args.out, "robustness.csv"), index=False)
    yd = pd.DataFrame(yearly)
    yd.to_csv(os.path.join(args.out, "yearly.csv"))
    print(df.round(3).to_string())
    print(yd.round(3).to_string())


if __name__ == "__main__":
    main()
