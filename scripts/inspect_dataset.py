import os
import sys
import glob
import numpy as np
import pandas as pd

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)

PROCESSED_CSV_PATH = os.path.join(PROCESSED_DIR, "train_features.csv")

# Configuration
SAMPLE_SIZE = 100000
RANDOM_STATE = 42

def inspect_and_preprocess():
    print("=" * 70)
    print("      GUARDNODE IoT — PHASE 2: DATASET INSPECTION & PREPROCESSING")
    print("=" * 70)

    # Find raw CSV files
    csv_files = glob.glob(os.path.join(RAW_DIR, "*.csv"))
    if not csv_files:
        raise FileNotFoundError(f"No CSV files found in raw directory: {RAW_DIR}")

    print(f"\n[INFO] Found {len(csv_files)} raw CSV file(s) in '{RAW_DIR}':")
    for f in csv_files:
        print(f"  - {os.path.basename(f)}")

    # Process first or all CSV files
    raw_file = csv_files[0]
    print(f"\n[INFO] Reading dataset file: {os.path.basename(raw_file)}")

    # Read a sample chunk to inspect actual schema
    sample_df = pd.read_csv(raw_file, nrows=1000)
    columns = list(sample_df.columns)
    
    print("\n--- ACTUAL DATASET COLUMNS DISCOVERED ---")
    for idx, col in enumerate(columns):
        print(f"  [{idx+1:02d}] {col} ({sample_df[col].dtype})")
    print("------------------------------------------")

    # Determine Label Column
    label_col = None
    possible_label_cols = ["label", "Label", "label_category", "class", "Class", "Attack_type"]
    for col in columns:
        if col.strip() in possible_label_cols or col.strip().lower() == "label":
            label_col = col
            break
    
    if not label_col:
        # Fallback to last column
        label_col = columns[-1]

    print(f"\n[INFO] Identified Label Column: '{label_col}'")

    # Determine Traffic Rate Columns
    # Target features: mean_packet_rate, median_packet_rate, max_packet_rate
    feature_cols = []
    
    # Case A: Directly contains mean_packet_rate, median_packet_rate, max_packet_rate
    expected_3 = ["mean_packet_rate", "median_packet_rate", "max_packet_rate"]
    if all(c in columns for c in expected_3):
        feature_cols = expected_3
        limitation_note = "Using exact packet arrival rate features from preprocessed dataset."
    else:
        # Case B: CICIoT2023 Flow Rate features (e.g., Rate, Srate, Drate, Duration, etc.)
        # Look for rate / interval columns in CICIoT2023
        rate_candidates = [c for c in columns if any(k in c.lower() for k in ["rate", "duration", "iat", "avg", "min", "max", "sum"])]
        print(f"[INFO] Available traffic rate candidate columns in CICIoT2023: {rate_candidates}")
        
        # Select best 3 traffic rate columns
        selected = []
        for pref in ["rate", "srate", "drate", "avg", "max", "min", "duration"]:
            for c in columns:
                if pref in c.lower() and c not in selected and c != label_col:
                    selected.append(c)
                    if len(selected) == 3:
                        break
            if len(selected) == 3:
                break
        
        if len(selected) < 3:
            # Pick first 3 numeric non-label columns
            num_cols = [c for c in columns if c != label_col and np.issubdtype(sample_df[c].dtype, np.number)]
            selected = num_cols[:3]

        feature_cols = selected
        limitation_note = (
            "The current implementation uses the available traffic-rate information in the "
            "CICIoT2023 flow data to construct a lightweight statistical representation. "
            "Raw PCAP-based packet-arrival-rate extraction is outside the current simplified implementation."
        )

    print(f"\n[INFO] Selected Feature Mapping: {feature_cols} -> [mean_packet_rate, median_packet_rate, max_packet_rate]")
    print(f"[RESEARCH LIMITATION NOTE]: {limitation_note}")

    # Load Full or Sampled Data
    print(f"\n[INFO] Loading up to {SAMPLE_SIZE} records with random_state={RANDOM_STATE}...")
    full_df = pd.read_csv(raw_file)
    
    total_raw_rows = len(full_df)
    print(f"[INFO] Total rows in raw CSV file: {total_raw_rows}")

    if len(full_df) > SAMPLE_SIZE:
        full_df = full_df.sample(n=SAMPLE_SIZE, random_state=RANDOM_STATE).reset_index(drop=True)
    
    print(f"[INFO] Processed Sample Size: {len(full_df)} rows")

    # Clean missing / infinity
    print("\n[INFO] Cleaning missing (NaN) and infinite (inf) values...")
    full_df = full_df.replace([np.inf, -np.inf], np.nan)
    initial_cnt = len(full_df)
    full_df = full_df.dropna(subset=feature_cols + [label_col]).reset_index(drop=True)
    cleaned_cnt = len(full_df)
    print(f"[INFO] Dropped {initial_cnt - cleaned_cnt} invalid/NaN/inf rows. Remaining clean rows: {cleaned_cnt}")

    # Encode Binary Label: NORMAL (0) vs ATTACK (1)
    raw_labels = full_df[label_col].astype(str)
    
    def map_binary_label(val):
        v = val.strip().lower()
        if v in ["normal", "benign", "0", "0.0"]:
            return 0
        return 1

    binary_labels = raw_labels.apply(map_binary_label)
    full_df["encoded_label"] = binary_labels

    label_counts = full_df["encoded_label"].value_counts()
    n_normal = label_counts.get(0, 0)
    n_attack = label_counts.get(1, 0)

    print("\n" + "="*50)
    print("      FINAL BINARY CLASS DISTRIBUTION")
    print("="*50)
    print(f"  NORMAL (0) : {n_normal:<8} ({n_normal/len(full_df)*100:.2f}%)")
    print(f"  ATTACK (1) : {n_attack:<8} ({n_attack/len(full_df)*100:.2f}%)")
    print("="*50)

    # Save Preprocessed Features with standardized names
    processed_df = pd.DataFrame({
        "mean_packet_rate": full_df[feature_cols[0]].values,
        "median_packet_rate": full_df[feature_cols[1]].values,
        "max_packet_rate": full_df[feature_cols[2]].values,
        "label": full_df["encoded_label"].values
    })

    processed_df.to_csv(PROCESSED_CSV_PATH, index=False)
    print(f"\n[SUCCESS] Preprocessed feature matrix saved to: {PROCESSED_CSV_PATH}")

    return {
        "columns": columns,
        "processed_rows": len(processed_df),
        "normal_count": int(n_normal),
        "attack_count": int(n_attack),
        "features_used": ["mean_packet_rate", "median_packet_rate", "max_packet_rate"],
        "mapped_from": feature_cols,
        "limitation_note": limitation_note
    }

if __name__ == "__main__":
    inspect_and_preprocess()
