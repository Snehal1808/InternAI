import streamlit as st
import pandas as pd
import numpy as np
import joblib
import tensorflow as tf
import re

# -------------------------
# Load trained components
# -------------------------
model = tf.keras.models.load_model("internship_model.keras")
le_location = joblib.load("le_location.pkl")
le_company = joblib.load("le_company.pkl")
scaler = joblib.load("scaler.pkl")

# -------------------------
# Utility Functions
# -------------------------
def clean_location(loc_str):
    if pd.isna(loc_str):
        return ""
    return loc_str.strip("()").replace("'", "")

def safe_encode(encoder, value, default="Unknown"):
    """Safely encode a label with fallback."""
    if value in encoder.classes_:
        return encoder.transform([value])[0]
    else:
        # Handle unseen label by mapping to "Unknown"
        if default not in encoder.classes_:
            encoder.classes_ = np.append(encoder.classes_, default)
        return encoder.transform([default])[0]

def parse_skills(sk):
    if pd.isna(sk):
        return []
    try:
        return eval(sk)
    except:
        return [sk]

def filter_internships(df, profile):
    df_filtered = df.copy()

    # Location filter
    if profile["location"]:
        pattern = "|".join([re.escape(loc) for loc in profile["location"]])
        df_filtered = df_filtered[df_filtered["Location"].str.contains(pattern, case=False, na=False)]

    # Skills filter
    def skills_match(row_skills, candidate_skills):
        if not candidate_skills:
            return True
        row_skills_lower = [s.lower() for s in row_skills]
        return any(skill.lower() in row_skills_lower for skill in candidate_skills)

    df_filtered["SkillsMatch"] = df_filtered["Skills"].apply(
        lambda x: skills_match(x, profile["skills"])
    )
    return df_filtered[df_filtered["SkillsMatch"]]

# -------------------------
# Load Data
# -------------------------
data = pd.read_csv("internship_data.csv")
data["Location"] = data["Location"].apply(clean_location)
data["Skills"] = data["Skills"].apply(parse_skills)

# Extract unique cities & skills for dropdowns
all_cities = sorted(set(sum([loc.split(",") for loc in data["Location"].tolist()], [])))
all_cities = [city.strip() for city in all_cities if city.strip() != ""]
all_skills = sorted(set(sum(data["Skills"].tolist(), [])))

# -------------------------
# Streamlit UI
# -------------------------
st.set_page_config(page_title="InternAI - Internship Recommendation", layout="wide")

st.sidebar.title("🦁 Candidate Profile")

language = st.sidebar.selectbox("🌐 Select Language", ["English", "Hindi"])
preferred_location = st.sidebar.multiselect("📍 Preferred Location(s)", options=all_cities)
skills = st.sidebar.multiselect("🛠 Skills", options=all_skills, help="Select the skills you know")
education = st.sidebar.selectbox("🎓 Education", ["High School", "Graduation", "Post-Graduation"])
min_stipend = st.sidebar.slider("💰 Minimum Stipend (₹/month)", 0, 50000, 5000, step=1000)

# -------------------------
# Recommendation Logic
# -------------------------
if st.sidebar.button("🚀 Get AI Recommendations"):
    candidate_profile = {
        "education": education,
        "skills": skills,
        "location": preferred_location
    }

    filtered = filter_internships(data, candidate_profile)
    filtered = filtered[filtered["Stipend"] >= min_stipend]

    if filtered.empty:
        st.warning("⚠️ No internships match your criteria. Try adjusting filters.")
    else:
        # Encode safely
        filtered["Location_enc"] = [safe_encode(le_location, l) for l in filtered["Location"]]
        filtered["Company_enc"] = [safe_encode(le_company, c) for c in filtered["Company Name"]]

        # Prepare features
        X = filtered[["Location_enc", "Stipend", "Duration"]]
        X = scaler.transform(X)

        # Predict
        scores = model.predict(X).flatten()
        filtered["Score"] = scores

        # Top 5
        top_internships = filtered.sort_values(by="Score", ascending=False).head(5)

        st.title("🎓 InternAI - Internship Recommendation")
        st.markdown("### Find your **Top 5 Internships** with AI 🚀")

        for idx, row in top_internships.iterrows():
            st.markdown(f"""
            ---
            **💼 Internship:** {row['Role']} at **{row['Company Name']}**  
            **📍 Location:** {row['Location']}  
            **💰 Stipend:** ₹{row['Stipend']} / month  
            **⏳ Duration:** {row['Duration']} months  
            **🛠 Skills Required:** {", ".join(row['Skills']) if row['Skills'] else "Not specified"}  
            **🔗 Apply Here:** [{row['Website Link']}]({row['Website Link']})  
            """)
