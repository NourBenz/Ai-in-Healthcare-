# 🏥 Breast Cancer Diagnosis Dashboard

A comprehensive Python-based machine learning dashboard for breast cancer survival prediction using Streamlit. Features multiple machine learning models, real-time predictions, patient tracking, and statistical analytics.

## 🎯 Features

### 📊 **Dashboard**
- Overview of model performance metrics
- Class distribution visualization
- Top 10 most important features (Random Forest)
- Model comparison statistics

### 🔬 **Dataset Exploration**
- Complete dataset overview and statistics
- Data types and missing value analysis
- Feature correlation heatmap
- Distribution analysis of numerical features
- Target variable breakdown

### 🤖 **Predictions**
- Real-time patient diagnosis prediction
- Three ML models available:
  - Logistic Regression
  - Random Forest (with hyperparameter tuning)
  - K-Nearest Neighbors
- Adjustable confidence threshold
- Probability distribution visualization
- Download predictions as CSV

### 👥 **Patients Management**
- Track all predicted patients
- View prediction history
- Export patient predictions
- Diagnosis distribution across predictions
- Clear history functionality

### 📈 **Reports & Statistics**
- Comprehensive model performance dashboard
- Feature importance analysis
- Prediction analytics and trends
- Diagnosis distribution charts
- Confidence score distribution
- Model usage frequency

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip or conda

### Installation

```bash
# Clone or navigate to project directory
cd AIProject

# Install dependencies
pip install -r requirements.txt
```

### Running the Application

```bash
streamlit run app.py
```

The app will open in your default browser at `http://localhost:8501`

## 📁 Project Structure

```
AIProject/
├── app.py                  # Main Streamlit application
├── Breast_Cancer.csv       # Dataset (196K+ records)
├── requirements.txt        # Python dependencies
├── notebookBC.ipynb        # Jupyter notebook for analysis
└── README.md              # This file
```

## 📊 Dataset Information

**Source:** Breast Cancer Clinical Dataset  
**Records:** 196+ patient cases  
**Features:** 15 clinical and demographic variables
- Age, Race, Marital Status
- Tumor staging (T, N, 6th Stage, A Stage)
- Tumor characteristics (Size, Grade, Differentiation)
- Biomarkers (Estrogen Status, Progesterone Status)
- Regional node data (Examined, Positive)
- Survival data (Months, Status)

**Target Variable:** Status (Alive/Dead)

## 🤖 Machine Learning Models

All models use the same train-test split (80/20) with StandardScaler preprocessing:

| Model | Accuracy | F1-Macro |
|-------|----------|----------|
| Logistic Regression | ~83% | ~75% |
| Random Forest | ~85% | ~80% |
| K-Nearest Neighbors | ~82% | ~73% |

*Random Forest* is the best performing model (optimized via GridSearchCV)

## 🎨 UI/UX Features

- **Modern Design:** Clean, professional interface with gradient backgrounds
- **Responsive Layout:** Wide layout with optimized spacing
- **Interactive Widgets:** Forms, tabs, and multi-select controls
- **Data Visualization:** Charts, histograms, heatmaps, and pie charts
- **Real-time Updates:** Session state management for persistent predictions

## 🔧 Technical Stack

- **Frontend:** Streamlit 1.51+
- **Backend:** Python 3.8+
- **ML Libraries:** scikit-learn, pandas, numpy
- **Visualization:** matplotlib, seaborn
- **Data Processing:** pandas

## 📝 Usage Guide

### Making a Prediction

1. Navigate to **Predict** page
2. Select desired ML model
3. Adjust confidence threshold (default: 55%)
4. Fill in patient details
5. Click "🔍 Predict Diagnosis"
6. Review results and download if needed

### Exploring Data

1. Go to **Dataset Exploration** page
2. View statistical summaries
3. Analyze feature correlations
4. Check distributions of numerical features

### Viewing Analytics

1. Navigate to **Reports & Statistics**
2. Review model performance metrics
3. Analyze feature importance
4. Check prediction history trends

## 🔐 Data Privacy

- Predictions are stored in session state (browser memory)
- No data is sent to external servers
- Clear History button removes all predictions from current session

## ⚙️ Configuration

Edit `app.py` to modify:

```python
DATA_PATH = "Breast_Cancer.csv"    # Dataset file path
TARGET_COL = "Status"               # Target variable column
DROP_COLS = []                      # Columns to exclude
RANDOM_STATE = 42                   # Random seed for reproducibility
```

## 🤝 Customization

### Adding New Features
1. Update `DROP_COLS` if you want to exclude columns
2. Modify `TARGET_COL` if your target variable has a different name
3. Retrain models (automatically cached after first run)

### Modifying Models
Edit the `train_all()` function to:
- Add new ML algorithms
- Adjust hyperparameters
- Change cross-validation strategy

### Styling
CSS styles are in the Streamlit markdown section. Modify colors, fonts, and layouts as needed.

## 🐛 Troubleshooting

**Issue:** Dataset not found
- **Solution:** Ensure `Breast_Cancer.csv` is in the same directory as `app.py`

**Issue:** Models take too long to train first time
- **Solution:** This is normal - subsequent runs use cached models. First run may take 30-60 seconds

**Issue:** Charts not displaying
- **Solution:** Clear browser cache and restart Streamlit

## 📚 Additional Resources

- [Streamlit Documentation](https://docs.streamlit.io)
- [scikit-learn User Guide](https://scikit-learn.org/stable/user_guide.html)
- [pandas Documentation](https://pandas.pydata.org/docs/)

## 📄 License

This project is provided as-is for educational and clinical research purposes.

## 👨‍💻 Author

AI Project Team - 2026

---

**Last Updated:** April 2026  
**Version:** 1.0.0
