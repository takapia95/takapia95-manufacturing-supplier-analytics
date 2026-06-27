import streamlit as st
import plotly.express as px
from dashboard.database import load_supplier_performance

st.set_page_config(page_title="Executive Dashboard", layout="wide")

st.title("🏭 Executive Dashboard")

df = load_supplier_performance()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Suppliers", len(df))
col2.metric("Avg Quality Score", round(df["AvgQualityScore"].mean(), 2))
col3.metric("Avg PPM", round(df["AvgPPM"].mean(), 2))
col4.metric("Avg OTD", round(df["AvgOnTimeDeliveryRate"].mean(), 2))

st.divider()

left, right = st.columns(2)

with left:
    st.subheader("Performance Band")
    fig = px.pie(
        df,
        names="SupplierPerformanceBand",
        hole=0.4
    )
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("Top 10 Suppliers by Quality")
    top_quality = df.sort_values("AvgQualityScore", ascending=False).head(10)
    fig = px.bar(
        top_quality,
        x="AvgQualityScore",
        y="SupplierName",
        orientation="h"
    )
    fig.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Supplier Table")
st.dataframe(df, use_container_width=True)