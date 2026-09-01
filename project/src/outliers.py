"""
Outlier Detection and Treatment Utilities
Provides modular functions for outlier flagging, filtering, and Winsorization
across numerical dataset features.
"""

from typing import Optional, List
import pandas as pd
import numpy as np


def detect_outliers_iqr(series: pd.Series, k: float = 1.5) -> pd.Series:
    """
    Detect outliers using the Interquartile Range (IQR) method.

    Parameters:
    -----------
    series : pd.Series
        Target numerical data series.
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
        raise ValueError("Multiplier k must be strictly positive.")

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
        Target numerical data series.
    threshold : float, default=3.0
        Absolute Z-score threshold cutoff. Must be positive.
    ddof : int, default=1
        Delta degrees of freedom for sample standard deviation.

    Returns:
    --------
    pd.Series
        Boolean mask where True indicates an outlier.
    """
    if series.empty:
        return pd.Series(dtype=bool)
    if threshold <= 0:
        raise ValueError("Threshold must be strictly positive.")

    mean_val = series.mean()
    std_val = series.std(ddof=ddof)

    if std_val == 0 or pd.isna(std_val):
        return pd.Series(False, index=series.index)

    z_scores = (series - mean_val) / std_val
    return z_scores.abs() > threshold


def winsorize_series(
    series: pd.Series, lower: float = 0.05, upper: float = 0.95
) -> pd.Series:
    """
    Cap extreme values outside specified lower and upper quantiles.

    Parameters:
    -----------
    series : pd.Series
        Target numerical data series.
    lower : float, default=0.05
        Lower percentile threshold (0.0 to 1.0).
    upper : float, default=0.95
        Upper percentile threshold (0.0 to 1.0).

    Returns:
    --------
    pd.Series
        Series with bounded extreme values.
    """
    if not (0.0 <= lower < upper <= 1.0):
        raise ValueError("Quantiles must satisfy 0.0 <= lower < upper <= 1.0")

    lower_val = series.quantile(lower)
    upper_val = series.quantile(upper)
    return series.clip(lower=lower_val, upper=upper_val)