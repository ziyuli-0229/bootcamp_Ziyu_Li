"""
Feature Engineering Utilities Module
Provides reusable data transformation routines including financial ratio construction,
rolling window temporal statistics, and categorical frequency encoding.
"""

from typing import List, Optional
import numpy as np
import pandas as pd


def add_spend_income_ratio(
    df: pd.DataFrame, spend_col: str = "spend", income_col: str = "income"
) -> pd.DataFrame:
    """
    Construct spend-to-income ratio to evaluate relative financial burden.

    Parameters:
    -----------
    df : pd.DataFrame
        Input dataset containing spend and income features.
    spend_col : str, default="spend"
        Column name representing spend volume.
    income_col : str, default="income"
        Column name representing baseline income.

    Returns:
    --------
    pd.DataFrame
        DataFrame with appended spend_income_ratio feature.
    """
    df_out = df.copy()
    if spend_col in df_out.columns and income_col in df_out.columns:
        df_out["spend_income_ratio"] = np.where(
            df_out[income_col] > 0,
            df_out[spend_col] / df_out[income_col],
            np.nan,
        )
    return df_out


def add_rolling_features(
    df: pd.DataFrame, target_col: str = "spend", window: int = 7
) -> pd.DataFrame:
    """
    Compute rolling mean and standard deviation over a time window.

    Parameters:
    -----------
    df : pd.DataFrame
        Input dataset sorted chronologically.
    target_col : str, default="spend"
        Target numerical feature column.
    window : int, default=7
        Rolling window length.

    Returns:
    --------
    pd.DataFrame
        DataFrame with appended rolling window statistics.
    """
    df_out = df.copy()
    if target_col in df_out.columns:
        df_out[f"{target_col}_rolling_mean_{window}d"] = (
            df_out[target_col].rolling(window=window, min_periods=1).mean()
        )
        df_out[f"{target_col}_rolling_std_{window}d"] = (
            df_out[target_col]
            .rolling(window=window, min_periods=1)
            .std()
            .fillna(0)
        )
    return df_out


def add_frequency_encoding(
    df: pd.DataFrame, cat_cols: List[str]
) -> pd.DataFrame:
    """
    Encode categorical variables using normalized population frequencies.

    Parameters:
    -----------
    df : pd.DataFrame
        Input dataset.
    cat_cols : List[str]
        List of categorical feature names to encode.

    Returns:
    --------
    pd.DataFrame
        DataFrame with appended frequency-encoded features.
    """
    df_out = df.copy()
    for col in cat_cols:
        if col in df_out.columns:
            freq_map = df_out[col].value_counts(normalize=True).to_dict()
            df_out[f"{col}_freq"] = df_out[col].map(freq_map)
    return df_out


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Run end-to-end feature engineering transformations across project dataset.

    Parameters:
    -----------
    df : pd.DataFrame
        Processed dataset from Stage 07/08.

    Returns:
    --------
    pd.DataFrame
        Engineered dataset prepared for downstream modeling.
    """
    df_out = df.copy()
    df_out = add_spend_income_ratio(df_out)
    df_out = add_rolling_features(df_out, target_col="spend", window=7)

    cat_cols = [c for c in ["region"] if c in df_out.columns]
    if cat_cols:
        df_out = add_frequency_encoding(df_out, cat_cols)

    return df_out