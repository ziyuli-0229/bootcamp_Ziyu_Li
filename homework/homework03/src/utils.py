import pandas as pd

def get_summary_stats(df: pd.DataFrame, group_col: str = None) -> pd.DataFrame:
    """
    Calculate descriptive statistics or category aggregations for a DataFrame.

    Args:
        df (pd.DataFrame): Input DataFrame to summarize.
        group_col (str, optional): Column name to perform groupby aggregation. Defaults to None.

    Returns:
        pd.DataFrame: DataFrame containing numeric summary stats or group means.
    """
    if group_col and group_col in df.columns:
        summary = df.groupby(group_col).mean(numeric_only=True)
    else:
        summary = df.describe()
        
    return summary