import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random


def generate_market_data(num_records=1000):
    """
    Simulates market transactions with injected anomalies based on ZeTheta specs.
    """
    print(f"Generating {num_records} transactions...")

    # 1. Normal Pattern Generation
    data = {
        'transaction_id': [f'TXN_{i}' for i in range(num_records)],
        'user_id': [random.randint(1000, 1050) for _ in range(num_records)],  # 50 users
        'amount': np.random.normal(100, 20, num_records),  # Normal distrib around $100
        'timestamp': [datetime.now() - timedelta(minutes=i) for i in range(num_records)],
        'location_score': np.random.normal(0.1, 0.05, num_records)  # Low score = consistent location
    }

    df = pd.DataFrame(data)

    # 2. Inject "Point Anomalies" (Massive amounts) [cite: 496]
    # Fraudsters trying to drain accounts
    anomalies_idx = np.random.choice(df.index, size=int(num_records * 0.05))  # 5% fraud [cite: 268]
    df.loc[anomalies_idx, 'amount'] = np.random.uniform(5000, 50000, size=len(anomalies_idx))

    # 3. Inject "Contextual Anomalies" (High Velocity) [cite: 514]
    # Same user trading rapidly
    burst_user = 1001
    for i in range(10):
        df.loc[len(df)] = [f'FRAUD_BURST_{i}', burst_user, 150, datetime.now(), 0.9]

    print("Data generation complete.")
    return df


if __name__ == "__main__":
    df = generate_market_data()
    # Save to simulate "Data Collection" [cite: 58]
    df.to_csv('../data/market_data.csv', index=False)
    print("Saved to data/market_data.csv")