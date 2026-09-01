"""
Evaluation and Risk Communication Helper Module
Provides functions for bootstrap resampling, confidence interval generation,
scenario sensitivity execution, and subgroup diagnostics.
"""

from typing import Any, Callable, Dict, Tuple
import numpy as np
import pandas as pd


def compute_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
    """Compute baseline regression/evaluation metrics."""
    mae = float(np.mean(np.abs(y_true - y_pred)))
    rmse = float(np.sqrt(np.mean((y_true - y_pred) ** 2)))
    return {"MAE": round(mae, 4), "RMSE": round(rmse, 4)}


def bootstrap_metric_ci(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    metric_fn: Callable = compute_metrics,
    n_boot: int = 600,
    seed: int = 111,
    alpha: float = 0.05,
) -> Dict[str, Dict[str, float]]:
    """
    Perform non-parametric bootstrap resampling to calculate 95% confidence intervals
    for operational metrics.
    """
    rng = np.random.default_rng(seed)
    n = len(y_true)
    boot_stats = []

    for _ in range(n_boot):
        idx = rng.choice(n, size=n, replace=True)
        boot_stats.append(metric_fn(y_true[idx], y_pred[idx]))

    metrics_keys = boot_stats[0].keys()
    ci_results = {}

    for key in metrics_keys:
        vals = [s[key] for s in boot_stats]
        lo, hi = np.percentile(vals, [100 * alpha / 2, 100 * (1 - alpha / 2)])
        ci_results[key] = {
            "mean": round(float(np.mean(vals)), 4),
            "ci_lower": round(float(lo), 4),
            "ci_upper": round(float(hi), 4),
        }

    return ci_results


def evaluate_subgroup_residuals(
    df: pd.DataFrame,
    target_col: str,
    pred_col: str,
    group_col: str,
) -> pd.DataFrame:
    """Compute residual distributions and performance across subgroup segments."""
    df_eval = df.copy()
    df_eval["residual"] = df_eval[target_col] - df_eval[pred_col]
    df_eval["abs_error"] = np.abs(df_eval["residual"])

    subgroup_summary = (
        df_eval.groupby(group_col)
        .agg(
            sample_size=(target_col, "count"),
            mean_residual=("residual", "mean"),
            std_residual=("residual", "std"),
            MAE=("abs_error", "mean"),
        )
        .round(4)
    )

    return subgroup_summary