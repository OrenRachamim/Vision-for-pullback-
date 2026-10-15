# Resistance breakouts - 903 stocks, 2016-01-01 -> today - only the zone holding the 52-week high

* exit: trailing stop 3.0xATR, max 60 days; initial stop = zone top - 1.0xATR
* 12,291 breakouts (1.3 per stock per year), 12,200 closed trades on 2,263 distinct dates

| | trades | win | avg R | vs random days | vs random uptrend days |
|---|---|---|---|---|---|
| all breakouts | 12,200 | 34% | +0.105 | -0.069 | +0.006 |
| random days (CONTROL) | 1,140,516 | 32% | +0.173 | | |
| random uptrend days | 557,190 | 33% | +0.099 | | |

Breakouts, date-clustered 95% CI of avg R: [+0.056, +0.151]

## Breakdowns (exploratory)

| group | trades | win | avg R | vs random days | vs random uptrend days |
|---|---|---|---|---|---|
| touches = 2 | 6,776 | 33% | +0.089 | -0.084 | -0.010 |
| touches = 3 | 3,175 | 35% | +0.121 | -0.052 | +0.022 |
| touches >= 4 | 2,249 | 34% | +0.126 | -0.047 | +0.027 |
| room to next resistance < 1 ATR | 1,887 | 35% | +0.256 | +0.083 | +0.157 |
| room 1-3 ATR | 0 | | | | |
| room > 3 ATR | 0 | | | | |
| no resistance above (new 1y high zone) | 10,313 | 33% | +0.077 | -0.096 | -0.022 |
| breakout volume < 1x avg | 3,696 | 31% | +0.081 | -0.093 | -0.018 |
| breakout volume 1-1.5x | 4,371 | 32% | +0.087 | -0.087 | -0.012 |
| breakout volume > 1.5x | 4,133 | 37% | +0.145 | -0.029 | +0.046 |
| in uptrend (>SMA50 & >SMA200) | 12,200 | 34% | +0.105 | -0.069 | +0.006 |
| not in uptrend | 0 | | | | |
