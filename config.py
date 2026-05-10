"""
Configuration file for Breast Cancer Diagnosis System
"""

import os
from pathlib import Path

# Project root
PROJECT_ROOT = Path(__file__).parent.absolute()

# Data configuration
DATA_CONFIG = {
    "DATA_PATH": PROJECT_ROOT / "Breast_Cancer.csv",
    "TARGET_COL": "Status",
    "DROP_COLS": [],  # Columns to exclude from features
    "TEST_SIZE": 0.2,
    "RANDOM_STATE": 42,
}

# Model configuration
MODEL_CONFIG = {
    "logistic_regression": {
        "max_iter": 1000,
        "random_state": 42,
    },
    "random_forest": {
        "random_state": 42,
        "n_estimators": [100, 200],
        "max_depth": [None, 10],
    },
    "knn": {
        "n_neighbors": 5,
    }
}

# Streamlit configuration
STREAMLIT_CONFIG = {
    "page_title": "🏥 MedAI Diagnosis - Breast Cancer Prediction",
    "layout": "wide",
    "page_icon": "🏥",
    "theme": {
        "primaryColor": "#e84545",
        "backgroundColor": "#f3f5fb",
        "secondaryBackgroundColor": "#ffffff",
        "textColor": "#1a1a2e",
        "font": "DM Sans",
    }
}

# Flask API configuration
API_CONFIG = {
    "DEBUG": True,
    "HOST": "0.0.0.0",
    "PORT": 5000,
    "CORS_ENABLED": True,
}

# Feature bounds for prediction form
FEATURE_CONFIG = {
    "step_precision": {
        "pressure_fields": 0.01,
        "rate_fields": 0.01,
        "temp_fields": 0.01,
        "default": 1.0,
    }
}

# Visualization configuration
VIZ_CONFIG = {
    "colors": {
        "primary": "#e84545",
        "secondary": "#4c6ef5",
        "success": "#22c58b",
        "warning": "#f59f00",
        "info": "#5a66f4",
    },
    "style": {
        "border_radius": "16px",
        "box_shadow": "0 4px 12px rgba(23, 31, 76, .06)",
    }
}

# Clinical thresholds
CLINICAL_CONFIG = {
    "confidence_threshold_default": 0.55,
    "confidence_threshold_min": 0.30,
    "confidence_threshold_max": 0.90,
}

# Logging configuration
LOGGING_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "log_file": PROJECT_ROOT / "logs" / "app.log",
}

# Export formats
EXPORT_CONFIG = {
    "supported_formats": ["csv", "json", "xlsx"],
    "default_format": "csv",
}
