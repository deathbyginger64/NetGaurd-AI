# =====================================================
# Suggestion Engine (Rule-Based Interpretation Layer)
# =====================================================

def classify_anomaly(features):
    """
    Classifies anomaly type based on traffic behavior.
    """

    packet_count = features["packet_count"]
    avg_size     = features["avg_packet_size"]
    unique_src   = features["unique_src_ips"]
    unique_dst   = features["unique_dst_ips"]

    # 🔥 Flooding Attack (realistic threshold)
    if packet_count > 100:
        return "Possible Flooding Attack"

    # 🔍 Network Scan
    if unique_dst > 10 and packet_count > 30:
        return "Possible Network Scan"

    # 📤 Data Exfiltration
    if avg_size > 700 and packet_count < 30:
        return "Possible Data Exfiltration"

    # ⚠️ Default
    return "Suspicious Burst Traffic"