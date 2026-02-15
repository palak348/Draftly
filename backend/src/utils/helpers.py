"""
Utility helpers: logging, caching, file saving, word counting.
"""

import os
import json
import logging
from datetime import datetime, timedelta
from pathlib import Path

from config import SystemConfig


# ---------------- LOGGING ----------------

def setup_logging():
    """Configure application logging."""

    root_logger = logging.getLogger()
    root_logger.setLevel(SystemConfig.LOG_LEVEL)

    # Prevent duplicate handlers
    if root_logger.handlers:
        root_logger.handlers.clear()

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    # File handler
    file_handler = logging.FileHandler(SystemConfig.LOG_FILE)
    file_handler.setFormatter(formatter)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)


# ---------------- CACHE ----------------

class CacheManager:
    """Simple JSON file-based cache."""

    def __init__(self):
        self.cache_dir = Path(SystemConfig.CACHE_DIR)
        self.cache_dir.mkdir(exist_ok=True)

    def _get_path(self, key: str) -> Path:
        return self.cache_dir / f"{key}.json"

    def get(self, key: str):
        path = self._get_path(key)
        if not path.exists():
            return None

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        timestamp = datetime.fromisoformat(data["timestamp"])
        if datetime.utcnow() - timestamp > timedelta(hours=SystemConfig.CACHE_TTL_HOURS):
            return None

        return data["value"]

    def set(self, key: str, value):
        path = self._get_path(key)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "timestamp": datetime.utcnow().isoformat(),
                    "value": value
                },
                f,
                ensure_ascii=False,
                indent=2
            )


# ---------------- FILE SAVING ----------------

def save_blog(content: str, title: str, metadata: dict) -> str:
    """Save blog markdown file to output directory."""
    import re

    output_dir = Path(SystemConfig.OUTPUT_DIR)
    output_dir.mkdir(exist_ok=True)

    # Remove characters invalid in Windows filenames
    safe_title = re.sub(r'[<>:"/\\|?*]', '', title.lower()).replace(" ", "_")
    safe_title = safe_title.strip("_") or "untitled"
    filename = f"{safe_title}.md"
    filepath = output_dir / filename

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    # Also save metadata
    meta_path = output_dir / f"{safe_title}_metadata.json"
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)

    return str(filepath)


# ---------------- WORD COUNT ----------------

def count_words(text: str) -> int:
    """Return word count."""
    return len(text.split())


# ---------------- PROGRESS TRACKER ----------------

class ProgressTracker:
    """Simple console progress tracker."""

    def __init__(self, total_steps: int):
        self.total_steps = total_steps
        self.current_step = 0

    def update(self, stage: str, message: str):
        """Update progress on console."""
        self.current_step += 1
        progress = f"[{self.current_step}/{self.total_steps}]"
        print(f"⏳ {progress} {stage}: {message}")
        logging.info("Progress Update: %s | %s", stage, message)

    def complete(self):
        """Mark as completed."""
        print("✅ Task processing complete.\n")
        logging.info("Progress: Complete")
