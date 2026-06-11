import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
VIDEO_DIR = BASE_DIR / "videos"
MUSIC_DIR = BASE_DIR / "music"
OUTPUT_DIR = BASE_DIR / "output"
LOGS_DIR = BASE_DIR / "logs"

# Get credentials from environment
IG_USER = os.getenv("IG_USER", "")
IG_PASS = os.getenv("IG_PASS", "")
