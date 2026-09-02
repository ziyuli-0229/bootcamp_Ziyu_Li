# Data Science Lifecycle Framework Guide

| Stage # | Lifecycle Stage | Repo File / Folder Path | Key Decision / Outcome |
| :--- | :--- | :--- | :--- |
| **01** | Problem Framing | `docs/problem_framing.md` | Defined core objective: predict price anomalies and evaluate pipeline consistency. |
| **02** | Data Acquisition | `data/raw/data.csv` | Sourced raw transactional price dataset; established automated ingestion scripts. |
| **03** | Data Cleaning | `src/clean.py` | Removed duplicate records, imputed missing numeric fields using median strategies. |
| **04** | Exploratory Analysis | `notebooks/eda.ipynb` | Identified right-skewed price distributions and seasonal variance in input features. |
| **05** | Feature Engineering | `src/features.py` | Created rolling-window averages and log-transformed highly skewed numerical features. |
| **06** | Model Training | `src/train.py` | Selected baseline Random Forest / XGBoost regressors for price estimation. |
| **07** | Model Evaluation | `reports/metrics.json` | Evaluated models using RMSE and MAE; established standard performance benchmarks. |
| **08** | Error Analysis | `notebooks/error_analysis.ipynb` | Discovered higher prediction errors in top 5% extreme price ranges. |
| **09** | Stakeholder Delivery | `reports/final_presentation.pdf` | Designed non-technical metric dashboards and executive summary slides. |
| **10** | Model Packaging | `models/model.json` | Serialized model parameters and preprocessing artifacts for downstream loading. |
| **11** | Code Refactoring | `src/pipeline.py` | Converted exploratory notebook cells into reusable Python modules with clear modular functions. |
| **12** | API / CLI Design | `src/run_step.py` | Built standard `argparse` CLI interfaces for execution automation. |
| **13** | Testing & Validation | `tests/test_pipeline.py` | Implemented unit tests for input schema assertion and basic transformation consistency. |
| **14** | Monitoring Strategy | `docs/monitoring_plan.md` | Defined logging schedules, schema validation rules, and data drift threshold alerts. |
| **15** | Orchestration & DAG | `docs/orchestration_plan.md` | Structured task dependencies into a DAG and implemented execution retry decorators. |
| **16** | Lifecycle Review | `docs/project_summary.md` | Consolidated lifecycle documentation, cleaned repo layout, and verified full reproducibility. |