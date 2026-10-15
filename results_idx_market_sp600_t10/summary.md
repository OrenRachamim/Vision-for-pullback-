# Pullback scanner - backtest report (`pullback_scanner.py`)

* tickers: 558 / 590 | period: 2016-01-01 -> today
* entry: next open | stop: base_lo | target: 2.0R | max hold: 10 days | dedupe cooldown: 5 bars | index combo (market): stock daily signal + index pullback signal within 5 days
* baseline = every trading day of the same tickers, same period (1,426,819 days)

## 1. Forward returns vs baseline (next open -> close t+h)

| group / horizon | n | mean | median | pct_up | t_vs_base | p |
|---|---|---|---|---|---|---|
| baseline 5d | 1,423,869 | 0.003 | 0.002 | 0.517 |  |  |
| daily 5d | 4,973 | 0.001 | 0.001 | 0.506 | -2.494 | 0.013 |
| combo 5d | 1,087 | 0.003 | -0.000 | 0.499 | -0.091 | 0.928 |
| baseline 10d | 1,420,919 | 0.006 | 0.004 | 0.527 |  |  |
| daily 10d | 4,962 | 0.004 | 0.003 | 0.527 | -2.258 | 0.024 |
| combo 10d | 1,081 | 0.010 | 0.006 | 0.547 | 2.041 | 0.041 |
| baseline 20d | 1,415,019 | 0.013 | 0.008 | 0.538 |  |  |
| daily 20d | 4,953 | 0.010 | 0.008 | 0.541 | -2.524 | 0.012 |
| combo 20d | 1,081 | 0.015 | 0.007 | 0.537 | 0.535 | 0.592 |
| baseline 60d | 1,391,419 | 0.041 | 0.025 | 0.563 |  |  |
| daily 60d | 4,912 | 0.021 | 0.021 | 0.557 | -8.472 | 0.000 |
| combo 60d | 1,064 | 0.024 | 0.028 | 0.583 | -3.398 | 0.001 |

> p is a normal-approx Welch test. Baseline days overlap, so treat p as optimistic.

## 2. Trade simulation with the scanner's own levels

| group | n | trades | win_rate | avg_R | R_ci95 | profit_factor | avg_risk_pct | stopped | trailed | hit_target | gap_below_stop | total_R |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| daily | 4976 | 4921 | 0.472 | 0.039 | [0.01, 0.07] | 1.098 | 0.059 | 0.314 | 0 | 0.102 | 0.009 | 195.424 |
| combo | 1089 | 1074 | 0.503 | 0.108 | [0.05, 0.17] | 1.310 | 0.062 | 0.269 | 0 | 0.088 | 0.008 | 116.506 |
| CONTROL: random days, same exits | 475467 | 474199 | 0.457 | 0.039 | [0.04, 0.04] | 1.090 | 0.062 | 0.363 | 0 | 0.139 | 0 | 18900.143 |

> CONTROL = same entry/stop/target/time rules on every 3rd trading day of the same tickers,
> stop distance drawn from the tested signals' risk distribution. The pattern adds value
> only if its avg_R is clearly above the control's.

* daily vs CONTROL: avg_R diff = -0.000R, t = -0.00, p = 1.000
* combo vs CONTROL: avg_R diff = +0.069R, t = 2.27, p = 0.023

## 3. Combo signals split by score and by each component

| split | n | trades | win_rate | avg_R | R_ci95 | profit_factor | fwd20 |
|---|---|---|---|---|---|---|---|
| score=25 | 167 | 166 | 0.572 | 0.175 | [0.01, 0.34] | 1.475 | 0.025 |
| score=50 | 447 | 438 | 0.500 | 0.137 | [0.05, 0.23] | 1.409 | 0.017 |
| score=75 | 355 | 352 | 0.483 | 0.080 | [-0.02, 0.18] | 1.232 | 0.011 |
| score=100 | 120 | 118 | 0.475 | -0.013 | [-0.17, 0.16] | 0.966 | 0.004 |
| slowing=True | 487 | 479 | 0.470 | 0.026 | [-0.06, 0.10] | 1.072 | 0.007 |
| slowing=False | 602 | 595 | 0.529 | 0.174 | [0.09, 0.26] | 1.515 | 0.021 |
| drying=True | 313 | 310 | 0.477 | 0.102 | [-0.01, 0.22] | 1.288 | 0.012 |
| drying=False | 776 | 764 | 0.513 | 0.111 | [0.04, 0.18] | 1.319 | 0.016 |
| uptrend=True | 717 | 707 | 0.501 | 0.097 | [0.03, 0.16] | 1.283 | 0.013 |
| uptrend=False | 372 | 367 | 0.507 | 0.130 | [0.03, 0.23] | 1.358 | 0.018 |

Phase lengths found by detect() (bars):

| phase | mean | min | 50% | max |
|---|---|---|---|---|
| decline_len | 15.162 | 2.000 | 13 | 41 |
| slowdown_len | 9.417 | 0 | 6.000 | 57 |
| base_len | 5.560 | 3.000 | 5.000 | 10 |
| peak_to_low | 22.076 | 0 | 21 | 40 |
| base_above_low | 0.008 | 0 | 0 | 0.071 |

## 4. Combo signals per year

| year | n | win_rate | avg_R | total_R | fwd20 |
|---|---|---|---|---|---|
| 2016 | 133 | 0.712 | 0.595 | 78.542 | 0.076 |
| 2017 | 214 | 0.474 | 0.073 | 15.525 | 0.004 |
| 2018 | 88 | 0.455 | -0.086 | -7.597 | -0.022 |
| 2019 | 96 | 0.625 | 0.175 | 16.758 | 0.014 |
| 2020 | 53 | 0.340 | -0.103 | -5.445 | 0.013 |
| 2021 | 37 | 0.514 | -0.102 | -3.792 | -0.002 |
| 2022 | 54 | 0.481 | 0.092 | 4.983 | 0.062 |
| 2023 | 151 | 0.403 | -0.121 | -17.959 | -0.002 |
| 2024 | 176 | 0.437 | 0.102 | 17.810 | 0.002 |
| 2025 | 18 | 0.722 | 0.408 | 7.350 | 0.018 |
| 2026 | 69 | 0.550 | 0.164 | 10.331 | 0.020 |

## 5. Combo signals per ticker (15 worst and 15 best by total_R)

| ticker | n | win_rate | avg_R | total_R | fwd20 |
|---|---|---|---|---|---|
| LRN | 2 | 0 | -2.736 | -5.472 | -0.098 |
| VSH | 4 | 0 | -1.020 | -4.080 | -0.068 |
| HSTM | 4 | 0 | -1.000 | -4.000 | -0.012 |
| FUL | 7 | 0.286 | -0.487 | -3.407 | -0.070 |
| WEN | 5 | 0.200 | -0.661 | -3.304 | -0.002 |
| MDU | 8 | 0.286 | -0.459 | -3.213 | 0.024 |
| JJSF | 3 | 0 | -1.000 | -3.000 | -0.049 |
| FSS | 5 | 0.400 | -0.584 | -2.920 | 0.014 |
| PFS | 4 | 0 | -0.726 | -2.903 | -0.016 |
| HZO | 2 | 0 | -1.444 | -2.889 | -0.178 |
| HASI | 4 | 0.250 | -0.720 | -2.881 | 0.040 |
| UCB | 3 | 0 | -0.885 | -2.654 | -0.077 |
| PAHC | 3 | 0.333 | -0.876 | -2.629 | -0.015 |
| VRTS | 5 | 0.200 | -0.482 | -2.412 | 0.032 |
| FBP | 3 | 0 | -0.804 | -2.411 | -0.027 |
| SAH | 2 | 1.000 | 1.650 | 3.300 | 0.077 |
| CENT | 5 | 0.750 | 0.647 | 3.386 | 0.068 |
| SBCF | 3 | 0.667 | 1.161 | 3.483 | 0.117 |
| CBRL | 7 | 0.429 | 0.517 | 3.616 | 0.036 |
| DEA | 4 | 1.000 | 0.916 | 3.663 | 0.040 |
| LKFN | 3 | 1.000 | 1.254 | 3.761 | 0.108 |
| DORM | 5 | 0.800 | 0.761 | 3.807 | 0.031 |
| RUSHA | 3 | 1.000 | 1.295 | 3.886 | 0.087 |
| GSHD | 1 | 1.000 | 4.106 | 4.106 | 0.414 |
| APLE | 5 | 0.800 | 0.839 | 4.197 | 0.075 |
| NBHC | 6 | 0.667 | 0.744 | 4.462 | 0.076 |
| GRBK | 3 | 1.000 | 1.574 | 4.723 | 0.128 |
| NIC | 5 | 0.800 | 0.970 | 4.851 | 0.052 |
| DCOM | 5 | 1.000 | 1.104 | 5.522 | 0.059 |
| NPK | 5 | 0.800 | 1.173 | 5.867 | 0.064 |
