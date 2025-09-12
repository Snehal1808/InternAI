import streamlit as st
import pandas as pd
import joblib

# Load model and encoders
model = joblib.load("model.pkl")
le_location = joblib.load("le_location.pkl")
le_skills = joblib.load("le_skills.pkl")
le_education = joblib.load("le_education.pkl")

# ---- Safe transform for LabelEncoder (handles unseen categories) ----
def safe_transform(encoder, values):
    known_classes = set(encoder.classes_)
    transformed = []
    for v in values:
        if v in known_classes:
            transformed.append(encoder.transform([v])[0])
        else:
            transformed.append(-1)   # Assign -1 for unseen values
    return transformed

# ---- AI Recommendation Page ----
def recommendations_page():
    st.title("🎯 AI-Powered Internship Recommendations")

    # Candidate Profile Inputs
    st.sidebar.header("🧑‍🎓 Candidate Profile")
    language = st.sidebar.selectbox("Select Language", ["English", "Hindi"])
    location = st.sidebar.multiselect("Preferred Location(s)", options=["Delhi", "Bangalore", "Hyderabad", "Mumbai", "Chennai", "Pune"])
    skills = st.sidebar.multiselect("Skills", options=["Python", "ML", "DL", "SQL", "Java", "C++", "Data Analysis"])
    education = st.sidebar.selectbox("Education", ["Diploma", "Graduation", "Post-Graduation", "PhD"])
    stipend = st.sidebar.slider("Minimum Stipend (₹/month)", 0, 50000, 0)

    if st.sidebar.button("🤖 Get AI Recommendations"):
        if not skills or not location:
            st.warning("⚠️ Please select at least one skill and one location.")
            return

        # Create candidate DataFrame
        candidate_data = pd.DataFrame({
            "Location": location,
            "Skills": skills,
            "Education": [education] * len(location)
        })

        # Encode safely
        candidate_data["Location_enc"] = safe_transform(le_location, candidate_data["Location"])
        candidate_data["Skills_enc"] = safe_transform(le_skills, candidate_data["Skills"])
        candidate_data["Education_enc"] = safe_transform(le_education, candidate_data["Education"])

        # Predict
        X = candidate_data[["Location_enc", "Skills_enc", "Education_enc"]]
        candidate_data["Match_Score"] = model.predict_proba(X)[:, 1]

        # Filter based on stipend
        candidate_data = candidate_data[candidate_data["Match_Score"] > 0.3]  # threshold
        candidate_data = candidate_data.sort_values(by="Match_Score", ascending=False)

        if candidate_data.empty:
            st.error("❌ No recommendations found. Try changing your preferences.")
        else:
            for _, row in candidate_data.iterrows():
                st.markdown(
                    f"""
                    <div style="border:1px solid #ccc; border-radius:10px; padding:15px; margin:10px 0; background:#1E1E1E;">
                        <h4 style="color:#FF4B4B;">📍 {row['Location']} | 🎓 {row['Education']}</h4>
                        <p><b>Skill:</b> {row['Skills']}</p>
                        <p><b>AI Match Score:</b> {row['Match_Score']:.2f}</p>
                        <div style="text-align:center; margin-top:10px;">
                            <a href="#" target="_blank">
                                <button style="background-color:#FF4B4B; color:white; border:none; border-radius:8px; padding:8px 20px; cursor:pointer;">
                                    Apply
                                </button>
                            </a>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

# Run app
if __name__ == "__main__":
    recommendations_page()
