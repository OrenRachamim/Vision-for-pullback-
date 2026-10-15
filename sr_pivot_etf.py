"""
sr_pivot_etf.py - אסטרטגיית נקודות הציר על תעודות סל (בלי הטיית שרידות), ובדיקת מילוי ביניים (pen 0.05%).
הרצה:  python sr_pivot_etf.py
"""
from concurrent.futures import ProcessPoolExecutor

import pandas as pd

import sr_optimize as O
import sr_pivot_check as PC
import sr_strategies as S

if __name__ == "__main__":
    U = {"ETF26": O.universe("universes/etfs.txt"), "900": O.universe("universes/sp500.txt", "universes/sp400.txt")}
    rows = []
    with ProcessPoolExecutor(4) as pool:
        for un, u in U.items():
            for name, dp in [("base (touch fill)", {}), ("pen 0.05%", dict(pen=0.0005)), ("pen 0.1%", dict(pen=0.001)),
                             ("hold 1, touch fill", dict(hold=1)), ("hold 1, pen 0.1%", dict(hold=1, pen=0.001))]:
                if un == "900" and not name.startswith(("pen 0.05", "hold 1, pen")):
                    continue
                for K in ((5,) if un == "ETF26" else (10,)):
                    tr, r = PC.run(pool, u, dict(PC.BASE, **dp), None, K)
                    rows.append(dict(universe=un, variant=name, K=K, **{f"{lab}_{k}": r[lab].get(k) for lab in ("train", "test")
                                                                     for k in ("CAGR", "MaxDD", "Sharpe", "avg")}))
                    print(rows[-1], flush=True)
    df = pd.DataFrame(rows)
    df.to_csv("results_sr_pivot/etf_and_pen.csv", index=False)
    print(df.round(3).to_string())
