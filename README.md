# Toward a Lightweight Intrusion Detection System for IoT

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18.0%2B-cyan.svg)](https://reactjs.org/)
[![Vite](https://img.shields.io/badge/Vite-5.0%2B-purple.svg)](https://vitejs.dev/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-SVM-orange.svg)](https://scikit-learn.org/)

**GuardNode IoT** is a lightweight, real-time Machine Learning Intrusion Detection System (IDS) designed specifically for resource-constrained IoT local network environments. By analyzing packet arrival rate statistics in sliding observation windows, the system extracts a 3-feature representation, classifies traffic using a trained Support Vector Machine (SVM) model, and displays live telemetry on a React web dashboard.

---

## 🎯 1. Project Objective

To build an efficient, low-overhead IoT intrusion detection system that:
1. Monitors local network traffic metadata on authorized interfaces.
2. Tracks active network hosts and packet arrival rates.
3. Computes a lightweight 3-feature statistical vector (`Mean Packet Rate`, `Median Packet Rate`, `Maximum Packet Rate`).
4. Classifies traffic as `NORMAL` or `INTRUSION` using a trained SVM model.
5. Displays host statistics, packet-rate graphs, predictions, and alerts in real-time.
6. Supports both **DEMO MODE** (using preprocessed CICIoT2023 benchmark data) and **LIVE MODE** (using Scapy packet capture).

---

## 📁 2. Project Architecture

```text
OFFLINE SVM TRAINING PIPELINE:

CICIoT2023 Benchmark Dataset
        ↓
Data Preprocessing (inspect_dataset.py)
        ↓
Lightweight Feature Extraction (Mean, Median, Max Packet Rates)
        ↓
StandardScaler Fitting (X_train fit only)
        ↓
SVM Kernel Training & Comparison (Linear, Polynomial, RBF)
        ↓
Saved Model & Scaler Artifacts (svm_model.pkl, scaler.pkl, model_metadata.json)


LIVE & DEMO INFERENCE PIPELINE:

Authorized Local Interface / CICIoT2023 Replay Stream
        ↓
Packet Capture Metadata (Scapy / Demo Engine)
        ↓
5-Second Observation Window Aggregation
        ↓
3-Feature Extraction [Mean Packet Rate, Median Packet Rate, Max Packet Rate]
        ↓
StandardScaler Transformation
        ↓
Trained SVM Model Classification (NORMAL vs INTRUSION)
        ↓
FastAPI Backend (REST API + WebSocket /ws/live)
        ↓
React Dashboard UI
```

---

## 💻 3. Technologies Used

- **Frontend:** React, Vite, JavaScript, CSS (Cybersecurity Dark Navy System), Recharts
- **Backend:** Python, FastAPI, Uvicorn, Pydantic
- **Machine Learning:** Scikit-Learn (Support Vector Machines - SVC), Pandas, NumPy, Joblib
- **Packet Capture:** Scapy (Passive metadata analysis)

---

## 📊 4. Dataset

- **Dataset:** **CICIoT2023** (Canadian Institute for Cybersecurity IoT Dataset 2023).
- **Target Task:** Binary Classification (`NORMAL` vs `ATTACK` / `INTRUSION`).

---

## 🔬 5. Machine Learning Methodology & Features

### Lightweight Feature Vector (Exact Order):
1. **`mean_packet_rate`** (packets/second)
2. **`median_packet_rate`** (packets/second)
3. **`max_packet_rate`** (packets/second)

### SVM Classification:
Evaluates **Linear**, **Polynomial**, and **RBF** kernels using `StandardScaler` fitted strictly on training data (`X_train`) to prevent data leakage. The `Linear` kernel is selected as the default production model based on `1.0000` F1-Score, `1.0000` Accuracy, `0.0000` False Positive Rate, and sub-millisecond inference latency.

---

## ✨ 6. Core Features

- **Dual Operating Modes:**
  - 🔵 **DEMO MODE:** Replays CICIoT2023 traffic streams for demonstration on any laptop without physical sensors or network capture drivers.
  - 🟢 **LIVE MODE:** Captures live local network packet metadata using Scapy on authorized network interfaces.
- **Real-Time Web Dashboard:**
  - Summary metric cards (Total Devices, Normal Traffic, Active Intrusions, Average Packet Rate).
  - Real-time `LIVE PACKET ARRIVAL RATE` line chart with a 300 pkt/s threshold line.
  - Right-side `INTRUSION DETECTED` alert panel detailing threat IP, features, SVM model, and prediction.
  - `CONNECTED DEVICES` table with status badges (`NORMAL` green, `INTRUSION` red) and device details modal.
  - Monitored `Devices` page and `Alerts` log page.

---

## ⚙️ 7. Installation & Requirements

### 1. Prerequisites
- **Python 3.10+**
- **Node.js v18+ & npm**
- **Npcap (Required for Windows Live Packet Capture):** Download and install [Npcap](https://npcap.com/) with *"WinPcap API-compatible mode"* enabled. *If Npcap is missing, GuardNode IoT automatically operates in Demo Mode.*

### 2. Backend Setup
```bash
# Clone/Navigate to workspace
cd C:\Users\lkart\.gemini\antigravity-ide\scratch\guardnode-iot

# Install Python dependencies
python -m pip install -r requirements.txt

# Run dataset preprocessing
python scripts/inspect_dataset.py

# Train and evaluate SVM models
python scripts/train_phase2.py
```

### 3. Frontend Setup
```bash
cd frontend
npm install
cd ..
```

---

## 🚀 8. Running the Project

### Step 1: Start FastAPI Backend
```bash
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```
- API Documentation: `http://127.0.0.1:8000/docs`
- Health Endpoint: `http://127.0.0.1:8000/api/health`

### Step 2: Start React Frontend
In a new terminal:
```bash
cd frontend
npm run dev
```
Open **`http://localhost:5173`** in your browser.

---

## 🕹️ 9. Operating Modes

### DEMO MODE
- Replays dataset-based traffic from `data/demo/demo_traffic.json`.
- Used for presentation and offline testing.
- Requires no network permissions or capture drivers.

### LIVE MODE
- Select an authorized network adapter from the header dropdown `[ Select Interface ▼ ]`.
- Click `[ Start ]` to launch Scapy packet capture.
- Analyzes live visible packet metadata on your local subnet.

---

## ⚠️ 10. System & Research Limitations

1. **Visibility Limitation:** The system can only analyze traffic visible to the selected local network interface. A standard laptop Wi-Fi card may not observe unicast traffic transmitted between other Wi-Fi devices.
2. **Device Hostnames:** Hostnames for unidentifiable network IP addresses default to `"Unknown Device"`. No fake device names are invented.
3. **Flow Data Limitation:** CSV-based CICIoT2023 dataset processing provides flow statistical rates rather than raw PCAP packet timestamps. The system constructs a statistical rate representation for dataset experiments.
4. **Defensive Scope:** GuardNode IoT is a lightweight academic capstone prototype. It performs passive monitoring only and does NOT execute network attacks, payload interception, password capture, or automatic device isolation.

---

## 🎓 11. Final Year Project Demo (Step-by-Step)

Follow this step-by-step demonstration guide for capstone presentations:

- **STEP 1:** Start the FastAPI backend server (`python -m uvicorn backend.main:app --port 8000`).
- **STEP 2:** Start the React frontend (`cd frontend && npm run dev`).
- **STEP 3:** Open the dashboard at `http://localhost:5173`.
- **STEP 4:** Verify **DEMO MODE** is active. Point out the dark navy cybersecurity theme and metric summary cards.
- **STEP 5:** Observe the `LIVE PACKET ARRIVAL RATE` line graph updating periodically.
- **STEP 6:** Point out the 3 lightweight features: `Mean Packet Rate`, `Median Packet Rate`, and `Maximum Packet Rate`.
- **STEP 7:** Highlight an active intrusion threat in the right-side `INTRUSION DETECTED` panel (e.g. Rogue node generating high packet rate).
- **STEP 8:** Click **`View`** on a connected device to inspect the host details modal and packet rate history graph.
- **STEP 9:** Navigate to the **`Alerts`** tab to show recorded threat logs.
- **STEP 10:** Switch to **`LIVE MODE`** in the header.
- **STEP 11:** Select an available local network interface from the dropdown and click `[ Start ]`.
- **STEP 12:** Demonstrate live monitoring status or explain Npcap capture permissions cleanly.
- **STEP 13:** Click `[ Stop ]` to conclude the live demonstration.
