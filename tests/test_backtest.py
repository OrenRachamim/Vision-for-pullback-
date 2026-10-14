"""
בדיקות אמינות למנוע עצמו (לא לאסטרטגיה):
  1. הסינון המוקדם לא משנה אף איתות לעומת הרצה מלאה.
  2. אין הצצה לעתיד: איתות ביום t זהה בין אם יש נתונים אחרי t ובין אם לא.
  3. סימולציית העסקה מחשבת סטופ / יעד / יציאה בזמן נכון.
הרצה:  python -m pytest -q tests        (או: python tests/test_backtest.py)
"""
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import backtest as bt          # noqa: E402
import pullback_scanner as ps  # noqa: E402


def random_market(seed, n=900):
    """נתונים סינתטיים עם הרבה ירידות/בסיסים/קפיצות ווליום, כדי לייצר איתותים."""
    rng = np.random.default_rng(seed)
    regime = np.repeat(rng.choice([0.004, -0.012, 0.0, 0.002], n // 6 + 1), 6)[:n]
    c = 50 * np.cumprod(1 + regime + rng.normal(0, 0.008, n))
    o = np.r_[c[0], c[:-1]] * (1 + rng.normal(0, 0.003, n))
    hi = np.maximum(o, c) * (1 + np.abs(rng.normal(0, 0.004, n)))
    lo = np.minimum(o, c) * (1 - np.abs(rng.normal(0, 0.004, n)))
    v = rng.lognormal(0, 0.45, n) * 1e6
    idx = pd.bdate_range("2019-01-01", periods=n)
    return pd.DataFrame(dict(Open=o, High=hi, Low=lo, Close=c, Volume=v), index=idx)


def _key(hits):
    return [(h["t"], h["daily"] is not None, h["weekly"] is not None,
             h["daily"] and h["daily"]["score"], h["weekly"] and h["weekly"]["score"])
            for h in hits]


def test_prefilter_is_exact():
    total = 0
    for seed in range(4):
        df = random_market(seed)
        fast = bt.scan_history(df, prefilter=True)
        slow = bt.scan_history(df, prefilter=False)
        assert _key(fast) == _key(slow)
        total += len(fast)
    assert total > 0, "synthetic data produced no signals - test is vacuous"


def test_no_lookahead():
    df = random_market(1)
    full = {h["t"]: h for h in bt.scan_history(df)}
    assert full
    for t, h in list(full.items())[:15]:
        cut = bt.scan_history(df.iloc[:t + 1], start=df.index[t])
        assert len(cut) == 1 and cut[0]["t"] == t
        for k in ("daily", "weekly"):
            assert (cut[0][k] is None) == (h[k] is None)
            if h[k]:
                assert cut[0][k]["base_lo"] == h[k]["base_lo"]


def _bars(rows):
    idx = pd.bdate_range("2024-01-01", periods=len(rows))
    return pd.DataFrame(rows, columns=["Open", "High", "Low", "Close"], index=idx).assign(Volume=1)


def test_trade_target_stop_time():
    # entry 100 at bar 1, stop 95 -> risk 5, 2R target = 110
    tgt = _bars([(99, 100, 98, 99), (100, 104, 99, 103), (103, 111, 102, 108), (108, 109, 107, 108)])
    r = bt.simulate_trade(tgt, 0, stop=95, target_r=2, max_hold=10)
    assert r["exit_reason"] == "target" and r["R"] == 2 and r["bars"] == 2

    stp = _bars([(99, 100, 98, 99), (100, 101, 96, 97), (97, 98, 94, 95)])
    r = bt.simulate_trade(stp, 0, stop=95, target_r=2, max_hold=10)
    assert r["exit_reason"] == "stop" and r["R"] == -1

    both = _bars([(99, 100, 98, 99), (100, 111, 94, 100)])           # same bar: stop wins
    assert bt.simulate_trade(both, 0, 95, 2, 10)["exit_reason"] == "stop"

    gap = _bars([(99, 100, 98, 99), (100, 101, 99, 100), (90, 91, 89, 90)])
    r = bt.simulate_trade(gap, 0, 95, 2, 10)
    assert r["exit_reason"] == "stop_gap" and r["R"] == -2

    tim = _bars([(99, 100, 98, 99)] + [(100, 101, 99, 100)] * 5 + [(100, 103, 99, 102)])
    r = bt.simulate_trade(tim, 0, 95, 2, max_hold=6)
    assert r["exit_reason"] == "time" and abs(r["R"] - 0.4) < 1e-12

    below = _bars([(99, 100, 98, 99), (94, 95, 93, 94)])
    assert bt.simulate_trade(below, 0, 95, 2, 10)["exit_reason"] == "gap_below_stop"


def test_scanner_window_matches_live_load():
    """בכל יום הסורק מקבל ~2 שנות נתונים, כמו load(period='2y'), ולכן SMA200 ביומי."""
    df = random_market(2)
    hits = bt.scan_history(df)
    for h in hits:
        n = h["t"] + 1 - h["t0"]
        assert 480 <= n <= 525 or h["t0"] == 0


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
