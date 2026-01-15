# ZeTheta Anomaly Detection System

A real-time market anomaly detection platform built for the ZeTheta 15-Day Challenge. This system identifies fraudulent transactions using unsupervised machine learning (Isolation Forest).

## 🚀 Features
- **Data Simulation**: Generates synthetic market transaction streams.
- **Detection Engine**: Isolation Forest model trained to spot unusual amounts and location patterns.
- **Live API**: FastAPI endpoint that processes transactions in <50ms.
- **Dashboard**: Real-time Streamlit monitor for alerts and analytics.

## 🛠️ Tech Stack
- **Core**: Python 3.9+
- **ML**: Scikit-learn, PyOD
- **API**: FastAPI, Uvicorn
- **Dashboard**: Streamlit, Plotly
- **Database**: SQLite

## ⚡ How to Run

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt