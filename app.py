import streamlit as st
import pandas as pd
import numpy as np
import ast
import re
from deep_translator import GoogleTranslator

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
    "5 Days a Week", "Job Offer", "Informal Dress Code"
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
        if any(p.lower() in item.lower() for p in PERKS_BENEFITS):
            perks.append(item)
        else:
            skills.append(item)
    return skills, perks

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
        body { background-color: #0e1117; color: #e0e0e0; }
        .stApp { background-color: #0e1117; }
        .main-title {
            text-align: center;
            font-size: 2.5rem;
            font-weight: 700;
            background: linear-gradient(90deg, #ff4b1f, #ff9068);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem;
        }
        .sub-title { text-align: center; color: #bbb; font-size: 1rem; margin-bottom: 2rem; }
        .internship-card { padding: 20px; border-radius: 16px; background: #161a23; margin-bottom: 20px; }
        .internship-card:hover { transform: translateY(-6px); box-shadow: 0 8px 20px rgba(0,0,0,0.7); }
        .top-match { border: 2px solid #FFD700; box-shadow: 0 0 20px #FFD700; }
        .progress-bar-bg { background-color: #334155; border-radius: 10px; height: 18px; overflow: hidden; }
        .badge { display: inline-block; padding: 2px 8px; border-radius: 10px; margin: 2px; font-size: 12px; background-color: #3B82F6; color: white; }
        .perk-badge { background-color: #8B5CF6; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>InternAI</h1>", unsafe_allow_html=True)
st.markdown("<h2 class='main-title'>Find Your Perfect Internship Match</h2>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>Our advanced AI analyzes your skills, interests, and preferences to recommend the most suitable internship opportunities just for you.</p>", unsafe_allow_html=True)

# ------------------- LOAD DATA -------------------
@st.cache_data
def load_data():
    df = pd.read_csv("internship_data.csv")
    df["Location"] = df["Location"].apply(clean_location)
    df["Duration"] = df["Duration"].apply(parse_duration)
    df["Stipend"] = df["Stipend"].apply(parse_stipend)
    df[["Skills", "Perks"]] = df["Skills"].apply(lambda x: pd.Series(parse_skills(x)))
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

# ------------------- PREDICTIONS -------------------
if predict_button:
    candidate_profile = {"education": candidate_education, "skills": candidate_skills, "location": candidate_location}
    filtered_data = filter_internships(data, candidate_profile)

    st.subheader(t("🧾 Candidate Summary"))
    st.write(f"**{t('Education')}:** {candidate_education}")
    st.write(f"**{t('Preferred Locations')}:** {', '.join(candidate_location) if candidate_location else t('Any')}") 
    st.write(f"**{t('Skills')}:** {', '.join(candidate_skills) if candidate_skills else t('Any')}")
    st.write(f"**{t('Minimum Stipend')}:** ₹{min_stipend:,}/month")

    if filtered_data.empty:
        st.warning(t("😔 No matching internships found! Try changing filters."))
    else:
        filtered_data = filtered_data[filtered_data["Stipend"] >= min_stipend]

        if filtered_data.empty:
            st.warning(t("😔 No internships meet your stipend requirement!"))
        else:
            filtered_data["Score"] = (
                filtered_data["Stipend"]*0.4 +
                filtered_data["Duration"]*0.2 +
                filtered_data["SkillsMatch"].astype(int)*0.4
            )
            top_internships = filtered_data.sort_values(by="Score", ascending=False).head(5)
            max_score = top_internships["Score"].max()
            st.subheader(t("🏆 Top Internship Recommendations"))

            cols = st.columns(2)
            for i, (_, row) in enumerate(top_internships.iterrows()):
                score_percentage = int((row["Score"] / max_score) * 100) if max_score > 0 else 0
                bar_color = "#16A34A" if score_percentage >= 80 else "#22C55E" if score_percentage >= 50 else "#FACC15"
                internship_locs = [loc.strip() for loc in row["Location"].split(",") if loc.strip()]
                unique_locs = list(dict.fromkeys(internship_locs))
                shown_locs = unique_locs if not candidate_location else [
                    loc for loc in unique_locs if any(cand.lower() in loc.lower() for cand in candidate_location)
                ] or unique_locs

                col = cols[i % 2]

                # Show button only if link is present
                apply_link_html = ""
                if pd.notna(row["Website Link"]) and str(row["Website Link"]).strip():
                    apply_link_html = f"""
                    <p style="text-align:center; margin-top:12px;">
                        <a href="{row['Website Link']}" target="_blank" style="
                            background:#3B82F6;
                            color:white;
                            padding:10px 20px;
                            border-radius:10px;
                            font-weight:bold;
                            text-decoration:none;
                            display:inline-block;
                            transition: background 0.3s ease;
                        " onmouseover="this.style.background='#2563EB'" onmouseout="this.style.background='#3B82F6'">
                            🚀 {t('Apply Now')}
                        </a>
                    </p>
                    """

                highlight_class = "top-match" if (row["SkillMatchRatio"] >= 0.8 and row["Stipend"] >= min_stipend) else ""

                col.markdown(f"""
                <div class="internship-card {highlight_class}">
                    <h4 style="color:#ff9068;">💼 {row['Role']}</h4>
                    <p style="color:#aaa;">🏢 {row['Company Name']}</p>
                    <p>📍 <b>{t('Location')}:</b> {', '.join(shown_locs)}</p>
                    <p>💰 <b>{t('Stipend')}:</b> ₹{int(row['Stipend']):,}/month</p>
                    <p>⏳ <b>{t('Duration')}:</b> {row['Duration']} {t('months')}</p>
                    <p>🛠 <b>{t('Skills Required')}:</b> {' '.join([f'<span class="badge">{skill}</span>' for skill in row['Skills']])}</p>
                    <p>🎁 <b>{t('Perks & Benefits')}:</b> {' '.join([f'<span class="badge perk-badge">{perk}</span>' for perk in row['Perks']])}</p>
                    <div class="progress-bar-bg">
                        <div style="
                            background-color:{bar_color};
                            width:{score_percentage}%;
                            height:100%;
                            text-align:center;
                            color:white;
                            font-weight:bold;
                            font-size:12px;
                            line-height:18px;
                            transition: width 1.2s ease-out;
                        ">{score_percentage}% {t('Match')}</div>
                    </div>
                    {apply_link_html}
                </div>
                """, unsafe_allow_html=True)
else:
    st.info(t("👈 Fill in your preferences and click **Get AI Recommendations** to see results."))
