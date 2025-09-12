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

def t(text):
    if target_lang == "en":
        return text
    try:
        return GoogleTranslator(source='auto', target=target_lang).translate(text)
    except:
        return text

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

        # Show only 6 internships max
        top_internships = filtered_data.sort_values(by="Score", ascending=False).head(6)
        max_score = top_internships["Score"].max()

        st.subheader(t("🏆 Your Matches"))

        cols = st.columns(2)  # grid layout like screenshot
        for i, (_, row) in enumerate(top_internships.iterrows()):
            score_percentage = int((row["Score"] / max_score) * 100) if max_score > 0 else 0
            bar_color = "#22c55e" if score_percentage >= 70 else "#facc15" if score_percentage >= 40 else "#ef4444"
            top_badge_html = '<div class="top-badge">🏆 Top Match</div>' if i == 0 else ""

            skills_html = " ".join([f'<span class="badge">{skill}</span>' for skill in row["Skills"]])
            perks_html = " ".join([f'<span class="badge perk-badge">{perk}</span>' for perk in row["Perks"]])

            apply_button_html = ""
            if pd.notna(row["Website Link"]) and str(row["Website Link"]).strip():
                apply_button_html = f'<div class="apply-btn-container"><a href="{row["Website Link"]}" target="_blank" class="apply-button">Apply Now 🚀</a></div>'

            html_card = f"""
            <div class="internship-card {'top-match' if i == 0 else ''}">
                {top_badge_html}
                <h3 style="color:#fff;">{row['Role']}</h3>
                <p style="color:#bbb;">🏢 {row['Company Name']}</p>
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
            cols[i % 2].markdown(html_card, unsafe_allow_html=True)

        # ------------------- CSV DOWNLOAD -------------------
        csv_buffer = io.StringIO()
        top_internships.to_csv(csv_buffer, index=False)
        st.download_button(
            label=t("💾 Download Top Internships as CSV"),
            data=csv_buffer.getvalue(),
            file_name="top_internships.csv",
            mime="text/csv"
        )
else:
    st.info(t("👈 Fill in your preferences and click **Get AI Recommendations** to see results."))
