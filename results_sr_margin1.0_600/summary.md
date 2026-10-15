# Resistance breakouts - 599 stocks, 2016-01-01 -> today - breakout = close > zone top + 1.0xATR - only the zone holding the all-time (since 2010) high

* exit: trailing stop 3.0xATR, max 60 days; initial stop = zone top - 1.0xATR
* 1,220 breakouts (0.2 per stock per year), 1,218 closed trades on 782 distinct dates

| | trades | win | avg R | vs random days | vs random uptrend days |
|---|---|---|---|---|---|
| all breakouts | 1,218 | 36% | +0.022 | -0.050 | +0.001 |
| random days (CONTROL) | 709,503 | 34% | +0.072 | | |
| random uptrend days | 303,411 | 33% | +0.021 | | |

Breakouts, date-clustered 95% CI of avg R: [-0.069, +0.117]

## Breakdowns (exploratory)

| group | trades | win | avg R | vs random days | vs random uptrend days |
|---|---|---|---|---|---|
| touches = 2 | 634 | 35% | -0.023 | -0.095 | -0.044 |
| touches = 3 | 357 | 36% | +0.019 | -0.052 | -0.002 |
| touches >= 4 | 227 | 38% | +0.152 | +0.080 | +0.131 |
| room to next resistance < 1 ATR | 0 | | | | |
| room 1-3 ATR | 0 | | | | |
| room > 3 ATR | 0 | | | | |
| no resistance above (new 1y high zone) | 1,218 | 36% | +0.022 | -0.050 | +0.001 |
| breakout volume < 1x avg | 234 | 38% | +0.062 | -0.010 | +0.041 |
| breakout volume 1-1.5x | 320 | 34% | -0.061 | -0.133 | -0.082 |
| breakout volume > 1.5x | 664 | 36% | +0.048 | -0.024 | +0.027 |
| in uptrend (>SMA50 & >SMA200) | 1,218 | 36% | +0.022 | -0.050 | +0.001 |
| not in uptrend | 0 | | | | |
