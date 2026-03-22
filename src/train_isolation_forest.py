import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib

DATASET = "data/processed/combined_features.csv"
MODEL_PATH = "models/isolation_forest.pkl"

# ---------------------------
# LOAD DATASET
# ---------------------------
df = pd.read_csv(DATASET)

# Drop non-feature columns
df_features = df.drop(columns=["time_sec", "source"])

print("Dataset shape:", df_features.shape)
print("Columns used for training:")
print(df_features.columns)

# ---------------------------
# TRAIN MODEL
# ---------------------------
model = IsolationForest(
    n_estimators=100,
    contamination=0.05,
    random_state=42,
    n_jobs=-1
)

model.fit(df_features)

# ---------------------------
# SAVE MODEL
# ---------------------------
joblib.dump(model, MODEL_PATH)

print("✅ Isolation Forest trained successfully")
print("📦 Model saved at:", MODEL_PATH)