import streamlit as st
import pandas as pd

# ============================
# Load your CSV results
# ============================
df = pd.read_csv("EV_US_Fit_Scores_Results.csv", encoding='latin1')

FEATURES = [
    "Price_norm", "Range_norm", "Charging_norm", "Maint_norm",
    "Space_norm", "Accel_norm", "Env_norm", "Safety_norm"
]

# ============================
# Define region-specific persona weights
# ============================

US_WEIGHTS = {
    "Value Maximizer": [0.25, 0.15, 0.13, 0.20, 0.05, 0.12, 0.05, 0.05],
    "Family User": [0.10, 0.15, 0.10, 0.10, 0.25, 0.05, 0.05, 0.20],
    "Performance Enthusiast": [0.05, 0.15, 0.20, 0.10, 0.10, 0.30, 0.05, 0.05],
    "Eco Advocate": [0.10, 0.20, 0.10, 0.05, 0.05, 0.10, 0.30, 0.10],
}

EU_WEIGHTS = {
    "Value Maximizer": [0.23, 0.15, 0.15, 0.20, 0.05, 0.05, 0.07, 0.10],
    "Family User": [0.12, 0.16, 0.16, 0.12, 0.05, 0.05, 0.14, 0.20],
    "Performance Enthusiast": [0.05, 0.20, 0.15, 0.05, 0.05, 0.30, 0.10, 0.10],
    "Eco Advocate": [0.10, 0.20, 0.10, 0.10, 0.05, 0.05, 0.30, 0.10],
}

CHINA_WEIGHTS = {
    "Value Maximizer": [0.25, 0.20, 0.15, 0.20, 0.05, 0.05, 0.05, 0.05],
    "Family User": [0.18, 0.13, 0.13, 0.12, 0.17, 0.05, 0.04, 0.18],
    "Performance Enthusiast": [0.05, 0.20, 0.20, 0.05, 0.05, 0.25, 0.10, 0.10],
    "Eco Advocate": [0.10, 0.20, 0.10, 0.05, 0.05, 0.10, 0.30, 0.10],
}

# ============================
# Sidebar controls
# ============================
st.sidebar.title("⚙️ Dashboard Controls")

# Persona selector
persona = st.sidebar.selectbox("Choose Persona", list(US_WEIGHTS.keys()))

# Region selector
regions = df['Region'].unique()
region = st.sidebar.selectbox("Select Region", regions)

# Filter dataframe by region
df_region = df[df['Region'] == region]

# Select region-specific weights
if region == "US":
    weights_dict = US_WEIGHTS
elif region == "EU":
    weights_dict = EU_WEIGHTS
else:
    weights_dict = CHINA_WEIGHTS

weights = weights_dict[persona]
w = pd.Series(weights, index=FEATURES)

# ============================
# Calculate Fit Score
# ============================
df_region["Fit Score"] = df_region[FEATURES].multiply(w, axis=1).sum(axis=1)
df_region["Rank"] = df_region["Fit Score"].rank(method="min", ascending=False).astype(int)

df_sorted = df_region.sort_values("Fit Score", ascending=False)

# ============================
# Display Results
# ============================
st.title("🚗 EV Fit Score Dashboard")
st.subheader(f"Persona: {persona} | Region: {region}")

st.write("### Ranked EV Models")
st.dataframe(df_sorted[["Model", "Region", "Fit Score", "Rank"]].reset_index(drop=True))

st.write("### Fit Score Chart")
st.bar_chart(df_sorted.set_index("Model")["Fit Score"])
