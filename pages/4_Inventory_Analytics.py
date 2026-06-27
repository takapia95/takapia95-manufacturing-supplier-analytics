import streamlit as st
import plotly.express as px

from dashboard.database import load_inventory_summary
from dashboard.theme import apply_theme, kpi_card, section_header

st.set_page_config(page_title="Inventory Analytics", layout="wide")
apply_theme()

st.title("📦 Inventory Analytics")
st.caption("Inventory cost, stock risk, and supplier-related inventory monitoring")

df = load_inventory_summary()

col1, col2, col3, col4 = st.columns(4)

with col1:
    kpi_card("Total Inventory Value", f"${df['InventoryValue'].sum():,.0f}", "Current inventory exposure")

with col2:
    kpi_card("Avg Stock Level", f"{df['StockLevel'].mean():.2f}", "Average available stock")

with col3:
    kpi_card("Low Stock Items", f"{df['LowStockFlag'].sum():,}", "Items below threshold")

with col4:
    highest_value = df.sort_values("InventoryValue", ascending=False).iloc[0]
    kpi_card("Highest Value Item", highest_value["PartName"], "Largest inventory exposure")

st.divider()

section_header("Inventory Value Analysis", "Parts and suppliers with the highest inventory exposure")

top_inventory = df.sort_values("InventoryValue", ascending=False).head(15)

fig = px.bar(
    top_inventory,
    x="InventoryValue",
    y="PartName",
    orientation="h",
    title="Top 15 Parts by Inventory Value"
)
fig.update_layout(yaxis={"categoryorder": "total ascending"}, height=600)
st.plotly_chart(fig, use_container_width=True)

st.divider()

left, right = st.columns(2)

with left:
    section_header("Stock Level by Part")
    stock_df = df.sort_values("StockLevel", ascending=True).head(15)

    fig = px.bar(
        stock_df,
        x="StockLevel",
        y="PartName",
        orientation="h",
        title="Lowest Stock Level Parts"
    )
    fig.update_layout(yaxis={"categoryorder": "total descending"}, height=500)
    st.plotly_chart(fig, use_container_width=True)

with right:
    section_header("Inventory by Supplier")
    supplier_inventory = (
        df.groupby("SupplierName", as_index=False)["InventoryValue"]
        .sum()
        .sort_values("InventoryValue", ascending=False)
        .head(10)
    )

    fig = px.pie(
        supplier_inventory,
        names="SupplierName",
        values="InventoryValue",
        hole=0.45,
        title="Top Supplier Inventory Exposure"
    )
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)

st.divider()

section_header("Inventory Executive Insights")

low_stock_count = df["LowStockFlag"].sum()
total_value = df["InventoryValue"].sum()

st.markdown(
    f"""
    <div class="section-card">
        <b>Inventory Summary:</b><br><br>
        Current inventory exposure is <b>${total_value:,.0f}</b>.
        There are <b>{low_stock_count:,}</b> low-stock items that may require purchasing,
        supplier follow-up, or production planning review.
        <br><br>
        The highest inventory value item is <b>{highest_value["PartName"]}</b>,
        representing a potential area for cost control and inventory optimization.
    </div>
    """,
    unsafe_allow_html=True
)

section_header("Inventory Detail Table")
st.dataframe(df, use_container_width=True)