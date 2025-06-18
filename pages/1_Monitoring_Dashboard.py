# pages/1_Monitoring_Dashboard.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

@st.cache_data
def load_data():
    date_rng = pd.date_range(start='2025-01-01', periods=1000, freq='H')
    return pd.DataFrame({
        'timestamp': date_rng,
        'furnace_temp': pd.Series(1450 + 30 * np.random.randn(1000)),
        'pull_rate': pd.Series(25 + 5 * np.random.randn(1000)),
        'energy_consumption': pd.Series(1200 + 100 * np.random.randn(1000)),
        'flue_o2': pd.Series(3.5 + 0.5 * np.random.randn(1000)),
        'co2_emission': pd.Series(800 + 50 * np.random.randn(1000)),
    })

data = load_data()

st.title("📈 Monitoring Dashboard")
selected_kpi = st.selectbox("Select KPI to visualize", data.columns[1:])
fig = px.line(data, x='timestamp', y=selected_kpi, title=f"{selected_kpi} Over Time")
st.plotly_chart(fig)
