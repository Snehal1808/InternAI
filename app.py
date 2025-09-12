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

# ------------------- TRANSLATION CACHE -------------------
@st.cache_data
def translate_text(text, target_lang):
    if target_lang == "en":
        return text
    try:
        return GoogleTranslator(source='auto', target=target_lang).translate(text)
    except:
        return text

# ------------------- FILTER FUNCTION -------------------
def filter_internships(df, profile):
    # Filter by location first
    if profile["location"]:
        pattern = "|".join([re.escape(loc) for loc in profile["location"]])
        df = df[df["Location"].str.contains(pattern, case=False, na=False)]

    # Filter by education if column exists
    if "Education" in df.columns:
        df = df[df["Education"].str.contains(profile["education"], case=False, na=False)]

    # Skill matching
    def skills_match(row_skills, candidate_skills):
        if not candidate_skills:
            return 1.0
        row_skills_lower = [s.lower() for s in row_skills]
        matches = sum(skill.lower() in row_skills_lower for skill in candidate_skills)
        return matches / len(candidate_skills)

    df.loc[:, "SkillMatchRatio"] = df["Skills"].apply(lambda x: skills_match(x, profile["skills"]))
    df = df[df["SkillMatchRatio"] >= 0.5]

    return df.copy()

# ------------------- STREAMLIT CONFIG -------------------
st.set_page_config(page_title="InternAI", page_icon="🚀", layout="wide")

# ------------------- CUSTOM CSS -------------------
st.markdown("""
<style>
body { background-color: #0e1117; color: #e0e0e0; }
.stApp { background-color: #0e1117; }

.cards-container {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
    justify-content: center;
    align-items: stretch;
}
.internship-card {
    flex: 1 1 45%;
    min-width: 300px;
    max-width: 500px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: 20px;
    border-radius: 16px;
    background: #161a23;
    transition: all 0.3s ease;
    position: relative;
}
.internship-card:hover {
    transform: translateY(-6px) scale(1.02);
    box-shadow: 0 8px 20px rgba(0,0,0,0.7);
}
.top-match { border: 2px solid #FFD700; box-shadow: 0 0 20px #FFD700; }
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
    box-shadow: 0 2px 6px rgba(0,0,0,0.4);
}
.progress-bar-bg { background-color: #334155; border-radius: 10px; height: 18px; overflow: hidden; }
.badge { display: inline-block; padding: 2px 8px; border-radius: 10px; margin: 2px; font-size: 12px; background-color: #3B82F6; color: white; }
.perk-badge { background-color: #8B5CF6; }
.apply-button {
    background-color: #ff4b4b;
    color: white !important;
    padding: 10px 20px;
    border-radius: 12px;
    font-weight: bold;
    text-decoration: none;
    display: inline-block;
    margin-top: 12px;
    box-shadow: 0 4px 10px rgba(255, 75, 75, 0.3);
    transition: all 0.3s ease;
}
.apply-button:hover {
    background-color: #e63b3b;
    box-shadow: 0 6px 14px rgba(255, 75, 75, 0.5);
    transform: scale(1.05);
}
@media (max-width: 768px) { .internship-card { flex: 1 1 90%; } }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center;'>🚀 InternAI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#bbb;'>Find your perfect internship match using AI</p>", unsafe_allow_html=True)

# ------------------- SIDEBAR -------------------
st.sidebar.header("🧑 Candidate Profile")
selected_language = st.sidebar.selectbox("🌐 Select Language", list(supported_languages.keys()), index=0)
target_lang = supported_languages[selected_language]

available_locations = sorted(list(set(sum([loc.split(",") for loc in data["Location"].dropna().unique()], []))))
available_skills = sorted({skill for skills in data["Skills"] for skill in (skills if isinstance(skills, list) else [])})

candidate_location = st.sidebar.multiselect(translate_text("📍 Preferred Location(s)", target_lang), options=available_locations, default=[])
candidate_skills = st.sidebar.multiselect(translate_text("🛠 Skills", target_lang), options=available_skills, default=[])
candidate_education = st.sidebar.selectbox(translate_text("🎓 Education", target_lang), ["Class 10", "Class 12", "Diploma", "Graduation"], index=3)
min_stipend = st.sidebar.slider(translate_text("💰 Minimum Stipend (₹/month)", target_lang), 0, 50000, 0, step=500)

predict_button = st.sidebar.button(translate_text("🔮 Get AI Recommendations", target_lang))

if predict_button:
    candidate_profile = {"education": candidate_education, "skills": candidate_skills, "location": candidate_location}
    filtered_data = filter_internships(data, candidate_profile)
    filtered_data = filtered_data[filtered_data["Stipend"] >= min_stipend]

    if filtered_data.empty:
        st.warning(translate_text("😔 No matching internships found! Try changing filters.", target_lang))
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

        # Top 6 internships
        top_internships = filtered_data.sort_values(by="Score", ascending=False).head(6)
        max_score = top_internships["Score"].max()

        st.subheader(translate_text("🏆 Top Internship Recommendations", target_lang))

        st.markdown('<div class="cards-container">', unsafe_allow_html=True)
        for i, (_, row) in enumerate(top_internships.iterrows()):
            score_percentage = int((row["Score"] / max_score) * 100) if max_score > 0 else 0

            apply_button_html = ""
            if pd.notna(row["Website Link"]) and str(row["Website Link"]).strip():
                apply_button_html = f'<div style="text-align:center;margin-top:10px;"><a href="{row["Website Link"]}" target="_blank" class="apply-button">🚀 {translate_text("Apply Now", target_lang)}</a></div>'

            top_badge_html = '<div class="top-badge">⭐ Top Match</div>' if i == 0 else ""
            bar_color = "#22c55e" if score_percentage >= 70 else "#facc15" if score_percentage >= 40 else "#ef4444"

            html_card = f"""
            <div class="internship-card {'top-match' if i == 0 else ''}">
            {top_badge_html}
            <h4 style="color:#ff9068;">💼 {row['Role']}</h4>
            <p style="color:#aaa;">🏢 {row['Company Name']}</p>
            <p>📍 <b>{translate_text('Location', target_lang)}:</b> {row['Location']}</p>
            <p>💰 <b>{translate_text('Stipend', target_lang)}:</b> ₹{int(row['Stipend']):,}/month</p>
            <p>⏳ <b>{translate_text('Duration', target_lang)}:</b> {row['Duration']} {translate_text('months', target_lang)}</p>
            <p>🛠 <b>{translate_text('Skills Required', target_lang)}:</b> {" ".join([f'<span class="badge">{skill}</span>' for skill in row['Skills']])}</p>
            <p>🎁 <b>{translate_text('Perks & Benefits', target_lang)}:</b> {" ".join([f'<span class="badge perk-badge">{perk}</span>' for perk in row['Perks']])}</p>
            <div class="progress-bar-bg">
                <div style="background-color:{bar_color}; width:{score_percentage}%; height:100%; text-align:center; color:white; font-weight:bold; font-size:12px; line-height:18px;">
                {score_percentage}% {translate_text('Match', target_lang)}
                </div>
            </div>
            {apply_button_html}
            </div>
            """
            st.markdown(html_card, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # ------------------- CSV DOWNLOAD -------------------
        csv_buffer = io.StringIO()
        top_internships[['Role','Company Name','Location','Stipend','Duration','Skills','Perks','Website Link','Score']].to_csv(csv_buffer, index=False)
        st.download_button(
            label=translate_text("💾 Download Top Internships as CSV", target_lang),
            data=csv_buffer.getvalue(),
            file_name="top_internships.csv",
            mime="text/csv"
        )

else:
    st.info(translate_text("👈 Fill in your preferences and click **Get AI Recommendations** to see results.", target_lang))
