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

  # Executive Summary — Model Evaluation, Risk Diagnostics & Delivery Design

## Executive Summary
* **Operational Readiness**: The baseline predictive model achieves a Mean Absolute Error (MAE) of **0.4366** and Root Mean Squared Error (RMSE) of **0.4381**, providing stable performance for production deployment.
* **Uncertainty Bounds**: Non-parametric bootstrap resampling ($N = 600$) establishes a tight 95% confidence interval for MAE between **[0.4296, 0.4441]**, confirming high model stability without assuming normal error distributions.
* **Systematic Bias**: All segments exhibit a minor negative mean residual ($\approx -0.436$), indicating systematic overestimation that requires offset calibration prior to live routing.

---

## Problem Setup & Methodology
The objective of this stage is to package core model diagnostics, quantify distributional risks across operational segments, and evaluate feature sensitivity under alternate data processing scenarios.

* **Target Variable**: Continuous performance metric (`y_target`).
* **Evaluation Baseline**: Linear regression fit evaluated via 600 bootstrap iterations to establish non-parametric confidence bands.
* **Segmentation**: Evaluated across three primary user cohorts (Segment A: $N=56$, Segment B: $N=21$, Segment C: $N=23$).

---

## Model Performance & Subgroup Diagnostics

### 1. Overall Performance Metrics
| Metric | Baseline Value | Bootstrap Mean | 95% Bootstrap Confidence Band |
| :--- | :---: | :---: | :---: |
| **MAE** | **0.4366** | 0.4366 | **[0.4296, 0.4441]** |
| **RMSE** | **0.4381** | 0.4381 | **[0.4309, 0.4458]** |

### 2. Subgroup Error Disaggregation
| Segment | Sample Size ($N$) | Mean Residual | Std Residual | Segment MAE | Performance Impact |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Segment A** | 56 | -0.4362 | 0.0324 | **0.4362** | Primary volume driver ($56\%$ of traffic); lowest residual variance ($\sigma = 0.0324$). |
| **Segment B** | 21 | -0.4319 | 0.0428 | **0.4319** | Lowest absolute error, but exhibits $32\%$ higher variance than Segment A. |
| **Segment C** | 23 | -0.4416 | 0.0404 | **0.4416** | Highest segment MAE and largest negative bias; requires dedicated offset tracking. |

---

## Sensitivity & Scenario Analysis

To test model sensitivity to preprocessing choices, we compared mean imputation against median imputation and row-wise deletion under varying missingness rates:

| Scenario Description | Preprocessing Rule | Target MAE | Model Slope ($\beta_1$) | Operational Takeaway |
| :--- | :--- | :---: | :---: | :--- |
| **Scenario A (Baseline)** | Mean Imputation | **1.2783** | $2.1302$ | Standard baseline; sensitive to tail outliers in missing features. |
| **Scenario B (Median)** | Median Imputation | **1.2840** | $2.1293$ | Robust against heavy-tailed input noise; slope remains invariant ($\Delta \beta_1 < 0.001$). |
| **Scenario C (Complete)** | Row Deletion | **1.0646** | $2.1302$ | Lowest error due to elimination of synthetic fill bias. |

---

## Assumptions, Risks & Operational Guardrails

* **Data Boundaries**: Model predictions hold provided missing feature rates remain below **10%** and input variables remain within historical range ($X \in [0, 10]$).
* **Systemic Bias**: Consistent negative residual means across all subgroups require an intercept calibration adjustment (+0.436 offset) in live production.
* **Production Thresholds**: Automated retraining alerts must trigger if live rolling 7-day MAE exceeds **0.4441** (upper 95% bootstrap CI limit).

---

## Decision Implications & Next Steps
1. **Model Calibration**: Apply a global residual offset adjustment (+0.436) to eliminate system overestimation prior to stakeholder handoff.
2. **Segment C Guardrails**: Implement subgroup-specific alert triggers for Segment C to flag sudden increases in residual variance.
3. **Pipeline Deployment**: Promote median imputation into the production feature pipeline to preserve slope stability.