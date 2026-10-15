"""
sr_recommend.py - מנוע ההמלצות: מריץ אסטרטגיה (ברירת מחדל: נקודות ציר S2, הטובה ביותר בבדיקות) על הנתונים
האחרונים ומדפיס את ההוראות למסחר של מחר.

  לכל מניה שעומדת בתנאים: לימיט קנייה = S2 של היום (P - (High - Low)), סטופ = S2 - 1*ATR,
  יציאה: בסגירה של היום השני אחרי הכניסה (hold=2), או בסטופ. דירוג לפי RSI(2) (נמוך = ראשון).
  בתיק של K משבצות: שמים פקודות על הראשונות ברשימה, ומבטלים את השאר ברגע שהתמלאו K.

אזהרה (ANALYSIS.md סעיף 23): היתרון ההיסטורי תלוי מאוד בהנחת המילוי והעלויות, ואין יתרון על תעודות סל.
זה כלי מחקר, לא המלצת השקעה.

הרצה:  python sr_features.py --universe ...   (לעדכון המאפיינים אחרי רענון הנתונים)
        python sr_recommend.py --universe universes/sp500.txt universes/sp400.txt --top 20
"""
import argparse
import json

import numpy as np
import pandas as pd

import sr_optimize as O
import sr_pivot_check as PC
import sr_strategies as S


def recommend(tickers, name="pivot", p=None, top=20):
    p = p or PC.BASE
    rows = []
    for tk in tickers:
        F = S.feats(tk)
        f = {k: F[k].values.astype(np.float64) for k in F.columns}
        if p.get("regime"):
            f["mkt"] = S.market(F.index)[p["regime"]]
        m, limit, stop, target, score = S.STRATS[name](f, p)
        t = len(F) - 1
        if not np.asarray(m)[t]:
            continue
        lim = limit[t] if np.ndim(limit) else np.nan
        rows.append(dict(ticker=tk, date=F.index[t].date(), close=f["c"][t],
                         buy_limit=round(lim, 2) if lim == lim else "open",
                         stop=round(stop[t], 2), target=round(target[t], 2) if target[t] == target[t] else "-",
                         exit=f"close of day {p.get('hold', 5)}" + (" or close > SMA5" if p.get("exit_sma5") else ""),
                         dist_pct=round((lim / f["c"][t] - 1) * 100, 2) if lim == lim else 0.0,
                         rsi2=round(f["rsi2"][t], 1), score=score[t]))
    df = pd.DataFrame(rows)
    return df.sort_values("score", ascending=False).head(top).drop(columns="score") if len(df) else df


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--universe", nargs="+", default=["universes/sp500.txt", "universes/sp400.txt"])
    ap.add_argument("--strategy", default="pivot")
    ap.add_argument("--params", default=None, help="JSON params (default: the tested pivot config)")
    ap.add_argument("--top", type=int, default=20)
    args = ap.parse_args(argv)
    u = O.universe(*args.universe)
    df = recommend(u, args.strategy, json.loads(args.params) if args.params else None, args.top)
    print(f"{len(df)} orders for the next session (data as of {df.date.max() if len(df) else '-'}):")
    print(df.to_string(index=False))


if __name__ == "__main__":
    main()
