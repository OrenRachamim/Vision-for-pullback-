"""
etf_test.py - קנייה של קרן המדד / הסקטור עצמה באיתות פולבק יומי (פרמטרי INDEX בסורק).

לכל קרן:
  * כל האיתותים (walk-forward, בלי הצצה לעתיד) וסימולציית עסקה לכל איתות - R מול כניסה אקראית לאותה קרן
    עם אותן יציאות.
  * תיק אמיתי של פוזיציה אחת: לא נכנסים לעסקה חדשה כשעסקה פתוחה. תשואה כוללת, תשואה שנתית, ירידה מקסימלית
    וחשיפה (% מהזמן בשוק) - מול קנייה והחזקה של אותה קרן.
  * רווח סמך לפי תאריכים: הקרנות זזות יחד, אז עסקאות מאותו שבוע אינן בלתי תלויות.

הרצה:
    python etf_test.py --group main  --trail-atr 3 --max-hold 60
    python etf_test.py --group fresh --max-hold 10          # יעד 2R
"""
import argparse
import os

import numpy as np
import pandas as pd

import backtest as bt
import pullback_scanner as ps

GROUPS = {
    "main": ["SPY", "MDY", "IJR", "XLK", "XLF", "XLV", "XLY", "XLP", "XLE", "XLI", "XLB", "XLU",
             "XLRE", "XLC"],
    "fresh": ["QQQ", "IWM", "DIA", "VTI", "EFA", "EEM", "SMH", "XBI", "KRE", "XHB", "XRT", "IBB"],
}


def portfolio(df, trades, start_pos):
    """פוזיציה אחת בכל פעם: עקומת הון יומית (ביום בעסקה - תשואת הקרן, אחרת 0)."""
    c = df["Close"].values
    o = df["Open"].values
    eq = np.ones(len(df))
    inpos = np.zeros(len(df), bool)
    busy_until, taken = -1, []
    for t, tr in trades:
        if t + 1 <= busy_until or tr is None or tr["exit_reason"] in ("gap_below_stop",):
            continue
        e, x = t + 1, t + tr["bars"]
        taken.append((t, tr))
        inpos[e:x + 1] = True
        busy_until = x
    r = np.zeros(len(df))
    for t, tr in taken:
        e, x = t + 1, t + tr["bars"]
        r[e] += c[e] / o[e] - 1                              # יום הכניסה: מפתיחה לסגירה
        r[e + 1:x + 1] += c[e + 1:x + 1] / c[e:x] - 1
        r[x] += tr["exit"] / c[x] - 1 if x < len(c) else 0  # יום היציאה: עד מחיר היציאה
    r = r[start_pos:]
    eq = np.cumprod(1 + r)
    return eq, inpos[start_pos:].mean(), len(taken)


def stats_curve(eq, years):
    tot = eq[-1] - 1
    cagr = eq[-1] ** (1 / years) - 1
    dd = (eq / np.maximum.accumulate(eq) - 1).min()
    return tot, cagr, dd


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--group", choices=list(GROUPS), default="main")
    ap.add_argument("--tickers", nargs="*")
    ap.add_argument("--start", default="2012-01-01")
    ap.add_argument("--end", default=None)
    ap.add_argument("--trail-atr", type=float, default=None)
    ap.add_argument("--max-hold", type=int, default=60)
    ap.add_argument("--target-r", type=float, default=2.0)
    ap.add_argument("--cache-dir", default="data")
    ap.add_argument("--out", default=None)
    args = ap.parse_args(argv)
    bt.use_scanner("pullback_scanner")
    tickers = args.tickers or GROUPS[args.group]
    bt.prefetch(tickers, args.cache_dir)
    rng = np.random.default_rng(0)
    exit_txt = (f"trailing {args.trail_atr}xATR" if args.trail_atr else f"{args.target_r}R target") \
        + f", max {args.max_hold}d"

    rows, all_sig, all_ctrl = [], [], []
    for tk in tickers:
        path = os.path.join(args.cache_dir, f"{tk}.csv")
        if not os.path.exists(path):
            continue
        df = bt.load_history(tk, args.cache_dir)
        hits = bt.scan_history(df, args.start, args.end, weekly=False, params=ps.INDEX)
        atr = bt.atr14(df) if args.trail_atr else None
        trades = [(h["t"], bt.simulate_trade(df, h["t"], h["daily"]["base_lo"], args.target_r,
                                             args.max_hold, args.trail_atr, atr)) for h in hits]
        closed = [(t, tr) for t, tr in trades if tr and tr["exit_reason"] not in ("open",)]
        R = np.array([tr["R"] for _, tr in closed if tr["R"] == tr["R"]])
        for t, tr in closed:
            if tr["R"] == tr["R"]:
                all_sig.append((df.index[t], tk, tr["R"]))
        # כניסה אקראית לאותה קרן, אותן יציאות, סטופ במרחק שנדגם מהאיתותים
        risks = [tr["risk_pct"] for _, tr in closed if tr.get("risk_pct")] or [0.03]
        lo = bt.bt_lo(df, args.start)
        hi = df.index.searchsorted(pd.Timestamp(args.end), side="right") if args.end else len(df)
        o = df["Open"].values
        ctrl = []
        for t in range(lo, hi - 1, 2):
            r = bt.simulate_trade(df, t, o[t + 1] * (1 - rng.choice(risks)), args.target_r,
                                  args.max_hold, args.trail_atr, atr)
            if r and r["exit_reason"] != "open":
                ctrl.append(r["R"])
        ctrl = np.array(ctrl)
        all_ctrl.extend(ctrl)
        # תיק של פוזיציה אחת מול קנייה והחזקה
        years = (hi - lo) / 252
        eq, expo, ntaken = portfolio(df.iloc[:hi], trades, lo)
        s_tot, s_cagr, s_dd = stats_curve(eq, years)
        bh = df["Close"].values[lo:hi] / df["Close"].values[lo]
        b_tot, b_cagr, b_dd = stats_curve(bh, years)
        rows.append(dict(etf=tk, signals=len(hits), trades=len(R), win=(R > 0).mean() if len(R) else np.nan,
                         avg_R=R.mean() if len(R) else np.nan, ctrl_R=ctrl.mean(),
                         diff_R=(R.mean() - ctrl.mean()) if len(R) else np.nan,
                         taken=ntaken, exposure=expo, strat_cagr=s_cagr, strat_maxdd=s_dd,
                         bh_cagr=b_cagr, bh_maxdd=b_dd,
                         ret_per_exposure=(s_cagr / expo) if expo else np.nan))
    t = pd.DataFrame(rows).set_index("etf")

    # רווח סמך לפי שבוע (קרנות מתואמות -> מקבצים לפי שבוע קלנדרי)
    sig = pd.DataFrame(all_sig, columns=["date", "etf", "R"])
    sig["week"] = pd.to_datetime(sig["date"]).dt.to_period("W")
    per = sig.groupby("week")["R"].agg(["sum", "count"])
    idx = rng.integers(0, len(per), (4000, len(per)))
    boots = per["sum"].values[idx].sum(1) / per["count"].values[idx].sum(1)
    ci = np.percentile(boots, [2.5, 97.5])
    ctrl_mean = np.mean(all_ctrl)

    pd.set_option("display.width", 200)
    txt = [f"# ETF pullback test - group '{args.group}', {args.start} -> {args.end or 'today'}, exit: {exit_txt}",
           "", t.round(3).to_string(), "",
           f"ALL: {len(sig)} trades on {len(per)} distinct weeks | avg_R {sig.R.mean():+.3f} "
           f"(week-clustered 95% CI [{ci[0]:+.3f}, {ci[1]:+.3f}]) | random entries same exits {ctrl_mean:+.3f} "
           f"| diff {sig.R.mean() - ctrl_mean:+.3f}R",
           f"median over ETFs: strategy CAGR {t.strat_cagr.median():.1%} at {t.exposure.median():.0%} exposure, "
           f"max DD {t.strat_maxdd.median():.1%} | buy&hold CAGR {t.bh_cagr.median():.1%}, max DD {t.bh_maxdd.median():.1%}"]
    print("\n".join(txt))
    if args.out:
        os.makedirs(args.out, exist_ok=True)
        open(os.path.join(args.out, "summary.txt"), "w").write("\n".join(txt) + "\n")
        t.to_csv(os.path.join(args.out, "per_etf.csv"))
        sig.drop(columns="week").to_csv(os.path.join(args.out, "trades.csv"), index=False)


if __name__ == "__main__":
    main()
