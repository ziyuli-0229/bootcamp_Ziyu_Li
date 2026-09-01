import os
import pandas as pd
from pathlib import Path

def get_summary_stats(df: pd.DataFrame, group_col: str = None) -> pd.DataFrame:
    """
    Calculate basic summary statistics for numerical columns in a DataFrame.
    Optionally performs groupby aggregation if group_col is provided.
    """
    if group_col and group_col in df.columns:
        return df.groupby(group_col).mean(numeric_only=True).reset_index()
    return df.describe()

def save_dataframe(df: pd.DataFrame, output_path: str) -> None:
    """
    Ensure destination directory exists and save DataFrame as CSV.
    """
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    print(f"Data successfully saved to {path.resolve()}")