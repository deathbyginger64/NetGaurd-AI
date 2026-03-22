from scapy.all import sniff, IP
import csv
import time
import os

# Ensure folder exists
os.makedirs("data/raw", exist_ok=True)

# 🔥 Dynamic file name (no overwrite)
OUTPUT_FILE = f"data/raw/capture_{int(time.time())}.csv"

CAPTURE_DURATION = 300  # seconds

packets_data = []


def process_packet(packet):
    if IP in packet:
        ip_layer = packet[IP]

        packet_info = {
            "timestamp": time.time(),
            "src_ip": ip_layer.src,
            "dst_ip": ip_layer.dst,
            "protocol": ip_layer.proto,
            "packet_size": len(packet)
        }

        packets_data.append(packet_info)


def start_capture():
    print(f"[+] Capturing packets for {CAPTURE_DURATION} seconds...")

    sniff(
        prn=process_packet,
        store=False,
        timeout=CAPTURE_DURATION,
        iface="wlan0"   # change to eth0 if needed
    )

    print("[+] Capture completed.")
    save_to_csv()


def save_to_csv():
    if len(packets_data) == 0:
        print("⚠️ No packets captured.")
        return

    with open(OUTPUT_FILE, "w", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["timestamp", "src_ip", "dst_ip", "protocol", "packet_size"]
        )
        writer.writeheader()
        writer.writerows(packets_data)

    print(f"[+] Saved {len(packets_data)} packets to CSV.")
    print(f"📁 File: {OUTPUT_FILE}")


if __name__ == "__main__":
    start_capture()