from __future__ import annotations

import streamlit as st


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


def render_section_header(title: str, description: str | None = None, *, spaced: bool = False) -> None:
    class_name = "section-block section-block--spaced" if spaced else "section-block"
    st.markdown(f'<div class="{class_name}">', unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)
    if description:
        st.markdown(
            f'<div class="section-description">{description}</div>',
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)
