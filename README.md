# 🚀 InternAI

**Find your perfect internship match using AI**

InternAI is an intelligent internship recommendation system that uses machine learning to match candidates with suitable internship opportunities based on their skills, location preferences, and education level.

## ✨ Features

- **AI-Powered Recommendations**: Uses a neural network model to score and rank internships
- **Multi-Language Support**: Available in 22+ Indian regional languages including Hindi, Tamil, Telugu, Bengali, and more
- **Smart Filtering**: Filter by location, skills, education level, and minimum stipend
- **Skill Matching**: Advanced algorithm to match candidate skills with job requirements
- **Interactive UI**: Clean, mobile-friendly Streamlit interface
- **Export Results**: Download top recommendations as CSV files
- **Real-time Translation**: Automatic translation of the interface and content

## 🛠 Technologies Used

- **Python**: Core programming language
- **Streamlit**: Web application framework
- **TensorFlow/Keras**: Neural network model for scoring internships
- **Pandas & NumPy**: Data processing and manipulation
- **Scikit-learn**: Data preprocessing and encoding
- **Deep Translator**: Multi-language support
- **Joblib**: Model serialization

## 📁 Project Structure

```
InternAI/
├── app.py                    # Main Streamlit application
├── InternAI.ipynb          # Jupyter notebook for model training
├── internship_data.csv     # Dataset containing internship listings
├── internship_model.keras  # Trained neural network model
├── le_company.pkl          # Company name label encoder
├── le_location.pkl         # Location label encoder
├── scaler.pkl              # Feature scaler for preprocessing
└── requirements.txt        # Python dependencies
```

## 🚀 Getting Started

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Snehal1808/InternAI.git
   cd InternAI
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

4. **Open your browser**
   Navigate to `http://localhost:8501` to access the application

## 💻 Usage

1. **Select Language**: Choose your preferred language from the sidebar
2. **Set Preferences**: 
   - Select preferred locations
   - Choose your skills from the available options
   - Set education level
   - Define minimum stipend requirements
3. **Get Recommendations**: Click "Get AI Recommendations" button
4. **View Results**: Browse through top 5 matched internships with match scores
5. **Apply**: Use the provided links to apply for internships
6. **Export**: Download results as CSV for future reference

## 🧠 How It Works

### Data Processing
- **Location Cleaning**: Standardizes location formats
- **Duration Parsing**: Extracts numeric duration from text
- **Stipend Processing**: Handles various stipend formats and ranges
- **Skill Extraction**: Separates skills from perks and benefits

### Recommendation Algorithm
1. **Filtering**: Initial filtering based on location and skill matching
2. **Feature Encoding**: Label encoding for categorical variables
3. **Scaling**: Standard scaling for numerical features
4. **Neural Network**: 3-layer neural network for scoring internships
5. **Ranking**: Sort by AI-generated scores to show best matches

### Model Architecture
```
Input Layer (3 features) → Dense(64, ReLU) → Dense(32, ReLU) → Dense(1, Sigmoid)
```

## 📊 Supported Languages

The application supports 22+ Indian languages:
- English, Hindi, Tamil, Telugu, Bengali
- Gujarati, Marathi, Kannada, Malayalam, Punjabi
- Assamese, Odia, Urdu, Sanskrit, Nepali
- And many more regional languages

## 🎯 Key Features Explained

### Smart Skill Matching
- Uses fuzzy matching to identify relevant skills
- Separates technical skills from perks and benefits
- Calculates skill match ratio for better recommendations

### Multi-Language Interface
- Real-time translation of UI elements
- Preserves functionality across all supported languages
- Fallback to English for translation errors

### Export Functionality
- Download top recommendations as CSV
- Includes all relevant internship details
- Easy to share and archive results

## 🔧 Model Training

The model is trained using the Jupyter notebook (`InternAI.ipynb`) which includes:
- Data preprocessing and cleaning
- Feature engineering and encoding
- Neural network architecture definition
- Model training and evaluation
- Serialization of trained components

## 📈 Performance

- **Real-time Processing**: Fast filtering and recommendation generation
- **Scalable**: Handles large datasets efficiently
- **Accurate Matching**: High-precision skill and location matching
- **User-Friendly**: Intuitive interface with clear match percentages

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 👨‍💻 Author

**Snehal** - [GitHub Profile](https://github.com/Snehal1808)

## 🙏 Acknowledgments

- Built for Smart India Hackathon
- Thanks to the open-source community for the amazing libraries
- Special thanks to all contributors and testers

---

**Made with ❤️ for students seeking internship opportunities**