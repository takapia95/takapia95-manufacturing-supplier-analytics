import streamlit as st

st.set_page_config(
    page_title="Supplier Quality Analytics",
    layout="wide"
)

st.title("🏭 Supplier Quality Analytics Dashboard")

st.markdown("""
Welcome to the Supplier Quality Analytics Dashboard.

Use the sidebar to navigate between:

- **Executive Dashboard**
- **Monthly Trends**

This project analyzes supplier quality, delivery performance, defect rates, PPM, scrap cost, and supplier risk levels using MySQL, SQL views, Python, and Streamlit.
""")