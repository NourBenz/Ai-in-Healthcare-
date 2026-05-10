# 🏗️ System Architecture & Design

## Overview

The Breast Cancer Diagnosis Dashboard is a comprehensive ML system with a modern web interface, backend API, and multiple machine learning models for clinical decision support.

## System Components

### 1. Frontend Layer
**Technology:** Streamlit  
**File:** `app.py`

```
┌─────────────────────────────────────────┐
│         Streamlit Dashboard             │
├─────────────────────────────────────────┤
│  Dashboard  │ Dataset  │ Predict │       │
│  Patients   │ Reports  │ Settings│       │
└─────────────────────────────────────────┘
         ↓
    Session State
    ├─ Models (cached)
    ├─ Prediction History
    ├─ UI State
    └─ User Preferences
```

**Pages:**
- **Dashboard:** Overview and KPIs
- **Dataset Exploration:** Data analysis and visualization
- **Predict:** Real-time prediction interface
- **Patients:** Patient tracking and history
- **Reports:** Statistical analysis and trends

### 2. Backend Layer
**Technology:** Flask + REST API  
**File:** `backend_api.py`

```
┌────────────────────────────────────────┐
│      Flask REST API Server             │
├────────────────────────────────────────┤
│  /api/train            │ Train models   │
│  /api/predict          │ Single predict │
│  /api/batch-predict    │ Batch predict  │
│  /api/metrics          │ Get metrics    │
│  /api/features         │ Feature info   │
│  /api/dataset/info     │ Data info      │
│  /api/feature-importance  │ Importance  │
│  /api/health           │ Status check   │
└────────────────────────────────────────┘
```

### 3. Data Processing Layer
**File:** `utils.py`

```
DataProcessor
├─ load_data()
├─ get_dataset_summary()
├─ get_column_stats()
└─ handle_missing_values()

PredictionProcessor
├─ prepare_input()
├─ format_prediction_result()
└─ create_prediction_record()

ExportHandler
├─ export_to_csv()
└─ export_to_json()

MetricsCalculator
├─ format_metrics()
└─ get_confusion_matrix()

ValidationHelper
├─ validate_patient_input()
└─ validate_file()

ReportGenerator
├─ generate_model_report()
└─ generate_prediction_summary()
```

### 4. Configuration Layer
**File:** `config.py`

```
CONFIG
├─ DATA_CONFIG
│  ├─ data_path
│  ├─ target_column
│  └─ train_test_split
├─ MODEL_CONFIG
│  ├─ logistic_regression
│  ├─ random_forest
│  └─ knn
├─ STREAMLIT_CONFIG
│  ├─ page_title
│  └─ theme
├─ API_CONFIG
│  ├─ host
│  └─ port
└─ VIZ_CONFIG
   ├─ colors
   └─ styles
```

### 5. ML Models Layer

```
┌───────────────────────────────────────┐
│    ML Model Pipeline (scikit-learn)   │
├───────────────────────────────────────┤
│  Data → Encoding → Scaling → Model    │
└───────────────────────────────────────┘
         ↓
┌───────────────────────────────────────┐
│      Three Trained Models             │
├───────────────────────────────────────┤
│  1. Logistic Regression (fast)        │
│  2. Random Forest (best accuracy)     │
│  3. K-Nearest Neighbors (robust)      │
└───────────────────────────────────────┘
```

## Data Flow

### Prediction Flow
```
User Input
    ↓
[Frontend - Streamlit]
    ↓
validate_patient_input()
    ↓
prepare_input()
    ↓
[Encoding Layer]
encode(categorical)
    ↓
[Scaling Layer]
scaler.transform()
    ↓
[Model Layer]
model.predict_proba()
    ↓
format_prediction_result()
    ↓
[Frontend - Display]
Show Results
    ↓
save to session_state
    ↓
[Export Layer]
download_to_csv()
```

### Training Flow
```
Dataset Load
    ↓
Data Cleaning
    ↓
Feature Engineering
    ├─ Categorical Encoding
    ├─ Numerical Scaling
    └─ Feature Selection (implicit)
    ↓
Train/Test Split (80/20)
    ↓
Model Training (Parallel)
    ├─ Logistic Regression
    ├─ Random Forest (with GridSearch)
    └─ KNN
    ↓
Model Evaluation
    ├─ Accuracy Score
    ├─ F1-Macro Score
    └─ Classification Report
    ↓
Cache Results
    ↓
Ready for Prediction
```

## Database Schema

### Prediction History (Session Memory)
```
{
  "Timestamp": "2024-04-26 14:30:00",
  "Model": "RandomForest",
  "Patient_Features": {...},
  "Predicted_Diagnosis": "Alive",
  "Confidence": 0.87,
  "Prob_Alive": 0.87,
  "Prob_Dead": 0.13
}
```

## Key Architectural Decisions

### 1. Single App File vs Multi-Page
**Decision:** Single app.py with conditional page rendering  
**Reason:** Simpler state management, easier model caching

### 2. Session State for Predictions
**Decision:** Store predictions in Streamlit session state  
**Reason:** No backend database setup required initially, suitable for demo

### 3. Model Caching
**Decision:** Use @st.cache_resource for model persistence  
**Reason:** Fast subsequent runs, single training operation

### 4. Three ML Models
**Decision:** Logistic Regression, Random Forest, KNN  
**Reason:** Covers different model families, allows user choice

### 5. Flask Backend (Optional)
**Decision:** Separate Flask API for scalability  
**Reason:** Easy to move to production, supports load balancing

## Deployment Scenarios

### Development
```
Streamlit (8501) ←→ Local Filesystem
   ↑
Browser (localhost:8501)
```

### Testing with Backend
```
Streamlit (8501) ←→ Flask API (5000)
   ↓              ↓
Browser      Filesystem
```

### Production (Scalable)
```
Load Balancer
    ├→ Streamlit Server 1 (8501)
    ├→ Streamlit Server 2 (8501)
    └→ Streamlit Server 3 (8501)
         ↓
    API Gateway
         ↓
    Flask Server (5000)
         ↓
    Database (PostgreSQL)
    Cache Layer (Redis)
    File Storage (S3)
```

## Security Considerations

### Current Implementation
- ✅ Input validation on user inputs
- ✅ Safe categorical encoding
- ✅ Feature range checking
- ⚠️ No authentication (local use)
- ⚠️ No data encryption (local use)

### Production Recommendations
- [ ] Add user authentication (JWT)
- [ ] Encrypt sensitive data
- [ ] Use HTTPS/SSL
- [ ] Implement rate limiting
- [ ] Add database encryption
- [ ] Use environment variables for secrets
- [ ] Add API key authentication
- [ ] Implement audit logging

## Performance Optimization

### Current Optimizations
1. **Model Caching:** Trained models cached after first run
2. **Data Caching:** Dataset loaded once via @st.cache_data
3. **Vectorized Operations:** NumPy/scikit-learn for efficient computation
4. **Lazy Loading:** Components load only when accessed

### Potential Improvements
1. Implement Redis caching for API
2. Use batch processing for bulk predictions
3. Add GPU acceleration for large datasets
4. Implement database indexing
5. Use CDN for static assets

## Scalability Roadmap

### Phase 1 (Current)
- ✅ Single Flask instance
- ✅ In-memory model storage
- ✅ Session-based prediction history

### Phase 2 (Recommended)
- [ ] PostgreSQL database
- [ ] Redis cache layer
- [ ] Multiple Flask instances behind load balancer
- [ ] Streamlit cloud deployment

### Phase 3 (Enterprise)
- [ ] Kubernetes orchestration
- [ ] Microservices architecture
- [ ] GraphQL API
- [ ] Real-time analytics dashboard
- [ ] Model versioning system

## Testing Strategy

### Unit Tests
```python
test_utils.py
├─ test_load_data()
├─ test_validate_input()
└─ test_format_results()

test_models.py
├─ test_model_training()
├─ test_predictions()
└─ test_metrics()
```

### Integration Tests
```python
test_api.py
├─ test_api_train()
├─ test_api_predict()
└─ test_api_metrics()

test_frontend.py
├─ test_page_load()
├─ test_prediction_form()
└─ test_export()
```

## Monitoring & Logging

### Key Metrics
- Model accuracy over time
- Prediction confidence distribution
- API response times
- Feature usage frequency
- Error rates and types

### Logging Levels
- INFO: Model training, API calls
- WARNING: Input validation issues, performance alerts
- ERROR: Model failures, API errors
- DEBUG: Detailed execution traces

## Technology Stack Summary

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Frontend | Streamlit | Interactive web interface |
| Backend | Flask | REST API server |
| ML | scikit-learn | Machine learning models |
| Data | pandas, NumPy | Data manipulation |
| Viz | matplotlib, seaborn | Data visualization |
| Config | Python | Configuration management |

## File Dependencies

```
app.py (main)
├── imports: streamlit, pandas, numpy, sklearn, matplotlib
├── uses: Breast_Cancer.csv
├── imports functions from: utils.py (optional)
└── connects to: backend_api.py (optional via API)

backend_api.py
├── imports: flask, pandas, sklearn, pickle
├── uses: Breast_Cancer.csv
├── imports from: utils.py (optional)
└── serves: REST API endpoints

utils.py
├── imports: pandas, numpy, sklearn
└── provides: Helper classes and functions

config.py
├── imports: os, pathlib
└── provides: Configuration constants
```

## Future Enhancements

1. **Model Improvements**
   - Deep learning models (LSTM, CNN)
   - Ensemble methods (XGBoost, LightGBM)
   - Hyperparameter tuning automation

2. **Feature Engineering**
   - Feature importance analysis
   - Feature interaction detection
   - Automated feature selection

3. **Clinical Features**
   - Risk stratification scores
   - Treatment recommendations
   - Clinical outcome predictions

4. **Data Management**
   - Multi-dataset support
   - Data versioning
   - Automated data validation

5. **UI/UX Improvements**
   - Dark mode
   - Mobile responsiveness
   - Custom report generation
   - Real-time collaboration

---

**Architecture Version:** 1.0  
**Last Updated:** April 2026
