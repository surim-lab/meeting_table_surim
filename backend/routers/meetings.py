from __future__ import annotations

from fastapi import APIRouter

from ..schemas import MeetingIn, MeetingOut
from ..services import meetings as meeting_service
from .errors import raise_bad_request


router = APIRouter(tags=["meetings"])


@router.post("/meetings", response_model=MeetingOut)
def create_meeting(payload: MeetingIn) -> MeetingOut:
    try:
        return meeting_service.create_meeting(payload.meeting_name)
    except ValueError as exc:
        raise_bad_request(exc)


@router.get("/meetings/{meeting_name}", response_model=MeetingOut)
def get_meeting(meeting_name: str) -> MeetingOut:
    try:
        return meeting_service.get_meeting(meeting_name)
    except ValueError as exc:
        raise_bad_request(exc)
