"""
Backend API for Breast Cancer Diagnosis System
Provides REST endpoints for model training, predictions, and analytics
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
import pickle
import json
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score, f1_score, classification_report, confusion_matrix
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Global variables for model state
models = {}
scaler = None
encoders = {}
target_le = None
feature_columns = []
categorical_map = {}
numerical_bounds = {}
metrics_data = {}

# Configuration
CONFIG = {
    "DATA_PATH": "Breast_Cancer.csv",
    "TARGET_COL": "Status",
    "DROP_COLS": [],
    "RANDOM_STATE": 42,
    "TEST_SIZE": 0.2
}


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "models_loaded": len(models) > 0
    })


@app.route('/api/train', methods=['POST'])
def train_models():
    """Train all models on the dataset"""
    try:
        global models, scaler, encoders, target_le, feature_columns, categorical_map, numerical_bounds, metrics_data
        
        logger.info("Starting model training...")
        
        # Load data
        df = pd.read_csv(CONFIG["DATA_PATH"])
        logger.info(f"Dataset loaded: {df.shape}")
        
        # Prepare data
        d = df.drop(columns=CONFIG["DROP_COLS"], errors='ignore').copy()
        X = d.drop(columns=[CONFIG["TARGET_COL"]]).copy()
        y_text = d[CONFIG["TARGET_COL"]].copy()
        
        feature_columns = X.columns.tolist()
        
        # Handle categorical variables
        cat_cols = X.select_dtypes(include=["object"]).columns.tolist()
        encoders = {}
        categorical_map = {}
        
        for col in cat_cols:
            le = LabelEncoder()
            X[col] = le.fit_transform(X[col].astype(str))
            encoders[col] = le
            categorical_map[col] = le.classes_.tolist()
        
        # Encode target
        target_le = LabelEncoder()
        y = target_le.fit_transform(y_text)
        
        # Train-test split
        X_tr, X_te, y_tr, y_te = train_test_split(
            X, y, test_size=CONFIG["TEST_SIZE"],
            random_state=CONFIG["RANDOM_STATE"], stratify=y
        )
        
        # Scale features
        scaler = StandardScaler()
        X_tr_s = scaler.fit_transform(X_tr)
        X_te_s = scaler.transform(X_te)
        
        logger.info("Features scaled and split")
        
        # Train models
        models = {}
        metrics_data = {}
        
        # Logistic Regression
        lr = LogisticRegression(max_iter=1000, random_state=CONFIG["RANDOM_STATE"])
        lr.fit(X_tr_s, y_tr)
        lr_pred = lr.predict(X_te_s)
        models["LogisticRegression"] = lr
        metrics_data["LogisticRegression"] = {
            "accuracy": float(accuracy_score(y_te, lr_pred) * 100),
            "f1": float(f1_score(y_te, lr_pred, average="macro") * 100),
            "classification_report": classification_report(y_te, lr_pred, output_dict=True)
        }
        logger.info(f"Logistic Regression - Accuracy: {metrics_data['LogisticRegression']['accuracy']:.2f}%")
        
        # Random Forest with GridSearch
        gs = GridSearchCV(
            RandomForestClassifier(random_state=CONFIG["RANDOM_STATE"]),
            {"n_estimators": [100, 200], "max_depth": [None, 10]},
            cv=3, scoring="f1_macro", n_jobs=-1
        )
        gs.fit(X_tr_s, y_tr)
        rf = gs.best_estimator_
        rf_pred = rf.predict(X_te_s)
        models["RandomForest"] = rf
        metrics_data["RandomForest"] = {
            "accuracy": float(accuracy_score(y_te, rf_pred) * 100),
            "f1": float(f1_score(y_te, rf_pred, average="macro") * 100),
            "classification_report": classification_report(y_te, rf_pred, output_dict=True),
            "best_params": gs.best_params_
        }
        logger.info(f"Random Forest - Accuracy: {metrics_data['RandomForest']['accuracy']:.2f}%")
        
        # KNN
        knn = KNeighborsClassifier(n_neighbors=5)
        knn.fit(X_tr_s, y_tr)
        knn_pred = knn.predict(X_te_s)
        models["KNN"] = knn
        metrics_data["KNN"] = {
            "accuracy": float(accuracy_score(y_te, knn_pred) * 100),
            "f1": float(f1_score(y_te, knn_pred, average="macro") * 100),
            "classification_report": classification_report(y_te, knn_pred, output_dict=True)
        }
        logger.info(f"KNN - Accuracy: {metrics_data['KNN']['accuracy']:.2f}%")
        
        # Store numerical bounds
        numerical_bounds = {}
        for col in X.columns:
            if col not in categorical_map:
                numerical_bounds[col] = {
                    "min": float(X[col].min()),
                    "max": float(X[col].max()),
                    "mean": float(X[col].mean())
                }
        
        return jsonify({
            "status": "success",
            "message": "Models trained successfully",
            "models": list(models.keys()),
            "metrics": metrics_data,
            "features": feature_columns,
            "dataset_size": len(df)
        })
    
    except Exception as e:
        logger.error(f"Training error: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/predict', methods=['POST'])
def predict():
    """Make predictions on patient data"""
    try:
        data = request.get_json()
        model_name = data.get("model", "RandomForest")
        patient_data = data.get("patient_data", {})
        
        if model_name not in models:
            return jsonify({"status": "error", "message": f"Model {model_name} not found"}), 400
        
        # Prepare patient data
        patient_df = pd.DataFrame([patient_data]).reindex(columns=feature_columns)
        
        # Encode categorical features
        enc = patient_df.copy()
        for col, le in encoders.items():
            enc[col] = le.transform(enc[col].astype(str))
        
        # Scale features
        scaled = scaler.transform(enc)
        
        # Make prediction
        model = models[model_name]
        pred_idx = int(model.predict(scaled)[0])
        pred_label = target_le.inverse_transform([pred_idx])[0]
        proba = model.predict_proba(scaled)[0]
        
        # Get class probabilities
        proba_dict = {
            cls: float(prob)
            for cls, prob in zip(target_le.classes_, proba)
        }
        
        return jsonify({
            "status": "success",
            "prediction": pred_label,
            "confidence": float(proba.max()),
            "probabilities": proba_dict,
            "model": model_name,
            "timestamp": datetime.now().isoformat()
        })
    
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/metrics', methods=['GET'])
def get_metrics():
    """Get model metrics"""
    if not metrics_data:
        return jsonify({"status": "error", "message": "Models not trained yet"}), 400
    
    return jsonify({
        "status": "success",
        "metrics": metrics_data,
        "best_model": max(metrics_data, key=lambda m: metrics_data[m]["f1"])
    })


@app.route('/api/features', methods=['GET'])
def get_features():
    """Get feature information"""
    if not feature_columns:
        return jsonify({"status": "error", "message": "Models not trained yet"}), 400
    
    return jsonify({
        "status": "success",
        "features": feature_columns,
        "categorical": categorical_map,
        "numerical": numerical_bounds
    })


@app.route('/api/dataset/info', methods=['GET'])
def dataset_info():
    """Get dataset information"""
    try:
        df = pd.read_csv(CONFIG["DATA_PATH"])
        
        return jsonify({
            "status": "success",
            "rows": len(df),
            "columns": len(df.columns),
            "missing_values": int(df.isnull().sum().sum()),
            "column_info": {
                col: {
                    "type": str(df[col].dtype),
                    "unique": int(df[col].nunique()),
                    "missing": int(df[col].isnull().sum())
                }
                for col in df.columns
            },
            "target_distribution": df[CONFIG["TARGET_COL"]].value_counts().to_dict()
        })
    
    except Exception as e:
        logger.error(f"Dataset info error: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/feature-importance', methods=['GET'])
def feature_importance():
    """Get feature importance from Random Forest"""
    try:
        if "RandomForest" not in models:
            return jsonify({"status": "error", "message": "Random Forest model not available"}), 400
        
        rf = models["RandomForest"]
        importance = sorted(
            zip(feature_columns, rf.feature_importances_),
            key=lambda x: -x[1]
        )
        
        return jsonify({
            "status": "success",
            "importance": [
                {"feature": feat, "score": float(score)}
                for feat, score in importance
            ]
        })
    
    except Exception as e:
        logger.error(f"Feature importance error: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/batch-predict', methods=['POST'])
def batch_predict():
    """Batch prediction for multiple patients"""
    try:
        data = request.get_json()
        model_name = data.get("model", "RandomForest")
        patients_data = data.get("patients", [])
        
        if model_name not in models:
            return jsonify({"status": "error", "message": f"Model {model_name} not found"}), 400
        
        results = []
        for patient_data in patients_data:
            # Prepare patient data
            patient_df = pd.DataFrame([patient_data]).reindex(columns=feature_columns)
            
            # Encode categorical features
            enc = patient_df.copy()
            for col, le in encoders.items():
                enc[col] = le.transform(enc[col].astype(str))
            
            # Scale features
            scaled = scaler.transform(enc)
            
            # Make prediction
            model = models[model_name]
            pred_idx = int(model.predict(scaled)[0])
            pred_label = target_le.inverse_transform([pred_idx])[0]
            proba = model.predict_proba(scaled)[0]
            
            results.append({
                "prediction": pred_label,
                "confidence": float(proba.max()),
                "timestamp": datetime.now().isoformat()
            })
        
        return jsonify({
            "status": "success",
            "predictions_count": len(results),
            "predictions": results
        })
    
    except Exception as e:
        logger.error(f"Batch prediction error: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == '__main__':
    logger.info("Starting Breast Cancer Diagnosis API Server")
    app.run(debug=True, host='0.0.0.0', port=5000)
