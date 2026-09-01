# Stage 10b — Time Series & Classification Documentation

## Feature Engineering Definitions

| Feature Name | Type | Transformation Logic | Purpose & Leakage Prevention |
| :--- | :--- | :--- | :--- |
| `spend_lag_1` | Numerical | `spend.shift(1)` | Captures immediate past observation without lookahead leakage. |
| `spend_lag_2` | Numerical | `spend.shift(2)` | Measures 2-period momentum. |
| `spend_roll_mean_5` | Numerical | `spend.rolling(5).mean().shift(1)` | Moving average baseline shifted by 1 period to prevent current-day leakage. |
| `spend_roll_std_20` | Numerical | `spend.rolling(20).std().shift(1)` | Captures localized volatility levels. |
| `y_up` | Target (Binary) | `(spend.shift(-1) > spend).astype(int)` | Binary directional indicator (1 = Increase, 0 = Decrease). |

## Scikit-Learn Pipeline Structure

- **Scaler**: `StandardScaler()` standardizes feature distributions to zero mean and unit variance.
- **Classifier**: `LogisticRegression(max_iter=1000)` fits a baseline linear decision boundary for directional prediction.