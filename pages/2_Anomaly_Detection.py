# pages/2_Anomaly_Detection.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

@st.cache_data
def load_data():
    date_rng = pd.date_range(start='2025-01-01', periods=1000, freq='H')
    return pd.DataFrame({
        'timestamp': date_rng,
        'furnace_temp': pd.Series(1450 + 30 * np.random.randn(1000)),
        'pull_rate': pd.Series(25 + 5 * np.random.randn(1000)),
        'energy_consumption': pd.Series(1200 + 100 * np.random.randn(1000)),
    })

data = load_data()

st.title("🔍 Anomaly Detection")
feature = st.selectbox("Select Feature", ['furnace_temp', 'energy_consumption', 'pull_rate'])
scaler = StandardScaler()
X_scaled = scaler.fit_transform(data[[feature]])
model = IsolationForest(contamination=0.05)
data['anomaly'] = model.fit_predict(X_scaled)
data['anomaly'] = data['anomaly'].map({1: 'Normal', -1: 'Anomaly'})
fig = px.scatter(data, x='timestamp', y=feature, color='anomaly', title=f"Anomalies in {feature}",
                 color_discrete_map={'Normal': 'blue', 'Anomaly': 'red'})
st.plotly_chart(fig)
