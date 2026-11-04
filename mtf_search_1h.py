"""
mtf_search_1h.py - אותו חיפוש רמה אחת למעלה, על שנתיים: פילטר יומי x טריגר שעתי, יציאה מדורגת שעתי -> יומי.

  יומי : none | up | conv | pull | high   (כמו mtf_search)
  שעתי : hrsimacd (RSI14<30 ב-3 נרות ואז חיתוך MACD) | hmacd | pdh (פריצת שיא אתמול) |
         hma (חזרה מעל SMA20 שעתי אחרי 7 נרות מתחתיו) | random
  כניסה בפתיחת הנר השעתי הבא; עסקה ראשונה בכל יום; טריגר בנרות 10:30-14:30.
  יציאות (ATR יומי; T בנרות שעה, 7 ליום): eod; next (סגירת מחר); L1h_{tight,wide}; Ld_{tight,wide};
          casc (שעתי -> יומי אם C>SMA20 יומי) ו-casc_nc.
  בחירה = חצי ראשון של הימים (~2024 - אמצע 2025), בדיקה = חצי שני.

הרצה:  python mtf_search_1h.py --out results_mtf_search_1h  &&  python mtf_search_report.py results_mtf_search_1h
"""
import argparse
import os
import zlib
from concurrent.futures import ProcessPoolExecutor

import numpy as np
import pandas as pd

import backtest as bt
import mtf_data as md
import mtf_search as S5
import mtf_strategy as ms

SETS = {"tight": [(0.5, 0.5, 7), (1.0, 1.0, 35)], "wide": [(0.8, 0.7, 14), (1.5, 1.2, 70)]}
MAX_BARS = 14 + 70 + 5
TRIGGERS = ("hrsimacd", "hmacd", "pdh", "hma", "random")
D_FILTERS, H_FILTERS = S5.D_FILTERS, ("none",)
EXITS = ["eod", "next"] + [f"{lvl}_{s}" for s in SETS for lvl in ("L1h", "Ld", "casc", "casc_nc")]


def features(tk):
    d, hr = md.load(tk, "daily"), md.load(tk, "1h")
    if len(d) < 300 or len(hr) < 400:
        return None
    C = d["Close"]
    s20, s50, s200 = (C.rolling(n).mean() for n in (20, 50, 200))
    datr = bt.atr14(d)
    up = (C > s50) & (s50 > s200)
    r2 = pd.Series(ms.rsi(C.values, 2), index=d.index)
    hi60 = d["High"].rolling(60).max()
    ds = ms.daily_signals(d)
    armed = np.zeros(len(d), bool)
    for i in np.nonzero(ds["signal"].values)[0]:
        armed[i:i + 5] = True
    dflt = {"none": np.ones(len(d), bool), "up": up.values, "conv": armed,
            "pull": (up & (r2 < 15)).values, "high": (up & (C >= 0.97 * hi60)).values}
    t = hr.index
    bar_days = t.tz_localize(None).normalize()
    o, h, l, c = (hr[k].values.astype(np.float64) for k in ("Open", "High", "Low", "Close"))
    day_id = pd.factorize(bar_days)[0].astype(np.int64)
    minutes = (t.hour * 60 + t.minute).values
    di = pd.DatetimeIndex(d.index)
    D = {k: S5._map_prev_day(di, bar_days, v.astype(float)) > 0.5 for k, v in dflt.items()}
    datr_b = S5._map_prev_day(di, bar_days, datr)
    dconf = S5._map_prev_day(di, bar_days, (C > s20).values.astype(float)) > 0.5
    pdh = S5._map_prev_day(di, bar_days, d["High"].values)
    r = ms.rsi(c)
    mc, sg = ms.macd(c)
    cross = np.zeros(len(c), bool)
    cross[1:] = (mc[1:] > sg[1:]) & (mc[:-1] <= sg[:-1])
    os_ = pd.Series(r).rolling(3, min_periods=1).min().values < 30
    brk = np.zeros(len(c), bool)
    brk[1:] = (c[1:] > pdh[1:]) & ~((c[:-1] > pdh[:-1]) & (day_id[:-1] == day_id[1:]))
    h20 = pd.Series(c).rolling(20).mean().values
    below7 = pd.Series(c < h20).rolling(7).sum().shift(1).values == 7
    hma = np.zeros(len(c), bool)
    hma[1:] = (c[1:] > h20[1:]) & below7[1:]
    window = (minutes >= 630) & (minutes <= 870) & (np.arange(len(c)) > 100) & np.isfinite(datr_b)
    window[len(c) - MAX_BARS:] = False
    rng = np.random.default_rng(zlib.crc32(tk.encode()))
    rnd = np.zeros(len(c), bool)
    for dd in np.unique(day_id):
        js = np.nonzero((day_id == dd) & window)[0]
        if len(js):
            rnd[rng.choice(js)] = True
    TR = {"hrsimacd": cross & os_, "hmacd": cross, "pdh": brk, "hma": hma, "random": rnd}
    TR = {k: v & window for k, v in TR.items()}
    return dict(o=o, h=h, l=l, c=c, day_id=day_id, minutes=minutes, dates=np.asarray(bar_days), datr=datr_b, D=D,
                H={"none": np.ones(len(c), bool)}, dconf=dconf, TR=TR)


def outcomes(F, j):
    e = j + 1
    o, h, l, c, day_id = F["o"], F["h"], F["l"], F["c"], F["day_id"]
    datr = F["datr"][j]
    res = {}
    x = S5.run_eod(c, e, day_id)
    res["eod"] = x / o[e] if x == x else np.nan
    nx = np.nonzero(day_id == day_id[e] + 1)[0]
    res["next"] = c[nx[-1]] / o[e] if len(nx) else np.nan
    for s, st in SETS.items():
        A = np.array([q[0] for q in st]); Sx = np.array([q[1] for q in st]); T = np.array([q[2] for q in st], np.int64)
        for lvl, idx, conf in [("L1h", [0], False), ("Ld", [1], False), ("casc", [0, 1], True), ("casc_nc", [0, 1], False)]:
            px, xi, stage, code = S5.run_exit(o, h, l, c, e, datr, A[idx], Sx[idx], T[idx], len(idx),
                                              F["dconf"], F["dconf"], conf)
            res[f"{lvl}_{s}"] = px / o[e] if px == px else np.nan
            res[f"bars_{lvl}_{s}"] = xi - e + 1                  # שעות מסחר בעסקה (לסימולציית תיק)
            if lvl == "casc":
                res[f"stage_{s}"] = stage
    return {k: (v * (1 - S5.COST) / (1 + S5.COST) - 1 if not k.startswith(("stage", "bars")) else v)
            for k, v in res.items()}


def run_ticker(tk):
    try:
        F = features(tk)
    except Exception:  # noqa: BLE001
        return []
    if F is None:
        return []
    rows, cache = [], {}
    for trig, tm in F["TR"].items():
        for dn in S5.D_FILTERS:
            js = np.nonzero(tm & F["D"][dn])[0]
            if len(js) == 0:
                continue
            first = js[np.r_[True, F["day_id"][js[1:]] != F["day_id"][js[:-1]]]]
            for j in first:
                if j not in cache:
                    cache[j] = outcomes(F, j)
                rows.append(dict(ticker=tk, date=F["dates"][j], hour=int(F["minutes"][j]), trig=trig, d=dn, hf="none",
                                 **cache[j]))
    return rows


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--universe", nargs="+", default=["universes/sp500.txt", "universes/sp400.txt",
                                                      "universes/sp600.txt"])
    ap.add_argument("--out", default="results_mtf_search_1h")
    args = ap.parse_args(argv)
    tk = list(dict.fromkeys(ln.strip().upper() for f in args.universe for ln in open(f) if ln.strip()))
    tk = [t for t in tk if os.path.exists(f"{md.DIRS['1h']}/{t}.pkl")]
    rows = []
    with ProcessPoolExecutor(4) as ex:
        for r in ex.map(run_ticker, tk, chunksize=8):
            rows += r
    df = pd.DataFrame(rows)
    os.makedirs(args.out, exist_ok=True)
    df.to_pickle(os.path.join(args.out, "trades.pkl"))
    print(len(df), "trade rows;", df.date.nunique(), "entry days", df.date.min(), "->", df.date.max())


if __name__ == "__main__":
    main()
