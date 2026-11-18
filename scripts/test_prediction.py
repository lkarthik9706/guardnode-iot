import os
import sys
import json
import pandas as pd

# Add root directory to sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from backend.ml.predict import predict_intrusion

def run_test_predictions():
    print("=" * 60)
    print("      GUARDNODE IoT — PHASE 2 MODEL INFERENCE TEST")
    print("=" * 60)

    # Test cases: combinations of Normal and Intrusion traffic samples
    test_samples = [
        {
            "name": "Normal IoT Device Baseline",
            "mean": 22.5,
            "median": 20.0,
            "max": 35.0
        },
        {
            "name": "Normal Smart Thermostat Stream",
            "mean": 45.1,
            "median": 42.0,
            "max": 68.0
        },
        {
            "name": "High-Volume Flood Attack Sample",
            "mean": 850.4,
            "median": 798.0,
            "max": 1250.0
        },
        {
            "name": "DDoS Packet Burst Intrusion",
            "mean": 1420.0,
            "median": 1390.0,
            "max": 2100.0
        }
    ]

    print(f"\n[INFO] Running inference on {len(test_samples)} test instances...\n")

    for idx, sample in enumerate(test_samples):
        res = predict_intrusion(
            mean_packet_rate=sample["mean"],
            median_packet_rate=sample["median"],
            max_packet_rate=sample["max"]
        )

        print(f"Test Case #{idx+1}: {sample['name']}")
        print("Input Features:")
        print(f"  - Mean packet rate   : {res['features']['mean_packet_rate']} pkt/s")
        print(f"  - Median packet rate : {res['features']['median_packet_rate']} pkt/s")
        print(f"  - Maximum packet rate: {res['features']['max_packet_rate']} pkt/s")
        print(f"Prediction Result      : {res['prediction']}")
        print(f"SVM Kernel Used        : {res.get('kernel', 'linear').upper()}")
        if "decision_score" in res:
            print(f"Decision Score         : {res['decision_score']}")
        if "decision_threshold" in res:
            print(f"Decision Threshold     : {res['decision_threshold']}")
        print("-" * 60)

if __name__ == "__main__":
    run_test_predictions()
