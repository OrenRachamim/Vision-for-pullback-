# Pullback scanner - backtest report (`pullback_scanner.py`)

* tickers: 878 / 898 | period: 2016-01-01 -> today
* entry: next open | stop: base_lo | exit: trailing stop 3.0*ATR14 from highest high, no target | max hold: 60 days | dedupe cooldown: 5 bars | combo: daily signal within 15 days after a weekly signal
* baseline = every trading day of the same tickers, same period (2,291,105 days)

## 1. Forward returns vs baseline (next open -> close t+h)

| group / horizon | n | mean | median | pct_up | t_vs_base | p |
|---|---|---|---|---|---|---|
| baseline 5d | 2,286,615 | 0.004 | 0.003 | 0.538 |  |  |
| daily 5d | 9,165 | 0.002 | 0.002 | 0.528 | -2.678 | 0.007 |
| weekly 5d | 694 | 0.002 | 0.001 | 0.520 | -1.579 | 0.114 |
| BUY SIGNAL (daily+weekly) 5d | 61 | 0.003 | 0.003 | 0.541 | -0.184 | 0.854 |
| combo 5d | 58 | 0.005 | 0.003 | 0.534 | 0.358 | 0.721 |
| baseline 10d | 2,282,125 | 0.008 | 0.006 | 0.552 |  |  |
| daily 10d | 9,143 | 0.005 | 0.005 | 0.545 | -4.126 | 0.000 |
| weekly 10d | 694 | 0.003 | 0.004 | 0.532 | -2.780 | 0.005 |
| BUY SIGNAL (daily+weekly) 10d | 61 | 0.009 | 0.009 | 0.574 | 0.110 | 0.912 |
| combo 10d | 58 | 0.010 | 0.013 | 0.603 | 0.238 | 0.812 |
| baseline 20d | 2,273,145 | 0.017 | 0.012 | 0.568 |  |  |
| daily 20d | 9,107 | 0.011 | 0.012 | 0.573 | -5.796 | 0.000 |
| weekly 20d | 692 | 0.006 | 0.009 | 0.561 | -4.173 | 0.000 |
| BUY SIGNAL (daily+weekly) 20d | 60 | 0.012 | 0.018 | 0.600 | -0.721 | 0.471 |
| combo 20d | 58 | 0.008 | 0.020 | 0.672 | -0.814 | 0.415 |
| baseline 60d | 2,237,225 | 0.051 | 0.036 | 0.607 |  |  |
| daily 60d | 9,027 | 0.028 | 0.032 | 0.606 | -13.014 | 0.000 |
| weekly 60d | 690 | 0.005 | 0.014 | 0.562 | -8.740 | 0.000 |
| BUY SIGNAL (daily+weekly) 60d | 60 | 0.008 | 0.041 | 0.667 | -2.002 | 0.045 |
| combo 60d | 57 | 0.019 | 0.051 | 0.684 | -1.621 | 0.105 |

> p is a normal-approx Welch test. Baseline days overlap, so treat p as optimistic.

## 2. Trade simulation with the scanner's own levels

| group | n | trades | win_rate | avg_R | R_ci95 | profit_factor | avg_risk_pct | stopped | trailed | hit_target | gap_below_stop | total_R |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| daily | 9192 | 9023 | 0.397 | 0.186 | [0.14, 0.23] | 1.438 | 0.056 | 0.186 | 0.776 | 0 | 0.012 | 1706.854 |
| weekly | 696 | 693 | 0.418 | 0.162 | [0.07, 0.25] | 1.511 | 0.069 | 0.056 | 0.904 | 0 | 0 | 114.140 |
| BUY SIGNAL (daily+weekly) | 61 | 60 | 0.533 | 0.195 | [-0.02, 0.41] | 1.777 | 0.070 | 0.049 | 0.902 | 0 | 0 | 12.502 |
| combo | 58 | 58 | 0.534 | 0.407 | [0.09, 0.77] | 2.840 | 0.074 | 0.034 | 0.914 | 0 | 0 | 23.620 |
| CONTROL: random days, same exits | 489986 | 488133 | 0.386 | 0.089 | [0.08, 0.09] | 1.244 | 0.074 | 0.138 | 0.841 | 0 | 0 | 44499.268 |

> CONTROL = same entry/stop/target/time rules on every 3rd trading day of the same tickers,
> stop distance drawn from the tested signals' risk distribution. The pattern adds value
> only if its avg_R is clearly above the control's.

* daily vs CONTROL: avg_R diff = +0.097R, t = 4.44, p = 0.000
* weekly vs CONTROL: avg_R diff = +0.074R, t = 1.62, p = 0.105
* BUY SIGNAL (daily+weekly) vs CONTROL: avg_R diff = +0.107R, t = 0.95, p = 0.344
* combo vs CONTROL: avg_R diff = +0.319R, t = 1.76, p = 0.079

> require-uptrend: buy only when price > SMA200; CONTROL also samples only days with price > SMA200.

## 3. Combo signals split by score and by each component

| split | n | trades | win_rate | avg_R | R_ci95 | profit_factor | fwd20 |
|---|---|---|---|---|---|---|---|
| score=50 | 18 | 18 | 0.611 | 0.345 | [-0.06, 0.77] | 2.590 | 0.002 |
| score=75 | 35 | 35 | 0.514 | 0.468 | [-0.00, 1.04] | 3.128 | 0.016 |
| score=100 | 5 | 5 | 0.400 | 0.204 | [-0.43, 1.18] | 1.828 | -0.031 |
| slowing=True | 40 | 40 | 0.500 | 0.435 | [0.01, 0.96] | 2.949 | 0.010 |
| slowing=False | 18 | 18 | 0.611 | 0.345 | [-0.06, 0.77] | 2.590 | 0.002 |
| drying=True | 5 | 5 | 0.400 | 0.204 | [-0.43, 1.18] | 1.828 | -0.031 |
| drying=False | 53 | 53 | 0.547 | 0.426 | [0.09, 0.85] | 2.947 | 0.012 |
| uptrend=True | 58 | 58 | 0.534 | 0.407 | [0.09, 0.77] | 2.840 | 0.008 |

Phase lengths found by detect() (bars):

| phase | mean | min | 50% | max |
|---|---|---|---|---|
| decline_len | 17.121 | 4.000 | 15.500 | 36 |
| slowdown_len | 15.845 | 0 | 13.500 | 49 |
| base_len | 7.862 | 3.000 | 9.500 | 10 |
| peak_to_low | 27.879 | 6.000 | 30 | 40 |
| base_above_low | 0.011 | 0 | 0.012 | 0.030 |

## 4. Combo signals per year

| year | n | win_rate | avg_R | total_R | fwd20 |
|---|---|---|---|---|---|
| 2016 | 9 | 0.444 | 0.298 | 2.678 | 0.014 |
| 2017 | 9 | 0.333 | 0.740 | 6.656 | 0.013 |
| 2018 | 3 | 0.333 | 0.233 | 0.699 | 0.016 |
| 2019 | 2 | 0 | -0.686 | -1.373 | -0.041 |
| 2020 | 4 | 0.500 | 0.077 | 0.307 | -0.104 |
| 2021 | 6 | 0.500 | 0.588 | 3.530 | 0.014 |
| 2023 | 9 | 0.667 | 0.584 | 5.256 | 0.016 |
| 2024 | 3 | 1.000 | 0.478 | 1.433 | 0.023 |
| 2025 | 6 | 0.833 | 0.304 | 1.824 | 0.032 |
| 2026 | 7 | 0.571 | 0.373 | 2.610 | 0.025 |

## 5. Combo signals per ticker (15 worst and 15 best by total_R)

| ticker | n | win_rate | avg_R | total_R | fwd20 |
|---|---|---|---|---|---|
| HII | 1 | 0 | -1.000 | -1.000 | -0.096 |
| XYL | 1 | 0 | -1.000 | -1.000 | -0.113 |
| GPN | 1 | 0 | -0.998 | -0.998 | -0.143 |
| ZTS | 1 | 0 | -0.887 | -0.887 | -0.016 |
| MMS | 1 | 0 | -0.841 | -0.841 | -0.051 |
| HXL | 1 | 0 | -0.739 | -0.739 | -0.081 |
| SUI | 1 | 0 | -0.729 | -0.729 | 0.012 |
| SGI | 1 | 0 | -0.687 | -0.687 | -0.465 |
| AZO | 1 | 0 | -0.647 | -0.647 | -0.038 |
| WTS | 1 | 0 | -0.639 | -0.639 | -0.007 |
| GWRE | 1 | 0 | -0.532 | -0.532 | -0.031 |
| ADP | 1 | 0 | -0.494 | -0.494 | 0.064 |
| TYL | 1 | 0 | -0.486 | -0.486 | -0.029 |
| WHR | 1 | 0 | -0.390 | -0.390 | 0.002 |
| DE | 1 | 0 | -0.367 | -0.367 | -0.055 |
| VZ | 1 | 1.000 | 0.720 | 0.720 | 0.121 |
| TXNM | 1 | 1.000 | 0.842 | 0.842 | 0.055 |
| DVA | 1 | 1.000 | 0.868 | 0.868 | 0.013 |
| CPT | 1 | 1.000 | 0.891 | 0.891 | 0.076 |
| JNJ | 1 | 1.000 | 0.928 | 0.928 | 0.097 |
| G | 1 | 1.000 | 0.962 | 0.962 | 0.082 |
| LEN | 1 | 1.000 | 0.987 | 0.987 | 0.094 |
| PAYX | 1 | 1.000 | 1.390 | 1.390 | 0.079 |
| DTE | 1 | 1.000 | 1.616 | 1.616 | 0.072 |
| FTV | 1 | 1.000 | 1.926 | 1.926 | 0.076 |
| APH | 1 | 1.000 | 2.046 | 2.046 | 0.067 |
| DIS | 1 | 1.000 | 2.165 | 2.165 | 0.075 |
| EXC | 2 | 1.000 | 1.164 | 2.328 | 0.068 |
| WM | 3 | 0.667 | 2.157 | 6.471 | 0.064 |
| NWS | 1 | 1.000 | 7.556 | 7.556 | 0.043 |
