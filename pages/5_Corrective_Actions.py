import streamlit as st
import plotly.express as px

from dashboard.database import load_corrective_action_status
from dashboard.theme import apply_theme, kpi_card, section_header

st.set_page_config(page_title="Corrective Actions", layout="wide")
apply_theme()

st.title("🛠 Corrective Actions")
st.caption("Supplier corrective action tracking, closure status, and risk monitoring")

df = load_corrective_action_status()

col1, col2, col3, col4 = st.columns(4)

with col1:
    kpi_card("Total Actions", f"{df['TotalActions'].sum():,}", "All corrective actions")

with col2:
    kpi_card("Open Actions", f"{df['OpenActions'].sum():,}", "Currently unresolved")

with col3:
    kpi_card("Closed Actions", f"{df['ClosedActions'].sum():,}", "Completed actions")

with col4:
    closure_rate = (df["ClosedActions"].sum() / df["TotalActions"].sum()) * 100 if df["TotalActions"].sum() else 0
    kpi_card("Closure Rate", f"{closure_rate:.2f}%", "Corrective action completion")

st.divider()

section_header("Corrective Action Status", "Open vs closed supplier corrective actions")

status_df = {
    "Status": ["Open", "Closed"],
    "Count": [df["OpenActions"].sum(), df["ClosedActions"].sum()]
}

fig = px.pie(
    status_df,
    names="Status",
    values="Count",
    hole=0.45,
    title="Corrective Action Status Distribution"
)
st.plotly_chart(fig, use_container_width=True)

st.divider()

section_header("Suppliers With Most Open Actions", "Suppliers requiring follow-up or escalation")

open_risk = df.sort_values("OpenActions", ascending=False).head(15)

fig = px.bar(
    open_risk,
    x="OpenActions",
    y="SupplierName",
    orientation="h",
    title="Top Suppliers by Open Corrective Actions"
)
fig.update_layout(yaxis={"categoryorder": "total ascending"}, height=600)
st.plotly_chart(fig, use_container_width=True)

st.divider()

section_header("Corrective Action Executive Insights")

highest_open = df.sort_values("OpenActions", ascending=False).iloc[0]

st.markdown(
    f"""
    <div class="section-card">
        <b>Corrective Action Summary:</b><br><br>
        The supplier network currently has <b>{df["TotalActions"].sum():,}</b> corrective actions,
        including <b>{df["OpenActions"].sum():,}</b> open items and 
        <b>{df["ClosedActions"].sum():,}</b> closed items.
        <br><br>
        The overall corrective action closure rate is <b>{closure_rate:.2f}%</b>.
        Supplier <b>{highest_open["SupplierName"]}</b> currently has the highest number of open actions,
        which may require escalation, supplier development support, or management review.
    </div>
    """,
    unsafe_allow_html=True
)

section_header("Corrective Action Detail Table")
st.dataframe(df, use_container_width=True)