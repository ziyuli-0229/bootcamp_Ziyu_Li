# Stage 14 — Deployment & Monitoring Plan

This document outlines the production monitoring framework, failure modes, metrics, alert routing, and ownership for the prediction service.

## 1. Failure Modes & 4-Layer Monitoring Metrics

| Layer | Failure Mode | Metric & Starting Threshold | Alert Recipient | Runbook First Step |
| :--- | :--- | :--- | :--- | :--- |
| **Data** | Schema drift / missing values | Null rate > 2% OR schema hash mismatch | Data Engineering On-call | Check upstream ETL pipeline logs |
| **Model** | Prediction accuracy decay | 2-week rolling MAE > 5.0 OR feature PSI > 0.10 | Lead Data Scientist | Trigger model evaluation on new ground truth |
| **System** | High latency / server overload | p95 latency > 250ms OR HTTP 5xx rate > 1% | DevOps / Platform On-call | Check Flask CPU/memory and restart container |
| **Business** | Anomaly in prediction output | Monthly prediction average shift > 15% | Product Manager / Analyst | Audit distribution shift vs. market conditions |

## 2. Retraining Cadence & Triggers
* **Scheduled Cadence:** Automatic monthly model retraining on the 1st of each month using the latest 90 days of data.
* **Event-Driven Triggers:** Immediate retraining initiated if feature Population Stability Index (PSI) exceeds 0.15 or 2-week rolling MAE degrades by > 20%.

## 3. Ownership & Governance
* **Dashboard Maintenance:** Data Science Team updates metrics and monitoring dashboards bi-weekly.
* **Rollback Approval:** Lead Data Scientist approves model rollbacks to previous `model.pkl` binaries.
* **Issue Tracking:** All production incidents logged in Jira under the `PROD-ML` queue.
