from __future__ import annotations

from datetime import date

import requests
import streamlit as st

from api import api_delete, api_get, api_post
from components.layout import render_section_header
from components.summary import empty_summary, render_summary
from components.time_form import render_time_range_fields
from state import MEETING_NAME_INPUT_KEY, sync_meeting_name_query
from time_utils import get_day_options, make_slots


def load_meeting_data(meeting_name: str) -> tuple[dict, list[dict]]:
    meeting_params = {"meeting_name": meeting_name}
    api_post("/meetings", {"meeting_name": meeting_name})
    summary = api_get("/summary", params=meeting_params)
    participants = api_get("/participants", params=meeting_params)
    return summary, participants


def render_meeting_page() -> None:
    left, right = st.columns([1, 1], gap="large")
    summary = empty_summary()

    with left:
        render_section_header(
            "가능 시간 등록",
            "모임 이름을 먼저 입력한 뒤 이름과 가능한 날짜, 시간 슬롯을 고르세요.",
        )

        meeting_name = st.text_input(
            "모임 이름",
            placeholder="예: 토요일 저녁 약속",
            key=MEETING_NAME_INPUT_KEY,
        ).strip()
        sync_meeting_name_query(meeting_name)

        if not meeting_name:
            st.info("같은 모임 이름을 입력한 사람들의 일정만 함께 표시됩니다.")
        else:
            try:
                summary, participants = load_meeting_data(meeting_name)
            except requests.RequestException:
                st.error("FastAPI 백엔드에 연결할 수 없습니다. `docker compose up --build` 또는 `uvicorn backend.main:app --reload`를 먼저 실행해주세요.")
                st.stop()

        if meeting_name:
            render_registration_form(meeting_name, participants)

    with right:
        render_summary(summary)


def render_registration_form(meeting_name: str, participants: list[dict]) -> None:
    current_year = date.today().year
    name = st.text_input("이름", placeholder="예: 홍길동")
    year = st.number_input("연도", min_value=current_year, max_value=current_year + 2, value=current_year, step=1)
    month = st.selectbox("월", list(range(1, 13)), index=date.today().month - 1, format_func=lambda x: f"{x}월")
    days = st.multiselect("일", get_day_options(year, month), format_func=lambda x: f"{x}일")

    start_time, end_time, time_valid = render_time_range_fields()
    if not time_valid:
        st.error("종료 시간이 시작 시간보다 이릅니다.")
    else:
        st.caption(f"선택된 시간: {start_time} - {end_time} · {len(days)}일")

    submitted = st.button("등록하기", type="primary", use_container_width=True)
    if submitted:
        submit_availability(meeting_name, name, year, month, days, start_time, end_time, time_valid)

    render_participants(participants)
    render_reset_button(meeting_name)


def submit_availability(
    meeting_name: str,
    name: str,
    year: int,
    month: int,
    days: list[int],
    start_time: str,
    end_time: str,
    time_valid: bool,
) -> None:
    if not name.strip():
        st.warning("이름을 입력해주세요.")
        return
    if not days:
        st.warning("하나 이상의 날짜를 선택해주세요.")
        return
    if not time_valid:
        st.error("종료 시간이 시작 시간보다 이릅니다.")
        return

    slots = make_slots(year, month, days, start_time, end_time)
    try:
        api_post("/participants", {"meeting_name": meeting_name, "name": name, "slots": slots})
        st.success("가능 시간이 등록되었습니다.")
        st.rerun()
    except requests.RequestException as exc:
        st.error(f"등록에 실패했습니다: {exc}")


def render_participants(participants: list[dict]) -> None:
    render_section_header("참가자 현황", spaced=True)
    if participants:
        for participant in participants:
            st.write(f"- {participant['name']} · {participant['slot_count']}개 슬롯")
    else:
        st.caption("아직 참가자가 없습니다.")


def render_reset_button(meeting_name: str) -> None:
    if st.button("이 모임 초기화", use_container_width=True):
        try:
            api_delete("/reset", params={"meeting_name": meeting_name})
            st.rerun()
        except requests.RequestException as exc:
            st.error(f"초기화에 실패했습니다: {exc}")
