# Stage 09 — Feature Engineering & Domain Rationales

## Engineered Features Summary

| Feature Name | Calculation / Transformation | Rationale & Domain Knowledge | Related EDA Insight (Stage 08) |
| :--- | :--- | :--- | :--- |
| `spend_income_ratio` | `spend / income` | Measures individual spending leverage relative to earning capacity. | Raw `income` and `spend` were heavily right-skewed. |
| `spend_rolling_mean_7d` | 7-period moving average of `spend` | Smoothes short-term spend fluctuations to capture true baseline trend. | Daily spend series exhibited high temporal volatility. |
| `spend_rolling_std_7d` | 7-period moving standard deviation | Quantifies short-term spending volatility and shock susceptibility. | Shock spikes aligned with high-risk events. |
| `region_freq` | Frequency proportion of `region` | Encodes region prevalence without adding high-cardinality dummy columns. | Categorical counts showed uneven region distributions. |