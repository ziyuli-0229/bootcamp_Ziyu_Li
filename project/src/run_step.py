import argparse
import json
import logging
import sys
import time
from datetime import datetime
from pathlib import Path


def retry(n_tries: int = 3, delay: float = 0.5):
    """Decorator to retry a function upon failure using linear backoff."""
    def decorator(fn):
        def wrapper(*args, **kwargs):
            for attempt in range(1, n_tries + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    logging.warning(
                        f"[Retry] Attempt {attempt}/{n_tries} failed for function '{fn.__name__}': {e}"
                    )
                    if attempt == n_tries:
                        logging.error(f"[Retry] Max retries reached for '{fn.__name__}'. Escalating error.")
                        raise
                    time.sleep(delay * attempt)
        return wrapper
    return decorator


@retry(n_tries=3, delay=0.5)
def process_data_step(input_path: str, output_path: str) -> None:
    """Reads input data, applies transformation logic, and writes output artifact."""
    logging.info(f"[process_data_step] Starting execution with input: {input_path}")
    
    in_file = Path(input_path)
    if not in_file.exists():
        raise FileNotFoundError(f"Input file not found at: {input_path}")

    # Read input payload
    raw_content = in_file.read_text(encoding="utf-8")
    logging.info(f"[process_data_step] Successfully read input artifact ({len(raw_content)} bytes)")

    # Execute processing / transformation logic
    processed_payload = {
        "processed_at": datetime.utcnow().isoformat(),
        "source_file": str(in_file.resolve()),
        "status": "success",
        "data_summary": f"Processed content length: {len(raw_content)}"
    }

    # Ensure output destination directory exists
    out_file = Path(output_path)
    out_file.parent.mkdir(parents=True, exist_ok=True)

    # Write checkpoint output
    out_file.write_text(json.dumps(processed_payload, indent=2), encoding="utf-8")
    logging.info(f"[process_data_step] Successfully wrote checkpoint artifact to: {output_path}")


def main(argv=None):
    """CLI Argument Parser entry point."""
    parser = argparse.ArgumentParser(description="CLI Runner for Stage 15 Orchestration Task")
    parser.add_argument("--input", required=True, help="Path to input data file")
    parser.add_argument("--output", required=True, help="Path to output target file")
    
    args = parser.parse_args(argv)

    # Configure stdout logging format
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)]
    )

    process_data_step(args.input, args.output)


if __name__ == "__main__":
    main()