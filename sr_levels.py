"""
sr_levels.py - זיהוי רמות תמיכה והתנגדות וזיהוי פריצה מעל התנגדות, בלי הצצה לעתיד.

שיטה:
  1. נקודות מפנה (pivots): שיא שהוא הגבוה ביותר מבין PIVOT_N הנרות שלפניו ו-PIVOT_N שאחריו (שפל - באותו אופן).
     נקודה כזו "ידועה" רק PIVOT_N ימים אחרי שקרתה - כך גם בבדיקה ההיסטורית.
  2. קיבוץ לרמות: נקודות מפנה (שיאים ושפלים יחד) שקרובות זו לזו עד TOL_ATR * ATR הן רמה אחת.
     מחיר הרמה = ממוצע הנקודות; חוזק = מספר הנגיעות.
  3. טווח: רק נקודות מפנה מ-LOOKBACK הימים האחרונים.
  4. ביום t: רמות מעל המחיר = התנגדות, מתחת = תמיכה.
  5. פריצה: סגירה מעל רמת התנגדות עם לפחות MIN_TOUCHES נגיעות, בשוליים של MARGIN_ATR * ATR,
     כשהסגירה הקודמת הייתה מתחת לרמה (פריצה ראשונה, לא המשך).

הרצה:  python sr_levels.py AAPL NVDA SPY     -> sr_charts/<TICKER>_levels.png (רמות כפי שנראות היום)
"""
import os
import sys

import numpy as np
import pandas as pd

import backtest as bt

PIVOT_N = 5          # נרות מכל צד לנקודת מפנה
TOL_ATR = 0.5        # מרחק מקסימלי (ביחידות ATR) בין נקודות באותה רמה
LOOKBACK = 250       # כמה ימים אחורה מחפשים נקודות מפנה (~שנה)
MIN_TOUCHES = 2      # מינימום נגיעות להתנגדות "אמיתית"
MARGIN_ATR = 0.1     # כמה מעל הרמה הסגירה צריכה להיות


def pivots(df, n=PIVOT_N):
    """מחזיר שתי רשימות (index, price) של שיאי ושפלי מפנה. הנקודה ב-i ידועה רק ביום i+n."""
    h, l = df["High"].values, df["Low"].values
    highs, lows = [], []
    for i in range(n, len(df) - n):
        win_h, win_l = h[i - n:i + n + 1], l[i - n:i + n + 1]
        if h[i] == win_h.max() and (win_h == h[i]).sum() == 1:
            highs.append((i, h[i]))
        if l[i] == win_l.min() and (win_l == l[i]).sum() == 1:
            lows.append((i, l[i]))
    return highs, lows


def cluster(points, tol):
    """קיבוץ נקודות לפי מחיר: נקודה מצטרפת לקבוצה אם היא עד tol מהממוצע שלה."""
    levels = []
    for i, p, kind in sorted(points, key=lambda x: x[1]):
        if levels and abs(p - levels[-1]["price"]) <= tol:
            lv = levels[-1]
            lv["pts"].append((i, p, kind))
            lv["price"] = float(np.mean([q[1] for q in lv["pts"]]))
        else:
            levels.append(dict(price=p, pts=[(i, p, kind)]))
    for lv in levels:
        lv["touches"] = len(lv["pts"])
        lv["first"] = min(q[0] for q in lv["pts"])
        lv["last"] = max(q[0] for q in lv["pts"])
        lv["highs"] = sum(q[2] == "H" for q in lv["pts"])
        lv["lows"] = sum(q[2] == "L" for q in lv["pts"])
    return levels


class Levels:
    """מחשב רמות כפי שהיו ידועות בכל יום t (רק נקודות מפנה שאושרו עד t)."""

    def __init__(self, df, n=PIVOT_N, lookback=LOOKBACK, tol_atr=TOL_ATR):
        self.df, self.n, self.lookback, self.tol_atr = df, n, lookback, tol_atr
        hi, lo = pivots(df, n)
        self.pts = sorted([(i, p, "H") for i, p in hi] + [(i, p, "L") for i, p in lo])
        self.idx = np.array([p[0] for p in self.pts])
        self.atr = bt.atr14(df)

    def asof(self, t):
        """רמות ביום t: נקודות מפנה עם i + n <= t ו-i >= t - lookback."""
        a = np.searchsorted(self.idx, t - self.lookback)
        b = np.searchsorted(self.idx, t - self.n, side="right")
        return cluster(self.pts[a:b], self.tol_atr * self.atr[t])


def find_breakouts(df, start=None, end=None, min_touches=MIN_TOUCHES, margin_atr=MARGIN_ATR, lv=None):
    """פריצות: סגירה ביום t מעל רמת התנגדות (נגיעות >= min_touches) כשהסגירה ב-t-1 הייתה מתחת לה."""
    lv = lv or Levels(df)
    c = df["Close"].values
    lo = max(bt.DAILY_WARMUP, df.index.searchsorted(pd.Timestamp(start)) if start else 0)
    hi = df.index.searchsorted(pd.Timestamp(end), side="right") if end else len(df)
    out = []
    for t in range(max(lo, 1), hi):
        levels = lv.asof(t)
        thr = margin_atr * lv.atr[t]
        broken = [L for L in levels if L["touches"] >= min_touches
                  and c[t - 1] <= L["price"] and c[t] > L["price"] + thr]
        if broken:
            L = max(broken, key=lambda x: x["price"])          # הרמה הגבוהה ביותר שנפרצה היום
            above = [x for x in levels if x["price"] > c[t]]
            nxt = min(above, key=lambda x: x["price"]) if above else None
            out.append(dict(t=t, level=L, next_resistance=nxt, levels=levels))
    return out


def plot_levels(df, t, path, title="", lv=None, bars=250, after=0, breakout=None):
    """גרף נרות עם רמות התמיכה/התנגדות כפי שהיו ידועות ביום t. עובי הקו = מספר הנגיעות."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    lv = lv or Levels(df)
    levels = lv.asof(t)
    a, b = max(0, t - bars + 1), min(len(df), t + 1 + after)
    d = df.iloc[a:b]
    fig, (ax, axv) = plt.subplots(2, 1, figsize=(13, 7), sharex=True, gridspec_kw={"height_ratios": [4, 1]})
    for i, (o, h, l, c) in enumerate(d[["Open", "High", "Low", "Close"]].values):
        col = "#3B6D11" if c >= o else "#A32D2D"
        alpha = 1.0 if a + i <= t else 0.35                     # נרות אחרי t - חיוורים (עתיד)
        ax.vlines(i, l, h, color=col, lw=1, alpha=alpha)
        ax.add_patch(plt.Rectangle((i - 0.3, min(o, c)), 0.6, max(abs(c - o), 1e-6), color=col, alpha=alpha))
    axv.bar(range(len(d)), d["Volume"], color=np.where(d["Close"] >= d["Open"], "#97C459", "#F09595"))
    close_t = df["Close"].values[t]
    for L in levels:
        if L["touches"] < MIN_TOUCHES:
            continue
        col = "#A32D2D" if L["price"] > close_t else "#185FA5"
        x0 = max(L["first"] - a, 0)
        ax.hlines(L["price"], x0, len(d) - 1, color=col, lw=0.6 + 0.7 * min(L["touches"], 6), alpha=0.75)
        ax.text(len(d) - 0.5, L["price"], f" {L['price']:.2f} ({L['touches']}x)", color=col,
                fontsize=8, va="center")
        for i, p, k in L["pts"]:
            if i >= a:
                ax.plot(i - a, p, marker="v" if k == "H" else "^", color=col, ms=5, ls="")
    if after:
        ax.axvline(t - a, color="#5F5E5A", ls=":", lw=1)
    if breakout:
        ax.annotate("BREAKOUT", (t - a, df["Close"].values[t]), xytext=(0, 30), textcoords="offset points",
                    ha="center", color="#3B6D11", fontweight="bold",
                    arrowprops=dict(arrowstyle="->", color="#3B6D11"))
    ax.set_title(title or f"Support (blue) / resistance (red) as known on {df.index[t].date()}  -  "
                          f"line width = number of touches")
    ax.set_xlim(-1, len(d) + 8)
    step = max(1, len(d) // 10)
    axv.set_xticks(range(0, len(d), step))
    axv.set_xticklabels([x.strftime("%Y-%m-%d") for x in d.index[::step]], fontsize=8)
    fig.tight_layout()
    fig.savefig(path, dpi=105)
    plt.close(fig)


if __name__ == "__main__":
    os.makedirs("sr_charts", exist_ok=True)
    for tk in [a.upper() for a in sys.argv[1:]] or ["AAPL", "NVDA", "JPM", "SPY"]:
        bt.prefetch([tk])
        df = bt.load_history(tk)
        plot_levels(df, len(df) - 1, f"sr_charts/{tk}_levels.png", title=f"{tk} - support (blue) / "
                    f"resistance (red) today; line width = touches")
        print("saved", f"sr_charts/{tk}_levels.png")
