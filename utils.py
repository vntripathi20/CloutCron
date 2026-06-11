import json
import random
from datetime import datetime
from pathlib import Path

import config


def setup():
    """Create required directories."""
    for folder in [config.DATA_DIR, config.VIDEO_DIR, config.MUSIC_DIR, config.OUTPUT_DIR, config.LOGS_DIR]:
        folder.mkdir(parents=True, exist_ok=True)


def load_quotes():
    """Load quotes from JSON file."""
    path = config.DATA_DIR / "quotes.json"
    if not path.exists():
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def pick_random_video():
    """Pick a random video from videos folder."""
    videos = list(config.VIDEO_DIR.glob("*.mp4")) + list(config.VIDEO_DIR.glob("*.mov"))
    if not videos:
        raise FileNotFoundError("No videos in videos/ folder")
    return random.choice(videos)


def pick_random_music():
    """Pick a random music track from music folder."""
    music = list(config.MUSIC_DIR.glob("*.mp3")) + list(config.MUSIC_DIR.glob("*.wav"))
    if not music:
        raise FileNotFoundError("No music in music/ folder")
    return random.choice(music)


def log_it(quote_text, output_file, status):
    """Log the post result."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    msg = f"{timestamp} | {quote_text[:40]} | {output_file} | {status}\n"
    with open(config.LOGS_DIR / "posts.log", "a") as f:
        f.write(msg)
