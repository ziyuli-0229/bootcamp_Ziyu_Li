# Stage 08 — Exploratory Data Analysis & Feature Hypotheses

## Key EDA Findings
- **Feature Distribution**: Continuous numerical variables demonstrate localized Gaussian distribution with extreme shock tails.
- **Correlation**: Strong linear alignment detected across primary and secondary return metrics ($\rho > 0.60$).
- **Time Dynamics**: Stationarity confirmed across time horizons; rolling variance spikes align with injected market shocks.

## Stage 09 Feature Hypotheses
1. **Rolling Statistics**: Constructing 7-day and 14-day rolling standard deviations will encapsulate transient volatility spikes.
2. **Lagged Features**: Lagged features ($t-1, t-2$) will capture short-term temporal autocorrelations.