<div align="center">

<br/>

```
███╗   ██╗███████╗████████╗ ██████╗ ██╗   ██╗ █████╗ ██████╗ ██████╗      █████╗ ██╗
████╗  ██║██╔════╝╚══██╔══╝██╔════╝ ██║   ██║██╔══██╗██╔══██╗██╔══██╗    ██╔══██╗██║
██╔██╗ ██║█████╗     ██║   ██║  ███╗██║   ██║███████║██████╔╝██║  ██║    ███████║██║
██║╚██╗██║██╔══╝     ██║   ██║   ██║██║   ██║██╔══██║██╔══██╗██║  ██║    ██╔══██║██║
██║ ╚████║███████╗   ██║   ╚██████╔╝╚██████╔╝██║  ██║██║  ██║██████╔╝    ██║  ██║██║
╚═╝  ╚═══╝╚══════╝   ╚═╝    ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝     ╚═╝  ╚═╝╚═╝
```

<br/>

**Hybrid Machine Learning · Network Intrusion Detection · Real-Time SOC Dashboard**

> Built as a real-time SOC simulation system for cybersecurity research and education

<br/>

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Scikit-learn](https://img.shields.io/badge/Scikit--learn-ML%20Engine-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-SOC%20Dashboard-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Scapy](https://img.shields.io/badge/Scapy-Packet%20Capture-009688?style=for-the-badge)](https://scapy.net)
[![SQLite](https://img.shields.io/badge/SQLite-Event%20Logging-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://sqlite.org)

<br/>

[![Status](https://img.shields.io/badge/Status-Active-success?style=flat-square)]()
[![Type](https://img.shields.io/badge/Type-Research%20Project-blue?style=flat-square)]()
[![Domain](https://img.shields.io/badge/Domain-Cybersecurity%20%2F%20ML-purple?style=flat-square)]()
[![License](https://img.shields.io/badge/License-Educational-lightgrey?style=flat-square)]()

<br/>

</div>

---

## 📌 What is NetGuard AI?

**NetGuard AI** is a real-time, AI-powered Network Intrusion Detection System (IDS) that monitors live network traffic, detects anomalies using a hybrid machine learning engine, and presents threats through a professional Security Operations Center (SOC) dashboard.

Unlike traditional signature-based IDS tools, NetGuard AI uses **unsupervised machine learning** — it learns what normal traffic looks like on your own network and automatically flags deviations, without requiring a labelled attack dataset.

<br/>

```
  📡 Live Traffic  →  🧠 Hybrid ML  →  ⚡ Confidence Score  →  📊 SOC Dashboard
```

<br/>

---

## ✨ Key Features

<br/>

| # | Feature | Description |
|---|---|---|
| 01 | 📡 **Live Packet Capture** | Real-time traffic sniffing via Scapy on configurable network interface |
| 02 | 🧠 **Hybrid ML Detection** | Isolation Forest + One-Class SVM working in parallel |
| 03 | ⚡ **3-Tier Confidence Scoring** | HIGH / MEDIUM / LOW based on dual-model agreement and anomaly score |
| 04 | 🔍 **Rule-Based Classification** | Pattern engine labels attack types — Flooding, Scan, Exfiltration |
| 05 | 🧾 **SQLite Event Logging** | All detections persisted with full schema and automatic migration |
| 06 | 📊 **Professional SOC Dashboard** | Live charts, alert feed, model metrics, and threat timeline |
| 07 | 🚨 **Attack Simulator** | Built-in DDoS / burst traffic generator for testing and demonstration |
| 08 | 📝 **Audit Log File** | All IDS events printed to terminal with timestamps for real-time review |

<br/>

---

## 🏗️ System Architecture

<br/>

```
┌─────────────────────────────────────────────────────────┐
│                   LIVE NETWORK TRAFFIC                  │
│              (1-second sliding windows)                 │
└───────────────────────────┬─────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                    SCAPY CAPTURE                        │
│         Bound to wlan0 / eth0 interface                 │
└───────────────────────────┬─────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                  FEATURE EXTRACTION                     │
│  packet_count · avg_size · max_size · src_ips · dst_ips │
└──────────────┬──────────────────────────┬───────────────┘
               │                          │
               ▼                          ▼
┌──────────────────────┐    ┌─────────────────────────────┐
│   ISOLATION FOREST   │    │       ONE-CLASS SVM          │
│   Anomaly scoring    │    │   Boundary classification    │
│   (raw features)     │    │   (StandardScaler applied)  │
└──────────┬───────────┘    └──────────────┬──────────────┘
           │                               │
           └──────────────┬────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│              HYBRID CONFIDENCE ASSIGNMENT               │
│                 🔴 HIGH · 🟠 MEDIUM · 🟢 LOW             │
└───────────────────────────┬─────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│             RULE-BASED ATTACK CLASSIFICATION            │
│    Flooding · Network Scan · Exfiltration · Burst       │
└───────────────────────────┬─────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                   SQLITE DATABASE                       │
│         Persistent event log with full schema           │
└───────────────────────────┬─────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│              STREAMLIT SOC DASHBOARD                    │
│           Auto-refreshes every 1 second                 │
└─────────────────────────────────────────────────────────┘
```

<br/>

---

## 📦 Dataset Preparation Pipeline

NetGuard AI builds its own training dataset from real traffic captured on your machine — no external datasets or manual labelling required.

<br/>

```
Packet Capture  →  Feature Extraction  →  Dataset Merging  →  Model Training
```

<br/>

### 🔹 Step 1 — Packet Capture

```
sudo python src/capture_single_device.py
```

Captures raw packet metadata (source/destination IPs, protocol, size) over a configurable duration and saves to `data/raw/`. Run multiple times under different conditions — idle, browsing, streaming, downloading — to build a diverse normal-traffic baseline.

<br/>

### 🔹 Step 2 — Feature Extraction

```
python src/feature_extractor.py
```

Aggregates raw packets into 1-second feature windows:

| Feature | Description |
|---|---|
| `packet_count` | Total packets observed in the window |
| `avg_packet_size` | Mean packet size in bytes |
| `max_packet_size` | Largest single packet observed |
| `unique_src_ips` | Number of distinct source IP addresses |
| `unique_dst_ips` | Number of distinct destination IP addresses |

Output saved to `data/processed/`.

<br/>

### 🔹 Step 3 — Dataset Merging

```
python src/merge_datasets.py
```

Combines all processed feature files, appends source labels for traceability, shuffles for randomness, and saves the final training dataset to:

```
data/processed/combined_features.csv
```

> **Why multiple captures?** Training on traffic from different real-world conditions teaches the model what *normal* looks like across a variety of scenarios — significantly reducing false positives during live detection.

<br/>

---

## ⚙️ Tech Stack

<br/>

| Layer | Technology | Purpose |
|---|---|---|
| Language | Python 3.9+ | Core runtime |
| Anomaly Detection | Isolation Forest | Unsupervised scoring |
| Boundary Validation | One-Class SVM | Decision boundary enforcement |
| Feature Scaling | StandardScaler | Normalise features for SVM |
| Packet Capture | Scapy | Live network sniffing |
| Dashboard | Streamlit + Altair | Visualisation and UI |
| Database | SQLite3 | Event persistence |
| Model Persistence | Joblib | Save and load `.pkl` models |
| Data Processing | Pandas + NumPy | Feature engineering |

<br/>

---

## 📁 Project Structure

```
NetGuard-AI/
│
├── src/
│   ├── isolation_forest_model.py   ← Live IDS engine (main detection loop)
│   ├── train_isolation_forest.py   ← Train and save Isolation Forest
│   ├── train_ocsvm.py              ← Train and save One-Class SVM + scaler
│   ├── capture_single_device.py    ← Raw packet capture to CSV
│   ├── feature_extractor.py        ← Per-second feature engineering
│   ├── merge_datasets.py           ← Combine feature CSVs for training
│   ├── db_manager.py               ← SQLite init, migration, fast insert
│   ├── suggestion_engine.py        ← Rule-based attack type classifier
│   ├── device_profiler.py          ← Network profile ID generator
│   ├── dashboard.py                ← Streamlit SOC dashboard
│   └── attack_simulator.py         ← Traffic attack simulator
│
├── data/
│   ├── raw/                        ← Raw packet CSVs from capture
│   └── processed/                  ← Feature CSVs + combined dataset
│
├── models/                         ← Auto-generated after training
│   ├── isolation_forest.pkl
│   ├── ocsvm_model.pkl
│   └── ocsvm_scaler.pkl
│
├── netguard.db                     ← SQLite event log (auto-created)
├── requirements.txt
└── README.md
```

<br/>

---

## ▶️ How to Run

### Prerequisites

- Python 3.9 or higher
- Root / sudo access (required for packet capture)
- Linux or macOS recommended (Scapy has limited Windows support)

<br/>

### Setup

**1 · Clone the repository**

```
git clone https://github.com/deathbyginger64/NetGuard-AI.git
cd NetGuard-AI
```

**2 · Create and activate a virtual environment**

```
python3 -m venv venv
source venv/bin/activate
```

**3 · Install all dependencies**

```
pip install -r requirements.txt
```

<br/>

### Build the Training Dataset

**4 · Capture normal network traffic** *(run 2–3 times under different conditions)*

```
sudo venv/bin/python src/capture_single_device.py
```

**5 · Extract features from captured data**

```
python src/feature_extractor.py
```

**6 · Merge all captured datasets**

```
python src/merge_datasets.py
```

<br/>

### Train the Models

**7 · Train Isolation Forest**

```
python src/train_isolation_forest.py
```

**8 · Train One-Class SVM**

```
python src/train_ocsvm.py
```

<br/>

### Run the System

**9 · Start the live IDS engine**

> Ensure the `models/` folder contains trained `.pkl` files before starting. Run steps 7 and 8 first if you haven't already.

```
sudo venv/bin/python src/isolation_forest_model.py
```

**10 · Launch the SOC dashboard** *(in a separate terminal)*

```
streamlit run src/dashboard.py
```

**11 · Run attack simulation** *(optional — for testing and demonstration)*

```
sudo venv/bin/python src/attack_simulator.py
```

<br/>

---

## 🧠 Detection Logic

### Confidence Assignment Rules

| Condition | Confidence | Meaning |
|---|---|---|
| Both models flag anomaly **and** IF score `< −0.1` | 🔴 **HIGH** | Full model agreement with strong anomaly score |
| Both models flag anomaly with borderline IF score | 🟠 **MEDIUM** | Agreement without strong signal — suspicious |
| Rule engine threshold breached | 🔴 **HIGH** | Clear behavioural anomaly — rule override |
| Only one model flags anomaly | 🟠 **MEDIUM** | Partial signal — possible noise or edge case |
| Both models report normal | 🟢 **LOW** | Traffic within expected parameters |

<br/>

### Rule Engine Thresholds

| Trigger | Threshold | Alert Label |
|---|---|---|
| Packet volume spike | `packet_count > 100 / sec` | Possible Flooding Attack |
| Wide destination spread | `unique_dst_ips > 10` + `packet_count > 30` | Possible Network Scan |
| Large payload, low volume | `avg_size > 700B` + `packet_count < 30` | Possible Data Exfiltration |
| Default fallback | — | Suspicious Burst Traffic |

<br/>

---

## 📊 Dashboard Capabilities

The SOC dashboard auto-refreshes every second and provides full operational visibility:

<br/>

| Panel | Description |
|---|---|
| 🎯 **Hero Card** | System status, active alert count, and current threat rate |
| 🚨 **Threat Banner** | CRITICAL / ELEVATED / LOW — driven by anomaly rate + avg risk score |
| 📡 **Live Telemetry** | Packets/sec, anomaly score, confidence level, and alert type |
| 📈 **Threat Timeline** | Full session plotted with colour-coded Normal vs Anomaly events |
| 🔥 **Threat Intelligence** | Attack type distribution chart and live alert feed cards |
| 🤖 **Model Intelligence** | Confidence distribution, model agreement %, score scatter plot |
| 📋 **Model Evaluation** | TP, FP, detection rate, and false positive rate |
| ⚙️ **Health Indicators** | Real-time IDS engine, database, and ingestion status |
| 📝 **Event Log** | Last 100 records with anomaly rows highlighted in red |

<br/>

---

## ⚠️ Important Notes

```
This is an unsupervised learning system — no labelled attack data is required
```

- The model learns *normal* from your own captured traffic
- False Negatives (FN) are approximated as 0 — standard practice for unsupervised IDS
- Detection metrics (TP, FP, precision, detection rate) are estimated using model confidence levels as a proxy
- Change the network interface (`wlan0` / `eth0`) in capture and IDS scripts to match your system's active interface
- Root / sudo is required for Scapy to access the network interface
- ⚠️ Note: This system is trained on self-captured network traffic to simulate real-world anomaly detection scenarios.

<br/>

---

## 🎯 Use Cases

- Network anomaly detection in research and home lab environments
- Cybersecurity final year and capstone projects
- SOC simulation and live demonstration to technical panels
- Benchmarking unsupervised ML approaches to network intrusion detection

<br/>

---

## 🔭 Future Improvements

- [ ] Deep learning integration — LSTM and Autoencoder models for temporal anomaly detection
- [ ] Docker containerisation for portable, reproducible deployment
- [ ] Multi-device and multi-interface simultaneous monitoring
- [ ] Integration with benchmark datasets — KDD Cup 99, CICIDS 2017/2018
- [ ] Real-time email and SMS alerting on CRITICAL threat level
- [ ] Exportable PDF incident reports generated from the dashboard
- [ ] REST API endpoint for external SIEM tool integration

<br/>

---

## 👨‍💻 Authors

<br/>

<div align="center">

| **Aditya Khandelwal** | **Astha Chakraborty** |
|---|---|
| B.Tech CSE — Cyber Security | B.Tech CSE — Cyber Security |

</div>

<br/>

---

<div align="center">

*Built for educational and research purposes · NetGuard AI*

</div>
