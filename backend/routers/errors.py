from __future__ import annotations

from fastapi import HTTPException


def raise_bad_request(exc: ValueError) -> None:
    raise HTTPException(status_code=400, detail=str(exc)) from exc
