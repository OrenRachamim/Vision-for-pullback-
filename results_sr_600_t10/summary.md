# Resistance breakouts - 599 stocks, 2016-01-01 -> today

* exit: 2.0R target, max 10 days; initial stop = zone top - 1.0xATR
* 30,658 breakouts (4.7 per stock per year), 30,407 closed trades on 2,560 distinct dates

| | trades | win | avg R | vs random days | vs random uptrend days |
|---|---|---|---|---|---|
| all breakouts | 30,407 | 43% | +0.029 | -0.013 | +0.024 |
| random days (CONTROL) | 711,397 | 43% | +0.042 | | |
| random uptrend days | 303,958 | 43% | +0.005 | | |

Breakouts, date-clustered 95% CI of avg R: [-0.005, +0.064]

## Breakdowns (exploratory)

| group | trades | win | avg R | vs random days | vs random uptrend days |
|---|---|---|---|---|---|
| touches = 2 | 10,346 | 42% | +0.026 | -0.016 | +0.022 |
| touches = 3 | 7,942 | 44% | +0.029 | -0.013 | +0.024 |
| touches >= 4 | 12,119 | 44% | +0.031 | -0.011 | +0.026 |
| room to next resistance < 1 ATR | 15,892 | 43% | +0.034 | -0.008 | +0.029 |
| room 1-3 ATR | 8,077 | 43% | +0.021 | -0.021 | +0.016 |
| room > 3 ATR | 983 | 43% | +0.029 | -0.013 | +0.024 |
| no resistance above (new 1y high zone) | 5,455 | 44% | +0.025 | -0.017 | +0.021 |
| breakout volume < 1x avg | 9,896 | 42% | +0.016 | -0.026 | +0.012 |
| breakout volume 1-1.5x | 10,178 | 43% | +0.035 | -0.007 | +0.030 |
| breakout volume > 1.5x | 10,333 | 45% | +0.035 | -0.007 | +0.030 |
| in uptrend (>SMA50 & >SMA200) | 22,973 | 44% | +0.034 | -0.009 | +0.029 |
| not in uptrend | 7,434 | 42% | +0.014 | -0.028 | +0.009 |
