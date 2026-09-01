"""
Data Cleaning and Preprocessing Module
Contains reusable functions for missing value imputation, column filtering,
and feature scaling across project datasets.
"""

from typing import List, Optional
import numpy as np
import pandas as pd


def drop_missing(df: pd.DataFrame, threshold: float = 0.5) -> pd.DataFrame:
    """
    Drop columns where the ratio of missing values exceeds the specified threshold.

    Parameters:
    -----------
    df : pd.DataFrame
        Input DataFrame.
    threshold : float, default=0.5
        Maximum allowable missingness ratio (0.0 to 1.0).

    Returns:
    --------
    pd.DataFrame
        DataFrame with sparse columns removed.
    """
    df_clean = df.copy()
    max_missing_count = len(df_clean) * threshold
    cols_to_drop = [
        col
        for col in df_clean.columns
        if df_clean[col].isna().sum() > max_missing_count
    ]
    return df_clean.drop(columns=cols_to_drop)


def fill_missing_median(
    df: pd.DataFrame, columns: Optional[List[str]] = None
) -> pd.DataFrame:
    """
    Impute missing numerical values using column median calculations.

    Parameters:
    -----------
    df : pd.DataFrame
        Input DataFrame.
    columns : Optional[List[str]], default=None
        Target column names. Imputes all numeric columns if set to None.

    Returns:
    --------
    pd.DataFrame
        DataFrame with imputed numeric features.
    """
    df_clean = df.copy()
    target_cols = (
        columns
        if columns is not None
        else df_clean.select_dtypes(include=[np.number]).columns
    )

    for col in target_cols:
        if col in df_clean.columns:
            median_val = df_clean[col].median()
            df_clean[col] = df_clean[col].fillna(median_val)
    return df_clean


def normalize_data(
    df: pd.DataFrame, columns: List[str], method: str = "minmax"
) -> pd.DataFrame:
    """
    Scale continuous numeric features using Min-Max scaling or Z-Score standardization.

    Parameters:
    -----------
    df : pd.DataFrame
        Input DataFrame.
    columns : List[str]
        List of numeric column names to normalize.
    method : str, default='minmax'
        Scaling method ('minmax' or 'zscore').

    Returns:
    --------
    pd.DataFrame
        DataFrame containing normalized numeric columns.
    """
    df_clean = df.copy()
    for col in columns:
        if col in df_clean.columns and pd.api.types.is_numeric_dtype(
            df_clean[col]
        ):
            if method == "minmax":
                min_val = df_clean[col].min()
                max_val = df_clean[col].max()
                if max_val != min_val:
                    df_clean[col] = (df_clean[col] - min_val) / (
                        max_val - min_val
                    )
            elif method == "zscore":
                mean_val = df_clean[col].mean()
                std_val = df_clean[col].std()
                if std_val != 0:
                    df_clean[col] = (df_clean[col] - mean_val) / std_val
    return df_clean


def preprocess_pipeline(
    df: pd.DataFrame, numeric_cols: Optional[List[str]] = None
) -> pd.DataFrame:
    """
    Execute end-to-end cleaning and normalization pipeline sequentially.

    Parameters:
    -----------
    df : pd.DataFrame
        Raw input DataFrame.
    numeric_cols : Optional[List[str]]
        Specific numerical columns to normalize.

    Returns:
    --------
    pd.DataFrame
        Cleaned, imputed, and scaled DataFrame ready for modeling.
    """
    df_clean = drop_missing(df, threshold=0.5)
    df_clean = fill_missing_median(df_clean, columns=numeric_cols)
    if numeric_cols:
        df_clean = normalize_data(
            df_clean, columns=numeric_cols, method="minmax"
        )
    return df_clean