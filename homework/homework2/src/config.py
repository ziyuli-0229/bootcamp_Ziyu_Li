import os
from pathlib import Path
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

def get_key(name: str, default: str = None) -> str:
    return os.getenv(name, default)

DATA_DIR = PROJECT_ROOT / get_key("DATA_DIR", "data")