# Resistance breakouts - 599 stocks, 2016-01-01 -> today - only the zone holding the 52-week high

* exit: 2.0R target, max 10 days; initial stop = zone top - 1.0xATR
* 5,903 breakouts (0.9 per stock per year), 5,859 closed trades on 1,907 distinct dates

| | trades | win | avg R | vs random days | vs random uptrend days |
|---|---|---|---|---|---|
| all breakouts | 5,859 | 43% | +0.013 | -0.029 | +0.007 |
| random days (CONTROL) | 711,433 | 43% | +0.042 | | |
| random uptrend days | 303,954 | 43% | +0.006 | | |

Breakouts, date-clustered 95% CI of avg R: [-0.031, +0.057]

## Breakdowns (exploratory)

| group | trades | win | avg R | vs random days | vs random uptrend days |
|---|---|---|---|---|---|
| touches = 2 | 3,192 | 43% | +0.022 | -0.020 | +0.016 |
| touches = 3 | 1,436 | 43% | -0.010 | -0.052 | -0.016 |
| touches >= 4 | 1,231 | 44% | +0.014 | -0.028 | +0.008 |
| room to next resistance < 1 ATR | 889 | 41% | -0.011 | -0.053 | -0.017 |
| room 1-3 ATR | 0 | | | | |
| room > 3 ATR | 0 | | | | |
| no resistance above (new 1y high zone) | 4,970 | 43% | +0.017 | -0.025 | +0.011 |
| breakout volume < 1x avg | 1,549 | 40% | -0.025 | -0.067 | -0.031 |
| breakout volume 1-1.5x | 1,843 | 43% | +0.017 | -0.025 | +0.011 |
| breakout volume > 1.5x | 2,467 | 45% | +0.034 | -0.008 | +0.027 |
| in uptrend (>SMA50 & >SMA200) | 5,859 | 43% | +0.013 | -0.029 | +0.007 |
| not in uptrend | 0 | | | | |
