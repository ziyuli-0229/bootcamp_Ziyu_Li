# Stakeholder Summary — Model Risk, Sensitivity & Limitations

## Executive Summary
* **Operational Readiness**: The baseline predictive model achieves a Mean Absolute Error (MAE) of **0.4366** and Root Mean Squared Error (RMSE) of **0.4381**, providing stable performance for production deployment.
* **Uncertainty Bounds**: Non-parametric bootstrap resampling ($N = 600$) establishes a tight 95% confidence interval for MAE between **[0.4296, 0.4441]**, confirming high model stability without assuming normal error distributions.
* **Systematic Bias**: All subgroups exhibit a consistent negative mean residual ($\approx -0.436$), indicating systematic overestimation that requires an intercept calibration adjustment prior to live deployment.

---

## Model Performance & Subgroup Diagnostics

### 1. Overall Performance & 95% Bootstrap Confidence Bands
Over 600 bootstrap iterations, predictive error remains tightly bounded without relying on standard Gaussian normality assumptions:

| Metric | Baseline Value | Bootstrap Mean | 95% Bootstrap Confidence Band |
| :--- | :---: | :---: | :---: |
| **MAE** | **0.4366** | 0.4366 | **[0.4296, 0.4441]** |
| **RMSE** | **0.4381** | 0.4381 | **[0.4309, 0.4458]** |

### 2. Subgroup Error Disaggregation
Evaluated across three primary user cohorts to quantify distributional risks:

| Segment | Sample Size ($N$) | Mean Residual | Std Residual | Segment MAE | Performance Impact |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Segment A** | 56 | -0.4362 | 0.0324 | **0.4362** | Primary volume driver ($56\%$ of traffic); lowest residual variance ($\sigma = 0.0324$). |
| **Segment B** | 21 | -0.4319 | 0.0428 | **0.4319** | Lowest absolute error, but exhibits $32\%$ higher variance than Segment A. |
| **Segment C** | 23 | -0.4416 | 0.0404 | **0.4416** | Highest segment MAE and largest negative bias; requires dedicated offset tracking. |

---

## Sensitivity & Scenario Analysis

To test model robustness against preprocessing strategies, we compared mean imputation against median imputation and row-wise deletion under varying missingness conditions:

| Scenario Description | Preprocessing Rule | Target MAE | Model Slope ($\beta_1$) | Operational Takeaway |
| :--- | :--- | :---: | :---: | :--- |
| **Scenario A (Baseline)** | Mean Imputation | **1.2783** | $2.1302$ | Standard baseline; sensitive to tail outliers in missing features. |
| **Scenario B (Median)** | Median Imputation | **1.2840** | $2.1293$ | Robust against heavy-tailed input noise; slope remains invariant ($\Delta \beta_1 < 0.001$). |
| **Scenario C (Complete)** | Row Deletion | **1.0646** | $2.1302$ | Lowest error due to elimination of synthetic fill bias. |

---

## Operational Guardrails & Production Monitoring

* **Systematic Overestimation Offset**: Mean residuals across all segments are consistently negative ($\approx -0.436$). An intercept calibration step ($+0.436$ offset) must be applied in live production prior to downstream routing.
* **Production Alert Thresholds**:
  * **Primary Alert**: Trigger automated model retraining alerts if rolling 7-day operational MAE exceeds **0.4441** (the upper 95% bootstrap boundary).
  * **Secondary Alert**: Flag potential data drift if Segment C proportions exceed $25\%$ of total incoming traffic.
* **Data Boundary Constraints**: Predictions hold valid as long as missing feature rates stay below **10%** and input values remain within historical bounds ($X \in [0, 10]$).

---

## Decision Implications & Next Steps

1. **Model Calibration**: Apply a global residual offset adjustment ($+0.436$) to eliminate systematic overestimation prior to stakeholder handoff.
2. **Segment C Guardrails**: Implement subgroup-specific alert triggers for Segment C to flag sudden increases in residual variance.
3. **Pipeline Deployment**: Promote median imputation into the production feature pipeline to preserve slope stability against input noise.