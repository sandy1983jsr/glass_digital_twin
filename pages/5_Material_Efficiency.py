# pages/5_Material_Efficiency.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

@st.cache_data
def load_data():
    date_rng = pd.date_range(start='2025-01-01', periods=1000, freq='H')
    return pd.DataFrame({
        'timestamp': date_rng,
        'cullet_percent': pd.Series(40 + 10 * np.random.randn(1000)),
        'batch_input_ton': pd.Series(100 + 5 * np.random.randn(1000)),
        'glass_output_ton': pd.Series(95 + 5 * np.random.randn(1000)),
        'energy_kwh': pd.Series(1200 + 100 * np.random.randn(1000)),
        'co2_emission_kg': pd.Series(1000 + 100 * np.random.randn(1000))
    })

data = load_data()
data['material_yield_percent'] = 100 * data['glass_output_ton'] / data['batch_input_ton']

st.title("🧪 Material Efficiency Dashboard")
st.markdown("""
Track material usage, cullet ratio, and their impact on energy and GHG metrics. Alerts are triggered for abnormal material yield drops.
""")

# Metrics
col1, col2, col3 = st.columns(3)
col1.metric("Average Cullet %", f"{data['cullet_percent'].mean():.1f}%")
col2.metric("Avg Material Yield %", f"{data['material_yield_percent'].mean():.1f}%")
col3.metric("Energy per Output (kWh/ton)", f"{(data['energy_kwh'] / data['glass_output_ton']).mean():.1f}")

# Correlation
corr_energy = data['material_yield_percent'].corr(data['energy_kwh'])
corr_ghg = data['material_yield_percent'].corr(data['co2_emission_kg'])

st.subheader("🔗 Correlation with Material Yield")
st.write(f"- Correlation with Energy Use: {corr_energy:.2f}")
st.write(f"- Correlation with CO₂ Emissions: {corr_ghg:.2f}")

# Visualization
fig = px.line(data, x='timestamp', y=['cullet_percent', 'material_yield_percent'],
              title="Cullet Ratio and Material Yield Over Time",
              labels={"value": "%", "timestamp": "Time"})
st.plotly_chart(fig)

# Alert logic
alert_threshold = 90
if data['material_yield_percent'].iloc[-1] < alert_threshold:
    st.error(f"⚠️ Alert: Material yield dropped below {alert_threshold}% (Current: {data['material_yield_percent'].iloc[-1]:.1f}%)")

st.markdown("""
- **High cullet %** can improve energy efficiency and reduce CO₂ emissions.
- **Material yield** drops may indicate process inefficiencies or material losses.
- This module correlates yield with energy/GHG and triggers alerts on underperformance.
""")
