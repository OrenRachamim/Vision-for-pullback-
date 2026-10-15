# Resistance breakouts - 599 stocks, 2016-01-01 -> today

* exit: trailing stop 3.0xATR, max 60 days; initial stop = zone top - 1.0xATR
* 30,658 breakouts (4.7 per stock per year), 30,385 closed trades on 2,560 distinct dates

| | trades | win | avg R | vs random days | vs random uptrend days |
|---|---|---|---|---|---|
| all breakouts | 30,385 | 31% | -0.004 | -0.080 | -0.014 |
| random days (CONTROL) | 709,849 | 31% | +0.076 | | |
| random uptrend days | 303,446 | 30% | +0.010 | | |

Breakouts, date-clustered 95% CI of avg R: [-0.047, +0.043]

## Breakdowns (exploratory)

| group | trades | win | avg R | vs random days | vs random uptrend days |
|---|---|---|---|---|---|
| touches = 2 | 10,336 | 30% | -0.013 | -0.089 | -0.023 |
| touches = 3 | 7,936 | 31% | -0.003 | -0.079 | -0.013 |
| touches >= 4 | 12,113 | 31% | +0.003 | -0.073 | -0.007 |
| room to next resistance < 1 ATR | 15,884 | 30% | -0.001 | -0.077 | -0.011 |
| room 1-3 ATR | 8,069 | 31% | +0.014 | -0.062 | +0.004 |
| room > 3 ATR | 983 | 31% | -0.020 | -0.096 | -0.029 |
| no resistance above (new 1y high zone) | 5,449 | 32% | -0.035 | -0.111 | -0.045 |
| breakout volume < 1x avg | 9,889 | 29% | -0.020 | -0.096 | -0.029 |
| breakout volume 1-1.5x | 10,171 | 30% | +0.001 | -0.075 | -0.009 |
| breakout volume > 1.5x | 10,325 | 33% | +0.006 | -0.070 | -0.004 |
| in uptrend (>SMA50 & >SMA200) | 22,953 | 31% | +0.003 | -0.073 | -0.007 |
| not in uptrend | 7,432 | 30% | -0.025 | -0.101 | -0.034 |
