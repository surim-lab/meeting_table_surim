from __future__ import annotations

from ..database import connect
from ..domain import meeting_key_from_name
from ..schemas import SummaryOut, TopSlotOut


def get_summary(meeting_name: str) -> SummaryOut:
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
            participants=[
                name.strip()
                for name in (row["participants"] or "").split(",")
                if name.strip()
            ],
        )
        for index, row in enumerate(rows)
    ]
    return SummaryOut(
        participant_count=participant_count,
        total_votes=total_votes,
        top_slots=top_slots,
    )
