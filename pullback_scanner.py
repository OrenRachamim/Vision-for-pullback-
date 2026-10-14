"""
pullback_scanner.py - זיהוי דפוס פולבק בארבעה שלבים (ירידה > האטה > בסיס > עלייה)
בגרף יומי ושבועי, וציור גרף נרות + ווליום עם השלבים צבועים.

הרצה במחשב שלך (Windows):
    pip install yfinance pandas numpy matplotlib
    python pullback_scanner.py AAPL MSFT NVDA AMD
בלי טיקרים -> רץ על נתוני דמה (לבדיקת הלוגיקה והגרף).
"""
import sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# ---------- ספים (לכוונון) ----------
DAILY = dict(min_drop=0.05, lookback=40, base_min=3, base_max=10, vol_mult=1.5)
WEEKLY = dict(min_drop=0.10, lookback=26, base_min=2, base_max=6, vol_mult=1.3)

PHASE_COLORS = {"decline": "#F7C1C1", "slowdown": "#FAC775",
                "base": "#B5D4F4", "rise": "#C0DD97"}
PHASE_NAMES = {"decline": "1 Decline", "slowdown": "2 Slowdown",
               "base": "3 Base", "rise": "4 Rise"}


def load(ticker, interval="1d", period="2y"):
    import yfinance as yf
    df = yf.download(ticker, period=period, interval=interval,
                     progress=False, auto_adjust=True)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    return df[["Open", "High", "Low", "Close", "Volume"]].dropna()


def to_weekly(df):
    return df.resample("W-FRI").agg({"Open": "first", "High": "max", "Low": "min",
                                     "Close": "last", "Volume": "sum"}).dropna()


def detect(df, p):
    """מחזיר dict עם גבולות ארבעת השלבים, או None אם אין דפוס בסוף הגרף."""
    if len(df) < p["lookback"] + 30:
        return None
    d = df.iloc[-p["lookback"]:].copy()
    vol_avg = df["Volume"].rolling(20).mean().iloc[-p["lookback"]:]
    body = (d["Close"] - d["Open"]).abs()
    atr = (d["High"] - d["Low"]).rolling(5).mean()
    c, lo, hi = d["Close"].values, d["Low"].values, d["High"].values

    # מסנן מגמה: מחיר מעל SMA200 (או SMA40 בשבועי)
    sma_len = 200 if len(df) > 260 else 40
    sma = df["Close"].rolling(sma_len).mean().iloc[-1]
    uptrend = bool(np.isnan(sma) or df["Close"].iloc[-1] > sma)

    # שלב 4: נר אחרון ירוק שנסגר מעל טווח הבסיס עם ווליום חזק
    # שלב 3: חיפוש בסיס - חלון שבו אין שפל חדש וטווח צר
    best = None
    for blen in range(p["base_min"], p["base_max"] + 1):
        b_end = len(d) - 1               # הנר האחרון = נר הפריצה
        b_start = b_end - blen
        if b_start < 8:
            continue
        base = d.iloc[b_start:b_end]
        base_hi, base_lo = base["High"].max(), base["Low"].min()
        last = d.iloc[-1]
        breakout = (last["Close"] > last["Open"] and last["Close"] > base_hi * 0.998
                    and last["Volume"] > p["vol_mult"] * vol_avg.iloc[-1])
        tight = (base_hi - base_lo) / base_lo < 0.05
        # בבסיס אסור שפל חדש משמעותי אחרי 2 הנרות הראשונים
        no_new_low = base["Low"].iloc[2:].min() >= base["Low"].iloc[:2].min() * 0.985
        if not (breakout and tight and no_new_low):
            continue
        # שלב 1+2: לפני הבסיס - ירידה משיא
        pre = d.iloc[:b_start]
        peak_i = int(np.argmax(pre["High"].values))
        drop = (pre["High"].iloc[peak_i] - base_lo) / pre["High"].iloc[peak_i]
        if drop < p["min_drop"] or b_start - peak_i < 4:
            continue
        # חלוקת הירידה: האטה = החלק שבו גופי הנרות והווליום קטנים מתחילת הירידה
        # תחילת ההאטה = אחרי הנר האדום הגדול האחרון של הירידה
        dec_body = body.iloc[peak_i + 1:b_start]
        big = np.where(dec_body.values > dec_body.median() * 1.2)[0]
        half = peak_i + 1 + (int(big[-1]) + 1 if len(big) else len(dec_body) // 2)
        half = min(max(half, peak_i + 2), b_start - 1)
        early_body = body.iloc[peak_i + 1:half].mean()
        late_body = body.iloc[half:b_start].mean()
        early_vol = d["Volume"].iloc[peak_i + 1:half].mean()
        base_vol = base["Volume"].mean()
        slowing = late_body < early_body * 0.8
        drying = base_vol < early_vol * 0.8
        score = 25 * slowing + 25 * drying + 25 * tight + 25 * uptrend
        cand = dict(peak=peak_i, slow=half, base=b_start, rise=b_end,
                    drop=drop, base_hi=base_hi, base_lo=base_lo,
                    slowing=slowing, drying=drying, uptrend=uptrend,
                    score=score, offset=len(df) - len(d))
        best = cand          # ממשיכים - הבסיס הארוך ביותר שעדיין עומד בתנאים מנצח
    return best


def plot(df, res, title, path, bars=80):
    d = df.iloc[-bars:]
    off = len(df) - bars
    fig, (ax, axv) = plt.subplots(2, 1, figsize=(12, 7), sharex=True,
                                  gridspec_kw={"height_ratios": [3, 1]})
    x = np.arange(len(d))
    up = d["Close"] >= d["Open"]
    for i, (o, h, l, c_) in enumerate(d[["Open", "High", "Low", "Close"]].values):
        col = "#3B6D11" if c_ >= o else "#A32D2D"
        ax.vlines(i, l, h, color=col, lw=1)
        ax.add_patch(Rectangle((i - 0.3, min(o, c_)), 0.6, max(abs(c_ - o), 1e-6),
                               color=col))
    axv.bar(x, d["Volume"], color=np.where(up, "#97C459", "#F09595"), width=0.7)
    axv.plot(x, df["Volume"].rolling(20).mean().iloc[-bars:].values,
             color="#5F5E5A", lw=1, label="Vol MA20")

    if res:
        g = res["offset"] - off      # המרה לאינדקס בגרף
        spans = [("decline", res["peak"], res["slow"]),
                 ("slowdown", res["slow"], res["base"]),
                 ("base", res["base"], res["rise"]),
                 ("rise", res["rise"], res["rise"] + 1)]
        for k, a, b in spans:
            a, b = a + g, b + g
            for axx in (ax, axv):
                axx.axvspan(a - 0.5, b - 0.5, color=PHASE_COLORS[k], alpha=0.45, lw=0)
            if k != "rise":
                ax.text((a + b - 1) / 2, d["High"].max() * 1.005,
                        PHASE_NAMES[k], ha="center", va="bottom", fontsize=9)
        ax.axhline(res["base_hi"], color="#185FA5", ls="--", lw=1, label="Entry (base high)")
        ax.axhline(res["base_lo"], color="#A32D2D", ls="--", lw=1, label="Stop (base low)")
        ax.annotate("BUY", (res["rise"] + g, d["Low"].iloc[res["rise"] + g]),
                    xytext=(0, -30), textcoords="offset points", ha="center",
                    arrowprops=dict(arrowstyle="->", color="#3B6D11"), color="#3B6D11")
        title += f"  |  score {res['score']}/100  drop {res['drop']:.1%}"
    ax.set_title(title)
    if res:
        ax.legend(loc="upper left", fontsize=8)
    step = max(1, bars // 8)
    axv.set_xticks(x[::step])
    axv.set_xticklabels([t.strftime("%Y-%m-%d") for t in d.index[::step]], fontsize=8)
    fig.tight_layout()
    fig.savefig(path, dpi=110)
    plt.close(fig)


def demo_data(seed=7):
    """נתוני דמה: מגמה עולה, ירידה, האטה, בסיס, פריצה."""
    rng = np.random.default_rng(seed)
    closes, vols = [], []
    p = 80.0
    for _ in range(220):  p *= 1 + rng.normal(0.0025, 0.012); closes.append(p); vols.append(rng.normal(1.0, .15))
    for _ in range(7):    p *= 1 + rng.normal(-0.018, .006); closes.append(p); vols.append(rng.normal(1.6, .15))
    for _ in range(5):    p *= 1 + rng.normal(-0.006, .003); closes.append(p); vols.append(rng.normal(.9, .1))
    for _ in range(6):    p *= 1 + rng.normal(0.0, .003);   closes.append(p); vols.append(rng.normal(.55, .05))
    p *= 1.03; closes.append(p); vols.append(2.0)
    idx = pd.bdate_range(end="2026-10-14", periods=len(closes))
    c = np.array(closes)
    o = np.r_[c[0], c[:-1]] * (1 + rng.normal(0, .002, len(c)))
    o[-1] = c[-2]
    hi = np.maximum(o, c) * (1 + np.abs(rng.normal(0, .004, len(c))))
    lo = np.minimum(o, c) * (1 - np.abs(rng.normal(0, .004, len(c))))
    return pd.DataFrame({"Open": o, "High": hi, "Low": lo, "Close": c,
                         "Volume": np.array(vols) * 5e6}, index=idx)


def scan(ticker, df=None):
    df = load(ticker) if df is None else df
    rd = detect(df, DAILY)
    wk = to_weekly(df)
    rw = detect(wk, WEEKLY)
    plot(df, rd, f"{ticker} daily", f"{ticker}_daily.png")
    plot(wk, rw, f"{ticker} weekly", f"{ticker}_weekly.png", bars=60)
    signal = rd is not None and rw is not None
    print(f"{ticker:6s} daily={'YES' if rd else 'no ':3s} "
          f"weekly={'YES' if rw else 'no ':3s} -> {'BUY SIGNAL' if signal else '-'}")
    return rd, rw


if __name__ == "__main__":
    tickers = sys.argv[1:]
    if not tickers:
        scan("DEMO", demo_data())
    for t in tickers:
        try:
            scan(t)
        except Exception as e:
            print(t, "error:", e)
