import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------------
# PAGE CONFIGURATION
# -------------------------------
st.set_page_config(page_title="Phantom Inventory Twin", layout="wide")

st.title("Phantom Inventory Twin – Warehouse Monitoring System")
st.write("A rule-based digital twin system for detecting phantom inventory and warehouse anomalies in real-time.")

# -------------------------------
# SIMULATED WAREHOUSE DATA
# -------------------------------
data = [
    {"SKU": "FAB-A101", "Zone": "A", "System_Stock": 120, "Physical_Stock": 120, "Weight": 5.2},
    {"SKU": "FAB-B205", "Zone": "B", "System_Stock": 85, "Physical_Stock": 0, "Weight": 0.0},
    {"SKU": "FAB-C309", "Zone": "C", "System_Stock": 200, "Physical_Stock": 185, "Weight": 4.8},
    {"SKU": "FAB-A415", "Zone": "A", "System_Stock": 60, "Physical_Stock": 60, "Weight": 1.1},
    {"SKU": "FAB-B512", "Zone": "B", "System_Stock": 140, "Physical_Stock": 140, "Weight": 5.5},
]

df = pd.DataFrame(data)

# -------------------------------
# KNOWLEDGE REPRESENTATION RULES
# -------------------------------
def classify_inventory(row):
    if row["Physical_Stock"] == 0:
        return "Phantom Inventory"
    elif row["Physical_Stock"] != row["System_Stock"]:
        return "Quantity Mismatch"
    elif row["Weight"] < 2:
        return "Damaged"
    else:
        return "Valid"

df["Status"] = df.apply(classify_inventory, axis=1)

# -------------------------------
# INFERENCE ENGINE (ACTIONS)
# -------------------------------
def infer_action(status):
    if status == "Phantom Inventory":
        return "Investigate missing item location"
    elif status == "Quantity Mismatch":
        return "Perform physical recount"
    elif status == "Damaged":
        return "Send for inspection"
    else:
        return "No action required"

df["Recommended_Action"] = df["Status"].apply(infer_action)

# -------------------------------
# KPI SECTION
# -------------------------------
st.subheader("System Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total SKUs", len(df))
col2.metric("Phantom Cases", df[df["Status"] == "Phantom Inventory"].shape[0])
col3.metric("Mismatch Cases", df[df["Status"] == "Quantity Mismatch"].shape[0])
col4.metric("Damaged Cases", df[df["Status"] == "Damaged"].shape[0])

# -------------------------------
# FILTER SECTION
# -------------------------------
st.subheader("Filter by Warehouse Zone")

selected_zone = st.selectbox("Select Zone", ["All"] + list(df["Zone"].unique()))

if selected_zone != "All":
    filtered_df = df[df["Zone"] == selected_zone]
else:
    filtered_df = df

# -------------------------------
# INVENTORY TABLE
# -------------------------------
st.subheader("Inventory Status Analysis")
st.dataframe(filtered_df, use_container_width=True)

# -------------------------------
# VISUAL ANALYTICS
# -------------------------------
st.subheader("Visual Analysis")

col1, col2 = st.columns(2)

# BAR CHART
with col1:
    st.markdown("### Stock Comparison (System vs Physical)")
    st.bar_chart(filtered_df.set_index("SKU")[["System_Stock", "Physical_Stock"]])

# PIE CHART
with col2:
    st.markdown("### Status Distribution")
    status_counts = filtered_df["Status"].value_counts()

    fig, ax = plt.subplots()
    ax.pie(status_counts, labels=status_counts.index, autopct="%1.1f%%")
    ax.set_title("Inventory Status Breakdown")
    st.pyplot(fig)

# -------------------------------
# ALERT GENERATION
# -------------------------------
st.subheader("Detected Anomalies")

issues = filtered_df[filtered_df["Status"] != "Valid"]

if issues.empty:
    st.success("No anomalies detected in the selected warehouse zone.")
else:
    for _, row in issues.iterrows():
        st.warning(
            f"{row['SKU']} (Zone {row['Zone']}) → {row['Status']} | Action: {row['Recommended_Action']}"
        )

# -------------------------------
# ZONE-LEVEL DIGITAL TWIN VIEW
# -------------------------------
st.subheader("Zone-Level Risk Assessment")

zone_summary = df.groupby("Zone")["Status"].apply(
    lambda x: "At Risk" if any(x != "Valid") else "Stable"
)

for zone, status in zone_summary.items():
    if status == "At Risk":
        st.error(f"Zone {zone}: {status}")
    else:
        st.success(f"Zone {zone}: {status}")

# -------------------------------
# SIMULATION MODULE
# -------------------------------
st.subheader("Simulation Module")

if st.button("Simulate Zone C Disruption"):
    impacted = df[df["Zone"] == "C"]
    st.error(f"{len(impacted)} SKUs affected in Zone C")
    st.info("Impact: Delay in fulfillment and stock imbalance expected.")

# -------------------------------
# FOOTER
# -------------------------------
st.write("---")
st.caption("Digital Twin System using Knowledge Representation & Rule-Based Inference for Warehouse Monitoring.")