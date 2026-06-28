import streamlit as st
import plotly.express as px

from dashboard.database import (
    load_supplier_performance,
    load_delivery_summary,
    load_inventory_summary,
    load_corrective_action_status,
    load_executive_kpis,
    load_monthly_trends,
)
from dashboard.theme import apply_theme, kpi_card, section_header
from dashboard.insights import (
    generate_executive_summary,
    generate_recommendations,
)
from dashboard.scoring import calculate_supplier_risk_scores
from dashboard.alerts import generate_alerts
from dashboard.narrative import generate_executive_narrative
st.set_page_config(page_title="Executive Dashboard", layout="wide")
apply_theme()

st.title("🏭 Executive Dashboard")
st.caption("Enterprise supplier quality, delivery, and risk performance overview")

supplier_df = load_supplier_performance()
delivery_df = load_delivery_summary()
inventory_df = load_inventory_summary()
corrective_df = load_corrective_action_status()
kpi_df = load_executive_kpis()
monthly_df = load_monthly_trends()

# Keep df for the existing charts and table
df = supplier_df
df = calculate_supplier_risk_scores(df)
alerts_df = generate_alerts(df)
executive_narrative = generate_executive_narrative(df, alerts_df)
executive_insights = generate_executive_summary(
    kpi_df=kpi_df,
    supplier_df=supplier_df,
    delivery_df=delivery_df,
    inventory_df=inventory_df,
    ca_df=corrective_df
)

executive_recommendations = generate_recommendations(
    kpi_df=kpi_df,
    supplier_df=supplier_df,
    delivery_df=delivery_df,
    inventory_df=inventory_df,
    ca_df=corrective_df
)

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
st.divider()

section_header(
    "Supplier Risk Heat Map",
    "Visual comparison of supplier quality, delivery reliability, defect exposure, and risk rating"
)

if all(col in df.columns for col in [
    "AvgQualityScore",
    "AvgOnTimeDeliveryRate",
    "AvgPPM",
    "SupplierRiskRating",
    "SupplierName",
]):
    fig = px.scatter(
        df,
        x="AvgQualityScore",
        y="AvgOnTimeDeliveryRate",
        size="AvgPPM",
        color="SupplierRiskRating",
        hover_name="SupplierName",
        hover_data={
            "AvgQualityScore": ":.2f",
            "AvgOnTimeDeliveryRate": ":.2f",
            "AvgPPM": ":.0f",
            "SupplierRiskScore": ":.2f",
            "SupplierRiskRating": True,
        },
        title="Supplier Risk Heat Map: Quality vs Delivery",
    )

    fig.update_layout(
        height=550,
        xaxis_title="Average Quality Score",
        yaxis_title="Average On-Time Delivery Rate (%)",
    )

    st.plotly_chart(fig, use_container_width=True)

else:
    st.warning("Supplier risk heat map cannot be displayed because required columns are missing.")
# -----------------------
# Executive Intelligence
# -----------------------
st.divider()

section_header(
    "Executive Alert Center",
    "High-priority supplier issues requiring management attention"
)
st.markdown(
    f"""
    <div class="section-card">
        <b>Executive Narrative Briefing:</b><br><br>
        {executive_narrative}
    </div>
    """,
    unsafe_allow_html=True
)
if alerts_df.empty:
    st.success("✅ No critical supplier alerts at this time.")
else:

    severity_order = {
        "Critical": 1,
        "Warning": 2,
    }

    alerts_df["Order"] = alerts_df["Severity"].map(severity_order)
    alerts_df = alerts_df.sort_values("Order").drop(columns="Order")

    def severity_icon(level):
        if level == "Critical":
            return "🔴"
        if level == "Warning":
            return "🟡"
        return "🟢"

    for _, row in alerts_df.head(10).iterrows():

        st.markdown(
            f"""
            <div class="section-card">
                <b>{severity_icon(row['Severity'])} {row['Severity']}</b><br><br>

                <b>Category:</b> {row['Category']}<br>

                <b>Supplier:</b> {row['Supplier']}<br>

                <b>Issue:</b> {row['Message']}
            </div>
            """,
            unsafe_allow_html=True
        )
section_header(
    "Executive Intelligence",
    "Automated business interpretation of supplier quality, delivery, and risk performance"
)

st.markdown("### Executive Summary")

for insight in executive_insights:
    st.markdown(
        f"""
        <div class="section-card">
            <b>Insight:</b><br>
            {insight}
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("### Recommended Executive Actions")

for recommendation in executive_recommendations:
    st.markdown(
        f"""
        <div class="section-card">
            <b>Recommended Action:</b><br>
            {recommendation}
        </div>
        """,
        unsafe_allow_html=True
    )

st.divider()

# -----------------------
# Supplier Table
# -----------------------
section_header(
    "Supplier Performance Detail",
    "Detailed supplier-level metrics for quality, delivery, and risk review"
)

display_columns = [
    "SupplierName",
    "AvgQualityScore",
    "AvgPPM",
    "AvgOnTimeDeliveryRate",
    "SupplierPerformanceBand",
    "SupplierRiskScore",
    "SupplierRiskRating",
]

available_columns = [col for col in display_columns if col in df.columns]

st.dataframe(
    df[available_columns].sort_values("SupplierRiskScore", ascending=True),
    use_container_width=True
)