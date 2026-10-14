# Pullback scanner - backtest report (`pullback_scanner.py`)

* tickers: 877 / 898 | period: 2016-01-01 -> today
* entry: next open | stop: base_lo | target: 2.0R | max hold: 10 days | dedupe cooldown: 5 bars | combo: daily signal within 15 days after a weekly signal
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
| daily | 9519 | 9379 | 0.505 | 0.072 | [0.05, 0.09] | 1.202 | 0.055 | 0.263 | 0.083 | 0.011 | 685.660 |
| weekly | 719 | 717 | 0.505 | 0.007 | [-0.04, 0.06] | 1.027 | 0.068 | 0.160 | 0.015 | 0 | 6.110 |
| BUY SIGNAL (daily+weekly) | 73 | 73 | 0.466 | -0.109 | [-0.29, 0.07] | 0.690 | 0.066 | 0.233 | 0.014 | 0 | -7.968 |
| combo | 115 | 115 | 0.461 | -0.126 | [-0.26, 0.01] | 0.644 | 0.064 | 0.235 | 0.009 | 0 | -14.526 |
| CONTROL: random days, same exits | 763445 | 761294 | 0.503 | 0.069 | [0.07, 0.07] | 1.190 | 0.064 | 0.280 | 0.095 | 0 | 52807.962 |

> CONTROL = same entry/stop/target/time rules on every 3rd trading day of the same tickers,
> stop distance drawn from the tested signals' risk distribution. The pattern adds value
> only if its avg_R is clearly above the control's.

* daily vs CONTROL: avg_R diff = +0.004R, t = 0.35, p = 0.726
* weekly vs CONTROL: avg_R diff = -0.061R, t = -2.31, p = 0.021
* BUY SIGNAL (daily+weekly) vs CONTROL: avg_R diff = -0.178R, t = -1.97, p = 0.048
* combo vs CONTROL: avg_R diff = -0.195R, t = -2.88, p = 0.004

## 3. Combo signals split by score and by each component

| split | n | trades | win_rate | avg_R | R_ci95 | profit_factor | fwd20 |
|---|---|---|---|---|---|---|---|
| score=25 | 21 | 21 | 0.381 | -0.316 | [-0.69, 0.04] | 0.365 | 0.010 |
| score=50 | 42 | 42 | 0.381 | -0.234 | [-0.44, -0.01] | 0.453 | -0.003 |
| score=75 | 42 | 42 | 0.548 | -0.000 | [-0.19, 0.20] | 0.998 | 0.007 |
| score=100 | 10 | 10 | 0.600 | 0.196 | [-0.10, 0.48] | 2.698 | 0.032 |
| slowing=True | 82 | 82 | 0.463 | -0.104 | [-0.24, 0.04] | 0.685 | 0.007 |
| slowing=False | 33 | 33 | 0.455 | -0.183 | [-0.49, 0.09] | 0.564 | 0.003 |
| drying=True | 12 | 12 | 0.583 | 0.107 | [-0.20, 0.40] | 1.596 | 0.027 |
| drying=False | 103 | 103 | 0.447 | -0.154 | [-0.30, -0.01] | 0.591 | 0.004 |
| uptrend=True | 62 | 62 | 0.565 | 0.052 | [-0.10, 0.21] | 1.219 | 0.008 |
| uptrend=False | 53 | 53 | 0.340 | -0.335 | [-0.55, -0.12] | 0.317 | 0.003 |

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
| 2016 | 15 | 0.533 | 0.128 | 1.917 | 0.011 |
| 2017 | 17 | 0.294 | -0.157 | -2.668 | 0.002 |
| 2018 | 12 | 0.417 | -0.175 | -2.096 | -0.004 |
| 2019 | 10 | 0.500 | -0.032 | -0.317 | 0.027 |
| 2020 | 7 | 0.429 | -0.332 | -2.322 | -0.066 |
| 2021 | 9 | 0.556 | 0.326 | 2.937 | 0.048 |
| 2022 | 1 | 0 | -0.536 | -0.536 | -0.011 |
| 2023 | 16 | 0.500 | -0.417 | -6.671 | -0.008 |
| 2024 | 8 | 0.750 | 0.154 | 1.233 | 0.013 |
| 2025 | 9 | 0.556 | -0.081 | -0.733 | 0.006 |
| 2026 | 11 | 0.273 | -0.479 | -5.271 | 0.027 |

## 5. Combo signals per ticker (15 worst and 15 best by total_R)

| ticker | n | win_rate | avg_R | total_R | fwd20 |
|---|---|---|---|---|---|
| TXNM | 2 | 0.500 | -1.003 | -2.005 | -0.055 |
| SGI | 1 | 0 | -1.220 | -1.220 | -0.465 |
| PSX | 1 | 0 | -1.136 | -1.136 | -0.009 |
| XYL | 1 | 0 | -1.000 | -1.000 | -0.113 |
| INCY | 1 | 0 | -1.000 | -1.000 | -0.027 |
| MDLZ | 1 | 0 | -1.000 | -1.000 | -0.048 |
| MIDD | 1 | 0 | -1.000 | -1.000 | -0.009 |
| MMS | 1 | 0 | -1.000 | -1.000 | -0.051 |
| FNF | 1 | 0 | -1.000 | -1.000 | 0.009 |
| NEE | 1 | 0 | -1.000 | -1.000 | -0.047 |
| NEM | 1 | 0 | -1.000 | -1.000 | -0.022 |
| OGS | 1 | 0 | -1.000 | -1.000 | 0.013 |
| XOM | 1 | 0 | -1.000 | -1.000 | -0.032 |
| CUZ | 1 | 0 | -1.000 | -1.000 | -0.013 |
| PRU | 1 | 0 | -1.000 | -1.000 | -0.050 |
| HSIC | 1 | 1.000 | 0.529 | 0.529 | 0.023 |
| JBL | 1 | 1.000 | 0.540 | 0.540 | -0.040 |
| COR | 2 | 0.500 | 0.324 | 0.648 | 0.023 |
| ROL | 1 | 1.000 | 0.676 | 0.676 | 0.125 |
| GPC | 1 | 1.000 | 0.732 | 0.732 | 0.066 |
| PAYX | 1 | 1.000 | 0.733 | 0.733 | 0.079 |
| EPR | 1 | 1.000 | 0.734 | 0.734 | 0.003 |
| ADP | 1 | 1.000 | 0.735 | 0.735 | 0.064 |
| AKAM | 1 | 1.000 | 0.896 | 0.896 | 0.102 |
| BMY | 1 | 1.000 | 1.071 | 1.071 | 0.082 |
| POST | 2 | 1.000 | 0.584 | 1.169 | 0.029 |
| G | 1 | 1.000 | 1.264 | 1.264 | 0.082 |
| MO | 1 | 1.000 | 1.430 | 1.430 | 0.022 |
| WM | 2 | 1.000 | 0.739 | 1.477 | 0.073 |
| GNTX | 1 | 1.000 | 2.000 | 2.000 | 0.190 |
