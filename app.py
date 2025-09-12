import streamlit as st
import pandas as pd
import joblib
import numpy as np

# Load trained model and dataset
@st.cache_resource
def load_model():
    return joblib.load("model.pkl")

@st.cache_data
def load_data():
    return pd.read_csv("internships.csv")

model = load_model()
df = load_data()

# Extract unique cities from dataset
def get_unique_cities(df):
    all_cities = []
    for loc in df["Location"].dropna():
        parts = [city.strip() for city in str(loc).split(",")]
        all_cities.extend(parts)
    unique_cities = sorted(set(all_cities))
    return unique_cities

# Extract unique skills
def get_unique_skills(df):
    all_skills = []
    for skills in df["Skills"].dropna():
        parts = [s.strip() for s in str(skills).split(",")]
        all_skills.extend(parts)
    unique_skills = sorted(set(all_skills))
    return unique_skills


# ---------------- Sidebar UI ---------------- #
st.sidebar.header("🦁 Candidate Profile")

# Language
language = st.sidebar.selectbox("🌐 Select Language", ["English", "Hindi"])

# Locations
st.sidebar.subheader("📍 Preferred Location(s)")
unique_cities = get_unique_cities(df)
selected_locations = st.sidebar.multiselect("Choose options", options=unique_cities)

# Skills (markdown menu style)
st.sidebar.subheader("🛠 Skills")
unique_skills = get_unique_skills(df)
selected_skills = st.sidebar.multiselect("Choose options", options=unique_skills)
if selected_skills:
    st.sidebar.markdown("**Selected Skills:**")
    for skill in selected_skills:
        st.sidebar.markdown(f"- {skill}")

# Education
education = st.sidebar.selectbox("🎓 Education", df["Education"].dropna().unique())

# Minimum stipend
min_stipend = st.sidebar.slider("💰 Minimum Stipend (₹/month)", 0, 50000, 5000, step=1000)

# Button
recommend_btn = st.sidebar.button("🚀 Get AI Recommendations")


# ---------------- Main UI ---------------- #
st.title("🚀 InternAI")
st.subheader("Find your perfect internship match using AI")

if recommend_btn:
    filtered = df.copy()

    # Apply filters
    if selected_locations:
        filtered = filtered[
            filtered["Location"].apply(
                lambda x: any(loc in str(x) for loc in selected_locations)
            )
        ]

    if selected_skills:
        filtered = filtered[
            filtered["Skills"].apply(
                lambda x: any(skill in str(x) for skill in selected_skills)
            )
        ]

    if education:
        filtered = filtered[filtered["Education"] == education]

    # Fix stipend issue (convert safely to float)
    filtered["Stipend"] = pd.to_numeric(filtered["Stipend"], errors="coerce")
    filtered = filtered[filtered["Stipend"] >= float(min_stipend)]

    if not filtered.empty:
        st.success(f"✅ Found {len(filtered)} matching internships!")
        for _, row in filtered.iterrows():
            with st.container():
                st.markdown(f"### 💼 {row['Title']}")
                st.markdown(f"**📍 Location:** {row['Location']}")
                st.markdown(f"**🛠 Skills:** {row['Skills']}")
                st.markdown(f"**🎓 Education:** {row['Education']}")
                st.markdown(f"**💰 Stipend:** ₹{row['Stipend']}/month")
                st.markdown(f"**⏳ Duration:** {row['Duration']}")
                st.markdown("---")
    else:
        st.warning("⚠️ No internships found. Try relaxing your filters.")
