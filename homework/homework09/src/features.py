"""
Feature Engineering Utilities Module
Provides reusable transformations including ratio generation, rolling statistics,
and frequency encoding for categorical attributes.
"""

from typing import List, Optional
import pandas as pd
import numpy as np


def add_spend_income_ratio(
    df: pd.DataFrame,
    spend_col: str = "monthly_spend",
    income_col: str = "income",
    output_col: str = "spend_income_ratio",
) -> pd.DataFrame:
    """
    Calculate the ratio of spending relative to income.

    Parameters:
    -----------
    df : pd.DataFrame
        Input dataset containing spend and income columns.
    spend_col : str, default="monthly_spend"
        Column name representing spend volume.
    income_col : str, default="income"
        Column name representing total income.
    output_col : str, default="spend_income_ratio"
        Target column name for the computed ratio.

    Returns:
    --------
    pd.DataFrame
        DataFrame with appended spend-to-income ratio column.
    """
    df_out = df.copy()
    # Avoid division by zero by setting invalid income ratios to NaN
    df_out[output_col] = np.where(
        df_out[income_col] > 0,
        df_out[spend_col] / df_out[income_col],
        np.nan,
    )
    return df_out


def add_rolling_spend_mean(
    df: pd.DataFrame,
    spend_col: str = "monthly_spend",
    window: int = 3,
    output_col: str = "rolling_spend_mean",
) -> pd.DataFrame:
    """
    Compute moving average over a rolling window for historical spend.

    Parameters:
    -----------
    df : pd.DataFrame
        Input dataset with sequential spend data.
    spend_col : str, default="monthly_spend"
        Column name for spend metric.
    window : int, default=3
        Rolling step window size.
    output_col : str, default="rolling_spend_mean"
        Target feature name for calculated rolling mean.

    Returns:
    --------
    pd.DataFrame
        DataFrame with appended rolling mean feature.
    """
    df_out = df.copy()
    df_out[output_col] = (
        df_out[spend_col].rolling(window=window, min_periods=1).mean()
    )
    return df_out


def add_frequency_encoding(
    df: pd.DataFrame,
    cat_col: str = "region",
    output_col: Optional[str] = None,
) -> pd.DataFrame:
    """
    Encode categorical values with their normalized frequency proportions.

    Parameters:
    -----------
    df : pd.DataFrame
        Input dataset containing categorical column.
    cat_col : str, default="region"
        Target categorical feature column name.
    output_col : Optional[str], default=None
        Target encoded column name. Defaults to f"{cat_col}_freq".

    Returns:
    --------
    pd.DataFrame
        DataFrame with appended frequency-encoded feature column.
    """
    df_out = df.copy()
    if output_col is None:
        output_col = f"{cat_col}_freq"

    freq_map = df_out[cat_col].value_counts(normalize=True).to_dict()
    df_out[output_col] = df_out[cat_col].map(freq_map)
    return df_out


def generate_engineered_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Execute end-to-end feature engineering pipeline across input DataFrame.

    Parameters:
    -----------
    df : pd.DataFrame
        Raw or preprocessed dataset.

    Returns:
    --------
    pd.DataFrame
        Dataset transformed with engineered features.
    """
    df_transformed = add_spend_income_ratio(df)
    df_transformed = add_rolling_spend_mean(df_transformed)
    df_transformed = add_frequency_encoding(df_transformed, cat_col="region")
    return df_transformed