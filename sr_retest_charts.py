"""
sr_retest_charts.py - גרפים לדוגמה של פריצת שיא כל הזמנים -> פולבק קטן -> אישור (שיא חדש) -> כניסה B.

מסמן: אזור ההתנגדות שנפרץ, יום הפריצה, נרות הפולבק, יום האישור, כניסה B, סטופ B והיציאה (סטופ נגרר 3xATR).
המדגם אקראי (seed קבוע) מתוך הפריצות שאושרו, כדי להראות גם הצלחות וגם כישלונות ביחס האמיתי.

הרצה:  python sr_retest_charts.py results_retest_900 --n 20 --out sr_charts/retest
"""
import argparse
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

import backtest as bt  # noqa: E402
import sr_levels as sr  # noqa: E402
import sr_retest as rt  # noqa: E402


def chart(tk, date, path, before=60):
    df = bt.load_history(tk)
    lv = sr.Levels(df)
    atr = lv.atr
    t0 = df.index.get_loc(pd.Timestamp(date))
    b = next(x for x in sr.find_breakouts(df, df.index[t0], df.index[t0], lv=lv, top_only="ath"))
    L = b["level"]
    status, tc, pb_low, pb_days = rt.retest(df, t0, L["top"], atr)
    stop = pb_low - 0.1 * atr[tc]
    tr = bt.simulate_trade(df, tc, stop, 2.0, rt.HOLD, rt.TRAIL, atr, return_path=True)
    ex = tr["exit_pos"]
    a, e = max(0, t0 - before), min(len(df), max(ex, tc + 20) + 6)
    d = df.iloc[a:e]
    x = lambda i: i - a

    fig, (ax, axv) = plt.subplots(2, 1, figsize=(13, 7), sharex=True, gridspec_kw={"height_ratios": [4, 1]})
    for i, (o, h, l, c) in enumerate(d[["Open", "High", "Low", "Close"]].values):
        col = "#3B6D11" if c >= o else "#A32D2D"
        ax.vlines(i, l, h, color=col, lw=1)
        ax.add_patch(plt.Rectangle((i - 0.3, min(o, c)), 0.6, max(abs(c - o), 1e-6), color=col))
    axv.bar(range(len(d)), d["Volume"], color=np.where(d["Close"] >= d["Open"], "#97C459", "#F09595"))
    x0 = max(L["first"] - a, 0)
    ax.fill_between([x0, x(t0)], L["bottom"], L["top"], color="#A32D2D", alpha=0.18, lw=0)
    ax.hlines(L["top"], x0, len(d) - 1, color="#A32D2D", lw=1.2, alpha=0.8)
    ax.text(x0, L["top"], f"ATH zone {L['top']:.2f} ({L['touches']}x) ", color="#A32D2D", fontsize=8,
            ha="right", va="bottom")
    ax.axvspan(x(t0) - 0.5, x(t0) + 0.5, color="#3B6D11", alpha=0.12)
    for k in pb_days:
        ax.axvspan(x(k) - 0.5, x(k) + 0.5, color="#EF9F27", alpha=0.25)
    ax.axvspan(x(tc) - 0.5, x(tc) + 0.5, color="#185FA5", alpha=0.18)
    hi = df["High"].values
    ax.annotate("1 BREAKOUT", (x(t0), hi[t0]), xytext=(-25, 35), textcoords="offset points", ha="center",
                color="#3B6D11", fontweight="bold", fontsize=9, arrowprops=dict(arrowstyle="->", color="#3B6D11"))
    ax.annotate(f"2 PULLBACK ({len(pb_days)}d)", (x(pb_days[0]), df["Low"].values[pb_days[0]]), xytext=(0, -40),
                textcoords="offset points", ha="center", color="#BA7517", fontweight="bold", fontsize=9,
                arrowprops=dict(arrowstyle="->", color="#BA7517"))
    ax.annotate("3 CONFIRM\n(new high)", (x(tc), hi[tc]), xytext=(25, 35), textcoords="offset points", ha="center",
                color="#185FA5", fontweight="bold", fontsize=9, arrowprops=dict(arrowstyle="->", color="#185FA5"))
    end = x(min(ex, len(df) - 1))
    ax.hlines(tr["entry"], x(tc + 1), end, color="#185FA5", ls="--", lw=1.1)
    ax.text(x(tc + 1), tr["entry"], f"entry B {tr['entry']:.2f} ", color="#185FA5", fontsize=8, ha="right",
            va="bottom", fontweight="bold")
    ax.hlines(stop, x(tc + 1), x(tc + 3), color="#A32D2D", ls=":", lw=1.1)
    ax.text(x(tc + 1), stop, f"stop {stop:.2f} ", color="#A32D2D", fontsize=8, ha="right", va="top")
    ts = np.asarray(tr["stop_path"], dtype=float)
    ax.plot(np.arange(x(tc + 1), x(tc + 1) + len(ts)), ts, color="#A32D2D", lw=0.9, alpha=0.6)
    win = tr["R"] > 0
    ax.plot(end, tr["exit"], marker="X", ms=10, color="#3B6D11" if win else "#A32D2D", ls="")
    ax.set_title(f"{tk}  breakout {df.index[t0].date()} -> pullback {len(pb_days)}d -> confirm "
                 f"{df.index[tc].date()} (+{tc - t0}d)  |  B: {tr['exit_reason']} after {tr['bars']}d, "
                 f"{tr['ret']:+.1%} = {tr['R']:+.2f}R", fontsize=10, color="#3B6D11" if win else "#A32D2D")
    ax.set_xlim(-1, len(d) + 2)
    step = max(1, len(d) // 10)
    axv.set_xticks(range(0, len(d), step))
    axv.set_xticklabels([z.strftime("%Y-%m-%d") for z in d.index[::step]], fontsize=8)
    fig.tight_layout()
    fig.savefig(path, dpi=100)
    plt.close(fig)
    return tr["R"]


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("dirs", nargs="+")
    ap.add_argument("--n", type=int, default=20)
    ap.add_argument("--since", default="2022-01-01")
    ap.add_argument("--out", default="sr_charts/retest")
    args = ap.parse_args(argv)
    bt.use_scanner("pullback_scanner")
    sig = pd.concat([pd.read_csv(f"{d}/signals.csv") for d in args.dirs])
    conf = sig[(sig.status == "confirmed") & (sig.date >= args.since) & sig.B_R.notna()]
    pick = conf.sample(args.n, random_state=1).sort_values("date")
    os.makedirs(args.out, exist_ok=True)
    rs = []
    for i, r in enumerate(pick.itertuples(), 1):
        p = os.path.join(args.out, f"{i:02d}_{r.ticker}_{r.date}.png")
        rs.append(chart(r.ticker, r.date, p))
        print(f"{p}  R={rs[-1]:+.2f}")
    rs = np.array(rs)
    print(f"sample: {len(rs)} | wins {(rs > 0).mean():.0%} | avg R {rs.mean():+.2f}")


if __name__ == "__main__":
    main()
