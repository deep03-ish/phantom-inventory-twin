import streamlit as st
import pandas as pd

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
# INVENTORY STATUS TABLE
# -------------------------------
st.subheader("Inventory Status Analysis")
st.dataframe(df, use_container_width=True)

# -------------------------------
# ALERT GENERATION
# -------------------------------
st.subheader("Detected Anomalies")

issues = df[df["Status"] != "Valid"]

if issues.empty:
    st.write("No anomalies detected in the current warehouse state.")
else:
    for _, row in issues.iterrows():
        st.write(
            f"SKU {row['SKU']} in Zone {row['Zone']} classified as {row['Status']} – {row['Recommended_Action']}"
        )

# -------------------------------
# ZONE-LEVEL DIGITAL TWIN VIEW
# -------------------------------
st.subheader("Zone-Level Risk Assessment")

zone_summary = df.groupby("Zone")["Status"].apply(
    lambda x: "At Risk" if any(x != "Valid") else "Stable"
)

for zone, status in zone_summary.items():
    st.write(f"Zone {zone}: {status}")

# -------------------------------
# SIMULATION ENGINE
# -------------------------------
st.subheader("Simulation Module")

if st.button("Simulate Zone C Disruption"):
    impacted = df[df["Zone"] == "C"]
    st.write(f"Number of affected SKUs: {len(impacted)}")
    st.write("Impact: Potential delay in order fulfillment and stock redistribution required.")

# -------------------------------
# FOOTER
# -------------------------------
st.write("---")
st.write("This dashboard represents a digital twin model integrating knowledge representation, rule-based inference, and warehouse monitoring.")