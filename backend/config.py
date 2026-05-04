from __future__ import annotations

import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = Path(os.getenv("TIMETABLE_DB", BASE_DIR / "time_table.db"))
LEGACY_MEETING_NAME = "default"
