"""
Exploratory Data Analysis (EDA) Module
Provides automated profiling and data quality diagnostic helpers.
"""

from typing import Optional
import numpy as np
import pandas as pd
from scipy.stats import kurtosis, skew


def eda_summary(
    df: pd.DataFrame,
    missing_threshold: float = 0.20,
    dominant_cat_threshold: float = 0.90,
) -> pd.DataFrame:
    """
    Generate a comprehensive profiling summary table for a DataFrame.

    Flags columns requiring attention before downstream feature engineering
    (high missingness, low variance, or heavily lopsided categories).

    Parameters:
    -----------
    df : pd.DataFrame
        Input DataFrame to profile.
    missing_threshold : float, default=0.20
        Ratio above which missingness is flagged (0.0 to 1.0).
    dominant_cat_threshold : float, default=0.90
        Ratio above which a single category is considered dominating.

    Returns:
    --------
    pd.DataFrame
        Summary table with dtypes, missingness, unique counts, skew, and warnings.
    """
    summary_rows = []
    total_rows = len(df)

    for col in df.columns:
        col_data = df[col]
        dtype = col_data.dtype
        null_count = col_data.isna().sum()
        null_pct = null_count / total_rows if total_rows > 0 else 0.0
        n_unique = col_data.nunique(dropna=True)

        # Initialize parametric metrics
        col_skew = np.nan
        col_kurt = np.nan
        top_val = None
        top_freq_pct = np.nan

        # Categorical profiling
        if not pd.api.types.is_numeric_dtype(col_data) or n_unique <= 2:
            val_counts = col_data.value_counts(dropna=True)
            if not val_counts.empty:
                top_val = val_counts.index[0]
                top_freq_pct = val_counts.iloc[0] / total_rows

        # Numeric profiling
        if pd.api.types.is_numeric_dtype(col_data) and not col_data.dropna().empty:
            clean_num = col_data.dropna()
            if len(clean_num) > 2:
                col_skew = float(skew(clean_num))
                col_kurt = float(kurtosis(clean_num))

        # Data quality flags
        high_missing = null_pct > missing_threshold
        lopsided_cat = top_freq_pct > dominant_cat_threshold if pd.notna(top_freq_pct) else False
        near_zero_var = (n_unique <= 1) or (pd.api.types.is_numeric_dtype(col_data) and col_data.var() == 0)

        flag_list = []
        if high_missing:
            flag_list.append("HIGH_MISSING")
        if lopsided_cat:
            flag_list.append("DOMINANT_CATEGORY")
        if near_zero_var:
            flag_list.append("ZERO_VARIANCE")

        attention_flag = ", ".join(flag_list) if flag_list else "OK"

        summary_rows.append(
            {
                "column": col,
                "dtype": dtype,
                "null_count": null_count,
                "null_pct": round(null_pct, 4),
                "n_unique": n_unique,
                "top_value": top_val,
                "top_value_pct": round(top_freq_pct, 4) if pd.notna(top_freq_pct) else np.nan,
                "skewness": round(col_skew, 4) if pd.notna(col_skew) else np.nan,
                "kurtosis": round(col_kurt, 4) if pd.notna(col_kurt) else np.nan,
                "attention_flag": attention_flag,
            }
        )

    return pd.DataFrame(summary_rows).set_index("column")