# Resistance breakouts - 599 stocks, 2016-01-01 -> today - breakout = close > zone top + 0.1xATR - only the zone holding the all-time (since 2010) high

* exit: trailing stop 3.0xATR, max 60 days; initial stop = zone top - 1.0xATR
* 3,290 breakouts (0.5 per stock per year), 3,263 closed trades on 1,458 distinct dates

| | trades | win | avg R | vs random days | vs random uptrend days |
|---|---|---|---|---|---|
| all breakouts | 3,263 | 30% | -0.016 | -0.087 | -0.022 |
| random days (CONTROL) | 710,058 | 30% | +0.071 | | |
| random uptrend days | 303,511 | 29% | +0.006 | | |

Breakouts, date-clustered 95% CI of avg R: [-0.095, +0.066]

## Breakdowns (exploratory)

| group | trades | win | avg R | vs random days | vs random uptrend days |
|---|---|---|---|---|---|
| touches = 2 | 1,882 | 30% | -0.021 | -0.092 | -0.027 |
| touches = 3 | 818 | 30% | -0.028 | -0.099 | -0.034 |
| touches >= 4 | 563 | 31% | +0.018 | -0.053 | +0.012 |
| room to next resistance < 1 ATR | 426 | 27% | -0.012 | -0.083 | -0.018 |
| room 1-3 ATR | 0 | | | | |
| room > 3 ATR | 0 | | | | |
| no resistance above (new 1y high zone) | 2,837 | 31% | -0.016 | -0.087 | -0.022 |
| breakout volume < 1x avg | 968 | 27% | -0.114 | -0.184 | -0.120 |
| breakout volume 1-1.5x | 1,079 | 30% | +0.034 | -0.036 | +0.029 |
| breakout volume > 1.5x | 1,216 | 33% | +0.017 | -0.054 | +0.011 |
| in uptrend (>SMA50 & >SMA200) | 3,263 | 30% | -0.016 | -0.087 | -0.022 |
| not in uptrend | 0 | | | | |
