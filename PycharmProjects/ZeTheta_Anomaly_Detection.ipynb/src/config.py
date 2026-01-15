import os

# Get the base directory of the project (one level up from 'src')
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Define absolute paths
DATA_DIR = os.path.join(BASE_DIR, 'data')
MODEL_PATH = os.path.join(DATA_DIR, 'model.pkl')
DB_PATH = os.path.join(DATA_DIR, 'transactions.db')

# Ensure the data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

print(f"--- CONFIGURATION ---")
print(f"Base Directory: {BASE_DIR}")
print(f"Database Path:  {DB_PATH}")