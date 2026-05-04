from __future__ import annotations

import os
import sqlite3
from hashlib import sha256
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator


BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = Path(os.getenv("TIMETABLE_DB", BASE_DIR / "time_table.db"))
LEGACY_MEETING_NAME = "default"


def normalize_meeting_name(value: str) -> str:
    meeting_name = value.strip()
    if not meeting_name:
        raise ValueError("meeting_name is required")
    if len(meeting_name) > 100:
        raise ValueError("meeting_name must be 100 characters or fewer")
    return meeting_name


def meeting_key_from_name(meeting_name: str) -> str:
    try:
        normalized = normalize_meeting_name(meeting_name)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return sha256(normalized.encode("utf-8")).hexdigest()


LEGACY_MEETING_KEY = sha256(LEGACY_MEETING_NAME.encode("utf-8")).hexdigest()


class SlotIn(BaseModel):
    date: str = Field(..., examples=["2026-05-03"])
    start_time: str = Field(..., examples=["14:00"])
    end_time: str = Field(..., examples=["15:00"])

    @field_validator("date")
    @classmethod
    def validate_date(cls, value: str) -> str:
        parts = value.split("-")
        if len(parts) != 3 or any(not part.isdigit() for part in parts):
            raise ValueError("date must be YYYY-MM-DD")
        year, month, day = map(int, parts)
        if not (1 <= month <= 12 and 1 <= day <= 31 and year >= 2000):
            raise ValueError("date is out of range")
        return value

    @field_validator("start_time", "end_time")
    @classmethod
    def validate_time(cls, value: str) -> str:
        parts = value.split(":")
        if len(parts) != 2 or any(not part.isdigit() for part in parts):
            raise ValueError("time must be HH:MM")
        hour, minute = map(int, parts)
        if not (0 <= hour <= 23 and minute in {0, 30}):
            raise ValueError("time must be on a 30-minute boundary")
        return f"{hour:02d}:{minute:02d}"


class ParticipantIn(BaseModel):
    meeting_name: str = Field(..., min_length=1, max_length=100)
    name: str = Field(..., min_length=1, max_length=50)
    slots: list[SlotIn] = Field(..., min_length=1)

    @field_validator("meeting_name")
    @classmethod
    def trim_meeting_name(cls, value: str) -> str:
        return normalize_meeting_name(value)

    @field_validator("name")
    @classmethod
    def trim_name(cls, value: str) -> str:
        name = value.strip()
        if not name:
            raise ValueError("name is required")
        return name


class MeetingIn(BaseModel):
    meeting_name: str = Field(..., min_length=1, max_length=100)

    @field_validator("meeting_name")
    @classmethod
    def trim_meeting_name(cls, value: str) -> str:
        return normalize_meeting_name(value)


class MeetingOut(BaseModel):
    meeting_name: str
    participant_count: int
    total_votes: int


class ParticipantOut(BaseModel):
    id: int
    name: str
    slot_count: int


class TopSlotOut(BaseModel):
    rank: int
    date: str
    start_time: str
    end_time: str
    vote_count: int
    participants: list[str]


class SummaryOut(BaseModel):
    participant_count: int
    total_votes: int
    top_slots: list[TopSlotOut]


@contextmanager
def connect() -> Iterator[sqlite3.Connection]:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        conn.execute("PRAGMA foreign_keys = ON")
        ensure_schema(conn)
        yield conn
        conn.commit()
    finally:
        conn.close()


def ensure_schema(conn: sqlite3.Connection) -> None:
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS meetings (
            meeting_key TEXT PRIMARY KEY,
            meeting_name TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS participants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            room_key TEXT NOT NULL,
            name TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS availability (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            participant_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            start_time TEXT NOT NULL,
            end_time TEXT NOT NULL,
            FOREIGN KEY (participant_id) REFERENCES participants(id) ON DELETE CASCADE,
            UNIQUE (participant_id, date, start_time, end_time)
            )
        """
    )
    columns = {row["name"] for row in conn.execute("PRAGMA table_info(participants)")}
    if "room_key" not in columns:
        conn.execute(
            f"ALTER TABLE participants ADD COLUMN room_key TEXT NOT NULL DEFAULT '{LEGACY_MEETING_KEY}'"
        )
    conn.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_participants_room_key_created
        ON participants (room_key, created_at, id)
        """
    )


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


def init_db() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        ensure_schema(conn)


app = FastAPI(title="Time Table API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup() -> None:
    init_db()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/meetings", response_model=MeetingOut)
def create_meeting(payload: MeetingIn) -> MeetingOut:
    with connect() as conn:
        meeting_key = ensure_meeting(conn, payload.meeting_name)
        participant_count, total_votes = get_meeting_counts(conn, meeting_key)
    return MeetingOut(
        meeting_name=payload.meeting_name,
        participant_count=participant_count,
        total_votes=total_votes,
    )


@app.get("/meetings/{meeting_name}", response_model=MeetingOut)
def get_meeting(meeting_name: str) -> MeetingOut:
    try:
        normalized = normalize_meeting_name(meeting_name)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
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


@app.post("/participants", response_model=ParticipantOut)
def create_participant(payload: ParticipantIn) -> ParticipantOut:
    unique_slots = {
        (slot.date, slot.start_time, slot.end_time)
        for slot in payload.slots
        if slot.start_time < slot.end_time
    }
    if not unique_slots:
        raise HTTPException(status_code=400, detail="At least one valid slot is required")

    with connect() as conn:
        room_key = ensure_meeting(conn, payload.meeting_name)
        cursor = conn.execute(
            "INSERT INTO participants (room_key, name) VALUES (?, ?)",
            (room_key, payload.name),
        )
        participant_id = int(cursor.lastrowid)
        conn.executemany(
            """
            INSERT OR IGNORE INTO availability
                (participant_id, date, start_time, end_time)
            VALUES (?, ?, ?, ?)
            """,
            [(participant_id, date, start, end) for date, start, end in sorted(unique_slots)],
        )

    return ParticipantOut(id=participant_id, name=payload.name, slot_count=len(unique_slots))


@app.get("/participants", response_model=list[ParticipantOut])
def list_participants(meeting_name: str = Query(..., min_length=1, max_length=100)) -> list[ParticipantOut]:
    room_key = meeting_key_from_name(meeting_name)
    with connect() as conn:
        rows = conn.execute(
            """
            SELECT p.id, p.name, COUNT(a.id) AS slot_count
            FROM participants p
            LEFT JOIN availability a ON a.participant_id = p.id
            WHERE p.room_key = ?
            GROUP BY p.id, p.name
            ORDER BY p.created_at DESC, p.id DESC
            """,
            (room_key,),
        ).fetchall()
    return [ParticipantOut(**dict(row)) for row in rows]


@app.get("/summary", response_model=SummaryOut)
def get_summary(meeting_name: str = Query(..., min_length=1, max_length=100)) -> SummaryOut:
    room_key = meeting_key_from_name(meeting_name)
    with connect() as conn:
        participant_count = conn.execute(
            "SELECT COUNT(*) FROM participants WHERE room_key = ?",
            (room_key,),
        ).fetchone()[0]
        total_votes = conn.execute(
            """
            SELECT COUNT(*)
            FROM availability a
            JOIN participants p ON p.id = a.participant_id
            WHERE p.room_key = ?
            """,
            (room_key,),
        ).fetchone()[0]
        rows = conn.execute(
            """
            SELECT
                a.date,
                a.start_time,
                a.end_time,
                COUNT(*) AS vote_count,
                GROUP_CONCAT(p.name, ', ') AS participants
            FROM availability a
            JOIN participants p ON p.id = a.participant_id
            WHERE p.room_key = ?
            GROUP BY a.date, a.start_time, a.end_time
            ORDER BY vote_count DESC, a.date ASC, a.start_time ASC
            LIMIT 3
            """,
            (room_key,),
        ).fetchall()

    top_slots = [
        TopSlotOut(
            rank=index + 1,
            date=row["date"],
            start_time=row["start_time"],
            end_time=row["end_time"],
            vote_count=row["vote_count"],
            participants=[name.strip() for name in (row["participants"] or "").split(",") if name.strip()],
        )
        for index, row in enumerate(rows)
    ]
    return SummaryOut(
        participant_count=participant_count,
        total_votes=total_votes,
        top_slots=top_slots,
    )


@app.delete("/reset")
def reset(meeting_name: str = Query(..., min_length=1, max_length=100)) -> dict[str, str]:
    room_key = meeting_key_from_name(meeting_name)
    with connect() as conn:
        conn.execute(
            """
            DELETE FROM availability
            WHERE participant_id IN (
                SELECT id FROM participants WHERE room_key = ?
            )
            """,
            (room_key,),
        )
        conn.execute("DELETE FROM participants WHERE room_key = ?", (room_key,))
    return {"status": "reset"}
