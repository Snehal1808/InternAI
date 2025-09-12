import streamlit as st
import pandas as pd
import numpy as np
import ast
import re
import difflib
import joblib
import tensorflow as tf
from deep_translator import GoogleTranslator
import plotly.graph_objects as go
from datetime import datetime

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

# ------------------- SKILLS RADAR CHART -------------------
def plot_skills_radar(required_skills, candidate_skills, chart_key):
    if not required_skills:
        return
    all_skills = list(set(required_skills + candidate_skills))
    candidate_values = [1 if skill in candidate_skills else 0 for skill in all_skills]
    required_values = [1 for _ in all_skills]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=required_values,
        theta=all_skills,
        fill='toself',
        name='Required Skills',
        line_color='red'
    ))
    fig.add_trace(go.Scatterpolar(
        r=candidate_values,
        theta=all_skills,
        fill='toself',
        name='Your Skills',
        line_color='green'
    ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0,1])),
        showlegend=True,
        template="plotly_dark",
        title="Skills Match Radar"
    )
    st.plotly_chart(fig, use_container_width=True, key=chart_key)

# ------------------- DEADLINE ALERT -------------------
def check_deadline(deadline_str):
    if pd.isna(deadline_str):
        return ""
    try:
        deadline = pd.to_datetime(deadline_str)
        days_left = (deadline - datetime.today()).days
        if days_left <= 3:
            return f"⚠️ Deadline in {days_left} day(s)!"
        elif days_left <= 7:
            return f"⏳ Deadline in {days_left} day(s)"
        else:
            return ""
    except:
        return ""

# ------------------- STREAMLIT CONFIG -------------------
st.set_page_config(page_title="InternAI", page_icon="🚀", layout="wide")

st.markdown("""
    <style>
        body { background-color: #0e1117; color: #e0e0e0; }
        .stApp { background-color: #0e1117; }
        .internship-card { padding: 20px; border-radius: 16px; background: #161a23; margin-bottom: 20px; transition: all 0.3s ease; position: relative; }
        .internship-card:hover { transform: translateY(-6px); box-shadow: 0 8px 20px rgba(0,0,0,0.7); }
        .top-match { border: 2px solid #FFD700; box-shadow: 0 0 20px #FFD700; }
        .top-badge { position: absolute; top: 10px; right: 10px; background: linear-gradient(45deg, #FFD700, #FFA500); color: black; font-weight: bold; padding: 4px 10px; border-radius: 12px; font-size: 12px; box-shadow: 0 2px 6px rgba(0,0,0,0.4); }
        .progress-bar-bg { background-color: #334155; border-radius: 10px; height: 18px; overflow: hidden; }
        .badge { display: inline-block; padding: 2px 8px; border-radius: 10px; margin: 2px; font-size: 12px; background-color: #3B82F6; color: white; }
        .perk-badge { background-color: #8B5CF6; }
        .apply-button { background-color: #ff4b4b; color: white !important; padding: 10px 20px; border-radius: 12px; font-weight: bold; text-decoration: none; display: inline-block; margin-top: 12px; box-shadow: 0 4px 10px rgba(255, 75, 75, 0.3); transition: all 0.3s ease; }
        .apply-button:hover { background-color: #e63b3b; box-shadow: 0 6px 14px rgba(255, 75, 75, 0.5); transform: scale(1.05); }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center;'>🚀 InternAI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#bbb;'>Find your perfect internship match using AI</p>", unsafe_allow_html=True)

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

# ------------------- PREDICTIONS -------------------
if predict_button:
    candidate_profile = {"education": candidate_education, "skills": candidate_skills, "location": candidate_location}
    filtered_data = filter_internships(data, candidate_profile)
    filtered_data = filtered_data[filtered_data["Stipend"] >= min_stipend]

    if filtered_data.empty:
        st.warning(t("😔 No matching internships found! Try changing filters."))
    else:
        # Encode + Scale
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

        top_internships = filtered_data.sort_values(by="Score", ascending=False).head(5)
        max_score = top_internships["Score"].max()

        st.subheader(t("🏆 Top Internship Recommendations"))
        cols = st.columns(2)

        for i, (_, row) in enumerate(top_internships.iterrows()):
            score_percentage = int((row["Score"] / max_score) * 100) if max_score > 0 else 0
            col = cols[i % 2]

            # Apply button
            apply_button_html = ""
            if pd.notna(row.get("Website Link", "")) and str(row["Website Link"]).strip():
                apply_button_html = f'<div style="text-align:center;margin-top:10px;"><a href="{row["Website Link"]}" target="_blank" class="apply-button">🚀 {t("Apply Now")}</a></div>'

            # Top badge
            top_badge_html = '<div class="top-badge">⭐ Top Match</div>' if i == 0 else ""

            # Progress bar color
            bar_color = "#22c55e" if score_percentage >= 70 else "#facc15" if score_percentage >= 40 else "#ef4444"

            # Deadline alert
            deadline_alert = check_deadline(row.get("Deadline", ""))

            # Internship Card HTML
            html_card = f"""
            <div class="internship-card {'top-match' if i == 0 else ''}">
            {top_badge_html}
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
            <p style='color:#FF5733; font-weight:bold;'>{deadline_alert}</p>
            {apply_button_html}
            </div>
            """
            col.markdown(html_card, unsafe_allow_html=True)

            # Skills Radar Chart with unique key
            plot_skills_radar(row['Skills'], candidate_skills, chart_key=f"radar_{i}")

            # Recommendation Explanation
            skills_match_ratio = row["SkillMatchRatio"]
            stipend_fit = row["Stipend"] >= min_stipend
            location_fit = any(loc in row["Location"] for loc in candidate_location)

            st.markdown(f"""
            <details>
            <summary style='color:#FFB703;'>ℹ️ {t('Why this internship was recommended')}</summary>
            <ul>
            <li>{t('Skills Match')}: {skills_match_ratio*100:.0f}%</li>
            <li>{t('Stipend meets your minimum')}: {'Yes' if stipend_fit else 'No'}</li>
            <li>{t('Location Match')}: {'Yes' if location_fit else 'No'}</li>
            </ul>
            </details>
            """, unsafe_allow_html=True)

else:
    st.info(t("👈 Fill in your preferences and click **Get AI Recommendations** to see results."))
