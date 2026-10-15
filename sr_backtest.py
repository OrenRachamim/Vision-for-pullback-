"""
sr_backtest.py - בדיקה היסטורית של פריצה מעל התנגדות (sr_levels.find_breakouts), בלי הצצה לעתיד.

עסקה: כניסה בפתיחת היום שאחרי הפריצה; סטופ התחלתי = ראש האזור שנפרץ פחות 1*ATR (חזרה לתוך האזור = כישלון);
יציאה לפי --trail-atr (סטופ נגרר) או יעד --target-r, עד --max-hold ימים.
השוואות (אותן יציאות, אותו פיזור מרחק-סטופ):
  CONTROL      - ימים אקראיים באותן מניות;
  CONTROL trend - ימים אקראיים שבהם המחיר מעל SMA50 ומעל SMA200 (פריצה תמיד קורית אחרי עלייה).
פילוחים לחקירה: מספר נגיעות, מרחק להתנגדות הבאה (ביחידות ATR), ווליום ביום הפריצה.

הרצה:
    python sr_backtest.py --universe universes/sp500.txt universes/sp400.txt --trail-atr 3 --max-hold 60 --out results_sr_900
"""
import argparse
import os
from concurrent.futures import ProcessPoolExecutor

import numpy as np
import pandas as pd

import backtest as bt
import pullback_scanner as ps
import sr_levels as sr

STOP_ATR = 1.0


def run_ticker(tk, args):
    df = bt.load_history(tk, args.cache_dir)
    if len(df) < bt.DAILY_WARMUP + 50:
        return tk, [], []
    lv = sr.Levels(df)
    atr = lv.atr
    bos = sr.find_breakouts(df, args.start, args.end, lv=lv, top_only=args.top_only, margin_atr=args.margin_atr)
    vol = ps.clean_event_volume(df)["Volume"]
    vr = (vol / vol.rolling(20).mean().shift(1)).values
    c = df["Close"].values
    sma50 = df["Close"].rolling(50).mean().values
    sma200 = df["Close"].rolling(200).mean().values
    rows = []
    for b in bos:
        t, L = b["t"], b["level"]
        stop = L["top"] - STOP_ATR * atr[t]
        tr = bt.simulate_trade(df, t, stop, args.target_r, args.max_hold, args.trail_atr, atr)
        if not tr:
            continue
        nxt = b["next_resistance"]
        rows.append(dict(ticker=tk, date=df.index[t].date(), level=L["top"], touches=L["touches"],
                         room_atr=((nxt["bottom"] - c[t]) / atr[t]) if nxt else np.nan,
                         vol_ratio=vr[t], uptrend=bool(c[t] > sma50[t] and c[t] > sma200[t]), **tr))
    # CONTROL: ימים אקראיים (כל יום שני), סטופ במרחק שנדגם מהאיתותים של אותה מניה או ברירת מחדל
    rng = np.random.default_rng(abs(hash(tk)) % 2**32)
    risks = [r["risk_pct"] for r in rows if r.get("risk_pct")] or [0.04]
    lo = bt.bt_lo(df, args.start)
    hi = df.index.searchsorted(pd.Timestamp(args.end), side="right") if args.end else len(df)
    o = df["Open"].values
    ctrl = []
    for t in range(lo, hi - 1, 2):
        r = bt.simulate_trade(df, t, o[t + 1] * (1 - rng.choice(risks)), args.target_r, args.max_hold,
                              args.trail_atr, atr)
        if r and r["exit_reason"] != "open" and r["R"] == r["R"]:
            ctrl.append((r["R"], bool(c[t] > sma50[t] and c[t] > sma200[t])))
    return tk, rows, ctrl


def date_ci(g, rng, n=4000):
    per = g.groupby("date")["R"].agg(["sum", "count"])
    idx = rng.integers(0, len(per), (n, len(per)))
    boots = per["sum"].values[idx].sum(1) / per["count"].values[idx].sum(1)
    return len(per), np.percentile(boots, 2.5), np.percentile(boots, 97.5)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("tickers", nargs="*")
    ap.add_argument("--universe", nargs="+", default=[])
    ap.add_argument("--start", default="2016-01-01")
    ap.add_argument("--end", default=None)
    ap.add_argument("--trail-atr", type=float, default=None)
    ap.add_argument("--max-hold", type=int, default=20)
    ap.add_argument("--target-r", type=float, default=2.0)
    ap.add_argument("--cache-dir", default="data")
    ap.add_argument("--jobs", type=int, default=os.cpu_count() or 1)
    ap.add_argument("--out", default="results_sr")
    ap.add_argument("--margin-atr", type=float, default=sr.MARGIN_ATR,
                    help="breakout = first close above zone top + K*ATR (default 0.1)")
    ap.add_argument("--top-only", choices=["year", "ath"], default=None,
                    help="only breakouts of the zone holding the 52-week high (year) or the all-time high in the data (ath)")
    args = ap.parse_args(argv)
    bt.use_scanner("pullback_scanner")
    tickers = [t.upper() for t in args.tickers]
    for p in args.universe:
        tickers += [ln.strip().upper() for ln in open(p) if ln.strip()]
    tickers = list(dict.fromkeys(tickers))
    bt.prefetch(tickers, args.cache_dir)
    tickers = [t for t in tickers if os.path.exists(os.path.join(args.cache_dir, f"{t}.csv"))]

    rows, ctrl = [], []
    with ProcessPoolExecutor(max_workers=args.jobs) as ex:
        for tk, r, cl in ex.map(run_ticker, tickers, [args] * len(tickers), chunksize=8):
            rows += r
            ctrl += cl
    sig = pd.DataFrame(rows)
    closed = sig[(sig.exit_reason != "open") & sig.R.notna()]
    cR = np.array([x[0] for x in ctrl])
    cT = np.array([x[0] for x in ctrl if x[1]])
    rng = np.random.default_rng(0)
    nd, lo, hi = date_ci(closed, rng)
    years = (pd.Timestamp(args.end or pd.Timestamp.now()) - pd.Timestamp(args.start)).days / 365.25
    ex_txt = (f"trailing stop {args.trail_atr}xATR" if args.trail_atr else f"{args.target_r}R target") \
        + f", max {args.max_hold} days; initial stop = zone top - {STOP_ATR}xATR"

    def line(name, g):
        if len(g) < 20:
            return f"| {name} | {len(g)} | | | | |"
        return (f"| {name} | {len(g):,} | {(g.R > 0).mean():.0%} | {g.R.mean():+.3f} | "
                f"{g.R.mean() - cR.mean():+.3f} | {g.R.mean() - cT.mean():+.3f} |")

    L = [f"# Resistance breakouts - {len(tickers)} stocks, {args.start} -> {args.end or 'today'}"
         + f" - breakout = close > zone top + {args.margin_atr}xATR"
         + (f" - only the zone holding the {'52-week' if args.top_only == 'year' else 'all-time (since 2010)'} high"
            if args.top_only else ""), "",
         f"* exit: {ex_txt}", f"* {len(sig):,} breakouts ({len(sig) / len(tickers) / years:.1f} per stock per year), "
         f"{len(closed):,} closed trades on {nd:,} distinct dates", "",
         "| | trades | win | avg R | vs random days | vs random uptrend days |", "|---|---|---|---|---|---|",
         line("all breakouts", closed),
         f"| random days (CONTROL) | {len(cR):,} | {(cR > 0).mean():.0%} | {cR.mean():+.3f} | | |",
         f"| random uptrend days | {len(cT):,} | {(cT > 0).mean():.0%} | {cT.mean():+.3f} | | |", "",
         f"Breakouts, date-clustered 95% CI of avg R: [{lo:+.3f}, {hi:+.3f}]", "",
         "## Breakdowns (exploratory)", "",
         "| group | trades | win | avg R | vs random days | vs random uptrend days |", "|---|---|---|---|---|---|"]
    for name, mask in [("touches = 2", closed.touches == 2), ("touches = 3", closed.touches == 3),
                       ("touches >= 4", closed.touches >= 4),
                       ("room to next resistance < 1 ATR", closed.room_atr < 1),
                       ("room 1-3 ATR", closed.room_atr.between(1, 3)),
                       ("room > 3 ATR", closed.room_atr > 3),
                       ("no resistance above (new 1y high zone)", closed.room_atr.isna()),
                       ("breakout volume < 1x avg", closed.vol_ratio < 1),
                       ("breakout volume 1-1.5x", closed.vol_ratio.between(1, 1.5)),
                       ("breakout volume > 1.5x", closed.vol_ratio > 1.5),
                       ("in uptrend (>SMA50 & >SMA200)", closed.uptrend),
                       ("not in uptrend", ~closed.uptrend)]:
        L.append(line(name, closed[mask]))
    text = "\n".join(L)
    os.makedirs(args.out, exist_ok=True)
    open(os.path.join(args.out, "summary.md"), "w", encoding="utf-8").write(text + "\n")
    sig.to_csv(os.path.join(args.out, "signals.csv"), index=False)
    print(text)


if __name__ == "__main__":
    main()
