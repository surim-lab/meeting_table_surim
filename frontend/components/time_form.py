from __future__ import annotations

import streamlit as st

from time_utils import HOUR_OPTIONS, MAX_TIME_MINUTES, MINUTE_OPTIONS, format_hm, to_minutes


def auto_push_end_time() -> None:
    start_min = to_minutes(st.session_state.start_hour, st.session_state.start_minute)
    end_min = to_minutes(st.session_state.end_hour, st.session_state.end_minute)
    if end_min > start_min:
        return
    new_end = min(start_min + 60, MAX_TIME_MINUTES)
    new_end = (new_end // 10) * 10
    if new_end <= start_min:
        return
    st.session_state.end_hour = new_end // 60
    st.session_state.end_minute = new_end % 60


def render_time_range_fields() -> tuple[str, str, bool]:
    st.markdown("**시작 시간**")
    start_h_col, start_m_col = st.columns(2)
    with start_h_col:
        start_hour = st.selectbox(
            "시작 시",
            HOUR_OPTIONS,
            index=10,
            format_func=lambda x: f"{x:02d}시",
            key="start_hour",
            on_change=auto_push_end_time,
        )
    with start_m_col:
        start_minute = st.selectbox(
            "시작 분",
            MINUTE_OPTIONS,
            index=0,
            format_func=lambda x: f"{x:02d}분",
            key="start_minute",
            on_change=auto_push_end_time,
        )

    st.markdown("**종료 시간**")
    end_h_col, end_m_col = st.columns(2)
    with end_h_col:
        end_hour = st.selectbox(
            "종료 시",
            HOUR_OPTIONS,
            index=11,
            format_func=lambda x: f"{x:02d}시",
            key="end_hour",
        )
    with end_m_col:
        end_minute = st.selectbox(
            "종료 분",
            MINUTE_OPTIONS,
            index=0,
            format_func=lambda x: f"{x:02d}분",
            key="end_minute",
        )

    start_time = format_hm(start_hour, start_minute)
    end_time = format_hm(end_hour, end_minute)
    time_valid = to_minutes(end_hour, end_minute) > to_minutes(start_hour, start_minute)
    return start_time, end_time, time_valid
