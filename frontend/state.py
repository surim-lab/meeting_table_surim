from __future__ import annotations

import streamlit as st


MEETING_NAME_KEY = "meeting_name"
MEETING_NAME_INPUT_KEY = "meeting_name_input"


def get_query_value(key: str) -> str:
    value = st.query_params.get(key, "")
    if value is None:
        return ""
    if isinstance(value, list):
        value = value[0] if value else ""
    return str(value).strip()


def seed_meeting_name_from_query() -> None:
    if MEETING_NAME_INPUT_KEY not in st.session_state:
        st.session_state[MEETING_NAME_INPUT_KEY] = get_query_value(MEETING_NAME_KEY)


def sync_meeting_name_query(meeting_name: str) -> None:
    current = get_query_value(MEETING_NAME_KEY)
    if meeting_name:
        if current != meeting_name:
            st.query_params[MEETING_NAME_KEY] = meeting_name
    elif current:
        del st.query_params[MEETING_NAME_KEY]
