import streamlit as st
import plotly.express as px

from dashboard.database import load_executive_kpis
from dashboard.theme import apply_theme, kpi_card, section_header

st.set_page_config(page_title="Executive KPIs", layout="wide")
apply_theme()

st.title("📊 Executive KPI Summary")
st.caption("High-level supplier quality, delivery, inventory, and corrective action performance")

df = load_executive_kpis()

row = df.iloc[0]

col1, col2, col3, col4 = st.columns(4)

with col1:
    kpi_card("Total Suppliers", f"{row['TotalSuppliers']:,}", "Active supplier base")

with col2:
    kpi_card("Avg Quality Score", f"{row['AvgQualityScore']:.2f}", "Overall quality health")

with col3:
    kpi_card("Avg PPM", f"{row['AvgPPM']:.2f}", "Overall defect rate")

with col4:
    kpi_card("Avg OTD Rate", f"{row['AvgOnTimeDeliveryRate']:.2f}%", "Delivery reliability")

st.divider()

col5, col6, col7, col8 = st.columns(4)

with col5:
    kpi_card("Total Scrap Cost", f"${row['TotalScrapCost']:,.0f}", "Quality cost impact")

with col6:
    kpi_card("Inventory Value", f"${row['TotalInventoryValue']:,.0f}", "Inventory exposure")

with col7:
    kpi_card("Open Actions", f"{row['OpenCorrectiveActions']:,}", "Supplier issue backlog")

with col8:
    kpi_card("Late Deliveries", f"{row['LateDeliveries']:,}", "Delivery risk signal")

st.divider()

section_header("Executive Performance Snapshot")

kpi_chart = {
    "Metric": [
        "Avg Quality Score",
        "Avg PPM",
        "Avg OTD Rate",
        "Open Corrective Actions",
        "Late Deliveries"
    ],
    "Value": [
        row["AvgQualityScore"],
        row["AvgPPM"],
        row["AvgOnTimeDeliveryRate"],
        row["OpenCorrectiveActions"],
        row["LateDeliveries"]
    ]
}

fig = px.bar(
    kpi_chart,
    x="Metric",
    y="Value",
    title="Executive KPI Overview"
)
st.plotly_chart(fig, use_container_width=True)

st.divider()

section_header("AI-Style Executive Insights")

st.markdown(
    f"""
    <div class="section-card">
        <b>Executive Business Summary:</b><br><br>
        The supplier quality network includes <b>{row['TotalSuppliers']:,}</b> active suppliers.
        Current average quality performance is <b>{row['AvgQualityScore']:.2f}</b>,
        with an average defect rate of <b>{row['AvgPPM']:.2f} PPM</b>.
        <br><br>
        Delivery reliability is currently averaging <b>{row['AvgOnTimeDeliveryRate']:.2f}%</b>,
        with <b>{row['LateDeliveries']:,}</b> late deliveries recorded.
        Total scrap cost is <b>${row['TotalScrapCost']:,.0f}</b>, and total inventory exposure is
        <b>${row['TotalInventoryValue']:,.0f}</b>.
        <br><br>
        There are <b>{row['OpenCorrectiveActions']:,}</b> open corrective actions.
        Management should prioritize suppliers with recurring quality defects, late deliveries,
        and unresolved corrective actions to reduce operational risk.
    </div>
    """,
    unsafe_allow_html=True
)

section_header("Executive KPI Data")
st.dataframe(df, use_container_width=True)