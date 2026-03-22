import pandas as pd
import os

FEATURE_DIR = "data/processed"
OUTPUT_FILE = "data/processed/combined_features.csv"


# -------------------------------------------------
# CHECK DIRECTORY
# -------------------------------------------------
if not os.path.exists(FEATURE_DIR):
    print("❌ data/processed folder not found")
    exit()


# -------------------------------------------------
# FIND FEATURE FILES
# -------------------------------------------------
files = [
    os.path.join(FEATURE_DIR, f)
    for f in os.listdir(FEATURE_DIR)
    if f.endswith(".csv") and f != "combined_features.csv"
]

if len(files) == 0:
    print("❌ No feature files found to merge")
    exit()


print("📂 Found feature files:")
for f in files:
    print(" -", f)


# -------------------------------------------------
# LOAD + TAG DATA
# -------------------------------------------------
df_list = []

for file in files:
    try:
        df = pd.read_csv(file)

        if df.empty:
            print(f"⚠️ Skipping empty file: {file}")
            continue

        # Add source column
        source_name = os.path.basename(file)
        df["source"] = source_name

        df_list.append(df)

    except Exception as e:
        print(f"❌ Error reading {file}: {e}")


if len(df_list) == 0:
    print("❌ No valid data to merge")
    exit()


# -------------------------------------------------
# COMBINE + SHUFFLE
# -------------------------------------------------
combined_df = pd.concat(df_list, ignore_index=True)

combined_df = combined_df.sample(frac=1, random_state=42).reset_index(drop=True)


# -------------------------------------------------
# SAVE
# -------------------------------------------------
combined_df.to_csv(OUTPUT_FILE, index=False)

print("\n✅ Combined dataset created successfully")
print("📁 Saved to:", OUTPUT_FILE)
print("📊 Shape:", combined_df.shape)
print("\nSample:")
print(combined_df.head())