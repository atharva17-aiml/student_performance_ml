import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
import joblib
import os
from datetime import datetime

# ---------------- CONFIG ----------------
DATA_PATH = "dataset/student_data.csv"
MODEL_DIR = "model"
MODEL_PATH = os.path.join(MODEL_DIR, "model.pkl")
META_PATH = os.path.join(MODEL_DIR, "metadata.pkl")

FEATURES = ['studytime', 'failures', 'absences', 'health', 'G1', 'G2']
TARGET = 'G3'

os.makedirs(MODEL_DIR, exist_ok=True)

# ---------------- LOAD DATA ----------------
data = pd.read_csv(DATA_PATH)

X = data[FEATURES]
y = data[TARGET]

# ---------------- TRAIN/TEST SPLIT ----------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ---------------- MODELS ----------------
pipelines = {
    "LinearRegression": Pipeline([
        ("scaler", StandardScaler()),
        ("model", LinearRegression())
    ]),
    "RandomForest": Pipeline([
        ("scaler", StandardScaler()),
        ("model", RandomForestRegressor(n_estimators=300, random_state=42, n_jobs=-1))
    ])
}

results = {}

# ---------------- TRAIN + CV ----------------
best_model = None
best_r2 = -1

for name, pipe in pipelines.items():
    cv_scores = cross_val_score(pipe, X_train, y_train, cv=5, scoring="r2")

    pipe.fit(X_train, y_train)
    preds = pipe.predict(X_test)

    r2 = r2_score(y_test, preds)
    mae = mean_absolute_error(y_test, preds)

    results[name] = {
        "cv_r2_mean": float(cv_scores.mean()),
        "test_r2": float(r2),
        "mae": float(mae)
    }

    if r2 > best_r2:
        best_r2 = r2
        best_model = pipe

# ---------------- SAVE MODEL ----------------
joblib.dump(best_model, MODEL_PATH)

# ---------------- SAVE METADATA ----------------
metadata = {
    "trained_at": datetime.now().isoformat(),
    "features": FEATURES,
    "target": TARGET,
    "metrics": results,
    "best_test_r2": best_r2
}

joblib.dump(metadata, META_PATH)

# ---------------- OUTPUT ----------------
print("✅ Best model saved to:", MODEL_PATH)
print("📊 Metrics:")
for model_name, m in results.items():
    print(f"  {model_name}: CV R2={m['cv_r2_mean']:.3f}, Test R2={m['test_r2']:.3f}, MAE={m['mae']:.3f}")
