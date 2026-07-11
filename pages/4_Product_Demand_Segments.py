import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("📦 Product Demand Segments")

cluster_data = pd.DataFrame({

    "Sub-Category": [
        "Accessories","Binders","Chairs","Storage","Phones","Tables",
        "Copiers","Art","Envelopes","Bookcases","Fasteners",
        "Furnishings","Paper","Labels","Supplies","Appliances","Machines"
    ],

    "Cluster":[
        0,0,0,0,0,0,
        1,
        2,2,2,2,2,2,2,2,2,
        3
    ],

    "PC1":[
        0.200367,0.484161,1.479554,0.254384,1.274893,0.663161,
        4.046026,
        -1.676784,-1.920711,-0.176589,-1.960973,-0.798984,
        -1.054223,-1.820825,-0.908790,-0.264248,
        2.179582
    ],

    "PC2":[
        0.116729,-0.805597,-1.711393,-0.905577,-1.682174,-0.700053,
        2.979941,
        0.535820,0.234844,0.003166,0.583155,0.421706,
        0.424876,0.550340,0.067744,0.707660,
        -0.821189
    ]
})

fig, ax = plt.subplots(figsize=(10,6))

colors = {
    0: "blue",
    1: "red",
    2: "green",
    3: "orange"
}

for cluster in sorted(cluster_data["Cluster"].unique()):

    data = cluster_data[cluster_data["Cluster"] == cluster]

    ax.scatter(
        data["PC1"],
        data["PC2"],
        s=120,
        color=colors[cluster],
        label=f"Cluster {cluster}"
    )

    for i, row in data.iterrows():

        ax.text(
            row["PC1"],
            row["PC2"],
            row["Sub-Category"],
            fontsize=8
        )

ax.set_title("K-Means Product Demand Segments")

ax.set_xlabel("Principal Component 1")

ax.set_ylabel("Principal Component 2")

ax.legend()

ax.grid(True)

st.pyplot(fig)

cluster_names = {
    0: "High Volume, Stable Demand",
    1: "Premium High Value",
    2: "Low Volume Products",
    3: "High Volatility Products"
}

cluster_data["Demand Segment"] = cluster_data["Cluster"].map(cluster_names)

st.subheader("Product Demand Segments")

st.dataframe(
    cluster_data[
        ["Sub-Category","Demand Segment"]
    ],
    use_container_width=True
)

st.subheader("Recommended Stocking Strategy")

st.markdown("""
### High Volume, Stable Demand
- Maintain high inventory levels.
- Replenish stock frequently.
- Prioritize supplier reliability.

### Premium High Value
- Keep moderate inventory.
- Monitor demand carefully.
- Avoid overstocking expensive products.

### Low Volume Products
- Maintain limited stock.
- Reorder only when necessary.
- Focus on reducing storage costs.

### High Volatility Products
- Monitor demand trends closely.
- Use demand forecasting frequently.
- Keep safety stock for unexpected demand spikes.
""")
