# Stage 14 — On-Call Handoff Plan

This document provides on-call operators with the deployment path, operational runbooks, and emergency response procedures for the prediction service.

* **Deployment Architecture Path:** Local Flask application (`app.py`) -> Docker Containerized Microservice -> Kubernetes/GCP Cloud Run deployment with load balancing.
* **Service Healthcheck:** Verify HTTP 200 response via `GET http://127.0.0.1:5000/predict/0.1/0.2`.
* **System Emergency Runbook:** If p95 latency > 250ms or 5xx errors spike, check container health via `docker logs app` and restart service using `docker-compose restart`.
* **Model Rollback Runbook:** If model predictions fail business validation, restore previous pickled binary from `model/model_v1.pkl` and restart `app.py`.
* **Data Pipeline Incident Runbook:** If 400 Bad Request errors spike, inspect client payload logs in Jira `PROD-ML` and notify Data Engineering.
* **Monitoring Dashboard Link:** Access Grafana metrics dashboard at `http://grafana.internal/d/ml-model-stage14`.
* **Escalation Path:** Primary On-call -> Platform DevOps (`#ops-alerts`) -> Lead Data Scientist (`#ds-team`).
