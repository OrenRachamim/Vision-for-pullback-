# Pullback scanner - backtest report (`pullback_scanner.py`)

* tickers: 558 / 590 | period: 2016-01-01 -> today
* entry: next open | stop: base_lo | target: 2.0R | max hold: 10 days | dedupe cooldown: 5 bars | combo: daily signal within 15 days after a weekly signal
* baseline = every trading day of the same tickers, same period (1,426,819 days)

## 1. Forward returns vs baseline (next open -> close t+h)

| group / horizon | n | mean | median | pct_up | t_vs_base | p |
|---|---|---|---|---|---|---|
| baseline 5d | 1,423,869 | 0.003 | 0.002 | 0.517 |  |  |
| daily 5d | 4,973 | 0.001 | 0.001 | 0.506 | -2.494 | 0.013 |
| weekly 5d | 272 | 0.000 | 0.002 | 0.533 | -1.237 | 0.216 |
| BUY SIGNAL (daily+weekly) 5d | 27 | 0.001 | 0.007 | 0.630 | -0.259 | 0.796 |
| combo 5d | 47 | 0.003 | 0.007 | 0.617 | -0.074 | 0.941 |
| baseline 10d | 1,420,919 | 0.006 | 0.004 | 0.527 |  |  |
| daily 10d | 4,962 | 0.004 | 0.003 | 0.527 | -2.258 | 0.024 |
| weekly 10d | 272 | -0.001 | -0.003 | 0.474 | -2.000 | 0.046 |
| BUY SIGNAL (daily+weekly) 10d | 27 | -0.008 | 0.000 | 0.519 | -1.900 | 0.057 |
| combo 10d | 47 | -0.002 | 0.004 | 0.532 | -1.273 | 0.203 |
| baseline 20d | 1,415,019 | 0.013 | 0.008 | 0.538 |  |  |
| daily 20d | 4,953 | 0.010 | 0.008 | 0.541 | -2.524 | 0.012 |
| weekly 20d | 272 | -0.001 | -0.008 | 0.445 | -2.933 | 0.003 |
| BUY SIGNAL (daily+weekly) 20d | 27 | -0.021 | -0.021 | 0.407 | -3.129 | 0.002 |
| combo 20d | 47 | -0.012 | 0.003 | 0.511 | -2.363 | 0.018 |
| baseline 60d | 1,391,419 | 0.041 | 0.025 | 0.563 |  |  |
| daily 60d | 4,912 | 0.021 | 0.021 | 0.557 | -8.472 | 0.000 |
| weekly 60d | 271 | -0.007 | 0.003 | 0.517 | -5.599 | 0.000 |
| BUY SIGNAL (daily+weekly) 60d | 27 | -0.002 | 0.031 | 0.556 | -1.840 | 0.066 |
| combo 60d | 47 | 0.016 | 0.035 | 0.574 | -1.307 | 0.191 |

> p is a normal-approx Welch test. Baseline days overlap, so treat p as optimistic.

## 2. Trade simulation with the scanner's own levels

| group | n | trades | win_rate | avg_R | R_ci95 | profit_factor | avg_risk_pct | stopped | hit_target | gap_below_stop | total_R |
|---|---|---|---|---|---|---|---|---|---|---|---|
| daily | 4976 | 4921 | 0.472 | 0.039 | [0.01, 0.07] | 1.098 | 0.059 | 0.314 | 0.102 | 0.009 | 195.424 |
| weekly | 273 | 272 | 0.474 | 0.040 | [-0.06, 0.13] | 1.140 | 0.070 | 0.161 | 0.055 | 0 | 11.039 |
| BUY SIGNAL (daily+weekly) | 27 | 27 | 0.556 | 0.048 | [-0.17, 0.29] | 1.240 | 0.079 | 0.111 | 0.037 | 0 | 1.309 |
| combo | 47 | 47 | 0.532 | 0.012 | [-0.20, 0.24] | 1.039 | 0.065 | 0.213 | 0.021 | 0 | 0.547 |
| CONTROL: random days, same exits | 475467 | 474225 | 0.459 | 0.036 | [0.03, 0.04] | 1.085 | 0.065 | 0.351 | 0.132 | 0 | 17388.115 |

> CONTROL = same entry/stop/target/time rules on every 3rd trading day of the same tickers,
> stop distance drawn from the tested signals' risk distribution. The pattern adds value
> only if its avg_R is clearly above the control's.

* daily vs CONTROL: avg_R diff = +0.003R, t = 0.21, p = 0.831
* weekly vs CONTROL: avg_R diff = +0.003R, t = 0.07, p = 0.943
* BUY SIGNAL (daily+weekly) vs CONTROL: avg_R diff = +0.012R, t = 0.10, p = 0.920
* combo vs CONTROL: avg_R diff = -0.025R, t = -0.22, p = 0.823

## 3. Combo signals split by score and by each component

| split | n | trades | win_rate | avg_R | R_ci95 | profit_factor | fwd20 |
|---|---|---|---|---|---|---|---|
| score=25 | 6 | 6 | 0.333 | -0.020 | [-0.36, 0.37] | 0.913 | -0.013 |
| score=50 | 24 | 24 | 0.625 | 0.202 | [-0.12, 0.54] | 1.825 | -0.006 |
| score=75 | 14 | 14 | 0.500 | -0.200 | [-0.53, 0.13] | 0.470 | -0.033 |
| score=100 | 3 | 3 | 0.333 | -0.459 | [nan, nan] | 0.118 | 0.032 |
| slowing=True | 27 | 27 | 0.593 | -0.020 | [-0.28, 0.20] | 0.926 | -0.014 |
| slowing=False | 20 | 20 | 0.450 | 0.055 | [-0.30, 0.44] | 1.166 | -0.010 |
| drying=True | 6 | 6 | 0.333 | -0.367 | [-0.84, 0.08] | 0.159 | -0.028 |
| drying=False | 41 | 41 | 0.561 | 0.067 | [-0.17, 0.29] | 1.240 | -0.010 |
| uptrend=True | 28 | 28 | 0.500 | -0.076 | [-0.38, 0.25] | 0.806 | -0.008 |
| uptrend=False | 19 | 19 | 0.579 | 0.141 | [-0.10, 0.38] | 1.881 | -0.019 |

Phase lengths found by detect() (bars):

| phase | mean | min | 50% | max |
|---|---|---|---|---|
| decline_len | 16.511 | 3.000 | 14 | 40 |
| slowdown_len | 15.957 | 0 | 13 | 47 |
| base_len | 7.255 | 3.000 | 8.000 | 10 |
| peak_to_low | 26.383 | 5.000 | 31 | 40 |
| base_above_low | 0.011 | 0 | 0.010 | 0.029 |

## 4. Combo signals per year

| year | n | win_rate | avg_R | total_R | fwd20 |
|---|---|---|---|---|---|
| 2016 | 7 | 0.571 | -0.084 | -0.588 | 0.012 |
| 2017 | 9 | 0.667 | 0.353 | 3.177 | -0.008 |
| 2018 | 7 | 0.286 | -0.263 | -1.843 | -0.023 |
| 2019 | 3 | 0.667 | -0.187 | -0.561 | -0.008 |
| 2020 | 1 | 0 | -1.000 | -1.000 | -0.194 |
| 2021 | 2 | 1.000 | 1.243 | 2.487 | -0.054 |
| 2023 | 6 | 0.500 | -0.145 | -0.872 | -0.017 |
| 2024 | 2 | 0.500 | 0.181 | 0.362 | -0.036 |
| 2025 | 8 | 0.375 | -0.133 | -1.060 | -0.009 |
| 2026 | 2 | 1.000 | 0.223 | 0.446 | 0.068 |

## 5. Combo signals per ticker (15 worst and 15 best by total_R)

| ticker | n | win_rate | avg_R | total_R | fwd20 |
|---|---|---|---|---|---|
| FLO | 2 | 0 | -1.000 | -2.000 | -0.139 |
| NIC | 1 | 0 | -1.250 | -1.250 | 0.047 |
| ABR | 1 | 0 | -1.000 | -1.000 | 0.034 |
| WABC | 1 | 0 | -1.000 | -1.000 | -0.031 |
| BKU | 1 | 0 | -1.000 | -1.000 | -0.105 |
| SBSI | 1 | 0 | -1.000 | -1.000 | 0.014 |
| CPF | 1 | 0 | -1.000 | -1.000 | -0.072 |
| MTRN | 1 | 0 | -1.000 | -1.000 | -0.044 |
| HCSG | 1 | 0 | -1.000 | -1.000 | -0.136 |
| CNS | 2 | 0 | -0.419 | -0.838 | -0.034 |
| SBCF | 1 | 0 | -0.786 | -0.786 | -0.072 |
| AMSF | 1 | 0 | -0.469 | -0.469 | 0.020 |
| TFIN | 1 | 0 | -0.449 | -0.449 | -0.127 |
| HSTM | 2 | 0 | -0.196 | -0.392 | 0.017 |
| WU | 1 | 0 | -0.352 | -0.352 | -0.005 |
| DEA | 1 | 1.000 | 0.401 | 0.401 | 0.025 |
| WEN | 1 | 1.000 | 0.424 | 0.424 | -0.007 |
| AGO | 1 | 1.000 | 0.444 | 0.444 | 0.012 |
| HTLD | 1 | 1.000 | 0.487 | 0.487 | 0.005 |
| SPNT | 1 | 1.000 | 0.636 | 0.636 | 0.021 |
| SXT | 1 | 1.000 | 0.760 | 0.760 | 0.031 |
| REYN | 1 | 1.000 | 0.781 | 0.781 | 0.033 |
| TRNO | 1 | 1.000 | 0.812 | 0.812 | 0.055 |
| MKTX | 1 | 1.000 | 0.890 | 0.890 | -0.046 |
| FFBC | 1 | 1.000 | 0.905 | 0.905 | -0.011 |
| NPK | 1 | 1.000 | 1.038 | 1.038 | 0.152 |
| OSIS | 1 | 1.000 | 1.050 | 1.050 | 0.070 |
| WINA | 1 | 1.000 | 1.058 | 1.058 | 0.113 |
| MSGS | 1 | 1.000 | 1.308 | 1.308 | 0.123 |
| TR | 1 | 1.000 | 2.000 | 2.000 | -0.114 |
