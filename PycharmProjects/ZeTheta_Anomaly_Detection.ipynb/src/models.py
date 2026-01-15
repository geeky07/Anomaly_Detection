import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import joblib  # <--- Added for saving/loading
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

    def predict_single(self, amount, location_score):
        """
        Predict for a single real-time transaction (API usage).
        """
        if not self.is_trained:
            raise Exception("Model is not trained!")

        # Preprocess single input
        input_data = [[amount, location_score]]
        X = self.scaler.transform(input_data)

        # Get score and prediction
        # Score: Lower is more anomalous.
        # Prediction: -1 is anomaly, 1 is normal.
        score = self.model.decision_function(X)[0]
        prediction = self.model.predict(X)[0]

        return {
            "is_anomaly": bool(prediction == -1),
            "anomaly_score": float(score),
            "risk_level": "HIGH" if score < -0.1 else "LOW"
        }