import streamlit as st
import pandas as pd
import numpy as np
import io
import joblib
import tensorflow as tf
from deep_translator import GoogleTranslator

# ------------------- TRANSLATION SETUP -------------------
supported_languages = {
    "English": "en", "Assamese": "as", "Bengali": "bn", "Gujarati": "gu",
    "Hindi": "hi", "Kannada": "kn", "Malayalam": "ml", "Marathi": "mr",
    "Odia": "or", "Punjabi": "pa", "Tamil": "ta", "Telugu": "te", "Urdu": "ur"
}

# Load your data and models
data = pd.read_csv("internships.csv")  # <-- replace with your dataset path
model = tf.keras.models.load_model("model.h5")
scaler = joblib.load("scaler.pkl")
le_location = joblib.load("le_location.pkl")
le_company = joblib.load("le_company.pkl")

# ------------------- HELPERS -------------------
def filter_internships(df, profile):
    """Filter internships based on candidate profile"""
    filtered = df.copy()

    # Education filter (simple contains check)
    if profile["education"]:
        filtered = filtered[filtered["Education"].str.contains(profile["education"], na=False)]

    # Skills filter
    if profile["skills"]:
        filtered = filtered[filtered["Skills"].apply(lambda x: any(skill in str(x) for skill in profile["skills"]))]

    # Location filter
    if profile["location"]:
        filtered = filtered[filtered["Location"].apply(lambda x: any(loc in str(x) for loc in profile["location"]))]

    return filtered

# Translation wrapper
def t(text):
    if target_lang == "en":
        return text
    try:
        return GoogleTranslator(source="auto", target=target_lang).translate(text)
    except:
        return text

# ------------------- SIDEBAR -------------------
st.sidebar.markdown(
    """
    <style>
        .sidebar-title { font-size:18px; font-weight:bold; color:#ffffff; margin-bottom:10px; }
        .sidebar-section { margin-bottom:20px; padding:10px; border-radius:10px; background:#161a23; }
    </style>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown("<div class='sidebar-title'>🧑 Candidate Profile</div>", unsafe_allow_html=True)

selected_language = st.sidebar.selectbox("🌐 Language", list(supported_languages.keys()), index=0)
target_lang = supported_languages[selected_language]

with st.sidebar:
    with st.container():
        st.markdown("<div class='sidebar-section'>", unsafe_allow_html=True)
        candidate_education = st.selectbox(t("🎓 Education"), ["Class 10", "Class 12", "Diploma", "Graduation"], index=3)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='sidebar-section'>", unsafe_allow_html=True)
        min_stipend = st.slider(t("💰 Minimum Stipend (₹/month)"), 0, 50000, 0, step=500)
        st.markdown("</div>", unsafe_allow_html=True)

        available_locations = sorted(list(set(sum([loc.split(",") for loc in data["Location"].dropna().unique()], []))))
        st.markdown("<div class='sidebar-section'>", unsafe_allow_html=True)
        candidate_location = st.multiselect(t("📍 Preferred Location(s)"), options=available_locations, default=[])
        st.markdown("</div>", unsafe_allow_html=True)

        available_skills = sorted({skill for skills in data["Skills"] for skill in (skills if isinstance(skills, list) else [])})
        st.markdown("<div class='sidebar-section'>", unsafe_allow_html=True)
        candidate_skills = st.multiselect(t("🛠 Skills"), options=available_skills, default=[])
        st.markdown("</div>", unsafe_allow_html=True)

        predict_button = st.button(t("🔮 Get AI Recommendations"), use_container_width=True)

# ------------------- PREDICTIONS -------------------
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

        # Pagination state
        if "page" not in st.session_state:
            st.session_state.page = 0

        per_page = 6
        start = st.session_state.page * per_page
        end = start + per_page

        top_internships = filtered_data.sort_values(by="Score", ascending=False).iloc[start:end]
        max_score = filtered_data["Score"].max()

        st.subheader(t("🏆 Your Matches"))

        # --- Custom CSS grid ---
        st.markdown(
            """
            <style>
                .cards-grid {
                    display: grid;
                    grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
                    gap: 20px;
                }
                .internship-card {
                    background: #1e293b;
                    border-radius: 12px;
                    padding: 16px;
                    color: white;
                    height: 100%;
                }
                .top-match { border: 2px solid #facc15; }
                .badge {
                    display: inline-block;
                    padding: 3px 8px;
                    margin: 2px;
                    background: #334155;
                    border-radius: 6px;
                    font-size: 12px;
                }
                .perk-badge { background: #4ade80; color: black; }
                .progress-bar-bg {
                    background: #334155;
                    border-radius: 6px;
                    height: 18px;
                    margin-top: 8px;
                    overflow: hidden;
                }
                .apply-button {
                    display: inline-block;
                    margin-top: 10px;
                    padding: 8px 12px;
                    background: #2563eb;
                    color: white;
                    text-decoration: none;
                    border-radius: 6px;
                    font-weight: bold;
                }
            </style>
            <div class="cards-grid">
            """,
            unsafe_allow_html=True,
        )

        # --- Render cards ---
        for i, (_, row) in enumerate(top_internships.iterrows()):
            score_percentage = int((row["Score"] / max_score) * 100) if max_score > 0 else 0
            bar_color = "#22c55e" if score_percentage >= 70 else "#facc15" if score_percentage >= 40 else "#ef4444"
            top_badge_html = '<div style="color:#facc15;font-weight:bold;">🏆 Top Match</div>' if i == 0 and st.session_state.page == 0 else ""

            skills_html = " ".join([f'<span class="badge">{skill}</span>' for skill in row["Skills"]])
            perks_html = " ".join([f'<span class="badge perk-badge">{perk}</span>' for perk in row["Perks"]])

            apply_button_html = ""
            if pd.notna(row["Website Link"]) and str(row["Website Link"]).strip():
                apply_button_html = f'<a href="{row["Website Link"]}" target="_blank" class="apply-button">Apply Now 🚀</a>'

            html_card = f"""
            <div class="internship-card {'top-match' if i == 0 and st.session_state.page == 0 else ''}">
                {top_badge_html}
                <h3>{row['Role']}</h3>
                <p>🏢 {row['Company Name']}</p>
                <p>📍 <b>{t('Location')}:</b> {row['Location']}</p>
                <p>💰 <b>{t('Stipend')}:</b> ₹{int(row['Stipend']):,}/month</p>
                <p>⏳ <b>{t('Duration')}:</b> {row['Duration']} {t('months')}</p>
                <p>🛠 <b>{t('Required Skills')}:</b> {skills_html}</p>
                <p>🎁 <b>{t('Perks & Benefits')}:</b> {perks_html}</p>
                <div class="progress-bar-bg">
                    <div style="background-color:{bar_color}; width:{score_percentage}%; height:100%; text-align:center; color:white; font-weight:bold; font-size:12px; line-height:18px;">
                        {score_percentage}% {t('Match')}
                    </div>
                </div>
                {apply_button_html}
            </div>
            """
            st.markdown(html_card, unsafe_allow_html=True)

        # Close grid
        st.markdown("</div>", unsafe_allow_html=True)

        # ------------------- PAGINATION -------------------
        total_pages = int(np.ceil(len(filtered_data) / per_page))
        col1, col2 = st.columns([1, 5])
        with col1:
            if st.session_state.page > 0:
                if st.button("⬅️ Previous"):
                    st.session_state.page -= 1
                    st.experimental_rerun()
        with col2:
            if st.session_state.page < total_pages - 1:
                if st.button("See More ➡️"):
                    st.session_state.page += 1
                    st.experimental_rerun()

        # ------------------- CSV DOWNLOAD -------------------
        csv_buffer = io.StringIO()
        filtered_data.sort_values(by="Score", ascending=False).to_csv(csv_buffer, index=False)
        st.download_button(
            label=t("💾 Download All Matches as CSV"),
            data=csv_buffer.getvalue(),
            file_name="internships.csv",
            mime="text/csv"
        )
else:
    st.info(t("👈 Fill in your preferences and click **Get AI Recommendations** to see results."))
