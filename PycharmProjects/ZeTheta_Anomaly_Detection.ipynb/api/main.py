import sqlite3
import time
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.models import AnomalyDetector
from src.config import MODEL_PATH, DB_PATH  # <--- Importing shared paths
import uvicorn
import os


# --- Database Setup ---
def init_db():
    print(f"Initializing Database at: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS transactions
                 (id TEXT PRIMARY KEY, user_id INT, amount REAL, 
                  location_score REAL, is_anomaly BOOLEAN, 
                  risk_score REAL, timestamp REAL)''')
    conn.commit()
    conn.close()


def log_transaction(txn_data):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("INSERT INTO transactions VALUES (?,?,?,?,?,?,?)",
                  (txn_data['transaction_id'], txn_data['user_id'],
                   txn_data['amount'], txn_data['location_score'],
                   txn_data['is_anomaly'], txn_data['risk_score'],
                   txn_data['timestamp']))
        conn.commit()
        conn.close()
        print(f"Logged transaction {txn_data['transaction_id']} to DB")
    except Exception as e:
        print(f"FAILED to log transaction: {e}")


# --- App Setup ---
app = FastAPI(title="ZeTheta Anomaly Detection System")

# Initialize Model
detector = AnomalyDetector(model_path=MODEL_PATH)


@app.on_event("startup")
def startup_event():
    init_db()
    if os.path.exists(MODEL_PATH):
        detector.load()
    else:
        print(f"WARNING: Model not found at {MODEL_PATH}")


class Transaction(BaseModel):
    transaction_id: str
    user_id: int
    amount: float
    location_score: float


@app.get("/")
def health_check():
    return {"status": "active"}


@app.post("/detect")
def detect_anomaly(txn: Transaction):
    try:
        # 1. Detect
        result = detector.predict_single(txn.amount, txn.location_score)

        # 2. Log
        log_data = {
            "transaction_id": txn.transaction_id,
            "user_id": txn.user_id,
            "amount": txn.amount,
            "location_score": txn.location_score,
            "is_anomaly": result['is_anomaly'],
            "risk_score": float(result['anomaly_score']),
            "timestamp": time.time()
        }
        log_transaction(log_data)

        # 3. Respond
        return {
            "transaction_id": txn.transaction_id,
            "action": "BLOCK" if result['is_anomaly'] else "ALLOW",
            "risk_score": result['anomaly_score']
        }
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)