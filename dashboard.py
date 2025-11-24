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

# User-friendly labels for sliders
FEATURE_LABELS = {
    "Price_norm": "Price",
    "Range_norm": "Range",
    "Charging_norm": "Charging Speed",
    "Maint_norm": "Maintenance Cost",
    "Space_norm": "Cargo Space",
    "Accel_norm": "Acceleration",
    "Env_norm": "Environmental Impact",
    "Safety_norm": "Safety Rating"
}

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
regions = df['Region'].unique()
region = st.sidebar.selectbox("Select Region", regions)

persona_options = ["Customize My Importance", "Value Maximizer", "Family User", "Performance Enthusiast", "Eco Advocate"]
persona = st.sidebar.selectbox("Choose Persona", persona_options)
df_region = df[df['Region'] == region]

# ============================
# Personal importance sliders
# ============================
default_slider_value = 5
slider_values = []

if persona == "Customize My Importance":
    st.sidebar.subheader("Set How Important Each Feature Is to You")
    
    # Create session state to store slider values
    for feature in FEATURES:
        if f"slider_{feature}" not in st.session_state:
            st.session_state[f"slider_{feature}"] = default_slider_value

    # Reset button
    if st.sidebar.button("Reset Sliders"):
        for feature in FEATURES:
            st.session_state[f"slider_{feature}"] = default_slider_value

    # Display sliders
    for feature in FEATURES:
        val = st.sidebar.slider(
            FEATURE_LABELS[feature],
            0, 10,
            value=st.session_state[f"slider_{feature}"],
            key=f"slider_{feature}"
        )
        slider_values.append(val)

    # Optional: normalize to sum 1
    slider_values = [v / sum(slider_values) for v in slider_values]
    importance_values = slider_values

else:
    # use region-specific defaults
    if region == "US":
        importance_dict = US_WEIGHTS
    elif region == "EU":
        importance_dict = EU_WEIGHTS
    else:
        importance_dict = CHINA_WEIGHTS
    importance_values = importance_dict[persona]



w = pd.Series(importance_values, index=FEATURES)

# ============================
# Calculate Fit Score
# ============================
df_region["Fit Score"] = df_region[FEATURES].multiply(w, axis=1).sum(axis=1)
df_region["Rank"] = df_region["Fit Score"].rank(method="min", ascending=False).astype(int)
df_sorted = df_region.sort_values("Fit Score", ascending=False)

# ============================
# Display
# ============================
st.title("🚗 EV Fit Score Dashboard")
if persona == "Customize My Importance":
    st.subheader(f"Personalized Importance | Region: {region}")
else:
    st.subheader(f"Persona: {persona} | Region: {region}")

st.write("### Ranked EV Models")
st.dataframe(df_sorted[["Model", "Region", "Fit Score", "Rank"]].reset_index(drop=True))
st.write("### Fit Score Chart")
st.bar_chart(df_sorted.set_index("Model")["Fit Score"])

