# Pullback scanner - backtest report (`pullback_scanner.py`)

* tickers: 877 / 898 | period: 2016-01-01 -> today
* entry: next open | stop: base_lo | target: 2.0R | max hold: 5 days | dedupe cooldown: 5 bars | combo: daily signal within 15 days after a weekly signal
* baseline = every trading day of the same tickers, same period (2,291,105 days)

## 1. Forward returns vs baseline (next open -> close t+h)

| group / horizon | n | mean | median | pct_up | t_vs_base | p |
|---|---|---|---|---|---|---|
| baseline 5d | 2,286,615 | 0.004 | 0.003 | 0.538 |  |  |
| daily 5d | 9,499 | 0.002 | 0.002 | 0.521 | -3.382 | 0.001 |
| weekly 5d | 717 | -0.000 | -0.000 | 0.492 | -3.269 | 0.001 |
| BUY SIGNAL (daily+weekly) 5d | 73 | -0.003 | -0.002 | 0.452 | -2.215 | 0.027 |
| combo 5d | 115 | -0.002 | -0.001 | 0.478 | -2.488 | 0.013 |
| baseline 10d | 2,282,125 | 0.008 | 0.006 | 0.552 |  |  |
| daily 10d | 9,485 | 0.005 | 0.005 | 0.542 | -4.155 | 0.000 |
| weekly 10d | 717 | 0.001 | 0.002 | 0.515 | -3.937 | 0.000 |
| BUY SIGNAL (daily+weekly) 10d | 73 | 0.001 | -0.000 | 0.479 | -1.621 | 0.105 |
| combo 10d | 115 | -0.002 | -0.001 | 0.470 | -2.594 | 0.009 |
| baseline 20d | 2,273,145 | 0.017 | 0.012 | 0.568 |  |  |
| daily 20d | 9,442 | 0.012 | 0.013 | 0.581 | -4.961 | 0.000 |
| weekly 20d | 715 | 0.005 | 0.009 | 0.568 | -4.565 | 0.000 |
| BUY SIGNAL (daily+weekly) 20d | 73 | 0.009 | 0.014 | 0.589 | -1.044 | 0.296 |
| combo 20d | 113 | 0.006 | 0.014 | 0.602 | -1.585 | 0.113 |
| baseline 60d | 2,237,225 | 0.051 | 0.036 | 0.607 |  |  |
| daily 60d | 9,364 | 0.027 | 0.032 | 0.603 | -13.544 | 0.000 |
| weekly 60d | 713 | 0.002 | 0.014 | 0.562 | -9.410 | 0.000 |
| BUY SIGNAL (daily+weekly) 60d | 73 | 0.001 | 0.041 | 0.644 | -2.684 | 0.007 |
| combo 60d | 112 | -0.001 | 0.035 | 0.607 | -3.687 | 0.000 |

> p is a normal-approx Welch test. Baseline days overlap, so treat p as optimistic.

## 2. Trade simulation with the scanner's own levels

| group | n | trades | win_rate | avg_R | R_ci95 | profit_factor | avg_risk_pct | stopped | hit_target | gap_below_stop | total_R |
|---|---|---|---|---|---|---|---|---|---|---|---|
| daily | 9519 | 9391 | 0.506 | 0.035 | [0.02, 0.05] | 1.129 | 0.055 | 0.157 | 0.039 | 0.011 | 334.116 |
| weekly | 719 | 717 | 0.488 | -0.001 | [-0.04, 0.04] | 0.996 | 0.068 | 0.058 | 0.003 | 0 | 0.163 |
| BUY SIGNAL (daily+weekly) | 73 | 73 | 0.452 | -0.074 | [-0.19, 0.04] | 0.663 | 0.066 | 0.082 | 0.014 | 0 | -5.423 |
| combo | 115 | 115 | 0.478 | -0.059 | [-0.15, 0.03] | 0.718 | 0.064 | 0.070 | 0.009 | 0 | -6.798 |
| CONTROL: random days, same exits | 763445 | 762596 | 0.516 | 0.037 | [0.04, 0.04] | 1.135 | 0.064 | 0.175 | 0.044 | 0 | 28278.942 |

> CONTROL = same entry/stop/target/time rules on every 3rd trading day of the same tickers,
> stop distance drawn from the tested signals' risk distribution. The pattern adds value
> only if its avg_R is clearly above the control's.

* daily vs CONTROL: avg_R diff = -0.002R, t = -0.19, p = 0.850
* weekly vs CONTROL: avg_R diff = -0.038R, t = -1.98, p = 0.048
* BUY SIGNAL (daily+weekly) vs CONTROL: avg_R diff = -0.111R, t = -1.87, p = 0.062
* combo vs CONTROL: avg_R diff = -0.096R, t = -2.10, p = 0.036

## 3. Combo signals split by score and by each component

| split | n | trades | win_rate | avg_R | R_ci95 | profit_factor | fwd20 |
|---|---|---|---|---|---|---|---|
| score=25 | 21 | 21 | 0.476 | -0.117 | [-0.29, 0.05] | 0.505 | 0.010 |
| score=50 | 42 | 42 | 0.476 | -0.097 | [-0.25, 0.07] | 0.589 | -0.003 |
| score=75 | 42 | 42 | 0.500 | -0.015 | [-0.17, 0.14] | 0.924 | 0.007 |
| score=100 | 10 | 10 | 0.400 | 0.036 | [-0.12, 0.22] | 1.355 | 0.032 |
| slowing=True | 82 | 82 | 0.476 | -0.048 | [-0.16, 0.07] | 0.776 | 0.007 |
| slowing=False | 33 | 33 | 0.485 | -0.086 | [-0.21, 0.05] | 0.560 | 0.003 |
| drying=True | 12 | 12 | 0.417 | -0.038 | [-0.24, 0.16] | 0.756 | 0.027 |
| drying=False | 103 | 103 | 0.485 | -0.062 | [-0.16, 0.03] | 0.715 | 0.004 |
| uptrend=True | 62 | 62 | 0.484 | 0.003 | [-0.11, 0.11] | 1.017 | 0.008 |
| uptrend=False | 53 | 53 | 0.472 | -0.131 | [-0.27, 0.02] | 0.511 | 0.003 |

Phase lengths found by detect() (bars):

| phase | mean | min | 50% | max |
|---|---|---|---|---|
| decline_len | 37 | 3.000 | 31 | 109 |
| slowdown_len | 26.757 | 0 | 21 | 108 |
| base_len | 7.783 | 3.000 | 9.000 | 10 |
| peak_to_low | 58.165 | 7.000 | 49 | 120 |
| base_above_low | 0.010 | 0 | 0.010 | 0.030 |

## 4. Combo signals per year

| year | n | win_rate | avg_R | total_R | fwd20 |
|---|---|---|---|---|---|
| 2016 | 15 | 0.533 | -0.086 | -1.290 | 0.011 |
| 2017 | 17 | 0.529 | -0.097 | -1.653 | 0.002 |
| 2018 | 12 | 0.417 | -0.172 | -2.062 | -0.004 |
| 2019 | 10 | 0.200 | -0.161 | -1.607 | 0.027 |
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
| MDLZ | 1 | 0 | -1.000 | -1.000 | -0.048 |
| XOM | 1 | 0 | -1.000 | -1.000 | -0.032 |
| OGS | 1 | 0 | -1.000 | -1.000 | 0.013 |
| CUZ | 1 | 0 | -1.000 | -1.000 | -0.013 |
| PRU | 1 | 0 | -1.000 | -1.000 | -0.050 |
| MMS | 1 | 0 | -1.000 | -1.000 | -0.051 |
| BNY | 1 | 0 | -1.000 | -1.000 | -0.112 |
| OMC | 1 | 0 | -1.000 | -1.000 | -0.137 |
| FE | 2 | 0 | -0.474 | -0.948 | 0.013 |
| STAG | 1 | 0 | -0.846 | -0.846 |  |
| PSX | 1 | 0 | -0.753 | -0.753 | -0.009 |
| HII | 1 | 0 | -0.638 | -0.638 | -0.096 |
| SYK | 1 | 0 | -0.547 | -0.547 | 0.052 |
| SGI | 1 | 0 | -0.523 | -0.523 | -0.465 |
| NWS | 1 | 1.000 | 0.333 | 0.333 | 0.043 |
| BMY | 1 | 1.000 | 0.393 | 0.393 | 0.082 |
| SSB | 1 | 1.000 | 0.421 | 0.421 | 0.018 |
| FNF | 1 | 1.000 | 0.427 | 0.427 | 0.009 |
| WHR | 1 | 1.000 | 0.479 | 0.479 | 0.002 |
| ROL | 1 | 1.000 | 0.505 | 0.505 | 0.125 |
| PWR | 1 | 1.000 | 0.560 | 0.560 | 0.015 |
| EPR | 1 | 1.000 | 0.579 | 0.579 | 0.003 |
| HSIC | 1 | 1.000 | 0.585 | 0.585 | 0.023 |
| POST | 2 | 1.000 | 0.383 | 0.767 | 0.029 |
| MO | 1 | 1.000 | 0.798 | 0.798 | 0.022 |
| WTS | 1 | 1.000 | 0.871 | 0.871 | -0.007 |
| WM | 2 | 1.000 | 0.499 | 0.998 | 0.073 |
| COR | 2 | 0.500 | 0.501 | 1.003 | 0.023 |
| GNTX | 1 | 1.000 | 2.000 | 2.000 | 0.190 |
