"""
Utility functions for Breast Cancer Diagnosis System
"""

import pandas as pd
import numpy as np
import logging
from datetime import datetime
from pathlib import Path
import json

logger = logging.getLogger(__name__)


class DataProcessor:
    """Handle data processing operations"""
    
    @staticmethod
    def load_data(filepath):
        """Load CSV data"""
        try:
            df = pd.read_csv(filepath)
            logger.info(f"Data loaded successfully: {df.shape}")
            return df
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            raise
    
    @staticmethod
    def get_dataset_summary(df):
        """Get comprehensive dataset summary"""
        summary = {
            "rows": len(df),
            "columns": len(df.columns),
            "missing_values": df.isnull().sum().sum(),
            "missing_percent": (df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100,
            "memory_usage_mb": df.memory_usage(deep=True).sum() / 1024 / 1024,
            "dtypes": df.dtypes.value_counts().to_dict(),
        }
        return summary
    
    @staticmethod
    def get_column_stats(df, column):
        """Get statistics for a specific column"""
        if pd.api.types.is_numeric_dtype(df[column]):
            stats = {
                "type": "numeric",
                "min": float(df[column].min()),
                "max": float(df[column].max()),
                "mean": float(df[column].mean()),
                "median": float(df[column].median()),
                "std": float(df[column].std()),
                "missing": int(df[column].isnull().sum()),
            }
        else:
            stats = {
                "type": "categorical",
                "unique_values": int(df[column].nunique()),
                "most_common": str(df[column].value_counts().idxmax()),
                "missing": int(df[column].isnull().sum()),
            }
        return stats
    
    @staticmethod
    def handle_missing_values(df, strategy="drop"):
        """Handle missing values"""
        if strategy == "drop":
            df_clean = df.dropna()
        elif strategy == "mean":
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            df_clean = df.copy()
            df_clean[numeric_cols] = df_clean[numeric_cols].fillna(df_clean[numeric_cols].mean())
        else:
            df_clean = df.copy()
        
        logger.info(f"Missing values handled: {df.shape} -> {df_clean.shape}")
        return df_clean


class PredictionProcessor:
    """Handle prediction-related operations"""
    
    @staticmethod
    def prepare_input(patient_data, feature_columns):
        """Prepare patient input for prediction"""
        patient_df = pd.DataFrame([patient_data]).reindex(columns=feature_columns)
        return patient_df
    
    @staticmethod
    def format_prediction_result(prediction, confidence, probabilities, model_name):
        """Format prediction result"""
        result = {
            "prediction": prediction,
            "confidence": float(confidence),
            "confidence_percent": f"{float(confidence)*100:.1f}%",
            "probabilities": {k: f"{v*100:.2f}%" for k, v in probabilities.items()},
            "model": model_name,
            "timestamp": datetime.now().isoformat(),
            "status": "high_confidence" if confidence >= 0.55 else "low_confidence"
        }
        return result
    
    @staticmethod
    def create_prediction_record(patient_data, prediction_result):
        """Create a record for prediction history"""
        record = {**patient_data}
        record.update({
            "predicted_diagnosis": prediction_result["prediction"],
            "confidence": prediction_result["confidence"],
            "model": prediction_result["model"],
            "timestamp": prediction_result["timestamp"],
        })
        return record


class ExportHandler:
    """Handle data export operations"""
    
    @staticmethod
    def export_to_csv(data, filename):
        """Export data to CSV"""
        try:
            df = pd.DataFrame(data) if isinstance(data, list) else data
            df.to_csv(filename, index=False)
            logger.info(f"Data exported to {filename}")
            return True
        except Exception as e:
            logger.error(f"Export error: {e}")
            return False
    
    @staticmethod
    def export_to_json(data, filename):
        """Export data to JSON"""
        try:
            if isinstance(data, pd.DataFrame):
                data = data.to_dict(orient='records')
            
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2, default=str)
            logger.info(f"Data exported to {filename}")
            return True
        except Exception as e:
            logger.error(f"Export error: {e}")
            return False


class MetricsCalculator:
    """Calculate and format metrics"""
    
    @staticmethod
    def format_metrics(y_true, y_pred, y_proba=None):
        """Format comprehensive metrics"""
        from sklearn.metrics import (
            accuracy_score, precision_score, recall_score, f1_score,
            roc_auc_score, confusion_matrix
        )
        
        metrics = {
            "accuracy": accuracy_score(y_true, y_pred),
            "precision": precision_score(y_true, y_pred, average='weighted', zero_division=0),
            "recall": recall_score(y_true, y_pred, average='weighted', zero_division=0),
            "f1": f1_score(y_true, y_pred, average='weighted', zero_division=0),
        }
        
        if y_proba is not None:
            try:
                metrics["roc_auc"] = roc_auc_score(y_true, y_proba[:, 1]) if y_proba.shape[1] == 2 else None
            except:
                metrics["roc_auc"] = None
        
        return metrics
    
    @staticmethod
    def get_confusion_matrix(y_true, y_pred):
        """Get confusion matrix"""
        from sklearn.metrics import confusion_matrix
        cm = confusion_matrix(y_true, y_pred)
        return cm


class ValidationHelper:
    """Validate inputs and data"""
    
    @staticmethod
    def validate_patient_input(patient_data, feature_columns, bounds):
        """Validate patient input data"""
        errors = []
        
        for col, value in patient_data.items():
            if col not in feature_columns:
                errors.append(f"Unknown feature: {col}")
            elif col in bounds and isinstance(value, (int, float)):
                if value < bounds[col]["min"] or value > bounds[col]["max"]:
                    errors.append(f"{col} out of bounds: {bounds[col]['min']}-{bounds[col]['max']}")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def validate_file(filepath):
        """Validate file existence and format"""
        p = Path(filepath)
        if not p.exists():
            return False, "File does not exist"
        if not p.suffix == ".csv":
            return False, "File must be CSV"
        return True, "Valid"


class ReportGenerator:
    """Generate reports and summaries"""
    
    @staticmethod
    def generate_model_report(metrics_data, best_model):
        """Generate model performance report"""
        report = {
            "report_date": datetime.now().isoformat(),
            "best_model": best_model,
            "models": metrics_data,
            "summary": {
                "avg_accuracy": np.mean([m["accuracy"] for m in metrics_data.values()]),
                "avg_f1": np.mean([m["f1"] for m in metrics_data.values()]),
                "best_accuracy": max([m["accuracy"] for m in metrics_data.values()]),
                "best_f1": max([m["f1"] for m in metrics_data.values()]),
            }
        }
        return report
    
    @staticmethod
    def generate_prediction_summary(predictions):
        """Generate summary from predictions"""
        df = pd.DataFrame(predictions)
        summary = {
            "total_predictions": len(df),
            "unique_diagnoses": df["predicted_diagnosis"].nunique() if "predicted_diagnosis" in df.columns else 0,
            "avg_confidence": df["confidence"].mean() if "confidence" in df.columns else 0,
            "high_confidence_count": len(df[df["confidence"] >= 0.55]) if "confidence" in df.columns else 0,
        }
        return summary
