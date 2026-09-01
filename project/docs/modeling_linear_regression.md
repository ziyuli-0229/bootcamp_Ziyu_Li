# Stage 10a — Linear Regression Modeling Documentation

## Feature Selection & Domain Rationale

| Feature Name | Type | Domain / Feature Logic |
| :--- | :--- | :--- |
| `spend_rolling_mean_7d` | Engineered Numerical | Primary trend driver capturing baseline spending momentum over a 7-day window. |
| `spend_income_ratio` | Engineered Ratio | Measures individual expenditure relative to earning capacity. |
| `spend_rolling_std_7d` | Engineered Numerical | Captures short-term variance and sudden demand spikes. |
| `region_freq` | Frequency Encoded | Incorporates geographic population density without increasing feature matrix dimensionality. |

## Model Coefficients & Interpretation

- **`spend_rolling_mean_7d`**: Strongest positive predictor ($\beta > 0$). Demonstrates that recent spending baseline is the primary estimator of future spend.
- **`spend_income_ratio`**: Moderate positive relationship, verifying higher financial leverage elevates spending levels.
- **Intercept**: Baseline predicted spend when continuous features are centered.

## Residual Diagnostics & Risks

1. **Linearity & Homoscedasticity**: Residuals maintain constant variance across prediction ranges without polynomial curves.
2. **Normality**: Errors are symmetrically distributed around zero.
3. **Operational Risks**: Out-of-sample performance depends on stability in consumer income distributions and absence of abrupt policy changes.