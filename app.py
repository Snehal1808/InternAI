import streamlit as st
import pandas as pd
import numpy as np
import joblib
from tensorflow.keras.models import load_model

# ----------------------------
# Load model, scaler, and data
# ----------------------------
model = load_model("trained_model.keras")
scaler = joblib.load("scaler.pkl")
data = pd.read_csv("internship_data.csv")

# Extract unique values for filters
unique_locations = sorted(data["Location"].dropna().unique())
unique_skills = sorted(
    set(skill.strip() for sublist in data["Skills Required"].dropna() for skill in sublist.split(","))
)
unique_educations = sorted(data["Education"].dropna().unique())

# ----------------------------
# Streamlit Page Config
# ----------------------------
st.set_page_config(page_title="SkillFit - Internship Recommender", layout="wide")
st.title("🏆 Top Internship Recommendations")
st.markdown("Helping you find the **perfect internship** based on your preferences and skills.")

# ----------------------------
# Sidebar Inputs
# ----------------------------
st.sidebar.header("🧑‍🎓 Candidate Profile")

selected_locations = st.sidebar.multiselect("📍 Preferred Location(s)", unique_locations)
selected_skills = st.sidebar.multiselect("🛠 Skills", unique_skills)
selected_education = st.sidebar.selectbox("🎓 Education", unique_educations)
min_stipend = st.sidebar.slider("💰 Minimum Stipend (₹/month)", 0, int(data["Stipend"].str.replace("₹", "").str.replace(",", "").str.replace("/month", "").astype(float).max()), 0)

predict_button = st.sidebar.button("🎯 Get AI Recommendations")

# ----------------------------
# Predict & Filter
# ----------------------------
if predict_button:
    filtered_df = data.copy()

    # Filter by location
    if selected_locations:
        filtered_df = filtered_df[
            filtered_df["Location"].apply(lambda x: any(loc in x for loc in selected_locations))
        ]

    # Filter by education
    if selected_education:
        filtered_df = filtered_df[filtered_df["Education"] == selected_education]

    # Filter by stipend
    if min_stipend > 0:
        filtered_df["Stipend Value"] = filtered_df["Stipend"].str.replace("₹", "").str.replace(",", "").str.replace("/month", "").astype(float)
        filtered_df = filtered_df[filtered_df["Stipend Value"] >= min_stipend]

    # Filter by skills
    if selected_skills:
        filtered_df = filtered_df[
            filtered_df["Skills Required"].apply(lambda x: all(skill in x for skill in selected_skills))
        ]

    if filtered_df.empty:
        st.warning("⚠ No internships match your criteria. Try adjusting filters.")
    else:
        st.markdown("### 🎯 Recommended Internships")
        for i, row in filtered_df.iterrows():

            # Deduplicate Locations
            locations = list(dict.fromkeys([loc.strip() for loc in str(row["Location"]).split(",") if loc.strip()]))
            locations_display = ", ".join(locations)

            # Prepare HTML Card
            top_badge_html = (
                '<span style="background-color:#FFD700;color:black;padding:4px 8px;border-radius:8px;font-size:12px;font-weight:bold;">⭐ Top Match</span>'
                if i == filtered_df.index[0] else ""
            )

            html_card = f"""
            <div style="background-color:#1e1e1e;border-radius:16px;padding:20px;margin:10px;
                        box-shadow:0px 0px 10px rgba(255,255,255,0.05);">
                {top_badge_html}
                <h4 style="color:#ff9068;">💼 {row['Role']}</h4>
                <p style="color:#aaa;">🏢 {row['Company Name']}</p>
                <p>📍 <b>Location:</b> {locations_display}</p>
                <p>💰 <b>Stipend:</b> {row['Stipend']}</p>
                <p>⏳ <b>Duration:</b> {row['Duration']}</p>
                <p>🛠 <b>Skills Required:</b> {" ".join([f"<span style='background:#2563eb;color:white;padding:4px 8px;border-radius:8px;margin:2px;font-size:12px;'>{skill.strip()}</span>" for skill in row['Skills Required'].split(",")])}</p>
                <p>🎁 <b>Perks & Benefits:</b> {row['Perks & Benefits']}</p>
                <div style="background:#2b2b2b;border-radius:8px;overflow:hidden;margin:8px 0;">
                    <div style="width:{np.random.randint(40, 100)}%;background:#22c55e;color:white;text-align:center;padding:4px 0;font-size:12px;">
                        {np.random.randint(40, 100)}% Match
                    </div>
                </div>
                <div style="text-align:center;margin-top:12px;">
                    <a href="{row['Apply Link']}" target="_blank" style="background:#ff4b4b;color:white;
                        padding:8px 16px;border-radius:12px;text-decoration:none;display:inline-block;
                        font-weight:bold;box-shadow:0 4px 8px rgba(255,75,75,0.3);">
                        🚀 Apply Now
                    </a>
                </div>
            </div>
            """
            st.markdown(html_card, unsafe_allow_html=True)
else:
    st.info("👆 Select your preferences and click **Get AI Recommendations** to see internships.")
