from __future__ import annotations

from hashlib import sha256

from .config import LEGACY_MEETING_NAME


def normalize_meeting_name(value: str) -> str:
    meeting_name = value.strip()
    if not meeting_name:
        raise ValueError("meeting_name is required")
    if len(meeting_name) > 100:
        raise ValueError("meeting_name must be 100 characters or fewer")
    return meeting_name


def meeting_key_from_name(meeting_name: str) -> str:
    normalized = normalize_meeting_name(meeting_name)
    return sha256(normalized.encode("utf-8")).hexdigest()


LEGACY_MEETING_KEY = sha256(LEGACY_MEETING_NAME.encode("utf-8")).hexdigest()
