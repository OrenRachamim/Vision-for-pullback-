# Pullback scanner - backtest report (`pullback_scanner.py`)

* tickers: 558 / 590 | period: 2016-01-01 -> today
* entry: next open | stop: base_lo | exit: trailing stop 3.0*ATR14 from highest high, no target | max hold: 60 days | dedupe cooldown: 5 bars | combo: daily signal within 15 days after a weekly signal
* baseline = every trading day of the same tickers, same period (1,426,819 days)

## 1. Forward returns vs baseline (next open -> close t+h)

| group / horizon | n | mean | median | pct_up | t_vs_base | p |
|---|---|---|---|---|---|---|
| baseline 5d | 1,423,869 | 0.003 | 0.002 | 0.517 |  |  |
| daily 5d | 4,973 | 0.001 | 0.001 | 0.506 | -2.494 | 0.013 |
| weekly 5d | 272 | 0.000 | 0.002 | 0.533 | -1.237 | 0.216 |
| BUY SIGNAL (daily+weekly) 5d | 27 | 0.001 | 0.007 | 0.630 | -0.259 | 0.796 |
| combo 5d | 28 | 0.008 | 0.009 | 0.643 | 0.828 | 0.407 |
| baseline 10d | 1,420,919 | 0.006 | 0.004 | 0.527 |  |  |
| daily 10d | 4,962 | 0.004 | 0.003 | 0.527 | -2.258 | 0.024 |
| weekly 10d | 272 | -0.001 | -0.003 | 0.474 | -2.000 | 0.046 |
| BUY SIGNAL (daily+weekly) 10d | 27 | -0.008 | 0.000 | 0.519 | -1.900 | 0.057 |
| combo 10d | 28 | -0.006 | -0.001 | 0.500 | -1.173 | 0.241 |
| baseline 20d | 1,415,019 | 0.013 | 0.008 | 0.538 |  |  |
| daily 20d | 4,953 | 0.010 | 0.008 | 0.541 | -2.524 | 0.012 |
| weekly 20d | 272 | -0.001 | -0.008 | 0.445 | -2.933 | 0.003 |
| BUY SIGNAL (daily+weekly) 20d | 27 | -0.021 | -0.021 | 0.407 | -3.129 | 0.002 |
| combo 20d | 28 | -0.008 | 0.000 | 0.500 | -1.379 | 0.168 |
| baseline 60d | 1,391,419 | 0.041 | 0.025 | 0.563 |  |  |
| daily 60d | 4,912 | 0.021 | 0.021 | 0.557 | -8.472 | 0.000 |
| weekly 60d | 271 | -0.007 | 0.003 | 0.517 | -5.599 | 0.000 |
| BUY SIGNAL (daily+weekly) 60d | 27 | -0.002 | 0.031 | 0.556 | -1.840 | 0.066 |
| combo 60d | 28 | 0.020 | 0.036 | 0.607 | -0.809 | 0.419 |

> p is a normal-approx Welch test. Baseline days overlap, so treat p as optimistic.

## 2. Trade simulation with the scanner's own levels

| group | n | trades | win_rate | avg_R | R_ci95 | profit_factor | avg_risk_pct | stopped | trailed | hit_target | gap_below_stop | total_R |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| daily | 4976 | 4915 | 0.357 | 0.074 | [0.03, 0.12] | 1.154 | 0.059 | 0.246 | 0.725 | 0 | 0.009 | 368.326 |
| weekly | 273 | 272 | 0.357 | 0.017 | [-0.12, 0.16] | 1.046 | 0.070 | 0.088 | 0.897 | 0 | 0 | 4.789 |
| BUY SIGNAL (daily+weekly) | 27 | 27 | 0.407 | 0.113 | [-0.19, 0.46] | 1.492 | 0.079 | 0.037 | 0.926 | 0 | 0 | 3.053 |
| combo | 28 | 28 | 0.393 | -0.059 | [-0.39, 0.30] | 0.851 | 0.069 | 0.214 | 0.786 | 0 | 0 | -1.648 |
| CONTROL: random days, same exits | 271395 | 270045 | 0.327 | 0.028 | [0.02, 0.04] | 1.058 | 0.069 | 0.278 | 0.704 | 0 | 0 | 8725.675 |

> CONTROL = same entry/stop/target/time rules on every 3rd trading day of the same tickers,
> stop distance drawn from the tested signals' risk distribution. The pattern adds value
> only if its avg_R is clearly above the control's.

* daily vs CONTROL: avg_R diff = +0.046R, t = 1.93, p = 0.054
* weekly vs CONTROL: avg_R diff = -0.011R, t = -0.17, p = 0.867
* BUY SIGNAL (daily+weekly) vs CONTROL: avg_R diff = +0.085R, t = 0.51, p = 0.612
* combo vs CONTROL: avg_R diff = -0.087R, t = -0.48, p = 0.634

> require-uptrend: buy only when price > SMA200; CONTROL also samples only days with price > SMA200.

## 3. Combo signals split by score and by each component

| split | n | trades | win_rate | avg_R | R_ci95 | profit_factor | fwd20 |
|---|---|---|---|---|---|---|---|
| score=50 | 14 | 14 | 0.429 | 0.046 | [-0.43, 0.62] | 1.125 | -0.009 |
| score=75 | 11 | 11 | 0.364 | -0.239 | [-0.59, 0.18] | 0.412 | -0.018 |
| score=100 | 3 | 3 | 0.333 | 0.111 | [nan, nan] | 1.233 | 0.032 |
| slowing=True | 14 | 14 | 0.357 | -0.164 | [-0.58, 0.29] | 0.611 | -0.007 |
| slowing=False | 14 | 14 | 0.429 | 0.046 | [-0.43, 0.62] | 1.125 | -0.009 |
| drying=True | 3 | 3 | 0.333 | 0.111 | [nan, nan] | 1.233 | 0.032 |
| drying=False | 25 | 25 | 0.400 | -0.079 | [-0.42, 0.27] | 0.794 | -0.013 |
| uptrend=True | 28 | 28 | 0.393 | -0.059 | [-0.39, 0.30] | 0.851 | -0.008 |

Phase lengths found by detect() (bars):

| phase | mean | min | 50% | max |
|---|---|---|---|---|
| decline_len | 14.036 | 3.000 | 11 | 35 |
| slowdown_len | 14.786 | 0 | 11.500 | 47 |
| base_len | 7.286 | 3.000 | 8.000 | 10 |
| peak_to_low | 22.679 | 5.000 | 21.500 | 40 |
| base_above_low | 0.009 | 0 | 0.007 | 0.025 |

## 4. Combo signals per year

| year | n | win_rate | avg_R | total_R | fwd20 |
|---|---|---|---|---|---|
| 2016 | 6 | 0.500 | 0.089 | 0.533 | 0.042 |
| 2017 | 4 | 0.500 | 0.312 | 1.248 | 0.016 |
| 2018 | 6 | 0.333 | -0.355 | -2.133 | -0.021 |
| 2019 | 2 | 0.500 | -0.268 | -0.536 | -0.028 |
| 2020 | 1 | 0 | -1.000 | -1.000 | -0.194 |
| 2021 | 1 | 1.000 | 1.374 | 1.374 | -0.114 |
| 2023 | 3 | 0 | -0.236 | -0.708 | -0.010 |
| 2024 | 1 | 0 | -1.000 | -1.000 | -0.127 |
| 2025 | 3 | 0.333 | -0.394 | -1.182 | 0.005 |
| 2026 | 1 | 1.000 | 1.755 | 1.755 | 0.085 |

## 5. Combo signals per ticker

| ticker | n | win_rate | avg_R | total_R | fwd20 |
|---|---|---|---|---|---|
| NIC | 1 | 0 | -1.250 | -1.250 | 0.047 |
| ABR | 1 | 0 | -1.000 | -1.000 | 0.034 |
| SBSI | 1 | 0 | -1.000 | -1.000 | 0.014 |
| MTRN | 1 | 0 | -1.000 | -1.000 | -0.044 |
| TFIN | 1 | 0 | -1.000 | -1.000 | -0.127 |
| FLO | 1 | 0 | -1.000 | -1.000 | -0.194 |
| WABC | 1 | 0 | -0.938 | -0.938 | -0.031 |
| CPF | 1 | 0 | -0.744 | -0.744 | -0.072 |
| BKU | 1 | 0 | -0.668 | -0.668 | -0.105 |
| HCSG | 1 | 0 | -0.631 | -0.631 | -0.136 |
| TMP | 1 | 0 | -0.471 | -0.471 | -0.024 |
| BRC | 1 | 0 | -0.445 | -0.445 | 0.033 |
| SBCF | 1 | 0 | -0.392 | -0.392 | -0.072 |
| HSTM | 1 | 0 | -0.203 | -0.203 | 0.016 |
| BMI | 1 | 0 | -0.173 | -0.173 | -0.037 |
| OUT | 1 | 0 | -0.088 | -0.088 | -0.038 |
| TNC | 1 | 0 | -0.035 | -0.035 | -0.021 |
| FFBC | 1 | 1.000 | 0.057 | 0.057 | -0.011 |
| CAG | 1 | 1.000 | 0.061 | 0.061 | 0.024 |
| DEA | 1 | 1.000 | 0.131 | 0.131 | 0.025 |
| WDFC | 1 | 1.000 | 0.132 | 0.132 | 0.049 |
| AGO | 1 | 1.000 | 0.201 | 0.201 | 0.012 |
| OSIS | 1 | 1.000 | 0.402 | 0.402 | 0.070 |
| MSGS | 1 | 1.000 | 1.186 | 1.186 | 0.123 |
| TR | 1 | 1.000 | 1.374 | 1.374 | -0.114 |
| WINA | 1 | 1.000 | 1.378 | 1.378 | 0.113 |
| CWT | 1 | 1.000 | 1.755 | 1.755 | 0.085 |
| NPK | 1 | 1.000 | 2.712 | 2.712 | 0.152 |
