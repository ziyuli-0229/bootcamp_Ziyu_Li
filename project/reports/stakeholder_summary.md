# Stakeholder Summary — Model Risk, Sensitivity & Limitations

## Executive Summary
This document provides an evaluation of the baseline modeling pipeline using non-parametric bootstrap resampling ($N = 600$) and subgroup residual diagnostics on the project dataset. Predictive metrics and risk boundaries are documented to establish production monitoring guardrails.

---

## Model Performance & Uncertainty Boundaries

* **Baseline Predictive Accuracy**: The primary baseline pipeline achieves a Mean Absolute Error (MAE) of **0.4366** and a Root Mean Squared Error (RMSE) of **0.4381**.
* **95% Bootstrap Confidence Intervals**: Non-parametric bootstrap resampling over 600 iterations yields tight 95% confidence bounds:
  * **MAE 95% CI**: **[0.4296, 0.4441]**
  * **RMSE 95% CI**: **[0.4309, 0.4458]**
* **Uncertainty Takeaway**: The narrow confidence interval demonstrates that prediction error is highly bounded and stable across resampling draws without relying on standard Gaussian normality assumptions.

---

## Subgroup Diagnostic Analysis

| Segment | Sample Size ($N$) | Mean Residual | Std Residual | Segment MAE | Performance Takeaway |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Segment A** | 56 | -0.4362 | 0.0324 | **0.4362** | Dominant segment ($56\%$ of sample); displays lowest error variance ($\sigma = 0.0324$). |
| **Segment B** | 21 | -0.4319 | 0.0428 | **0.4319** | Lowest segment MAE, though residual volatility is $32\%$ higher than Segment A. |
| **Segment C** | 23 | -0.4416 | 0.0404 | **0.4416** | Highest prediction error and largest negative bias (mean residual = -0.4416). |

---

## Operational Guardrails & Production Monitoring

* **Systematic Overestimation Bias**: Mean residuals across all segments are consistently negative ($\approx -0.436$), indicating the baseline fit systematically overpredicts target values. A model calibration step (offset adjustment) is recommended before live deployment.
* **Segment Risk**: Segment C underperforms relative to Segments A and B, suggesting potential unobserved cohort heterogeneity.
* **Production Alert Thresholds**:
  * **Primary Alert**: Trigger automated model retraining alerts if rolling operational MAE exceeds **0.4441** (the upper 95% bootstrap boundary).
  * **Secondary Alert**: Flag data drift if Segment C proportions exceed $25\%$ of incoming traffic.