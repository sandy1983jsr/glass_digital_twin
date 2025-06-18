# pages/4_GHG_Accounting.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

@st.cache_data
def load_data():
    date_rng = pd.date_range(start='2025-01-01', periods=1000, freq='H')
    return pd.DataFrame({
        'timestamp': date_rng,
        'natural_gas_consumed_m3': pd.Series(500 + 50 * np.random.randn(1000)),
        'electricity_kwh': pd.Series(1200 + 100 * np.random.randn(1000)),
        'co2_direct': pd.Series(0.185 * (500 + 50 * np.random.randn(1000))),  # Direct emissions from NG
        'co2_indirect': pd.Series(0.82 * (1200 + 100 * np.random.randn(1000))),  # Grid EF ~0.82 kgCO2/kWh
    })

data = load_data()
data['total_ghg'] = data['co2_direct'] + data['co2_indirect']

st.title("🌍 GHG Accounting Dashboard")
st.markdown("""
Estimate Scope 1 and Scope 2 emissions based on energy usage:
- **Scope 1**: Natural gas combustion (direct emissions)
- **Scope 2**: Grid electricity (indirect emissions)
""")

col1, col2, col3 = st.columns(3)
col1.metric("Direct (Scope 1) Emissions [kgCO₂]", f"{data['co2_direct'].sum():,.0f}")
col2.metric("Indirect (Scope 2) Emissions [kgCO₂]", f"{data['co2_indirect'].sum():,.0f}")
col3.metric("Total GHG Emissions [kgCO₂]", f"{data['total_ghg'].sum():,.0f}")

fig = px.area(data, x='timestamp', y=['co2_direct', 'co2_indirect'],
              title="GHG Emissions Over Time", labels={"value": "kgCO₂", "timestamp": "Time"})
st.plotly_chart(fig)
