"""
sr_strategies.py - מנוע בדיקה לאסטרטגיות מסחר קצרות (כמה ימים) המבוססות על תמיכה/התנגדות.

זרימה:
  1. sr_features.py מחשב לכל מניה ולכל יום את האזורים/רמות כפי שהיו ידועים באותו יום (feat_cache/).
  2. כל אסטרטגיה מייצרת איתותים ביום t (אחרי הסגירה): כניסה ב-t+1 בפתיחה, או בפקודת לימיט ב-t+1;
     סטופ, יעד (אופציונלי), החזקה מקסימלית, ויציאה אופציונלית "סגירה מעל SMA5" (ביצוע בפתיחה שלמחרת).
  3. simulate(): עסקה לכל איתות. סטופ ויעד באותו נר -> סטופ. פתיחה מתחת לסטופ ביום הכניסה -> לא נכנסים.
     עלות: COST לכל צד (עמלה + החלקה).
  4. portfolio(): תיק עם K משבצות שוות (equity/K לכל עסקה, ריבית דריבית), עסקה אחת לכל מניה בו-זמנית;
     כשיש יותר איתותים ממשבצות - לפי score. שווי יומי לפי סגירות -> CAGR, ירידה מקסימלית, Sharpe.

האסטרטגיות (המוכרות ברשת) - ראו STRATS ו-GRIDS.
"""
import os
import pickle

import numpy as np
import pandas as pd

import sr_features as sf

COST = 0.0005            # לכל צד (5bp) - עמלה + החלקה במניות נזילות
_F = {}                  # מטמון מאפיינים בתהליך העבודה


def feats(tk):
    if tk not in _F:
        _F[tk] = sf.load(tk)
    return _F[tk]


# ---------------------------------------------------------------- אסטרטגיות
# כל פונקציה מקבלת dict של מערכים (מאפיינים) ו-p (פרמטרים) ומחזירה dict: t, limit, stop, target, score
# (מערכים באורך מספר האיתותים; limit=nan -> כניסה בפתיחה; target=nan -> בלי יעד).

def _trend(f, p):
    m = np.ones(len(f["c"]), bool)
    if p.get("regime"):
        m &= f["mkt"]
    tr = p.get("trend", "200")
    if "200" in tr:
        m &= f["c"] > f["sma200"]
    if "50" in tr:
        m &= f["c"] > f["sma50"]
    if "up" in tr:
        m &= f["sma50"] > f["sma200"]
    return m


def _target(f, p, entry_ref):
    """יעד: התנגדות הבאה (res), או k*ATR, או אין."""
    tg = p.get("target", "res")
    if tg == "res":
        return np.where(np.isnan(f["res_bot"]), entry_ref + 3 * f["atr"], f["res_bot"] - 0.05 * f["atr"])
    if tg == "none":
        return np.full(len(entry_ref), np.nan)
    return entry_ref + float(tg) * f["atr"]


def _rr_ok(f, p, entry_ref, stop, target):
    rr = p.get("min_rr", 0)
    if not rr:
        return np.ones(len(entry_ref), bool)
    with np.errstate(invalid="ignore", divide="ignore"):
        return np.isnan(target) | ((target - entry_ref) / (entry_ref - stop) >= rr)


def s_support_bounce(f, p):
    """קנייה בתמיכה: השפל נגע באזור תמיכה (עד a*ATR מעל ראשו) והסגירה נשארה מעל ראש האזור.
    סטופ מתחת לתחתית האזור, יעד = ההתנגדות הבאה."""
    c, l, atr = f["c"], f["l"], f["atr"]
    m = _trend(f, p) & (f["sup_n"] >= p.get("touches", 2))
    m &= (l <= f["sup_top"] + p.get("near", 0.25) * atr) & (c >= f["sup_top"])
    if p.get("green"):
        m &= c > f["o"]
    if p.get("rsi2"):
        m &= f["rsi2"] < p["rsi2"]
    stop = f["sup_bot"] - p.get("stop_atr", 0.5) * atr
    target = _target(f, p, c)
    m &= _rr_ok(f, p, c, stop, target)
    return m, np.nan, stop, target, -f["rsi2"]


def s_spring(f, p):
    """תמיכה כוזבת / Spring (Wyckoff): השפל ירד מתחת לתחתית התמיכה, אבל הסגירה חזרה מעליה."""
    c, l, atr = f["c"], f["l"], f["atr"]
    m = _trend(f, p) & (f["sup_n"] >= p.get("touches", 2))
    m &= (l < f["sup_bot"] - p.get("pierce", 0.1) * atr) & (c > f["sup_bot"])
    if p.get("green"):
        m &= c > f["o"]
    stop = l - p.get("stop_atr", 0.2) * atr
    target = _target(f, p, c)
    m &= _rr_ok(f, p, c, stop, target)
    return m, np.nan, stop, target, -f["rsi2"]


def s_break_retest(f, p):
    """פריצה ובדיקה חוזרת (התנגדות הופכת לתמיכה): 2-20 ימים אחרי פריצת אזור, המחיר חזר לראש האזור
    (שפל עד a*ATR מעליו) ונסגר מעליו."""
    c, l, atr = f["c"], f["l"], f["atr"]
    t = np.arange(len(c))
    age = t - f["brk_t"]
    m = _trend(f, p) & (age >= p.get("min_age", 2)) & (age <= p.get("max_age", 20))
    m &= (l <= f["brk_top"] + p.get("near", 0.25) * atr) & (c > f["brk_top"])
    if p.get("green"):
        m &= c > f["o"]
    stop = f["brk_bot"] - p.get("stop_atr", 0.5) * atr
    target = _target(f, p, c) if p.get("target", "hh") != "hh" else np.maximum(f["hh20"], c + atr)
    return m, np.nan, stop, target, -f["rsi2"]


def s_breakout(f, p):
    """פריצת התנגדות קלאסית: היום שבו הסגירה עברה את ראש האזור. אופציה: ווליום גבוה."""
    c, atr = f["c"], f["atr"]
    t = np.arange(len(c))
    m = _trend(f, p) & (f["brk_t"] == t)
    if p.get("vol"):
        m &= f["vr"] >= p["vol"]
    stop = f["brk_bot"] - p.get("stop_atr", 0.5) * atr
    target = _target(f, p, c)
    return m, np.nan, stop, target, f["vr"]


def s_pivot(f, p):
    """נקודות ציר קלאסיות (Floor pivots): לימיט קנייה ב-S1 (או S2) של מחר, במגמה עולה; יעד = P."""
    lvl = f["pS1"] if p.get("level", "S1") == "S1" else f["pS2"]
    atr = f["atr"]
    m = _trend(f, p) & (f["c"] > lvl)
    stop = lvl - p.get("stop_atr", 1.0) * atr
    target = f["pP"] if p.get("target", "P") == "P" else _target(f, p, lvl)
    return m, lvl, stop, target, -f["rsi2"]


def s_fib(f, p):
    """תיקון פיבונאצ'י: אחרי תנועה עולה (שפל -> שיא מפנה אחרון, לפחות m*ATR), לימיט קנייה ברמת התיקון
    (38.2/50/61.8%), סטופ מתחת ל-78.6% (או השפל), יעד = השיא."""
    c, atr = f["c"], f["atr"]
    hi, lo = f["swing_hi"], f["swing_lo"]
    rng = hi - lo
    t = np.arange(len(c))
    lvl = hi - p.get("fib", 0.618) * rng
    m = _trend(f, p) & (rng >= p.get("min_swing", 4) * atr) & (t - f["swing_hi_t"] <= p.get("max_age", 30))
    m &= (f["l"] > lvl) & (c < hi)                         # עוד לא הגיע לרמה, והשיא לא נפרץ
    stop = hi - p.get("stop_fib", 0.786) * rng - 0.1 * atr
    target = hi if p.get("target", "hi") == "hi" else _target(f, p, lvl)
    return m, lvl, stop, target, rng / atr


def s_ma_support(f, p):
    """ממוצע נע כתמיכה דינמית: במגמה עולה, השפל נגע ב-SMA (20/50) והסגירה מעליו."""
    c, l, atr = f["c"], f["l"], f["atr"]
    ma = f[f"sma{p.get('ma', 50)}"]
    m = _trend(f, p) & (f["sma50"] > f["sma200"]) & (l <= ma + p.get("near", 0.1) * atr) & (c > ma)
    stop = ma - p.get("stop_atr", 1.0) * atr
    target = _target(f, p, c)
    return m, np.nan, stop, target, -f["rsi2"]


def s_nday_low(f, p):
    """תמיכה קצרת טווח / חזרה לממוצע (Connors): במגמה עולה, סגירה מתחת לשפל של N הימים הקודמים
    או RSI(2) נמוך; יציאה בסגירה מעל SMA5 (ביצוע בפתיחה שלמחרת) או אחרי H ימים."""
    c = f["c"]
    m = _trend(f, p)
    if p.get("rsi2"):
        m &= f["rsi2"] < p["rsi2"]
    if p.get("below_low"):
        m &= c < f["ll10"]
    if p.get("at_support"):                                 # שילוב: גם נוגע באזור תמיכה
        m &= (f["l"] <= f["sup_top"] + 0.25 * f["atr"]) & (f["sup_n"] >= 2)
    sa = p.get("stop_atr")
    stop = c - sa * f["atr"] if sa else np.full(len(c), np.nan)
    return m, np.nan, stop, np.full(len(c), np.nan), -f["rsi2"]


def s_random(f, p):
    """בסיס השוואה: כניסה אקראית (הסתברות q ליום) במגמה עולה, אותה החזקה."""
    rng = np.random.default_rng(int(f["c"][300] * 1000) % 2**32)
    m = _trend(f, p) & (rng.random(len(f["c"])) < p.get("q", 0.03))
    return m, np.nan, np.full(len(m), np.nan), np.full(len(m), np.nan), rng.random(len(m))


STRATS = dict(support_bounce=s_support_bounce, spring=s_spring, break_retest=s_break_retest,
              breakout=s_breakout, pivot=s_pivot, fib=s_fib, ma_support=s_ma_support, nday_low=s_nday_low,
              random=s_random)


# ---------------------------------------------------------------- עסקאות
def simulate(f, sig_t, limit, stop, target, hold, exit_sma5):
    """עסקה לכל איתות. מחזיר רשימת tuples: (t, entry_i, exit_i, entry_px, exit_px, reason)."""
    o, h, l, c, sma5 = f["o"], f["h"], f["l"], f["c"], f["sma5"]
    n = len(c)
    out = []
    for k, t in enumerate(sig_t):
        e = t + 1
        if e >= n:
            continue
        lim, st, tg = limit[k], stop[k], target[k]
        if lim == lim:                                      # לימיט
            if o[e] <= lim:
                px = o[e]
            elif l[e] <= lim:
                px = lim
            else:
                continue
        else:
            px = o[e]
        if (st == st and px <= st) or (tg == tg and px >= tg):
            continue
        last = min(e + hold - 1, n - 1)
        reason, xi, xpx = "time", last, c[last]
        for j in range(e, last + 1):
            if st == st and j > e and o[j] <= st:
                reason, xi, xpx = "stop", j, o[j]; break
            if st == st and l[j] <= st:
                reason, xi, xpx = "stop", j, st; break
            if tg == tg and j > e and o[j] >= tg:
                reason, xi, xpx = "target", j, o[j]; break
            # ביום מילוי לימיט לא יודעים אם השיא היה לפני השפל (נר יומי) -> אין יציאה ביעד באותו יום
            if tg == tg and h[j] >= tg and not (j == e and lim == lim):
                reason, xi, xpx = "target", j, tg; break
            if exit_sma5 and c[j] > sma5[j] and j + 1 < n:
                reason, xi, xpx = "sma5", j + 1, o[j + 1]; break
        else:
            if last < e + hold - 1:
                reason = "open"
        out.append((t, e, xi, px, xpx, reason))
    return out


_MKT = {}


def market(index):
    """מצב השוק (SPY) ביום t: מעל SMA200, מעל SMA50, RSI2 - מיושר לתאריכי המניה."""
    if "spy" not in _MKT:
        import backtest as bt
        c = bt.load_history("SPY")["Close"]
        _MKT["spy"] = pd.DataFrame(dict(up200=c > c.rolling(200).mean(), up50=c > c.rolling(50).mean()))
    m = _MKT["spy"].reindex(index).ffill()
    return {k: m[k].fillna(False).values.astype(bool) for k in m.columns}


def run_ticker(args):
    tk, name, p, start = args
    F = feats(tk)
    f = {k: F[k].values.astype(np.float64) for k in F.columns}
    if p.get("regime"):
        f["mkt"] = market(F.index)[p["regime"]]
    lo = F.index.searchsorted(pd.Timestamp(start))
    m, limit, stop, target, score = STRATS[name](f, p)
    m = np.asarray(m, bool)
    m[:max(lo, 260)] = False
    m[-1] = False
    t = np.nonzero(m)[0]
    if len(t) == 0:
        return []
    bc = lambda x: (np.broadcast_to(x, m.shape) if np.ndim(x) == 0 else x)[t]
    limit, stop, target, score = bc(limit), bc(stop), bc(target), bc(score)
    tr = simulate(f, t, limit, stop, target, p.get("hold", 5), p.get("exit_sma5", False))
    idx = F.index
    sc = dict(zip(t, score))
    return [(tk, idx[a], idx[e], idx[x], pe, px, r, float(sc[a])) for a, e, x, pe, px, r in tr]


def trades(pool, tickers, name, p, start="2016-01-01"):
    rows = []
    for r in pool.map(run_ticker, [(tk, name, p, start) for tk in tickers], chunksize=16):
        rows += r
    df = pd.DataFrame(rows, columns=["ticker", "sig", "entry", "exit", "pe", "px", "reason", "score"])
    df["ret"] = df.px * (1 - COST) / (df.pe * (1 + COST)) - 1
    return df


# ---------------------------------------------------------------- תיק
_CLOSE = {}


def close_matrix(tickers):
    key = tuple(tickers)
    if key not in _CLOSE:
        _CLOSE.clear()
        cols = {tk: feats(tk)["c"] for tk in tickers}
        _CLOSE[key] = pd.DataFrame(cols).sort_index().ffill()
    return _CLOSE[key]


def portfolio(tr, tickers, start, end=None, K=10, seed=0):
    """תיק K משבצות. מחזיר (equity Series, מדדים, עסקאות שבוצעו)."""
    C = close_matrix(tickers)
    C = C.loc[start:end] if end else C.loc[start:]
    dates = C.index
    tr = tr[(tr.entry >= dates[0]) & (tr.entry <= dates[-1]) & (tr.reason != "open")]
    tr = tr.assign(_r=np.random.default_rng(seed).random(len(tr))).sort_values(
        ["entry", "score", "_r"], ascending=[True, False, True])
    by_entry = {d: g for d, g in tr.groupby("entry")}
    col = {tk: i for i, tk in enumerate(C.columns)}
    Cv = C.values
    cash, pos = 1.0, {}                                     # ticker -> (shares, exit_date, exit_px_net)
    eq = np.empty(len(dates))
    taken = []
    prev_eq = 1.0
    for di, d in enumerate(dates):
        g = by_entry.get(d)
        if g is not None and len(pos) < K:
            for r in g.itertuples(index=False):
                if len(pos) >= K:
                    break
                if r.ticker in pos:
                    continue
                alloc = min(prev_eq / K, cash)
                if alloc <= prev_eq / K * 0.5:
                    break
                cash -= alloc
                pos[r.ticker] = (alloc / (r.pe * (1 + COST)), r.exit, r.px * (1 - COST))
                taken.append(r)
        for tk in [k for k, v in pos.items() if v[1] <= d]:
            sh, _, xp = pos.pop(tk)
            cash += sh * xp
        mtm = sum(sh * Cv[di, col[tk]] for tk, (sh, _, _) in pos.items())
        eq[di] = cash + mtm
        prev_eq = eq[di]
    eq = pd.Series(eq, index=dates)
    taken = pd.DataFrame(taken)
    return eq, metrics(eq, taken), taken


def metrics(eq, taken):
    yrs = (eq.index[-1] - eq.index[0]).days / 365.25
    dr = eq.pct_change().dropna()
    dd = (eq / eq.cummax() - 1).min()
    res = dict(CAGR=eq.iloc[-1] ** (1 / yrs) - 1 if yrs > 0 else np.nan, MaxDD=dd,
               Sharpe=dr.mean() / dr.std() * np.sqrt(252) if dr.std() > 0 else np.nan,
               trades=len(taken))
    if len(taken):
        hold = (pd.to_datetime(taken.exit) - pd.to_datetime(taken.entry)).dt.days
        res.update(win=(taken.ret > 0).mean(), avg=taken.ret.mean(), hold_days=hold.mean(),
                   per_year=len(taken) / yrs)
    return res


def bench(tk, start, end=None):
    import backtest as bt
    c = bt.load_history(tk)["Close"]
    c = c.loc[start:end] if end else c.loc[start:]
    return metrics(c / c.iloc[0], pd.DataFrame())
