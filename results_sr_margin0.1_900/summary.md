# Resistance breakouts - 903 stocks, 2016-01-01 -> today - breakout = close > zone top + 0.1xATR - only the zone holding the all-time (since 2010) high

* exit: trailing stop 3.0xATR, max 60 days; initial stop = zone top - 1.0xATR
* 9,184 breakouts (0.9 per stock per year), 9,120 closed trades on 2,134 distinct dates

| | trades | win | avg R | vs random days | vs random uptrend days |
|---|---|---|---|---|---|
| all breakouts | 9,120 | 33% | +0.103 | -0.068 | +0.007 |
| random days (CONTROL) | 1,140,509 | 32% | +0.170 | | |
| random uptrend days | 557,192 | 33% | +0.096 | | |

Breakouts, date-clustered 95% CI of avg R: [+0.049, +0.156]

## Breakdowns (exploratory)

| group | trades | win | avg R | vs random days | vs random uptrend days |
|---|---|---|---|---|---|
| touches = 2 | 5,265 | 33% | +0.099 | -0.071 | +0.003 |
| touches = 3 | 2,326 | 34% | +0.090 | -0.080 | -0.006 |
| touches >= 4 | 1,529 | 35% | +0.134 | -0.036 | +0.039 |
| room to next resistance < 1 ATR | 1,277 | 36% | +0.239 | +0.069 | +0.144 |
| room 1-3 ATR | 0 | | | | |
| room > 3 ATR | 0 | | | | |
| no resistance above (new 1y high zone) | 7,843 | 33% | +0.080 | -0.090 | -0.015 |
| breakout volume < 1x avg | 3,085 | 32% | +0.091 | -0.079 | -0.005 |
| breakout volume 1-1.5x | 3,335 | 32% | +0.091 | -0.079 | -0.004 |
| breakout volume > 1.5x | 2,700 | 36% | +0.130 | -0.040 | +0.034 |
| in uptrend (>SMA50 & >SMA200) | 9,120 | 33% | +0.103 | -0.068 | +0.007 |
| not in uptrend | 0 | | | | |
