import os
from src.data_gen import generate_market_data
from src.models import AnomalyDetector


def force_train_model():
    print("--- 🛠️ FIXING MODEL PATH ---")

    # 1. Define the correct path inside the 'data' folder
    # This ensures the file is exactly where the API looks for it
    base_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(base_dir, 'data', 'model.pkl')

    print(f"Target path: {model_path}")

    # 2. Generate training data
    print("Generating training data...")
    df = generate_market_data(num_records=5000)

    # 3. Initialize detector with the EXPLICIT path
    detector = AnomalyDetector(model_path=model_path)

    # 4. Train and Save
    detector.train(df)
    print("✅ Model successfully saved to data/model.pkl")


if __name__ == "__main__":
    force_train_model()