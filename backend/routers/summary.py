from __future__ import annotations

from fastapi import APIRouter, Query

from ..schemas import SummaryOut
from ..services import summary as summary_service
from .errors import raise_bad_request


router = APIRouter(tags=["summary"])


@router.get("/summary", response_model=SummaryOut)
def get_summary(
    meeting_name: str = Query(..., min_length=1, max_length=100),
) -> SummaryOut:
    try:
        return summary_service.get_summary(meeting_name)
    except ValueError as exc:
        raise_bad_request(exc)
