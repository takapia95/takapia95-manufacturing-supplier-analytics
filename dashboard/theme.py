import streamlit as st

def apply_theme():
    st.markdown(
        """
        <style>
        /* Main app background */
        .stApp {
            background-color: #F5F7FA;
        }

        /* Page container */
        .block-container {
            padding-top: 1.5rem;
            padding-bottom: 2rem;
        }

        /* Headers */
        h1, h2, h3 {
            color: #1F2937;
            font-family: "Inter", "Segoe UI", sans-serif;
        }

        /* KPI card */
        .kpi-card {
            background: white;
            padding: 22px 24px;
            border-radius: 14px;
            box-shadow: 0 4px 14px rgba(0,0,0,0.06);
            border-left: 6px solid #1E3A8A;
            margin-bottom: 16px;
        }

        .kpi-label {
            font-size: 14px;
            color: #6B7280;
            font-weight: 600;
            margin-bottom: 6px;
        }

        .kpi-value {
            font-size: 30px;
            color: #111827;
            font-weight: 800;
        }

        .kpi-note {
            font-size: 13px;
            color: #6B7280;
            margin-top: 6px;
        }

        /* Section cards */
        .section-card {
            background: white;
            padding: 22px;
            border-radius: 14px;
            box-shadow: 0 4px 14px rgba(0,0,0,0.05);
            margin-bottom: 20px;
        }

        /* Sidebar */
        section[data-testid="stSidebar"] {
            background-color: #111827;
        }

        section[data-testid="stSidebar"] * {
            color: white;
        }

        /* Buttons */
        .stDownloadButton button {
            background-color: #1E3A8A;
            color: white;
            border-radius: 8px;
            border: none;
            font-weight: 600;
        }

        </style>
        """,
        unsafe_allow_html=True
    )


def kpi_card(label, value, note=None):
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-note">{note if note else ""}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def section_header(title, subtitle=None):
    st.markdown(f"## {title}")
    if subtitle:
        st.caption(subtitle)