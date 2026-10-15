# Resistance breakouts - 599 stocks, 2016-01-01 -> today - only the zone holding the all-time (since 2010) high

* exit: 2.0R target, max 10 days; initial stop = zone top - 1.0xATR
* 3,012 breakouts (0.5 per stock per year), 2,990 closed trades on 1,395 distinct dates

| | trades | win | avg R | vs random days | vs random uptrend days |
|---|---|---|---|---|---|
| all breakouts | 2,990 | 44% | +0.012 | -0.027 | +0.011 |
| random days (CONTROL) | 711,535 | 43% | +0.039 | | |
| random uptrend days | 303,981 | 42% | +0.001 | | |

Breakouts, date-clustered 95% CI of avg R: [-0.042, +0.066]

## Breakdowns (exploratory)

| group | trades | win | avg R | vs random days | vs random uptrend days |
|---|---|---|---|---|---|
| touches = 2 | 1,720 | 43% | +0.004 | -0.035 | +0.003 |
| touches = 3 | 753 | 44% | +0.045 | +0.007 | +0.045 |
| touches >= 4 | 517 | 45% | -0.012 | -0.051 | -0.013 |
| room to next resistance < 1 ATR | 397 | 43% | +0.022 | -0.016 | +0.021 |
| room 1-3 ATR | 0 | | | | |
| room > 3 ATR | 0 | | | | |
| no resistance above (new 1y high zone) | 2,593 | 44% | +0.010 | -0.029 | +0.009 |
| breakout volume < 1x avg | 845 | 42% | -0.004 | -0.043 | -0.005 |
| breakout volume 1-1.5x | 976 | 44% | +0.017 | -0.021 | +0.017 |
| breakout volume > 1.5x | 1,169 | 45% | +0.018 | -0.020 | +0.018 |
| in uptrend (>SMA50 & >SMA200) | 2,990 | 44% | +0.012 | -0.027 | +0.011 |
| not in uptrend | 0 | | | | |
