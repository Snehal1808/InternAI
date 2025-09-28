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
<img width="1918" height="889" alt="Screenshot 2025-08-06 200319" src="https://github.com/user-attachments/assets/fbb1aa1f-5ce5-4e60-b9a3-05e7ab5c59a1" />
<img width="1907" height="891" alt="Screenshot 2025-08-06 200624" src="https://github.com/user-attachments/assets/f12c26ce-2e64-43c0-b929-d60118989700" />
<img width="1919" height="895" alt="Screenshot 2025-08-06 200646" src="https://github.com/user-attachments/assets/f295c137-7d40-49aa-a983-6672c82a825c" />
<img width="1917" height="875" alt="Screenshot 2025-08-06 200704" src="https://github.com/user-attachments/assets/c9bac703-132d-4d8e-b261-6c5e0f1e7a08" />
<img width="1919" height="874" alt="Screenshot 2025-08-06 200719" src="https://github.com/user-attachments/assets/3aaaf8f9-4478-4c6d-9a49-5b18bfa7018b" />

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
