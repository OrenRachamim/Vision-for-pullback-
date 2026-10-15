# Resistance breakouts - 599 stocks, 2016-01-01 -> today - only the zone holding the all-time (since 2010) high

* exit: trailing stop 3.0xATR, max 60 days; initial stop = zone top - 1.0xATR
* 3,012 breakouts (0.5 per stock per year), 2,988 closed trades on 1,394 distinct dates

| | trades | win | avg R | vs random days | vs random uptrend days |
|---|---|---|---|---|---|
| all breakouts | 2,988 | 31% | -0.007 | -0.077 | -0.013 |
| random days (CONTROL) | 710,038 | 30% | +0.070 | | |
| random uptrend days | 303,518 | 30% | +0.006 | | |

Breakouts, date-clustered 95% CI of avg R: [-0.089, +0.077]

## Breakdowns (exploratory)

| group | trades | win | avg R | vs random days | vs random uptrend days |
|---|---|---|---|---|---|
| touches = 2 | 1,719 | 30% | -0.020 | -0.089 | -0.026 |
| touches = 3 | 753 | 31% | -0.017 | -0.087 | -0.023 |
| touches >= 4 | 516 | 32% | +0.048 | -0.022 | +0.042 |
| room to next resistance < 1 ATR | 397 | 27% | +0.021 | -0.049 | +0.015 |
| room 1-3 ATR | 0 | | | | |
| room > 3 ATR | 0 | | | | |
| no resistance above (new 1y high zone) | 2,591 | 31% | -0.012 | -0.081 | -0.018 |
| breakout volume < 1x avg | 845 | 27% | -0.111 | -0.181 | -0.117 |
| breakout volume 1-1.5x | 975 | 30% | +0.035 | -0.035 | +0.029 |
| breakout volume > 1.5x | 1,168 | 34% | +0.033 | -0.037 | +0.027 |
| in uptrend (>SMA50 & >SMA200) | 2,988 | 31% | -0.007 | -0.077 | -0.013 |
| not in uptrend | 0 | | | | |
