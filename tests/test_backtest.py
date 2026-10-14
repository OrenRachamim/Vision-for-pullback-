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


def test_combo_weekly_arms_then_daily_triggers():
    df = _bars([(100, 101, 99, 100)] * 60)
    W = dict(base_lo=95.0, score=50)
    D = dict(base_lo=98.0, score=50)
    h = lambda t, d=None, w=None: dict(t=t, t0=0, daily=d, weekly=w)

    # daily before weekly does not count; daily inside the window does
    out = bt.combo_signals(df, [h(5, d=D), h(10, w=W), h(14, d=D)], arm_days=15)
    assert [(c["t"], c["weekly_hit"]["t"]) for c in out] == [(14, 10)]
    # same day counts
    assert [c["t"] for c in bt.combo_signals(df, [h(10, d=D, w=W)], 15)] == [10]
    # daily after the window does not count
    assert bt.combo_signals(df, [h(10, w=W), h(26, d=D)], 15) == []
    # close below the weekly base_lo cancels the arming
    low = df.copy()
    low.iloc[12, low.columns.get_loc("Close")] = 90
    assert bt.combo_signals(low, [h(10, w=W), h(14, d=D)], 15) == []
    # one buy per weekly setup: repeated weekly days right after a buy do not re-arm
    out = bt.combo_signals(df, [h(10, w=W), h(11, d=D, w=W), h(13, d=D, w=W)], 15)
    assert [c["t"] for c in out] == [11]


def test_combo_require_uptrend_waits_for_uptrend_daily():
    df = _bars([(100, 101, 99, 100)] * 60)
    W = dict(base_lo=95.0, score=50)
    down, up = dict(base_lo=98.0, score=50, uptrend=False), dict(base_lo=98.0, score=50, uptrend=True)
    h = lambda t, d=None, w=None: dict(t=t, t0=0, daily=d, weekly=w)
    hits = [h(10, w=W), h(12, d=down), h(16, d=up)]
    assert [c["t"] for c in bt.combo_signals(df, hits, 15)] == [12]
    assert [c["t"] for c in bt.combo_signals(df, hits, 15, require_uptrend=True)] == [16]


def test_event_days_and_volume_cap():
    idx = pd.bdate_range("2024-06-03", "2024-07-05")
    ev = ps.event_days(idx)
    assert list(idx[ev].date.astype(str)) == ["2024-06-21", "2024-06-28"]
    # Good Friday 2024-03-29 is not the third Friday; 2022-06-17 third Friday is a trading day
    idx2 = pd.bdate_range("2025-03-01", "2025-03-31")
    assert list(idx2[ps.event_days(idx2)].date.astype(str)) == ["2025-03-21"]
    df = pd.DataFrame(dict(Open=1.0, High=1.0, Low=1.0, Close=1.0, Volume=100.0), index=idx)
    df.loc["2024-06-21", "Volume"] = 1000.0
    out = ps.clean_event_volume(df)
    assert out.loc["2024-06-21", "Volume"] == 100.0          # spike capped at past median
    assert out.loc["2024-06-20", "Volume"] == 100.0          # normal days untouched
    assert df.loc["2024-06-21", "Volume"] == 1000.0          # input not modified


def test_trailing_stop():
    atr = np.full(10, 2.0)
    # entry 100 (bar 1), initial stop 95 -> risk 5; k=2, ATR=2 -> trail = highest high - 4
    up = _bars([(99, 100, 98, 99), (100, 110, 99, 109), (109, 120, 112, 119), (118, 119, 110, 111)])
    r = bt.simulate_trade(up, 0, 95, max_hold=10, trail_atr=2, atr=atr)
    assert r["exit_reason"] == "trail" and r["exit"] == 116 and abs(r["R"] - 3.2) < 1e-12
    # gap open below the trailing stop -> exit at the open
    gap = _bars([(99, 100, 98, 99), (100, 110, 99, 109), (109, 120, 112, 119), (112, 113, 108, 110)])
    r = bt.simulate_trade(gap, 0, 95, max_hold=10, trail_atr=2, atr=atr)
    assert r["exit_reason"] == "trail_gap" and r["exit"] == 112
    # entry bar uses only the initial stop; no fixed target even after a big run
    run = _bars([(99, 100, 98, 99), (100, 150, 96, 149), (149, 160, 147, 159)])
    r = bt.simulate_trade(run, 0, 95, max_hold=2, trail_atr=2, atr=atr)
    assert r["exit_reason"] == "time" and r["exit"] == 159
    # trailing stop never falls below the initial stop
    flat = _bars([(99, 100, 98, 99), (100, 101, 96, 100), (100, 101, 94, 95)])
    r = bt.simulate_trade(flat, 0, 95, max_hold=10, trail_atr=3, atr=np.full(10, 5.0))
    assert r["exit_reason"] == "stop" and r["R"] == -1
