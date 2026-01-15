# train_once.py
from src.data_gen import generate_market_data
from src.models import AnomalyDetector

# 1. Generate Data
df = generate_market_data(num_records=5000)

# 2. Train and Save
detector = AnomalyDetector(model_path='../data/model.pkl') # Save in data folder
detector.train(df)

print("Setup complete. You are ready to launch the API.")