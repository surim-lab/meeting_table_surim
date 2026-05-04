from __future__ import annotations

import sqlite3

from ..database import connect
from ..domain import meeting_key_from_name, normalize_meeting_name
from ..schemas import MeetingOut


def ensure_meeting(conn: sqlite3.Connection, meeting_name: str) -> str:
    normalized = normalize_meeting_name(meeting_name)
    meeting_key = meeting_key_from_name(normalized)
    conn.execute(
        """
        INSERT INTO meetings (meeting_key, meeting_name)
        VALUES (?, ?)
        ON CONFLICT(meeting_key) DO UPDATE SET meeting_name = excluded.meeting_name
        """,
        (meeting_key, normalized),
    )
    return meeting_key


def get_meeting_counts(conn: sqlite3.Connection, meeting_key: str) -> tuple[int, int]:
    participant_count = conn.execute(
        "SELECT COUNT(*) FROM participants WHERE room_key = ?",
        (meeting_key,),
    ).fetchone()[0]
    total_votes = conn.execute(
        """
        SELECT COUNT(*)
        FROM availability a
        JOIN participants p ON p.id = a.participant_id
        WHERE p.room_key = ?
        """,
        (meeting_key,),
    ).fetchone()[0]
    return participant_count, total_votes


def create_meeting(meeting_name: str) -> MeetingOut:
    normalized = normalize_meeting_name(meeting_name)
    with connect() as conn:
        meeting_key = ensure_meeting(conn, normalized)
        participant_count, total_votes = get_meeting_counts(conn, meeting_key)
    return MeetingOut(
        meeting_name=normalized,
        participant_count=participant_count,
        total_votes=total_votes,
    )


def get_meeting(meeting_name: str) -> MeetingOut:
    normalized = normalize_meeting_name(meeting_name)
    meeting_key = meeting_key_from_name(normalized)
    with connect() as conn:
        row = conn.execute(
            "SELECT meeting_name FROM meetings WHERE meeting_key = ?",
            (meeting_key,),
        ).fetchone()
        participant_count, total_votes = get_meeting_counts(conn, meeting_key)
    return MeetingOut(
        meeting_name=row["meeting_name"] if row else normalized,
        participant_count=participant_count,
        total_votes=total_votes,
    )
