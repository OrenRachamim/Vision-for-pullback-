# Resistance breakouts - 903 stocks, 2016-01-01 -> today - only the zone holding the all-time (since 2010) high

* exit: 2.0R target, max 10 days; initial stop = zone top - 1.0xATR
* 8,246 breakouts (0.8 per stock per year), 8,188 closed trades on 2,061 distinct dates

| | trades | win | avg R | vs random days | vs random uptrend days |
|---|---|---|---|---|---|
| all breakouts | 8,188 | 46% | +0.047 | -0.034 | -0.006 |
| random days (CONTROL) | 1,142,823 | 45% | +0.082 | | |
| random uptrend days | 557,755 | 45% | +0.054 | | |

Breakouts, date-clustered 95% CI of avg R: [+0.010, +0.087]

## Breakdowns (exploratory)

| group | trades | win | avg R | vs random days | vs random uptrend days |
|---|---|---|---|---|---|
| touches = 2 | 4,721 | 45% | +0.038 | -0.044 | -0.016 |
| touches = 3 | 2,088 | 47% | +0.034 | -0.047 | -0.019 |
| touches >= 4 | 1,379 | 49% | +0.100 | +0.019 | +0.047 |
| room to next resistance < 1 ATR | 1,161 | 49% | +0.197 | +0.115 | +0.144 |
| room 1-3 ATR | 0 | | | | |
| room > 3 ATR | 0 | | | | |
| no resistance above (new 1y high zone) | 7,027 | 46% | +0.023 | -0.059 | -0.031 |
| breakout volume < 1x avg | 2,643 | 44% | +0.035 | -0.046 | -0.018 |
| breakout volume 1-1.5x | 2,987 | 46% | +0.030 | -0.052 | -0.024 |
| breakout volume > 1.5x | 2,558 | 49% | +0.081 | -0.001 | +0.027 |
| in uptrend (>SMA50 & >SMA200) | 8,188 | 46% | +0.047 | -0.034 | -0.006 |
| not in uptrend | 0 | | | | |
