import pandas as pd
import os

# Ensure output folder exists
os.makedirs("data/processed", exist_ok=True)

RAW_DIR = "data/raw"
OUTPUT_FILE = "data/processed/features_output.csv"


# -------------------------------------------------
# FIND LATEST RAW FILE (🔥 DYNAMIC)
# -------------------------------------------------
if not os.path.exists(RAW_DIR):
    print("❌ data/raw folder not found")
    exit()

files = [f for f in os.listdir(RAW_DIR) if f.endswith(".csv")]

if not files:
    print("❌ No raw files found in data/raw/")
    exit()

latest_file = max(files, key=lambda x: os.path.getctime(os.path.join(RAW_DIR, x)))
RAW_FILE = os.path.join(RAW_DIR, latest_file)

print("📂 Using latest file:", RAW_FILE)


# -------------------------------------------------
# LOAD DATA
# -------------------------------------------------
df = pd.read_csv(RAW_FILE)

if df.empty:
    print("❌ Raw dataset is empty")
    exit()

print("📊 Raw data shape:", df.shape)


# -------------------------------------------------
# TIME NORMALIZATION
# -------------------------------------------------
df["time_sec"] = df["timestamp"].astype(int)


# -------------------------------------------------
# FEATURE EXTRACTION
# -------------------------------------------------
features = df.groupby("time_sec").agg(
    packet_count=("packet_size", "count"),
    avg_packet_size=("packet_size", "mean"),
    max_packet_size=("packet_size", "max"),
    unique_src_ips=("src_ip", "nunique"),
    unique_dst_ips=("dst_ip", "nunique"),
)


# -------------------------------------------------
# SAVE FEATURES
# -------------------------------------------------
features.to_csv(OUTPUT_FILE)

print("\n✅ Feature extraction complete")
print("📁 Saved to:", OUTPUT_FILE)
print("\nSample:")
print(features.head())