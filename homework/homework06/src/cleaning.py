"""
Data Cleaning and Preprocessing Utilities Module
Provides reusable functions for missing value handling and data normalization.
"""

from typing import List, Optional
import pandas as pd
import numpy as np


def fill_missing_median(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    """
    Imputes missing values in specified numeric columns using column median values.

    Parameters:
    -----------
    df : pd.DataFrame
        Input DataFrame to process.
    columns : List[str]
        List of numeric column names for median imputation.

    Returns:
    --------
    pd.DataFrame
        DataFrame with missing values imputed in target columns.
    """
    df_out = df.copy()
    for col in columns:
        if col in df_out.columns:
            median_val = df_out[col].median()
            df_out[col] = df_out[col].fillna(median_val)
    return df_out


def drop_missing(
    df: pd.DataFrame,
    threshold: Optional[float] = None,
    columns: Optional[List[str]] = None,
) -> pd.DataFrame:
    """
    Drops columns exceeding a missingness threshold or drops rows missing critical values.

    Parameters:
    -----------
    df : pd.DataFrame
        Input DataFrame.
    threshold : Optional[float]
        Maximum allowed fraction of missing values per column (0.0 to 1.0).
        Columns exceeding this missingness ratio are dropped.
    columns : Optional[List[str]]
        List of critical columns; rows containing NaN in these columns are dropped.

    Returns:
    --------
    pd.DataFrame
        DataFrame with filtered columns and rows.
    """
    df_out = df.copy()

    # Drop columns exceeding maximum missingness ratio
    if threshold is not None:
        max_missing_count = len(df_out) * threshold
        cols_to_drop = [
            c for c in df_out.columns if df_out[c].isna().sum() > max_missing_count
        ]
        df_out = df_out.drop(columns=cols_to_drop)

    # Drop rows missing critical column values
    if columns is not None:
        valid_cols = [c for c in columns if c in df_out.columns]
        df_out = df_out.dropna(subset=valid_cols)

    return df_out


def normalize_data(
    df: pd.DataFrame, columns: List[str], method: str = "minmax"
) -> pd.DataFrame:
    """
    Scales numeric feature distributions using Min-Max scaling or Z-score standardization.

    Min-Max Scaling formula:
    $$x' = \\frac{x - x_{min}}{x_{max} - x_{min}}$$

    Parameters:
    -----------
    df : pd.DataFrame
        Input DataFrame.
    columns : List[str]
        List of numeric columns to scale.
    method : str
        Scaling algorithm: 'minmax' (range 0 to 1) or 'zscore' (mean 0, std 1).

    Returns:
    --------
    pd.DataFrame
        DataFrame containing normalized numeric columns.
    """
    df_out = df.copy()
    for col in columns:
        if col in df_out.columns and pd.api.types.is_numeric_dtype(df_out[col]):
            if method == "minmax":
                min_val = df_out[col].min()
                max_val = df_out[col].max()
                if max_val != min_val:
                    df_out[col] = (df_out[col] - min_val) / (max_val - min_val)
            elif method == "zscore":
                mean_val = df_out[col].mean()
                std_val = df_out[col].std()
                if std_val != 0:
                    df_out[col] = (df_out[col] - mean_val) / std_val
    return df_out