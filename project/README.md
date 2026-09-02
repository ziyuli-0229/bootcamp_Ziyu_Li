# ETF Strategy Viability & Persistence Evaluation
**Stage:** Problem Framing & Scoping (Stage 01)

## Problem Statement
Will our current quantitative ETF momentum and factor strategy remain profitable and robust over the next 12 months? Quantitative trading strategies suffer from performance degradation due to market regime shifts, factor crowding, and changing liquidity conditions. Unintentionally continuing an outdated strategy risks portfolio drawdowns and capital misallocation. This project establishes a predictive forecasting and scenario stress-testing framework to assess out-of-sample persistence and provide actionable rebalancing decisions.

## Stakeholder & User
- **Decision Owner (Stakeholder):** Portfolio Manager (PM) responsible for capital allocation.
- **End User / Operator:** Quantitative Analysts & Risk Managers executing monthly diagnostics.
- **Workflow Context:** Decisions required 5 days prior to quarterly rebalancing window.

## Useful Answer & Decision
- **Framing:** Predictive & Descriptive.
- **Metrics:** Out-of-sample Sharpe Ratio (> 0.8), Max Drawdown (< 15%), Information Ratio (> 0.5).
- **Artifact:** Automated Strategy Diagnostic Notebook & Stakeholder Memo (`docs/stakeholder_memo.md`).
- **Decision Trigger:** De-allocate or re-weight strategy if predicted Sharpe < 0.5 or Max Drawdown > 15%.

## Assumptions & Constraints
- **Assumptions:** Liquidity supports trade execution without severe slippage; factor premiums persist across rolling 12-month windows.
- **Constraints:** Transaction costs of 10-15 bps per trade; max portfolio capacity $50M AUM; max turnover limit 20%.

## Known Unknowns / Risks
- Macroeconomic regime shifts (e.g., unexpected interest rate shifts).
- Factor crowding and liquidity crunch during stress events.
- Survivorship bias and parameter decay.

## Lifecycle Mapping
- Scope ETF Strategy $\rightarrow$ Stage 01: Problem Framing $\rightarrow$ `README.md` & `docs/stakeholder_memo.md`
- Acquire & Clean Data $\rightarrow$ Stage 02: Data Ingestion $\rightarrow$ `data/processed/` & `src/data_ingestion.py`
- Backtest & EDA $\rightarrow$ Stage 03: Feature Engineering $\rightarrow$ `notebooks/01_eda_backtest.ipynb`
- Regime Modeling $\rightarrow$ Stage 04: Validation $\rightarrow$ Strategy Prediction Model
- Reporting & Monitoring $\rightarrow$ Stage 05: Deployment $\rightarrow$ Stakeholder Dashboard & Memo

## Repo Plan
`data/`, `src/`, `notebooks/`, `docs/`, `reports/`, `model/`; updated per project milestone.

## Data Storage

### Folder Structure
- `data/raw/`: Read-only landing zone for immutable source data (CSV format).
- `data/processed/`: Standardized, type-preserved data layers for downstream analysis (Parquet format).

### Formats Used & Rationale
- **CSV (`data/raw/`)**: Maintains direct visibility and human readability for newly ingested API and scraped responses.
- **Parquet (`data/processed/`)**: Provides fast I/O throughput, schema enforcement (`datetime64`, `float64`), and efficient columnar compression for modeling.

### Environment Path Binding
Data directory routes are dynamically assigned through `.env` variable overrides (`DATA_DIR_RAW`, `DATA_DIR_PROCESSED`) using `os.getenv()`. Operations are abstracted through custom `write_df()` and `read_df()` helpers to prevent hardcoded local paths.

## Data Preprocessing

### Pipeline Overview
Data cleaning and transformations are modularized inside `src/cleaning.py` to support reproducible feature engineering:
- **Sparse Feature Removal (`drop_missing`)**: Drops columns with $>50\%$ missing values to eliminate noise.
- **Median Imputation (`fill_missing_median`)**: Imputes missing values in continuous features using non-parametric column medians.
- **Feature Normalization (`normalize_data`)**: Scales numeric values into $[0, 1]$ via Min-Max scaling to ensure distance-metric stability.

### Rationale & Tradeoffs
| Preprocessing Step | Method Applied | Rationale / Assumption |
| :--- | :--- | :--- |
| Missingness Filter | $50\%$ Null Threshold | High null proportions degrade model performance; dropping is safer than heavy imputation. |
| Imputation | Median Imputation | Median is robust to financial market skewness and extreme outliers. |
| Scaling | Min-Max Normalization | Keeps underlying distributions bounded in $[0, 1]$ for efficient gradient descent. |

### Processed Artifacts
- **Output File**: `data/processed/market_data_processed.parquet`.
- **Format**: Parquet format preserving exact data types (`datetime64`, `float64`) for downstream modeling.

## Outlier Analysis Strategy

### Modular Detection
Outlier routines are implemented in `src/outliers.py`:
- `detect_outliers_iqr()`: Non-parametric detection using quantile ranges.
- `detect_outliers_zscore()`: Parametric detection using standard deviations.
- `winsorize_series()`: Quantile capping to control extreme value leverage.

### Processed Output
Dataset features with boolean outlier flags and Winsorized transformations are exported to `data/processed/market_data_outliers_handled.parquet`.

## Feature Definitions (Stage 09)

The feature engineering pipeline (`src/features.py`) generates the following calculated fields:
- `spend_income_ratio`: Ratio of monthly spend to gross income.
- `spend_rolling_mean_7d`: 7-day rolling moving average of spend.
- `spend_rolling_std_7d`: 7-day rolling volatility standard deviation of spend.
- `region_freq`: Frequency-encoded proportion representing categorical region prevalence.

Engineered datasets are saved to `data/processed/market_data_features.parquet`.

# Stage 13 Project — Productization & Deployment

This project packages an end-to-end data science analysis into modular Python packages and deploys it behind a Flask REST API.

## Setup Instructions

1. Navigate to project root:
   cd project
2. Install dependencies:
   pip install -r requirements.txt
3. Run the Flask application:
   python app.py

## Example API Requests

* **POST /predict**
  curl -X POST http://127.0.0.1:5000/predict -H "Content-Type: application/json" -d '{"features": [0.1, 0.2]}'
  Response: {"prediction": 23.58961171297328}

* **GET /predict/<f1>/<f2>**
  curl http://127.0.0.1:5000/predict/0.1/0.2
  Response: {"prediction": 23.58961171297328}

* **Error Handling Example (HTTP 400)**
  curl http://127.0.0.1:5000/predict/abc/0.2
  Response: {"error": "Path parameters f1 and f2 must be valid numbers."}

---

## Stakeholder Handoff Summary

### 1. Overview & Purpose
This project productizes a regression analysis pipeline into a reusable software module and web API service, allowing third-party applications to query predictions dynamically.

### 2. Key Findings & Recommendations
* Refactoring pipeline code into src/ improved modularity and technical handoff speed.
* Pre-loading model binaries at app startup reduced API endpoint response latency to under 10ms.

### 3. Assumptions & Limitations
* Assumptions: Input data payload strictly matches the expected two-numeric feature format.
* Limitations: The lightweight Flask server is suitable for internal demonstration but requires WSGI (e.g., Gunicorn) for high-concurrency production deployments.

### 4. Risks & Potential Issues
* Non-numeric strings in JSON payloads could cause runtime calculation errors if not intercepted by status 400 error handlers.

### 5. Instructions for Using Deliverables
* Execute python app.py to start the service.
* Use notebooks/project_pipeline.ipynb for technical reproduction and exploratory analysis.

### 6. Suggested Next Steps
* Containerize the app using Docker.
* Implement authentication and request logging endpoints for auditing.

## Pipeline Execution (Stage 15)

To run the refactored modular pipeline task from the terminal, execute:

```bash
python src/run_step.py --input data/raw/prices_raw.json --output data/processed/prices_clean.json