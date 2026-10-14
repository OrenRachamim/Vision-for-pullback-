# Pullback scanner - backtest report (`pullback_scanner.py`)

* tickers: 852 / 898 | period: 2022-01-01 -> today
* entry: next open | stop: base_lo | target: 2.0R | max hold: 10 days | dedupe cooldown: 5 bars | combo: daily signal within 15 days after a weekly signal
* baseline = every trading day of the same tickers, same period (1,060,379 days)

## 1. Forward returns vs baseline (next open -> close t+h)

| group / horizon | n | mean | median | pct_up | t_vs_base | p |
|---|---|---|---|---|---|---|
| baseline 5d | 1,055,889 | 0.002 | 0.002 | 0.523 |  |  |
| daily 5d | 4,197 | 0.002 | 0.001 | 0.512 | -0.700 | 0.484 |
| weekly 5d | 320 | 0.000 | 0.001 | 0.516 | -1.368 | 0.171 |
| BUY SIGNAL (daily+weekly) 5d | 31 | -0.001 | -0.000 | 0.484 | -0.822 | 0.411 |
| combo 5d | 23 | 0.006 | 0.003 | 0.565 | 0.749 | 0.454 |
| baseline 10d | 1,051,399 | 0.005 | 0.004 | 0.529 |  |  |
| daily 10d | 4,183 | 0.004 | 0.003 | 0.526 | -1.097 | 0.273 |
| weekly 10d | 320 | -0.001 | 0.001 | 0.509 | -2.214 | 0.027 |
| BUY SIGNAL (daily+weekly) 10d | 31 | 0.003 | 0.008 | 0.548 | -0.310 | 0.757 |
| combo 10d | 23 | 0.019 | 0.025 | 0.696 | 1.691 | 0.091 |
| baseline 20d | 1,042,419 | 0.011 | 0.007 | 0.534 |  |  |
| daily 20d | 4,140 | 0.012 | 0.012 | 0.565 | 0.949 | 0.343 |
| weekly 20d | 318 | 0.003 | 0.003 | 0.516 | -2.309 | 0.021 |
| BUY SIGNAL (daily+weekly) 20d | 31 | 0.004 | 0.013 | 0.548 | -0.660 | 0.509 |
| combo 20d | 22 | 0.023 | 0.027 | 0.727 | 0.956 | 0.339 |
| baseline 60d | 1,006,499 | 0.036 | 0.023 | 0.566 |  |  |
| daily 60d | 4,062 | 0.031 | 0.029 | 0.597 | -2.323 | 0.020 |
| weekly 60d | 316 | 0.007 | 0.006 | 0.525 | -4.557 | 0.000 |
| BUY SIGNAL (daily+weekly) 60d | 31 | 0.025 | 0.013 | 0.613 | -0.577 | 0.564 |
| combo 60d | 21 | 0.041 | 0.044 | 0.714 | 0.214 | 0.831 |

> p is a normal-approx Welch test. Baseline days overlap, so treat p as optimistic.

## 2. Trade simulation with the scanner's own levels

| group | n | trades | win_rate | avg_R | R_ci95 | profit_factor | avg_risk_pct | stopped | hit_target | gap_below_stop | total_R |
|---|---|---|---|---|---|---|---|---|---|---|---|
| daily | 4217 | 4147 | 0.488 | 0.057 | [0.03, 0.09] | 1.153 | 0.058 | 0.278 | 0.091 | 0.009 | 244.528 |
| weekly | 322 | 320 | 0.500 | -0.032 | [-0.12, 0.06] | 0.903 | 0.066 | 0.202 | 0.019 | 0 | -9.409 |
| BUY SIGNAL (daily+weekly) | 31 | 31 | 0.516 | -0.247 | [-0.57, 0.07] | 0.504 | 0.062 | 0.355 | 0 | 0 | -7.647 |
| combo | 23 | 23 | 0.696 | 0.119 | [-0.15, 0.37] | 1.515 | 0.071 | 0.130 | 0 | 0 | 2.743 |
| CONTROL: random days, same exits | 208290 | 207213 | 0.488 | 0.032 | [0.03, 0.04] | 1.090 | 0.071 | 0.260 | 0.074 | 0 | 6787.032 |

> CONTROL = same entry/stop/target/time rules on every 3rd trading day of the same tickers,
> stop distance drawn from the tested signals' risk distribution. The pattern adds value
> only if its avg_R is clearly above the control's.

* daily vs CONTROL: avg_R diff = +0.025R, t = 1.63, p = 0.103
* weekly vs CONTROL: avg_R diff = -0.063R, t = -1.47, p = 0.141
* BUY SIGNAL (daily+weekly) vs CONTROL: avg_R diff = -0.278R, t = -1.71, p = 0.087
* combo vs CONTROL: avg_R diff = +0.088R, t = 0.62, p = 0.534

> require-uptrend: buy only when price > SMA200; CONTROL also samples only days with price > SMA200.

## 3. Combo signals split by score and by each component

| split | n | trades | win_rate | avg_R | R_ci95 | profit_factor | fwd20 |
|---|---|---|---|---|---|---|---|
| score=50 | 5 | 5 | 0.800 | -0.008 | [-0.51, 0.36] | 0.962 | 0.029 |
| score=75 | 15 | 15 | 0.733 | 0.225 | [-0.15, 0.56] | 2.059 | 0.022 |
| score=100 | 3 | 3 | 0.333 | -0.199 | [nan, nan] | 0.475 | 0.019 |
| slowing=True | 18 | 18 | 0.667 | 0.154 | [-0.18, 0.47] | 1.643 | 0.021 |
| slowing=False | 5 | 5 | 0.800 | -0.008 | [-0.51, 0.36] | 0.962 | 0.029 |
| drying=True | 3 | 3 | 0.333 | -0.199 | [nan, nan] | 0.475 | 0.019 |
| drying=False | 20 | 20 | 0.750 | 0.167 | [-0.14, 0.44] | 1.797 | 0.023 |
| uptrend=True | 23 | 23 | 0.696 | 0.119 | [-0.15, 0.37] | 1.515 | 0.023 |

Phase lengths found by detect() (bars):

| phase | mean | min | 50% | max |
|---|---|---|---|---|
| decline_len | 15.043 | 4.000 | 13 | 32 |
| slowdown_len | 21.565 | 3.000 | 18 | 49 |
| base_len | 7.565 | 3.000 | 9.000 | 10 |
| peak_to_low | 32.435 | 15 | 35 | 40 |
| base_above_low | 0.009 | 0 | 0.010 | 0.025 |

## 4. Combo signals per year

| year | n | win_rate | avg_R | total_R | fwd20 |
|---|---|---|---|---|---|
| 2023 | 8 | 0.875 | 0.281 | 2.247 | 0.017 |
| 2024 | 4 | 0.750 | 0.350 | 1.400 | 0.015 |
| 2025 | 3 | 1.000 | 0.456 | 1.367 | 0.044 |
| 2026 | 8 | 0.375 | -0.284 | -2.271 | 0.025 |

## 5. Combo signals per ticker

| ticker | n | win_rate | avg_R | total_R | fwd20 |
|---|---|---|---|---|---|
| PSX | 1 | 0 | -1.136 | -1.136 | -0.009 |
| XYL | 1 | 0 | -1.000 | -1.000 | -0.113 |
| SUI | 1 | 0 | -1.000 | -1.000 | 0.012 |
| EGP | 1 | 0 | -0.758 | -0.758 |  |
| HII | 1 | 0 | -0.685 | -0.685 | -0.096 |
| DTE | 1 | 0 | -0.367 | -0.367 | 0.072 |
| TXRH | 1 | 1.000 | 0.008 | 0.008 | -0.050 |
| EXC | 2 | 0.500 | 0.048 | 0.096 | 0.068 |
| FTV | 1 | 1.000 | 0.129 | 0.129 | 0.076 |
| JNJ | 1 | 1.000 | 0.150 | 0.150 | 0.097 |
| WM | 1 | 1.000 | 0.245 | 0.245 | 0.023 |
| ROST | 1 | 1.000 | 0.321 | 0.321 | 0.053 |
| MKC | 1 | 1.000 | 0.454 | 0.454 | 0.047 |
| POST | 1 | 1.000 | 0.483 | 0.483 | 0.031 |
| APH | 1 | 1.000 | 0.517 | 0.517 | 0.067 |
| ACI | 1 | 1.000 | 0.518 | 0.518 | 0.035 |
| HSIC | 1 | 1.000 | 0.529 | 0.529 | 0.023 |
| JBL | 1 | 1.000 | 0.540 | 0.540 | -0.040 |
| EPR | 1 | 1.000 | 0.734 | 0.734 | 0.003 |
| VZ | 1 | 1.000 | 0.751 | 0.751 | 0.121 |
| COR | 1 | 1.000 | 0.785 | 0.785 | -0.005 |
| MO | 1 | 1.000 | 1.430 | 1.430 | 0.022 |
