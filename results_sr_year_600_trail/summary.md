# Resistance breakouts - 599 stocks, 2016-01-01 -> today - only the zone holding the 52-week high

* exit: trailing stop 3.0xATR, max 60 days; initial stop = zone top - 1.0xATR
* 5,903 breakouts (0.9 per stock per year), 5,853 closed trades on 1,906 distinct dates

| | trades | win | avg R | vs random days | vs random uptrend days |
|---|---|---|---|---|---|
| all breakouts | 5,853 | 31% | -0.044 | -0.115 | -0.053 |
| random days (CONTROL) | 709,880 | 31% | +0.071 | | |
| random uptrend days | 303,451 | 30% | +0.009 | | |

Breakouts, date-clustered 95% CI of avg R: [-0.106, +0.022]

## Breakdowns (exploratory)

| group | trades | win | avg R | vs random days | vs random uptrend days |
|---|---|---|---|---|---|
| touches = 2 | 3,189 | 30% | -0.060 | -0.130 | -0.068 |
| touches = 3 | 1,435 | 30% | -0.086 | -0.157 | -0.095 |
| touches >= 4 | 1,229 | 32% | +0.045 | -0.026 | +0.036 |
| room to next resistance < 1 ATR | 889 | 28% | -0.009 | -0.080 | -0.018 |
| room 1-3 ATR | 0 | | | | |
| room > 3 ATR | 0 | | | | |
| no resistance above (new 1y high zone) | 4,964 | 31% | -0.050 | -0.121 | -0.059 |
| breakout volume < 1x avg | 1,549 | 28% | -0.130 | -0.201 | -0.139 |
| breakout volume 1-1.5x | 1,842 | 30% | +0.005 | -0.066 | -0.004 |
| breakout volume > 1.5x | 2,462 | 32% | -0.027 | -0.098 | -0.036 |
| in uptrend (>SMA50 & >SMA200) | 5,853 | 31% | -0.044 | -0.115 | -0.053 |
| not in uptrend | 0 | | | | |
