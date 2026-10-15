# Resistance breakouts - 903 stocks, 2016-01-01 -> today

* exit: trailing stop 3.0xATR, max 60 days; initial stop = zone top - 1.0xATR
* 50,141 breakouts (5.1 per stock per year), 49,673 closed trades on 2,603 distinct dates

| | trades | win | avg R | vs random days | vs random uptrend days |
|---|---|---|---|---|---|
| all breakouts | 49,673 | 34% | +0.126 | -0.048 | +0.013 |
| random days (CONTROL) | 1,140,411 | 33% | +0.174 | | |
| random uptrend days | 557,211 | 33% | +0.113 | | |

Breakouts, date-clustered 95% CI of avg R: [+0.080, +0.175]

## Breakdowns (exploratory)

| group | trades | win | avg R | vs random days | vs random uptrend days |
|---|---|---|---|---|---|
| touches = 2 | 17,448 | 33% | +0.124 | -0.050 | +0.011 |
| touches = 3 | 13,045 | 34% | +0.115 | -0.059 | +0.002 |
| touches >= 4 | 19,180 | 34% | +0.136 | -0.038 | +0.023 |
| room to next resistance < 1 ATR | 25,142 | 34% | +0.145 | -0.029 | +0.032 |
| room 1-3 ATR | 12,332 | 34% | +0.140 | -0.034 | +0.027 |
| room > 3 ATR | 1,139 | 30% | +0.004 | -0.171 | -0.110 |
| no resistance above (new 1y high zone) | 11,060 | 34% | +0.081 | -0.094 | -0.032 |
| breakout volume < 1x avg | 17,175 | 32% | +0.128 | -0.046 | +0.015 |
| breakout volume 1-1.5x | 18,089 | 33% | +0.144 | -0.030 | +0.031 |
| breakout volume > 1.5x | 14,409 | 36% | +0.103 | -0.072 | -0.010 |
| in uptrend (>SMA50 & >SMA200) | 39,458 | 34% | +0.116 | -0.058 | +0.003 |
| not in uptrend | 10,215 | 33% | +0.165 | -0.010 | +0.051 |
