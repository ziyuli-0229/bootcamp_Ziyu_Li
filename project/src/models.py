"""
Linear Regression Modeling Utility Module
Provides automated training, evaluation metrics, coefficient extraction,
and residual generation functions.
"""

from typing import Dict, Tuple
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score


def train_linear_model(
    X_train: pd.DataFrame, y_train: pd.Series
) -> LinearRegression:
    """
    Fit an Ordinary Least Squares (OLS) Linear Regression model.

    Parameters:
    -----------
    X_train : pd.DataFrame
        Training feature matrix.
    y_train : pd.Series
        Training target vector.

    Returns:
    --------
    LinearRegression
        Fitted Scikit-Learn linear regression model instance.
    """
    model = LinearRegression()
    model.fit(X_train, y_train)
    return model


def evaluate_model_performance(
    model: LinearRegression, X_test: pd.DataFrame, y_test: pd.Series
) -> Tuple[Dict[str, float], np.ndarray, np.ndarray]:
    """
    Generate predictions and calculate regression metrics ($R^2$ and RMSE).

    Parameters:
    -----------
    model : LinearRegression
        Fitted regression model.
    X_test : pd.DataFrame
        Testing feature matrix.
    y_test : pd.Series
        Testing target vector.

    Returns:
    --------
    Tuple[Dict[str, float], np.ndarray, np.ndarray]
        Dictionary of metrics, array of predictions, and array of residuals.
    """
    predictions = model.predict(X_test)
    residuals = y_test.values - predictions

    r2 = float(r2_score(y_test, predictions))
    rmse = float(np.sqrt(mean_squared_error(y_test, predictions)))

    metrics = {"R2": round(r2, 4), "RMSE": round(rmse, 6)}
    return metrics, predictions, residuals


def extract_coefficients(
    model: LinearRegression, feature_names: list
) -> pd.DataFrame:
    """
    Extract fitted model coefficients into a structured DataFrame.

    Parameters:
    -----------
    model : LinearRegression
        Fitted regression estimator.
    feature_names : list
        List of predictor variable names.

    Returns:
    --------
    pd.DataFrame
        DataFrame listing features, coefficients, and intercept.
    """
    coef_df = pd.DataFrame(
        {"Feature": feature_names, "Coefficient": model.coef_}
    )
    intercept_df = pd.DataFrame(
        {"Feature": ["Intercept"], "Coefficient": [model.intercept_]}
    )
    return pd.concat([intercept_df, coef_df], ignore_index=True)