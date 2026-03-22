import socket
import hashlib

def get_network_profile():
    try:
        hostname = socket.gethostname()

        # Safer IP fetch (works better on Linux)
        try:
            ip_address = socket.gethostbyname(hostname)
        except:
            ip_address = "127.0.0.1"

        profile_string = f"{hostname}-{ip_address}"

        # Generate short unique ID
        profile_id = hashlib.md5(profile_string.encode()).hexdigest()[:8]

        return profile_id

    except Exception as e:
        print("⚠️ Device profiling failed:", e)
        return "unknown_profile"