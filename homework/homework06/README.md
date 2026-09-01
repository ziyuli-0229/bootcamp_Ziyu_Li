## Data Preprocessing Strategy

### Pipeline Architecture
The data cleaning layer is modularized under `src/cleaning.py` to ensure reproducible pipeline transformations:
1. **Filtering Sparse Features**: `drop_missing()` removes columns exceeding a specified missing value threshold (default threshold: 50%).
2. **Median Imputation**: `fill_missing_median()` fills missing numerical data using robust non-parametric column medians.
3. **Feature Scaling**: `normalize_data()` rescales continuous numerical variables into $[0, 1]$ via Min-Max scaling or standardizes them using Z-score logic.

### Directory Mapping
- `data/raw/sample_data.csv`: Source dataset containing missing values and raw formats.
- `data/processed/sample_data_cleaned.csv`: Cleaned, imputed, and normalized dataset ready for exploratory analysis and modeling.
- `src/cleaning.py`: Production-grade cleaning utility functions with type hints and explicit docstrings.