import os
import sys
import time
import json
import joblib
import numpy as np
import pandas as pd
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
)

# Optional matplotlib/seaborn imports for PNG generation
HAS_PLOTTING = False
try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import seaborn as sns
    HAS_PLOTTING = True
except Exception:
    HAS_PLOTTING = False

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED_CSV_PATH = os.path.join(BASE_DIR, "data", "processed", "train_features.csv")
MODELS_DIR = os.path.join(BASE_DIR, "models")
RESULTS_DIR = os.path.join(BASE_DIR, "results")

os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)

MODEL_PKL_PATH = os.path.join(MODELS_DIR, "svm_model.pkl")
SCALER_PKL_PATH = os.path.join(MODELS_DIR, "scaler.pkl")
METADATA_JSON_PATH = os.path.join(MODELS_DIR, "model_metadata.json")

# Mandatory Features & Order
FEATURE_NAMES = ["mean_packet_rate", "median_packet_rate", "max_packet_rate"]
CLASS_NAMES = ["NORMAL", "ATTACK"]
RANDOM_STATE = 42

def save_confusion_matrix_plot(cm, kernel_name, filepath):
    """Saves a confusion matrix plot PNG file."""
    if not HAS_PLOTTING:
        print(f"[NOTE] Matplotlib not available, skipping plot: {filepath}")
        return
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", 
                xticklabels=CLASS_NAMES, yticklabels=CLASS_NAMES)
    plt.title(f"Confusion Matrix - SVM ({kernel_name.capitalize()} Kernel)")
    plt.xlabel("Predicted Label")
    plt.ylabel("True Label")
    plt.tight_layout()
    plt.savefig(filepath, dpi=300)
    plt.close()
    print(f"[SUCCESS] Saved confusion matrix image: {filepath}")

def save_bar_comparison_plot(kernels, values, metric_name, filepath, color="skyblue"):
    """Saves a bar comparison plot PNG file."""
    if not HAS_PLOTTING:
        print(f"[NOTE] Matplotlib not available, skipping plot: {filepath}")
        return
    plt.figure(figsize=(7, 4.5))
    bars = plt.bar([k.capitalize() for k in kernels], values, color=color, width=0.4)
    plt.title(f"SVM Kernel Comparison - {metric_name}")
    plt.ylabel(metric_name)
    plt.ylim(0, 1.1)
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, yval + 0.02, f"{yval:.4f}", ha="center", va="bottom", fontsize=10)
    plt.tight_layout()
    plt.savefig(filepath, dpi=300)
    plt.close()
    print(f"[SUCCESS] Saved comparison plot: {filepath}")

def train_and_evaluate_phase2():
    print("\n" + "="*70)
    print("      GUARDNODE IoT — PHASE 2: SVM MODEL TRAINING & EVALUATION")
    print("="*70)

    if not os.path.exists(PROCESSED_CSV_PATH):
        print(f"[INFO] Processed features missing at '{PROCESSED_CSV_PATH}'. Running dataset inspection...")
        from scripts.inspect_dataset import inspect_and_preprocess
        inspect_and_preprocess()

    df = pd.read_csv(PROCESSED_CSV_PATH)
    print(f"[INFO] Loaded preprocessed dataset with {len(df)} samples.")
    
    # Validate columns
    for col in FEATURE_NAMES + ["label"]:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")

    X = df[FEATURE_NAMES].values
    y = df["label"].values

    # Step 6: 80/20 train/test split with stratification
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y
    )
    print(f"[INFO] Dataset split: {len(X_train)} training samples, {len(X_test)} testing samples.")

    # Step 6: Fit StandardScaler ONLY on X_train (avoids data leakage)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    print("[INFO] StandardScaler fitted strictly on training set (X_train).")

    # Step 7: Train 3 SVM Kernels (Linear, Polynomial, RBF)
    kernels = ["linear", "poly", "rbf"]
    results = {}
    best_kernel = None
    best_score = -1.0
    best_model = None

    print("\n[INFO] Training Linear, Polynomial, and RBF SVM models...\n")

    comparison_rows = []

    for k in kernels:
        # Fit model
        t0 = time.time()
        model = SVC(kernel=k, probability=True, random_state=RANDOM_STATE)
        model.fit(X_train_scaled, y_train)
        train_time = round(time.time() - t0, 4)

        # Inference on test set
        t_pred_start = time.time()
        y_pred = model.predict(X_test_scaled)
        pred_time = round(time.time() - t_pred_start, 4)

        # Calculate exact metrics
        acc = float(accuracy_score(y_test, y_pred))
        prec = float(precision_score(y_test, y_pred, zero_division=0))
        rec = float(recall_score(y_test, y_pred, zero_division=0))
        f1 = float(f1_score(y_test, y_pred, zero_division=0))

        cm = confusion_matrix(y_test, y_pred)
        tn, fp, fn, tp = cm.ravel()

        fpr = float(fp / (fp + tn)) if (fp + tn) > 0 else 0.0
        fnr = float(fn / (fn + tp)) if (fn + tp) > 0 else 0.0

        res = {
            "kernel": k,
            "accuracy": round(acc, 4),
            "precision": round(prec, 4),
            "recall": round(rec, 4),
            "tpr": round(rec, 4),
            "f1_score": round(f1, 4),
            "fpr": round(fpr, 4),
            "fnr": round(fnr, 4),
            "training_time": train_time,
            "prediction_time": pred_time,
            "confusion_matrix": {"TN": int(tn), "FP": int(fp), "FN": int(fn), "TP": int(tp)}
        }
        results[k] = res

        comparison_rows.append({
            "Kernel": k.capitalize(),
            "Accuracy": round(acc, 4),
            "Precision": round(prec, 4),
            "Recall_TPR": round(rec, 4),
            "F1_Score": round(f1, 4),
            "FPR": round(fpr, 4),
            "FNR": round(fnr, 4),
            "Training_Time_Sec": train_time,
            "Prediction_Time_Sec": pred_time,
            "TN": int(tn),
            "FP": int(fp),
            "FN": int(fn),
            "TP": int(tp)
        })

        # Save confusion matrix plot
        cm_path = os.path.join(RESULTS_DIR, f"confusion_matrix_{k}.png")
        save_confusion_matrix_plot(cm, k, cm_path)

        # Select best model based on high F1, high Accuracy, low FPR
        composite_score = f1 + acc - (2.0 * fpr)
        if composite_score > best_score:
            best_score = composite_score
            best_kernel = k
            best_model = model

    # Step 8: Print clean comparison table in console
    print("\n" + "-"*82)
    print("                          SVM KERNEL COMPARISON")
    print("-"*82)
    print(f"{'Kernel':<12} | {'Accuracy':<10} | {'Precision':<10} | {'Recall':<10} | {'F1':<10} | {'FPR':<8} | {'Train Time (s)':<12}")
    print("-"*82)
    for k in kernels:
        r = results[k]
        print(f"{r['kernel'].capitalize():<12} | {r['accuracy']:<10.4f} | {r['precision']:<10.4f} | {r['recall']:<10.4f} | {r['f1_score']:<10.4f} | {r['fpr']:<8.4f} | {r['training_time']:<12.4f}")
    print("-"*82)

    # Step 9: Save model comparison CSV
    comp_df = pd.DataFrame(comparison_rows)
    comp_csv_path = os.path.join(RESULTS_DIR, "model_comparison.csv")
    comp_df.to_csv(comp_csv_path, index=False)
    print(f"\n[SUCCESS] Model comparison table saved to: {comp_csv_path}")

    # Save Comparison Plots
    acc_plot_path = os.path.join(RESULTS_DIR, "kernel_accuracy_comparison.png")
    f1_plot_path = os.path.join(RESULTS_DIR, "kernel_f1_comparison.png")
    
    accuracies = [results[k]["accuracy"] for k in kernels]
    f1_scores = [results[k]["f1_score"] for k in kernels]
    
    save_bar_comparison_plot(kernels, accuracies, "Accuracy", acc_plot_path, color="#3B82F6")
    save_bar_comparison_plot(kernels, f1_scores, "F1-Score", f1_plot_path, color="#10B981")

    # Step 10: Select & Print Best Model
    best_res = results[best_kernel]
    print(f"\nBEST MODEL:\n{best_kernel.upper()} Kernel")
    print(f"REASON:\nSelected '{best_kernel.upper()}' kernel achieved F1-Score of {best_res['f1_score']:.4f}, Accuracy of {best_res['accuracy']:.4f}, FPR of {best_res['fpr']:.4f}, and ultra-low training time of {best_res['training_time']} seconds.")

    # Step 11: Save production model, scaler, metadata
    joblib.dump(best_model, MODEL_PKL_PATH)
    joblib.dump(scaler, SCALER_PKL_PATH)
    print(f"\n[SUCCESS] Saved production model to: {MODEL_PKL_PATH}")
    print(f"[SUCCESS] Saved fitted scaler to: {SCALER_PKL_PATH}")

    metadata = {
        "model": "SVM",
        "kernel": best_kernel,
        "features": FEATURE_NAMES,
        "classes": CLASS_NAMES,
        "accuracy": best_res["accuracy"],
        "precision": best_res["precision"],
        "recall": best_res["recall"],
        "tpr": best_res["tpr"],
        "fpr": best_res["fpr"],
        "fnr": best_res["fnr"],
        "f1_score": best_res["f1_score"],
        "training_time": best_res["training_time"],
        "prediction_time": best_res["prediction_time"],
        "training_date": datetime.now().isoformat(),
        "num_train_samples": len(X_train),
        "num_test_samples": len(X_test),
        "confusion_matrix": best_res["confusion_matrix"],
        "all_kernel_results": results
    }

    with open(METADATA_JSON_PATH, "w") as f:
        json.dump(metadata, f, indent=2)
    print(f"[SUCCESS] Saved metadata to: {METADATA_JSON_PATH}\n")

    return metadata

if __name__ == "__main__":
    train_and_evaluate_phase2()
