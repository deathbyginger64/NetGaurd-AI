import time
import pandas as pd
import joblib
from scapy.all import sniff, IP

from device_profiler import get_network_profile
from db_manager import init_db, insert_log_fast
from suggestion_engine import classify_anomaly


# =====================================================
# LOAD MODELS
# =====================================================

ISO_MODEL_PATH = "models/isolation_forest.pkl"
SVM_MODEL_PATH = "models/ocsvm_model.pkl"
SCALER_PATH    = "models/ocsvm_scaler.pkl"

iso_model  = joblib.load(ISO_MODEL_PATH)
svm_model  = joblib.load(SVM_MODEL_PATH)
svm_scaler = joblib.load(SCALER_PATH)

print("✅ Isolation Forest model loaded")
print("✅ One-Class SVM model loaded")
print("✅ SVM scaler loaded")


# =====================================================
# INIT DATABASE
# =====================================================

init_db()
print("🗄️ Database initialized")


# =====================================================
# NETWORK PROFILE
# =====================================================

profile_id = get_network_profile()
print("📡 Active Network Profile ID:", profile_id)
print("🚨 Live IDS started. Press CTRL + C to stop.\n")


# =====================================================
# PACKET BUFFER
# =====================================================

packet_buffer = []

def capture_packet(packet):
    if IP in packet:
        packet_buffer.append({
            "src_ip": packet[IP].src,
            "dst_ip": packet[IP].dst,
            "size":   len(packet)
        })


# =====================================================
# CONFIG
# =====================================================

IF_SCORE_THRESHOLD = -0.1


# =====================================================
# LIVE LOOP
# =====================================================

running = True

while running:
    try:

        packet_buffer.clear()
        window_start = time.time()

        sniff(
            prn=capture_packet,
            timeout=1,
            store=False,
            filter="ip"
        )

        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(window_start))

        # =================================================
        # NO TRAFFIC
        # =================================================

        if len(packet_buffer) == 0:

            features = {
                "packet_count": 0,
                "avg_packet_size": 0.0,
                "max_packet_size": 0,
                "unique_src_ips": 0,
                "unique_dst_ips": 0
            }

            print(f"🟢 No traffic detected at {timestamp}")

            insert_log_fast(
                features=features,
                score=0.0,
                label="Normal",
                profile_id=profile_id,
                timestamp=timestamp,
                alert_type="None",
                confidence="LOW"
            )

            continue

        # =================================================
        # FEATURE EXTRACTION
        # =================================================

        df = pd.DataFrame(packet_buffer)

        features = {
            "packet_count": int(len(df)),
            "avg_packet_size": float(df["size"].mean()),
            "max_packet_size": int(df["size"].max()),
            "unique_src_ips": int(df["src_ip"].nunique()),
            "unique_dst_ips": int(df["dst_ip"].nunique())
        }

        feature_df = pd.DataFrame([features])

        # =================================================
        # MODEL PREDICTIONS
        # =================================================

        iso_pred  = iso_model.predict(feature_df)[0]
        iso_score = float(iso_model.decision_function(feature_df)[0])

        scaled_features = svm_scaler.transform(feature_df)
        svm_pred = svm_model.predict(scaled_features)[0]

        # =================================================
        # RULE FLAGS
        # =================================================

        rule_flag = False

        if features["packet_count"] > 30:
            rule_flag = True

        if features["unique_src_ips"] > 10:
            rule_flag = True

        # =================================================
        # HYBRID LOGIC
        # =================================================

        if iso_pred == -1 and svm_pred == -1 and iso_score < IF_SCORE_THRESHOLD:
            prediction = -1
            confidence = "HIGH"
            score      = iso_score

        elif iso_pred == -1 and svm_pred == -1:
            prediction = -1
            confidence = "MEDIUM"
            score      = iso_score

        elif rule_flag:
            prediction = -1
            confidence = "HIGH"
            score      = iso_score

        elif iso_pred == -1 or svm_pred == -1:
            prediction = -1
            confidence = "MEDIUM"
            score      = iso_score

        else:
            prediction = 1
            confidence = "LOW"
            score      = iso_score

        # =================================================
        # DECISION
        # =================================================

        if prediction == -1:

            label      = "Anomaly"
            alert_type = classify_anomaly(features)

            print("\n🚨 ANOMALY DETECTED")
            print(f"🕒 Time       : {timestamp}")
            print(f"⚠️ Alert Type  : {alert_type}")
            print(f"📉 IF Score    : {round(iso_score, 4)}")
            print(f"⚡ Confidence  : {confidence}")
            print(f"🔎 Model Votes : IF={iso_pred} | SVM={svm_pred}")
            print(feature_df.to_string(index=False))
            print()

        else:

            label      = "Normal"
            alert_type = "None"

            print(
                f"🟢 Normal {timestamp} | "
                f"IF={round(iso_score,4)} | SVM={svm_pred} | conf={confidence}"
            )

        # =================================================
        # SAVE
        # =================================================

        insert_log_fast(
            features=features,
            score=score,
            label=label,
            profile_id=profile_id,
            timestamp=timestamp,
            alert_type=alert_type,
            confidence=confidence
        )

    except KeyboardInterrupt:
        print("\n🛑 IDS stopped by user")
        running = False