# Pullback scanner - backtest report (`pullback_scanner.py`)

* tickers: 560 / 590 | period: 2016-01-01 -> today
* entry: next open | stop: base_lo | target: 2.0R | max hold: 20 days | dedupe cooldown: 5 bars | combo: daily signal within 15 days after a weekly signal
* baseline = every trading day of the same tickers, same period (1,426,819 days)

## 1. Forward returns vs baseline (next open -> close t+h)

| group / horizon | n | mean | median | pct_up | t_vs_base | p |
|---|---|---|---|---|---|---|
| baseline 5d | 1,423,869 | 0.003 | 0.002 | 0.517 |  |  |
| daily 5d | 5,189 | -0.000 | -0.001 | 0.482 | -4.748 | 0.000 |
| weekly 5d | 264 | -0.002 | 0.002 | 0.519 | -1.796 | 0.073 |
| BUY SIGNAL (daily+weekly) 5d | 33 | -0.004 | 0.000 | 0.515 | -1.550 | 0.121 |
| combo 5d | 36 | 0.004 | 0.002 | 0.528 | 0.278 | 0.781 |
| baseline 10d | 1,420,919 | 0.006 | 0.004 | 0.527 |  |  |
| daily 10d | 5,185 | 0.004 | 0.002 | 0.516 | -2.823 | 0.005 |
| weekly 10d | 264 | 0.000 | -0.001 | 0.492 | -1.683 | 0.092 |
| BUY SIGNAL (daily+weekly) 10d | 33 | 0.004 | 0.011 | 0.576 | -0.275 | 0.783 |
| combo 10d | 36 | 0.011 | 0.010 | 0.611 | 0.505 | 0.614 |
| baseline 20d | 1,415,019 | 0.013 | 0.008 | 0.538 |  |  |
| daily 20d | 5,175 | 0.010 | 0.009 | 0.542 | -2.163 | 0.031 |
| weekly 20d | 264 | 0.000 | -0.007 | 0.451 | -2.490 | 0.013 |
| BUY SIGNAL (daily+weekly) 20d | 33 | -0.004 | -0.005 | 0.485 | -1.171 | 0.242 |
| combo 20d | 36 | 0.018 | 0.019 | 0.639 | 0.346 | 0.729 |
| baseline 60d | 1,391,419 | 0.041 | 0.025 | 0.563 |  |  |
| daily 60d | 5,134 | 0.020 | 0.020 | 0.556 | -9.179 | 0.000 |
| weekly 60d | 263 | -0.009 | 0.005 | 0.529 | -5.484 | 0.000 |
| BUY SIGNAL (daily+weekly) 60d | 33 | -0.015 | 0.003 | 0.515 | -2.156 | 0.031 |
| combo 60d | 36 | 0.026 | 0.038 | 0.667 | -0.612 | 0.540 |

> p is a normal-approx Welch test. Baseline days overlap, so treat p as optimistic.

## 2. Trade simulation with the scanner's own levels

| group | n | trades | win_rate | avg_R | R_ci95 | profit_factor | avg_risk_pct | stopped | hit_target | gap_below_stop | total_R |
|---|---|---|---|---|---|---|---|---|---|---|---|
| daily | 5192 | 5138 | 0.440 | 0.052 | [0.02, 0.09] | 1.104 | 0.059 | 0.440 | 0.185 | 0.009 | 271.171 |
| weekly | 264 | 264 | 0.443 | 0.028 | [-0.10, 0.15] | 1.070 | 0.071 | 0.295 | 0.110 | 0 | 7.399 |
| BUY SIGNAL (daily+weekly) | 33 | 33 | 0.515 | 0.131 | [-0.20, 0.47] | 1.393 | 0.067 | 0.273 | 0.121 | 0 | 4.334 |
| combo | 36 | 36 | 0.556 | 0.208 | [-0.16, 0.56] | 1.540 | 0.062 | 0.361 | 0.194 | 0 | 7.474 |
| CONTROL: random days, same exits | 271395 | 270327 | 0.426 | 0.032 | [0.03, 0.04] | 1.061 | 0.062 | 0.460 | 0.194 | 0 | 8782.856 |

> CONTROL = same entry/stop/target/time rules on every 3rd trading day of the same tickers,
> stop distance drawn from the tested signals' risk distribution. The pattern adds value
> only if its avg_R is clearly above the control's.

* daily vs CONTROL: avg_R diff = +0.021R, t = 1.20, p = 0.229
* weekly vs CONTROL: avg_R diff = -0.004R, t = -0.06, p = 0.954
* BUY SIGNAL (daily+weekly) vs CONTROL: avg_R diff = +0.100R, t = 0.57, p = 0.570
* combo vs CONTROL: avg_R diff = +0.176R, t = 0.91, p = 0.363

> require-uptrend: buy only when price > SMA200; CONTROL also samples only days with price > SMA200.

## 3. Combo signals split by score and by each component

| split | n | trades | win_rate | avg_R | R_ci95 | profit_factor | fwd20 |
|---|---|---|---|---|---|---|---|
| score=50 | 14 | 14 | 0.500 | 0.131 | [-0.47, 0.77] | 1.292 | 0.004 |
| score=75 | 18 | 18 | 0.556 | 0.154 | [-0.32, 0.65] | 1.440 | 0.018 |
| score=100 | 4 | 4 | 0.750 | 0.715 | [nan, nan] | 3.290 | 0.067 |
| slowing=True | 22 | 22 | 0.591 | 0.256 | [-0.21, 0.73] | 1.746 | 0.027 |
| slowing=False | 14 | 14 | 0.500 | 0.131 | [-0.47, 0.77] | 1.292 | 0.004 |
| drying=True | 4 | 4 | 0.750 | 0.715 | [nan, nan] | 3.290 | 0.067 |
| drying=False | 32 | 32 | 0.531 | 0.144 | [-0.24, 0.54] | 1.366 | 0.012 |
| uptrend=True | 36 | 36 | 0.556 | 0.208 | [-0.16, 0.56] | 1.540 | 0.018 |

Phase lengths found by detect() (bars):

| phase | mean | min | 50% | max |
|---|---|---|---|---|
| decline_len | 14.278 | 3.000 | 11 | 35 |
| slowdown_len | 15.861 | 0 | 12.500 | 47 |
| base_len | 6.806 | 3.000 | 7.000 | 10 |
| peak_to_low | 24.083 | 5.000 | 24 | 40 |
| base_above_low | 0.011 | 0 | 0.012 | 0.028 |

## 4. Combo signals per year

| year | n | win_rate | avg_R | total_R | fwd20 |
|---|---|---|---|---|---|
| 2016 | 7 | 0.571 | 0.062 | 0.431 | 0.043 |
| 2017 | 5 | 0.800 | 0.979 | 4.893 | 0.047 |
| 2018 | 6 | 0.167 | -0.500 | -3.000 | -0.021 |
| 2019 | 4 | 0.750 | -0.091 | -0.366 | -0.011 |
| 2020 | 1 | 0 | -1.000 | -1.000 | -0.194 |
| 2021 | 1 | 0 | -0.178 | -0.178 | -0.008 |
| 2023 | 2 | 0 | -0.566 | -1.132 | -0.022 |
| 2024 | 6 | 0.833 | 1.093 | 6.556 | 0.073 |
| 2025 | 3 | 0.667 | -0.058 | -0.175 | 0.005 |
| 2026 | 1 | 1.000 | 1.445 | 1.445 | 0.085 |

## 5. Combo signals per ticker

| ticker | n | win_rate | avg_R | total_R | fwd20 |
|---|---|---|---|---|---|
| NIC | 1 | 0 | -1.250 | -1.250 | 0.047 |
| ABR | 1 | 0 | -1.000 | -1.000 | 0.034 |
| MTRN | 1 | 0 | -1.000 | -1.000 | -0.044 |
| SBCF | 1 | 0 | -1.000 | -1.000 | -0.072 |
| SBSI | 1 | 0 | -1.000 | -1.000 | 0.014 |
| HCSG | 1 | 0 | -1.000 | -1.000 | -0.136 |
| FLO | 1 | 0 | -1.000 | -1.000 | -0.194 |
| FFBC | 1 | 0 | -1.000 | -1.000 | -0.011 |
| TMP | 1 | 0 | -1.000 | -1.000 | -0.024 |
| TFIN | 1 | 0 | -1.000 | -1.000 | -0.127 |
| CPF | 1 | 0 | -1.000 | -1.000 | -0.072 |
| BKU | 1 | 0 | -1.000 | -1.000 | -0.105 |
| WABC | 1 | 0 | -1.000 | -1.000 | -0.031 |
| OUT | 1 | 0 | -0.273 | -0.273 | -0.038 |
| NHI | 1 | 0 | -0.178 | -0.178 | -0.008 |
| TNC | 1 | 0 | -0.132 | -0.132 | -0.021 |
| CHCO | 1 | 1.000 | 0.014 | 0.014 | 0.001 |
| SHO | 1 | 1.000 | 0.060 | 0.060 | 0.004 |
| AGO | 1 | 1.000 | 0.142 | 0.142 | 0.012 |
| NWL | 1 | 1.000 | 0.158 | 0.158 | 0.013 |
| CAG | 1 | 1.000 | 0.280 | 0.280 | 0.024 |
| WDFC | 1 | 1.000 | 0.462 | 0.462 | 0.049 |
| DEA | 1 | 1.000 | 0.499 | 0.499 | 0.025 |
| CPK | 1 | 1.000 | 0.538 | 0.538 | 0.045 |
| MC | 1 | 1.000 | 0.667 | 0.667 | 0.035 |
| BRC | 1 | 1.000 | 0.683 | 0.683 | 0.033 |
| OSIS | 1 | 1.000 | 0.863 | 0.863 | 0.070 |
| SNEX | 1 | 1.000 | 1.374 | 1.374 | 0.081 |
| CWT | 1 | 1.000 | 1.445 | 1.445 | 0.085 |
| NPK | 1 | 1.000 | 2.000 | 2.000 | 0.152 |
| MSGS | 1 | 1.000 | 2.000 | 2.000 | 0.123 |
| FULT | 1 | 1.000 | 2.000 | 2.000 | 0.175 |
| FELE | 1 | 1.000 | 2.000 | 2.000 | 0.103 |
| BANF | 1 | 1.000 | 2.000 | 2.000 | 0.234 |
| WINA | 1 | 1.000 | 2.000 | 2.000 | 0.113 |
| IVT | 1 | 1.000 | 2.122 | 2.122 | 0.073 |
