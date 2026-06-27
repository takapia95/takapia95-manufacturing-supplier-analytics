import streamlit as st
import plotly.express as px

from dashboard.database import load_supplier_performance
from dashboard.theme import apply_theme, kpi_card, section_header

st.set_page_config(page_title="Executive Dashboard", layout="wide")
apply_theme()

st.title("🏭 Executive Dashboard")
st.caption("Enterprise supplier quality, delivery, and risk performance overview")

df = load_supplier_performance()

# -----------------------
# Executive KPI Cards
# -----------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    kpi_card("Total Suppliers", f"{len(df):,}", "Active supplier base")

with col2:
    kpi_card(
        "Avg Quality Score",
        f"{df['AvgQualityScore'].mean():.2f}",
        "Higher is better"
    )

with col3:
    kpi_card(
        "Avg PPM",
        f"{df['AvgPPM'].mean():.2f}",
        "Lower defect rate is better"
    )

with col4:
    kpi_card(
        "Avg On-Time Delivery",
        f"{df['AvgOnTimeDeliveryRate'].mean():.2f}%",
        "Supplier delivery reliability"
    )

st.divider()

# -----------------------
# Risk Summary
# -----------------------
section_header(
    "Supplier Performance Risk Summary",
    "Overview of supplier performance bands across the supplier base"
)

left, right = st.columns(2)

with left:
    band_counts = df["SupplierPerformanceBand"].value_counts().reset_index()
    band_counts.columns = ["Performance Band", "Supplier Count"]

    fig = px.pie(
        band_counts,
        names="Performance Band",
        values="Supplier Count",
        hole=0.45,
        title="Supplier Performance Band Distribution"
    )
    fig.update_layout(height=420)
    st.plotly_chart(fig, use_container_width=True)

with right:
    fig = px.bar(
        band_counts,
        x="Performance Band",
        y="Supplier Count",
        title="Supplier Count by Performance Band",
        text="Supplier Count"
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(height=420)
    st.plotly_chart(fig, use_container_width=True)

st.divider()

# -----------------------
# Top and Worst Suppliers
# -----------------------
section_header(
    "Supplier Ranking",
    "Best and worst suppliers based on quality performance"
)

left, right = st.columns(2)

with left:
    top_quality = df.sort_values("AvgQualityScore", ascending=False).head(10)

    fig = px.bar(
        top_quality,
        x="AvgQualityScore",
        y="SupplierName",
        orientation="h",
        title="Top 10 Suppliers by Quality Score"
    )
    fig.update_layout(
        yaxis={"categoryorder": "total ascending"},
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)

with right:
    worst_quality = df.sort_values("AvgQualityScore", ascending=True).head(10)

    fig = px.bar(
        worst_quality,
        x="AvgQualityScore",
        y="SupplierName",
        orientation="h",
        title="Bottom 10 Suppliers by Quality Score"
    )
    fig.update_layout(
        yaxis={"categoryorder": "total descending"},
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)

st.divider()

# -----------------------
# Executive Insights
# -----------------------
section_header("Executive Insights")

avg_quality = df["AvgQualityScore"].mean()
avg_ppm = df["AvgPPM"].mean()
avg_otd = df["AvgOnTimeDeliveryRate"].mean()

worst_supplier = df.sort_values("AvgQualityScore").iloc[0]
best_supplier = df.sort_values("AvgQualityScore", ascending=False).iloc[0]

st.markdown(
    f"""
    <div class="section-card">
        <b>Key Business Summary:</b><br><br>
        The supplier network currently includes <b>{len(df):,}</b> active suppliers.
        The average quality score is <b>{avg_quality:.2f}</b>, with an average defect rate of
        <b>{avg_ppm:.2f} PPM</b> and average on-time delivery rate of <b>{avg_otd:.2f}%</b>.
        <br><br>
        The strongest supplier by quality score is <b>{best_supplier["SupplierName"]}</b>.
        The lowest-performing supplier is <b>{worst_supplier["SupplierName"]}</b>, which may require
        additional supplier development review, corrective action tracking, or process validation.
    </div>
    """,
    unsafe_allow_html=True
)

# -----------------------
# Supplier Table
# -----------------------
section_header(
    "Supplier Performance Detail",
    "Detailed supplier-level metrics for quality, delivery, and risk review"
)

st.dataframe(df, use_container_width=True)