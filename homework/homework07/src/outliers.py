"""
Outlier Detection and Handling Utilities Module
Provides reusable modular functions for IQR detection, Z-score analysis,
and Winsorization capping across continuous datasets.
"""

from typing import Optional
import pandas as pd
import numpy as np


def detect_outliers_iqr(series: pd.Series, k: float = 1.5) -> pd.Series:
    """
    Detect outliers using the Interquartile Range (IQR) method.

    Parameters:
    -----------
    series : pd.Series
        Target numeric data series.
    k : float, default=1.5
        Multiplier for IQR fence bounds. Must be positive.

    Returns:
    --------
    pd.Series
        Boolean mask where True indicates an outlier.
    """
    if series.empty:
        return pd.Series(dtype=bool)
    if k <= 0:
        raise ValueError("IQR multiplier 'k' must be strictly positive.")

    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - k * iqr
    upper_bound = q3 + k * iqr

    return (series < lower_bound) | (series > upper_bound)


def detect_outliers_zscore(
    series: pd.Series, threshold: float = 3.0, ddof: int = 1
) -> pd.Series:
    """
    Detect outliers using standardized Z-score transformation.

    Parameters:
    -----------
    series : pd.Series
        Target numeric data series.
    threshold : float, default=3.0
        Absolute Z-score cutoff. Must be positive.
    ddof : int, default=1
        Delta Degrees of Freedom for sample standard deviation.

    Returns:
    --------
    pd.Series
        Boolean mask where True indicates an outlier.
    """
    if series.empty:
        return pd.Series(dtype=bool)
    if threshold <= 0:
        raise ValueError("Z-score threshold must be strictly positive.")

    mu = series.mean()
    sigma = series.std(ddof=ddof)

    if sigma == 0 or pd.isna(sigma):
        return pd.Series(False, index=series.index)

    z_scores = (series - mu) / sigma
    return z_scores.abs() > threshold


def winsorize_series(
    series: pd.Series, lower: float = 0.05, upper: float = 0.95
) -> pd.Series:
    """
    Cap extreme values at specified lower and upper quantiles.

    Parameters:
    -----------
    series : pd.Series
        Target numeric series.
    lower : float, default=0.05
        Lower quantile threshold (0.0 to 1.0).
    upper : float, default=0.95
        Upper quantile threshold (0.0 to 1.0).

    Returns:
    --------
    pd.Series
        Series with capped extreme values.
    """
    if not (0.0 <= lower < upper <= 1.0):
        raise ValueError("Quantiles must satisfy 0.0 <= lower < upper <= 1.0")

    lo_val = series.quantile(lower)
    hi_val = series.quantile(upper)
    return series.clip(lower=lo_val, upper=hi_val)