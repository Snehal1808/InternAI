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

        # Sort by score
        all_internships = filtered_data.sort_values(by="Score", ascending=False).reset_index(drop=True)
        max_score = all_internships["Score"].max()

        st.subheader(t("🏆 Your Matches"))

        # ---------- Pagination setup ----------
        if "internship_offset" not in st.session_state:
            st.session_state.internship_offset = 0
        page_size = 6
        start_idx = st.session_state.internship_offset
        end_idx = start_idx + page_size

        internships_to_show = all_internships.iloc[start_idx:end_idx]

        # ---------- Render internships ----------
        for i, (_, row) in enumerate(internships_to_show.iterrows(), start=start_idx):
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
            st.markdown(html_card, unsafe_allow_html=True)

        # ---------- See More Button ----------
        if end_idx < len(all_internships):
            if st.button("👉 See More Internships"):
                st.session_state.internship_offset += page_size
                st.experimental_rerun()

        # ---------- Reset Button ----------
        if st.session_state.internship_offset > 0:
            if st.button("🔄 Back to Top Matches"):
                st.session_state.internship_offset = 0
                st.experimental_rerun()

else:
    st.info(t("👈 Fill in your preferences and click **Get AI Recommendations** to see results."))
