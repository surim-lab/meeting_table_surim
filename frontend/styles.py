from __future__ import annotations

import streamlit as st


def inject_styles() -> None:
    st.markdown(
        """
        <style>
        :root {
            --page-bg: #f3e9ff;
            --page-bg-soft: #fff1f4;
            --page-bg-mint: #e6f7ef;
            --page-bg-sky: #e3f1ff;
            --card-bg: rgba(255, 255, 255, 0.86);
            --card-border: rgba(176, 158, 214, 0.28);
            --text-main: #3b3350;
            --text-muted: #7a6f8c;
            --accent: #b39ddb;
            --accent-soft: #ece4f7;
            --pastel-pink: #fbd4e3;
            --pastel-mint: #c6ecd6;
            --pastel-sky: #c9e3fa;
            --pastel-lemon: #fff1b8;
        }

        .stApp {
            background:
                radial-gradient(circle at 12% 10%, rgba(214, 199, 240, 0.55), transparent 38%),
                radial-gradient(circle at 88% 18%, rgba(251, 212, 227, 0.50), transparent 42%),
                radial-gradient(circle at 78% 92%, rgba(198, 236, 214, 0.50), transparent 42%),
                radial-gradient(circle at 8% 88%, rgba(201, 227, 250, 0.50), transparent 42%),
                linear-gradient(180deg, var(--page-bg-soft) 0%, var(--page-bg) 58%, var(--page-bg-mint) 100%);
            color: var(--text-main);
        }

        .block-container {
            max-width: 1180px;
            padding-top: 2.1rem;
            padding-bottom: 2.5rem;
        }

        .section-block {
            margin: 1.1rem 0 0.4rem;
            padding-left: 0.7rem;
            border-left: 4px solid var(--accent);
        }

        .section-block--spaced {
            margin-top: 1.6rem;
        }

        .app-header {
            display: flex;
            flex-direction: column;
            gap: 0.35rem;
            padding: 0.55rem 0 1.2rem;
            margin-bottom: 0.7rem;
            border-bottom: 1px solid rgba(179, 157, 219, 0.22);
        }

        .app-kicker {
            color: #6a4f8a;
            font-size: 0.78rem;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            font-weight: 700;
        }

        .app-title {
            color: var(--text-main);
            font-size: 1.85rem;
            font-weight: 800;
            line-height: 1.25;
            margin: 0;
        }

        .app-subtitle {
            color: var(--text-muted);
            font-size: 0.98rem;
            line-height: 1.6;
            margin: 0;
        }

        .hero-card {
            border-radius: 14px;
            padding: 1.3rem 1.45rem;
            margin: 0.7rem 0 1rem;
            background: linear-gradient(135deg, #d6c7f0 0%, #fbd4e3 52%, #ffd9c2 100%);
            box-shadow: 0 22px 55px rgba(179, 157, 219, 0.13);
        }

        .metric-row {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 0.75rem;
        }

        .metric-chip {
            border-radius: 10px;
            padding: 0.85rem 0.9rem;
            background: rgba(255, 255, 255, 0.62);
            border: 1px solid rgba(255, 255, 255, 0.68);
        }

        .metric-label {
            color: var(--text-muted);
            font-size: 0.78rem;
            margin-bottom: 0.2rem;
        }

        .metric-value {
            color: var(--text-main);
            font-size: 1.35rem;
            font-weight: 800;
        }

        .section-title {
            font-size: 1.05rem;
            font-weight: 800;
            color: var(--text-main);
            margin-bottom: 0.2rem;
        }

        .section-description {
            color: var(--text-muted);
            font-size: 0.9rem;
            line-height: 1.55;
            margin-bottom: 0.9rem;
        }

        .rank-card {
            border-radius: 12px;
            padding: 0.95rem 1rem;
            background: linear-gradient(135deg, rgba(236, 228, 247, 0.85), rgba(201, 227, 250, 0.78));
            border: 1px solid rgba(179, 157, 219, 0.22);
            margin-bottom: 0.72rem;
        }

        .rank-line {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 0.8rem;
        }

        .rank-title {
            font-weight: 800;
            color: var(--text-main);
            font-size: 1rem;
        }

        .rank-count {
            border-radius: 999px;
            background: rgba(255, 255, 255, 0.7);
            color: #5a4a78;
            padding: 0.35rem 0.65rem;
            font-weight: 800;
            white-space: nowrap;
        }

        .rank-names {
            color: var(--text-muted);
            font-size: 0.86rem;
            margin-top: 0.45rem;
            line-height: 1.45;
            word-break: break-word;
        }

        .app-footer {
            margin-top: 2.4rem;
            padding: 1rem 0 0.4rem;
            border-top: 1px solid rgba(179, 157, 219, 0.22);
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0.6rem;
            color: var(--text-muted);
            font-size: 0.85rem;
        }

        .app-footer-author {
            font-weight: 700;
            color: var(--text-main);
        }

        .app-footer-email {
            color: #6a4f8a;
            text-decoration: none;
            border-bottom: 1px dashed rgba(106, 79, 138, 0.4);
        }

        .app-footer-email:hover {
            color: #3b3350;
        }

        div[data-testid="stButton"] button {
            background: linear-gradient(135deg, #b39ddb 0%, #f8bbd0 100%);
            color: #3b3350;
            border: none;
            border-radius: 10px;
            font-weight: 800;
            min-height: 44px;
            box-shadow: 0 8px 18px rgba(179, 157, 219, 0.28);
        }

        div[data-testid="stButton"] button:hover {
            background: linear-gradient(135deg, #c5b3e5 0%, #fcc6d7 100%);
            color: #3b3350;
            border: none;
        }

        div[data-testid="stTextInput"] input,
        div[data-testid="stNumberInput"] input {
            border-radius: 10px;
            border: 1px solid rgba(179, 157, 219, 0.35);
            background: rgba(255, 255, 255, 0.93);
            font-size: 16px;
        }

        .stMultiSelect [data-baseweb="select"],
        .stSelectbox [data-baseweb="select"] {
            border-radius: 10px;
        }

        .stMultiSelect [data-baseweb="select"] *,
        .stSelectbox [data-baseweb="select"] * {
            font-size: 16px;
        }

        @media (prefers-color-scheme: dark) {
            .stApp,
            .stApp p,
            .stApp span,
            .stApp label,
            .stApp div,
            .stApp h1,
            .stApp h2,
            .stApp h3,
            .stApp h4,
            .stApp h5,
            .stApp h6 {
                color: var(--text-main) !important;
            }

            .stApp .app-subtitle,
            .stApp .section-description,
            .stApp .metric-label,
            .stApp .rank-names,
            .stApp .app-footer,
            .stApp small,
            .stApp [data-testid="stCaptionContainer"],
            .stApp [data-testid="stCaptionContainer"] * {
                color: var(--text-muted) !important;
            }

            .stApp .app-kicker {
                color: #6a4f8a !important;
            }

            .stApp .rank-count {
                color: #5a4a78 !important;
            }

            .stApp .app-footer-email {
                color: #6a4f8a !important;
            }

            div[data-testid="stTextInput"] input,
            div[data-testid="stNumberInput"] input,
            div[data-testid="stTextArea"] textarea {
                color: var(--text-main) !important;
                background: rgba(255, 255, 255, 0.93) !important;
            }

            .stMultiSelect [data-baseweb="select"] *,
            .stSelectbox [data-baseweb="select"] * {
                color: var(--text-main) !important;
            }

            div[data-testid="stButton"] button {
                color: #3b3350 !important;
            }
        }

        @media (max-width: 760px) {
            .block-container {
                padding-top: 1rem;
                padding-bottom: 1.5rem;
                padding-left: 0.85rem !important;
                padding-right: 0.85rem !important;
            }

            .app-header {
                padding: 0.3rem 0 0.85rem;
                margin-bottom: 0.5rem;
            }

            .app-kicker {
                font-size: 0.7rem;
            }

            .app-title {
                font-size: 1.5rem;
                line-height: 1.3;
            }

            .app-subtitle {
                font-size: 0.9rem;
                line-height: 1.5;
            }

            .hero-card {
                padding: 1rem 1.05rem;
                margin: 0.5rem 0 0.85rem;
                border-radius: 12px;
            }

            .metric-row {
                grid-template-columns: 1fr;
                gap: 0.5rem;
            }

            .metric-chip {
                padding: 0.65rem 0.85rem;
                display: flex;
                align-items: baseline;
                justify-content: space-between;
                gap: 0.6rem;
            }

            .metric-label {
                margin-bottom: 0;
                font-size: 0.85rem;
            }

            .metric-value {
                font-size: 1.15rem;
            }

            .section-block {
                margin: 0.9rem 0 0.3rem;
                padding-left: 0.55rem;
                border-left-width: 3px;
            }

            .section-title {
                font-size: 1rem;
            }

            .section-description {
                font-size: 0.86rem;
                margin-bottom: 0.7rem;
            }

            .rank-card {
                padding: 0.8rem 0.9rem;
                border-radius: 10px;
            }

            .rank-line {
                align-items: flex-start;
                flex-direction: column;
                gap: 0.4rem;
            }

            .rank-title {
                font-size: 0.95rem;
                line-height: 1.4;
            }

            .rank-count {
                font-size: 0.85rem;
                padding: 0.28rem 0.6rem;
            }

            .rank-names {
                font-size: 0.85rem;
            }

            div[data-testid="stButton"] button {
                min-height: 48px;
                font-size: 1rem;
            }

            label[data-testid="stWidgetLabel"] p {
                font-size: 0.95rem;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
