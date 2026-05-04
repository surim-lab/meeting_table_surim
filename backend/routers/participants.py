from __future__ import annotations

from fastapi import APIRouter, Query

from ..schemas import ParticipantIn, ParticipantOut
from ..services import participants as participant_service
from .errors import raise_bad_request


router = APIRouter(tags=["participants"])


@router.post("/participants", response_model=ParticipantOut)
def create_participant(payload: ParticipantIn) -> ParticipantOut:
    try:
        return participant_service.create_participant(payload)
    except ValueError as exc:
        raise_bad_request(exc)


@router.get("/participants", response_model=list[ParticipantOut])
def list_participants(
    meeting_name: str = Query(..., min_length=1, max_length=100),
) -> list[ParticipantOut]:
    try:
        return participant_service.list_participants(meeting_name)
    except ValueError as exc:
        raise_bad_request(exc)


@router.delete("/reset")
def reset(meeting_name: str = Query(..., min_length=1, max_length=100)) -> dict[str, str]:
    try:
        return participant_service.reset_meeting(meeting_name)
    except ValueError as exc:
        raise_bad_request(exc)
