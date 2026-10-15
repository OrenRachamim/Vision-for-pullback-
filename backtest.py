"""
backtest.py - מנוע בדיקה היסטורית (walk-forward) ל-pullback_scanner.py על נתוני אמת.

הרעיון: לכל יום מסחר בהיסטוריה "מריצים את הסורק כאילו היום הוא אותו יום" -
רק עם הנתונים שהיו ידועים עד סוף אותו יום (חלון של שנתיים, בדיוק כמו load() בסורק,
כולל נר שבועי חלקי). כל איתות נרשם, ואז בודקים מה קרה אחריו בפועל:
  * תשואות קדימה (5/10/20/60 ימים) מול בסיס-השוואה - כל הימים של אותה מניה.
  * סימולציית עסקה עם רמות הסורק: כניסה בפתיחת היום הבא, סטופ = base_lo,
    יעד = R כפול הסיכון, יציאה בזמן אחרי max_hold ימים.
  * פילוח לפי score ולפי כל רכיב (slowing / drying / uptrend) - האם הניקוד מנבא משהו.

הרצה:
    pip install -r requirements.txt
    python backtest.py                         # יוניברס ברירת מחדל, 2016 עד היום
    python backtest.py AAPL MSFT NVDA --start 2018-01-01 --charts 20
    python backtest.py --csv-dir my_data       # קבצי CSV משלך (Date,Open,High,Low,Close,Volume)
תוצרים בתיקיית results/: summary.md, signals.csv, charts/*.png, equity.png
"""
import argparse
import importlib
import math
import os
import sys
from concurrent.futures import ProcessPoolExecutor

import numpy as np
import pandas as pd

import pullback_scanner as ps

DEFAULT_UNIVERSE = [
    "AAPL", "MSFT", "NVDA", "AMZN", "GOOGL", "META", "TSLA", "AMD", "AVGO", "ORCL",
    "CRM", "ADBE", "NFLX", "COST", "WMT", "HD", "JPM", "V", "MA", "UNH",
    "LLY", "JNJ", "PG", "KO", "PEP", "XOM", "CVX", "CAT", "DE", "LMT",
]
HORIZONS = (5, 10, 20, 60)
LIVE_WINDOW_DAYS = 730          # load() בסורק מוריד period="2y"
DATA_START = "2010-01-01"       # מספיק לחימום + חלון של שנתיים לפני 2016
DAILY_WARMUP = 261              # מתחת לזה הסורק עובר מ-SMA200 ל-SMA40


# ---------------------------------------------------------------- data
def load_history(ticker, cache_dir="data", csv_dir=None, refresh=False):
    """היסטוריה יומית מלאה. CSV משלך > מטמון מקומי > yfinance (מ-DATA_START)."""
    if csv_dir:
        path = os.path.join(csv_dir, f"{ticker}.csv")
        df = pd.read_csv(path, index_col=0, parse_dates=True)
    else:
        path = os.path.join(cache_dir, f"{ticker}.csv")
        if os.path.exists(path) and not refresh:
            df = pd.read_csv(path, index_col=0, parse_dates=True)
        else:
            import yfinance as yf
            df = yf.download(ticker, start=DATA_START, interval="1d",
                             progress=False, auto_adjust=True)
            if df.empty:
                raise ValueError("no data returned")
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)
            df = df[["Open", "High", "Low", "Close", "Volume"]]
            # הנר של היום עלול להיות חלקי (שוק פתוח) - לא שומרים אותו במטמון
            today = pd.Timestamp.now(tz="America/New_York").normalize().tz_localize(None)
            df = df[df.index < today]
            os.makedirs(cache_dir, exist_ok=True)
            df.to_csv(path)
    df.index = pd.to_datetime(df.index).tz_localize(None)
    df = df[["Open", "High", "Low", "Close", "Volume"]].astype(float).dropna()
    return df[df["Volume"] > 0].sort_index()


def prefetch(tickers, cache_dir="data", chunk=50):
    """מוריד במנות את כל הטיקרים שעוד אין להם מטמון - הרבה יותר מהיר מאחד-אחד."""
    missing = [t for t in tickers if not os.path.exists(os.path.join(cache_dir, f"{t}.csv"))]
    if not missing:
        return
    import yfinance as yf
    os.makedirs(cache_dir, exist_ok=True)
    today = pd.Timestamp.now(tz="America/New_York").normalize().tz_localize(None)
    for i in range(0, len(missing), chunk):
        part = missing[i:i + chunk]
        print(f"downloading {i + len(part)}/{len(missing)} ...", flush=True)
        raw = yf.download(part, start=DATA_START, interval="1d", progress=False,
                          auto_adjust=True, group_by="ticker", threads=True)
        for t in part:
            try:
                df = raw[t][["Open", "High", "Low", "Close", "Volume"]].dropna()
            except KeyError:
                continue
            df = df[df.index < today]
            if len(df):
                df.to_csv(os.path.join(cache_dir, f"{t}.csv"))


# ---------------------------------------------------------------- prefilters
# detect() מחזיר None תמיד אם הנר האחרון לא ירוק או שהווליום שלו לא מעל vol_mult*MA20
# (התנאי breakout נדרש לכל אורכי הבסיס). לכן מסננים מראש רק ימים כאלה - זה לא משנה
# את התוצאה, רק חוסך זמן. tests/test_backtest.py מוודא שקילות מלאה מול ריצה בלי סינון.
TOL = 0.995                     # מרווח ביטחון כך שהסינון לעולם לא יפסול איתות אמיתי


def daily_candidates(df, vol_mult=None):
    vma = df["Volume"].rolling(20).mean()
    vm = ps.DAILY["vol_mult"] if vol_mult is None else vol_mult
    return ((df["Close"] > df["Open"]) & (df["Volume"] > TOL * vm * vma)).values


def weekly_candidates(df):
    """הנר השבועי החלקי כפי שהוא נראה בסוף כל יום (בלי מידע מהמשך השבוע)."""
    per = df.index.to_period("W-FRI")
    g = df.groupby(per)
    wk_open = g["Open"].transform("first")
    wk_vol = g["Volume"].cumsum()
    full = df["Volume"].groupby(per).sum()                 # שבועות שהושלמו
    prev19 = full.rolling(19).sum().shift(1)
    avg = (prev19.reindex(per).values + wk_vol.values) / 20
    return ((df["Close"].values > wk_open.values) &
            (wk_vol.values > TOL * ps.WEEKLY["vol_mult"] * avg))


# ---------------------------------------------------------------- walk-forward
def scan_history(df, start=None, end=None, prefilter=True, daily=True, weekly=True, params=None):
    """מריץ את detect() יום-יום. מחזיר רשימת dict - שורה לכל יום עם איתות כלשהו."""
    if hasattr(ps, "clean_event_volume"):      # הגרסה המקורית (v1) לא כוללת את התיקון
        df = ps.clean_event_volume(df)
    idx = df.index
    lo = max(DAILY_WARMUP, idx.searchsorted(pd.Timestamp(start)) if start else 0)
    hi = idx.searchsorted(pd.Timestamp(end), side="right") if end else len(df)
    params = params or ps.DAILY
    dcand = daily_candidates(df, params["vol_mult"]) if prefilter else np.ones(len(df), bool)
    if not daily:
        dcand = np.zeros(len(df), bool)
    wcand = weekly_candidates(df) if prefilter else np.ones(len(df), bool)
    if not weekly:
        wcand = np.zeros(len(df), bool)
    out = []
    for t in range(lo, hi):
        if not (dcand[t] or wcand[t]):
            continue
        t0 = idx.searchsorted(idx[t] - pd.Timedelta(days=LIVE_WINDOW_DAYS))
        win = df.iloc[t0:t + 1]                           # מה שהסורק היה רואה ביום t
        rd = ps.detect(win, params) if dcand[t] else None
        rw = ps.detect(ps.to_weekly(win), ps.WEEKLY) if wcand[t] else None
        if rd or rw:
            out.append(dict(t=t, t0=t0, daily=rd, weekly=rw))
    return out


MARKET_ETF = {"sp500": "SPY", "sp400": "MDY", "sp600": "IJR"}
SECTOR_ETF = {"Information Technology": "XLK", "Financials": "XLF", "Health Care": "XLV",
              "Consumer Discretionary": "XLY", "Consumer Staples": "XLP", "Energy": "XLE",
              "Industrials": "XLI", "Materials": "XLB", "Utilities": "XLU",
              "Real Estate": "XLRE", "Communication Services": "XLC"}


def index_for(ticker, mode, membership="universes/membership.csv"):
    """המדד שהמניה משתייכת אליו: market -> SPY/MDY/IJR, sector -> קרן הסקטור (XLK, XLF...)."""
    if not hasattr(index_for, "_m"):
        index_for._m = (pd.read_csv(membership).set_index("ticker")
                        if os.path.exists(membership) else pd.DataFrame())
    m = index_for._m
    if ticker not in m.index:
        return "SPY" if mode == "market" else None
    row = m.loc[ticker]
    return MARKET_ETF.get(row["index"], "SPY") if mode == "market" else SECTOR_ETF.get(row["sector"])


_INDEX_CACHE = {}


def index_hits(etf, args):
    """איתותי הפולבק היומי של המדד (פרמטרים INDEX), עם מטמון לכל תהליך."""
    if etf not in _INDEX_CACHE:
        df = load_history(etf, args.cache_dir)
        hits = scan_history(df, args.start, args.end, weekly=False, params=ps.INDEX)
        _INDEX_CACHE[etf] = (df, hits)
    return _INDEX_CACHE[etf]


def index_combo_signals(df, hits, idf, ihits, window=5):
    """איתות קנייה: איתות יומי במניה, וגם איתות פולבק במדד שלה באותו יום או עד window ימי מסחר
    לפני כן - כל עוד המדד לא נסגר מתחת ל-base_lo שלו מאז. מחזיר [(stock_hit, index_hit)]."""
    if not hits or not ihits:
        return []
    icl = idf["Close"]
    idates = idf.index
    ih = [(idates[h["t"]], h) for h in ihits]
    out = []
    for h in hits:
        if not h["daily"]:
            continue
        day = df.index[h["t"]]
        pos = idates.searchsorted(day, side="right") - 1            # יום המסחר של המדד <= היום
        if pos < 0:
            continue
        lo_day = idates[max(0, pos - window)]
        cands = [x for d, x in ih if lo_day <= d <= day]
        if not cands:
            continue
        ix = cands[-1]
        if icl.iloc[ix["t"]:pos + 1].min() < ix["daily"]["base_lo"]:
            continue
        out.append((h, ix))
    return out


def combo_signals(df, hits, arm_days=15, require_uptrend=False):
    """איתות משולב: איתות שבועי "דורך" את המניה, ורק אחריו (באותו יום או עד arm_days ימי מסחר)
    איתות יומי מפעיל קנייה. סגירה מתחת ל-base_lo השבועי מבטלת את הדריכה.
    כל הגדרה שבועית נותנת לכל היותר קנייה אחת (אחרי קנייה אין דריכה מחדש למשך arm_days).
    require_uptrend: האיתות היומי מפעיל קנייה רק אם המחיר מעל SMA200; אחרת הדריכה ממשיכה לחכות."""
    if not hits:
        return []
    close = df["Close"].values
    by_t = {h["t"]: h for h in hits}
    out, armed, blocked_until = [], None, -1
    for t in range(hits[0]["t"], min(hits[-1]["t"] + 1, len(df))):
        if armed and (t > armed["until"] or close[t] < armed["lo"]):
            armed = None
        h = by_t.get(t)
        if h is None:
            continue
        if h["weekly"] and armed is None and t > blocked_until:
            armed = dict(hit=h, until=t + arm_days, lo=h["weekly"]["base_lo"])
        if armed and h["daily"] and (not require_uptrend or h["daily"]["uptrend"]):
            out.append(dict(t=t, daily_hit=h, weekly_hit=armed["hit"]))
            armed, blocked_until = None, t + arm_days
    return out


# ---------------------------------------------------------------- outcomes
def atr14(df):
    """ATR של 14 ימים (ממוצע פשוט של True Range). ערך ביום j משתמש רק בנתונים עד j."""
    h, l, c = df["High"].values, df["Low"].values, df["Close"].values
    pc = np.r_[c[0], c[:-1]]
    tr = np.maximum(h - l, np.maximum(abs(h - pc), abs(l - pc)))
    return pd.Series(tr).rolling(14, min_periods=1).mean().values


def simulate_trade(df, t, stop, target_r=2.0, max_hold=20, trail_atr=None, atr=None,
                   return_path=False):
    """כניסה בפתיחת t+1. אם סטופ ויעד באותו נר - מניחים שהסטופ קרה קודם (שמרני).
    trail_atr=k: בלי יעד קבוע; סטופ נגרר = הגבוה ביותר מאז הכניסה פחות k*ATR, מחושב עד אתמול
    בלבד, ולעולם לא יורד. הסטופ ההתחלתי (base_lo) נשאר רצפה."""
    if t + 1 >= len(df):
        return None
    o, h, l, c = (df[k].values for k in ("Open", "High", "Low", "Close"))
    entry = o[t + 1]
    if entry <= stop:
        return dict(entry=entry, exit=entry, R=np.nan, ret=0.0, exit_reason="gap_below_stop",
                    bars=0, mfe=np.nan, mae=np.nan)
    risk = entry - stop
    init_stop = stop
    target = np.inf if trail_atr else entry + target_r * risk
    if trail_atr and atr is None:
        atr = atr14(df)
    last = min(t + max_hold, len(df) - 1)
    reason, px, j = "time", c[last], last
    hh = -np.inf
    path = []                                              # הסטופ שהיה בתוקף בכל יום (לגרף)
    for j in range(t + 1, last + 1):
        if trail_atr and j > t + 1:
            hh = max(hh, h[j - 1])
            stop = max(stop, hh - trail_atr * atr[j - 1])
        path.append(stop)
        kind = "trail" if stop > init_stop else "stop"
        if j > t + 1 and o[j] <= stop:
            reason, px = kind + "_gap", o[j]; break
        if j > t + 1 and o[j] >= target:
            reason, px = "target_gap", o[j]; break
        if l[j] <= stop:
            reason, px = kind, stop; break
        if h[j] >= target:
            reason, px = "target", target; break
    else:
        j = last
        if last < t + max_hold:
            reason = "open"                                # עדיין לא הסתיימה
    seg = slice(t + 1, j + 1)
    out = dict(entry=entry, exit=px, R=(px - entry) / risk, ret=px / entry - 1,
               exit_reason=reason, bars=j - t, risk_pct=risk / entry,
               mfe=h[seg].max() / entry - 1, mae=l[seg].min() / entry - 1)
    if return_path:
        out.update(stop_path=path[:j - t], exit_pos=j, init_stop=init_stop)
    return out


def forward_returns(df):
    """תשואה מפתיחת t+1 עד סגירת t+h, לכל יום t. משמש גם לאיתותים וגם לבסיס ההשוואה."""
    nxt_open = df["Open"].shift(-1)
    return pd.DataFrame({f"fwd{h}": df["Close"].shift(-h) / nxt_open - 1 for h in HORIZONS},
                        index=df.index)


def use_scanner(name):
    """בוחר איזו גרסה של הסורק נבדקת (pullback_scanner / pullback_scanner_v1)."""
    global ps
    ps = importlib.import_module(name)


def make_row(df, fwd, ticker, kind, hit, res, args, atr=None):
    t = hit["t"]
    row = dict(ticker=ticker, date=df.index[t].date(), tpos=t, kind=kind,
               both=hit["daily"] is not None and hit["weekly"] is not None,
               score=int(res["score"]), drop=float(res["drop"]),
               slowing=bool(res["slowing"]), drying=bool(res["drying"]),
               uptrend=bool(res["uptrend"]),
               decline_len=res["slow"] - res["peak"],
               slowdown_len=res["base"] - res["slow"],
               base_len=res["rise"] - res["base"],
               base_hi=float(res["base_hi"]), base_lo=float(res["base_lo"]),
               close=df["Close"].iloc[t])
    if kind != "weekly":
        # מדידה ישירה על המחירים, זהה לשתי הגרסאות: כמה הבסיס מעל השפל האמיתי
        pk = hit["t0"] + res["offset"] + res["peak"]
        low_i = pk + int(np.argmin(df["Low"].values[pk:t]))
        row.update(peak_to_low=low_i - pk,
                   base_above_low=res["base_lo"] / df["Low"].iloc[low_i] - 1)
    row.update(fwd.iloc[t].to_dict())
    tr = simulate_trade(df, t, res["base_lo"], args.target_r, args.max_hold,
                        args.trail_atr, atr)
    if tr:
        row.update(tr)
    return row


def focus_kind(args):
    return ("combo" if args.combo or args.index_combo
            else "weekly" if args.weekly_only else "daily")


def run_ticker(ticker, args):
    use_scanner(args.scanner)
    df = load_history(ticker, args.cache_dir, args.csv_dir, args.refresh)
    hits = scan_history(df, args.start, args.end, prefilter=not args.no_prefilter,
                        daily=not args.weekly_only, weekly=not args.index_combo)
    fwd = forward_returns(df)
    lo = bt_lo(df, args.start)
    hi = df.index.searchsorted(pd.Timestamp(args.end), side="right") if args.end else len(df)
    base = fwd.iloc[lo:hi].assign(ticker=ticker)
    atr = atr14(df) if args.trail_atr else None
    rows = []
    for hit in hits:
        for kind in ("daily", "weekly"):
            if hit[kind] is not None:
                rows.append(make_row(df, fwd, ticker, kind, hit, hit[kind], args, atr))
    if args.index_combo:
        etf = index_for(ticker, args.index_combo)
        if etf:
            idf, ihits = index_hits(etf, args)
            for h, ix in index_combo_signals(df, hits, idf, ihits, args.index_window):
                row = make_row(df, fwd, ticker, "combo", h, h["daily"], args, atr)
                row.update(index=etf, index_date=idf.index[ix["t"]].date(), index_tpos=ix["t"],
                           index_score=int(ix["daily"]["score"]),
                           index_drop=float(ix["daily"]["drop"]),
                           days_after_index=int(idf.index.searchsorted(df.index[h["t"]], side="right")
                                                - 1 - ix["t"]))
                rows.append(row)
    if args.combo:
        for c in combo_signals(df, hits, args.arm_days, args.require_uptrend):
            wk = c["weekly_hit"]
            row = make_row(df, fwd, ticker, "combo", c["daily_hit"], c["daily_hit"]["daily"], args, atr)
            row.update(weekly_date=df.index[wk["t"]].date(), weekly_tpos=wk["t"],
                       days_after_weekly=c["t"] - wk["t"], weekly_score=int(wk["weekly"]["score"]),
                       weekly_base_lo=float(wk["weekly"]["base_lo"]))
            rows.append(row)
    return ticker, rows, base, hits, df


# ---------------------------------------------------------------- statistics
def welch(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    a, b = a[~np.isnan(a)], b[~np.isnan(b)]
    if len(a) < 2 or len(b) < 2:
        return np.nan, np.nan
    se = math.sqrt(a.var(ddof=1) / len(a) + b.var(ddof=1) / len(b))
    t = (a.mean() - b.mean()) / se if se else np.nan
    return t, math.erfc(abs(t) / math.sqrt(2))           # p דו-צדדי, קירוב נורמלי


def boot_ci(x, n=2000, seed=0):
    x = np.asarray(x, float)
    x = x[~np.isnan(x)]
    if len(x) < 5:
        return np.nan, np.nan
    if len(x) > 5000:   # מדגם גדול: קירוב נורמלי, בלי מטריצה של n*len(x) בזיכרון
        se = x.std(ddof=1) / math.sqrt(len(x))
        return x.mean() - 1.96 * se, x.mean() + 1.96 * se
    rng = np.random.default_rng(seed)
    m = rng.choice(x, (n, len(x))).mean(1)
    return np.percentile(m, 2.5), np.percentile(m, 97.5)


def dedupe(sig, cooldown):
    """איתות שחוזר על אותה מניה תוך cooldown ימי מסחר נחשב כפילות של אותה פריצה."""
    if cooldown <= 0 or sig.empty:
        return sig
    keep = []
    for (_, _), g in sig.sort_values("date").groupby(["ticker", "kind"]):
        last = None
        for i, d in zip(g.index, g["tpos"]):
            if last is None or d - last > cooldown:
                keep.append(i)
                last = d
    return sig.loc[keep]


def trade_stats(g):
    r = g["R"].dropna()
    closed = g[g["exit_reason"] != "open"]["R"].dropna()
    wins, losses = closed[closed > 0], closed[closed <= 0]
    lo, hi = boot_ci(closed)
    return dict(n=len(g), trades=len(closed),
                win_rate=len(wins) / len(closed) if len(closed) else np.nan,
                avg_R=closed.mean() if len(closed) else np.nan, R_ci95=f"[{lo:.2f}, {hi:.2f}]",
                profit_factor=wins.sum() / -losses.sum() if losses.sum() < 0 else np.nan,
                avg_risk_pct=g["risk_pct"].mean() if "risk_pct" in g else np.nan,
                stopped=(g["exit_reason"].isin(["stop", "stop_gap"])).mean(),
                trailed=(g["exit_reason"].isin(["trail", "trail_gap"])).mean(),
                hit_target=(g["exit_reason"].isin(["target", "target_gap"])).mean(),
                gap_below_stop=(g["exit_reason"] == "gap_below_stop").mean(),
                total_R=r.sum())


def random_control(hits_by, sig, args, stride=3, seed=0):
    """אותם כללי יציאה בדיוק, אבל כניסה בימים אקראיים: סטופ במרחק אחוזי שנדגם מהאיתותים.
    אם האיתותים לא טובים מזה - הרווח מגיע מכללי היציאה ומהשוק העולה, לא מהדפוס."""
    focus = focus_kind(args)
    risks = sig.loc[sig.kind == focus, "risk_pct"].dropna().values
    if not len(risks):
        return pd.DataFrame()
    rng = np.random.default_rng(seed)
    rows = []
    for tk, (_, df) in hits_by.items():
        lo = bt_lo(df, args.start)
        hi = df.index.searchsorted(pd.Timestamp(args.end), side="right") if args.end else len(df)
        o = df["Open"].values
        atr = atr14(df) if args.trail_atr else None
        # במצב require_uptrend משווים רק לימים אקראיים שגם בהם המחיר מעל SMA200 - השוואה הוגנת
        up = (df["Close"] > df["Close"].rolling(200).mean()).values if args.require_uptrend else None
        for t in range(lo, hi - 1, stride):
            if up is not None and not up[t]:
                continue
            r = simulate_trade(df, t, o[t + 1] * (1 - rng.choice(risks)), args.target_r,
                               args.max_hold, args.trail_atr, atr)
            if r:   # רק העמודות ש-trade_stats צריך - ביוניברס גדול יש מיליון עסקאות
                rows.append((r["R"], r["exit_reason"], r.get("risk_pct", np.nan)))
    return pd.DataFrame(rows, columns=["R", "exit_reason", "risk_pct"])


def bt_lo(df, start):
    return max(DAILY_WARMUP, df.index.searchsorted(pd.Timestamp(start)))


def fmt_table(df, floats="{:.3f}"):
    cols = list(df.columns)
    lines = ["| " + " | ".join([df.index.name or ""] + cols) + " |",
             "|" + "---|" * (len(cols) + 1)]
    for i, row in df.iterrows():
        cells = []
        for col, v in zip(cols, row):
            if isinstance(v, (float, np.floating)) and v == v and float(v).is_integer() \
                    and (abs(v) >= 10 or v == 0 or col in ("n", "trades")):
                cells.append(f"{int(v):,}")
            elif isinstance(v, (float, np.floating)):
                cells.append("" if np.isnan(v) else floats.format(v))
            else:
                cells.append(str(v))
        lines.append("| " + " | ".join([str(i)] + cells) + " |")
    return "\n".join(lines)


# ---------------------------------------------------------------- report
def build_report(sig, base, args, out, control=None):
    L = [f"# Pullback scanner - backtest report (`{args.scanner}.py`)",
         "",
         f"* tickers: {sig['ticker'].nunique() if len(sig) else 0} / {base['ticker'].nunique()}"
         f" | period: {args.start} -> {args.end or 'today'}",
         f"* entry: next open | stop: base_lo | "
         + (f"exit: trailing stop {args.trail_atr}*ATR14 from highest high, no target"
            if args.trail_atr else f"target: {args.target_r}R")
         + f" | max hold: {args.max_hold} days"
         f" | dedupe cooldown: {args.cooldown} bars"
         + (f" | combo: daily signal within {args.arm_days} days after a weekly signal"
            if args.combo else "")
         + (f" | index combo ({args.index_combo}): stock daily signal + index pullback signal "
            f"within {args.index_window} days" if args.index_combo else ""),
         f"* baseline = every trading day of the same tickers, same period"
         f" ({len(base):,} days)",
         ""]
    if sig.empty:
        L.append("**No signals found.**")
        open(os.path.join(out, "summary.md"), "w", encoding="utf-8").write("\n".join(L))
        return "\n".join(L)

    groups = {"daily": sig[sig.kind == "daily"],
              "weekly": sig[sig.kind == "weekly"],
              "BUY SIGNAL (daily+weekly)": sig[(sig.kind == "daily") & sig.both],
              "combo": sig[sig.kind == "combo"]}
    focus = focus_kind(args)
    groups = {k: g for k, g in groups.items() if len(g) or k == focus}

    # 1. forward returns vs baseline
    L += ["## 1. Forward returns vs baseline (next open -> close t+h)", ""]
    rows = {}
    for h in HORIZONS:
        c = f"fwd{h}"
        b = base[c].dropna()
        rows[f"baseline {h}d"] = dict(n=len(b), mean=b.mean(), median=b.median(),
                                      pct_up=(b > 0).mean(), t_vs_base=np.nan, p=np.nan)
        for name, g in groups.items():
            x = g[c].dropna()
            t, p = welch(x, b)
            rows[f"{name} {h}d"] = dict(n=len(x), mean=x.mean() if len(x) else np.nan,
                                        median=x.median() if len(x) else np.nan,
                                        pct_up=(x > 0).mean() if len(x) else np.nan,
                                        t_vs_base=t, p=p)
    t1 = pd.DataFrame(rows).T
    t1["n"] = t1["n"].astype(int)
    t1.index.name = "group / horizon"
    L += [fmt_table(t1), "",
          "> p is a normal-approx Welch test. Baseline days overlap, so treat p as optimistic.", ""]

    # 2. trade simulation
    L += ["## 2. Trade simulation with the scanner's own levels", ""]
    t2 = {k: trade_stats(g) for k, g in groups.items() if len(g)}
    if control is not None and len(control):
        t2["CONTROL: random days, same exits"] = trade_stats(control.assign(risk_pct=control["risk_pct"]))
    t2 = pd.DataFrame(t2).T
    t2.index.name = "group"
    L += [fmt_table(t2), "",
          "> CONTROL = same entry/stop/target/time rules on every 3rd trading day of the same tickers,",
          "> stop distance drawn from the tested signals' risk distribution. The pattern adds value",
          "> only if its avg_R is clearly above the control's.", ""]
    if control is not None and len(control):
        cr = control[control["exit_reason"] != "open"]["R"]
        for k, g in groups.items():
            x = g[g["exit_reason"] != "open"]["R"]
            if len(x) > 2:
                t, p = welch(x, cr)
                L.append(f"* {k} vs CONTROL: avg_R diff = {x.mean() - cr.mean():+.3f}R,"
                         f" t = {t:.2f}, p = {p:.3f}")
        L.append("")
    if args.require_uptrend:
        L += ["> require-uptrend: buy only when price > SMA200; CONTROL also samples only days with price > SMA200.", ""]

    # 3. does the score / its components carry information?
    d = groups[focus]
    L += [f"## 3. {focus.title()} signals split by score and by each component", ""]
    parts = {f"score={s}": d[d.score == s] for s in sorted(d.score.unique())}
    for f in ("slowing", "drying", "uptrend"):
        parts[f"{f}=True"] = d[d[f]]
        parts[f"{f}=False"] = d[~d[f]]
    t3 = pd.DataFrame({k: {**trade_stats(g), "fwd20": g["fwd20"].mean()}
                       for k, g in parts.items() if len(g)}).T
    t3 = t3[["n", "trades", "win_rate", "avg_R", "R_ci95", "profit_factor", "fwd20"]]
    t3.index.name = "split"
    L += [fmt_table(t3), ""]

    L += ["Phase lengths found by detect() (bars):", "",
          fmt_table(d[[c for c in ("decline_len", "slowdown_len", "base_len", "peak_to_low",
                               "base_above_low") if c in d]].describe()
                    .T[["mean", "min", "50%", "max"]].rename_axis("phase")), ""]

    # 4. per year
    L += [f"## 4. {focus.title()} signals per year", ""]
    yr = d.assign(year=pd.to_datetime(d["date"]).dt.year)
    t4 = pd.DataFrame({y: {**trade_stats(g), "fwd20": g["fwd20"].mean()}
                       for y, g in yr.groupby("year")}).T
    t4 = t4[["n", "win_rate", "avg_R", "total_R", "fwd20"]]
    t4.index.name = "year"
    L += [fmt_table(t4), ""]

    # 5. per ticker
    L += [f"## 5. {focus.title()} signals per ticker"
          + (" (15 worst and 15 best by total_R)" if d["ticker"].nunique() > 40 else ""), ""]
    t5 = pd.DataFrame({tk: {**trade_stats(g), "fwd20": g["fwd20"].mean()}
                       for tk, g in d.groupby("ticker")}).T
    t5 = t5[["n", "win_rate", "avg_R", "total_R", "fwd20"]].sort_values("total_R")
    if len(t5) > 40:
        t5 = pd.concat([t5.head(15), t5.tail(15)])
    t5.index.name = "ticker"
    L += [fmt_table(t5), ""]

    text = "\n".join(L)
    with open(os.path.join(out, "summary.md"), "w", encoding="utf-8") as f:
        f.write(text)
    return text


def equity_chart(sig, path):
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(11, 4.5))
    for name, g, col in (("daily", sig[sig.kind == "daily"], "#185FA5"),
                         ("weekly", sig[sig.kind == "weekly"], "#A32D2D"),
                         ("daily+weekly", sig[(sig.kind == "daily") & sig.both], "#3B6D11"),
                         ("combo weekly->daily", sig[sig.kind == "combo"], "#7A4FB0")):
        g = g.dropna(subset=["R"]).sort_values("date")
        if len(g):
            ax.plot(pd.to_datetime(g["date"]), g["R"].cumsum(), label=f"{name} (n={len(g)})",
                    color=col, lw=1.6)
    ax.axhline(0, color="#888", lw=0.8)
    ax.set_ylabel("cumulative R (1R = risk per trade)")
    ax.set_title("Cumulative R of all signals, in date order")
    ax.legend(loc="upper left")
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(path, dpi=110)
    plt.close(fig)


def signal_chart(df, hit, kind, ticker, path, after=20, marks=(), note=""):
    """גרף הסורק עצמו (ps.plot) ביום האיתות + `after` נרות של מה שקרה אחר כך."""
    t, t0 = hit["t"], hit["t0"]
    res = hit[kind]
    before = res["rise"] - res["peak"] + 12           # תמיד להראות את השיא ועוד קצת לפניו
    if kind == "daily":
        ext = df.iloc[t0:t + 1 + after]                    # האינדקסים של res נשארים תקפים
        bars = max(80, before) + min(after, len(df) - 1 - t)
    else:
        win_w = ps.to_weekly(df.iloc[t0:t + 1])
        later = ps.to_weekly(df.iloc[t + 1:t + 1 + after * 5])
        later = later[later.index > win_w.index[-1]]     # בלי שארית השבוע של יום האיתות
        ext = pd.concat([win_w, later.iloc[:after // 4 or 1]])
        bars = max(60, before) + (len(ext) - len(win_w))
    unit = "1 candle = 1 day" if kind == "daily" else "1 candle = 1 week"
    ps.plot(ext, res, f"{ticker} {kind.upper()} [{unit}] signal {df.index[t].date()}{note} (+{after} bars after)",
            path, bars=min(bars, len(ext)), marks=marks)


def stacked_chart(df, daily_hit, weekly_hit, ticker, path, after=20):
    """גרף יומי ביום הקנייה למעלה, וגרף שבועי ביום האיתות השבועי שדרך את המניה למטה."""
    import matplotlib.pyplot as plt
    tmp = [path + s for s in (".d.png", ".w.png")]
    d_day, w_day = df.index[daily_hit["t"]], df.index[weekly_hit["t"]]
    gap = daily_hit["t"] - weekly_hit["t"]
    # כל פאנל מסמן את התאריך של האיתות השני, כי לשני הגרפים יש סקאלת זמן שונה
    signal_chart(df, daily_hit, "daily", ticker, tmp[0], after=after,
                 note=f" = BUY, {gap} days after weekly",
                 marks=[(w_day, f"W signal {w_day.date()}", "#7A4FB0")])
    signal_chart(df, weekly_hit, "weekly", ticker, tmp[1], after=after,
                 note=" = arming",
                 marks=[(d_day, f"D buy {d_day.date()}", "#185FA5")])
    fig, axes = plt.subplots(2, 1, figsize=(12, 14))
    for ax, p in zip(axes, tmp):
        ax.imshow(plt.imread(p))
        ax.axis("off")
    fig.tight_layout()
    fig.savefig(path, dpi=100)
    plt.close(fig)
    for p in tmp:
        os.remove(p)


def trade_chart(df, t, stop, ticker, path, trail_atr=3.0, max_hold=60, before=40, title=""):
    """גרף יומי של עסקה: כניסה, סטופ התחלתי, הסטופ הנגרר יום-יום, ויציאה."""
    import matplotlib.pyplot as plt
    tr = simulate_trade(df, t, stop, max_hold=max_hold, trail_atr=trail_atr, return_path=True)
    a, b = max(0, t - before), min(len(df), tr["exit_pos"] + 8)
    d = df.iloc[a:b]
    fig, (ax, axv) = plt.subplots(2, 1, figsize=(12, 6.5), sharex=True,
                                  gridspec_kw={"height_ratios": [3, 1]})
    for i, (o, h, l, c) in enumerate(d[["Open", "High", "Low", "Close"]].values):
        col = "#3B6D11" if c >= o else "#A32D2D"
        ax.vlines(i, l, h, color=col, lw=1)
        ax.add_patch(plt.Rectangle((i - 0.3, min(o, c)), 0.6, max(abs(c - o), 1e-6), color=col))
    axv.bar(range(len(d)), d["Volume"], color=np.where(d["Close"] >= d["Open"], "#97C459", "#F09595"))
    e0 = t + 1 - a                                          # נר הכניסה
    xs = np.arange(e0, e0 + len(tr["stop_path"]))
    ax.step(xs, tr["stop_path"], where="mid", color="#A32D2D", lw=1.8, label=f"trailing stop ({trail_atr}xATR)")
    ax.hlines(tr["init_stop"], e0 - 3, e0 + 3, color="#A32D2D", ls="--", lw=1, label="initial stop (base low)")
    ax.axvspan(e0 - 0.5, tr["exit_pos"] - a + 0.5, color="#B5D4F4", alpha=0.25, lw=0)
    ax.plot(e0, tr["entry"], marker="^", color="#185FA5", ms=11, ls="", label=f"entry {tr['entry']:.2f}")
    col = "#3B6D11" if tr["R"] > 0 else "#A32D2D"
    ax.plot(tr["exit_pos"] - a, tr["exit"], marker="v", color=col, ms=11, ls="",
            label=f"exit {tr['exit']:.2f} ({tr['exit_reason']}, {tr['bars']} days)")
    ax.set_title(f"{ticker}  {title}  |  result {tr['R']:+.2f}R  ({tr['ret']:+.1%})")
    ax.legend(loc="upper left", fontsize=8)
    step = max(1, len(d) // 8)
    axv.set_xticks(range(0, len(d), step))
    axv.set_xticklabels([x.strftime("%Y-%m-%d") for x in d.index[::step]], fontsize=8)
    fig.tight_layout()
    fig.savefig(path, dpi=105)
    plt.close(fig)
    return tr


def index_stacked_chart(df, hit, idf, ihit, ticker, etf, path, after=20):
    """למעלה: המניה ביום הקנייה. למטה: המדד שלה ביום איתות הפולבק שלו. כל פאנל מסמן את התאריך של השני."""
    import matplotlib.pyplot as plt
    tmp = [path + s for s in (".s.png", ".i.png")]
    s_day, i_day = df.index[hit["t"]], idf.index[ihit["t"]]
    signal_chart(df, hit, "daily", ticker, tmp[0], after=after, note=" = BUY",
                 marks=[(i_day, f"{etf} signal {i_day.date()}", "#7A4FB0")])
    signal_chart(idf, ihit, "daily", etf, tmp[1], after=after, note=f" = index pullback ({ticker}'s index)",
                 marks=[(s_day, f"{ticker} buy {s_day.date()}", "#185FA5")])
    fig, axes = plt.subplots(2, 1, figsize=(12, 14))
    for ax, p in zip(axes, tmp):
        ax.imshow(plt.imread(p))
        ax.axis("off")
    fig.tight_layout()
    fig.savefig(path, dpi=100)
    plt.close(fig)
    for p in tmp:
        os.remove(p)


# ---------------------------------------------------------------- main
def main(argv=None):
    ap = argparse.ArgumentParser(description="Walk-forward backtest for pullback_scanner.py")
    ap.add_argument("tickers", nargs="*", help="default: built-in large-cap universe")
    ap.add_argument("--universe", nargs="+", default=[],
                    help="text file(s) with one ticker per line, e.g. universes/sp500.txt")
    ap.add_argument("--combo", action="store_true",
                    help="weekly signal arms the stock, a later daily signal triggers the buy")
    ap.add_argument("--arm-days", type=int, default=15,
                    help="combo: trading days after the weekly signal in which a daily signal counts")
    ap.add_argument("--index-combo", choices=["market", "sector"], default=None,
                    help="buy when the stock's daily signal coincides with a pullback signal in its index "
                         "(market: SPY/MDY/IJR, sector: XLK/XLF/...)")
    ap.add_argument("--index-window", type=int, default=5,
                    help="index signal may come up to N trading days before the stock signal")
    ap.add_argument("--require-uptrend", action="store_true",
                    help="combo: the daily trigger must have price above SMA200 (control matches)")
    ap.add_argument("--weekly-only", action="store_true",
                    help="skip daily detection (much faster for large universes)")
    ap.add_argument("--start", default="2016-01-01")
    ap.add_argument("--end", default=None)
    ap.add_argument("--target-r", type=float, default=2.0, help="profit target in R (default 2)")
    ap.add_argument("--max-hold", type=int, default=20, help="time exit in trading days")
    ap.add_argument("--trail-atr", type=float, default=None,
                    help="trailing stop: highest high since entry minus K*ATR14, no fixed target")
    ap.add_argument("--cooldown", type=int, default=5,
                    help="ignore repeat signals of the same ticker within N bars (0 = keep all)")
    ap.add_argument("--charts", type=int, default=12, help="how many signal charts to draw")
    ap.add_argument("--out", default="results")
    ap.add_argument("--scanner", default="pullback_scanner",
                    help="module to test: pullback_scanner (fixed) or pullback_scanner_v1 (original)")
    ap.add_argument("--cache-dir", default="data")
    ap.add_argument("--csv-dir", default=None, help="read <TICKER>.csv from here instead of yfinance")
    ap.add_argument("--refresh", action="store_true", help="re-download instead of using cache")
    ap.add_argument("--no-prefilter", action="store_true", help="slow path, for verification")
    ap.add_argument("--jobs", type=int, default=os.cpu_count() or 1)
    args = ap.parse_args(argv)
    tickers = [t.upper() for t in args.tickers]
    for path in args.universe:
        tickers += [ln.strip().upper() for ln in open(path, encoding="utf-8") if ln.strip()]
    tickers = list(dict.fromkeys(tickers)) or DEFAULT_UNIVERSE
    use_scanner(args.scanner)
    os.makedirs(os.path.join(args.out, "charts"), exist_ok=True)

    # הורדה במנות, סריקה במקביל
    if not args.csv_dir and not args.refresh:
        prefetch(tickers, args.cache_dir)
    ok = []
    for tk in tickers:
        try:
            load_history(tk, args.cache_dir, args.csv_dir, args.refresh)
            ok.append(tk)
        except Exception as e:
            print(f"{tk:6s} data error: {e}")
    args.refresh = False

    all_rows, bases, hits_by = [], [], {}
    with ProcessPoolExecutor(max_workers=max(1, args.jobs)) as ex:
        futs = {tk: ex.submit(run_ticker, tk, args) for tk in ok}
        for tk, fu in futs.items():
            try:
                _, rows, base, hits, df = fu.result()
            except Exception as e:
                print(f"{tk:6s} error: {e}")
                continue
            nd = sum(r["kind"] == "daily" for r in rows)
            nw = sum(r["kind"] == "weekly" for r in rows)
            nc = sum(r["kind"] == "combo" for r in rows)
            print(f"{tk:6s} {len(df):5d} bars  daily signals={nd:3d}  weekly signals={nw:3d}"
                  + (f"  combo={nc:3d}" if args.combo or args.index_combo else ""))
            all_rows += rows
            bases.append(base)
            hits_by[tk] = (hits, df)

    sig = pd.DataFrame(all_rows)
    base = pd.concat(bases) if bases else pd.DataFrame(columns=["ticker"])
    raw_n = len(sig)
    sig = dedupe(sig, args.cooldown).sort_values(["date", "ticker"]) if raw_n else sig
    if raw_n:
        print(f"\n{raw_n} raw signals -> {len(sig)} after {args.cooldown}-bar dedupe")
        sig.drop(columns=["tpos"]).to_csv(os.path.join(args.out, "signals.csv"), index=False)
        equity_chart(sig, os.path.join(args.out, "equity.png"))
        _draw_samples(sig, hits_by, args)
    control = random_control(hits_by, sig, args) if raw_n else None
    print()
    print(build_report(sig, base, args, args.out, control))
    print(f"\nresults written to {os.path.abspath(args.out)}/")


def _draw_samples(sig, hits_by, args):
    """דוגמה אקראית (קבועה) של איתותים יומיים, כדי לבדוק בעין שהדפוס באמת נראה כמו פולבק."""
    if args.charts <= 0:
        return
    if args.index_combo:
        pick = sig[sig.kind == "combo"]
        for _, r in pick.sample(min(args.charts, len(pick)), random_state=1).iterrows():
            hits, df = hits_by[r["ticker"]]
            idf, ihits = index_hits(r["index"], args)
            sh = {h["t"]: h for h in hits}[r["tpos"]]
            ih = {h["t"]: h for h in ihits}[r["index_tpos"]]
            name = f"{r['ticker']}_{r['date']}_{r['index']}_{r.get('exit_reason', 'na')}.png"
            try:
                index_stacked_chart(df, sh, idf, ih, r["ticker"], r["index"],
                                    os.path.join(args.out, "charts", name))
            except Exception as e:
                print("chart error", name, e)
        return
    if args.combo:
        pick = sig[sig.kind == "combo"]
        for _, r in pick.sample(min(args.charts, len(pick)), random_state=1).iterrows():
            hits, df = hits_by[r["ticker"]]
            by_t = {h["t"]: h for h in hits}
            name = f"{r['ticker']}_{r['date']}_combo_{r.get('exit_reason', 'na')}.png"
            try:
                stacked_chart(df, by_t[r["tpos"]], by_t[r["weekly_tpos"]], r["ticker"],
                              os.path.join(args.out, "charts", name))
            except Exception as e:
                print("chart error", name, e)
        return
    pick = sig[sig.kind == "daily"]
    pick = pick.sample(min(args.charts, len(pick)), random_state=1) if len(pick) else pick
    wk = sig[sig.kind == "weekly"]
    n_wk = args.charts if args.weekly_only else max(args.charts // 3, 1)
    pick = pd.concat([pick, wk.sample(min(n_wk, len(wk)), random_state=1)
                      if len(wk) else wk])
    for _, r in pick.iterrows():
        hits, df = hits_by[r["ticker"]]
        hit = next(h for h in hits if h["t"] == r["tpos"])
        name = f"{r['ticker']}_{r['date']}_{r['kind']}_{r.get('exit_reason', 'na')}.png"
        try:
            signal_chart(df, hit, r["kind"], r["ticker"], os.path.join(args.out, "charts", name))
        except Exception as e:
            print("chart error", name, e)


if __name__ == "__main__":
    main()
