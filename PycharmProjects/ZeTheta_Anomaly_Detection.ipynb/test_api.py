import requests
import json
import time

# The URL of your running API
API_URL = "http://127.0.0.1:8000/detect"


def run_simulation():
    print(f"--- 🚀 Starting Live Traffic Simulation ---")
    print(f"Targeting System: {API_URL}\n")

    # Scenario 1: legitimate User
    # Small amount ($100), consistent location (0.1 score)
    normal_txn = {
        "transaction_id": "TXN_SAFE_001",
        "user_id": 105,
        "amount": 100.00,
        "location_score": 0.1
    }

    # Scenario 2: Fraud Attack
    # Massive amount ($50,000), suspicious location (0.95 score)
    fraud_txn = {
        "transaction_id": "TXN_ATTACK_999",
        "user_id": 666,
        "amount": 50000.00,
        "location_score": 0.95
    }

    transactions = [normal_txn, fraud_txn]

    for txn in transactions:
        print(f"Processing Transaction: {txn['transaction_id']}...")
        print(f"   Amount: ${txn['amount']} | Location Score: {txn['location_score']}")

        try:
            # Send POST request to your API
            response = requests.post(API_URL, json=txn)

            if response.status_code == 200:
                result = response.json()

                # Check the decision
                if result['action'] == "BLOCK":
                    print(f"   ❌ SYSTEM DECISION: BLOCKED (Anomaly Detected!)")
                    print(f"   ⚠️  Risk Score: {result['risk_score']}")
                else:
                    print(f"   ✅ SYSTEM DECISION: ALLOWED")
            else:
                print(f"   Error: API returned status {response.status_code}")
                print(response.text)

        except requests.exceptions.ConnectionError:
            print("   ❌ CONNECTION ERROR: Is api/main.py running?")

        print("-" * 40)
        time.sleep(1)  # Pause for effect


if __name__ == "__main__":
    run_simulation()