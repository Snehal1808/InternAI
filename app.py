import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
from tensorflow.keras.models import load_model

# =========================
# Load model + encoders
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model = load_model(os.path.join(BASE_DIR, "internship_model.keras"))
le_location = joblib.load(os.path.join(BASE_DIR, "le_location.pkl"))
le_company = joblib.load(os.path.join(BASE_DIR, "le_company.pkl"))
scaler = joblib.load(os.path.join(BASE_DIR, "scaler.pkl"))

# =========================
# Streamlit UI
# =========================
st.title("🎓 InternAI - Internship Recommendation")

st.sidebar.header("🧑 Candidate Profile")
language = st.sidebar.selectbox("Select Language", ["English", "Hindi"])
locations = st.sidebar.multiselect("Preferred Location(s)", le_location.classes_)
skills = st.sidebar.text_area("Skills (comma separated)", "Python, Data Analysis")
education = st.sidebar.selectbox("Education", ["High School", "Graduation", "Post-Graduation"])
stipend = st.sidebar.slider("Minimum Stipend (₹/month)", 0, 50000, 0)

if st.sidebar.button("🔍 Get AI Recommendations"):
    # Convert inputs
    skills_list = [s.strip() for s in skills.split(",") if s.strip()]

    # Handle location encoding safely
    if not locations:
        st.error("Please select at least one location.")
    else:
        for loc in locations:
            if loc not in le_location.classes_:
                st.error(f"⚠️ Unknown location: {loc}. Please select a valid one.")
                st.stop()

        loc_encoded = le_location.transform([locations[0]])[0]  # taking first for demo
        comp_encoded = le_company.transform([le_company.classes_[0]])[0]  # dummy (no company input)

        # Feature vector
        features = np.array([[loc_encoded, stipend, 2]])  # fixed duration=2 months for demo
        features_scaled = scaler.transform(features)

        # Prediction score
        score = model.predict(features_scaled)[0][0]

        st.subheader("✨ Recommended Internship")
        st.write(f"**Score:** {score:.2f}")
        st.write(f"**Location:** {locations[0]}")
        st.write(f"**Skills:** {', '.join(skills_list)}")
        st.write(f"**Education:** {education}")
        st.success("🎯 This internship is a good match for you!")
