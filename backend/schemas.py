from __future__ import annotations

from pydantic import BaseModel, Field, field_validator

from .domain import normalize_meeting_name


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
        if not (0 <= hour <= 23 and 0 <= minute <= 59 and minute % 10 == 0):
            raise ValueError("time must be on a 10-minute boundary")
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
