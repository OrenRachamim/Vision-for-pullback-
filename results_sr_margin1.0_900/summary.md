# Resistance breakouts - 903 stocks, 2016-01-01 -> today - breakout = close > zone top + 1.0xATR - only the zone holding the all-time (since 2010) high

* exit: trailing stop 3.0xATR, max 60 days; initial stop = zone top - 1.0xATR
* 3,487 breakouts (0.4 per stock per year), 3,477 closed trades on 1,460 distinct dates

| | trades | win | avg R | vs random days | vs random uptrend days |
|---|---|---|---|---|---|
| all breakouts | 3,477 | 40% | +0.096 | -0.054 | +0.008 |
| random days (CONTROL) | 1,139,365 | 37% | +0.150 | | |
| random uptrend days | 556,961 | 37% | +0.087 | | |

Breakouts, date-clustered 95% CI of avg R: [+0.045, +0.148]

## Breakdowns (exploratory)

| group | trades | win | avg R | vs random days | vs random uptrend days |
|---|---|---|---|---|---|
| touches = 2 | 1,901 | 39% | +0.088 | -0.062 | +0.001 |
| touches = 3 | 942 | 40% | +0.110 | -0.041 | +0.022 |
| touches >= 4 | 634 | 41% | +0.098 | -0.052 | +0.011 |
| room to next resistance < 1 ATR | 0 | | | | |
| room 1-3 ATR | 0 | | | | |
| room > 3 ATR | 0 | | | | |
| no resistance above (new 1y high zone) | 3,477 | 40% | +0.096 | -0.054 | +0.008 |
| breakout volume < 1x avg | 741 | 39% | +0.094 | -0.056 | +0.007 |
| breakout volume 1-1.5x | 1,142 | 37% | +0.069 | -0.081 | -0.018 |
| breakout volume > 1.5x | 1,594 | 42% | +0.116 | -0.035 | +0.028 |
| in uptrend (>SMA50 & >SMA200) | 3,477 | 40% | +0.096 | -0.054 | +0.008 |
| not in uptrend | 0 | | | | |
