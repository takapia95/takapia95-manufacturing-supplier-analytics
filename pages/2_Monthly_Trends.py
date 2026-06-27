import streamlit as st
import plotly.express as px

from dashboard.database import load_monthly_trends
from dashboard.theme import apply_theme, section_header

st.set_page_config(page_title="Monthly Trends", layout="wide")
apply_theme()

st.title("📈 Monthly Supplier Trends")
st.caption("Monthly supplier quality, delivery, scrap cost, and defect trend monitoring")

df = load_monthly_trends()

df["Month"] = df["Month"].astype(str)

# -----------------------
# Sidebar Filters
# -----------------------
st.sidebar.header("Trend Filters")

supplier_options = ["All"] + sorted(df["SupplierID"].dropna().unique().tolist())

supplier = st.sidebar.selectbox(
    "Select Supplier",
    options=supplier_options
)

if supplier != "All":
    df = df[df["SupplierID"] == supplier]

# -----------------------
# KPI Summary
# -----------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("Avg Quality Score", f"{df['SupplierQualityScore'].mean():.2f}")
col2.metric("Avg PPM", f"{df['PPM'].mean():.2f}")
col3.metric("Total Scrap Cost", f"${df['ScrapCost'].sum():,.0f}")
col4.metric("Avg OTD", f"{df['OnTimeDeliveryRate'].mean():.2f}%")

st.divider()

# -----------------------
# Moving Averages
# -----------------------
df = df.sort_values(["SupplierID", "Month"])

df["QualityScore_MA3"] = (
    df.groupby("SupplierID")["SupplierQualityScore"]
    .transform(lambda x: x.rolling(window=3, min_periods=1).mean())
)

df["PPM_MA3"] = (
    df.groupby("SupplierID")["PPM"]
    .transform(lambda x: x.rolling(window=3, min_periods=1).mean())
)

# -----------------------
# Charts
# -----------------------
section_header(
    "Supplier Quality and Defect Trends",
    "Monthly trend analysis with 3-month moving averages"
)

col1, col2 = st.columns(2)

with col1:
    fig = px.line(
        df,
        x="Month",
        y="SupplierQualityScore",
        color="SupplierID",
        markers=True,
        title="Supplier Quality Score Over Time"
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.line(
        df,
        x="Month",
        y="QualityScore_MA3",
        color="SupplierID",
        markers=True,
        title="3-Month Moving Avg Quality Score"
    )
    st.plotly_chart(fig, use_container_width=True)

col3, col4 = st.columns(2)

with col3:
    fig = px.line(
        df,
        x="Month",
        y="PPM",
        color="SupplierID",
        markers=True,
        title="PPM Over Time"
    )
    st.plotly_chart(fig, use_container_width=True)

with col4:
    fig = px.line(
        df,
        x="Month",
        y="PPM_MA3",
        color="SupplierID",
        markers=True,
        title="3-Month Moving Avg PPM"
    )
    st.plotly_chart(fig, use_container_width=True)

st.divider()

section_header(
    "Cost and Delivery Trends",
    "Scrap cost and delivery reliability performance over time"
)

col5, col6 = st.columns(2)

with col5:
    fig = px.line(
        df,
        x="Month",
        y="ScrapCost",
        color="SupplierID",
        markers=True,
        title="Scrap Cost Over Time"
    )
    st.plotly_chart(fig, use_container_width=True)

with col6:
    fig = px.line(
        df,
        x="Month",
        y="OnTimeDeliveryRate",
        color="SupplierID",
        markers=True,
        title="On-Time Delivery Rate Over Time"
    )
    st.plotly_chart(fig, use_container_width=True)

st.divider()

# -----------------------
# Executive Trend Insight
# -----------------------
section_header("Trend Insights")

best_month = df.sort_values("SupplierQualityScore", ascending=False).iloc[0]
worst_month = df.sort_values("SupplierQualityScore", ascending=True).iloc[0]
highest_ppm = df.sort_values("PPM", ascending=False).iloc[0]

st.markdown(
    f"""
    <div class="section-card">
        <b>Monthly Trend Summary:</b><br><br>
        The selected supplier view shows an average quality score of 
        <b>{df['SupplierQualityScore'].mean():.2f}</b>, average PPM of 
        <b>{df['PPM'].mean():.2f}</b>, total scrap cost of 
        <b>${df['ScrapCost'].sum():,.0f}</b>, and average on-time delivery rate of 
        <b>{df['OnTimeDeliveryRate'].mean():.2f}%</b>.
        <br><br>
        The strongest monthly quality performance occurred for supplier 
        <b>{best_month['SupplierID']}</b> in <b>{best_month['Month']}</b>.
        The weakest monthly quality performance occurred for supplier 
        <b>{worst_month['SupplierID']}</b> in <b>{worst_month['Month']}</b>.
        The highest defect level was supplier <b>{highest_ppm['SupplierID']}</b>
        in <b>{highest_ppm['Month']}</b>.
    </div>
    """,
    unsafe_allow_html=True
)

# -----------------------
# Data Table
# -----------------------
section_header("Monthly KPI Data")

st.dataframe(df, use_container_width=True)