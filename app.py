import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
import re
from tensorflow.keras.models import load_model

# =========================
# Load model + encoders
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model = load_model(os.path.join(BASE_DIR, "internship_model.keras"))
le_location = joblib.load(os.path.join(BASE_DIR, "le_location.pkl"))
le_company = joblib.load(os.path.join(BASE_DIR, "le_company.pkl"))
scaler = joblib.load(os.path.join(BASE_DIR, "scaler.pkl"))

# Load dataset
data_path = os.path.join(BASE_DIR, "internship_data.csv")
data = pd.read_csv(data_path)

# =========================
# Preprocessing
# =========================
def clean_location(loc_str):
    if pd.isna(loc_str):
        return []
    # Split multi-location entries into list of cities
    cities = re.split(r",|/|;", loc_str)
    return [c.strip() for c in cities if c.strip()]

# Extract unique skills
def parse_skills(sk):
    if pd.isna(sk):
        return []
    try:
        return eval(sk) if isinstance(sk, str) else sk
    except:
        return [sk]

data["Skills"] = data["Skills"].apply(parse_skills)
all_skills = sorted({s for sub in data["Skills"] for s in sub if s})

# Unique city list
all_locations = sorted({city for loc in data["Location"].dropna() for city in clean_location(loc)})

# =========================
# Streamlit UI
# =========================
st.title("🎓 InternAI - Internship Recommendation")
st.markdown("Find your **Top 5 Internships** with AI 🚀")

st.sidebar.header("🧑 Candidate Profile")
language = st.sidebar.selectbox("🌐 Select Language", ["English", "Hindi"])
locations = st.sidebar.multiselect("📍 Preferred Location(s)", all_locations)
skills = st.sidebar.multiselect("🛠 Skills", all_skills)
education = st.sidebar.selectbox("🎓 Education", ["High School", "Graduation", "Post-Graduation"])
stipend = st.sidebar.slider("💰 Minimum Stipend (₹/month)", 0, 50000, 0)

# =========================
# Recommendation Logic
# =========================
if st.sidebar.button("🔍 Get AI Recommendations"):

    filtered = data.copy()

    # Location filter
    if locations:
        pattern = "|".join([re.escape(loc) for loc in locations])
        filtered = filtered[filtered["Location"].str.contains(pattern, case=False, na=False)]

    # Skills filter
    if skills:
        filtered = filtered[filtered["Skills"].apply(lambda x: any(skill in x for skill in skills))]

    if filtered.empty:
        st.warning("⚠️ No internships found matching your preferences.")
    else:
        # Encode & predict scores
        filtered["Location_enc"] = le_location.transform(
            [clean_location(l)[0] if clean_location(l) else le_location.classes_[0] for l in filtered["Location"]]
        )
        filtered["Company_enc"] = le_company.transform(filtered["Company Name"].fillna(le_company.classes_[0]))

        X = filtered[["Location_enc", "Stipend", "Duration"]].fillna(0)
        X_scaled = scaler.transform(X)

        scores = model.predict(X_scaled).flatten()
        filtered["Score"] = scores

        top5 = filtered.sort_values(by="Score", ascending=False).head(5)

        st.subheader("✨ Top 5 Recommended Internships")
        for idx, row in top5.iterrows():
            with st.container():
                st.markdown(f"### {row['Role']} at **{row['Company Name']}**")
                st.markdown(f"📍 Location: {row['Location']}")
                st.markdown(f"💰 Stipend: ₹{row['Stipend']} /month")
                st.markdown(f"⏳ Duration: {row['Duration']} months")
                st.markdown(f"🛠 Skills Required: {', '.join(row['Skills'])}")
                if pd.notna(row.get("Website Link")) and str(row["Website Link"]).startswith("http"):
                    st.markdown(f"[👉 Apply Here]({row['Website Link']})", unsafe_allow_html=True)
                st.divider()
