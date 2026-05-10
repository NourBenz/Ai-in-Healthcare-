# 🚀 Getting Started - Breast Cancer Diagnosis Dashboard

Complete guide for running the entire system with Streamlit frontend and Flask backend.

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git (optional, for version control)

## 🔧 Installation Steps

### Step 1: Set Up Python Environment

**Windows:**
```bash
# Navigate to project directory
cd C:\Users\narug\Documents\Projects\AIProject

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate
```

**macOS/Linux:**
```bash
cd ~/Documents/Projects/AIProject
python3 -m venv venv
source venv/bin/activate
```

### Step 2: Install Dependencies

```bash
# Upgrade pip first
pip install --upgrade pip

# Install all requirements
pip install -r requirements.txt
```

### Step 3: Verify Installation

```bash
# Check if Streamlit is installed
streamlit --version

# Check if Flask is installed
python -c "import flask; print(f'Flask version: {flask.__version__}')"
```

## 🎯 Running the Application

### Option 1: Streamlit Dashboard Only (Recommended for beginners)

```bash
# Make sure you're in the project directory with venv activated
streamlit run app.py
```

The dashboard will open in your browser at `http://localhost:8501`

### Option 2: Full Stack (Streamlit + Flask Backend)

#### Terminal 1 - Start Backend API:
```bash
# Activate virtual environment (if not already activated)
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # macOS/Linux

# Start Flask API server
python backend_api.py
```

You should see:
```
 * Running on http://0.0.0.0:5000
 * WARNING in production...
```

#### Terminal 2 - Start Streamlit Dashboard:
```bash
# Activate virtual environment
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # macOS/Linux

# Start Streamlit app
streamlit run app.py
```

## 📱 Using the Dashboard

### Navigation

The dashboard has 5 main sections (accessible from the left sidebar):

1. **Dashboard** 
   - Overview of dataset and model performance
   - Key metrics and statistics
   - Feature importance visualization
   - Clinical tips

2. **Dataset Exploration**
   - Complete data analysis
   - Feature distributions
   - Correlation heatmap
   - Statistical summaries
   - Missing value analysis

3. **Predict**
   - Make predictions on new patients
   - Select ML model (Logistic Regression, Random Forest, KNN)
   - Adjust confidence threshold
   - View prediction results
   - Download predictions as CSV

4. **Patients**
   - View all predicted patients
   - Track prediction history
   - Export patient data
   - Clear history

5. **Reports & Statistics**
   - Model performance comparison
   - Feature importance analysis
   - Prediction analytics
   - Diagnosis distribution
   - Confidence score trends

### Making a Prediction

1. Click **"Predict"** in the sidebar
2. Select your preferred ML model
3. Adjust the confidence threshold (default: 55%)
4. Fill in patient details in the form
5. Click **"🔍 Predict Diagnosis"**
6. Review the result and download if needed

## 🔌 API Endpoints (if running Backend)

### Health Check
```
GET /api/health
```

### Train Models
```
POST /api/train
```

### Make Prediction
```
POST /api/predict
Content-Type: application/json

{
  "model": "RandomForest",
  "patient_data": {
    "Age": 65,
    "Race": "White",
    ...
  }
}
```

### Get Metrics
```
GET /api/metrics
```

### Get Features
```
GET /api/features
```

### Get Dataset Info
```
GET /api/dataset/info
```

### Feature Importance
```
GET /api/feature-importance
```

### Batch Prediction
```
POST /api/batch-predict
Content-Type: application/json

{
  "model": "RandomForest",
  "patients": [...]
}
```

## 📊 Data Format

### Patient Input Format

When making predictions, provide patient data in this format:

```python
patient_data = {
    "Age": 65,
    "Race": "White",
    "Marital Status": "Married",
    "T Stage": "T1",
    "N Stage": "N1",
    "6th Stage": "IIA",
    "differentiate": "Poorly differentiated",
    "Grade": 3,
    "A Stage": "Regional",
    "Tumor Size": 18,
    "Estrogen Status": "Positive",
    "Progesterone Status": "Positive",
    "Regional Node Examined": 24,
    "Reginol Node Positive": 1,
    "Survival Months": 60
}
```

## 🐛 Troubleshooting

### Issue: "ModuleNotFoundError"
```
Solution: Make sure your virtual environment is activated and all requirements are installed
pip install -r requirements.txt
```

### Issue: "Port 8501 is already in use"
```
Solution: Kill the existing process or specify a different port
streamlit run app.py --server.port 8502
```

### Issue: "Port 5000 is already in use" (for backend)
```
Solution: Edit backend_api.py and change the port in the last line:
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Issue: Dataset not found
```
Solution: Verify Breast_Cancer.csv is in the project root directory
ls -la Breast_Cancer.csv  # macOS/Linux
dir Breast_Cancer.csv    # Windows
```

### Issue: Models take too long to train
```
Solution: This is normal for the first run (60-120 seconds).
Subsequent runs use cached models. You can clear cache:
streamlit cache clear
```

## 📁 Project File Structure

```
AIProject/
├── app.py                    # Main Streamlit application
├── backend_api.py            # Flask REST API
├── config.py                 # Configuration settings
├── utils.py                  # Utility functions
├── Breast_Cancer.csv         # Dataset
├── requirements.txt          # Python dependencies
├── README.md                 # Project documentation
├── GETTING_STARTED.md        # This file
└── notebookBC.ipynb          # Jupyter notebook analysis
```

## 🔒 Production Deployment

### For Production Use (Do NOT use debug=True):

**Streamlit Production:**
```bash
streamlit run app.py --logger.level=error --client.showErrorDetails=false
```

**Flask Production:**
```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 backend_api:app
```

### Environment Variables

Create a `.env` file in the project root:

```
FLASK_ENV=production
DEBUG=False
API_HOST=0.0.0.0
API_PORT=5000
DATA_PATH=Breast_Cancer.csv
```

## 📈 Performance Tips

1. **First Run**: Models are trained once and cached. First run takes 60-120 seconds.
2. **Memory**: For large datasets, consider:
   - Reducing test_size in config.py
   - Using feature selection
   - Increasing machine RAM

3. **Speed Optimization**:
   - Use Random Forest for best performance
   - Reduce number of GridSearchCV iterations if needed
   - Run backend and frontend on separate machines for production

## 📚 Additional Resources

- [Streamlit Documentation](https://docs.streamlit.io)
- [Flask Documentation](https://flask.palletsprojects.com)
- [scikit-learn Docs](https://scikit-learn.org/stable)
- [pandas User Guide](https://pandas.pydata.org/docs)

## ✅ Verification Checklist

- [ ] Python 3.8+ installed
- [ ] Virtual environment created and activated
- [ ] All requirements installed successfully
- [ ] Breast_Cancer.csv in project directory
- [ ] app.py runs without errors
- [ ] Dashboard loads in browser at localhost:8501
- [ ] Can make predictions successfully
- [ ] Backend API starts (if using full stack)
- [ ] Can access API endpoints

## 🆘 Getting Help

1. Check the troubleshooting section above
2. Review console output for error messages
3. Verify all requirements are installed: `pip list`
4. Clear Streamlit cache: `streamlit cache clear`
5. Restart both backend and frontend services

## 🎉 Ready to Go!

Once everything is set up, you have a fully functional ML dashboard with:
- ✅ Real-time predictions
- ✅ Multiple ML models
- ✅ Patient tracking
- ✅ Statistical analysis
- ✅ REST API backend
- ✅ Beautiful UI/UX

Enjoy! 🚀

---

**Last Updated:** April 2026  
**Version:** 1.0.0
