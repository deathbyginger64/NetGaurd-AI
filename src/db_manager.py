import sqlite3

DB_PATH = "netguard.db"

# -------------------------------------------------
# Persistent connection
# -------------------------------------------------
conn = sqlite3.connect(DB_PATH, check_same_thread=False)
cursor = conn.cursor()


# -------------------------------------------------
# INIT DATABASE (SAFE + MIGRATION READY)
# -------------------------------------------------
def init_db():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS anomaly_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            profile_id TEXT,
            packet_count INTEGER,
            avg_packet_size REAL,
            max_packet_size INTEGER,
            unique_src_ips INTEGER,
            unique_dst_ips INTEGER,
            anomaly_score REAL,
            label TEXT,
            alert_type TEXT,
            confidence TEXT
        )
    """)
    conn.commit()

    # Safe migration (if old DB exists without confidence column)
    try:
        cursor.execute("ALTER TABLE anomaly_logs ADD COLUMN confidence TEXT")
        conn.commit()
    except sqlite3.OperationalError:
        pass  # Column already exists


# -------------------------------------------------
# FAST INSERT
# -------------------------------------------------
def insert_log_fast(features, score, label, profile_id, timestamp, alert_type, confidence):
    try:
        cursor.execute("""
            INSERT INTO anomaly_logs (
                timestamp,
                profile_id,
                packet_count,
                avg_packet_size,
                max_packet_size,
                unique_src_ips,
                unique_dst_ips,
                anomaly_score,
                label,
                alert_type,
                confidence
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            timestamp,
            profile_id,
            features["packet_count"],
            features["avg_packet_size"],
            features["max_packet_size"],
            features["unique_src_ips"],
            features["unique_dst_ips"],
            score,
            label,
            alert_type,
            confidence
        ))
        conn.commit()

    except Exception as e:
        print("❌ DB Insert Error:", e)