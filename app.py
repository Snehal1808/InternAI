import streamlit as st
import pandas as pd
import ast
import re
from sklearn.preprocessing import LabelEncoder, StandardScaler
import joblib
import numpy as np
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, InputLayer

# ------------------- TRANSLATION SUPPORT -------------------
translations = {
    "en": {
        "title": "🎓 Internship Recommendation System",
        "sidebar_title": "🔎 Candidate Preferences",
        "📍 Preferred Location(s)": "📍 Preferred Location(s)",
        "🛠 Skills": "🛠 Skills",
        "📚 Education": "📚 Education",
        "💰 Minimum Stipend": "💰 Minimum Stipend",
        "📆 Maximum Duration (months)": "📆 Maximum Duration (months)",
        "Show Recommendations": "Show Recommendations",
        "Recommended Internships": "✅ Recommended Internships",
    },
    "hi": {
        "title": "🎓 इंटर्नशिप सिफारिश प्रणाली",
        "sidebar_title": "🔎 उम्मीदवार की प्राथमिकताएँ",
        "📍 Preferred Location(s)": "📍 पसंदीदा स्थान",
        "🛠 Skills": "🛠 कौशल",
        "📚 Education": "📚 शिक्षा",
        "💰 Minimum Stipend": "💰 न्यूनतम वजीफ़ा",
        "📆 Maximum Duration (months)": "📆 अधिकतम अवधि (महीने)",
        "Show Recommendations": "सिफारिशें दिखाएँ",
        "Recommended Internships": "✅ अनुशंसित इंटर्नशिप",
    }
}

# Current language
lang = st.sidebar.selectbox("🌐 Language", ["en", "hi"])
def t(key): return translations[lang].get(key, key)

# ------------------- CLEANING FUNCTIONS -------------------
def parse_skills(skills_str):
    try:
        return ast.literal_eval(skills_str) if pd.notna(skills_str) else []
    except:
        return []

def parse_duration(duration_str):
    if pd.isna(duration_str): return None
    match = re.search(r'(\d+)', str(duration_str))
    return int(match.group(1)) if match else None

def parse_stipend(stipend_str):
    if pd.isna(stipend_str): return 0
    match = re.search(r'₹?(\d+)', str(stipend_str).replace(",", ""))
    return int(match.group(1)) if match else 0

def clean_location(loc_str):
    if pd.isna(loc_str): return []
    return [city.strip() for city in str(loc_str).split(",") if city.strip()]

# ------------------- LOAD DATA -------------------
@st.cache_data
def load_data():
    df = pd.read_csv("internship_data.csv")
    df["Duration"] = df["Duration"].apply(parse_duration)
    df["Stipend"] = df["Stipend"].apply(parse_stipend)
    df["Skills"] = df["Skills"].apply(parse_skills)
    if "Education" not in df.columns:
        df["Education"] = "Graduation"
    return df

data = load_data()

# ------------------- UNIQUE CITIES & SKILLS -------------------
all_cities = []
for locs in data["Location"].dropna():
    all_cities.extend(clean_location(locs))
available_locations = sorted(set(all_cities))

available_skills = sorted({skill for skills in data["Skills"] for skill in (skills if isinstance(skills, list) else [])})

# ------------------- FILTER FUNCTION -------------------
def filter_internships(df, candidate_location, candidate_skills, candidate_edu, min_stipend, max_duration):
    filtered = df.copy()

    # ✅ Location filter (checks each row’s list of cities)
    if candidate_location:
        filtered = filtered[filtered["Location"].apply(
            lambda loc: any(city in clean_location(loc) for city in candidate_location)
        )]

    # ✅ Skills filter
    if candidate_skills:
        filtered = filtered[filtered["Skills"].apply(
            lambda skills: any(skill in skills for skill in candidate_skills)
        )]

    # ✅ Education filter
    if candidate_edu:
        filtered = filtered[filtered["Education"].str.contains(candidate_edu, case=False, na=False)]

    # ✅ Stipend filter
    if min_stipend:
        filtered = filtered[filtered["Stipend"] >= min_stipend]

    # ✅ Duration filter
    if max_duration:
        filtered = filtered[filtered["Duration"].fillna(0) <= max_duration]

    return filtered

# ------------------- UI -------------------
st.title(t("title"))
st.sidebar.header(t("sidebar_title"))

candidate_location = st.sidebar.multiselect(t("📍 Preferred Location(s)"), options=available_locations, default=[])
candidate_skills = st.sidebar.multiselect(t("🛠 Skills"), options=available_skills, default=[])
candidate_edu = st.sidebar.selectbox(t("📚 Education"), options=["Graduation", "Post-Graduation", "PhD"])
min_stipend = st.sidebar.number_input(t("💰 Minimum Stipend"), min_value=0, value=0, step=500)
max_duration = st.sidebar.slider(t("📆 Maximum Duration (months)"), min_value=1, max_value=12, value=6)

if st.sidebar.button(t("Show Recommendations")):
    recommendations = filter_internships(data, candidate_location, candidate_skills, candidate_edu, min_stipend, max_duration)

    st.subheader(t("Recommended Internships"))

    if not recommendations.empty:
        for _, row in recommendations.iterrows():
            st.markdown(f"""
            ### 🏢 {row['Company']}
            - 📍 Location: {row['Location']}
            - 💰 Stipend: ₹{row['Stipend']}
            - 📆 Duration: {row['Duration']} months
            - 📚 Education: {row['Education']}
            - 🛠 **Skills Required:**
            {"".join([f"- {s}\n" for s in row['Skills']]) if row['Skills'] else "None"}
            ---
            """)
    else:
        st.warning("⚠️ No internships found matching your preferences.")
