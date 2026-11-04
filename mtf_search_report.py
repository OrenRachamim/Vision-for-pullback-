"""
mtf_search_report.py - ניתוח החיפוש של mtf_search.py: בחירה על חצי ימים ראשון, בדיקה על החצי השני.

  * לכל שילוב (טריגר x פילטר יומי x פילטר שעתי) ולכל יציאה: ממוצע לעסקה, ו"עודף" = ממוצע פחות כניסה אקראית
    עם אותם פילטרים ואותה יציאה באותה תקופה.
  * בוחרים את הטובים לפי העודף בחצי הראשון (לפחות MIN_N עסקאות) ומדווחים את החצי השני.
  * השוואת יציאות: מדורגת מול רמה אחת, על כל העסקאות.
הרצה:  python mtf_search_report.py results_mtf_search      (או results_mtf_search_1h - החיפוש השעתי)
"""
import os
import sys

import numpy as np
import pandas as pd

import mtf_search as S5
import mtf_search_1h as S1

MIN_N = 100


def clustered_ci(g, col, n=2000, seed=0):
    per = g.groupby("date")[col].agg(["sum", "count"])
    if len(per) < 3:
        return np.nan, np.nan
    idx = np.random.default_rng(seed).integers(0, len(per), (n, len(per)))
    b = per["sum"].values[idx].sum(1) / per["count"].values[idx].sum(1)
    return np.percentile(b, 2.5), np.percentile(b, 97.5)


def main(d, S=S5):
    df = pd.read_pickle(os.path.join(d, "trades.pkl"))
    days = np.sort(df.date.unique())
    cut = days[len(days) // 2]
    df["half"] = np.where(df.date < cut, "sel", "test")
    ex = S.EXITS
    L = [f"# Multi-timeframe search - {df.ticker.nunique()} stocks, entries {pd.Timestamp(days[0]).date()} -> "
         f"{pd.Timestamp(days[-1]).date()} ({len(days)} days); selection < {pd.Timestamp(cut).date()} <= test", "",
         f"combos: {len(S.TRIGGERS) - 1} triggers x {len(S.D_FILTERS)} daily x {len(S.H_FILTERS)} hourly = "
         f"{(len(S.TRIGGERS) - 1) * len(S.D_FILTERS) * len(S.H_FILTERS)}, x {len(ex)} exits = "
         f"{(len(S.TRIGGERS) - 1) * len(S.D_FILTERS) * len(S.H_FILTERS) * len(ex)} tested configurations", ""]
    # השוואת יציאות על כל העסקאות (כל הטריגרים, בלי פילטרים) ועל כניסה אקראית
    base = df[(df.d == "none") & (df.hf == "none")]
    L += ["## Exits compared (no filters; avg per trade after costs)", "",
          "| exit | random entry (all) | all 4 triggers | random, sel half | random, test half |", "|---|---|---|---|---|"]
    for e in ex:
        r = base[base.trig == "random"]
        t = base[base.trig != "random"]
        L.append(f"| {e} | {r[e].mean():+.3%} | {t[e].mean():+.3%} | {r[r.half == 'sel'][e].mean():+.3%} | "
                 f"{r[r.half == 'test'][e].mean():+.3%} |")
    st = base[base.trig == "random"]
    for s in S.SETS:
        vc = st[f"stage_{s}"].value_counts(normalize=True).sort_index()
        L.append(f"\ncascade {s}: exits at stage 1 {vc.get(1, 0):.0%}, stage 2 {vc.get(2, 0):.0%}, "
                 f"stage 3 {vc.get(3, 0):.0%}")
    # טבלת שילובים
    g = df.groupby(["trig", "d", "hf", "half"])
    agg = g[ex].mean()
    cnt = g.size().rename("n")
    tab = agg.join(cnt).reset_index()
    rnd = tab[tab.trig == "random"].set_index(["d", "hf", "half"])
    rows = []
    for r in tab[tab.trig != "random"].itertuples(index=False):
        key = (r.d, r.hf, r.half)
        if key not in rnd.index:
            continue
        for e in ex:
            rows.append(dict(trig=r.trig, d=r.d, hf=r.hf, half=r.half, exit=e, n=r.n, avg=getattr(r, e),
                             rand=rnd.loc[key, e], excess=getattr(r, e) - rnd.loc[key, e]))
    R = pd.DataFrame(rows)
    sel = R[(R.half == "sel") & (R.n >= MIN_N)].set_index(["trig", "d", "hf", "exit"])
    tst = R[R.half == "test"].set_index(["trig", "d", "hf", "exit"])
    both = sel.join(tst, lsuffix="_sel", rsuffix="_test", how="inner")
    both = both[both.n_test >= 30]
    L += ["", f"## Top 20 by selection-half excess over random (n_sel >= {MIN_N}) -> what happened in the test half", "",
          "| trigger | daily | hourly | exit | n sel | avg sel | excess sel | n test | avg test | random test | excess test |",
          "|---|---|---|---|---|---|---|---|---|---|---|"]
    top = both.sort_values("excess_sel", ascending=False).head(20)
    for k, r in top.iterrows():
        L.append(f"| {k[0]} | {k[1]} | {k[2]} | {k[3]} | {r.n_sel:.0f} | {r.avg_sel:+.3%} | {r.excess_sel:+.3%} | "
                 f"{r.n_test:.0f} | {r.avg_test:+.3%} | {r.rand_test:+.3%} | {r.excess_test:+.3%} |")
    L += ["", f"top-20 average excess: selection {top.excess_sel.mean():+.3%} -> test {top.excess_test.mean():+.3%}",
          f"all {len(both)} configs: corr(excess sel, excess test) = {both.excess_sel.corr(both.excess_test):+.2f}; "
          f"share with positive test excess: {(both.excess_test > 0).mean():.0%}; "
          f"share with positive test avg: {(both.avg_test > 0).mean():.0%}"]
    # הטובה ביותר: CI בבדיקה
    k = top.index[0]
    g_t = df[(df.trig == k[0]) & (df.d == k[1]) & (df.hf == k[2]) & (df.half == "test")]
    lo, hi = clustered_ci(g_t, k[3])
    L += ["", f"best selected config {k}: test avg {g_t[k[3]].mean():+.3%}, 95% date-clustered CI [{lo:+.3%}, {hi:+.3%}], "
              f"win {(g_t[k[3]] > 0).mean():.0%}, n {len(g_t)}"]
    text = "\n".join(L)
    open(os.path.join(d, "summary.md"), "w", encoding="utf-8").write(text + "\n")
    R.to_csv(os.path.join(d, "configs.csv"), index=False)
    print(text)


if __name__ == "__main__":
    main(sys.argv[1], S1 if "1h" in sys.argv[1] else S5)
