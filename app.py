import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load Dataset

df = pd.read_csv("Superstore.csv")

# Convert Order Date
df["Order Date"] = pd.to_datetime(
    df["Order Date"],
    format="mixed",
    dayfirst=True
)

# Dashboard Title

st.title("📊 Retail Sales Dashboard")


# Sidebar Filters

st.sidebar.header("Filters")

selected_region = st.sidebar.selectbox(
    "Select Region",
    ["All"] + sorted(df["Region"].unique())
)

selected_category = st.sidebar.selectbox(
    "Select Category",
    ["All"] + sorted(df["Category"].unique())
)


# Apply Filters

filtered_df = df.copy()

if selected_region != "All":
    filtered_df = filtered_df[
        filtered_df["Region"] == selected_region
    ]

if selected_category != "All":
    filtered_df = filtered_df[
        filtered_df["Category"] == selected_category
    ]


# KPI Cards

total_sales = filtered_df["Sales"].sum()
total_orders = len(filtered_df)
average_sales = filtered_df["Sales"].mean()

col1, col2, col3 = st.columns(3)

col1.metric(
    "💰 Total Sales",
    f"${total_sales:,.2f}"
)

col2.metric(
    "📦 Total Orders",
    f"{total_orders:,}"
)

col3.metric(
    "📈 Average Sale",
    f"${average_sales:.2f}"
)


# Dataset

st.subheader("Dataset Preview")

st.dataframe(filtered_df.head(10))


# Total Sales by Year

st.subheader("📊 Total Sales by Year")

yearly_sales = (
    filtered_df.groupby(filtered_df["Order Date"].dt.year)["Sales"]
    .sum()
)

fig, ax = plt.subplots(figsize=(8,5))

yearly_sales.plot(kind="bar", ax=ax)

ax.set_title("Total Sales by Year")
ax.set_xlabel("Year")
ax.set_ylabel("Sales")

st.pyplot(fig)


# Monthly Sales Trend

st.subheader("📈 Monthly Sales Trend")

monthly_sales = (
    filtered_df.groupby(
        pd.Grouper(
            key="Order Date",
            freq="ME"
        )
    )["Sales"]
    .sum()
    .reset_index()
)

fig, ax = plt.subplots(figsize=(12,5))

ax.plot(
    monthly_sales["Order Date"],
    monthly_sales["Sales"],
    marker="o"
)

ax.set_title("Monthly Sales Trend")
ax.set_xlabel("Date")
ax.set_ylabel("Sales")

plt.xticks(rotation=45)

st.pyplot(fig)
