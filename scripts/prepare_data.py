"""
GUARDNODE IoT IDS — REAL CICIoT2023 CLASS-BALANCED FEATURE CONSTRUCTION PIPELINE

Dataset: data/raw/archive (1).zip
Splits:
  - CICIOT23/train/train.csv           -> data/processed/train_features.csv
  - CICIOT23/validation/validation.csv -> data/processed/validation_features.csv
  - CICIOT23/test/test.csv             -> data/processed/test_features.csv

Scientific & Technical Design Rationale:
1. Class-Specific Flow-Rate Windows:
   Because raw dataset rows are heavily imbalanced (~97.64% attack, ~2.36% benign) and raw CSV rows are flow records
   rather than individual packet arrivals, naive consecutive row windowing mixed normal and attack traffic, producing
   100% attack windows.
   To eliminate class contamination within observation windows, we construct feature windows strictly within each class:
     - NORMAL windows: Grouping 5 consecutive 'BenignTraffic' flow rates.
     - INTRUSION windows: Grouping 5 consecutive attack flow rates.

2. Feature Vector Definition:
   For each class-specific window of 5 flow-rate records:
     - mean_packet_rate   = mean(Rate)
     - median_packet_rate = median(Rate)
     - max_packet_rate    = max(Rate)
   Feature order: [mean_packet_rate, median_packet_rate, max_packet_rate]

3. Target Labels:
   - BenignTraffic -> 0 (NORMAL)
   - Attack categories -> 1 (INTRUSION)

4. Deterministic Class Balancing (Training Only):
   For training, we select equal numbers of NORMAL and INTRUSION windows deterministically:
     n_train_per_class = min(n_normal_windows, n_intrusion_windows)
   We take the first n_train_per_class deterministic windows from each class without synthetic oversampling or duplicate rows.

5. Preserved Validation & Test Distributions:
   Validation and test sets preserve their full natural class distributions for realistic evaluation auditing.
"""

import os
import sys
import json
import zipfile
import numpy as np
import pandas as pd

# Path definitions
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
DATA_PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")

ZIP_PATH = os.path.join(DATA_RAW_DIR, "archive (1).zip")
REPORT_PATH = os.path.join(DATA_PROCESSED_DIR, "preprocessing_report.json")

WINDOW_SIZE = 5
CHUNK_SIZE = 100000  # 100,000 rows per chunk

SPLIT_FILES = {
    "train": {
        "zip_internal_path": "CICIOT23/train/train.csv",
        "output_csv": os.path.join(DATA_PROCESSED_DIR, "train_features.csv"),
        "balance_training": True
    },
    "validation": {
        "zip_internal_path": "CICIOT23/validation/validation.csv",
        "output_csv": os.path.join(DATA_PROCESSED_DIR, "validation_features.csv"),
        "balance_training": False
    },
    "test": {
        "zip_internal_path": "CICIOT23/test/test.csv",
        "output_csv": os.path.join(DATA_PROCESSED_DIR, "test_features.csv"),
        "balance_training": False
    }
}


def compute_class_windows(rate_values: np.ndarray, label_val: int):
    """
    Computes statistical feature windows (mean, median, max) for a 1D array of flow Rate values.
    Returns DataFrame with columns: mean_packet_rate, median_packet_rate, max_packet_rate, label
    """
    total_records = len(rate_values)
    num_windows = total_records // WINDOW_SIZE
    discarded_records = total_records % WINDOW_SIZE

    if num_windows == 0:
        empty_df = pd.DataFrame(columns=["mean_packet_rate", "median_packet_rate", "max_packet_rate", "label"])
        return empty_df, 0, discarded_records, []

    # Slice exact full windows
    valid_rates = rate_values[:num_windows * WINDOW_SIZE]
    rate_matrix = valid_rates.reshape((num_windows, WINDOW_SIZE))

    w_means = np.round(np.mean(rate_matrix, axis=1), 2)
    w_medians = np.round(np.median(rate_matrix, axis=1), 2)
    w_maxs = np.round(np.max(rate_matrix, axis=1), 2)
    w_labels = np.full(num_windows, label_val, dtype=int)

    df_windows = pd.DataFrame({
        "mean_packet_rate": w_means,
        "median_packet_rate": w_medians,
        "max_packet_rate": w_maxs,
        "label": w_labels
    })

    return df_windows, num_windows, discarded_records, rate_matrix[:2]  # return first 2 windows matrix for preview


def process_split(zf: zipfile.ZipFile, split_name: str, config: dict):
    print(f"\n==================================================")
    print(f"PROCESSING SPLIT: {split_name.upper()}")
    print(f"Input: {config['zip_internal_path']}")
    print(f"Output: {config['output_csv']}")
    print(f"==================================================")

    invalid_rate_records_removed = 0
    original_label_counts = {}

    normal_rates_list = []
    attack_rates_list = []

    with zf.open(config['zip_internal_path']) as f:
        for chunk in pd.read_csv(f, chunksize=CHUNK_SIZE, usecols=['Rate', 'label']):
            # Audit original labels
            for label_val, cnt in chunk['label'].value_counts().items():
                lbl_key = str(label_val)
                original_label_counts[lbl_key] = original_label_counts.get(lbl_key, 0) + int(cnt)

            # Convert Rate to numeric and filter valid records
            chunk['Rate_num'] = pd.to_numeric(chunk['Rate'], errors='coerce')
            valid_mask = chunk['Rate_num'].notnull() & np.isfinite(chunk['Rate_num'])
            invalid_count = int(len(chunk) - valid_mask.sum())
            invalid_rate_records_removed += invalid_count

            valid_chunk = chunk[valid_mask]

            # Separate into NORMAL (BenignTraffic) and INTRUSION
            normal_mask = valid_chunk['label'] == 'BenignTraffic'
            normal_chunk_rates = valid_chunk.loc[normal_mask, 'Rate_num'].to_numpy(dtype=np.float64)
            attack_chunk_rates = valid_chunk.loc[~normal_mask, 'Rate_num'].to_numpy(dtype=np.float64)

            normal_rates_list.append(normal_chunk_rates)
            attack_rates_list.append(attack_chunk_rates)

    normal_rates = np.concatenate(normal_rates_list) if normal_rates_list else np.array([], dtype=np.float64)
    attack_rates = np.concatenate(attack_rates_list) if attack_rates_list else np.array([], dtype=np.float64)

    total_raw_records = len(normal_rates) + len(attack_rates) + invalid_rate_records_removed
    normal_source_records = len(normal_rates)
    attack_source_records = len(attack_rates)

    # Compute class-specific flow-rate windows
    df_normal_win, n_normal_win, disc_normal_rec, normal_sample_mat = compute_class_windows(normal_rates, label_val=0)
    df_attack_win, n_attack_win, disc_attack_rec, attack_sample_mat = compute_class_windows(attack_rates, label_val=1)

    total_discarded_records = invalid_rate_records_removed + disc_normal_rec + disc_attack_rec

    print(f"  Source Records: {total_raw_records:,} (Normal: {normal_source_records:,}, Attack: {attack_source_records:,})")
    print(f"  Available Windows: Normal = {n_normal_win:,}, Attack = {n_attack_win:,}")

    # Print required sample preview
    if len(normal_sample_mat) > 0:
        r_samp = normal_sample_mat[0]
        m_val = round(float(np.mean(r_samp)), 2)
        med_val = round(float(np.median(r_samp)), 2)
        mx_val = round(float(np.max(r_samp)), 2)
        print(f"\n[SAMPLE PREVIEW] NORMAL WINDOW:")
        print(f"  Rate values: {[round(x, 2) for x in r_samp]}")
        print(f"  Mean: {m_val}")
        print(f"  Median: {med_val}")
        print(f"  Max: {mx_val}")
        print(f"  Label: 0 (NORMAL)")

    if len(attack_sample_mat) > 0:
        r_samp = attack_sample_mat[0]
        m_val = round(float(np.mean(r_samp)), 2)
        med_val = round(float(np.median(r_samp)), 2)
        mx_val = round(float(np.max(r_samp)), 2)
        print(f"\n[SAMPLE PREVIEW] INTRUSION WINDOW:")
        print(f"  Rate values: {[round(x, 2) for x in r_samp]}")
        print(f"  Mean: {m_val}")
        print(f"  Median: {med_val}")
        print(f"  Max: {mx_val}")
        print(f"  Label: 1 (INTRUSION)")

    # Class balancing selection logic
    discarded_for_balancing = 0
    if config["balance_training"]:
        n_select = min(n_normal_win, n_attack_win)
        df_normal_sel = df_normal_win.iloc[:n_select].copy()
        df_attack_sel = df_attack_win.iloc[:n_select].copy()
        discarded_for_balancing = int((n_normal_win - n_select) + (n_attack_win - n_select))
        
        # Combine and shuffle with fixed seed (random_state=42) for deterministic training order
        final_df = pd.concat([df_normal_sel, df_attack_sel], ignore_index=True)
        final_df = final_df.sample(frac=1.0, random_state=42).reset_index(drop=True)
        print(f"\n[BALANCING] Training set balanced deterministically: {n_select:,} NORMAL + {n_select:,} INTRUSION windows")
    else:
        # Combine all validation/test windows without balancing to preserve natural test distribution
        final_df = pd.concat([df_normal_win, df_attack_win], ignore_index=True)
        final_df = final_df.sample(frac=1.0, random_state=42).reset_index(drop=True)

    # Strict feature column order assertion
    expected_cols = ["mean_packet_rate", "median_packet_rate", "max_packet_rate", "label"]
    assert list(final_df.columns) == expected_cols, f"Column names mismatch! Found: {list(final_df.columns)}"

    # Save to CSV
    final_df.to_csv(config['output_csv'], index=False)
    print(f"[SUCCESS] Saved {len(final_df):,} class-specific feature windows to: {config['output_csv']}")

    total_output_win = len(final_df)
    out_normal_win = int((final_df['label'] == 0).sum())
    out_intrusion_win = int((final_df['label'] == 1).sum())

    all_valid_rates = np.concatenate([normal_rates, attack_rates]) if (len(normal_rates) + len(attack_rates)) > 0 else np.array([0.0])

    stats_dict = {
        "split_name": split_name,
        "output_file": config['output_csv'],
        "raw_flow_records": int(total_raw_records),
        "valid_rate_records": int(len(all_valid_rates)),
        "invalid_rate_records_removed": int(invalid_rate_records_removed),
        "normal_source_records": int(normal_source_records),
        "intrusion_source_records": int(attack_source_records),
        "normal_windows_available": int(n_normal_win),
        "intrusion_windows_available": int(n_attack_win),
        "total_windows_available": int(n_normal_win + n_attack_win),
        "selected_output_windows": int(total_output_win),
        "output_normal_windows": int(out_normal_win),
        "output_normal_percentage": round(float(out_normal_win / total_output_win * 100), 2) if total_output_win > 0 else 0.0,
        "output_intrusion_windows": int(out_intrusion_win),
        "output_intrusion_percentage": round(float(out_intrusion_win / total_output_win * 100), 2) if total_output_win > 0 else 0.0,
        "discarded_for_balancing": int(discarded_for_balancing),
        "discarded_trailing_records": int(disc_normal_rec + disc_attack_rec),
        "raw_rate_stats": {
            "min": round(float(np.min(all_valid_rates)), 4),
            "max": round(float(np.max(all_valid_rates)), 4),
            "mean": round(float(np.mean(all_valid_rates)), 4),
            "median": round(float(np.median(all_valid_rates)), 4)
        },
        "feature_stats_after_windowing": {
            "mean_packet_rate": {
                "min": round(float(final_df['mean_packet_rate'].min()), 4),
                "max": round(float(final_df['mean_packet_rate'].max()), 4),
                "mean": round(float(final_df['mean_packet_rate'].mean()), 4),
                "median": round(float(final_df['mean_packet_rate'].median()), 4)
            },
            "median_packet_rate": {
                "min": round(float(final_df['median_packet_rate'].min()), 4),
                "max": round(float(final_df['median_packet_rate'].max()), 4),
                "mean": round(float(final_df['median_packet_rate'].mean()), 4),
                "median": round(float(final_df['median_packet_rate'].median()), 4)
            },
            "max_packet_rate": {
                "min": round(float(final_df['max_packet_rate'].min()), 4),
                "max": round(float(final_df['max_packet_rate'].max()), 4),
                "mean": round(float(final_df['max_packet_rate'].mean()), 4),
                "median": round(float(final_df['max_packet_rate'].median()), 4)
            }
        },
        "original_label_distribution": {k: int(v) for k, v in original_label_counts.items()}
    }

    return stats_dict


def prepare_real_ciciot2023():
    os.makedirs(DATA_PROCESSED_DIR, exist_ok=True)

    print(f"Checking dataset ZIP archive at: {ZIP_PATH}")
    if not os.path.exists(ZIP_PATH):
        print(f"[ERROR] Dataset ZIP not found at {ZIP_PATH}!")
        sys.exit(1)

    if not zipfile.is_zipfile(ZIP_PATH):
        print(f"[ERROR] File at {ZIP_PATH} is not a valid ZIP archive!")
        sys.exit(1)

    report = {
        "dataset": "CICIoT2023 (Official Class-Specific Flow-Rate Windows)",
        "zip_archive": ZIP_PATH,
        "window_size": WINDOW_SIZE,
        "synthetic_data_generated": False,
        "feature_order": ["mean_packet_rate", "median_packet_rate", "max_packet_rate"],
        "target_mapping": {
            "BenignTraffic": "NORMAL / 0",
            "All attack categories": "INTRUSION / 1"
        },
        "splits": {}
    }

    with zipfile.ZipFile(ZIP_PATH, 'r') as zf:
        for split_name, config in SPLIT_FILES.items():
            split_stats = process_split(zf, split_name, config)
            report["splits"][split_name] = split_stats

    # Write overall preprocessing report JSON
    with open(REPORT_PATH, "w") as f:
        json.dump(report, f, indent=2)

    print(f"\n==================================================")
    print(f"CLASS-BALANCED PREPROCESSING COMPLETE — REPORT SAVED")
    print(f"Report File: {REPORT_PATH}")
    print(f"==================================================")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    prepare_real_ciciot2023()
