# streamlit_app.py (main file for multi-page app)
import streamlit as st

st.set_page_config(page_title="Glass Manufacturing Digital Twin", layout="wide")

st.title("Glass Manufacturing Digital Twin")
st.markdown("""
This digital twin application (prepared by Sandeep) helps monitor and optimize glass manufacturing processes, with modules for real-time monitoring, anomaly detection, forecasting, and GHG accounting.

Use the sidebar to navigate between modules.
""")
