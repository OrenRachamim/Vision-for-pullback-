"""
mtf_data.py - הורדת נתונים לאסטרטגיה רב-שכבתית (יומי / שעתי / 5 דקות) מ-yfinance.

  יומי   : data/<T>.csv            (מ-2010, רענון מלא)
  שעתי   : data_1h/<T>.pkl         (730 יום אחורה - המקסימום ב-yfinance)
  5 דקות : data_5m/<T>.pkl         (60 יום אחורה - המקסימום ב-yfinance)
זמנים ב-America/New_York. הנרות של היום הנוכחי (שוק פתוח / חלקי) לא נשמרים.

הרצה:  python mtf_data.py --universe universes/sp500.txt universes/sp400.txt universes/sp600.txt --what daily 1h 5m
"""
import argparse
import os
import time

import pandas as pd

import backtest as bt

DIRS = {"1h": "data_1h", "5m": "data_5m"}
SPEC = {"1h": dict(period="730d", interval="60m"), "5m": dict(period="60d", interval="5m")}


def _today():
    return pd.Timestamp.now(tz="America/New_York").normalize()


def _split(df, tickers):
    """yf.download של כמה מניות -> dict ticker -> DataFrame OHLCV."""
    out = {}
    if df is None or df.empty:
        return out
    if not isinstance(df.columns, pd.MultiIndex):
        return {tickers[0]: df}
    lvl = 1 if set(tickers) & set(df.columns.get_level_values(1)) else 0
    for tk in tickers:
        try:
            g = df.xs(tk, axis=1, level=lvl)
        except KeyError:
            continue
        out[tk] = g
    return out


def download(tickers, what, batch=50, pause=2.0):
    import yfinance as yf
    os.makedirs(DIRS.get(what, "data"), exist_ok=True)
    today = _today()
    done = 0
    for i in range(0, len(tickers), batch):
        chunk = tickers[i:i + batch]
        for attempt in range(4):
            try:
                if what == "daily":
                    raw = yf.download(chunk, start=bt.DATA_START, interval="1d", progress=False,
                                      auto_adjust=True, group_by="ticker", threads=True)
                else:
                    raw = yf.download(chunk, progress=False, auto_adjust=True, group_by="ticker", threads=True,
                                      prepost=False, **SPEC[what])
                break
            except Exception as e:  # noqa: BLE001
                print("retry", attempt, e)
                time.sleep(5 * 2 ** attempt)
        else:
            continue
        for tk, g in _split(raw, chunk).items():
            g = g[["Open", "High", "Low", "Close", "Volume"]].dropna()
            if g.empty:
                continue
            if what == "daily":
                g = g[g.index < today.tz_localize(None)]
                g.index.name = "Date"
                g.to_csv(os.path.join("data", f"{tk}.csv"))
            else:
                g.index = g.index.tz_convert("America/New_York")
                g = g[g.index < today]
                g.to_pickle(os.path.join(DIRS[what], f"{tk}.pkl"))
            done += 1
        print(what, f"{min(i + batch, len(tickers))}/{len(tickers)} saved {done}", flush=True)
        time.sleep(pause)
    return done


def load(tk, what):
    if what == "daily":
        return bt.load_history(tk)
    return pd.read_pickle(os.path.join(DIRS[what], f"{tk}.pkl"))


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--universe", nargs="+", required=True)
    ap.add_argument("--what", nargs="+", default=["daily", "1h", "5m"], choices=["daily", "1h", "5m"])
    args = ap.parse_args(argv)
    tickers = list(dict.fromkeys(ln.strip().upper() for p in args.universe for ln in open(p) if ln.strip()))
    tickers = [t.replace(".", "-") for t in tickers]
    for w in args.what:
        n = download(tickers, w)
        print(f"{w}: {n}/{len(tickers)} tickers saved")


if __name__ == "__main__":
    main()
