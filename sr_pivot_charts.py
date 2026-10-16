"""
sr_pivot_charts.py - גרפים לדוגמה של עסקאות נקודות ציר (לימיט קנייה ב-S2 של אתמול, יציאה בסגירה של היום השני).

כל גרף: ~30 נרות לפני העסקה. נר האיתות (אתמול) מסומן; ממנו מחושבים P / S1 / S2 / R1 ליום הכניסה
(קווים מקווקווים ביום הכניסה). מסומנים: מילוי הלימיט, הסטופ, והיציאה.
המדגם אקראי (seed קבוע) מתוך כל העסקאות מ-2023, כדי להראות הצלחות וכישלונות ביחס האמיתי.

הרצה:  python sr_pivot_charts.py --n 12 --out sr_charts/pivot
"""
import argparse
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

import sr_optimize as O  # noqa: E402
import sr_pivot_check as PC  # noqa: E402
import sr_strategies as S  # noqa: E402

WHITE = dict(fc="white", ec="none", alpha=0.85, pad=1)


def chart(r, path, before=30, after=4):
    F = S.feats(r.ticker)
    idx = F.index
    t, e, x = idx.get_loc(r.sig), idx.get_loc(r.entry), idx.get_loc(r.exit)
    a, b = max(0, t - before), min(len(F), x + after + 1)
    d = F.iloc[a:b]
    X = lambda i: i - a
    o, h, l, c = (F[k].values for k in ("o", "h", "l", "c"))
    P, S1, S2, R1 = (F[k].values[t] for k in ("pP", "pS1", "pS2", "pR1"))
    stop = S2 - PC.BASE["stop_atr"] * F["atr"].values[t]

    fig, (ax, axv) = plt.subplots(2, 1, figsize=(12, 7), sharex=True, gridspec_kw={"height_ratios": [4, 1]})
    for i, (oo, hh, ll, cc) in enumerate(d[["o", "h", "l", "c"]].values):
        col = "#3B6D11" if cc >= oo else "#A32D2D"
        ax.vlines(i, ll, hh, color=col, lw=1)
        ax.add_patch(plt.Rectangle((i - 0.3, min(oo, cc)), 0.6, max(abs(cc - oo), 1e-6), color=col))
    axv.bar(range(len(d)), d["v"], color=np.where(d["c"] >= d["o"], "#97C459", "#F09595"))
    ax.plot(range(len(d)), d["sma200"], color="#888780", lw=1, label="SMA200")
    # נר האיתות ורמות הציר ליום הכניסה
    ax.axvspan(X(t) - 0.5, X(t) + 0.5, color="#888780", alpha=0.15)
    ax.annotate(f"signal day\nH {h[t]:.2f}  L {l[t]:.2f}  C {c[t]:.2f}", (X(t), h[t]), xytext=(-70, 30),
                textcoords="offset points", fontsize=8, color="#444441", bbox=WHITE,
                arrowprops=dict(arrowstyle="->", color="#888780"))
    x0, x1 = X(e) - 0.6, X(x) + 0.6
    for val, name, col, ls in [(R1, "R1", "#A32D2D", ":"), (P, "P", "#444441", "--"), (S1, "S1", "#185FA5", ":"),
                               (S2, "S2 = buy limit", "#185FA5", "-"), (stop, "stop", "#A32D2D", "--")]:
        ax.hlines(val, x0, x1 + 2, color=col, ls=ls, lw=1.3 if name.startswith("S2") else 1)
        ax.text(x1 + 2.2, val, f"{name} {val:.2f}", color=col, fontsize=8, va="center",
                fontweight="bold" if name.startswith("S2") else None)
    ax.axvspan(X(e) - 0.5, X(x) + 0.5, color="#185FA5", alpha=0.08)
    ax.plot(X(e), r.pe, marker="^", ms=11, color="#185FA5", ls="")
    ax.annotate(f"BUY {r.pe:.2f}" + (" (gap open)" if r.pe < S2 - 1e-6 else ""), (X(e), r.pe), xytext=(-60, -30),
                textcoords="offset points", fontsize=9, color="#185FA5", fontweight="bold", bbox=WHITE,
                arrowprops=dict(arrowstyle="->", color="#185FA5"))
    win = r.ret > 0
    ax.plot(X(x), r.px, marker="X", ms=11, color="#3B6D11" if win else "#A32D2D", ls="")
    ax.annotate(f"SELL {r.px:.2f} ({r.reason})", (X(x), r.px), xytext=(15, 25), textcoords="offset points",
                fontsize=9, color="#3B6D11" if win else "#A32D2D", fontweight="bold", bbox=WHITE,
                arrowprops=dict(arrowstyle="->", color="#3B6D11" if win else "#A32D2D"))
    drop = (S2 / c[t] - 1) * 100
    ax.set_title(f"{r.ticker}  signal {r.sig.date()} -> buy {r.entry.date()} at S2 ({drop:+.1f}% below close) -> "
                 f"sell {r.exit.date()}  |  {r.ret:+.2%} after costs", fontsize=10,
                 color="#3B6D11" if win else "#A32D2D")
    lo_, hi_ = min(d["l"].min(), stop), max(d["h"].max(), R1)
    ax.set_ylim(lo_ - (hi_ - lo_) * 0.05, hi_ + (hi_ - lo_) * 0.08)
    ax.set_xlim(-1, len(d) + 9)
    ax.legend(loc="upper left", fontsize=8)
    step = max(1, len(d) // 8)
    axv.set_xticks(range(0, len(d), step))
    axv.set_xticklabels([z.strftime("%Y-%m-%d") for z in d.index[::step]], fontsize=8)
    axv.set_yticks([])
    fig.tight_layout()
    fig.savefig(path, dpi=100)
    plt.close(fig)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=12)
    ap.add_argument("--since", default="2023-01-01")
    ap.add_argument("--out", default="sr_charts/pivot")
    args = ap.parse_args(argv)
    u = O.universe("universes/sp500.txt", "universes/sp400.txt")
    rng = np.random.default_rng(3)
    sub = list(rng.choice(u, 120, replace=False))
    tr = pd.concat([pd.DataFrame(S.run_ticker((tk, "pivot", PC.BASE, args.since)),
                                 columns=["ticker", "sig", "entry", "exit", "pe", "px", "reason", "score"])
                    for tk in sub])
    tr = tr[tr.reason != "open"]
    tr["ret"] = tr.px * (1 - S.COST) / (tr.pe * (1 + S.COST)) - 1
    print(f"{len(tr)} trades in sample pool: win {(tr.ret > 0).mean():.0%}, avg {tr.ret.mean():+.2%}")
    pick = tr.sample(args.n, random_state=1).sort_values("entry")
    os.makedirs(args.out, exist_ok=True)
    for i, r in enumerate(pick.itertuples(), 1):
        p = os.path.join(args.out, f"{i:02d}_{r.ticker}_{r.entry.date()}.png")
        chart(r, p)
        print(f"{p}  {r.ret:+.2%} {r.reason}")
    print(f"shown: win {(pick.ret > 0).mean():.0%}, avg {pick.ret.mean():+.2%}")


if __name__ == "__main__":
    main()
