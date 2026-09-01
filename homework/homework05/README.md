## Data Storage Strategy

### Directory Architecture
The data layer isolates raw ingested datasets from processed, optimized data assets:
- `data/raw/`: Read-only landing zone for immutable source files (stored as CSV).
- `data/processed/`: Optimized target directory for cleaned and structured data (stored as Parquet).

### Storage Formats & Rationale
- **CSV (`data/raw/`)**: Used for incoming raw data due to human readability and broad system compatibility.
- **Parquet (`data/processed/`)**: Used for processed analytical layers due to efficient columnar storage, fast I/O throughput, schema enforcement, and native preservation of data types (`datetime64`, `float64`).

### Environment-Driven I/O Configuration
Storage directories are decoupled from source code using environment variables configured in `.env`:
```text
DATA_DIR_RAW=data/raw
DATA_DIR_PROCESSED=data/processed