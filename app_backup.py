import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

st.set_page_config(page_title="Supplier Quality Analytics Dashboard", layout="wide")

st.title("🏭 Supplier Quality Analytics Dashboard")
st.caption("Manufacturing supplier quality, delivery, and risk monitoring dashboard")

engine = create_engine(
    "mysql+pymysql://root@127.0.0.1:3306/supplier_quality_analytics",
    connect_args={"connect_timeout": 5}
)

df = pd.read_sql("SELECT * FROM vw_supplier_performance", engine)

# -----------------------
# Sidebar Filters
# -----------------------
st.sidebar.header("Dashboard Filters")

category_filter = st.sidebar.multiselect(
    "Supplier Category",
    options=sorted(df["SupplierCategory"].dropna().unique()),
    default=sorted(df["SupplierCategory"].dropna().unique())
)

risk_filter = st.sidebar.multiselect(
    "Risk Level",
    options=sorted(df["RiskLevel"].dropna().unique()),
    default=sorted(df["RiskLevel"].dropna().unique())
)

band_filter = st.sidebar.multiselect(
    "Performance Band",
    options=sorted(df["SupplierPerformanceBand"].dropna().unique()),
    default=sorted(df["SupplierPerformanceBand"].dropna().unique())
)

supplier_filter = st.sidebar.multiselect(
    "Supplier",
    options=sorted(df["SupplierName"].dropna().unique()),
    default=sorted(df["SupplierName"].dropna().unique())
)

filtered_df = df[
    (df["SupplierCategory"].isin(category_filter)) &
    (df["RiskLevel"].isin(risk_filter)) &
    (df["SupplierPerformanceBand"].isin(band_filter)) &
    (df["SupplierName"].isin(supplier_filter))
]

# -----------------------
# KPI Cards
# -----------------------
col1, col2, col3, col4, col5, col6 = st.columns(6)

col1.metric("🏭 Suppliers", len(filtered_df))
col2.metric("⭐ Avg Quality", round(filtered_df["AvgQualityScore"].mean(), 2))
col3.metric("📦 Avg PPM", round(filtered_df["AvgPPM"].mean(), 2))
col4.metric("🚚 Avg OTD", round(filtered_df["AvgOnTimeDeliveryRate"].mean(), 2))
col5.metric("⚠️ High Risk", filtered_df[filtered_df["RiskLevel"] == "High"].shape[0])
col6.metric("🚨 Critical", filtered_df[filtered_df["SupplierPerformanceBand"] == "Critical"].shape[0])

st.divider()

# -----------------------
# Charts
# -----------------------
left, right = st.columns(2)

with left:
    st.subheader("Supplier Performance Bands")
    band_counts = filtered_df["SupplierPerformanceBand"].value_counts().reset_index()
    band_counts.columns = ["Performance Band", "Count"]

    fig_band = px.pie(
        band_counts,
        names="Performance Band",
        values="Count",
        hole=0.4
    )
    st.plotly_chart(fig_band, use_container_width=True)

with right:
    st.subheader("Top 10 Suppliers by Quality Score")
    top_quality = filtered_df.sort_values("AvgQualityScore", ascending=False).head(10)

    fig_quality = px.bar(
        top_quality,
        x="AvgQualityScore",
        y="SupplierName",
        orientation="h"
    )
    fig_quality.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig_quality, use_container_width=True)

st.subheader("Highest PPM Suppliers")
top_ppm = filtered_df.sort_values("AvgPPM", ascending=False).head(10)

fig_ppm = px.bar(
    top_ppm,
    x="AvgPPM",
    y="SupplierName",
    orientation="h"
)
fig_ppm.update_layout(yaxis={"categoryorder": "total ascending"})
st.plotly_chart(fig_ppm, use_container_width=True)

# -----------------------
# Data Table + Download
# -----------------------
st.subheader("Supplier Performance Table")
st.dataframe(filtered_df, use_container_width=True)

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇️ Download Supplier Report CSV",
    data=csv,
    file_name="supplier_performance_report.csv",
    mime="text/csv"
)