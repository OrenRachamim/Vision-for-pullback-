"""
mtf_search.py - חיפוש רחב של כניסות רב-שכבתיות (יומי x שעתי x 5 דקות) ויציאה "מדורגת" (cascade).

כניסה = פילטר יומי  x  פילטר שעתי  x  טריגר 5 דקות  (העסקה הראשונה שעומדת בכולם בכל יום, 10:00-15:00):
  יומי : none | up (C>SMA50>SMA200) | conv (התכנסות ממוצעים + פריצה, 5 ימים) | pull (up + RSI2<15) | high (up + עד 3% משיא 60 יום)
  שעתי : none | hup (C>SMA20>SMA50 שעתי) | hos (RSI14 שעתי < 35) | hconv (ממוצעים שעתיים 10..100 בטווח 3%)
  5 דק : rsimacd (RSI<30 ב-30 דק' ואז חיתוך MACD) | macd (כל חיתוך MACD למעלה) | orb (פריצת טווח 30 הדקות
         הראשונות) | vwap (חזרה מעל VWAP אחרי 30 דק' מתחתיו) | random (נר אקראי - בסיס)
  הכל ידוע בזמן ההחלטה: יומי עד סגירת אתמול, שעתי עד הנר השעתי שנסגר, 5 דקות עד סגירת נר הטריגר. כניסה בפתיחת הנר הבא.

יציאות (ביחידות ATR יומי של אתמול; עלות 5bp לכל צד):
  eod      - סגירת היום.
  L5 / L1h / Ld - רמה אחת: יעד a, סטופ s, זמן T (נרות 5 דקות).
  cascade  - מתחילים ברמת 5 הדקות; אם נכשלה (סטופ או זמן) והמגמה השעתית עדיין שלמה (C>SMA20 שעתי) - עוברים
             לרמה השעתית (יעד/סטופ/זמן רחבים יותר, מאותו מחיר כניסה); אם גם היא נכשלה והמגמה היומית שלמה
             (C>SMA20 יומי) - לרמה היומית. אחרת יוצאים. casc_nc = אותו דבר בלי בדיקת המגמה.
  שני סטים: tight ו-wide.

בחירה מול בדיקה: חצי ראשון של ימי הכניסה = בחירה, חצי שני = בדיקה. כל שילוב מושווה לכניסה אקראית עם אותם
פילטרים ואותה יציאה.

הרצה:  python mtf_search.py --out results_mtf_search
"""
import argparse
import os
import zlib
from concurrent.futures import ProcessPoolExecutor

import numpy as np
import pandas as pd
from numba import njit

import backtest as bt
import mtf_data as md
import mtf_strategy as ms

COST = 0.0005
SETS = {  # (a, s, T) לכל רמה: a/s ביחידות ATR יומי, T בנרות 5 דקות
    "tight": [(0.25, 0.25, 12), (0.5, 0.5, 78), (1.0, 1.0, 390)],
    "wide": [(0.4, 0.3, 24), (0.8, 0.7, 156), (1.5, 1.2, 780)],
}
MAX_BARS = 24 + 156 + 780 + 10
D_FILTERS = ("none", "up", "conv", "pull", "high")
H_FILTERS = ("none", "hup", "hos", "hconv")
TRIGGERS = ("rsimacd", "macd", "orb", "vwap", "random")


@njit(cache=True)
def run_exit(o, h, l, c, e, datr, A, S, T, nst, hconf, dconf, confirm):
    """יציאה מדורגת. מחזיר (מחיר יציאה, אינדקס יציאה, שלב (1..3), קוד: 1 יעד, 2 סטופ, 3 זמן, 4 בלי אישור, 0 פתוח)."""
    n = len(c)
    entry = o[e]
    start = e
    for k in range(nst):
        tgt = entry + A[k] * datr
        stp = entry - S[k] * datr
        end = start + T[k] - 1
        if end >= n:
            return np.nan, n - 1, k + 1, 0
        fail = -1
        code = 3
        for j in range(start, end + 1):
            if l[j] <= stp:
                fail = j
                code = 2
                break
            if h[j] >= tgt:
                px = o[j] if (j > e and o[j] >= tgt) else tgt
                return px, j, k + 1, 1
        if fail < 0:
            fail = end
        if k == nst - 1:
            if code == 2:
                return (o[fail] if (fail > e and o[fail] <= stp) else stp), fail, k + 1, 2
            return c[fail], fail, k + 1, 3
        ok = True
        if confirm:
            ok = hconf[fail] if k == 0 else dconf[fail]
        if not ok:
            if code == 2:
                return (o[fail] if (fail > e and o[fail] <= stp) else stp), fail, k + 1, 4
            return c[fail], fail, k + 1, 4
        nstp = entry - S[k + 1] * datr
        if l[fail] <= nstp:                                   # אותו נר כבר עבר גם את הסטופ הבא
            return nstp, fail, k + 2, 2
        start = fail + 1
    return np.nan, n - 1, nst, 0


@njit(cache=True)
def run_eod(c, e, day_id):
    n = len(c)
    j = e
    while j + 1 < n and day_id[j + 1] == day_id[e]:
        j += 1
    if j + 1 >= n:
        return np.nan
    return c[j]


def _map_prev_day(d_index, bar_days, values):
    """ערך יומי של יום המסחר הקודם לכל נר (בלי הצצה)."""
    pos = d_index.searchsorted(bar_days) - 1
    out = np.full(len(bar_days), np.nan)
    ok = pos >= 0
    out[ok] = values[pos[ok]]
    return out


def features(tk):
    d, hr, m = md.load(tk, "daily"), md.load(tk, "1h"), md.load(tk, "5m")
    if len(d) < 300 or len(hr) < 150 or len(m) < 1500:
        return None
    # --- יומי
    C = d["Close"]
    s20, s50, s200 = (C.rolling(n).mean() for n in (20, 50, 200))
    datr = bt.atr14(d)
    up = (C > s50) & (s50 > s200)
    r2 = pd.Series(ms.rsi(C.values, 2), index=d.index)
    hi60 = d["High"].rolling(60).max()
    ds = ms.daily_signals(d)
    armed = np.zeros(len(d), bool)
    for i in np.nonzero(ds["signal"].values)[0]:
        armed[i:i + 5] = True                                  # ידוע בסגירת i -> תקף לימים i+1..i+5 (ראו מיפוי)
    dflt = {"none": np.ones(len(d), bool), "up": up.values, "conv": armed,
            "pull": (up & (r2 < 15)).values, "high": (up & (C >= 0.97 * hi60)).values}
    # --- 5 דקות
    t5 = m.index
    bar_days = t5.tz_localize(None).normalize()
    o, h, l, c, v = (m[k].values.astype(np.float64) for k in ("Open", "High", "Low", "Close", "Volume"))
    day_id = pd.factorize(bar_days)[0].astype(np.int64)
    minutes = (t5.hour * 60 + t5.minute).values
    di = pd.DatetimeIndex(d.index)
    D = {k: _map_prev_day(di, bar_days, v_.astype(float)) > 0.5 for k, v_ in dflt.items()}
    datr_b = _map_prev_day(di, bar_days, datr)
    dconf = _map_prev_day(di, bar_days, (C > s20).values.astype(float)) > 0.5
    # --- שעתי (הנר השעתי האחרון שנסגר עד סגירת נר ה-5 דקות)
    hc = hr["Close"]
    h20, h50 = hc.rolling(20).mean(), hc.rolling(50).mean()
    hmas = pd.concat([hc.rolling(n).mean() for n in ms.H_MAS], axis=1)
    hspread = (hmas.max(axis=1) - hmas.min(axis=1)) / hc
    hr14 = pd.Series(ms.rsi(hc.values), index=hr.index)
    h_end = hr.index + pd.Timedelta(minutes=60)
    close_t = hr.index.normalize() + pd.Timedelta(hours=16)
    h_end = h_end.where(h_end <= close_t, close_t)
    hb = h_end.searchsorted(t5 + pd.Timedelta(minutes=5), side="right") - 1
    valid_h = hb >= 100
    hb = np.clip(hb, 0, len(hr) - 1)
    H = {"none": np.ones(len(c), bool),
         "hup": ((hc > h20) & (h20 > h50)).values[hb] & valid_h,
         "hos": (hr14 < 35).values[hb] & valid_h,
         "hconv": (hspread <= 0.03).values[hb] & valid_h}
    hconf = (hc > h20).values[hb] & valid_h
    # --- טריגרים 5 דקות
    r = ms.rsi(c)
    mc, sg = ms.macd(c)
    cross = np.zeros(len(c), bool)
    cross[1:] = (mc[1:] > sg[1:]) & (mc[:-1] <= sg[:-1])
    os_ = pd.Series(r).rolling(6, min_periods=1).min().values < 30
    first30 = minutes < 600
    orh = pd.Series(np.where(first30, h, -np.inf)).groupby(day_id).cummax().values
    orb = np.zeros(len(c), bool)
    orb[1:] = (c[1:] > orh[1:]) & (c[:-1] <= orh[:-1]) & (day_id[1:] == day_id[:-1])
    tp = (h + l + c) / 3
    cpv = pd.Series(tp * v).groupby(day_id).cumsum().values
    cv = pd.Series(v).groupby(day_id).cumsum().values
    vwap = cpv / np.where(cv > 0, cv, np.nan)
    below = pd.Series(c < vwap).rolling(6).sum().shift(1).values == 6
    vw = np.zeros(len(c), bool)
    vw[1:] = (c[1:] > vwap[1:]) & below[1:]
    window = (minutes >= 600) & (minutes + 5 <= 900) & (np.arange(len(c)) > 300)
    window &= np.isfinite(datr_b)
    window[len(c) - MAX_BARS:] = False                         # מספיק נתונים לכל היציאות
    rng = np.random.default_rng(zlib.crc32(tk.encode()))
    rnd = np.zeros(len(c), bool)
    for dd in np.unique(day_id):
        js = np.nonzero((day_id == dd) & window)[0]
        if len(js):
            rnd[rng.choice(js)] = True
    TR = {"rsimacd": cross & os_, "macd": cross, "orb": orb & ~first30, "vwap": vw, "random": rnd}
    TR = {k: v_ & window for k, v_ in TR.items()}
    return dict(o=o, h=h, l=l, c=c, day_id=day_id, dates=np.asarray(bar_days), datr=datr_b, D=D, H=H,
                hconf=hconf, dconf=dconf, TR=TR)


EXITS = ["eod"] + [f"{lvl}_{s}" for s in SETS for lvl in ("L5", "L1h", "Ld", "casc", "casc_nc")]


def outcomes(F, j):
    """כל היציאות לכניסה אחרי נר j (כניסה בפתיחת j+1)."""
    e = j + 1
    o, h, l, c = F["o"], F["h"], F["l"], F["c"]
    datr = F["datr"][j]
    res = {}
    x = run_eod(c, e, F["day_id"])
    res["eod"] = x / o[e] if x == x else np.nan
    for s, st in SETS.items():
        A = np.array([q[0] for q in st]); S = np.array([q[1] for q in st]); T = np.array([q[2] for q in st], np.int64)
        for lvl, idx, conf in [("L5", [0], False), ("L1h", [1], False), ("Ld", [2], False),
                               ("casc", [0, 1, 2], True), ("casc_nc", [0, 1, 2], False)]:
            px, xi, stage, code = run_exit(o, h, l, c, e, datr, A[idx], S[idx], T[idx], len(idx),
                                           F["hconf"], F["dconf"], conf)
            res[f"{lvl}_{s}"] = px / o[e] if px == px else np.nan
            if lvl == "casc":
                res[f"stage_{s}"] = stage
    return {k: (v * (1 - COST) / (1 + COST) - 1 if not k.startswith("stage") else v) for k, v in res.items()}


def run_ticker(tk):
    try:
        F = features(tk)
    except Exception:  # noqa: BLE001
        return []
    if F is None:
        return []
    rows = []
    cache = {}
    for trig, tm in F["TR"].items():
        for dn in D_FILTERS:
            for hn in H_FILTERS:
                mask = tm & F["D"][dn] & F["H"][hn]
                js = np.nonzero(mask)[0]
                if len(js) == 0:
                    continue
                first = js[np.r_[True, F["day_id"][js[1:]] != F["day_id"][js[:-1]]]]   # הראשונה בכל יום
                for j in first:
                    if j not in cache:
                        cache[j] = outcomes(F, j)
                    rows.append(dict(ticker=tk, date=F["dates"][j], trig=trig, d=dn, hf=hn, **cache[j]))
    return rows


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--universe", nargs="+", default=["universes/sp500.txt", "universes/sp400.txt",
                                                      "universes/sp600.txt"])
    ap.add_argument("--out", default="results_mtf_search")
    args = ap.parse_args(argv)
    tk = list(dict.fromkeys(ln.strip().upper() for f in args.universe for ln in open(f) if ln.strip()))
    tk = [t for t in tk if os.path.exists(f"{md.DIRS['5m']}/{t}.pkl") and os.path.exists(f"{md.DIRS['1h']}/{t}.pkl")]
    rows = []
    with ProcessPoolExecutor(4) as ex:
        for r in ex.map(run_ticker, tk, chunksize=8):
            rows += r
    df = pd.DataFrame(rows)
    os.makedirs(args.out, exist_ok=True)
    df.to_pickle(os.path.join(args.out, "trades.pkl"))
    print(len(df), "trade rows;", df.date.nunique(), "entry days", df.date.min(), "->", df.date.max())


if __name__ == "__main__":
    main()
