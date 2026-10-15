"""
sr_retest.py - פריצה מעל אזור שיא כל הזמנים, ואז פולבק קטן ואישור: האם הכניסה אחרי האישור "בטוחה" יותר?

לכל פריצה (sr_levels.find_breakouts, top_only="ath") ביום t0:
  פולבק  : בימים שאחרי t0 - 1 עד 3 נרות יורדים (סגירה < סגירה קודמת). יותר מ-3 ברצף -> מבוטל.
           סגירה מתחת לראש האזור פחות 1*ATR -> הפריצה נכשלה, מבוטל.
  אישור  : סגירה מעל השיא הגבוה ביותר מאז t0 (שיא כל-הזמנים חדש), אחרי שהיה פולבק, עד 10 ימים מ-t0.
  כניסה  : (A) מיד - פתיחה ב-t0+1;  (B) אחרי אישור - פתיחה ביום שאחרי האישור.
  סטופ   : (A) ראש האזור פחות 1*ATR (כמו קודם); (B) שפל הפולבק פחות 0.1*ATR.
השוואה: ימים אקראיים שבהם המניה במגמה עולה (מעל SMA50 ו-SMA200), אותן מדידות.

הרצה:  python sr_retest.py --universe universes/sp500.txt universes/sp400.txt --out results_retest_900
"""
import argparse
import os
import zlib
from concurrent.futures import ProcessPoolExecutor

import numpy as np
import pandas as pd

import backtest as bt
import sr_levels as sr

WINDOW = 10        # ימים מהפריצה לאישור
MAX_PULLBACK = 3   # מקסימום נרות יורדים ברצף
TRAIL, HOLD = 3.0, 60


def fwd_stats(df, e_idx):
    """כניסה בפתיחה של e_idx: שיא תוך 5 ימים, וסגירה אחרי 5/10/20 ימים - ביחס לכניסה."""
    o, h, c = df["Open"].values, df["High"].values, df["Close"].values
    if e_idx + 20 >= len(df):
        return None
    e = o[e_idx]
    return dict(mh5=h[e_idx:e_idx + 5].max() / e - 1, c5=c[e_idx + 4] / e - 1,
                c10=c[e_idx + 9] / e - 1, c20=c[e_idx + 19] / e - 1)


def retest(df, t0, top, atr):
    """פולבק ואישור אחרי פריצה ב-t0. מחזיר (status, יום האישור, שפל הפולבק, ימי הפולבק)."""
    h, l, c = df["High"].values, df["Low"].values, df["Close"].values
    status, hh, streak, pb_low, pb_days = "no_confirm", h[t0], 0, np.inf, []
    for k in range(t0 + 1, min(t0 + WINDOW + 1, len(df) - 1)):
        if c[k] < top - atr[t0]:
            return "failed", None, pb_low, pb_days
        if c[k] < c[k - 1]:
            streak += 1; pb_days.append(k); pb_low = min(pb_low, l[k])
            if streak > MAX_PULLBACK:
                return "too_deep", None, pb_low, pb_days
        else:
            if pb_days and c[k] > hh:
                return "confirmed", k, pb_low, pb_days
            streak = 0
        hh = max(hh, h[k])
    return status, None, pb_low, pb_days


def run_ticker(tk, start):
    df = bt.load_history(tk)
    if len(df) < bt.DAILY_WARMUP + 60:
        return [], []
    lv = sr.Levels(df)
    atr = lv.atr
    o, h, l, c = (df[k].values for k in ("Open", "High", "Low", "Close"))
    rows = []
    for b in sr.find_breakouts(df, start, None, lv=lv, top_only="ath"):
        t0, top = b["t"], b["level"]["top"]
        row = dict(ticker=tk, date=df.index[t0].date())
        a = fwd_stats(df, t0 + 1)
        if a is None:
            continue
        row.update({f"A_{k}": v for k, v in a.items()})
        tr = bt.simulate_trade(df, t0, top - atr[t0], 2.0, HOLD, TRAIL, atr)
        row["A_R"] = tr["R"] if tr and tr["exit_reason"] != "open" else np.nan
        status, tc, pb_low, _ = retest(df, t0, top, atr)
        row["status"] = status
        if status == "confirmed":
            bstats = fwd_stats(df, tc + 1)
            if bstats is None:
                continue
            row.update({f"B_{k}": v for k, v in bstats.items()})
            row["days_to_confirm"] = tc - t0
            trb = bt.simulate_trade(df, tc, pb_low - 0.1 * atr[tc], 2.0, HOLD, TRAIL, atr)
            row["B_R"] = trb["R"] if trb and trb["exit_reason"] != "open" else np.nan
            row["B_risk"] = trb.get("risk_pct", np.nan) if trb else np.nan
        rows.append(row)
    # בסיס: ימים אקראיים במגמה עולה
    sma50 = pd.Series(c).rolling(50).mean().values
    sma200 = pd.Series(c).rolling(200).mean().values
    lo = bt.bt_lo(df, start)
    cand = [t for t in range(lo, len(df) - 25) if c[t] > sma50[t] and c[t] > sma200[t]]
    rng = np.random.default_rng(zlib.crc32(tk.encode()))
    base = []
    risks = [r["B_risk"] for r in rows if r.get("B_risk") == r.get("B_risk") and r.get("B_risk")] or [0.04]
    for t in rng.choice(cand, min(len(cand), 40), replace=False) if cand else []:
        s = fwd_stats(df, t + 1)
        tr = bt.simulate_trade(df, t, o[t + 1] * (1 - rng.choice(risks)), 2.0, HOLD, TRAIL, atr)
        if s:
            s["R"] = tr["R"] if tr and tr["exit_reason"] != "open" else np.nan
            base.append(s)
    return rows, base


def summarize(sig, base, label):
    conf = sig[sig.status == "confirmed"]
    def line(name, mh5, c5, c10, c20, R):
        return (f"| {name} | {len(mh5):,} | {(mh5 >= .02).mean():.0%} | {(mh5 >= .03).mean():.0%} | {(c5 > 0).mean():.0%} | "
                f"{c5.mean():+.2%} | {c10.mean():+.2%} | {c20.mean():+.2%} | {np.nanmean(R):+.3f} |")
    L = [f"## {label}", "",
         f"* breakouts: {len(sig):,} | confirmed (pullback + new high within {WINDOW} days): {len(conf):,} "
         f"({len(conf) / len(sig):.0%}) | failed (closed below zone): {(sig.status == 'failed').mean():.0%} | "
         f"no pullback/no new high: {(sig.status == 'no_confirm').mean():.0%} | pullback > {MAX_PULLBACK} days: "
         f"{(sig.status == 'too_deep').mean():.0%}",
         f"* median days from breakout to confirmation: {conf.days_to_confirm.median():.0f}", "",
         "| entry | n | touched +2% in 5d | touched +3% in 5d | up after 5d | avg 5d | avg 10d | avg 20d | avg R (trail) |",
         "|---|---|---|---|---|---|---|---|---|",
         line("A: right after breakout (all)", sig.A_mh5, sig.A_c5, sig.A_c10, sig.A_c20, sig.A_R),
         line("A: right after breakout (only those later confirmed)", conf.A_mh5, conf.A_c5, conf.A_c10, conf.A_c20, conf.A_R),
         line("**B: after pullback + confirmation**", conf.B_mh5, conf.B_c5, conf.B_c10, conf.B_c20, conf.B_R),
         line("random uptrend days", base.mh5, base.c5, base.c10, base.c20, base.R), ""]
    return "\n".join(L)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--universe", nargs="+", required=True)
    ap.add_argument("--start", default="2016-01-01")
    ap.add_argument("--out", default="results_retest")
    args = ap.parse_args(argv)
    bt.use_scanner("pullback_scanner")
    tickers = [ln.strip().upper() for p in args.universe for ln in open(p) if ln.strip()]
    tickers = [t for t in dict.fromkeys(tickers) if os.path.exists(f"data/{t}.csv")]
    rows, base = [], []
    with ProcessPoolExecutor() as ex:
        for r, b in ex.map(run_ticker, tickers, [args.start] * len(tickers), chunksize=8):
            rows += r
            base += b
    sig, base = pd.DataFrame(rows), pd.DataFrame(base)
    text = summarize(sig, base, f"{len(tickers)} stocks, {args.start} -> today")
    os.makedirs(args.out, exist_ok=True)
    open(os.path.join(args.out, "summary.md"), "w", encoding="utf-8").write(text + "\n")
    sig.to_csv(os.path.join(args.out, "signals.csv"), index=False)
    print(text)


if __name__ == "__main__":
    main()
