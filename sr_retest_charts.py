"""
sr_retest_charts.py - גרפים לדוגמה של פריצת שיא כל הזמנים -> פולבק קטן -> אישור (שיא חדש) -> כניסה B.

מסמן: אזור ההתנגדות שנפרץ, יום הפריצה, נרות הפולבק, יום האישור, כניסה B, סטופ B והיציאה (סטופ נגרר 3xATR).
המדגם אקראי (seed קבוע) מתוך הפריצות שאושרו, כדי להראות גם הצלחות וגם כישלונות ביחס האמיתי.

הרצה:  python sr_retest_charts.py results_retest_900 results_retest_600 --n 20 --out sr_charts/retest
(גרף ארוך של ~15 חודשים עם כל האזורים כפי שהיו ידועים ביום הפריצה + חלון זום על העסקה)
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

WHITE = dict(fc="white", ec="none", alpha=0.85, pad=1)


def chart(tk, date, path, before=300):
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
    ex = min(ex, len(df) - 1)
    e = min(len(df), max(ex, tc + 20) + 6)
    win = tr["R"] > 0
    fig = plt.figure(figsize=(20, 8))
    gs = fig.add_gridspec(2, 2, width_ratios=[3, 2], height_ratios=[4, 1], wspace=0.12, hspace=0.05)
    for col_i, (a, detail) in enumerate([(max(0, t0 - before), False), (max(0, t0 - 40), True)]):
        ax, axv = fig.add_subplot(gs[0, col_i]), fig.add_subplot(gs[1, col_i])
        d = df.iloc[a:e]
        x = lambda i: i - a
        for i, (o, h, l, c) in enumerate(d[["Open", "High", "Low", "Close"]].values):
            col = "#3B6D11" if c >= o else "#A32D2D"
            ax.vlines(i, l, h, color=col, lw=1)
            ax.add_patch(plt.Rectangle((i - 0.3, min(o, c)), 0.6, max(abs(c - o), 1e-6), color=col))
        axv.bar(range(len(d)), d["Volume"], color=np.where(d["Close"] >= d["Open"], "#97C459", "#F09595"))
        ylo, yhi = d["Low"].min(), d["High"].max()
        pad = (yhi - ylo) * 0.06
        # כל אזורי התמיכה/התנגדות כפי שהיו ידועים ביום הפריצה (חלון של 250 יום), עם נקודות הנגיעה
        for Z in lv.asof(t0):
            if Z["touches"] < sr.MIN_TOUCHES or Z["id"] == L["id"] or Z["top"] < ylo - pad or Z["bottom"] > yhi + pad:
                continue
            col = "#A32D2D" if Z["bottom"] > df["Close"].values[t0] else "#185FA5"
            z0 = max(Z["first"] - a, 0)
            ax.fill_between([z0, len(d) - 1], Z["bottom"], Z["top"], color=col,
                            alpha=0.06 + 0.02 * min(Z["touches"], 6), lw=0)
            ax.hlines(Z["top"], z0, len(d) - 1, color=col, lw=0.5 + 0.3 * min(Z["touches"], 6), alpha=0.6)
            ax.text(len(d) + 0.5, Z["top"], f" {Z['top']:.2f} ({Z['touches']}x)", color=col, fontsize=7, va="center")
            for i, p, k in Z["pts"]:
                if i >= a:
                    ax.plot(i - a, p, marker="v" if k == "H" else "^", color=col, ms=4, ls="", alpha=0.7)
        for i, p, k in L["pts"]:
            if i >= a:
                ax.plot(i - a, p, marker="v" if k == "H" else "^", color="#A32D2D", ms=6, ls="")
        x0 = max(L["first"] - a, 0)
        ax.fill_between([x0, x(t0)], L["bottom"], L["top"], color="#A32D2D", alpha=0.18, lw=0)
        ax.hlines(L["top"], x0, len(d) - 1, color="#A32D2D", lw=1.2, alpha=0.8)
        ax.text(len(d) + 0.5, L["top"], f" ATH zone {L['top']:.2f} ({L['touches']}x)", color="#A32D2D",
                fontsize=8, va="center", fontweight="bold")
        ax.axvspan(x(t0) - 0.5, x(t0) + 0.5, color="#3B6D11", alpha=0.15)
        for k in pb_days:
            ax.axvspan(x(k) - 0.5, x(k) + 0.5, color="#EF9F27", alpha=0.3)
        ax.axvspan(x(tc) - 0.5, x(tc) + 0.5, color="#185FA5", alpha=0.2)
        ts = np.asarray(tr["stop_path"], dtype=float)
        ax.plot(np.arange(x(tc + 1), x(tc + 1) + len(ts)), ts, color="#A32D2D", lw=0.9, alpha=0.6)
        ax.hlines(tr["entry"], x(tc + 1), x(ex), color="#185FA5", ls="--", lw=1.1)
        ax.plot(x(ex), tr["exit"], marker="X", ms=10, color="#3B6D11" if win else "#A32D2D", ls="")
        if detail:
            hi = df["High"].values
            ax.annotate("1 BREAKOUT", (x(t0), hi[t0]), xytext=(-60, 20), textcoords="offset points", ha="center",
                        color="#3B6D11", fontweight="bold", fontsize=9, arrowprops=dict(arrowstyle="->", color="#3B6D11"), bbox=WHITE)
            ax.annotate(f"2 PULLBACK ({len(pb_days)}d)", (x(pb_days[0]), df["Low"].values[pb_days[0]]),
                        xytext=(-40, -55), textcoords="offset points", ha="center", color="#BA7517", fontweight="bold",
                        fontsize=9, arrowprops=dict(arrowstyle="->", color="#BA7517"), bbox=WHITE)
            ax.annotate(f"3 CONFIRM (new high)\nentry B {tr['entry']:.2f}", (x(tc), hi[tc]), xytext=(55, 15),
                        textcoords="offset points", ha="center", color="#185FA5", fontweight="bold", fontsize=9,
                        arrowprops=dict(arrowstyle="->", color="#185FA5"), bbox=WHITE)
            ax.annotate(f"stop {stop:.2f}", (x(tc + 1), stop), xytext=(50, -40), textcoords="offset points",
                        color="#A32D2D", fontsize=8, arrowprops=dict(arrowstyle="->", color="#A32D2D", lw=0.8), bbox=WHITE)
            ax.set_title("zoom: the trade", fontsize=10)
        else:
            fig.suptitle(f"{tk}  breakout {df.index[t0].date()} -> pullback {len(pb_days)}d -> confirm "
                         f"{df.index[tc].date()} (+{tc - t0}d)  |  B: {tr['exit_reason']} after {tr['bars']}d, "
                         f"{tr['ret']:+.1%} = {tr['R']:+.2f}R      (zones as known on the breakout day; "
                         f"blue = support, red = resistance)", fontsize=11, color="#3B6D11" if win else "#A32D2D",
                         y=0.97)
            ax.set_title(f"{df.index[a].date()} -> {df.index[e - 1].date()}", fontsize=10)
        ax.set_ylim(ylo - pad, yhi + pad * (3 if detail else 1))
        ax.set_xlim(-1, len(d) + (14 if not detail else 10))
        axv.set_xlim(ax.get_xlim())
        ax.set_xticks([])
        step = max(1, len(d) // (12 if not detail else 6))
        axv.set_xticks(range(0, len(d), step))
        axv.set_xticklabels([z.strftime("%Y-%m-%d") for z in d.index[::step]], fontsize=8)
        axv.set_yticks([])
    fig.savefig(path, dpi=95, bbox_inches="tight")
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
