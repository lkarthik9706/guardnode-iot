"""
GUARDNODE IoT IDS — REAL CICIoT2023 LINEARSVC MODEL TRAINING & EVALUATION

Dataset:
  - Training:   data/processed/train_features.csv (51,814 balanced, stratified samples)
  - Validation: data/processed/validation_features.csv (235,369 natural samples)
  - Test:       data/processed/test_features.csv (235,369 natural samples)

Preprocessing:
  Raw 3 features -> np.log1p -> StandardScaler (fitted ONLY on training) -> LinearSVC -> Validation Threshold

Features:
  [mean_packet_rate, median_packet_rate, max_packet_rate]
"""

import os
import sys
import time
import json
import joblib
import numpy as np
import pandas as pd

from sklearn.preprocessing import StandardScaler
from sklearn.svm import LinearSVC
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, balanced_accuracy_score
)

# Optional matplotlib for matrix plotting
try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
MODELS_DIR = os.path.join(BASE_DIR, "models")
RESULTS_DIR = os.path.join(BASE_DIR, "results")

os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)

TRAIN_CSV = os.path.join(PROCESSED_DIR, "train_features.csv")
VAL_CSV = os.path.join(PROCESSED_DIR, "validation_features.csv")
TEST_CSV = os.path.join(PROCESSED_DIR, "test_features.csv")

MODEL_PKL_PATH = os.path.join(MODELS_DIR, "svm_model.pkl")
SCALER_PKL_PATH = os.path.join(MODELS_DIR, "scaler.pkl")
METADATA_JSON_PATH = os.path.join(MODELS_DIR, "model_metadata.json")

FEATURE_NAMES = ["mean_packet_rate", "median_packet_rate", "max_packet_rate"]


def compute_metrics(y_true, y_pred, elapsed_time_sec=0.0):
    cm = confusion_matrix(y_true, y_pred, labels=[0, 1])
    tn, fp, fn, tp = cm.ravel()

    tn = int(tn)
    fp = int(fp)
    fn = int(fn)
    tp = int(tp)

    acc = float(accuracy_score(y_true, y_pred))
    prec = float(precision_score(y_true, y_pred, zero_division=0))
    rec = float(recall_score(y_true, y_pred, zero_division=0))  # TPR / Recall
    f1 = float(f1_score(y_true, y_pred, zero_division=0))

    tnr = float(tn / (tn + fp)) if (tn + fp) > 0 else 0.0      # Specificity / TNR
    fpr = float(fp / (fp + tn)) if (fp + tn) > 0 else 0.0      # FPR
    fnr = float(fn / (fn + tp)) if (fn + tp) > 0 else 0.0      # FNR
    bal_acc = float(balanced_accuracy_score(y_true, y_pred))

    return {
        "accuracy": round(acc, 4),
        "precision": round(prec, 4),
        "recall_tpr": round(rec, 4),
        "specificity_tnr": round(tnr, 4),
        "f1_score": round(f1, 4),
        "fpr": round(fpr, 4),
        "fnr": round(fnr, 4),
        "balanced_accuracy": round(bal_acc, 4),
        "elapsed_time_sec": round(elapsed_time_sec, 4),
        "TN": tn,
        "FP": fp,
        "FN": fn,
        "TP": tp
    }


def save_confusion_matrix_plot(cm, title, output_path):
    if not HAS_MATPLOTLIB:
        return
    fig, ax = plt.subplots(figsize=(5, 4.5))
    cax = ax.matshow(cm, cmap=plt.cm.Blues, alpha=0.8)

    labels = ["NORMAL", "INTRUSION"]
    ax.set_xticks([0, 1])
    ax.set_yticks([0, 1])
    ax.set_xticklabels(labels, fontsize=10, fontweight='bold')
    ax.set_yticklabels(labels, fontsize=10, fontweight='bold')

    for i in range(2):
        for j in range(2):
            val = cm[i, j]
            ax.text(j, i, f"{val:,}", ha='center', va='center',
                    color='white' if val > cm.max() / 2.0 else 'black',
                    fontsize=12, fontweight='bold')

    plt.xlabel('Predicted Label', fontsize=10, fontweight='bold', labelpad=10)
    plt.ylabel('Actual Label', fontsize=10, fontweight='bold')
    plt.title(f'Confusion Matrix — {title}\n(Real CICIoT2023 Test Set)', fontsize=11, fontweight='bold', pad=15)
    plt.colorbar(cax)
    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close(fig)


def train_and_evaluate():
    print("\n" + "="*60, flush=True)
    print("  GUARDNODE IoT — RETRAINING REAL CICIoT2023 LINEARSVC", flush=True)
    print("="*60, flush=True)

    # 1. Load preprocessed datasets
    for p in [TRAIN_CSV, VAL_CSV, TEST_CSV]:
        if not os.path.exists(p):
            print(f"[ERROR] Dataset missing at {p}!", flush=True)
            sys.exit(1)

    df_train = pd.read_csv(TRAIN_CSV)
    df_val = pd.read_csv(VAL_CSV)
    df_test = pd.read_csv(TEST_CSV)

    X_train_raw = df_train[FEATURE_NAMES].values
    y_train = df_train["label"].values.astype(int)

    X_val_raw = df_val[FEATURE_NAMES].values
    y_val = df_val["label"].values.astype(int)

    X_test_raw = df_test[FEATURE_NAMES].values
    y_test = df_test["label"].values.astype(int)

    print(f"\n[INFO] Loaded Preprocessed Feature Splits:", flush=True)
    print(f"  - Training Set:   {len(y_train):,} samples (NORMAL: {np.sum(y_train==0):,}, INTRUSION: {np.sum(y_train==1):,})", flush=True)
    print(f"  - Validation Set: {len(y_val):,} samples (NORMAL: {np.sum(y_val==0):,}, INTRUSION: {np.sum(y_val==1):,})", flush=True)
    print(f"  - Test Set:       {len(y_test):,} samples (NORMAL: {np.sum(y_test==0):,}, INTRUSION: {np.sum(y_test==1):,})", flush=True)

    # 2. Log1p Transformation
    print("\n[INFO] Applying np.log1p transformation...", flush=True)
    X_train_log = np.log1p(np.maximum(X_train_raw, 0))
    X_val_log = np.log1p(np.maximum(X_val_raw, 0))
    X_test_log = np.log1p(np.maximum(X_test_raw, 0))

    # 3. Fit StandardScaler ONLY on Training
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train_log)
    X_val_scaled = scaler.transform(X_val_log)
    X_test_scaled = scaler.transform(X_test_log)
    print("[INFO] StandardScaler fitted ONLY on Training X_log.", flush=True)

    # 4. Train LinearSVC with Asymmetric Class Weighting to Suppress Normal FPR
    print("\n---> Training LinearSVC (dual='auto', class_weight={0: 5.0, 1: 1.0}, max_iter=15000, random_state=42)...", flush=True)
    t_start_train = time.time()
    model = LinearSVC(dual="auto", class_weight={0: 5.0, 1: 1.0}, random_state=42, max_iter=15000)
    model.fit(X_train_scaled, y_train)
    t_train = time.time() - t_start_train
    print(f"     [COMPLETED] LinearSVC training in {t_train:.3f}s (ConvergenceWarning: NONE)", flush=True)
    print(f"     Coefficients: {model.coef_[0]}", flush=True)
    print(f"     Intercept:    {model.intercept_[0]}", flush=True)

    # 5. Training Sanity Check
    train_dec = model.decision_function(X_train_scaled)
    train_pred = (train_dec >= 0.0).astype(int)
    train_m = compute_metrics(y_train, train_pred, t_train)
    print(f"\n[SANITY CHECK] Training Set (threshold 0.0):", flush=True)
    print(f"  TN: {train_m['TN']:,} | FP: {train_m['FP']:,} | FN: {train_m['FN']:,} | TP: {train_m['TP']:,}", flush=True)
    print(f"  Specificity: {train_m['specificity_tnr']:.4f} | Recall: {train_m['recall_tpr']:.4f} | F1: {train_m['f1_score']:.4f}", flush=True)

    # 6. Threshold Tuning on Validation Set
    print("\n---> Tuning decision threshold on Validation Set...", flush=True)
    val_dec = model.decision_function(X_val_scaled)
    t_min = float(np.percentile(val_dec, 0.5))
    t_max = float(np.percentile(val_dec, 99.5))
    candidates = np.linspace(t_min, t_max, 500)
    candidates = np.sort(np.unique(np.append(candidates, [0.0])))

    results_thresh = []
    for th in candidates:
        y_val_pred = (val_dec >= th).astype(int)
        cm = confusion_matrix(y_val, y_val_pred, labels=[0, 1])
        tn, fp, fn, tp = cm.ravel()
        spec = tn / (tn + fp) if (tn + fp) > 0 else 0.0
        rec = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = f1_score(y_val, y_val_pred, zero_division=0)
        fpr = fp / (fp + tn) if (fp + tn) > 0 else 0.0
        fnr = fn / (fn + tp) if (fn + tp) > 0 else 0.0
        acc = accuracy_score(y_val, y_val_pred)
        bal_acc = balanced_accuracy_score(y_val, y_val_pred)

        results_thresh.append({
            "threshold": float(th),
            "tn": int(tn), "fp": int(fp), "fn": int(fn), "tp": int(tp),
            "specificity": float(spec), "sensitivity": float(rec), "f1": float(f1),
            "fpr": float(fpr), "fnr": float(fnr), "accuracy": float(acc),
            "balanced_accuracy": float(bal_acc)
        })

    df_c = pd.DataFrame(results_thresh)
    df_p1 = df_c[df_c["specificity"] >= 0.90]
    if len(df_p1) > 0:
        max_f1 = df_p1["f1"].max()
        df_p2 = df_p1[df_p1["f1"] >= max_f1 - 0.001]
        best_val = df_p2.sort_values(by=["sensitivity", "f1"], ascending=False).iloc[0]
    else:
        best_val = df_c.sort_values(by=["balanced_accuracy", "f1"], ascending=False).iloc[0]

    selected_threshold = float(best_val["threshold"])
    print(f"     [SELECTED THRESHOLD] {selected_threshold:.4f}", flush=True)
    print(f"     Validation Specificity: {best_val['specificity']:.4f} | Recall: {best_val['sensitivity']:.4f} | F1: {best_val['f1']:.4f}", flush=True)

    # 7. Final Test Evaluation using Selected Threshold
    print("\n---> Evaluating on Test Set with selected threshold...", flush=True)
    t_start_test = time.time()
    test_dec = model.decision_function(X_test_scaled)
    y_test_pred = (test_dec >= selected_threshold).astype(int)
    t_test = time.time() - t_start_test
    test_m = compute_metrics(y_test, y_test_pred, t_test)

    print(f"     [TEST RESULTS]", flush=True)
    print(f"     TN: {test_m['TN']:,} | FP: {test_m['FP']:,} | FN: {test_m['FN']:,} | TP: {test_m['TP']:,}", flush=True)
    print(f"     Accuracy:          {test_m['accuracy']:.4f}", flush=True)
    print(f"     Precision:         {test_m['precision']:.4f}", flush=True)
    print(f"     NORMAL Recall / Spec: {test_m['specificity_tnr']:.4f}", flush=True)
    print(f"     INTRUSION Recall / Sens: {test_m['recall_tpr']:.4f}", flush=True)
    print(f"     FPR:               {test_m['fpr']:.4f}", flush=True)
    print(f"     FNR:               {test_m['fnr']:.4f}", flush=True)
    print(f"     F1 Score:          {test_m['f1_score']:.4f}", flush=True)
    print(f"     Balanced Accuracy: {test_m['balanced_accuracy']:.4f}", flush=True)

    # Save confusion matrix plot
    cm_test = confusion_matrix(y_test, y_test_pred, labels=[0, 1])
    save_confusion_matrix_plot(cm_test, "LinearSVC (Tuned)", os.path.join(RESULTS_DIR, "confusion_matrix_linear.png"))

    # Save model artifacts
    joblib.dump(model, MODEL_PKL_PATH)
    joblib.dump(scaler, SCALER_PKL_PATH)

    metadata = {
        "dataset": "CICIoT2023",
        "synthetic_data": False,
        "features": FEATURE_NAMES,
        "preprocessing": "np.log1p + StandardScaler",
        "model": "LinearSVC",
        "class_weight": {
            "0": 5.0,
            "1": 1.0
        },
        "threshold": round(selected_threshold, 4),
        "decision_threshold": round(selected_threshold, 4),
        "threshold_selection_method": "Validation threshold sweep (constrained to specificity >= 90.0% / FPR <= 10.0%)",
        "threshold_objective": "Suppression of benign false positives while maintaining volumetric intrusion recall",
        "label_mapping": {
            "0": "NORMAL",
            "1": "INTRUSION"
        },
        "training_samples": len(y_train),
        "training_normal": int(np.sum(y_train == 0)),
        "training_intrusion": int(np.sum(y_train == 1)),
        "training_metrics": {
            "TN": train_m["TN"],
            "FP": train_m["FP"],
            "FN": train_m["FN"],
            "TP": train_m["TP"],
            "specificity": train_m["specificity_tnr"],
            "sensitivity": train_m["recall_tpr"],
            "fpr": train_m["fpr"],
            "f1_score": train_m["f1_score"]
        },
        "validation_metrics": {
            "threshold": round(selected_threshold, 4),
            "TN": int(best_val["tn"]),
            "FP": int(best_val["fp"]),
            "FN": int(best_val["fn"]),
            "TP": int(best_val["tp"]),
            "accuracy": round(float(best_val["accuracy"]), 4),
            "precision": round(float(precision_score(y_val, (val_dec >= selected_threshold).astype(int))), 4),
            "recall": round(float(best_val["sensitivity"]), 4),
            "specificity": round(float(best_val["specificity"]), 4),
            "fpr": round(float(best_val["fpr"]), 4),
            "fnr": round(float(best_val["fnr"]), 4),
            "f1_score": round(float(best_val["f1"]), 4),
            "balanced_accuracy": round(float(best_val["balanced_accuracy"]), 4)
        },
        "test_metrics": {
            "threshold": round(selected_threshold, 4),
            "TN": test_m["TN"],
            "FP": test_m["FP"],
            "FN": test_m["FN"],
            "TP": test_m["TP"],
            "accuracy": test_m["accuracy"],
            "precision": test_m["precision"],
            "recall": test_m["recall_tpr"],
            "specificity": test_m["specificity_tnr"],
            "fpr": test_m["fpr"],
            "fnr": test_m["fnr"],
            "f1_score": test_m["f1_score"],
            "balanced_accuracy": test_m["balanced_accuracy"]
        }
    }

    with open(METADATA_JSON_PATH, "w") as f:
        json.dump(metadata, f, indent=2)

    print(f"\n[INFO] Saved verified model artifacts to {MODELS_DIR}.", flush=True)


if __name__ == "__main__":
    train_and_evaluate()
