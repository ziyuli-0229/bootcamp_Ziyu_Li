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
- **CSV (`data/raw/`)**: Maintains direct visibility and human readability for newly ingested API and scraped responses[cite: 4].
- **Parquet (`data/processed/`)**: Provides fast I/O throughput, schema enforcement (`datetime64`, `float64`), and efficient columnar compression for modeling.

### Environment Path Binding
Data directory routes are dynamically assigned through `.env` variable overrides (`DATA_DIR_RAW`, `DATA_DIR_PROCESSED`) using `os.getenv()`[cite: 4]. Operations are abstracted through custom `write_df()` and `read_df()` helpers to prevent hardcoded local paths[cite: 4].

## Data Preprocessing

### Pipeline Overview
Data cleaning and transformations are modularized inside `src/cleaning.py` to support reproducible feature engineering[cite: 7]:
- **Sparse Feature Removal (`drop_missing`)**: Drops columns with $>50\%$ missing values to eliminate noise[cite: 7].
- **Median Imputation (`fill_missing_median`)**: Imputes missing values in continuous features using non-parametric column medians[cite: 7].
- **Feature Normalization (`normalize_data`)**: Scales numeric values into $[0, 1]$ via Min-Max scaling to ensure distance-metric stability[cite: 7].

### Rationale & Tradeoffs
| Preprocessing Step | Method Applied | Rationale / Assumption |
| :--- | :--- | :--- |
| Missingness Filter | $50\%$ Null Threshold | High null proportions degrade model performance; dropping is safer than heavy imputation[cite: 7]. |
| Imputation | Median Imputation | Median is robust to financial market skewness and extreme outliers[cite: 7]. |
| Scaling | Min-Max Normalization | Keeps underlying distributions bounded in $[0, 1]$ for efficient gradient descent[cite: 7]. |

### Processed Artifacts
- **Output File**: `data/processed/market_data_processed.parquet`[cite: 7].
- **Format**: Parquet format preserving exact data types (`datetime64`, `float64`) for downstream modeling[cite: 7].