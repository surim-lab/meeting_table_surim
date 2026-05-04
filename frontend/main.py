from __future__ import annotations

import streamlit as st

from components.layout import render_footer, render_header
from state import seed_meeting_name_from_query
from styles import inject_styles
from views.meeting_page import render_meeting_page


def main() -> None:
    st.set_page_config(page_title="약속 시간 투표", layout="wide")
    seed_meeting_name_from_query()
    inject_styles()
    render_header()
    render_meeting_page()
    render_footer()


if __name__ == "__main__":
    main()
