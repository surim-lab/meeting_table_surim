from __future__ import annotations

import os

import requests


API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")


def api_get(path: str, params: dict | None = None) -> dict | list:
    response = requests.get(f"{API_BASE_URL}{path}", params=params, timeout=5)
    response.raise_for_status()
    return response.json()


def api_post(path: str, payload: dict) -> dict:
    response = requests.post(f"{API_BASE_URL}{path}", json=payload, timeout=5)
    response.raise_for_status()
    return response.json()


def api_delete(path: str, params: dict | None = None) -> dict:
    response = requests.delete(f"{API_BASE_URL}{path}", params=params, timeout=5)
    response.raise_for_status()
    return response.json()
