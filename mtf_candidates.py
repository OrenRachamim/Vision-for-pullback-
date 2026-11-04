"""
mtf_candidates.py - בדיקת עמידות לשתי הכניסות שנבחרו בחיפוש השעתי (mtf_search_1h), בלי כיוונון נוסף:
  A: יומי conv (התכנסות ממוצעים 10..200 + פריצה) + שעתי pdh (סגירה מעל שיא אתמול), יציאה Ld_wide
  B: שעתי hrsimacd (RSI14<30 ואז חיתוך MACD), בלי פילטר יומי, יציאה Ld_wide
  Ld_wide = יעד 1.5 ATR יומי, סטופ 1.2 ATR, עד 10 ימי מסחר.
  השוואה: כניסה אקראית עם אותו פילטר יומי ואותה יציאה.
  * לפי חצי / רבעון / מדד (S&P 500 / 400 / 600).
  * תיק: K משבצות שוות, ריבית דריבית, עסקה אחת למניה; שווי לפי עסקאות שנסגרו (ירידה מוערכת בחסר).
הרצה:  python mtf_candidates.py results_mtf_search_1h
"""
import os
import sys

import numpy as np
import pandas as pd

import backtest as bt

CANDS = {"A: conv + pdh": ("pdh", "conv"), "B: hourly RSI+MACD": ("hrsimacd", "none")}
EXIT = "Ld_wide"


def portfolio(t, K, seed=0):
    t = t.sort_values(["date", "hour"]).copy()
    days = pd.DatetimeIndex(sorted(t.date.unique()))
    t["e"] = days.searchsorted(t.date)
    t["x"] = t.e + np.ceil(t[f"bars_{EXIT}"] / 7).astype(int)
    t["_r"] = np.random.default_rng(seed).random(len(t))
    t = t.sort_values(["e", "hour", "_r"])
    cash, pos, eq, taken = 1.0, {}, [], 0
    by = {e: g for e, g in t.groupby("e")}
    for d in range(len(days)):
        for tk in [k for k, v in pos.items() if v[1] < d]:
            a, _, r = pos.pop(tk)
            cash += a * (1 + r)
        book = cash + sum(v[0] for v in pos.values())
        g = by.get(d)
        if g is not None:
            for r in g.itertuples(index=False):
                if len(pos) >= K:
                    break
                if r.ticker in pos:
                    continue
                a = min(book / K, cash)
                if a < book / K * 0.5:
                    break
                cash -= a
                pos[r.ticker] = (a, r.x, getattr(r, EXIT))
                taken += 1
        eq.append(cash + sum(v[0] for v in pos.values()))
    eq = pd.Series(eq, index=days)
    yrs = (days[-1] - days[0]).days / 365.25
    return dict(CAGR=eq.iloc[-1] ** (1 / yrs) - 1, MaxDD=(eq / eq.cummax() - 1).min(), trades=taken,
                per_year=taken / yrs, final=eq.iloc[-1])


def main(d):
    df = pd.read_pickle(os.path.join(d, "trades.pkl"))
    df = df[df[EXIT].notna()]
    days = np.sort(df.date.unique())
    cut = days[len(days) // 2]
    df["half"] = np.where(df.date < cut, "selection", "test")
    df["q"] = pd.to_datetime(df.date).dt.to_period("Q").astype(str)
    mem = {}
    for idx in ("sp500", "sp400", "sp600"):
        for ln in open(f"universes/{idx}.txt"):
            mem.setdefault(ln.strip().upper(), idx)
    df["index"] = df.ticker.map(mem)
    L = [f"# Robustness of the selected hourly-level entries (exit {EXIT}: target 1.5 ATR, stop 1.2 ATR, max 10 days)",
         f"entries {pd.Timestamp(days[0]).date()} -> {pd.Timestamp(days[-1]).date()}; selection < "
         f"{pd.Timestamp(cut).date()} <= test", ""]
    for name, (trig, dflt) in CANDS.items():
        s = df[(df.trig == trig) & (df.d == dflt)]
        r = df[(df.trig == "random") & (df.d == dflt)]
        L += [f"## {name}", "", "| slice | n | win | avg | random avg | excess |", "|---|---|---|---|---|---|"]
        for col, vals in [("half", ["selection", "test"]), ("index", ["sp500", "sp400", "sp600"]),
                          ("q", sorted(s.q.unique()))]:
            for v in vals:
                a, b = s[s[col] == v][EXIT], r[r[col] == v][EXIT]
                if len(a) < 10:
                    continue
                L.append(f"| {col}={v} | {len(a):,} | {(a > 0).mean():.0%} | {a.mean():+.2%} | {b.mean():+.2%} | "
                         f"{a.mean() - b.mean():+.2%} |")
        qs = s.groupby("q")[EXIT].mean() - r.groupby("q")[EXIT].mean()
        L += ["", f"quarters with positive excess: {(qs > 0).sum()}/{len(qs)}", "",
              "| portfolio | K | period | CAGR | max DD (realized) | trades/yr |", "|---|---|---|---|---|---|"]
        for K in (10, 20):
            for per, sub_s, sub_r in [("full", s, r), ("test half", s[s.half == "test"], r[r.half == "test"])]:
                ps, pr = portfolio(sub_s, K), portfolio(sub_r, K)
                L.append(f"| strategy | {K} | {per} | {ps['CAGR']:+.1%} | {ps['MaxDD']:.1%} | {ps['per_year']:.0f} |")
                L.append(f"| random entry, same filter+exit | {K} | {per} | {pr['CAGR']:+.1%} | {pr['MaxDD']:.1%} | "
                         f"{pr['per_year']:.0f} |")
        L.append("")
    spy = bt.load_history("SPY", refresh=True)["Close"]
    for per, a in [("full", days[0]), ("test half", cut)]:
        c = spy.loc[pd.Timestamp(a):pd.Timestamp(days[-1])]
        yrs = (c.index[-1] - c.index[0]).days / 365.25
        L.append(f"SPY buy & hold, {per}: {(c.iloc[-1] / c.iloc[0]) ** (1 / yrs) - 1:+.1%} per year, "
                 f"max DD {(c / c.cummax() - 1).min():.1%}")
    text = "\n".join(L)
    open(os.path.join(d, "candidates.md"), "w", encoding="utf-8").write(text + "\n")
    print(text)


if __name__ == "__main__":
    main(sys.argv[1])
