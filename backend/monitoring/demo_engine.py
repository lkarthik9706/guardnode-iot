import os
import time
import json
import threading
from backend.ml.model_service import model_service
from backend.monitoring.device_tracker import device_tracker

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DEMO_JSON_PATH = os.path.join(BASE_DIR, "data", "demo", "demo_traffic.json")

class DemoEngine:
    def __init__(self, broadcast_callback=None):
        self.is_running = False
        self.thread = None
        self.broadcast_callback = broadcast_callback
        self.demo_data = []
        self.load_demo_data()

    def load_demo_data(self):
        if os.path.exists(DEMO_JSON_PATH):
            try:
                with open(DEMO_JSON_PATH, "r") as f:
                    self.demo_data = json.load(f)
                print(f"[INFO] Loaded {len(self.demo_data)} demo traffic events.")
            except Exception as e:
                print(f"[ERROR] Failed to load demo JSON: {e}")
                self.demo_data = []

        if not self.demo_data:
            # Fallback inline demo records
            self.demo_data = [
                {
                    "device_ip": "192.168.1.15",
                    "mean_packet_rate": 810.4,
                    "median_packet_rate": 798.0,
                    "maximum_packet_rate": 850.0,
                    "packet_rate": 850.0
                },
                {
                    "device_ip": "192.168.1.10",
                    "mean_packet_rate": 22.5,
                    "median_packet_rate": 20.0,
                    "maximum_packet_rate": 35.0,
                    "packet_rate": 35.0
                },
                {
                    "device_ip": "192.168.1.88",
                    "mean_packet_rate": 1420.0,
                    "median_packet_rate": 1390.0,
                    "maximum_packet_rate": 1650.0,
                    "packet_rate": 1650.0
                }
            ]

    def start(self):
        if self.is_running:
            return
        self.is_running = True
        self.thread = threading.Thread(target=self._run_loop, daemon=True)
        self.thread.start()
        print("[INFO] Demo Engine started.")

    def stop(self):
        self.is_running = False
        print("[INFO] Demo Engine stopped.")

    def _run_loop(self):
        idx = 0
        while self.is_running:
            if not self.demo_data:
                time.sleep(1)
                continue

            event = self.demo_data[idx % len(self.demo_data)]
            idx += 1

            mean_r = float(event.get("mean_packet_rate", 50.0))
            median_r = float(event.get("median_packet_rate", 45.0))
            max_r = float(event.get("maximum_packet_rate", event.get("packet_rate", 60.0)))
            ip = event["device_ip"]

            # Predict via SVM Model Service
            pred_info = model_service.predict(mean_r, median_r, max_r)

            stats = {
                "mean_packet_rate": mean_r,
                "median_packet_rate": median_r,
                "max_packet_rate": max_r,
                "packet_rate": max_r
            }

            device_tracker.update_device(
                ip=ip,
                window_rate=max_r,
                packets_count=int(max_r),
                mode="DEMO",
                stats=stats,
                prediction_info=pred_info
            )
            device_tracker.record_traffic_snapshot()

            summary = device_tracker.get_summary()

            # Invoke WS broadcast if provided
            if self.broadcast_callback:
                try:
                    self.broadcast_callback(summary)
                except Exception:
                    pass

            time.sleep(1.5)

demo_engine = DemoEngine()
