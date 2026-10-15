# Resistance breakouts - 599 stocks, 2016-01-01 -> today - breakout = close > zone top + 0.5xATR - only the zone holding the all-time (since 2010) high

* exit: trailing stop 3.0xATR, max 60 days; initial stop = zone top - 1.0xATR
* 2,363 breakouts (0.4 per stock per year), 2,349 closed trades on 1,229 distinct dates

| | trades | win | avg R | vs random days | vs random uptrend days |
|---|---|---|---|---|---|
| all breakouts | 2,349 | 33% | +0.006 | -0.065 | -0.009 |
| random days (CONTROL) | 709,686 | 32% | +0.070 | | |
| random uptrend days | 303,441 | 32% | +0.014 | | |

Breakouts, date-clustered 95% CI of avg R: [-0.068, +0.085]

## Breakdowns (exploratory)

| group | trades | win | avg R | vs random days | vs random uptrend days |
|---|---|---|---|---|---|
| touches = 2 | 1,315 | 32% | -0.032 | -0.103 | -0.046 |
| touches = 3 | 616 | 33% | -0.023 | -0.093 | -0.037 |
| touches >= 4 | 418 | 37% | +0.166 | +0.096 | +0.152 |
| room to next resistance < 1 ATR | 113 | 20% | -0.308 | -0.378 | -0.322 |
| room 1-3 ATR | 0 | | | | |
| room > 3 ATR | 0 | | | | |
| no resistance above (new 1y high zone) | 2,236 | 34% | +0.021 | -0.049 | +0.007 |
| breakout volume < 1x avg | 620 | 32% | -0.008 | -0.079 | -0.022 |
| breakout volume 1-1.5x | 722 | 31% | -0.015 | -0.085 | -0.029 |
| breakout volume > 1.5x | 1,007 | 36% | +0.029 | -0.042 | +0.014 |
| in uptrend (>SMA50 & >SMA200) | 2,349 | 33% | +0.006 | -0.065 | -0.009 |
| not in uptrend | 0 | | | | |
