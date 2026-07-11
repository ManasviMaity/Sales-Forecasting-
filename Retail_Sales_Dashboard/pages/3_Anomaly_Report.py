import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest

st.title("🚨 Sales Anomaly Report")

df = pd.read_csv("superstore.csv")

df["Order Date"] = pd.to_datetime(
    df["Order Date"],
    format="mixed",
    dayfirst=True
)

weekly_sales = (
    df.groupby(pd.Grouper(key="Order Date", freq="W"))["Sales"]
    .sum()
    .reset_index()
)

model = IsolationForest(
    contamination=0.05,
    random_state=42
)

weekly_sales["Anomaly"] = model.fit_predict(
    weekly_sales[["Sales"]]
)

anomalies = weekly_sales[
    weekly_sales["Anomaly"] == -1
]

fig, ax = plt.subplots(figsize=(12,5))

ax.plot(
    weekly_sales["Order Date"],
    weekly_sales["Sales"],
    label="Weekly Sales"
)

ax.scatter(
    anomalies["Order Date"],
    anomalies["Sales"],
    color="red",
    s=80,
    label="Anomaly"
)

ax.set_title("Weekly Sales with Detected Anomalies")
ax.set_xlabel("Date")
ax.set_ylabel("Sales")
ax.legend()
ax.grid(True)

st.pyplot(fig)

st.subheader("Detected Anomalies")

st.dataframe(
    anomalies[["Order Date", "Sales"]],
    use_container_width=True
)

st.subheader("Possible Business Explanation")

st.markdown("""
- High sales spikes may correspond to festive or holiday sales.
- Very low sales weeks may indicate seasonal slowdowns.
- Promotional campaigns can create sudden increases in demand.
- Inventory shortages may cause unusually low sales.
""")


weekly_sales["Rolling Mean"] = weekly_sales["Sales"].rolling(window=8).mean()

weekly_sales["Rolling Std"] = weekly_sales["Sales"].rolling(window=8).std()

weekly_sales["Z_Score"] = (
    (weekly_sales["Sales"] - weekly_sales["Rolling Mean"])
    / weekly_sales["Rolling Std"]
)

weekly_sales["Z_Anomaly"] = abs(weekly_sales["Z_Score"]) > 2

z_anomalies = weekly_sales[weekly_sales["Z_Anomaly"]]

st.subheader("Z-Score Based Anomaly Detection")

fig, ax = plt.subplots(figsize=(12,5))

ax.plot(
    weekly_sales["Order Date"],
    weekly_sales["Sales"],
    label="Weekly Sales"
)

ax.scatter(
    z_anomalies["Order Date"],
    z_anomalies["Sales"],
    color="orange",
    s=80,
    label="Z-Score Anomaly"
)

ax.set_title("Weekly Sales with Z-Score Anomalies")
ax.set_xlabel("Date")
ax.set_ylabel("Sales")
ax.legend()
ax.grid(True)

st.pyplot(fig)

st.subheader("Z-Score Anomaly Table")

if len(z_anomalies) > 0:
    st.dataframe(
        z_anomalies[["Order Date", "Sales", "Z_Score"]],
        use_container_width=True
    )
else:
    st.info("No anomalies were detected using the Z-Score method.")

st.subheader("Comparison")

st.markdown("""
### Isolation Forest
- Machine Learning based method.
- Learns unusual sales patterns automatically.
- Detects both unusually high and unusually low sales.

### Z-Score
- Statistical method.
- Flags observations more than **2 standard deviations** from the rolling mean.
- Simpler and easier to interpret.

### Observation
Isolation Forest generally detects more anomalies because it considers the overall data distribution. Z-Score is more conservative and may detect fewer anomalies, especially when sales variability is high.
""")
