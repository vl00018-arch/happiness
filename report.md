# World Happiness Report — EDA (2015–2019)
DSCI 101-001 · Introduction to Data Science · West Virginia University
_Generated 2026-11-20 12:31_

## DATA OVERVIEW

### Countries and mean score per year

|   Year |   countries |   mean_score |
|-------:|------------:|-------------:|
|   2015 |         158 |        5.376 |
|   2016 |         157 |        5.382 |
|   2017 |         155 |        5.354 |
|   2018 |         156 |        5.376 |
|   2019 |         156 |        5.407 |

### Missing values per column (all years)

| Column     |   Missing values |
|:-----------|-----------------:|
| Corruption |                1 |

### Countries still without a region

|   # | Country   |
|----:|:----------|
|   1 | (none)    |

**NOTE:** 'Corruption' is the *Trust (Government Corruption)* factor — a HIGHER value means people perceive LESS corruption.

## TASK 1 — Distribution of Happiness Score

### Summary statistics of Happiness Score by year

|   Year |   count |   mean |   std |   min |   25% |   50% |   75% |   max |   skew |   kurtosis |
|-------:|--------:|-------:|------:|------:|------:|------:|------:|------:|-------:|-----------:|
|   2015 |     158 |  5.376 | 1.145 | 2.839 | 4.526 | 5.232 | 6.244 | 7.587 |  0.098 |     -0.776 |
|   2016 |     157 |  5.382 | 1.142 | 2.905 | 4.404 | 5.314 | 6.269 | 7.526 |  0.044 |     -0.89  |
|   2017 |     155 |  5.354 | 1.131 | 2.693 | 4.506 | 5.279 | 6.102 | 7.537 |  0.01  |     -0.75  |
|   2018 |     156 |  5.376 | 1.12  | 2.905 | 4.454 | 5.378 | 6.168 | 7.632 |  0.015 |     -0.711 |
|   2019 |     156 |  5.407 | 1.113 | 2.853 | 4.544 | 5.38  | 6.184 | 7.769 |  0.011 |     -0.608 |

## TASK 2 — GDP per Capita vs Health (Life Expectancy)

### Correlation between GDP per Capita and Health, by year

|   Year |   n |   Pearson r (GDP vs Health) |
|-------:|----:|----------------------------:|
|   2015 | 158 |                       0.816 |
|   2016 | 157 |                       0.837 |
|   2017 | 155 |                       0.843 |
|   2018 | 156 |                       0.844 |
|   2019 | 156 |                       0.835 |

## TASK 3 — Freedom vs Generosity

### Correlation between Freedom and Generosity, by year

|   Year |   n |   Pearson r (Freedom vs Generosity) |
|-------:|----:|------------------------------------:|
|   2015 | 158 |                               0.374 |
|   2016 | 157 |                               0.362 |
|   2017 | 155 |                               0.316 |
|   2018 | 156 |                               0.298 |
|   2019 | 156 |                               0.27  |

## TASK 4 — GDP per Capita, Corruption (Trust), Generosity — 3D

### Pairwise Pearson correlations by year

|   Year |   GDP–Corruption |   GDP–Generosity |   Corruption–Generosity |
|-------:|-----------------:|-----------------:|------------------------:|
|   2015 |            0.308 |           -0.01  |                   0.276 |
|   2016 |            0.294 |           -0.026 |                   0.306 |
|   2017 |            0.351 |           -0.019 |                   0.294 |
|   2018 |            0.32  |           -0.011 |                   0.362 |
|   2019 |            0.299 |           -0.08  |                   0.327 |

## TASK 5 — Countries missing between consecutive years

### Name changes detected (treated as the same country)

|   # |   Year | RawName                  | Country             |
|----:|-------:|:-------------------------|:--------------------|
|   1 |   2015 | Somaliland region        | Somaliland Region   |
|   2 |   2017 | Taiwan Province of China | Taiwan              |
|   3 |   2017 | Hong Kong S.A.R., China  | Hong Kong           |
|   4 |   2018 | Trinidad & Tobago        | Trinidad and Tobago |
|   5 |   2018 | Northern Cyprus          | North Cyprus        |
|   6 |   2019 | Trinidad & Tobago        | Trinidad and Tobago |
|   7 |   2019 | Northern Cyprus          | North Cyprus        |
|   8 |   2019 | North Macedonia          | Macedonia           |

### Country count changes between consecutive years

| Comparison   |   n in first year |   n in second year |   Dropped |   Added |
|:-------------|------------------:|-------------------:|----------:|--------:|
| 2015 vs 2016 |               158 |                157 |         6 |       5 |
| 2016 vs 2017 |               157 |                155 |         5 |       3 |
| 2017 vs 2018 |               155 |                156 |         0 |       1 |
| 2018 vs 2019 |               156 |                156 |         3 |       3 |

### Every country that entered or left the dataset

|   # | Comparison   | Country                  | Status          |
|----:|:-------------|:-------------------------|:----------------|
|   1 | 2015 vs 2016 | Central African Republic | missing in 2016 |
|   2 | 2015 vs 2016 | Djibouti                 | missing in 2016 |
|   3 | 2015 vs 2016 | Lesotho                  | missing in 2016 |
|   4 | 2015 vs 2016 | Mozambique               | missing in 2016 |
|   5 | 2015 vs 2016 | Oman                     | missing in 2016 |
|   6 | 2015 vs 2016 | Swaziland                | missing in 2016 |
|   7 | 2015 vs 2016 | Belize                   | new in 2016     |
|   8 | 2015 vs 2016 | Namibia                  | new in 2016     |
|   9 | 2015 vs 2016 | Puerto Rico              | new in 2016     |
|  10 | 2015 vs 2016 | Somalia                  | new in 2016     |
|  11 | 2015 vs 2016 | South Sudan              | new in 2016     |
|  12 | 2016 vs 2017 | Comoros                  | missing in 2017 |
|  13 | 2016 vs 2017 | Laos                     | missing in 2017 |
|  14 | 2016 vs 2017 | Puerto Rico              | missing in 2017 |
|  15 | 2016 vs 2017 | Somaliland Region        | missing in 2017 |
|  16 | 2016 vs 2017 | Suriname                 | missing in 2017 |
|  17 | 2016 vs 2017 | Central African Republic | new in 2017     |
|  18 | 2016 vs 2017 | Lesotho                  | new in 2017     |
|  19 | 2016 vs 2017 | Mozambique               | new in 2017     |
|  20 | 2017 vs 2018 | Laos                     | new in 2018     |
|  21 | 2018 vs 2019 | Angola                   | missing in 2019 |
|  22 | 2018 vs 2019 | Belize                   | missing in 2019 |
|  23 | 2018 vs 2019 | Sudan                    | missing in 2019 |
|  24 | 2018 vs 2019 | Comoros                  | new in 2019     |
|  25 | 2018 vs 2019 | Gambia                   | new in 2019     |
|  26 | 2018 vs 2019 | Swaziland                | new in 2019     |

**Countries present in all 5 years: 146**

## TASK 6 — Pearson, Spearman and Kendall correlation coefficients

### Score & Generosity

|   Year |   n |   Pearson r |   Pearson p |   Spearman rho |   Spearman p |   Kendall tau |   Kendall p |
|-------:|----:|------------:|------------:|---------------:|-------------:|--------------:|------------:|
|   2015 | 158 |      0.1803 |      0.0234 |         0.1725 |       0.0302 |        0.1127 |      0.0356 |
|   2016 | 157 |      0.1568 |      0.0498 |         0.1492 |       0.0622 |        0.0971 |      0.0711 |
|   2017 | 155 |      0.1553 |      0.0537 |         0.1364 |       0.0905 |        0.0859 |      0.1128 |
|   2018 | 156 |      0.1358 |      0.0909 |         0.1123 |       0.1628 |        0.0724 |      0.1804 |
|   2019 | 156 |      0.0758 |      0.3468 |         0.0705 |       0.3819 |        0.0438 |      0.4184 |

### Freedom & Generosity

|   Year |   n |   Pearson r |   Pearson p |   Spearman rho |   Spearman p |   Kendall tau |   Kendall p |
|-------:|----:|------------:|------------:|---------------:|-------------:|--------------:|------------:|
|   2015 | 158 |      0.3739 |      0      |         0.4185 |            0 |        0.2834 |           0 |
|   2016 | 157 |      0.3618 |      0      |         0.4006 |            0 |        0.2736 |           0 |
|   2017 | 155 |      0.3161 |      0.0001 |         0.3496 |            0 |        0.2345 |           0 |
|   2018 | 156 |      0.298  |      0.0002 |         0.3483 |            0 |        0.2393 |           0 |
|   2019 | 156 |      0.2697 |      0.0007 |         0.3241 |            0 |        0.2262 |           0 |

### GDP & Corruption

|   Year |   n |   Pearson r |   Pearson p |   Spearman rho |   Spearman p |   Kendall tau |   Kendall p |
|-------:|----:|------------:|------------:|---------------:|-------------:|--------------:|------------:|
|   2015 | 158 |      0.3079 |      0.0001 |         0.2277 |       0.004  |        0.1426 |      0.0079 |
|   2016 | 157 |      0.2942 |      0.0002 |         0.2235 |       0.0049 |        0.1435 |      0.0077 |
|   2017 | 155 |      0.3509 |      0      |         0.2456 |       0.0021 |        0.1578 |      0.0036 |
|   2018 | 155 |      0.3196 |      0.0001 |         0.2433 |       0.0023 |        0.1558 |      0.0041 |
|   2019 | 156 |      0.2989 |      0.0002 |         0.2232 |       0.0051 |        0.1352 |      0.0125 |

### GDP & Freedom

|   Year |   n |   Pearson r |   Pearson p |   Spearman rho |   Spearman p |   Kendall tau |   Kendall p |
|-------:|----:|------------:|------------:|---------------:|-------------:|--------------:|------------:|
|   2015 | 158 |      0.3703 |           0 |         0.4154 |            0 |        0.2863 |           0 |
|   2016 | 157 |      0.3623 |           0 |         0.3973 |            0 |        0.2783 |           0 |
|   2017 | 155 |      0.3699 |           0 |         0.4068 |            0 |        0.2821 |           0 |
|   2018 | 156 |      0.3323 |           0 |         0.3685 |            0 |        0.2572 |           0 |
|   2019 | 156 |      0.3791 |           0 |         0.3934 |            0 |        0.2708 |           0 |

## TASK 7 — Variables most strongly related to Happiness Score

### Pearson correlation of each factor with Happiness Score

| Factor     |   2015 |   2016 |   2017 |   2018 |   2019 |   Mean |
|:-----------|-------:|-------:|-------:|-------:|-------:|-------:|
| GDP        |  0.781 |  0.79  |  0.812 |  0.802 |  0.794 |  0.796 |
| Health     |  0.724 |  0.765 |  0.782 |  0.776 |  0.78  |  0.765 |
| Family     |  0.741 |  0.739 |  0.753 |  0.746 |  0.777 |  0.751 |
| Freedom    |  0.568 |  0.567 |  0.57  |  0.544 |  0.567 |  0.563 |
| Corruption |  0.395 |  0.402 |  0.429 |  0.405 |  0.386 |  0.403 |
| Generosity |  0.18  |  0.157 |  0.155 |  0.136 |  0.076 |  0.141 |

### Spearman correlation of each factor with Happiness Score

| Factor     |   2015 |   2016 |   2017 |   2018 |   2019 |   Mean |
|:-----------|-------:|-------:|-------:|-------:|-------:|-------:|
| GDP        |  0.796 |  0.808 |  0.825 |  0.823 |  0.814 |  0.813 |
| Health     |  0.757 |  0.771 |  0.788 |  0.793 |  0.807 |  0.783 |
| Family     |  0.77  |  0.762 |  0.774 |  0.776 |  0.816 |  0.78  |
| Freedom    |  0.576 |  0.563 |  0.556 |  0.535 |  0.552 |  0.556 |
| Corruption |  0.302 |  0.312 |  0.301 |  0.25  |  0.217 |  0.277 |
| Generosity |  0.172 |  0.149 |  0.136 |  0.112 |  0.07  |  0.128 |

### Ranking (strongest -> weakest, by mean Pearson r)

|   # | Factor     |   Mean Pearson r |
|----:|:-----------|-----------------:|
|   1 | GDP        |            0.796 |
|   2 | Health     |            0.765 |
|   3 | Family     |            0.751 |
|   4 | Freedom    |            0.563 |
|   5 | Corruption |            0.403 |
|   6 | Generosity |            0.141 |

### Full correlation matrix (2015–2019 pooled)

|            |   Score |    GDP |   Family |   Health |   Freedom |   Corruption |   Generosity |
|:-----------|--------:|-------:|---------:|---------:|----------:|-------------:|-------------:|
| Score      |   1     |  0.789 |    0.649 |    0.742 |     0.551 |        0.398 |        0.138 |
| GDP        |   0.789 |  1     |    0.586 |    0.784 |     0.341 |        0.306 |       -0.015 |
| Family     |   0.649 |  0.586 |    1     |    0.573 |     0.42  |        0.126 |       -0.037 |
| Health     |   0.742 |  0.784 |    0.573 |    1     |     0.341 |        0.251 |        0.011 |
| Freedom    |   0.551 |  0.341 |    0.42  |    0.341 |     1     |        0.46  |        0.291 |
| Corruption |   0.398 |  0.306 |    0.126 |    0.251 |     0.46  |        1     |        0.319 |
| Generosity |   0.138 | -0.015 |   -0.037 |    0.011 |     0.291 |        0.319 |        1     |

## TASK 8 — World map (choropleth) of Happiness Score

### Not placed on the map

|   # | Country           |
|----:|:------------------|
|   1 | North Cyprus      |
|   2 | Somaliland Region |

## TASK 9 — Happiness rank trends by year and region

### Number of ranked countries per year

|   Year |   Ranked countries |
|-------:|-------------------:|
|   2015 |                158 |
|   2016 |                157 |
|   2017 |                155 |
|   2018 |                156 |
|   2019 |                156 |

### Mean happiness rank by region (lower = happier)

| Region                          |   2015 |   2016 |   2017 |   2018 |   2019 |   Change 2015→2019 (+ = worse) |
|:--------------------------------|-------:|-------:|-------:|-------:|-------:|-------------------------------:|
| Australia and New Zealand       |    9.5 |    8.5 |    9   |    9   |    9.5 |                            0   |
| North America                   |   10   |    9.5 |   10.5 |   12.5 |   14   |                            4   |
| Western Europe                  |   29.5 |   29.2 |   27.1 |   24.7 |   23.4 |                           -6.1 |
| Latin America and Caribbean     |   46.9 |   48.3 |   50.8 |   50.5 |   51.4 |                            4.5 |
| Eastern Asia                    |   64.5 |   67.2 |   64.8 |   65.5 |   64.8 |                            0.3 |
| Central and Eastern Europe      |   79   |   78.4 |   75.1 |   75   |   71   |                           -8   |
| Middle East and Northern Africa |   77.6 |   78.1 |   76.4 |   80.9 |   84.9 |                            7.3 |
| Southeastern Asia               |   81.2 |   80   |   73.8 |   81.9 |   85.1 |                            3.9 |
| Southern Asia                   |  113.1 |  111.7 |  109.9 |  111.7 |  115.9 |                            2.7 |
| Sub-Saharan Africa              |  127.9 |  129.7 |  127.9 |  126.9 |  124.8 |                           -3.1 |

### Mean happiness score by region

| Region                          |   2015 |   2016 |   2017 |   2018 |   2019 |
|:--------------------------------|-------:|-------:|-------:|-------:|-------:|
| Australia and New Zealand       |  7.285 |  7.323 |  7.299 |  7.298 |  7.268 |
| North America                   |  7.273 |  7.254 |  7.155 |  7.107 |  7.085 |
| Western Europe                  |  6.69  |  6.686 |  6.704 |  6.782 |  6.842 |
| Latin America and Caribbean     |  6.145 |  6.102 |  5.958 |  5.95  |  5.954 |
| Eastern Asia                    |  5.626 |  5.624 |  5.647 |  5.672 |  5.689 |
| Central and Eastern Europe      |  5.333 |  5.371 |  5.41  |  5.464 |  5.562 |
| Middle East and Northern Africa |  5.407 |  5.386 |  5.37  |  5.283 |  5.237 |
| Southeastern Asia               |  5.317 |  5.339 |  5.445 |  5.313 |  5.274 |
| Southern Asia                   |  4.581 |  4.563 |  4.628 |  4.604 |  4.527 |
| Sub-Saharan Africa              |  4.203 |  4.136 |  4.112 |  4.195 |  4.3   |

### Top 10 risers 2015→2019 (positive = moved up)

| Country      |   2015 |   2019 |   Change |
|:-------------|-------:|-------:|---------:|
| Benin        |    155 |    102 |       53 |
| Ivory Coast  |    151 |     99 |       52 |
| Honduras     |    105 |     59 |       46 |
| Hungary      |    104 |     62 |       42 |
| Gabon        |    143 |    104 |       39 |
| Romania      |     86 |     48 |       38 |
| Bulgaria     |    134 |     97 |       37 |
| Burkina Faso |    152 |    115 |       37 |
| Cameroon     |    133 |     96 |       37 |
| Cambodia     |    145 |    109 |       36 |

### Top 10 fallers 2015→2019

| Country    |   2015 |   2019 |   Change |
|:-----------|-------:|-------:|---------:|
| Venezuela  |     23 |    108 |      -85 |
| Zambia     |     85 |    138 |      -53 |
| Lesotho    |     97 |    144 |      -47 |
| Swaziland  |    101 |    135 |      -34 |
| Zimbabwe   |    115 |    146 |      -31 |
| Mozambique |     94 |    123 |      -29 |
| Haiti      |    119 |    147 |      -28 |
| Liberia    |    116 |    141 |      -25 |
| India      |    117 |    140 |      -23 |
| Belarus    |     59 |     81 |      -22 |

---

## Figures

- `images/task1_score_histograms.png`
- `images/task2_gdp_vs_health.png`
- `images/task3_freedom_vs_generosity.png`
- `images/task4_3d_2015.png`
- `images/task4_3d_2016.png`
- `images/task4_3d_2017.png`
- `images/task4_3d_2018.png`
- `images/task4_3d_2019.png`
- `images/task6_correlations.png`
- `images/task7_correlation_matrix.png`
- `images/task7_factor_score_heatmap.png`
- `images/task8_world_map_2015.png`
- `images/task8_world_map_2016.png`
- `images/task8_world_map_2017.png`
- `images/task8_world_map_2018.png`
- `images/task8_world_map_2019.png`
- `images/task9_biggest_movers.png`
- `images/task9_region_rank_trends.png`
- `images/task4_3d_interactive.html` (interactive — open in a browser)
- `images/task8_world_map_interactive.html` (interactive — open in a browser)
