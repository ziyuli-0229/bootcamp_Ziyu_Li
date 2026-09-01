"""
Stage 11 — Evaluation & Risk Communication Helpers
Provides functions for imputation, linear regression fitting, metric bootstrapping,
and prediction interval generation.
"""

from typing import Any, Dict, Tuple
import numpy as np
import pandas as pd


def mean_impute(a: np.ndarray) -> np.ndarray:
    """Impute missing values in array using mean."""
    m = np.nanmean(a)
    out = a.copy()
    out[np.isnan(out)] = m
    return out


def median_impute(a: np.ndarray) -> np.ndarray:
    """Impute missing values in array using median."""
    m = np.nanmedian(a)
    out = a.copy()
    out[np.isnan(out)] = m
    return out


class SimpleLinReg:
    """Simple OLS Linear Regression fit via Pseudo-Inverse."""

    def fit(self, X: np.ndarray, y: np.ndarray):
        X1 = np.c_[np.ones(len(X)), X.ravel()]
        beta = np.linalg.pinv(X1) @ y
        self.intercept_, self.coef_ = float(beta[0]), np.array(
            [float(beta[1])]
        )
        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        return self.intercept_ + self.coef_[0] * X.ravel()


def mae(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Calculate Mean Absolute Error."""
    return float(np.mean(np.abs(y_true - y_pred)))


def fit_fn(X: np.ndarray, y: np.ndarray) -> SimpleLinReg:
    return SimpleLinReg().fit(X, y)


def pred_fn(model: Any, X: np.ndarray) -> np.ndarray:
    return model.predict(X)


def bootstrap_metric(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    fn: Any = mae,
    n_boot: int = 600,
    seed: int = 111,
    alpha: float = 0.05,
) -> Dict[str, float]:
    """Resample predictions with replacement to generate percentile-based CIs."""
    rng = np.random.default_rng(seed)
    idx = np.arange(len(y_true))
    stats = []
    for _ in range(n_boot):
        b = rng.choice(idx, size=len(idx), replace=True)
        stats.append(fn(y_true[b], y_pred[b]))
    lo, hi = np.percentile(stats, [100 * alpha / 2, 100 * (1 - alpha / 2)])
    return {
        "mean": float(np.mean(stats)),
        "lo": float(lo),
        "hi": float(hi),
    }


def bootstrap_predictions(
    X: np.ndarray,
    y: np.ndarray,
    x_grid: np.ndarray,
    n_boot: int = 600,
    seed: int = 111,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Bootstrap regression fit lines to construct non-parametric prediction CIs."""
    rng = np.random.default_rng(seed)
    preds = []
    idx = np.arange(len(y))
    for _ in range(n_boot):
        b = rng.choice(idx, size=len(idx), replace=True)
        m = fit_fn(X[b].reshape(-1, 1), y[b])
        preds.append(m.predict(x_grid))
    P = np.vstack(preds)
    return (
        P.mean(axis=0),
        np.percentile(P, 2.5, axis=0),
        np.percentile(P, 97.5, axis=0),
    )