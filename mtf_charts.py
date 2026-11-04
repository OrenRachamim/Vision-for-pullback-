"""
mtf_charts.py - גרפים לדוגמה לאסטרטגיה הרב-שכבתית: לכל עסקה שלוש רמות זו מתחת לזו.
  יומי (~9 חודשים, SMA 10..200, יום האיתות) | שעתי (~8 ימים, SMA 10/20/50/100) |
  5 דקות (יום העסקה + RSI + MACD, נקודת הכניסה, הסטופ והיציאה בסוף היום).
הרצה:  python mtf_charts.py results_mtf --n 8 --out mtf_charts
"""
import argparse
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

import mtf_data as md  # noqa: E402
import mtf_strategy as ms  # noqa: E402

COL = {10: "#E24B4A", 20: "#EF9F27", 50: "#639922", 100: "#378ADD", 150: "#7F77DD", 200: "#444441"}


def candles(ax, d, x=None):
    x = np.arange(len(d)) if x is None else x
    for i, (o, h, l, c) in zip(x, d[["Open", "High", "Low", "Close"]].values):
        col = "#3B6D11" if c >= o else "#A32D2D"
        ax.vlines(i, l, h, color=col, lw=0.8)
        ax.add_patch(plt.Rectangle((i - 0.3, min(o, c)), 0.6, max(abs(c - o), 1e-9), color=col))


def ticks(ax, idx, n, fmt):
    step = max(1, len(idx) // n)
    ax.set_xticks(range(0, len(idx), step))
    ax.set_xticklabels([z.strftime(fmt) for z in idx[::step]], fontsize=7)


def chart(r, path, hold=1, h_spread=ms.P["H_SPREAD"]):
    d, h, m = md.load(r.ticker, "daily"), md.load(r.ticker, "1h"), md.load(r.ticker, "5m")
    t = pd.Timestamp(r.time)
    sig = pd.Timestamp(r.dsig_date)
    fig = plt.figure(figsize=(14, 12))
    gs = fig.add_gridspec(5, 1, height_ratios=[3, 3, 3, 1, 1], hspace=0.35)
    # יומי
    ax = fig.add_subplot(gs[0])
    i_sig = d.index.get_loc(sig)
    dd = d.iloc[max(0, i_sig - 180):i_sig + 8]
    candles(ax, dd)
    for n in ms.D_MAS:
        ax.plot(np.arange(len(dd)), d["Close"].rolling(n).mean().loc[dd.index], color=COL[n], lw=0.9, label=f"SMA{n}")
    ks = dd.index.get_loc(sig)
    k0 = ks - (hold - 1)                                     # יום הפריצה (עם המתנה - hold-1 ימים לפני האיתות)
    ax.axvspan(k0 - 0.5, k0 + 0.5, color="#3B6D11", alpha=0.2)
    if hold > 1:
        ax.axvspan(k0 + 0.5, ks + 0.5, color="#185FA5", alpha=0.12)
    sp = ms.daily_signals(d)["spread"].iloc[max(0, i_sig - (hold - 1) - 9):i_sig - (hold - 1) + 1].min()
    ax.set_title(f"DAILY - {r.ticker}: MAs 10..200 converge (spread {sp:.1%}) and close above all of them "
                 f"for the first time on {dd.index[k0].date()}"
                 + (f"; stays above for {hold} days -> signal {sig.date()} (blue)" if hold > 1 else ""),
                 fontsize=9, loc="left")
    ax.legend(fontsize=6, ncol=6, loc="upper left")
    ticks(ax, dd.index, 10, "%Y-%m-%d")
    # שעתי
    ax = fig.add_subplot(gs[1])
    j = h.index.searchsorted(t)
    hh = h.iloc[max(0, j - 60):j + 6]
    candles(ax, hh)
    for n in ms.H_MAS:
        ax.plot(np.arange(len(hh)), h["Close"].rolling(n).mean().loc[hh.index], color=COL[n], lw=0.9, label=f"SMA{n} (1h)")
    ax.axvline(hh.index.searchsorted(t) - 0.5, color="#185FA5", ls="--", lw=1)
    ax.set_title(f"HOURLY: SMA 10/20/50/100 spread {r.h_spread:.1%} at the last closed hour before entry "
                 f"(filter <= {h_spread:.0%})", fontsize=9, loc="left")
    ax.legend(fontsize=6, ncol=4, loc="upper left")
    ticks(ax, hh.index, 10, "%m-%d %H:%M")
    # 5 דקות
    day = m[m.index.normalize() == t.normalize()]
    k = day.index.get_loc(t)
    ax = fig.add_subplot(gs[2])
    candles(ax, day)
    i_all = m.index.get_loc(t)
    stop = m["Low"].values[max(0, i_all - 1 - ms.P["STOP_BARS"] + 1):i_all].min()
    ax.plot(k, day["Open"].iloc[k], marker="^", ms=11, color="#185FA5", ls="")
    ax.hlines(stop, k, len(day) - 1, color="#A32D2D", ls="--", lw=1)
    ax.text(len(day) - 0.5, stop, f" stop {stop:.2f}", color="#A32D2D", fontsize=7, va="center")
    ax.plot(len(day) - 1, day["Close"].iloc[-1], marker="X", ms=10,
            color="#3B6D11" if r.eod_ret > 0 else "#A32D2D", ls="")
    ax.set_title(f"5-MIN {t.date()}: buy {t.strftime('%H:%M')} at {day['Open'].iloc[k]:.2f} -> close "
                 f"{day['Close'].iloc[-1]:.2f}  |  end-of-day {r.eod_ret:+.2%}, stop/2R {r['2R_ret']:+.2%} "
                 f"({r['2R_why']})", fontsize=9, loc="left", color="#3B6D11" if r.eod_ret > 0 else "#A32D2D")
    ticks(ax, day.index, 13, "%H:%M")
    c_all = m["Close"].values
    rs = pd.Series(ms.rsi(c_all), index=m.index).loc[day.index]
    mc, sg = ms.macd(c_all)
    mc, sg = pd.Series(mc, index=m.index).loc[day.index], pd.Series(sg, index=m.index).loc[day.index]
    ax = fig.add_subplot(gs[3])
    ax.plot(np.arange(len(day)), rs.values, color="#534AB7", lw=1)
    ax.axhline(ms.P["RSI_OS"], color="#A32D2D", ls=":", lw=1)
    ax.axvline(k - 0.5, color="#185FA5", ls="--", lw=1)
    ax.set_ylabel("RSI14", fontsize=8)
    ticks(ax, day.index, 13, "%H:%M")
    ax = fig.add_subplot(gs[4])
    ax.plot(np.arange(len(day)), mc.values, color="#185FA5", lw=1, label="MACD")
    ax.plot(np.arange(len(day)), sg.values, color="#EF9F27", lw=1, label="signal")
    ax.bar(np.arange(len(day)), (mc - sg).values, color=np.where(mc > sg, "#97C459", "#F09595"))
    ax.axvline(k - 0.5, color="#185FA5", ls="--", lw=1)
    ax.legend(fontsize=6, loc="upper left")
    ticks(ax, day.index, 13, "%H:%M")
    fig.savefig(path, dpi=90, bbox_inches="tight")
    plt.close(fig)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("res")
    ap.add_argument("--n", type=int, default=8)
    ap.add_argument("--out", default="mtf_charts")
    ap.add_argument("--seed", type=int, default=2)
    ap.add_argument("--d_hold", type=int, default=1, help="the D_HOLD the results were run with")
    ap.add_argument("--h_spread", type=float, default=ms.P["H_SPREAD"], help="the H_SPREAD the results were run with")
    ap.add_argument("--skip", nargs="*", default=[], help="folders of charts already drawn - pick other trades")
    args = ap.parse_args(argv)
    T = pd.read_csv(os.path.join(args.res, "trigger_trades.csv"))
    full = T[T.armed & T.h_conv & T.eod_ret.notna()]
    done = {f.split("_", 1)[1][:-4] for d in args.skip if os.path.isdir(d) for f in os.listdir(d) if f.endswith(".png")}
    full = full[~(full.ticker + "_" + full.time.astype(str).str[:10]).isin(done)]
    pick = full.sample(min(args.n, len(full)), random_state=args.seed).sort_values("time")
    os.makedirs(args.out, exist_ok=True)
    for i, (_, r) in enumerate(pick.iterrows(), 1):
        p = os.path.join(args.out, f"{i:02d}_{r.ticker}_{str(r.time)[:10]}.png")
        chart(r, p, args.d_hold, args.h_spread)
        print(p, f"{r.eod_ret:+.2%}")


if __name__ == "__main__":
    main()
