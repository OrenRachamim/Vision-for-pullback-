# Multi-timeframe search - 1467 stocks, entries 2023-12-28 -> 2026-10-16 (703 days); selection < 2025-05-23 <= test

combos: 4 triggers x 5 daily x 1 hourly = 20, x 10 exits = 200 tested configurations

## Exits compared (no filters; avg per trade after costs)

| exit | random entry (all) | all 4 triggers | random, sel half | random, test half |
|---|---|---|---|---|
| eod | -0.107% | -0.097% | -0.095% | -0.119% |
| next | -0.052% | -0.060% | -0.061% | -0.043% |
| L1h_tight | -0.076% | -0.044% | -0.068% | -0.085% |
| Ld_tight | +0.051% | +0.063% | +0.078% | +0.026% |
| casc_tight | -0.030% | -0.007% | -0.023% | -0.036% |
| casc_nc_tight | +0.054% | +0.071% | +0.091% | +0.017% |
| L1h_wide | -0.034% | +0.010% | -0.019% | -0.049% |
| Ld_wide | +0.164% | +0.191% | +0.194% | +0.135% |
| casc_wide | +0.033% | +0.066% | +0.043% | +0.023% |
| casc_nc_wide | +0.164% | +0.194% | +0.208% | +0.121% |

cascade tight: exits at stage 1 68%, stage 2 32%, stage 3 0%

cascade wide: exits at stage 1 66%, stage 2 34%, stage 3 0%

## Top 20 by selection-half excess over random (n_sel >= 100) -> what happened in the test half

| trigger | daily | hourly | exit | n sel | avg sel | excess sel | n test | avg test | random test | excess test |
|---|---|---|---|---|---|---|---|---|---|---|
| pdh | conv | none | Ld_wide | 290 | +1.032% | +0.957% | 543 | +0.412% | +0.121% | +0.291% |
| pdh | conv | none | Ld_tight | 290 | +0.676% | +0.717% | 543 | +0.307% | +0.026% | +0.281% |
| pdh | conv | none | casc_nc_wide | 290 | +0.749% | +0.680% | 543 | +0.354% | +0.056% | +0.297% |
| pdh | conv | none | casc_wide | 290 | +0.644% | +0.592% | 543 | +0.367% | +0.058% | +0.309% |
| pdh | conv | none | casc_nc_tight | 290 | +0.509% | +0.550% | 543 | +0.173% | +0.015% | +0.157% |
| pdh | conv | none | casc_tight | 290 | +0.452% | +0.500% | 543 | +0.154% | +0.008% | +0.146% |
| pdh | conv | none | next | 290 | +0.242% | +0.381% | 543 | +0.115% | -0.026% | +0.141% |
| pdh | conv | none | L1h_wide | 290 | +0.212% | +0.320% | 543 | +0.149% | -0.042% | +0.191% |
| hrsimacd | none | none | casc_nc_wide | 6768 | +0.486% | +0.277% | 6518 | +0.346% | +0.121% | +0.225% |
| hrsimacd | none | none | Ld_wide | 6768 | +0.438% | +0.244% | 6518 | +0.406% | +0.135% | +0.271% |
| pdh | conv | none | L1h_tight | 290 | +0.095% | +0.230% | 543 | -0.039% | -0.075% | +0.036% |
| hrsimacd | none | none | L1h_wide | 6768 | +0.210% | +0.229% | 6518 | +0.221% | -0.049% | +0.271% |
| hma | conv | none | next | 204 | +0.088% | +0.227% | 205 | +0.155% | -0.026% | +0.181% |
| hma | conv | none | Ld_wide | 204 | +0.295% | +0.221% | 205 | +0.196% | +0.121% | +0.075% |
| hrsimacd | none | none | L1h_tight | 6768 | +0.134% | +0.202% | 6518 | +0.074% | -0.085% | +0.158% |
| hrsimacd | none | none | casc_nc_tight | 6768 | +0.277% | +0.186% | 6518 | +0.225% | +0.017% | +0.208% |
| hrsimacd | none | none | casc_wide | 6768 | +0.221% | +0.178% | 6518 | +0.226% | +0.023% | +0.203% |
| hrsimacd | none | none | Ld_tight | 6768 | +0.242% | +0.164% | 6518 | +0.291% | +0.026% | +0.265% |
| hrsimacd | none | none | casc_tight | 6768 | +0.139% | +0.162% | 6518 | +0.066% | -0.036% | +0.102% |
| hma | none | none | Ld_wide | 41640 | +0.335% | +0.141% | 40461 | +0.189% | +0.135% | +0.054% |

top-20 average excess: selection +0.358% -> test +0.193%
all 180 configs: corr(excess sel, excess test) = +0.47; share with positive test excess: 59%; share with positive test avg: 53%

best selected config ('pdh', 'conv', 'none', 'Ld_wide'): test avg +0.412%, 95% date-clustered CI [+0.022%, +0.751%], win 53%, n 543
