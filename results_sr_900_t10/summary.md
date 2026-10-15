# Resistance breakouts - 903 stocks, 2016-01-01 -> today

* exit: 2.0R target, max 10 days; initial stop = zone top - 1.0xATR
* 50,141 breakouts (5.1 per stock per year), 49,710 closed trades on 2,604 distinct dates

| | trades | win | avg R | vs random days | vs random uptrend days |
|---|---|---|---|---|---|
| all breakouts | 49,710 | 46% | +0.067 | -0.015 | +0.013 |
| random days (CONTROL) | 1,142,719 | 45% | +0.082 | | |
| random uptrend days | 557,765 | 46% | +0.055 | | |

Breakouts, date-clustered 95% CI of avg R: [+0.038, +0.096]

## Breakdowns (exploratory)

| group | trades | win | avg R | vs random days | vs random uptrend days |
|---|---|---|---|---|---|
| touches = 2 | 17,464 | 45% | +0.048 | -0.034 | -0.007 |
| touches = 3 | 13,054 | 46% | +0.075 | -0.007 | +0.020 |
| touches >= 4 | 19,192 | 47% | +0.080 | -0.002 | +0.025 |
| room to next resistance < 1 ATR | 25,166 | 46% | +0.087 | +0.005 | +0.032 |
| room 1-3 ATR | 12,338 | 46% | +0.068 | -0.014 | +0.013 |
| room > 3 ATR | 1,141 | 43% | +0.022 | -0.060 | -0.032 |
| no resistance above (new 1y high zone) | 11,065 | 46% | +0.027 | -0.055 | -0.027 |
| breakout volume < 1x avg | 17,185 | 45% | +0.064 | -0.018 | +0.009 |
| breakout volume 1-1.5x | 18,102 | 46% | +0.072 | -0.010 | +0.018 |
| breakout volume > 1.5x | 14,423 | 48% | +0.065 | -0.018 | +0.010 |
| in uptrend (>SMA50 & >SMA200) | 39,483 | 46% | +0.068 | -0.014 | +0.014 |
| not in uptrend | 10,227 | 45% | +0.064 | -0.018 | +0.009 |
