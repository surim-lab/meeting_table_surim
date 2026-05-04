from __future__ import annotations

from ..database import connect
from ..domain import meeting_key_from_name
from ..schemas import ParticipantIn, ParticipantOut
from .meetings import ensure_meeting


def create_participant(payload: ParticipantIn) -> ParticipantOut:
    unique_slots = {
        (slot.date, slot.start_time, slot.end_time)
        for slot in payload.slots
        if slot.start_time < slot.end_time
    }
    if not unique_slots:
        raise ValueError("At least one valid slot is required")

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
            [(participant_id, slot_date, start, end) for slot_date, start, end in sorted(unique_slots)],
        )

    return ParticipantOut(id=participant_id, name=payload.name, slot_count=len(unique_slots))


def list_participants(meeting_name: str) -> list[ParticipantOut]:
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


def reset_meeting(meeting_name: str) -> dict[str, str]:
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
