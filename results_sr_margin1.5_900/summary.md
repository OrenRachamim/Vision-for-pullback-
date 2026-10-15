# Resistance breakouts - 903 stocks, 2016-01-01 -> today - breakout = close > zone top + 1.5xATR - only the zone holding the all-time (since 2010) high

* exit: trailing stop 3.0xATR, max 60 days; initial stop = zone top - 1.0xATR
* 1,253 breakouts (0.1 per stock per year), 1,250 closed trades on 773 distinct dates

| | trades | win | avg R | vs random days | vs random uptrend days |
|---|---|---|---|---|---|
| all breakouts | 1,250 | 44% | +0.103 | -0.033 | +0.025 |
| random days (CONTROL) | 1,139,181 | 38% | +0.136 | | |
| random uptrend days | 556,922 | 38% | +0.078 | | |

Breakouts, date-clustered 95% CI of avg R: [+0.038, +0.169]

## Breakdowns (exploratory)

| group | trades | win | avg R | vs random days | vs random uptrend days |
|---|---|---|---|---|---|
| touches = 2 | 654 | 43% | +0.122 | -0.014 | +0.044 |
| touches = 3 | 334 | 47% | +0.133 | -0.003 | +0.055 |
| touches >= 4 | 262 | 42% | +0.019 | -0.117 | -0.059 |
| room to next resistance < 1 ATR | 0 | | | | |
| room 1-3 ATR | 0 | | | | |
| room > 3 ATR | 0 | | | | |
| no resistance above (new 1y high zone) | 1,250 | 44% | +0.103 | -0.033 | +0.025 |
| breakout volume < 1x avg | 109 | 42% | +0.118 | -0.018 | +0.040 |
| breakout volume 1-1.5x | 255 | 38% | +0.058 | -0.077 | -0.020 |
| breakout volume > 1.5x | 886 | 46% | +0.114 | -0.021 | +0.036 |
| in uptrend (>SMA50 & >SMA200) | 1,250 | 44% | +0.103 | -0.033 | +0.025 |
| not in uptrend | 0 | | | | |
