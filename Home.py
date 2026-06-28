import streamlit as st

from dashboard.theme import apply_theme, kpi_card, section_header
from dashboard.database import (
    load_supplier_performance,
    load_delivery_summary,
    load_inventory_summary,
    load_corrective_action_status,
)

st.set_page_config(page_title="Supplier Quality Analytics Dashboard", layout="wide")
apply_theme()

# -----------------------
# Hero Section
# -----------------------
st.title("🏭 Supplier Quality Analytics Dashboard")
st.caption("Enterprise Manufacturing Analytics Platform")

st.markdown(
    """
    <div class="section-card">
        <h3>Supplier Quality, Delivery, Inventory, and Corrective Action Intelligence</h3>
        <p>
        This dashboard simulates a production-style manufacturing analytics platform used to monitor
        supplier performance, identify operational risk, analyze delivery reliability, track inventory exposure,
        and review corrective action status.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# -----------------------
# Load Data
# -----------------------
supplier_df = load_supplier_performance()
delivery_df = load_delivery_summary()
inventory_df = load_inventory_summary()
car_df = load_corrective_action_status()

# -----------------------
# Executive Snapshot
# -----------------------
section_header("Executive Snapshot", "High-level overview of supplier network health")

col1, col2, col3, col4 = st.columns(4)

with col1:
    kpi_card("Total Suppliers", f"{len(supplier_df):,}", "Active supplier base")

with col2:
    kpi_card(
        "Avg Quality Score",
        f"{supplier_df['AvgQualityScore'].mean():.2f}",
        "Supplier quality performance"
    )

with col3:
    kpi_card(
        "Avg OTD Rate",
        f"{delivery_df['OnTimeDeliveryRate'].mean():.2f}%",
        "On-time delivery reliability"
    )

with col4:
    kpi_card(
        "Open Actions",
        f"{car_df['OpenActions'].sum():,}",
        "Supplier corrective action backlog"
    )

st.divider()

# -----------------------
# Dashboard Modules
# -----------------------
section_header("Dashboard Modules", "Use the sidebar to navigate through each analytics area")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
        <div class="section-card">
            <h4>🏭 Executive Dashboard</h4>
            <p>Monitor supplier quality, defect rate, delivery performance, and supplier risk bands.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="section-card">
            <h4>🚚 Delivery Analysis</h4>
            <p>Analyze late deliveries, on-time delivery rate, and suppliers with delivery risk.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        """
        <div class="section-card">
            <h4>📈 Monthly Trends</h4>
            <p>Track supplier quality score, PPM, scrap cost, and delivery trends over time.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="section-card">
            <h4>📦 Inventory Analytics</h4>
            <p>Review inventory exposure, low-stock items, and supplier-related inventory value.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        """
        <div class="section-card">
            <h4>🛠 Corrective Actions</h4>
            <p>Track open, closed, and overdue supplier corrective actions across the supplier base.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="section-card">
            <h4>📊 Executive KPIs</h4>
            <p>View consolidated enterprise-level KPIs for leadership reporting.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

st.divider()

# -----------------------
# Architecture
# -----------------------
section_header("Project Architecture", "End-to-end BI and data engineering workflow")

st.markdown(
    """
    <div class="section-card">
        <h4>Data Pipeline</h4>
        <p>
        CSV Source Data → Python ETL → MySQL Database → SQL Views → Pandas/SQLAlchemy → Streamlit Dashboard
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# -----------------------
# Technology Stack
# -----------------------
section_header("Technology Stack")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("**Database**  \nMySQL")

with col2:
    st.markdown("**Backend**  \nPython, Pandas, SQLAlchemy")

with col3:
    st.markdown("**Visualization**  \nPlotly, Streamlit")

with col4:
    st.markdown("**Business Logic**  \nSQL Views, ETL Pipeline")

st.divider()

# -----------------------
# Portfolio Summary
# -----------------------
section_header("Portfolio Project Summary")

st.markdown(
    """
    <div class="section-card">
        <p>
        This project demonstrates practical BI, data engineering, and manufacturing analytics skills:
        database design, ETL development, SQL business logic, KPI modeling, dashboard engineering,
        and executive-level data storytelling.
        </p>
        <p>
        It is designed for roles such as Manufacturing Data Analyst, BI Analyst, Supplier Quality Analyst,
        Operations Data Analyst, and Connected Factory Data Engineer.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)