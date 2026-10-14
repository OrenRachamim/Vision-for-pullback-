# Pullback scanner - backtest report (`pullback_scanner.py`)

* tickers: 877 / 898 | period: 2016-01-01 -> today
* entry: next open | stop: base_lo | target: 2.0R | max hold: 5 days | dedupe cooldown: 5 bars | combo: daily signal within 15 days after a weekly signal
* baseline = every trading day of the same tickers, same period (2,291,105 days)

## 1. Forward returns vs baseline (next open -> close t+h)

| group / horizon | n | mean | median | pct_up | t_vs_base | p |
|---|---|---|---|---|---|---|
| baseline 5d | 2,286,615 | 0.004 | 0.003 | 0.538 |  |  |
| daily 5d | 9,576 | 0.002 | 0.002 | 0.520 | -3.483 | 0.000 |
| weekly 5d | 717 | -0.000 | -0.000 | 0.492 | -3.269 | 0.001 |
| BUY SIGNAL (daily+weekly) 5d | 72 | -0.003 | -0.002 | 0.444 | -2.246 | 0.025 |
| combo 5d | 113 | -0.001 | -0.001 | 0.487 | -2.226 | 0.026 |
| baseline 10d | 2,282,125 | 0.008 | 0.006 | 0.552 |  |  |
| daily 10d | 9,562 | 0.005 | 0.005 | 0.542 | -4.214 | 0.000 |
| weekly 10d | 717 | 0.001 | 0.002 | 0.515 | -3.937 | 0.000 |
| BUY SIGNAL (daily+weekly) 10d | 72 | 0.001 | -0.000 | 0.472 | -1.629 | 0.103 |
| combo 10d | 113 | -0.002 | -0.001 | 0.478 | -2.476 | 0.013 |
| baseline 20d | 2,273,145 | 0.017 | 0.012 | 0.568 |  |  |
| daily 20d | 9,519 | 0.012 | 0.013 | 0.580 | -5.044 | 0.000 |
| weekly 20d | 715 | 0.005 | 0.009 | 0.568 | -4.565 | 0.000 |
| BUY SIGNAL (daily+weekly) 20d | 72 | 0.010 | 0.015 | 0.583 | -1.021 | 0.307 |
| combo 20d | 111 | 0.006 | 0.015 | 0.604 | -1.474 | 0.140 |
| baseline 60d | 2,237,225 | 0.051 | 0.036 | 0.607 |  |  |
| daily 60d | 9,441 | 0.027 | 0.032 | 0.603 | -13.543 | 0.000 |
| weekly 60d | 713 | 0.002 | 0.014 | 0.562 | -9.410 | 0.000 |
| BUY SIGNAL (daily+weekly) 60d | 72 | 0.001 | 0.048 | 0.639 | -2.677 | 0.007 |
| combo 60d | 110 | -0.001 | 0.035 | 0.600 | -3.661 | 0.000 |

> p is a normal-approx Welch test. Baseline days overlap, so treat p as optimistic.

## 2. Trade simulation with the scanner's own levels

| group | n | trades | win_rate | avg_R | R_ci95 | profit_factor | avg_risk_pct | stopped | hit_target | gap_below_stop | total_R |
|---|---|---|---|---|---|---|---|---|---|---|---|
| daily | 9596 | 9467 | 0.505 | 0.035 | [0.02, 0.05] | 1.126 | 0.055 | 0.158 | 0.039 | 0.011 | 330.499 |
| weekly | 719 | 717 | 0.488 | -0.001 | [-0.04, 0.04] | 0.996 | 0.068 | 0.058 | 0.003 | 0 | 0.163 |
| BUY SIGNAL (daily+weekly) | 72 | 72 | 0.444 | -0.079 | [-0.19, 0.04] | 0.648 | 0.067 | 0.083 | 0.014 | 0 | -5.664 |
| combo | 113 | 113 | 0.487 | -0.038 | [-0.13, 0.05] | 0.807 | 0.064 | 0.053 | 0.009 | 0 | -4.266 |
| CONTROL: random days, same exits | 763445 | 762613 | 0.517 | 0.037 | [0.04, 0.04] | 1.136 | 0.064 | 0.173 | 0.043 | 0 | 28361.835 |

> CONTROL = same entry/stop/target/time rules on every 3rd trading day of the same tickers,
> stop distance drawn from the tested signals' risk distribution. The pattern adds value
> only if its avg_R is clearly above the control's.

* daily vs CONTROL: avg_R diff = -0.002R, t = -0.29, p = 0.775
* weekly vs CONTROL: avg_R diff = -0.038R, t = -1.98, p = 0.047
* BUY SIGNAL (daily+weekly) vs CONTROL: avg_R diff = -0.116R, t = -1.92, p = 0.055
* combo vs CONTROL: avg_R diff = -0.075R, t = -1.64, p = 0.100

## 3. Combo signals split by score and by each component

| split | n | trades | win_rate | avg_R | R_ci95 | profit_factor | fwd20 |
|---|---|---|---|---|---|---|---|
| score=25 | 11 | 11 | 0.545 | -0.054 | [-0.33, 0.25] | 0.773 | -0.022 |
| score=50 | 50 | 50 | 0.500 | -0.056 | [-0.18, 0.08] | 0.701 | 0.004 |
| score=75 | 42 | 42 | 0.500 | -0.013 | [-0.18, 0.15] | 0.941 | 0.019 |
| score=100 | 10 | 10 | 0.300 | -0.034 | [-0.13, 0.07] | 0.622 | -0.001 |
| slowing=True | 89 | 89 | 0.483 | -0.031 | [-0.14, 0.07] | 0.843 | 0.014 |
| slowing=False | 24 | 24 | 0.500 | -0.063 | [-0.23, 0.10] | 0.670 | -0.020 |
| drying=True | 16 | 16 | 0.250 | -0.253 | [-0.47, -0.04] | 0.208 | -0.002 |
| drying=False | 97 | 97 | 0.526 | -0.002 | [-0.09, 0.09] | 0.987 | 0.008 |
| uptrend=True | 59 | 59 | 0.492 | 0.033 | [-0.07, 0.14] | 1.244 | 0.010 |
| uptrend=False | 54 | 54 | 0.481 | -0.115 | [-0.26, 0.03] | 0.565 | 0.003 |

Phase lengths found by detect() (bars):

| phase | mean | min | 50% | max |
|---|---|---|---|---|
| decline_len | 19.381 | 3.000 | 18 | 40 |
| slowdown_len | 16.168 | 0 | 15 | 49 |
| base_len | 7.850 | 3.000 | 9.000 | 10 |
| peak_to_low | 30.097 | 6.000 | 33 | 40 |
| base_above_low | 0.010 | 0 | 0.009 | 0.030 |

## 4. Combo signals per year

| year | n | win_rate | avg_R | total_R | fwd20 |
|---|---|---|---|---|---|
| 2016 | 14 | 0.571 | -0.021 | -0.290 | 0.016 |
| 2017 | 17 | 0.588 | 0.007 | 0.119 | 0.002 |
| 2018 | 12 | 0.417 | -0.172 | -2.062 | -0.004 |
| 2019 | 9 | 0.111 | -0.205 | -1.848 | 0.030 |
| 2020 | 7 | 0.571 | 0.073 | 0.512 | -0.066 |
| 2021 | 9 | 0.556 | 0.385 | 3.466 | 0.048 |
| 2022 | 1 | 1.000 | 0.076 | 0.076 | -0.011 |
| 2023 | 16 | 0.500 | -0.087 | -1.400 | -0.008 |
| 2024 | 8 | 0.500 | 0.112 | 0.899 | 0.013 |
| 2025 | 9 | 0.556 | -0.107 | -0.963 | 0.006 |
| 2026 | 11 | 0.364 | -0.252 | -2.776 | 0.027 |

## 5. Combo signals per ticker (15 worst and 15 best by total_R)

| ticker | n | win_rate | avg_R | total_R | fwd20 |
|---|---|---|---|---|---|
| BKH | 2 | 0 | -0.582 | -1.164 | -0.040 |
| BNY | 1 | 0 | -1.000 | -1.000 | -0.112 |
| CUZ | 1 | 0 | -1.000 | -1.000 | -0.013 |
| PRU | 1 | 0 | -1.000 | -1.000 | -0.050 |
| OMC | 1 | 0 | -1.000 | -1.000 | -0.137 |
| MMS | 1 | 0 | -1.000 | -1.000 | -0.051 |
| OGS | 1 | 0 | -1.000 | -1.000 | 0.013 |
| FE | 2 | 0 | -0.474 | -0.948 | 0.013 |
| STAG | 1 | 0 | -0.846 | -0.846 |  |
| PSX | 1 | 0 | -0.753 | -0.753 | -0.009 |
| HII | 1 | 0 | -0.638 | -0.638 | -0.096 |
| SYK | 1 | 0 | -0.547 | -0.547 | 0.052 |
| SGI | 1 | 0 | -0.523 | -0.523 | -0.465 |
| EAT | 1 | 0 | -0.517 | -0.517 | 0.018 |
| CB | 1 | 0 | -0.491 | -0.491 | -0.005 |
| BMY | 1 | 1.000 | 0.393 | 0.393 | 0.082 |
| SSB | 1 | 1.000 | 0.421 | 0.421 | 0.018 |
| FNF | 1 | 1.000 | 0.427 | 0.427 | 0.009 |
| WHR | 1 | 1.000 | 0.479 | 0.479 | 0.002 |
| ROL | 1 | 1.000 | 0.505 | 0.505 | 0.125 |
| PWR | 1 | 1.000 | 0.560 | 0.560 | 0.015 |
| EPR | 1 | 1.000 | 0.579 | 0.579 | 0.003 |
| HSIC | 1 | 1.000 | 0.585 | 0.585 | 0.023 |
| POST | 2 | 1.000 | 0.383 | 0.767 | 0.029 |
| KMB | 1 | 1.000 | 0.773 | 0.773 | -0.017 |
| MO | 1 | 1.000 | 0.798 | 0.798 | 0.022 |
| WTS | 1 | 1.000 | 0.871 | 0.871 | -0.007 |
| WM | 2 | 1.000 | 0.499 | 0.998 | 0.073 |
| COR | 2 | 0.500 | 0.501 | 1.003 | 0.023 |
| GNTX | 1 | 1.000 | 2.000 | 2.000 | 0.190 |
