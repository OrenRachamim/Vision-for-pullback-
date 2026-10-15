# Resistance breakouts - 903 stocks, 2016-01-01 -> today - only the zone holding the all-time (since 2010) high

* exit: trailing stop 3.0xATR, max 60 days; initial stop = zone top - 1.0xATR
* 8,246 breakouts (0.8 per stock per year), 8,187 closed trades on 2,061 distinct dates

| | trades | win | avg R | vs random days | vs random uptrend days |
|---|---|---|---|---|---|
| all breakouts | 8,187 | 33% | +0.103 | -0.066 | +0.003 |
| random days (CONTROL) | 1,140,553 | 32% | +0.169 | | |
| random uptrend days | 557,194 | 33% | +0.100 | | |

Breakouts, date-clustered 95% CI of avg R: [+0.050, +0.160]

## Breakdowns (exploratory)

| group | trades | win | avg R | vs random days | vs random uptrend days |
|---|---|---|---|---|---|
| touches = 2 | 4,721 | 33% | +0.097 | -0.072 | -0.002 |
| touches = 3 | 2,087 | 34% | +0.084 | -0.085 | -0.016 |
| touches >= 4 | 1,379 | 36% | +0.150 | -0.019 | +0.051 |
| room to next resistance < 1 ATR | 1,161 | 36% | +0.274 | +0.105 | +0.175 |
| room 1-3 ATR | 0 | | | | |
| room > 3 ATR | 0 | | | | |
| no resistance above (new 1y high zone) | 7,026 | 33% | +0.075 | -0.094 | -0.025 |
| breakout volume < 1x avg | 2,643 | 32% | +0.092 | -0.077 | -0.008 |
| breakout volume 1-1.5x | 2,986 | 32% | +0.085 | -0.084 | -0.014 |
| breakout volume > 1.5x | 2,558 | 37% | +0.134 | -0.035 | +0.035 |
| in uptrend (>SMA50 & >SMA200) | 8,187 | 33% | +0.103 | -0.066 | +0.003 |
| not in uptrend | 0 | | | | |
