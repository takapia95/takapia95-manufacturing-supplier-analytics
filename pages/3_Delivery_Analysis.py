import streamlit as st
import plotly.express as px

from dashboard.database import load_delivery_summary
from dashboard.theme import apply_theme, kpi_card, section_header

st.set_page_config(page_title="Delivery Analysis", layout="wide")
apply_theme()

st.title("🚚 Delivery Analysis")
st.caption("Supplier delivery reliability, late shipment risk, and on-time performance monitoring")

df = load_delivery_summary()

# -----------------------
# KPI Cards
# -----------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    kpi_card("Total Deliveries", f"{df['TotalDeliveries'].sum():,}", "All supplier deliveries")

with col2:
    kpi_card("Late Deliveries", f"{df['LateDeliveries'].sum():,}", "Total delayed deliveries")

with col3:
    avg_otd = df["OnTimeDeliveryRate"].mean()
    kpi_card("Avg OTD Rate", f"{avg_otd:.2f}%", "Average supplier delivery reliability")

with col4:
    worst_supplier = df.sort_values("OnTimeDeliveryRate").iloc[0]
    kpi_card("Highest Risk Supplier", worst_supplier["SupplierName"], "Lowest delivery performance")

st.divider()

# -----------------------
# Delivery Performance Charts
# -----------------------
section_header(
    "Delivery Performance Overview",
    "Supplier-level on-time delivery and late delivery risk"
)

left, right = st.columns(2)

with left:
    top_delivery = df.sort_values("OnTimeDeliveryRate", ascending=False).head(10)

    fig = px.bar(
        top_delivery,
        x="OnTimeDeliveryRate",
        y="SupplierName",
        orientation="h",
        title="Top 10 Suppliers by On-Time Delivery Rate"
    )
    fig.update_layout(yaxis={"categoryorder": "total ascending"}, height=500)
    st.plotly_chart(fig, use_container_width=True)

with right:
    worst_delivery = df.sort_values("OnTimeDeliveryRate", ascending=True).head(10)

    fig = px.bar(
        worst_delivery,
        x="OnTimeDeliveryRate",
        y="SupplierName",
        orientation="h",
        title="Bottom 10 Suppliers by On-Time Delivery Rate"
    )
    fig.update_layout(yaxis={"categoryorder": "total descending"}, height=500)
    st.plotly_chart(fig, use_container_width=True)

st.divider()

# -----------------------
# Late Delivery Risk
# -----------------------
section_header(
    "Late Delivery Risk",
    "Suppliers contributing the highest number of delayed shipments"
)

late_risk = df.sort_values("LateDeliveries", ascending=False).head(15)

fig = px.bar(
    late_risk,
    x="LateDeliveries",
    y="SupplierName",
    orientation="h",
    title="Top Late Delivery Contributors"
)
fig.update_layout(yaxis={"categoryorder": "total ascending"}, height=600)
st.plotly_chart(fig, use_container_width=True)

st.divider()

# -----------------------
# Executive Insight
# -----------------------
section_header("Delivery Executive Insights")

total_deliveries = df["TotalDeliveries"].sum()
late_deliveries = df["LateDeliveries"].sum()
late_rate = (late_deliveries / total_deliveries) * 100 if total_deliveries else 0

best_supplier = df.sort_values("OnTimeDeliveryRate", ascending=False).iloc[0]
worst_supplier = df.sort_values("OnTimeDeliveryRate", ascending=True).iloc[0]

st.markdown(
    f"""
    <div class="section-card">
        <b>Delivery Performance Summary:</b><br><br>
        The supplier network recorded <b>{total_deliveries:,}</b> total deliveries, with 
        <b>{late_deliveries:,}</b> late deliveries. This represents an estimated late delivery rate of 
        <b>{late_rate:.2f}%</b>.
        <br><br>
        The strongest delivery performer is <b>{best_supplier["SupplierName"]}</b> with an on-time delivery rate of 
        <b>{best_supplier["OnTimeDeliveryRate"]:.2f}%</b>.
        The highest delivery-risk supplier is <b>{worst_supplier["SupplierName"]}</b> with an on-time delivery rate of 
        <b>{worst_supplier["OnTimeDeliveryRate"]:.2f}%</b>.
        <br><br>
        Recommended business action: review suppliers with low delivery reliability for capacity constraints,
        logistics issues, production delays, or recurring shipment planning problems.
    </div>
    """,
    unsafe_allow_html=True
)

st.divider()

# -----------------------
# Data Table
# -----------------------
section_header("Delivery Detail Table")

st.dataframe(df, use_container_width=True)