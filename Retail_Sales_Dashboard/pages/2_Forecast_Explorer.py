import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("🔮 Forecast Explorer")

forecast_data = {
    "Overall Sales": [51037.70, 30091.78, 61376.89],
    "Furniture": [9716.00, 6214.69, 16723.81],
    "Technology": [20370.97, 24370.32, 30328.62],
    "Office Supplies": [25796.03, 25957.26, 29761.83],
    "West": [11175.51, 15125.34, 21355.62],
    "East": [25088.46, 25353.45, 27580.83]
}

months = ["Jan 2019", "Feb 2019", "Mar 2019"]

choice = st.selectbox(
    "Select Category / Region",
    list(forecast_data.keys())
)

horizon = st.slider(
    "Forecast Horizon (Months)",
    1,
    3,
    3
)

forecast = forecast_data[choice][:horizon]
forecast_months = months[:horizon]

fig, ax = plt.subplots(figsize=(8,4))

ax.plot(
    forecast_months,
    forecast,
    marker="o",
    linewidth=2
)

ax.set_title(f"{choice} Sales Forecast")
ax.set_xlabel("Month")
ax.set_ylabel("Forecasted Sales")
ax.grid(True)

st.pyplot(fig)

forecast_df = pd.DataFrame({
    "Month": forecast_months,
    "Forecasted Sales": forecast
})

st.subheader("Forecast Values")
st.dataframe(forecast_df, use_container_width=True)

st.subheader("Model Performance")

col1, col2, col3 = st.columns(3)

col1.metric("MAE", "13,915.32")
col2.metric("RMSE", "18,893.85")
col3.metric("MAPE", "13.29%")
