import os
from pathlib import Path
from dotenv import load_dotenv

def load_env():
    """Load environment variables from .env file."""
    load_dotenv()

def get_key(name: str, default=None):
    """Retrieve environment variable by name."""
    return os.getenv(name, default)

# Resolve project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"

def ensure_directories():
    """Automatically create all standard project subdirectories."""
    subdirs = [
        DATA_DIR / "raw",
        DATA_DIR / "processed",
        PROJECT_ROOT / "notebooks",
        PROJECT_ROOT / "src",
        PROJECT_ROOT / "docs",
        PROJECT_ROOT / "reports",
        PROJECT_ROOT / "model",
    ]
    for directory in subdirs:
        directory.mkdir(parents=True, exist_ok=True)

# Auto-run when module is loaded
load_env()
ensure_directories()