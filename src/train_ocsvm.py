import pandas as pd
import joblib

from sklearn.svm import OneClassSVM
from sklearn.preprocessing import StandardScaler


# =====================================================
# LOAD DATASET
# =====================================================

DATA_PATH = "data/processed/combined_features.csv"

df = pd.read_csv(DATA_PATH)

print("Dataset shape:", df.shape)


# =====================================================
# SELECT FEATURES
# =====================================================

features = [
    "packet_count",
    "avg_packet_size",
    "max_packet_size",
    "unique_src_ips",
    "unique_dst_ips"
]

X = df[features]


# =====================================================
# FEATURE SCALING
# =====================================================

scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)


# =====================================================
# TRAIN ONE-CLASS SVM
# =====================================================

svm_model = OneClassSVM(
    kernel="rbf",
    gamma="auto",
    nu=0.05
)

svm_model.fit(X_scaled)


# =====================================================
# SAVE MODEL + SCALER
# =====================================================

joblib.dump(svm_model, "models/ocsvm_model.pkl")
joblib.dump(scaler, "models/ocsvm_scaler.pkl")

print("✅ One-Class SVM trained successfully")
print("📦 Model saved at: models/ocsvm_model.pkl")
print("📦 Scaler saved at: models/ocsvm_scaler.pkl")