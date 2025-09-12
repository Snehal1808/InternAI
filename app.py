import streamlit as st
import pandas as pd
import numpy as np
import ast
import re
import difflib
import joblib
import tensorflow as tf
from deep_translator import GoogleTranslator
import io

# ------------------- TRANSLATION SETUP -------------------
supported_languages = {
    "English": "en", "Assamese": "as", "Bengali": "bn", "Bodo": "brx", "Dogri": "doi",
    "Gujarati": "gu", "Hindi": "hi", "Kannada": "kn", "Kashmiri": "ks", "Konkani": "kok",
    "Maithili": "mai", "Malayalam": "ml", "Manipuri": "mni", "Marathi": "mr", "Nepali": "ne",
    "Odia": "or", "Punjabi": "pa", "Sanskrit": "sa", "Santali": "sat", "Sindhi": "sd",
    "Tamil": "ta", "Telugu": "te", "Urdu": "ur"
}

PERKS_BENEFITS = [
    "Certificate", "Letter of Recommendation", "Flexible Work Hours",
    "5 Days a Week", "Job Offer", "Informal Dress Code",
    "Free Snacks & Beverages", "Free Snacks", "Free Beverages",
    "Work From Home", "WFH", "Remote Work", "Health Insurance",
    "Performance Bonus", "Team Outings", "Training & Development",
    "Casual Dress Code", "Travel Reimbursement"
]

# ------------------- CLEANING FUNCTIONS -------------------
def clean_location(loc_str):
    if pd.isna(loc_str):
        return ""
    return loc_str.strip("()").replace("'", "")

def parse_duration(dur):
    if pd.isna(dur):
        return 0
    match = re.search(r"(\d+)", str(dur))
    return int(match.group(1)) if match else 0

def parse_stipend(stipend):
    if pd.isna(stipend) or "Unpaid" in str(stipend):
        return 0
    nums = re.findall(r"\d+", stipend.replace(",", ""))
    if len(nums) == 1:
        return int(nums[0])
    elif len(nums) == 2:
        return (int(nums[0]) + int(nums[1])) // 2
    return 0

def parse_skills(sk):
    if pd.isna(sk):
        return [], []
    try:
        items = ast.literal_eval(sk)
        if not isinstance(items, list):
            items = [items]
    except:
        items = [sk]

    skills, perks = [], []
    for item in items:
        item_lower = item.lower()
        matched_perk = any(
            difflib.SequenceMatcher(None, item_lower, p.lower()).ratio() > 0.7 or p.lower() in item_lower
            for p in PERKS_BENEFITS
        )
        if matched_perk:
            perks.append(item)
        else:
            skills.append(item)
    return skills, perks

# ------------------- LOAD MODEL + ENCODERS -------------------
@st.cache_resource
def load_model():
    model = tf.keras.models.load_model("internship_model.keras")
    le_location = joblib.load("le_location.pkl")
    le_company = joblib.load("le_company.pkl")
    scaler = joblib.load("scaler.pkl")
    return model, le_location, le_company, scaler

model, le_location, le_company, scaler = load_model()

# ------------------- FILTER FUNCTION -------------------
def filter_internships(df, profile):
    pattern = "|".join([re.escape(loc) for loc in profile["location"]])
    df_filtered = df[df["Location"].str.contains(pattern, case=False, na=False)] if pattern else df.copy()

    def skills_match(row_skills, candidate_skills):
        if not candidate_skills:
            return 1.0
        row_skills_lower = [s.lower() for s in row_skills]
        matches = sum(skill.lower() in row_skills_lower for skill in candidate_skills)
        return matches / len(candidate_skills)

    df_filtered.loc[:, "SkillMatchRatio"] = df_filtered["Skills"].apply(lambda x: skills_match(x, profile["skills"]))
    df_filtered.loc[:, "SkillsMatch"] = df_filtered["SkillMatchRatio"] >= 0.5
    return df_filtered[df_filtered["SkillsMatch"]].copy()

# ------------------- STREAMLIT CONFIG -------------------
st.set_page_config(page_title="InternAI", page_icon="🚀", layout="wide")

st.markdown("""
<style>
/* Grid container */
.internship-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
    gap: 20px;
    margin-top: 20px;
}

/* Card styling */
.internship-card {
    background-color: #161a23;
    border-radius: 16px;
    padding: 20px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.25);
    color: white;
    min-height: 340px;  /* Equal height */
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    transition: all 0.3s ease;
}
.internship-card:hover { transform: translateY(-6px); }

/* Top Match Highlight */
.top-match {
    border: 2px solid gold;
    box-shadow: 0 0 15px gold;
}
.top-badge {
    position: absolute;
    top: 10px;
    right: 10px;
    background: linear-gradient(45deg, #FFD700, #FFA500);
    color: black;
    font-weight: bold;
    padding: 4px 10px;
    border-radius: 12px;
    font-size: 12px;
}

/* Progress bar */
.progress-bar-bg {
    width: 100%;
    height: 18px;
    background: #333;
    border-radius: 8px;
    overflow: hidden;
    margin-top: 10px;
}

/* Badges */
.badge {
    background: #2563eb;
    color: white;
    padding: 3px 8px;
    border-radius: 8px;
    font-size: 12px;
    margin: 2px;
    display: inline-block;
}
.perk-badge { background: #9333ea; }

/* Apply Button */
.apply-button {
    display: inline-block;
    padding: 8px 14px;
    background: #ff4b4b;
    color: white;
    border-radius: 10px;
    text-decoration: none;
    font-weight: bold;
    transition: 0.2s;
    margin-top: 10px;
    text-align: center;
}
.apply-button:hover { background: #e63b3b; }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center;'>🚀 InternAI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#bbb;'>Find your perfect internship match using AI</p>", unsafe_allow_html=True)

# ------------------- LOAD DATA -------------------
@st.cache_data
def load_data():
    df = pd.read_csv("internship_data.csv")
    df["Location"] = df["Location"].apply(clean_location)
    df["Duration"] = df["Duration"].apply(parse_duration)
    df["Stipend"] = df["Stipend"].apply(parse_stipend)
    df[["Skills", "Perks"]] = df["Skills"].apply(lambda x: pd.Series(parse_skills(x)))
    if "Education" not in df.columns:
        df["Education"] = "Graduation"
    return df

data = load_data()

# ------------------- SIDEBAR -------------------
st.sidebar.header("🧑 Candidate Profile")
selected_language = st.sidebar.selectbox("🌐 Select Language", list(supported_languages.keys()), index=0)
target_lang = supported_languages[selected_language]

def t(text):
    if target_lang == "en":
        return text
    try:
        return GoogleTranslator(source='auto', target=target_lang).translate(text)
    except:
        return text

available_locations = sorted(list(set(sum([loc.split(",") for loc in data["Location"].dropna().unique()], []))))
available_skills = sorted({skill for skills in data["Skills"] for skill in (skills if isinstance(skills, list) else [])})

candidate_location = st.sidebar.multiselect(t("📍 Preferred Location(s)"), options=available_locations, default=[])
candidate_skills = st.sidebar.multiselect(t("🛠 Skills"), options=available_skills, default=[])
candidate_education = st.sidebar.selectbox(t("🎓 Education"), ["Class 10", "Class 12", "Diploma", "Graduation"], index=3)
min_stipend = st.sidebar.slider(t("💰 Minimum Stipend (₹/month)"), 0, 50000, 0, step=500)

predict_button = st.sidebar.button(t("🔮 Get AI Recommendations"))

# ------------------- PREDICTIONS + PAGINATION -------------------
if predict_button:
    candidate_profile = {"education": candidate_education, "skills": candidate_skills, "location": candidate_location}
    filtered_data = filter_internships(data, candidate_profile)
    filtered_data = filtered_data[filtered_data["Stipend"] >= min_stipend]

    if filtered_data.empty:
        st.warning(t("😔 No matching internships found! Try changing filters."))
    else:
        try:
            filtered_data["Location_enc"] = le_location.transform(filtered_data["Location"])
        except:
            filtered_data["Location_enc"] = 0

        try:
            filtered_data["Company_enc"] = le_company.transform(filtered_data["Company Name"])
        except:
            filtered_data["Company_enc"] = 0

        X = filtered_data[["Location_enc", "Stipend", "Duration"]]
        X_scaled = scaler.transform(X)
        filtered_data["Score"] = model.predict(X_scaled).flatten()

        filtered_data = filtered_data.sort_values(by="Score", ascending=False)

        # Pagination state
        if "page" not in st.session_state:
            st.session_state.page = 0

        start_idx = st.session_state.page * 6
        end_idx = start_idx + 6
        internships_to_show = filtered_data.iloc[start_idx:end_idx]

        st.subheader(t("🏆 Internship Recommendations"))

        st.markdown('<div class="internship-grid">', unsafe_allow_html=True)
        max_score = filtered_data["Score"].max()

        for i, (_, row) in enumerate(internships_to_show.iterrows()):
            score_percentage = int((row["Score"] / max_score) * 100) if max_score > 0 else 0
            bar_color = "#22c55e" if score_percentage >= 70 else "#facc15" if score_percentage >= 40 else "#ef4444"

            apply_button_html = ""
            if pd.notna(row["Website Link"]) and str(row["Website Link"]).strip():
                apply_button_html = f'<a href="{row["Website Link"]}" target="_blank" class="apply-button">🚀 {t("Apply Now")}</a>'

            html_card = f"""
            <div class="internship-card {'top-match' if i == 0 and st.session_state.page == 0 else ''}">
                {"<div class='top-badge'>⭐ Top Match</div>" if i == 0 and st.session_state.page == 0 else ""}
                <h4 style="color:#ff9068;">💼 {row['Role']}</h4>
                <p style="color:#aaa;">🏢 {row['Company Name']}</p>
                <p>📍 <b>{t('Location')}:</b> {row['Location']}</p>
                <p>💰 <b>{t('Stipend')}:</b> ₹{int(row['Stipend']):,}/month</p>
                <p>⏳ <b>{t('Duration')}:</b> {row['Duration']} {t('months')}</p>
                <p>🛠 <b>{t('Skills Required')}:</b> {" ".join([f'<span class="badge">{skill}</span>' for skill in row['Skills']])}</p>
                <p>🎁 <b>{t('Perks & Benefits')}:</b> {" ".join([f'<span class="badge perk-badge">{perk}</span>' for perk in row['Perks']])}</p>
                <div class="progress-bar-bg">
                    <div style="background-color:{bar_color}; width:{score_percentage}%; height:100%; text-align:center; color:white; font-weight:bold; font-size:12px; line-height:18px;">
                        {score_percentage}% {t('Match')}
                    </div>
                </div>
                {apply_button_html}
            </div>
            """
            st.markdown(html_card, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        # Pagination controls
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            if st.session_state.page > 0 and st.button("⬅️ Previous"):
                st.session_state.page -= 1
                st.rerun()
        with col3:
            if end_idx < len(filtered_data) and st.button("Next ➡️"):
                st.session_state.page += 1
                st.rerun()

else:
    st.info(t("👈 Fill in your preferences and click **Get AI Recommendations** to see results."))
