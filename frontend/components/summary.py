from __future__ import annotations

import streamlit as st

from time_utils import format_slot


def empty_summary() -> dict:
    return {"participant_count": 0, "total_votes": 0, "top_slots": []}


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
