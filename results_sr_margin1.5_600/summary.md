# Resistance breakouts - 599 stocks, 2016-01-01 -> today - breakout = close > zone top + 1.5xATR - only the zone holding the all-time (since 2010) high

* exit: trailing stop 3.0xATR, max 60 days; initial stop = zone top - 1.0xATR
* 499 breakouts (0.1 per stock per year), 498 closed trades on 381 distinct dates

| | trades | win | avg R | vs random days | vs random uptrend days |
|---|---|---|---|---|---|
| all breakouts | 498 | 36% | -0.036 | -0.104 | -0.054 |
| random days (CONTROL) | 709,553 | 33% | +0.068 | | |
| random uptrend days | 303,420 | 33% | +0.018 | | |

Breakouts, date-clustered 95% CI of avg R: [-0.139, +0.073]

## Breakdowns (exploratory)

| group | trades | win | avg R | vs random days | vs random uptrend days |
|---|---|---|---|---|---|
| touches = 2 | 264 | 36% | -0.025 | -0.093 | -0.043 |
| touches = 3 | 144 | 35% | -0.074 | -0.142 | -0.092 |
| touches >= 4 | 90 | 37% | -0.008 | -0.076 | -0.025 |
| room to next resistance < 1 ATR | 0 | | | | |
| room 1-3 ATR | 0 | | | | |
| room > 3 ATR | 0 | | | | |
| no resistance above (new 1y high zone) | 498 | 36% | -0.036 | -0.104 | -0.054 |
| breakout volume < 1x avg | 36 | 39% | -0.070 | -0.138 | -0.088 |
| breakout volume 1-1.5x | 81 | 37% | -0.132 | -0.200 | -0.150 |
| breakout volume > 1.5x | 381 | 35% | -0.012 | -0.080 | -0.030 |
| in uptrend (>SMA50 & >SMA200) | 498 | 36% | -0.036 | -0.104 | -0.054 |
| not in uptrend | 0 | | | | |
