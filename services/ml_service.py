import joblib
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "..", "model", "model.pkl")

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model not found at {MODEL_PATH}")

# ✅ Use joblib instead of pickle
model = joblib.load(MODEL_PATH)

def predict_student(features):
    """
    features: list[int]
    returns: float
    """
    return float(model.predict([features])[0])
