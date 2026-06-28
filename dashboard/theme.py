import streamlit as st


def apply_theme():
    st.markdown(
        """
        <style>

        /* -----------------------
           Global
        ------------------------ */

        .stApp {
            background-color: #F5F7FA;
            color: #111827;
        }

        .block-container {
            padding-top: 1.5rem;
            padding-bottom: 2rem;
        }

        h1, h2, h3, h4 {
            color: #1F2937;
            font-family: "Inter", "Segoe UI", sans-serif;
        }

        p {
            color: #374151;
        }

        /* -----------------------
           KPI Cards
        ------------------------ */

        .kpi-card {
            background: white;
            padding: 22px;
            border-radius: 14px;
            box-shadow: 0 4px 14px rgba(0,0,0,0.06);
            border-left: 6px solid #1E3A8A;
            margin-bottom: 18px;
        }

        .kpi-label {
            font-size: 14px;
            color: #6B7280;
            font-weight: 600;
        }

        .kpi-value {
            font-size: 30px;
            font-weight: 700;
            color: #111827;
        }

        .kpi-note {
            font-size: 13px;
            color: #6B7280;
        }

        /* -----------------------
           Section Cards
        ------------------------ */

        .section-card {
            background: white;
            padding: 22px;
            border-radius: 14px;
            box-shadow: 0 4px 14px rgba(0,0,0,.05);
            margin-bottom: 20px;
        }

        .section-card h3,
        .section-card h4,
        .section-card p {
            color: #111827 !important;
        }

        /* -----------------------
           Sidebar
        ------------------------ */

        section[data-testid="stSidebar"] {
            background-color: #111827;
        }

        section[data-testid="stSidebar"] * {
            color: #F9FAFB !important;
        }

        /* -----------------------
           Buttons
        ------------------------ */

        .stDownloadButton button {
            background: #1E3A8A;
            color: white;
            border-radius: 8px;
            border: none;
            font-weight: 600;
        }

        </style>
        """,
        unsafe_allow_html=True
    )


def kpi_card(label, value, note=""):
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-note">{note}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_header(title, subtitle=None):
    st.markdown(f"## {title}")
    if subtitle:
        st.caption(subtitle)