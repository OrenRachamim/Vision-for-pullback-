"""
sr_features.py - מאפיינים יומיים לכל מניה, כפי שהיו ידועים בסוף כל יום (בלי הצצה לעתיד), לשימוש מנוע האסטרטגיות.

לכל יום t (אחרי הסגירה):
  * מחיר/מגמה: ATR14, SMA5/20/50/200, RSI(2), RSI(14), ווליום יחסי, שפל/שיא N ימים קודמים.
  * אזורי תמיכה/התנגדות (sr_levels.Levels.asof(t)) עם לפחות 2 נגיעות:
      sup_*  - האזור הגבוה ביותר שתחתיתו מתחת לסגירה (המחיר מעליו או בתוכו) = תמיכה;
      res_*  - האזור הנמוך ביותר שתחתיתו מעל הסגירה = התנגדות.
  * פריצה אחרונה של אזור התנגדות (סגירה ראשונה מעל ראש האזור + 0.1ATR אחרי 10 סגירות מתחתיו):
      brk_top / brk_bot / brk_t - האזור והיום (נשמר 20 יום) - לאסטרטגיית "פריצה ובדיקה חוזרת".
  * תנועה אחרונה (פיבונאצ'י): שיא מפנה אחרון שאושר (swing_hi) והשפל הנמוך ביותר ב-60 הימים שלפניו (swing_lo).
  * נקודות ציר קלאסיות (Floor pivots) מהיום הקודם: P, S1, S2, R1.

נשמר ל-feat_cache/<TICKER>.pkl. הרצה:  python sr_features.py --universe universes/sp500.txt ...
"""
import argparse
import os
import pickle
from concurrent.futures import ProcessPoolExecutor

import numpy as np
import pandas as pd

import backtest as bt
import sr_levels as sr

CACHE = "feat_cache"
FROM = "2013-01-01"          # 3 שנות חימום לפני 2016


def rsi(c, n):
    d = np.diff(c, prepend=np.nan)
    up = pd.Series(np.where(d > 0, d, 0.0)).ewm(alpha=1 / n, adjust=False).mean().values
    dn = pd.Series(np.where(d < 0, -d, 0.0)).ewm(alpha=1 / n, adjust=False).mean().values
    with np.errstate(divide="ignore", invalid="ignore"):
        return 100 - 100 / (1 + up / dn)


def build(tk):
    df = bt.load_history(tk)
    df = df[df.index >= FROM]
    if len(df) < 400:
        return None
    o, h, l, c, v = (df[k].values for k in ("Open", "High", "Low", "Close", "Volume"))
    lv = sr.Levels(df)
    atr = lv.atr
    n = len(df)
    S = lambda w: pd.Series(c).rolling(w).mean().values
    out = dict(o=o, h=h, l=l, c=c, v=v, atr=atr, sma5=S(5), sma10=S(10), sma20=S(20), sma50=S(50), sma200=S(200),
               rsi2=rsi(c, 2), rsi14=rsi(c, 14),
               vr=v / pd.Series(v).rolling(20).mean().shift(1).values,
               ll10=pd.Series(l).rolling(10).min().shift(1).values,
               hh20=pd.Series(h).rolling(20).max().shift(1).values)
    P = (h + l + c) / 3
    out.update(pP=P, pS1=2 * P - h, pS2=P - (h - l), pR1=2 * P - l)   # ידועים בסוף היום - משמשים למחר
    cols = ["sup_top", "sup_bot", "sup_n", "res_top", "res_bot", "res_n", "brk_top", "brk_bot", "brk_t",
            "swing_hi", "swing_lo", "swing_hi_t"]
    for k in cols:
        out[k] = np.full(n, np.nan)
    broken = {}
    last_brk = None
    pts = lv.pts
    for t in range(260, n):
        levels = [L for L in lv.asof(t) if L["touches"] >= 2]
        sup = [L for L in levels if L["bottom"] <= c[t]]
        res = [L for L in levels if L["bottom"] > c[t]]
        if sup:
            L = max(sup, key=lambda x: x["bottom"])
            out["sup_top"][t], out["sup_bot"][t], out["sup_n"][t] = L["top"], L["bottom"], L["touches"]
        if res:
            L = min(res, key=lambda x: x["bottom"])
            out["res_top"][t], out["res_bot"][t], out["res_n"][t] = L["top"], L["bottom"], L["touches"]
        thr = 0.1 * atr[t]
        for L in levels:
            top = L["top"]
            if L["last_kind"] != "H" or not (c[t] > top + thr and c[t - 1] <= top + thr):
                continue
            if not (c[t - 11:t - 1] < top).all():
                continue
            if L["id"] in broken and L["last_high"] <= broken[L["id"]]:
                continue
            broken[L["id"]] = t
            if last_brk is None or last_brk[2] < t or top > last_brk[0]:
                last_brk = (top, L["bottom"], t)
        if last_brk and t - last_brk[2] <= 20:
            out["brk_top"][t], out["brk_bot"][t], out["brk_t"][t] = last_brk
        # שיא מפנה אחרון שאושר (i + PIVOT_N <= t) ושפל 60 הימים שלפניו
        b = np.searchsorted(lv.idx, t - sr.PIVOT_N, side="right")
        for j in range(b - 1, max(b - 40, -1), -1):
            i, p, kind = pts[j]
            if kind == "H":
                lo_ = l[max(0, i - 60):i + 1].min()
                out["swing_hi"][t], out["swing_lo"][t], out["swing_hi_t"][t] = p, lo_, i
                break
    feat = pd.DataFrame(out, index=df.index).astype(np.float32)
    return feat


def save(tk):
    path = os.path.join(CACHE, f"{tk}.pkl")
    if os.path.exists(path):
        return tk, True
    try:
        f = build(tk)
    except Exception as e:  # noqa: BLE001
        return tk, repr(e)
    if f is None:
        return tk, False
    with open(path, "wb") as fh:
        pickle.dump(f, fh, protocol=pickle.HIGHEST_PROTOCOL)
    return tk, True


def load(tk):
    with open(os.path.join(CACHE, f"{tk}.pkl"), "rb") as fh:
        return pickle.load(fh)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--universe", nargs="+", required=True)
    args = ap.parse_args(argv)
    bt.use_scanner("pullback_scanner")
    tickers = [ln.strip().upper() for p in args.universe for ln in open(p) if ln.strip()]
    tickers = [t for t in dict.fromkeys(tickers) if os.path.exists(f"data/{t}.csv")]
    os.makedirs(CACHE, exist_ok=True)
    bad = []
    with ProcessPoolExecutor() as ex:
        for tk, ok in ex.map(save, tickers, chunksize=4):
            if ok is not True:
                bad.append((tk, ok))
    print(f"{len(tickers) - len(bad)} built, skipped: {bad[:10]}")


if __name__ == "__main__":
    main()
