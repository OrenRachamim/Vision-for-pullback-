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
import matplotlib.transforms
from matplotlib.patches import Rectangle

# ---------- ספים (לכוונון) ----------
# peak_lookback - כמה נרות אחורה (מהשפל) מותר לחפש את השיא שממנו התחילה הירידה
# min_decline   - מינימום נרות בין השיא לשפל (מסנן "ירידה" של גאפ אחד)
# near_low      - הבסיס חייב להיווצר עד X% מעל השפל האמיתי של הירידה
DAILY = dict(min_drop=0.05, lookback=40, base_min=3, base_max=10, vol_mult=1.5,
             peak_lookback=40, min_decline=5, near_low=0.03)   # יומי = פולבק קצר (עד ~2 חודשים)
WEEKLY = dict(min_drop=0.10, lookback=26, base_min=2, base_max=6, vol_mult=1.3,
              peak_lookback=52, min_decline=3, near_low=0.05)
SLOW_SPLIT = 0.75   # שלב ההאטה מתחיל אחרי שהמחיר השלים 75% מהירידה (בסגירה)

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


def event_days(index):
    """ימי ווליום מכני: יום שישי השלישי של מרץ/יוני/ספטמבר/דצמבר (פקיעת אופציות ואיזון מדדים)
    ויום שישי האחרון של יוני (איזון Russell). חג -> יום המסחר שלפניו. מחזיר מערך bool לפי index."""
    idx = pd.DatetimeIndex(index)
    days = []
    for y in range(idx.year.min(), idx.year.max() + 1):
        for m in (3, 6, 9, 12):
            fridays = pd.date_range(f"{y}-{m:02d}-01", periods=31, freq="D")
            fridays = fridays[(fridays.month == m) & (fridays.weekday == 4)]
            days.append(fridays[2])
            if m == 6:
                days.append(fridays[-1])
    # רק תאריכים בתוך טווח הנתונים: תאריך עתידי לא יסמן את היום האחרון (בלי הצצה לעתיד)
    days = pd.DatetimeIndex([d for d in days if idx[0] <= d <= idx[-1]])
    pos = idx.searchsorted(days, side="right") - 1        # חג -> יום המסחר האחרון שלפניו
    mask = np.zeros(len(idx), bool)
    mask[pos] = True
    return mask


def clean_event_volume(df):
    """בימי ווליום מכני - הווליום נחתך לחציון 20 הימים שלפניו (רק נתוני עבר), כדי שקפיצה של קרנות
    מדדים לא תיחשב "פריצה בווליום" ולא תנפח את הווליום השבועי."""
    ev = event_days(df.index)
    if not ev.any():
        return df
    med = df["Volume"].rolling(20, min_periods=5).median().shift(1)
    vol = df["Volume"].where(~ev, np.minimum(df["Volume"], med.fillna(df["Volume"])))
    return df.assign(Volume=vol)


def to_weekly(df):
    return df.resample("W-FRI").agg({"Open": "first", "High": "max", "Low": "min",
                                     "Close": "last", "Volume": "sum"}).dropna()


def detect(df, p):
    """מחזיר dict עם גבולות ארבעת השלבים, או None אם אין דפוס בסוף הגרף."""
    if len(df) < p["lookback"] + 30:
        return None
    d = df.iloc[-(p["peak_lookback"] + p["lookback"] + p["base_max"] + 2):]
    o, h, l, c, v = (d[k].values for k in ("Open", "High", "Low", "Close", "Volume"))
    body = np.abs(c - o)
    vol_avg = df["Volume"].rolling(20).mean().iloc[-1]

    # מסנן מגמה: מחיר מעל SMA200 (או SMA40 בשבועי)
    sma_len = 200 if len(df) > 260 else 40
    sma = df["Close"].rolling(sma_len).mean().iloc[-1]
    uptrend = bool(np.isnan(sma) or df["Close"].iloc[-1] > sma)

    # שלב 4: נר אחרון ירוק עם ווליום חזק (הסגירה מעל הבסיס נבדקת לכל אורך בסיס)
    last = len(d) - 1
    if not (c[last] > o[last] and v[last] > p["vol_mult"] * vol_avg):
        return None

    # נקודת התחלה: השפל הנמוך ביותר ב-lookback הנרות שלפני הפריצה (כולל הבסיס)
    w0 = max(0, last - p["lookback"])
    tr0 = w0 + int(np.argmin(l[w0:last]))
    # השיא: הגבוה ביותר מאז הפעם האחרונה שהמחיר היה מתחת לשפל הזה (עד peak_lookback נרות אחורה),
    # כולל ראלי שאחרי השפל - כך הירידה הנמדדת היא תמיד הגל האחרון לפני הבסיס
    p0 = max(0, tr0 - p["peak_lookback"])
    below = np.where(l[p0:tr0] < l[tr0])[0]
    s0 = p0 + int(below[-1]) + 1 if len(below) else p0
    if s0 >= tr0:
        return None
    pk = s0 + int(np.argmax(h[s0:last]))
    if pk + 1 >= last:
        return None
    # השפל האמיתי של הגל: הנמוך ביותר אחרי השיא
    tr = pk + 1 + int(np.argmin(l[pk + 1:last]))
    trough = l[tr]
    drop = (h[pk] - trough) / h[pk]
    if drop < p["min_drop"] or tr - pk < p["min_decline"]:
        return None

    best = None
    for blen in range(p["base_min"], p["base_max"] + 1):
        b_start = last - blen
        if b_start <= pk + 1:
            break
        base_hi, base_lo = h[b_start:last].max(), l[b_start:last].min()
        breakout = c[last] > base_hi * 0.998
        tight = (base_hi - base_lo) / base_lo < 0.05
        # בבסיס אסור שפל חדש משמעותי אחרי 2 הנרות הראשונים
        bl = l[b_start:last]
        no_new_low = blen <= 2 or bl[2:].min() >= bl[:2].min() * 0.985
        # הבסיס חייב לשבת קרוב לשפל האמיתי, לא דגל אחרי ריבאונד
        near_low = base_lo <= trough * (1 + p["near_low"])
        if not (breakout and tight and no_new_low and near_low):
            continue
        # שלב 2: ההאטה מתחילה כשהמחיר השלים SLOW_SPLIT מהירידה, ונמשכת עד הבסיס
        dec_end = min(tr, b_start - 1)
        level = h[pk] - SLOW_SPLIT * (h[pk] - trough)
        hit = np.where(c[pk + 1:dec_end + 1] <= level)[0]
        slow = min(pk + 1 + (int(hit[0]) + 1 if len(hit) else dec_end - pk), b_start)
        n_early, n_late = slow - 1 - pk, b_start - slow
        early_speed = (c[pk] - c[slow - 1]) / max(n_early, 1)       # ירידה לנר
        late_speed = (c[slow - 1] - c[b_start - 1]) / n_late if n_late else np.inf
        early_body = body[pk + 1:slow].mean()
        late_body = body[slow:b_start].mean() if n_late else np.inf
        slowing = bool(n_late >= 2 and late_speed < 0.5 * early_speed
                       and late_body < early_body)
        early_vol = v[pk + 1:slow].mean()
        drying = bool(v[b_start:last].mean() < early_vol * 0.8)
        score = 25 * slowing + 25 * drying + 25 * tight + 25 * uptrend
        best = dict(peak=pk, slow=slow, base=b_start, rise=last, trough=tr,
                    drop=drop, base_hi=base_hi, base_lo=base_lo,
                    slowing=slowing, drying=drying, uptrend=uptrend,
                    score=score, offset=len(df) - len(d))
        # ממשיכים - הבסיס הארוך ביותר שעדיין עומד בתנאים מנצח
    return best


def plot(df, res, title, path, bars=80, marks=()):
    """marks: רשימת (תאריך, טקסט, צבע) - קו אנכי על הנר של התאריך (או הראשון אחריו)."""
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
        lab = matplotlib.transforms.blended_transform_factory(ax.transData, ax.transAxes)
        for n, (k, a, b) in enumerate(spans):
            a, b = a + g, b + g
            for axx in (ax, axv):
                axx.axvspan(a - 0.5, b - 0.5, color=PHASE_COLORS[k], alpha=0.45, lw=0)
            if k != "rise" and b > a:
                ax.text((a + b - 1) / 2, 0.97 - 0.05 * (n % 2), PHASE_NAMES[k],
                        transform=lab, ha="center", va="top", fontsize=9)
        if "trough" in res:
            ax.plot(res["trough"] + g, d["Low"].iloc[res["trough"] + g] if 0 <= res["trough"] + g < len(d)
                    else res["base_lo"], marker="^", color="#A32D2D", ms=7, ls="")
        ax.axhline(res["base_hi"], color="#185FA5", ls="--", lw=1, label="Entry (base high)")
        ax.axhline(res["base_lo"], color="#A32D2D", ls="--", lw=1, label="Stop (base low)")
        ax.annotate("BUY", (res["rise"] + g, d["Low"].iloc[res["rise"] + g]),
                    xytext=(0, -30), textcoords="offset points", ha="center",
                    arrowprops=dict(arrowstyle="->", color="#3B6D11"), color="#3B6D11")
        title += f"  |  score {res['score']}/100  drop {res['drop']:.1%}"
    for when, text, col in marks:
        pos = np.where(d.index >= pd.Timestamp(when))[0]
        if len(pos):
            for axx in (ax, axv):
                axx.axvline(pos[0], color=col, ls=":", lw=1.8)
            ax.text(pos[0], 0.03, f" {text}", transform=matplotlib.transforms.blended_transform_factory(
                ax.transData, ax.transAxes), color=col, fontsize=9, fontweight="bold", va="bottom")
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
    df = clean_event_volume(load(ticker) if df is None else df)
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
