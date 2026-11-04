# Robustness of the selected hourly-level entries (exit Ld_wide: target 1.5 ATR, stop 1.2 ATR, max 10 days)
entries 2023-12-28 -> 2026-10-16; selection < 2025-05-23 <= test

## A: conv + pdh

| slice | n | win | avg | random avg | excess |
|---|---|---|---|---|---|
| half=selection | 290 | 60% | +1.03% | +0.07% | +0.96% |
| half=test | 543 | 53% | +0.41% | +0.12% | +0.29% |
| index=sp500 | 304 | 58% | +0.69% | +0.13% | +0.57% |
| index=sp400 | 214 | 56% | +0.76% | +0.07% | +0.68% |
| index=sp600 | 315 | 53% | +0.48% | +0.09% | +0.39% |
| q=2024Q1 | 41 | 66% | +1.19% | +0.37% | +0.82% |
| q=2024Q2 | 31 | 77% | +2.08% | +0.19% | +1.89% |
| q=2024Q3 | 71 | 62% | +1.22% | +0.34% | +0.88% |
| q=2024Q4 | 32 | 62% | +1.35% | -0.47% | +1.82% |
| q=2025Q1 | 67 | 46% | +0.07% | -0.35% | +0.41% |
| q=2025Q2 | 62 | 56% | +0.97% | +0.06% | +0.91% |
| q=2025Q3 | 62 | 32% | -0.99% | -0.26% | -0.73% |
| q=2025Q4 | 82 | 33% | -0.99% | -0.47% | -0.53% |
| q=2026Q1 | 109 | 54% | +0.34% | +0.24% | +0.10% |
| q=2026Q2 | 186 | 66% | +1.40% | +0.91% | +0.49% |
| q=2026Q3 | 55 | 45% | +0.03% | +0.21% | -0.18% |
| q=2026Q4 | 35 | 77% | +1.71% | +0.83% | +0.88% |

quarters with positive excess: 9/13

| portfolio | K | period | CAGR | max DD (realized) | trades/yr |
|---|---|---|---|---|---|
| strategy | 10 | full | +8.3% | -10.1% | 182 |
| random entry, same filter+exit | 10 | full | +2.9% | -15.6% | 419 |
| strategy | 10 | test half | +3.5% | -9.9% | 218 |
| random entry, same filter+exit | 10 | test half | -2.0% | -11.2% | 422 |
| strategy | 20 | full | +5.4% | -5.0% | 215 |
| random entry, same filter+exit | 20 | full | +0.3% | -15.2% | 698 |
| strategy | 20 | test half | +3.7% | -5.0% | 278 |
| random entry, same filter+exit | 20 | test half | +3.3% | -7.4% | 702 |

## B: hourly RSI+MACD

| slice | n | win | avg | random avg | excess |
|---|---|---|---|---|---|
| half=selection | 6,768 | 50% | +0.44% | +0.19% | +0.24% |
| half=test | 6,518 | 51% | +0.41% | +0.13% | +0.27% |
| index=sp500 | 4,577 | 50% | +0.39% | +0.21% | +0.18% |
| index=sp400 | 3,509 | 50% | +0.42% | +0.17% | +0.25% |
| index=sp600 | 5,200 | 50% | +0.45% | +0.12% | +0.33% |
| q=2024Q1 | 915 | 59% | +0.95% | +0.31% | +0.64% |
| q=2024Q2 | 1,357 | 49% | +0.26% | -0.09% | +0.36% |
| q=2024Q3 | 922 | 59% | +1.41% | +0.59% | +0.83% |
| q=2024Q4 | 1,599 | 42% | +0.18% | +0.00% | +0.18% |
| q=2025Q1 | 1,190 | 45% | -0.29% | -0.64% | +0.36% |
| q=2025Q2 | 1,127 | 56% | +1.01% | +1.33% | -0.32% |
| q=2025Q3 | 921 | 49% | +0.37% | +0.18% | +0.20% |
| q=2025Q4 | 1,274 | 55% | +0.74% | +0.06% | +0.68% |
| q=2026Q1 | 1,245 | 53% | +0.43% | -0.06% | +0.49% |
| q=2026Q2 | 935 | 56% | +0.94% | +0.62% | +0.32% |
| q=2026Q3 | 1,605 | 40% | -0.39% | -0.48% | +0.09% |
| q=2026Q4 | 192 | 52% | -0.32% | +0.50% | -0.82% |

quarters with positive excess: 10/13

| portfolio | K | period | CAGR | max DD (realized) | trades/yr |
|---|---|---|---|---|---|
| strategy | 10 | full | +6.5% | -20.2% | 404 |
| random entry, same filter+exit | 10 | full | +2.3% | -19.7% | 465 |
| strategy | 10 | test half | +17.9% | -7.8% | 407 |
| random entry, same filter+exit | 10 | test half | -4.9% | -17.7% | 454 |
| strategy | 20 | full | +7.1% | -15.9% | 786 |
| random entry, same filter+exit | 20 | full | +4.4% | -18.1% | 930 |
| strategy | 20 | test half | +13.6% | -6.9% | 803 |
| random entry, same filter+exit | 20 | test half | -0.9% | -11.6% | 911 |

SPY buy & hold, full: +19.7% per year, max DD -18.8%
SPY buy & hold, test half: +23.3% per year, max DD -8.9%
