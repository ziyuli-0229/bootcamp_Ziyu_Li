# Outlier Analysis & Risk Documentation

## Outlier Definitions & Detection Strategy
Outliers are defined as observations that deviate significantly from the underlying feature distribution:
- **IQR Threshold ($k = 1.5$)**: Fences are set at $[Q_1 - 1.5 \times \text{IQR}, Q_3 + 1.5 \times \text{IQR}]$. This non-parametric approach requires no assumption of normality.
- **Z-Score Threshold ($\text{Threshold} = 3.0$)**: Identifies data points where $|Z| > 3.0$ relative to sample mean and standard deviation ($ddof = 1$). Assumes an approximately normal distribution.

## Sensitivity Analysis & Handling Strategy
- **Winsorization ($5\% - 95\%$)**: Bounds extreme values without discarding observations, preserving sample size while capping leverage points.
- **Filtering**: Removing flagged outliers is evaluated during model cross-validation to assess stability and metrics ($R^2$, $\text{MAE}$).

## Assumptions & Risk Assessment
- **Primary Assumption**: Extreme spikes represent transient noise or market shocks rather than permanent structural breaks.
- **Downstream Risks**: Discarding extreme observations can underestimate tail risk, drawdowns, and volatility metrics in financial or risk-sensitive domains.