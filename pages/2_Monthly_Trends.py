import streamlit as st
import plotly.express as px
from dashboard.database import load_monthly_trends

st.set_page_config(page_title="Monthly Trends", layout="wide")

st.title("📈 Monthly Supplier Trends")

df = load_monthly_trends()

df["Month"] = df["Month"].astype(str)

supplier = st.sidebar.selectbox(
    "Select Supplier",
    options=["All"] + sorted(df["SupplierID"].unique())
)

if supplier != "All":
    df = df[df["SupplierID"] == supplier]

col1, col2 = st.columns(2)

with col1:
    st.subheader("Supplier Quality Score Over Time")
    fig = px.line(df, x="Month", y="SupplierQualityScore", color="SupplierID")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("PPM Over Time")
    fig = px.line(df, x="Month", y="PPM", color="SupplierID")
    st.plotly_chart(fig, use_container_width=True)

col3, col4 = st.columns(2)

with col3:
    st.subheader("Scrap Cost Over Time")
    fig = px.line(df, x="Month", y="ScrapCost", color="SupplierID")
    st.plotly_chart(fig, use_container_width=True)

with col4:
    st.subheader("On-Time Delivery Rate Over Time")
    fig = px.line(df, x="Month", y="OnTimeDeliveryRate", color="SupplierID")
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Monthly KPI Data")
st.dataframe(df, use_container_width=True)