"""
API Client for Breast Cancer Diagnosis System
Provides convenient methods to interact with the backend API
"""

import requests
import json
import logging
from typing import Dict, List, Any, Tuple

logger = logging.getLogger(__name__)


class APIClient:
    """Client for communicating with the Breast Cancer Diagnosis API"""
    
    def __init__(self, base_url: str = "http://localhost:5000"):
        """
        Initialize API client
        
        Args:
            base_url: Base URL of the API server
        """
        self.base_url = base_url
        self.session = requests.Session()
    
    def health_check(self) -> Dict[str, Any]:
        """Check API health status"""
        try:
            response = self.session.get(f"{self.base_url}/api/health")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return {"status": "error", "message": str(e)}
    
    def train_models(self) -> Dict[str, Any]:
        """Trigger model training"""
        try:
            response = self.session.post(f"{self.base_url}/api/train")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Training failed: {e}")
            return {"status": "error", "message": str(e)}
    
    def predict(self, patient_data: Dict[str, Any], model: str = "RandomForest") -> Dict[str, Any]:
        """
        Make a prediction
        
        Args:
            patient_data: Dictionary with patient features
            model: Model name to use (LogisticRegression, RandomForest, KNN)
        
        Returns:
            Prediction result
        """
        try:
            payload = {
                "model": model,
                "patient_data": patient_data
            }
            response = self.session.post(
                f"{self.base_url}/api/predict",
                json=payload
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Prediction failed: {e}")
            return {"status": "error", "message": str(e)}
    
    def batch_predict(self, patients_data: List[Dict], model: str = "RandomForest") -> Dict[str, Any]:
        """
        Make batch predictions
        
        Args:
            patients_data: List of patient data dictionaries
            model: Model name to use
        
        Returns:
            Batch prediction results
        """
        try:
            payload = {
                "model": model,
                "patients": patients_data
            }
            response = self.session.post(
                f"{self.base_url}/api/batch-predict",
                json=payload
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Batch prediction failed: {e}")
            return {"status": "error", "message": str(e)}
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get model metrics"""
        try:
            response = self.session.get(f"{self.base_url}/api/metrics")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to get metrics: {e}")
            return {"status": "error", "message": str(e)}
    
    def get_features(self) -> Dict[str, Any]:
        """Get feature information"""
        try:
            response = self.session.get(f"{self.base_url}/api/features")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to get features: {e}")
            return {"status": "error", "message": str(e)}
    
    def get_dataset_info(self) -> Dict[str, Any]:
        """Get dataset information"""
        try:
            response = self.session.get(f"{self.base_url}/api/dataset/info")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to get dataset info: {e}")
            return {"status": "error", "message": str(e)}
    
    def get_feature_importance(self) -> Dict[str, Any]:
        """Get feature importance scores"""
        try:
            response = self.session.get(f"{self.base_url}/api/feature-importance")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to get feature importance: {e}")
            return {"status": "error", "message": str(e)}


# Example usage
if __name__ == "__main__":
    # Initialize client
    client = APIClient()
    
    # Check health
    print("Checking API health...")
    health = client.health_check()
    print(json.dumps(health, indent=2))
    
    if health.get("status") == "healthy":
        # Train models
        print("\nTraining models...")
        training = client.train_models()
        print(f"Training status: {training.get('status')}")
        
        # Get features
        print("\nGetting features...")
        features = client.get_features()
        print(f"Available features: {len(features.get('features', []))} features")
        
        # Get metrics
        print("\nGetting metrics...")
        metrics = client.get_metrics()
        print(f"Best model: {metrics.get('best_model')}")
        
        # Example prediction
        sample_patient = {
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
        
        print("\nMaking prediction...")
        prediction = client.predict(sample_patient)
        print(json.dumps(prediction, indent=2))
    else:
        print("API is not healthy. Make sure the backend is running.")
