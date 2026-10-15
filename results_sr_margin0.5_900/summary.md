# Resistance breakouts - 903 stocks, 2016-01-01 -> today - breakout = close > zone top + 0.5xATR - only the zone holding the all-time (since 2010) high

* exit: trailing stop 3.0xATR, max 60 days; initial stop = zone top - 1.0xATR
* 6,637 breakouts (0.7 per stock per year), 6,614 closed trades on 1,925 distinct dates

| | trades | win | avg R | vs random days | vs random uptrend days |
|---|---|---|---|---|---|
| all breakouts | 6,614 | 37% | +0.091 | -0.073 | -0.005 |
| random days (CONTROL) | 1,139,897 | 35% | +0.164 | | |
| random uptrend days | 557,078 | 35% | +0.095 | | |

Breakouts, date-clustered 95% CI of avg R: [+0.039, +0.141]

## Breakdowns (exploratory)

| group | trades | win | avg R | vs random days | vs random uptrend days |
|---|---|---|---|---|---|
| touches = 2 | 3,753 | 37% | +0.079 | -0.085 | -0.016 |
| touches = 3 | 1,710 | 37% | +0.074 | -0.090 | -0.022 |
| touches >= 4 | 1,151 | 38% | +0.154 | -0.010 | +0.058 |
| room to next resistance < 1 ATR | 342 | 42% | +0.404 | +0.240 | +0.308 |
| room 1-3 ATR | 0 | | | | |
| room > 3 ATR | 0 | | | | |
| no resistance above (new 1y high zone) | 6,272 | 37% | +0.073 | -0.090 | -0.022 |
| breakout volume < 1x avg | 1,935 | 35% | +0.070 | -0.093 | -0.025 |
| breakout volume 1-1.5x | 2,390 | 36% | +0.068 | -0.096 | -0.027 |
| breakout volume > 1.5x | 2,289 | 40% | +0.131 | -0.032 | +0.036 |
| in uptrend (>SMA50 & >SMA200) | 6,614 | 37% | +0.091 | -0.073 | -0.005 |
| not in uptrend | 0 | | | | |
