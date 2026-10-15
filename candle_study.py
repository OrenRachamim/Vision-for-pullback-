"""
candle_study.py - איזה נר יומי (כולל הווליום שלו) מנבא יום ירוק / חזק אחריו, בקרנות מדד.

לכל יום t מסווגים את הנר לפי מה שידוע בסגירה של t בלבד:
  color  : green (close > open) / red
  body   : |close-open| / ATR14 -> small (<0.3) / medium / large (>0.8)
  closeloc: (close-low)/(high-low) -> bottom (<1/3) / mid / top (>2/3)
  vol    : volume / ממוצע 20 ימים קודמים -> low (<0.8) / normal / high (>1.3)
           (ימי פקיעה/איזון מנוקים כמו בסורק)
ומודדים מה קרה אחר כך:
  next_green : האם יום t+1 ירוק (close > open)
  cc1        : close(t) -> close(t+1)   (כניסה בסגירה, יציאה בסגירה למחרת)
  oc1        : open(t+1) -> close(t+1)  (כניסה בפתיחה למחרת, יציאה בסגירה)
  cc2        : close(t) -> close(t+2)

כדי לא "למצוא" דפוס במקרה מתוך עשרות קבוצות:
  * גילוי: קרנות ראשיות 2012-2019. אימות: אותן קבוצות ב-2020-2026, ובנפרד בקרנות טריות.
  * מובהקות לפי תאריך: קודם ממוצע של כל הקרנות באותו יום, ואז t-test על הימים (הקרנות זזות יחד).

הרצה:  python candle_study.py            -> results_candles/
"""
import os

import numpy as np
import pandas as pd

import backtest as bt
import pullback_scanner as ps

MAIN = ["SPY", "MDY", "IJR", "XLK", "XLF", "XLV", "XLY", "XLP", "XLE", "XLI", "XLB", "XLU", "XLRE", "XLC"]
FRESH = ["QQQ", "IWM", "DIA", "VTI", "EFA", "EEM", "SMH", "XBI", "KRE", "XHB", "XRT", "IBB"]
OUT = "results_candles"


def features(tk):
    df = ps.clean_event_volume(bt.load_history(tk))
    o, h, l, c, v = (df[k] for k in ("Open", "High", "Low", "Close", "Volume"))
    atr = pd.Series(bt.atr14(df), index=df.index)
    rng = (h - l).replace(0, np.nan)
    f = pd.DataFrame(index=df.index)
    f["etf"] = tk
    f["color"] = np.where(c > o, "green", "red")
    b = (c - o).abs() / atr
    f["body"] = np.select([b < 0.3, b > 0.8], ["small", "large"], "medium")
    cl = (c - l) / rng
    f["closeloc"] = np.select([cl < 1 / 3, cl > 2 / 3], ["bottom", "top"], "mid")
    vr = v / v.rolling(20).mean().shift(1)                  # ממוצע של 20 הימים שלפני
    f["vol"] = np.select([vr < 0.8, vr > 1.3], ["low", "high"], "normal")
    f["next_green"] = (c.shift(-1) > o.shift(-1)).astype(float)
    f["cc1"] = c.shift(-1) / c - 1
    f["oc1"] = c.shift(-1) / o.shift(-1) - 1
    f["cc2"] = c.shift(-2) / c - 1
    f.loc[vr.isna() | atr.isna() | f["cc2"].isna(), ["cc1"]] = np.nan
    return f.dropna(subset=["cc1"])


def table(d, keys, base):
    """לכל קבוצה: מספר ימים, הסתברות ליום ירוק, תשואות ממוצעות, והפרש מהבסיס עם t לפי תאריך."""
    rows = []
    for k, g in d.groupby(keys):
        per_day = g.groupby(level=0)[["cc1", "oc1", "cc2", "next_green"]].mean()   # ממוצע לפי תאריך
        n = len(per_day)
        if n < 30:
            continue
        row = dict(zip(keys, k if isinstance(k, tuple) else (k,)))
        row.update(days=n, next_green=per_day.next_green.mean(),
                   cc1_bp=per_day.cc1.mean() * 1e4, oc1_bp=per_day.oc1.mean() * 1e4,
                   cc2_bp=per_day.cc2.mean() * 1e4)
        row["cc1_vs_base_bp"] = (per_day.cc1.mean() - base.mean()) * 1e4
        row["t"] = (per_day.cc1.mean() - base.mean()) / (per_day.cc1.std(ddof=1) / np.sqrt(n))
        rows.append(row)
    return pd.DataFrame(rows)


def run(etfs, start, end):
    d = pd.concat([features(t) for t in etfs])
    d = d[(d.index >= start) & (d.index <= end)]
    base = d.groupby(level=0)["cc1"].mean()                     # יום ממוצע (כל הקרנות)
    return d, base


def fmt(df):
    cols = [c for c in df.columns]
    out = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    for _, r in df.iterrows():
        cells = []
        for c in cols:
            v = r[c]
            if c == "days":
                cells.append(f"{int(v):,}")
            elif c == "next_green":
                cells.append(f"{v:.1%}")
            elif isinstance(v, float):
                cells.append(f"{v:+.1f}" if c != "t" else f"{v:+.2f}")
            else:
                cells.append(str(v))
        out.append("| " + " | ".join(cells) + " |")
    return "\n".join(out)


def main():
    bt.prefetch(MAIN + FRESH)
    os.makedirs(OUT, exist_ok=True)
    sets = {"train: main 2012-2019": run(MAIN, "2012-01-01", "2019-12-31"),
            "test: main 2020-2026": run(MAIN, "2020-01-01", "2026-12-31"),
            "test: fresh 2012-2026": run(FRESH, "2012-01-01", "2026-12-31")}
    L = ["# Candle study: which daily candle (and its volume) predicts the next day - index ETFs", "",
         "Returns in basis points (1bp = 0.01%). `cc1` = close(t)->close(t+1), `oc1` = open(t+1)->close(t+1),",
         "`cc2` = close(t)->close(t+2). `t` = date-clustered t-stat of cc1 vs an average day. |t| > 2 ~ significant,",
         "but with ~50 groups expect 2-3 such results by chance - only results that repeat in BOTH test sets count.", ""]
    for name, (d, base) in sets.items():
        L += [f"* {name}: {d.etf.nunique()} ETFs, {len(base):,} days, average day: next green "
              f"{d.groupby(level=0).next_green.mean().mean():.1%}, cc1 {base.mean() * 1e4:+.1f}bp"]
    L.append("")

    views = [("color + body + volume", ["color", "body", "vol"]),
             ("color + close location + volume", ["color", "closeloc", "vol"]),
             ("volume alone", ["vol"]), ("color + body", ["color", "body"])]
    merged = {}
    for title, keys in views:
        L += [f"## {title}", ""]
        parts = []
        for name, (d, base) in sets.items():
            t = table(d, keys, base).set_index(keys)
            t.columns = pd.MultiIndex.from_product([[name], t.columns])
            parts.append(t)
        m = pd.concat(parts, axis=1)
        merged[title] = m
        show = pd.DataFrame(index=m.index)
        for name in sets:
            short = name.split(":")[0] + (" fresh" if "fresh" in name else (" 20-26" if "2020" in name else ""))
            show[f"{short} days"] = m[(name, "days")]
            show[f"{short} green%"] = m[(name, "next_green")]
            show[f"{short} cc1"] = m[(name, "cc1_vs_base_bp")]
            show[f"{short} t"] = m[(name, "t")]
        show = show.reset_index()
        cols = list(show.columns)
        out = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
        for _, r in show.iterrows():
            cells = []
            for c in cols:
                v = r[c]
                if isinstance(v, str):
                    cells.append(v)
                elif "days" in c:
                    cells.append("" if v != v else f"{int(v):,}")
                elif "green%" in c:
                    cells.append("" if v != v else f"{v:.1%}")
                elif c.endswith(" t"):
                    cells.append("" if v != v else (f"**{v:+.2f}**" if abs(v) > 2 else f"{v:+.2f}"))
                else:
                    cells.append("" if v != v else f"{v:+.1f}")
            out.append("| " + " | ".join(cells) + " |")
        L += out + [""]

    # קבוצות שמובהקות בגילוי - האם הן חוזרות בשני מבחני האימות?
    L += ["## Groups significant in the discovery period - do they hold up?", ""]
    m = merged["color + body + volume"]
    tr = m["train: main 2012-2019"]
    sig = tr[tr["t"].abs() > 2].index
    rows = []
    for k in sig:
        r = dict(group=" / ".join(k))
        for name in sets:
            r[name] = f"{m.loc[k, (name, 'cc1_vs_base_bp')]:+.1f}bp (t={m.loc[k, (name, 't')]:+.2f})"
        rows.append(r)
    L += [fmt(pd.DataFrame(rows)) if rows else "none", ""]
    text = "\n".join(L)
    open(os.path.join(OUT, "summary.md"), "w", encoding="utf-8").write(text)
    for title, m in merged.items():
        m.to_csv(os.path.join(OUT, title.replace(" ", "_").replace("+", "") + ".csv"))
    print(text)
    return sets, merged


if __name__ == "__main__":
    main()
