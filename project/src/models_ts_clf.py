"""
Time Series and Classification Helper Module
Provides functions for generating time-lagged and rolling window features
without data leakage, constructing Scikit-Learn pipelines, and evaluating models.
"""

from typing import Dict, List, Tuple
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


def create_time_series_features(
    df: pd.DataFrame,
    target_col: str = "spend",
    lags: List[int] = [1, 2],
    rolling_windows: List[int] = [5, 20],
) -> pd.DataFrame:
    """
    Generate lag and rolling statistics for time series features while shifting by 1
    period to strictly prevent lookahead data leakage.

    Parameters:
    -----------
    df : pd.DataFrame
        Input DataFrame indexed by time or sorted chronologically.
    target_col : str, default="spend"
        Base column name to derive temporal features from.
    lags : List[int], default=[1, 2]
        List of lag steps to generate.
    rolling_windows : List[int], default=[5, 20]
        List of window lengths for rolling mean and standard deviation.

    Returns:
    --------
    pd.DataFrame
        DataFrame containing engineered lag/rolling features and binary direction target.
    """
    df_out = df.copy()

    # 1. Lag Features (Shifted by k steps)
    for k in lags:
        df_out[f"{target_col}_lag_{k}"] = df_out[target_col].shift(k)

    # 2. Rolling Window Features (Shifted by 1 step to exclude current observation)
    for w in rolling_windows:
        df_out[f"{target_col}_roll_mean_{w}"] = (
            df_out[target_col].rolling(window=w).mean().shift(1)
        )
        df_out[f"{target_col}_roll_std_{w}"] = (
            df_out[target_col].rolling(window=w).std().shift(1)
        )

    # 3. Targets (Next-step directional classification: 1 = Up, 0 = Down)
    df_out["y_next_step"] = df_out[target_col].shift(-1)
    df_out["y_up"] = (df_out["y_next_step"] > df_out[target_col]).astype(int)

    # Drop missing rows created by lag, rolling window, and lookahead target
    df_out = df_out.dropna().copy()
    return df_out


def build_classification_pipeline() -> Pipeline:
    """
    Build a Scikit-Learn pipeline combining feature scaling and logistic regression.

    Returns:
    --------
    Pipeline
        Executable Scikit-Learn pipeline.
    """
    pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("clf", LogisticRegression(max_iter=1000, random_state=7)),
    ])
    return pipeline


def evaluate_classification_metrics(
    model: Pipeline, X_test: pd.DataFrame, y_test: pd.Series
) -> Tuple[Dict[str, float], np.ndarray]:
    """
    Compute accuracy, precision, recall, and F1 metrics for test predictions.

    Parameters:
    -----------
    model : Pipeline
        Fitted classification pipeline.
    X_test : pd.DataFrame
        Test feature matrix.
    y_test : pd.Series
        Test ground truth labels.

    Returns:
    --------
    Tuple[Dict[str, float], np.ndarray]
        Dictionary of classification metrics and array of predictions.
    """
    preds = model.predict(X_test)
    metrics = {
        "Accuracy": round(float(accuracy_score(y_test, preds)), 4),
        "Precision": round(
            float(precision_score(y_test, preds, zero_division=0)), 4
        ),
        "Recall": round(
            float(recall_score(y_test, preds, zero_division=0)), 4
        ),
        "F1_Score": round(float(f1_score(y_test, preds, zero_division=0)), 4),
    }
    return metrics, preds