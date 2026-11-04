"""
mtf_strategy.py - אסטרטגיה רב-שכבתית: יומי -> שעתי -> 5 דקות.

  1. יומי  : התכנסות ממוצעים נעים (SMA 10/20/50/100/150/200 בטווח של D_SPREAD מהמחיר, באחד מ-D_CONV_DAYS
              הימים האחרונים), והמחיר נסגר מעל כולם לראשונה (לא היה מעל כולם ב-D_FIRST הימים הקודמים).
              D_HOLD>1: ממתינים שהמחיר יישאר מעל כולם D_HOLD ימים ברצף ויעלה מאז הפריצה - האיתות ביום ה-D_HOLD.
              האיתות "חמוש" ל-ARM_DAYS ימי המסחר הבאים.
  2. שעתי  : התכנסות ממוצעים שעתיים (SMA 10/20/50/100 בטווח של H_SPREAD) בנר השעתי האחרון שנסגר.
  3. 5 דקות: RSI(14) מתחת ל-RSI_OS ב-RSI_LOOK הנרות האחרונים, ואז חיתוך MACD(12,26,9) כלפי מעלה
              -> קנייה בפתיחת הנר הבא. לא נכנסים אחרי 15:30. עסקה אחת למניה ביום.
  יציאות: eod   - סגירת היום;
          2R    - סטופ בשפל 12 הנרות האחרונים (הירידה), יעד 2R, אחרת סגירת היום;
          next  - אותו סטופ, בלי יעד, יציאה בסגירת יום המסחר הבא.
  עלות 5bp לכל צד. בלי הצצה לעתיד: יומי עד סגירת אתמול, שעתי עד הנר שנסגר, 5 דקות עד סגירת נר האיתות.

בסיסי השוואה (כל עסקה מתויגת לפי השכבות שהיא עוברת, ולכן אפשר לבודד כל שכבה):
  * אותו טריגר 5 דקות בלי הפילטרים;  * כניסה בשעה אקראית באותם ימים/מניות.

הרצה:  python mtf_strategy.py --out results_mtf
"""
import argparse
import os
from concurrent.futures import ProcessPoolExecutor

import numpy as np
import pandas as pd

import mtf_data as md

D_MAS = (10, 20, 50, 100, 150, 200)
H_MAS = (10, 20, 50, 100)
P = dict(D_SPREAD=0.05, D_CONV_DAYS=10, D_FIRST=20, D_HOLD=1, ARM_DAYS=5, H_SPREAD=0.02, RSI_OS=30, RSI_LOOK=6,
         STOP_BARS=12, COST=0.0005)


def rsi(c, n=14):
    d = np.diff(c, prepend=np.nan)
    up = pd.Series(np.where(d > 0, d, 0.0)).ewm(alpha=1 / n, adjust=False).mean().values
    dn = pd.Series(np.where(d < 0, -d, 0.0)).ewm(alpha=1 / n, adjust=False).mean().values
    with np.errstate(divide="ignore", invalid="ignore"):
        return 100 - 100 / (1 + up / dn)


def macd(c, f=12, s=26, g=9):
    c = pd.Series(c)
    m = c.ewm(span=f, adjust=False).mean() - c.ewm(span=s, adjust=False).mean()
    return m.values, m.ewm(span=g, adjust=False).mean().values


def daily_signals(df, p=P):
    """מחזיר DataFrame יומי עם spread, above_all, signal (יום t, ידוע בסגירה)."""
    c = df["Close"]
    mas = pd.concat([c.rolling(n).mean() for n in D_MAS], axis=1)
    spread = (mas.max(axis=1) - mas.min(axis=1)) / c
    above = (c > mas.max(axis=1)) & mas.notna().all(axis=1)
    conv = (spread <= p["D_SPREAD"]).rolling(p["D_CONV_DAYS"], min_periods=1).max().astype(bool)
    prev_above = above.shift(1).rolling(p["D_FIRST"], min_periods=1).max().fillna(1).astype(bool)
    start = above & conv & ~prev_above                     # היום הראשון מעל כל הממוצעים
    n = p.get("D_HOLD", 1)
    if n <= 1:
        sig = start
    else:
        # המתנה: המחיר נשאר מעל כל הממוצעים n ימים ברצף מאז הפריצה, והסגירה ביום ה-n גבוהה מסגירת יום הפריצה
        run = above.groupby((~above).cumsum()).cumsum()
        sig = (run == n) & start.shift(n - 1, fill_value=False) & (c > c.shift(n - 1))
    return pd.DataFrame(dict(spread=spread, above=above, signal=sig), index=df.index)


def armed_dates(dsig, k):
    """ימי מסחר שבהם איתות יומי חמוש: t+1 .. t+k (האיתות ידוע רק בסגירת t)."""
    idx = dsig.index
    out = {}
    for i in np.nonzero(dsig["signal"].values)[0]:
        for j in range(i + 1, min(i + 1 + k, len(idx))):
            out.setdefault(idx[j].date(), idx[i].date())
    return out


def hourly_flags(h, p=P):
    c = h["Close"]
    mas = pd.concat([c.rolling(n).mean() for n in H_MAS], axis=1)
    spread = ((mas.max(axis=1) - mas.min(axis=1)) / c).values
    above = (c > mas.max(axis=1)).values
    start = h.index
    end = start + pd.Timedelta(minutes=60)
    close_t = start.normalize() + pd.Timedelta(hours=16)
    end = end.where(end <= close_t, close_t)
    return end, spread, above


def simulate(o, hi, lo, c, day_id, e, stop, target, exit_day_id):
    """5 דקות: כניסה בפתיחת e; יציאה בסטופ/יעד או בסגירת הנר האחרון של exit_day_id."""
    entry = o[e]
    n = len(c)
    for j in range(e, n):
        if day_id[j] > exit_day_id:
            return entry, c[j - 1], "time"
        if stop == stop:
            if j > e and day_id[j] != day_id[j - 1] and o[j] <= stop:
                return entry, o[j], "stop"
            if lo[j] <= stop:
                return entry, stop, "stop"
        if target == target and hi[j] >= target:
            return entry, target, "target"
    return entry, c[n - 1], "open"


def run_ticker(args):
    tk, p, seed = args
    try:
        d = md.load(tk, "daily")
        h = md.load(tk, "1h")
        m = md.load(tk, "5m")
    except Exception:  # noqa: BLE001
        return [], []
    if len(d) < 260 or len(h) < 120 or len(m) < 500:
        return [], []
    ds = daily_signals(d, p)
    arm = armed_dates(ds, p["ARM_DAYS"])
    h_end, h_spread, h_above = hourly_flags(h, p)
    o, hi, lo, c = (m[k].values for k in ("Open", "High", "Low", "Close"))
    t5 = m.index
    days = t5.normalize()
    day_id = pd.factorize(days)[0]
    last_of_day = pd.Series(np.arange(len(t5))).groupby(day_id).max().values
    r = rsi(c)
    mc, sg = macd(c)
    minutes = (t5.hour * 60 + t5.minute).values
    cross = np.zeros(len(c), bool)
    cross[1:] = (mc[1:] > sg[1:]) & (mc[:-1] <= sg[:-1])
    os_ = pd.Series(r).rolling(p["RSI_LOOK"], min_periods=1).min().values < p["RSI_OS"]
    trig = cross & os_ & (minutes + 5 <= 15 * 60 + 30) & (np.arange(len(c)) > 300)   # 300 נרות חימום
    rng = np.random.default_rng(seed)

    def row(j, kind):
        e = j + 1
        if e >= len(c) or day_id[e] != day_id[j]:
            return None
        dec = t5[j] + pd.Timedelta(minutes=5)                      # זמן ההחלטה: סגירת נר j
        hb = h_end.searchsorted(dec, side="right") - 1            # הנר השעתי האחרון שנסגר עד אז
        if hb < 100:
            return None
        dt = t5[j].date()
        stop = lo[max(0, j - p["STOP_BARS"] + 1):j + 1].min() - 0.0001 * c[j]
        out = dict(ticker=tk, kind=kind, time=t5[e], date=dt, armed=dt in arm,
                   dsig_date=arm.get(dt), h_conv=bool(h_spread[hb] <= p["H_SPREAD"]), h_above=bool(h_above[hb]),
                   h_spread=h_spread[hb], rsi_min=pd.Series(r[max(0, j - 5):j + 1]).min())
        entry = o[e]
        if entry <= stop:
            return None
        risk = entry - stop
        out["risk_pct"] = risk / entry
        nxt = day_id[e] + 1 if day_id[e] + 1 <= day_id[-1] else None
        for name, tg, xd in [("eod", np.nan, day_id[e]), ("2R", entry + 2 * risk, day_id[e]),
                             ("next", np.nan, nxt)]:
            if xd is None:
                out[f"{name}_ret"] = np.nan
                continue
            en, ex, why = simulate(o, hi, lo, c, day_id, e, stop if name != "eod" else np.nan, tg, xd)
            if why == "open":
                out[f"{name}_ret"] = np.nan
                continue
            out[f"{name}_ret"] = ex * (1 - p["COST"]) / (en * (1 + p["COST"])) - 1
            out[f"{name}_R"] = (ex - en) / risk
            out[f"{name}_why"] = why
        return out

    trades, rand = [], []
    seen = set()
    for j in np.nonzero(trig)[0]:
        if day_id[j] in seen:
            continue
        x = row(j, "trigger")
        if x:
            seen.add(day_id[j])
            trades.append(x)
    # בסיס: נר אקראי אחד בכל יום (10:00-15:25)
    for di in range(day_id.max() + 1):
        js = np.nonzero((day_id == di) & (minutes >= 600) & (minutes + 5 <= 15 * 60 + 30))[0]
        js = js[js > 300]
        if len(js):
            x = row(int(rng.choice(js)), "random")
            if x:
                rand.append(x)
    return trades, rand


def stats(g, ex):
    col = f"{ex}_ret"
    g = g[g[col].notna()]
    if len(g) < 5:
        return dict(n=len(g))
    rng = np.random.default_rng(0)
    per = g.groupby("date")[col].agg(["sum", "count"])
    idx = rng.integers(0, len(per), (3000, len(per)))
    boots = per["sum"].values[idx].sum(1) / per["count"].values[idx].sum(1)
    return dict(n=len(g), days=len(per), win=(g[col] > 0).mean(), avg=g[col].mean(),
                lo=np.percentile(boots, 2.5), hi=np.percentile(boots, 97.5),
                R=g[f"{ex}_R"].mean() if f"{ex}_R" in g else np.nan)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--universe", nargs="+", default=["universes/sp500.txt", "universes/sp400.txt",
                                                      "universes/sp600.txt"])
    ap.add_argument("--out", default="results_mtf")
    for k, v in P.items():
        ap.add_argument(f"--{k.lower()}", type=type(v), default=v)
    args = ap.parse_args(argv)
    p = {k: getattr(args, k.lower()) for k in P}
    tk = list(dict.fromkeys(ln.strip().upper() for f in args.universe for ln in open(f) if ln.strip()))
    tk = [t for t in tk if os.path.exists(f"{md.DIRS['5m']}/{t}.pkl") and os.path.exists(f"{md.DIRS['1h']}/{t}.pkl")]
    T, R = [], []
    with ProcessPoolExecutor(4) as ex:
        for t, r in ex.map(run_ticker, [(x, p, i) for i, x in enumerate(tk)], chunksize=8):
            T += t
            R += r
    T, R = pd.DataFrame(T), pd.DataFrame(R)
    os.makedirs(args.out, exist_ok=True)
    T.to_csv(os.path.join(args.out, "trigger_trades.csv"), index=False)
    R.to_csv(os.path.join(args.out, "random_trades.csv"), index=False)
    groups = [
        ("**FULL: daily + hourly + 5m trigger**", T[T.armed & T.h_conv]),
        ("daily + 5m trigger (no hourly filter)", T[T.armed]),
        ("daily + hourly conv + above hourly MAs + 5m", T[T.armed & T.h_conv & T.h_above]),
        ("5m trigger only (all stocks/days)", T),
        ("random 5m entry, daily + hourly days", R[R.armed & R.h_conv]),
        ("random 5m entry, daily-armed days", R[R.armed]),
        ("random 5m entry, all stocks/days", R),
    ]
    span = f"{pd.to_datetime(R.time).min()} -> {pd.to_datetime(R.time).max()}" if len(R) else ""
    L = [f"# Multi-timeframe strategy - {len(tk)} stocks, 5-min data {span}", "",
         "params: " + ", ".join(f"{k}={v}" for k, v in p.items()), "",
         "| group | exit | trades | days | win | avg/trade | 95% CI (date-clustered) | avg R |", "|---|---|---|---|---|---|---|---|"]
    for name, g in groups:
        for ex_ in ("eod", "2R", "next"):
            s = stats(g, ex_)
            if s.get("n", 0) < 5:
                L.append(f"| {name} | {ex_} | {s.get('n', 0)} | | | | | |")
                continue
            L.append(f"| {name} | {ex_} | {s['n']:,} | {s['days']} | {s['win']:.0%} | {s['avg']:+.3%} | "
                     f"[{s['lo']:+.3%}, {s['hi']:+.3%}] | {s['R']:+.3f} |")
    full = T[T.armed & T.h_conv]
    L += ["", f"daily signals feeding the window: {full.dsig_date.nunique() if len(full) else 0} distinct dates, "
              f"{full.ticker.nunique() if len(full) else 0} stocks"]
    text = "\n".join(L)
    open(os.path.join(args.out, "summary.md"), "w", encoding="utf-8").write(text + "\n")
    print(text)


if __name__ == "__main__":
    main()
