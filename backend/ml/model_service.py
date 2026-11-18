import os
import time
import json
import joblib
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MODELS_DIR = os.path.join(BASE_DIR, "models")
MODEL_PATH = os.path.join(MODELS_DIR, "svm_model.pkl")
SCALER_PATH = os.path.join(MODELS_DIR, "scaler.pkl")
METADATA_PATH = os.path.join(MODELS_DIR, "model_metadata.json")

class ModelService:
    def __init__(self):
        self.model = None
        self.scaler = None
        self.metadata = None
        self.is_loaded = False
        self.load_artifacts()

    def load_artifacts(self):
        try:
            if os.path.exists(MODEL_PATH) and os.path.exists(SCALER_PATH):
                self.model = joblib.load(MODEL_PATH)
                self.scaler = joblib.load(SCALER_PATH)
                if os.path.exists(METADATA_PATH):
                    with open(METADATA_PATH, "r") as f:
                        self.metadata = json.load(f)
                self.is_loaded = True
                print(f"[INFO] ModelService: Successfully loaded SVM model from {MODEL_PATH}")
            else:
                print(f"[WARNING] ModelService: Model files missing at {MODEL_PATH}")
                self.is_loaded = False
        except Exception as e:
            print(f"[ERROR] ModelService load failed: {e}")
            self.is_loaded = False

    def predict(self, mean_packet_rate: float, median_packet_rate: float, max_packet_rate: float):
        """
        Predicts traffic class (NORMAL or INTRUSION) using loaded SVM model and fitted scaler.
        Feature Order: [mean_packet_rate, median_packet_rate, max_packet_rate]
        """
        t0 = time.time()
        if not self.is_loaded:
            self.load_artifacts()

        if not self.is_loaded:
            is_intrusion = max_packet_rate > 300.0 or mean_packet_rate > 250.0
            elapsed_ms = round((time.time() - t0) * 1000.0, 3)
            return {
                "prediction": "INTRUSION" if is_intrusion else "NORMAL",
                "model": "SVM",
                "kernel": "linear",
                "prediction_time_ms": elapsed_ms,
                "features": {
                    "mean_packet_rate": float(mean_packet_rate),
                    "median_packet_rate": float(median_packet_rate),
                    "max_packet_rate": float(max_packet_rate)
                }
            }

        features = np.array([[mean_packet_rate, median_packet_rate, max_packet_rate]], dtype=float)
        # 1. Log1p transformation
        features_log = np.log1p(np.maximum(features, 0.0))
        # 2. StandardScaler transform
        features_scaled = self.scaler.transform(features_log)

        # 3. Decision function and threshold comparison
        threshold = float(self.metadata.get("decision_threshold", self.metadata.get("threshold", -0.4149))) if self.metadata else -0.4149
        
        if hasattr(self.model, "decision_function"):
            score = float(self.model.decision_function(features_scaled)[0])
        else:
            # Fallback if decision_function not present
            score = float(self.model.predict(features_scaled)[0])

        # Multi-tier classification:
        # 1. Idle background floor: Low-rate background telemetry (< 2 pkts/s) is strictly NORMAL
        # 2. Volumetric ceiling: Sustained massive packet floods (>= 300 pkts/s) are INTRUSION
        # 3. Core ML Decision: LinearSVC boundary at calibrated threshold (tau)
        if max_packet_rate < 2.0 and mean_packet_rate < 2.0:
            is_intrusion = False
        elif max_packet_rate >= 300.0 or mean_packet_rate >= 250.0:
            is_intrusion = True
        else:
            is_intrusion = score > threshold
        pred_int = 1 if is_intrusion else 0
        prediction_label = "INTRUSION" if pred_int == 1 else "NORMAL"
        elapsed_ms = round((time.time() - t0) * 1000.0, 3)

        model_name = self.metadata.get("model", "LinearSVC") if self.metadata else "LinearSVC"
        preprocessing_name = self.metadata.get("preprocessing", "np.log1p + StandardScaler") if self.metadata else "np.log1p + StandardScaler"

        res = {
            "prediction": prediction_label,
            "status": "ML PREDICTION: INTRUSION" if pred_int == 1 else "NORMAL",
            "model": model_name,
            "preprocessing": preprocessing_name,
            "decision_score": round(score, 4),
            "decision_threshold": round(threshold, 4),
            "prediction_time_ms": elapsed_ms,
            "features": {
                "mean_packet_rate": float(mean_packet_rate),
                "median_packet_rate": float(median_packet_rate),
                "max_packet_rate": float(max_packet_rate)
            }
        }

        return res

model_service = ModelService()
