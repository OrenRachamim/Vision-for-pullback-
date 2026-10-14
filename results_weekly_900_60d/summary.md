# Pullback scanner - backtest report (`pullback_scanner.py`)

* tickers: 331 / 898 | period: 2016-01-01 -> today
* entry: next open | stop: base_lo | target: 3.0R | max hold: 60 days | dedupe cooldown: 5 bars
* baseline = every trading day of the same tickers, same period (2,291,105 days)

## 1. Forward returns vs baseline (next open -> close t+h)

| group / horizon | n | mean | median | pct_up | t_vs_base | p |
|---|---|---|---|---|---|---|
| baseline 5d | 2,286,615 | 0.004 | 0.003 | 0.538 |  |  |
| weekly 5d | 524 | -0.001 | -0.001 | 0.483 | -3.283 | 0.001 |
| baseline 10d | 2,282,125 | 0.008 | 0.006 | 0.552 |  |  |
| weekly 10d | 524 | 0.000 | 0.000 | 0.502 | -4.089 | 0.000 |
| baseline 20d | 2,273,145 | 0.017 | 0.012 | 0.568 |  |  |
| weekly 20d | 523 | 0.003 | 0.009 | 0.570 | -4.548 | 0.000 |
| baseline 60d | 2,237,225 | 0.051 | 0.036 | 0.607 |  |  |
| weekly 60d | 521 | 0.004 | 0.016 | 0.582 | -7.693 | 0.000 |

> p is a normal-approx Welch test. Baseline days overlap, so treat p as optimistic.

## 2. Trade simulation with the scanner's own levels

| group | n | trades | win_rate | avg_R | R_ci95 | profit_factor | avg_risk_pct | stopped | hit_target | gap_below_stop | total_R |
|---|---|---|---|---|---|---|---|---|---|---|---|
| weekly | 526 | 524 | 0.456 | 0.196 | [0.07, 0.31] | 1.381 | 0.067 | 0.477 | 0.106 | 0 | 103.550 |
| CONTROL: random days, same exits | 763445 | 756894 | 0.407 | 0.221 | [0.22, 0.22] | 1.377 | 0.067 | 0.541 | 0.179 | 0 | 169657.151 |

> CONTROL = same entry/stop/target/time rules on every 3rd trading day of the same tickers,
> stop distance drawn from the tested signals' risk distribution. The pattern adds value
> only if its avg_R is clearly above the control's.

* weekly vs CONTROL: avg_R diff = -0.025R, t = -0.39, p = 0.695

## 3. Weekly signals split by score and by each component

| split | n | trades | win_rate | avg_R | R_ci95 | profit_factor | fwd20 |
|---|---|---|---|---|---|---|---|
| score=25 | 116 | 115 | 0.400 | 0.047 | [-0.21, 0.31] | 1.081 | 0.002 |
| score=50 | 218 | 218 | 0.482 | 0.357 | [0.15, 0.58] | 1.714 | -0.002 |
| score=75 | 145 | 144 | 0.472 | 0.110 | [-0.09, 0.32] | 1.225 | 0.014 |
| score=100 | 47 | 47 | 0.426 | 0.077 | [-0.28, 0.48] | 1.153 | 0.004 |
| slowing=True | 290 | 289 | 0.460 | 0.227 | [0.07, 0.40] | 1.450 | 0.005 |
| slowing=False | 236 | 235 | 0.451 | 0.158 | [-0.02, 0.34] | 1.299 | 0.002 |
| drying=True | 142 | 142 | 0.366 | 0.009 | [-0.22, 0.26] | 1.015 | 0.000 |
| drying=False | 384 | 382 | 0.490 | 0.266 | [0.12, 0.41] | 1.552 | 0.005 |
| uptrend=True | 217 | 216 | 0.537 | 0.247 | [0.09, 0.42] | 1.605 | 0.012 |
| uptrend=False | 309 | 308 | 0.399 | 0.160 | [-0.03, 0.35] | 1.272 | -0.002 |

Phase lengths found by detect() (bars):

| phase | mean | min | 50% | max |
|---|---|---|---|---|
| decline_len | 14.462 | 2.000 | 12 | 53 |
| slowdown_len | 9.625 | 0 | 7.000 | 53 |
| base_len | 2.639 | 2.000 | 2.000 | 6.000 |

## 4. Weekly signals per year

| year | n | win_rate | avg_R | total_R | fwd20 |
|---|---|---|---|---|---|
| 2016 | 41 | 0.659 | 0.578 | 23.683 | 0.033 |
| 2017 | 87 | 0.644 | 0.431 | 37.506 | 0.003 |
| 2018 | 65 | 0.462 | 0.178 | 11.580 | -0.016 |
| 2019 | 42 | 0.476 | 0.337 | 14.169 | 0.023 |
| 2020 | 17 | 0.118 | -0.743 | -12.634 | -0.028 |
| 2021 | 33 | 0.485 | 0.468 | 15.459 | 0.019 |
| 2022 | 12 | 0.167 | -0.374 | -4.489 | -0.009 |
| 2023 | 78 | 0.359 | 0.043 | 3.322 | -0.005 |
| 2024 | 43 | 0.465 | 0.397 | 17.060 | 0.008 |
| 2025 | 67 | 0.299 | -0.189 | -12.676 | -0.010 |
| 2026 | 41 | 0.462 | 0.251 | 10.571 | 0.025 |

## 5. Weekly signals per ticker (15 worst and 15 best by total_R)

| ticker | n | win_rate | avg_R | total_R | fwd20 |
|---|---|---|---|---|---|
| TXNM | 3 | 0 | -1.626 | -4.879 | -0.017 |
| AIG | 5 | 0 | -0.964 | -4.820 | -0.054 |
| AMCR | 4 | 0 | -1.000 | -4.000 | 0.013 |
| HSIC | 6 | 0.333 | -0.581 | -3.485 | -0.035 |
| AOS | 3 | 0 | -1.045 | -3.136 | -0.145 |
| ZBH | 3 | 0 | -1.000 | -3.000 | 0.022 |
| XOM | 3 | 0 | -1.000 | -3.000 | -0.032 |
| ROP | 2 | 0 | -1.416 | -2.832 | -0.123 |
| PNW | 2 | 0 | -1.249 | -2.498 | 0.005 |
| SR | 2 | 0 | -1.070 | -2.139 | -0.070 |
| SSB | 2 | 0 | -1.070 | -2.139 | -0.052 |
| SUI | 2 | 0 | -1.047 | -2.094 | -0.018 |
| FBIN | 2 | 0 | -1.045 | -2.089 | -0.074 |
| NWSA | 2 | 0 | -1.027 | -2.053 | -0.003 |
| CVS | 3 | 0 | -0.679 | -2.038 | -0.024 |
| LIN | 2 | 1.000 | 2.139 | 4.279 | 0.054 |
| SCI | 2 | 1.000 | 2.181 | 4.361 | 0.059 |
| STZ | 2 | 1.000 | 2.199 | 4.397 | 0.007 |
| FTV | 2 | 1.000 | 2.205 | 4.410 | 0.058 |
| CLH | 2 | 1.000 | 2.211 | 4.422 | 0.080 |
| D | 3 | 1.000 | 1.520 | 4.561 | 0.042 |
| AMGN | 2 | 1.000 | 2.338 | 4.676 | 0.128 |
| KHC | 4 | 0.750 | 1.187 | 4.749 | 0.024 |
| LLY | 2 | 1.000 | 2.444 | 4.889 | 0.056 |
| HUBB | 4 | 0.750 | 1.448 | 5.792 | 0.006 |
| CASY | 2 | 1.000 | 3.000 | 6.000 | 0.064 |
| MO | 2 | 1.000 | 3.014 | 6.028 | 0.024 |
| WM | 3 | 1.000 | 2.335 | 7.005 | 0.085 |
| RPM | 3 | 1.000 | 2.602 | 7.807 | 0.073 |
| FFIV | 3 | 1.000 | 3.076 | 9.228 | 0.008 |
