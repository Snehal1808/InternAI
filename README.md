# 🚀 InternAI - Smart Internship Matching System

An AI-powered internship recommendation platform achieving **personalized matching** using neural networks. Built for students to find perfect internship opportunities through intelligent skill and location matching with **22+ regional language support**.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://intern-ai.streamlit.app/)

## ✨ Key Features
- **AI-Powered Matching**: 3-layer neural network with feature scaling (personalized scoring)
- **Multi-Language Interface**: 
  - 22+ Indian regional languages (Hindi, Tamil, Telugu, Bengali, etc.)
  - Real-time translation capabilities
  - Mobile-responsive design
- **Smart Filtering**: Location, skills, education level, and stipend filtering
- **Export & Apply**: CSV download and direct application links

## 🚀 Try It Now!
The app is live on Streamlit—no installation needed!
👉 **[Launch App](https://intern-ai.streamlit.app/)**

## 🖼️ Screenshots
<img width="1892" height="890" alt="Screenshot (260)" src="https://github.com/user-attachments/assets/59f2901c-63e2-4a17-a393-2c3db66cf46d" />
<img width="1893" height="885" alt="Screenshot (258)" src="https://github.com/user-attachments/assets/366c623c-e230-4b25-8655-6f1269f38f0d" />
<img width="1885" height="883" alt="Screenshot (259)" src="https://github.com/user-attachments/assets/b5e4e0bb-ac7d-490d-9006-c0cd783e45b7" />

## 🛠 Tech Stack
| Component | Technologies |
|-----------|--------------|
| **Machine Learning** | TensorFlow/Keras, Scikit-learn |
| **Frontend** | Streamlit, Deep Translator |
| **Data Processing** | Pandas, NumPy, Joblib |
| **Language Support** | Google Translator API |

## 📂 Project Structure
```
InternAI/
├── app.py                    # Streamlit application
├── internship_model.keras   # Trained neural network
├── le_company.pkl           # Company encoder
├── le_location.pkl          # Location encoder
├── scaler.pkl               # Feature scaler
├── internship_data.csv      # Dataset
├── requirements.txt         # Dependencies
└── InternAI.ipynb          # Model training notebook
```

## 🧠 Model Architecture
```python
model = Sequential([
    Dense(64, activation='relu', input_shape=(3,)),
    Dense(32, activation='relu'),
    Dense(1, activation='sigmoid')
])
```

## 📊 Performance Metrics
| Metric | Value |
|--------|-------|
| Features Used | Location, Stipend, Duration |
| Skill Matching | Fuzzy string matching (70% threshold) |
| Language Support | 22+ Indian regional languages |
| Processing Speed | Real-time filtering & scoring |

## 🤝 Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you'd like to change.

## 📜 License
Distributed under the MIT License. See [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) for more information.

## ✉️ Contact
Snehal Kumar Subudhi - snehalsubu18@gmail.com
