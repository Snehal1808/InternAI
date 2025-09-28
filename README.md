# 🚀 InternAI

**AI-powered internship recommendation system with multi-language support**

InternAI uses machine learning to match candidates with internships based on skills, location, and education level, supporting 22+ Indian regional languages.

## ✨ Features

- **AI-Powered Matching**: Neural network scoring system for personalized recommendations
- **Multi-Language Support**: Interface available in Hindi, Tamil, Telugu, Bengali, and 18+ more languages
- **Smart Filtering**: Filter by location, skills, education, and minimum stipend
- **Export Results**: Download recommendations as CSV files
- **Mobile-Friendly**: Responsive Streamlit interface

## 🛠 Tech Stack

- **Backend**: Python, TensorFlow/Keras, Pandas, Scikit-learn
- **Frontend**: Streamlit with Deep Translator for multi-language support
- **ML Model**: 3-layer neural network with feature scaling and label encoding

## 📁 Project Structure

```
InternAI/
├── app.py                    # Main Streamlit application
├── InternAI.ipynb          # Model training notebook
├── internship_data.csv     # Internship dataset
├── internship_model.keras  # Trained ML model
├── *.pkl files             # Encoders and scaler
└── requirements.txt        # Dependencies
```

## 🚀 Quick Start

```bash
git clone https://github.com/Snehal1808/InternAI.git
cd InternAI
pip install -r requirements.txt
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

## 💻 How to Use

1. Select your preferred language from the sidebar
2. Set preferences: locations, skills, education level, minimum stipend
3. Click "Get AI Recommendations"
4. View top 5 matches with AI-generated scores
5. Apply directly or export results as CSV

## 🧠 How It Works

1. **Data Processing**: Cleans and standardizes internship data (locations, stipends, skills)
2. **Filtering**: Matches user preferences with available internships
3. **AI Scoring**: Neural network evaluates and ranks matches
4. **Results**: Displays top recommendations with match percentages

### Model Architecture
```
Input (3 features) → Dense(64) → Dense(32) → Dense(1) → Score
```

## 🤝 Contributing

Contributions welcome! Please open an issue before making major changes.

## 👨‍💻 Author

**Snehal** - [GitHub](https://github.com/Snehal1808)

---

*Built for Smart India Hackathon - Making internship discovery accessible across India* 🇮🇳