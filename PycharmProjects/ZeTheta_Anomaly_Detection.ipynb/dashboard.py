import streamlit as st
import pandas as pd
import sqlite3
import time
import plotly.express as px
from src.config import DB_PATH  # <--- Importing shared paths

st.set_page_config(page_title="ZeTheta Sentinel", layout="wide")


def load_data():
    """Fetch latest transactions from the SQLite DB."""
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query("SELECT * FROM transactions ORDER BY timestamp DESC LIMIT 100", conn)
        conn.close()
        return df
    except Exception as e:
        print(f"Database error: {e}")
        return pd.DataFrame()


# --- Dashboard UI ---
st.title("🛡️ ZeTheta Anomaly Detection Monitor")
st.text(f"Monitoring Database: {DB_PATH}")  # Debug info

placeholder = st.empty()

while True:
    df = load_data()

    with placeholder.container():
        if df.empty:
            st.warning("No transaction data found yet. Waiting for API traffic...")
            st.info("Tip: Run 'test_api.py' to generate traffic.")
        else:
            # Metrics
            total_txns = len(df)
            fraud_txns = df[df['is_anomaly'] == 1].shape[0]

            k1, k2 = st.columns(2)
            k1.metric("Transactions Monitored", total_txns)
            k2.metric("Anomalies Detected", fraud_txns, delta_color="inverse")

            # Alert Table
            st.subheader("🚨 Recent Activity")
            st.dataframe(df[['timestamp', 'id', 'amount', 'risk_score', 'is_anomaly']])

    time.sleep(2)