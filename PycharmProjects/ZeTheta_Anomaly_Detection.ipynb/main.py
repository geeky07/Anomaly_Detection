import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import joblib
import os


class AnomalyDetector:
    def __init__(self, contamination=0.05, model_path='model.pkl'):
        self.model_path = model_path
        self.model = IsolationForest(
            n_estimators=100,
            max_samples='auto',
            contamination=contamination,
            random_state=42
        )
        self.scaler = StandardScaler()
        self.is_trained = False

    def train(self, df):
        """Train the model and save it."""
        print("Training Isolation Forest model...")
        features = df[['amount', 'location_score']]

        # Fit scaler and model
        X = self.scaler.fit_transform(features)
        self.model.fit(X)
        self.is_trained = True

        # Save both model and scaler
        joblib.dump({'model': self.model, 'scaler': self.scaler}, self.model_path)
        print(f"Model saved to {self.model_path}")

    def load(self):
        """Load a pre-trained model from disk."""
        if os.path.exists(self.model_path):
            data = joblib.load(self.model_path)
            self.model = data['model']
            self.scaler = data['scaler']
            self.is_trained = True
            print("Model loaded successfully.")
        else:
            print("No saved model found. Please train first.")

    def predict(self, df):
        """
        Batch prediction for multiple records (Used in main.py pipeline).
        """
        if not self.is_trained:
            # Try to load if not explicitly trained in this session
            if os.path.exists(self.model_path):
                self.load()
            else:
                raise Exception("Model is not trained and no saved model found!")

        features = df[['amount', 'location_score']]
        X = self.scaler.transform(features)

        # -1 for outliers, 1 for inliers
        df['anomaly_prediction'] = self.model.predict(X)

        # Anomaly score (lower is more anomalous)
        df['anomaly_score'] = self.model.decision_function(X)

        return df

    def predict_single(self, amount, location_score):
        """
        Real-time prediction for a single transaction (Used in FastAPI).
        """
        if not self.is_trained:
            self.load()  # Auto-load if needed

        # Preprocess single input (reshape for sklearn)
        input_data = [[amount, location_score]]
        X = self.scaler.transform(input_data)

        score = self.model.decision_function(X)[0]
        prediction = self.model.predict(X)[0]

        return {
            "is_anomaly": bool(prediction == -1),
            "anomaly_score": float(score),
            "risk_level": "HIGH" if score < -0.1 else "LOW"
        }