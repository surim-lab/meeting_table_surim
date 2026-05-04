from __future__ import annotations

import calendar
import os
from datetime import date

import requests
import streamlit as st

from styles import inject_styles


API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
SLOT_OPTIONS = [f"{hour:02d}:00" for hour in range(8, 23)]


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


def render_header() -> None:
    st.markdown(
        """
        <header class="app-header">
            <div class="app-kicker">MEETING TIME VOTE</div>
            <h1 class="app-title">모임 약속 시간 정하기</h1>
            <p class="app-subtitle">
                참가자들이 가능한 월, 일, 시간 슬롯을 선택하면 가장 많은 사람이 가능한 후보 TOP 3를 계산합니다.
            </p>
        </header>
        """,
        unsafe_allow_html=True,
    )


def render_footer() -> None:
    st.markdown(
        """
        <footer class="app-footer">
            <div class="app-footer-author">황수림</div>
            <a class="app-footer-email" href="mailto:srhwang@surromind.ai">srhwang@surromind.ai</a>
        </footer>
        """,
        unsafe_allow_html=True,
    )


def get_day_options(year: int, month: int) -> list[int]:
    _, last_day = calendar.monthrange(year, month)
    return list(range(1, last_day + 1))


def make_slots(year: int, month: int, days: list[int], times: list[str]) -> list[dict[str, str]]:
    slots = []
    for day in sorted(days):
        slot_date = date(year, month, day).isoformat()
        for start_time in sorted(times):
            hour = int(start_time.split(":")[0])
            end_time = f"{hour + 1:02d}:00"
            slots.append(
                {
                    "date": slot_date,
                    "start_time": start_time,
                    "end_time": end_time,
                }
            )
    return slots


def format_slot(slot: dict) -> str:
    month = int(slot["date"].split("-")[1])
    day = int(slot["date"].split("-")[2])
    return f"{month}월 {day}일 {slot['start_time']} - {slot['end_time']}"


def render_summary(summary: dict) -> None:
    st.markdown(
        f"""
        <section class="hero-card">
            <div class="metric-row">
                <div class="metric-chip">
                    <div class="metric-label">참가자</div>
                    <div class="metric-value">{summary['participant_count']}명</div>
                </div>
                <div class="metric-chip">
                    <div class="metric-label">선택된 슬롯</div>
                    <div class="metric-value">{summary['total_votes']}개</div>
                </div>
                <div class="metric-chip">
                    <div class="metric-label">후보</div>
                    <div class="metric-value">{len(summary['top_slots'])}개</div>
                </div>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="section-block">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">후보 시간 TOP 3</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    if not summary["top_slots"]:
        st.info("아직 등록된 가능 시간이 없습니다.")
    for slot in summary["top_slots"]:
        names = ", ".join(slot["participants"])
        st.markdown(
            f"""
            <div class="rank-card">
                <div class="rank-line">
                    <div class="rank-title">#{slot['rank']} · {format_slot(slot)}</div>
                    <div class="rank-count">{slot['vote_count']}명 가능</div>
                </div>
                <div class="rank-names">{names}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def empty_summary() -> dict:
    return {"participant_count": 0, "total_votes": 0, "top_slots": []}


def main() -> None:
    st.set_page_config(page_title="약속 시간 투표", layout="wide")
    inject_styles()
    render_header()

    left, right = st.columns([1, 1], gap="large")
    summary = empty_summary()

    with left:
        st.markdown('<div class="section-block">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">가능 시간 등록</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="section-description">모임 이름을 먼저 입력한 뒤 이름과 가능한 날짜, 시간 슬롯을 고르세요.</div>',
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

        meeting_name = st.text_input("모임 이름", placeholder="예: 토요일 저녁 약속")
        meeting_name = meeting_name.strip()
        if not meeting_name:
            st.info("같은 모임 이름을 입력한 사람들의 일정만 함께 표시됩니다.")
        else:
            try:
                meeting_params = {"meeting_name": meeting_name}
                api_post("/meetings", {"meeting_name": meeting_name})
                summary = api_get("/summary", params=meeting_params)
                participants = api_get("/participants", params=meeting_params)
            except requests.RequestException:
                st.error("FastAPI 백엔드에 연결할 수 없습니다. `docker compose up --build` 또는 `uvicorn backend.main:app --reload`를 먼저 실행해주세요.")
                st.stop()

        current_year = date.today().year
        if meeting_name:
            name = st.text_input("이름", placeholder="예: 홍길동")
            year = st.number_input("연도", min_value=current_year, max_value=current_year + 2, value=current_year, step=1)
            month = st.selectbox("월", list(range(1, 13)), index=date.today().month - 1, format_func=lambda x: f"{x}월")
            days = st.multiselect("일", get_day_options(year, month), format_func=lambda x: f"{x}일")
            times = st.multiselect("시간 슬롯", SLOT_OPTIONS, default=["10:00", "14:00"], format_func=lambda x: f"{x} - {int(x[:2]) + 1:02d}:00")

            slots = make_slots(year, month, days, times)
            st.caption(f"선택된 가능 시간: {len(slots)}개")

            submitted = st.button("등록하기", type="primary", use_container_width=True)
            if submitted:
                if not name.strip():
                    st.warning("이름을 입력해주세요.")
                elif not slots:
                    st.warning("하나 이상의 날짜와 시간 슬롯을 선택해주세요.")
                else:
                    try:
                        api_post("/participants", {"meeting_name": meeting_name, "name": name, "slots": slots})
                        st.success("가능 시간이 등록되었습니다.")
                        st.rerun()
                    except requests.RequestException as exc:
                        st.error(f"등록에 실패했습니다: {exc}")

            st.markdown('<div class="section-block section-block--spaced">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">참가자 현황</div>', unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            if participants:
                for participant in participants:
                    st.write(f"- {participant['name']} · {participant['slot_count']}개 슬롯")
            else:
                st.caption("아직 참가자가 없습니다.")

            if st.button("이 모임 초기화", use_container_width=True):
                try:
                    api_delete("/reset", params=meeting_params)
                    st.rerun()
                except requests.RequestException as exc:
                    st.error(f"초기화에 실패했습니다: {exc}")

    with right:
        render_summary(summary)

    render_footer()


if __name__ == "__main__":
    main()
