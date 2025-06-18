# pages/3_Forecasting.py
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

@st.cache_data
def load_data():
    date_rng = pd.date_range(start='2025-01-01', periods=1000, freq='H')
    df = pd.DataFrame({
        'timestamp': date_rng,
        'energy_consumption': 1200 + 100 * np.random.randn(1000),
        'raw_material_input': 800 + 50 * np.random.randn(1000),
        'cullet_percent': 30 + 5 * np.random.randn(1000),
        'water_usage': 300 + 20 * np.random.randn(1000),
        'air_consumption': 500 + 30 * np.random.randn(1000),
        'waste_generated': 20 + 5 * np.random.randn(1000),
    })
    return df

def create_features(df, window=6):
    for col in ['energy_consumption', 'raw_material_input', 'cullet_percent', 
                'water_usage', 'air_consumption', 'waste_generated']:
        for i in range(1, window + 1):
            df[f'{col}_lag_{i}'] = df[col].shift(i)
    return df.dropna()

# Load and process data
data = load_data()
data = create_features(data)

# Define feature columns
feature_cols = [col for col in data.columns if 'lag' in col]
X = data[feature_cols]
y = data['energy_consumption']

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

# Normalize
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train model
model = Ridge()
model.fit(X_train_scaled, y_train)
y_pred = model.predict(X_test_scaled)
mse = mean_squared_error(y_test, y_pred)

# Forecast next hour
latest = data.iloc[-1:]
next_input = latest[feature_cols]
next_scaled = scaler.transform(next_input)
forecast = model.predict(next_scaled)[0]

# Streamlit UI
st.title("📊 Multivariate Forecasting")
st.metric("Next Hour Energy Forecast (kWh)", round(forecast, 2))
st.write(f"Model MSE on test set: {mse:.2f}")

st.subheader("📉 Forecast vs Actual")
fig, ax = plt.subplots()
ax.plot(y_test.values, label='Actual')
ax.plot(y_pred, label='Predicted')
ax.set_title('Forecast vs Actual (Energy)')
ax.legend()
st.pyplot(fig)

st.subheader("📌 Feature Contributions")
st.write("This model incorporates:")
st.markdown("""
- Raw material input  
- Cullet %  
- Water usage  
- Compressed air consumption  
- Waste generation  
- Lagged values of each for past 6 hours
""")
