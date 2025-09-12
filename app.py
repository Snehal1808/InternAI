cols = st.columns(2)

for i, (_, row) in enumerate(top_internships.iterrows()):
    score_percentage = int((row["Score"] / max_score) * 100) if max_score > 0 else 0
    bar_color = "#16A34A" if score_percentage >= 80 else "#22C55E" if score_percentage >= 50 else "#FACC15"
    col = cols[i % 2]

    # Top match badge only for first card
    top_badge_html = '<div class="top-badge">🏆 Top Match</div>' if i == 0 else ""

    # Apply button (centered)
    apply_button_html = ""
    if pd.notna(row["Website Link"]) and str(row["Website Link"]).strip():
        apply_button_html = f'''
        <div class="apply-btn-container">
            <a href="{row["Website Link"]}" target="_blank" class="apply-button">🚀 {t("Apply Now")}</a>
        </div>
        '''

    # ✅ Render card with markdown (HTML enabled)
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
    {apply_button_html}
</div>
"""
    col.markdown(html_card, unsafe_allow_html=True)
