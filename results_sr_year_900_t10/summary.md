# Resistance breakouts - 903 stocks, 2016-01-01 -> today - only the zone holding the 52-week high

* exit: 2.0R target, max 10 days; initial stop = zone top - 1.0xATR
* 12,291 breakouts (1.3 per stock per year), 12,205 closed trades on 2,264 distinct dates

| | trades | win | avg R | vs random days | vs random uptrend days |
|---|---|---|---|---|---|
| all breakouts | 12,205 | 46% | +0.044 | -0.036 | -0.010 |
| random days (CONTROL) | 1,142,745 | 45% | +0.079 | | |
| random uptrend days | 557,734 | 45% | +0.053 | | |

Breakouts, date-clustered 95% CI of avg R: [+0.010, +0.076]

## Breakdowns (exploratory)

| group | trades | win | avg R | vs random days | vs random uptrend days |
|---|---|---|---|---|---|
| touches = 2 | 6,779 | 45% | +0.027 | -0.053 | -0.026 |
| touches = 3 | 3,177 | 47% | +0.064 | -0.015 | +0.011 |
| touches >= 4 | 2,249 | 47% | +0.065 | -0.015 | +0.011 |
| room to next resistance < 1 ATR | 1,888 | 48% | +0.169 | +0.090 | +0.116 |
| room 1-3 ATR | 0 | | | | |
| room > 3 ATR | 0 | | | | |
| no resistance above (new 1y high zone) | 10,317 | 45% | +0.021 | -0.059 | -0.033 |
| breakout volume < 1x avg | 3,697 | 44% | +0.022 | -0.058 | -0.032 |
| breakout volume 1-1.5x | 4,373 | 45% | +0.025 | -0.055 | -0.029 |
| breakout volume > 1.5x | 4,135 | 49% | +0.083 | +0.004 | +0.030 |
| in uptrend (>SMA50 & >SMA200) | 12,205 | 46% | +0.044 | -0.036 | -0.010 |
| not in uptrend | 0 | | | | |
