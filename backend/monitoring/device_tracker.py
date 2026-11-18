import ipaddress
import time
from datetime import datetime
from collections import deque
from backend.ml.model_service import model_service
from backend.monitoring.feature_extractor import (
    compute_lightweight_features,
    MIN_OBSERVATION_WINDOWS,
    MAX_RATE_HISTORY
)

def classify_ip_endpoint(ip_str: str) -> str:
    """
    Classifies an IP address as 'LOCAL' or 'EXTERNAL'.
    Recognizes private IPv4 (10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16, 127.0.0.0/8)
    and IPv6 link-local, loopback, multicast.
    """
    try:
        ip_obj = ipaddress.ip_address(ip_str)
        if ip_obj.is_private or ip_obj.is_loopback or ip_obj.is_link_local or ip_obj.is_multicast:
            return "LOCAL"
        return "EXTERNAL"
    except Exception:
        return "LOCAL"

class DeviceTracker:
    def __init__(self):
        self.devices = {}
        self.alerts = deque(maxlen=MAX_RATE_HISTORY)
        self.traffic_history = deque(maxlen=MAX_RATE_HISTORY)
        self.packets_analyzed = 0

    def clear(self):
        """Clears device table, alerts, traffic history, and resets packets analyzed count."""
        self.devices = {}
        self.alerts.clear()
        self.traffic_history.clear()
        self.packets_analyzed = 0

    def get_device_name(self, ip: str, mode: str = "DEMO"):
        if mode == "LIVE":
            endpoint_type = classify_ip_endpoint(ip)
            if ip == "127.0.0.1":
                return "Localhost Agent"
            if endpoint_type == "LOCAL":
                known_local = {
                    "192.168.1.1": "Gateway Router",
                    "10.0.0.1": "Gateway Router",
                    "172.16.0.1": "Gateway Router"
                }
                return known_local.get(ip, "Local Network Endpoint")
            else:
                return "Unknown Endpoint"
        else:
            known_hosts = {
                "127.0.0.1": "Localhost Agent",
                "192.168.1.1": "Gateway Router",
                "192.168.1.10": "Smart Thermostat",
                "192.168.1.15": "IoT Security Camera",
                "192.168.1.22": "Smart Door Lock",
                "192.168.1.45": "Smart TV Hub"
            }
            return known_hosts.get(ip, "Unknown Device")

    def increment_packet_count(self, ip: str, count: int = 1):
        """
        Increment packets_analyzed and immediately register live endpoints upon first observation
        so they appear on the dashboard in real time rather than waiting for window completion.
        """
        self.packets_analyzed += count
        now_str = datetime.now().strftime("%H:%M:%S")

        if ip not in self.devices:
            self.devices[ip] = {
                "ip": ip,
                "name": self.get_device_name(ip, mode="LIVE"),
                "endpoint_type": classify_ip_endpoint(ip),
                "packet_rate": 0.0,
                "mean_packet_rate": 0.0,
                "median_packet_rate": 0.0,
                "max_packet_rate": 0.0,
                "maximum_packet_rate": 0.0,
                "status": "OBSERVING",
                "last_seen": now_str,
                "first_seen": now_str,
                "packet_count": count,
                "completed_windows": 0,
                "intrusion_count": 0,
                "rate_history": deque(maxlen=MAX_RATE_HISTORY)
            }
        else:
            self.devices[ip]["packet_count"] += count
            self.devices[ip]["last_seen"] = now_str

    def update_device(self, ip: str, window_rate: float = 0.0, packets_count: int = 0, mode: str = "LIVE", stats: dict = None, prediction_info: dict = None):
        """
        Updates telemetry state for an observed endpoint.
        Supports both LIVE observation-window rates and DEMO traffic events.
        """
        now_str = datetime.now().strftime("%H:%M:%S")
        name = self.get_device_name(ip, mode=mode)
        endpoint_type = classify_ip_endpoint(ip)

        if mode == "DEMO":
            self.packets_analyzed += packets_count
            mean_r = stats["mean_packet_rate"] if stats else window_rate
            median_r = stats["median_packet_rate"] if stats else window_rate
            max_r = stats["max_packet_rate"] if stats else window_rate
            packet_r = stats.get("packet_rate", max_r) if stats else window_rate
            pred_label = prediction_info["prediction"] if prediction_info else "NORMAL"

            if ip not in self.devices:
                self.devices[ip] = {
                    "ip": ip,
                    "name": name,
                    "endpoint_type": endpoint_type,
                    "packet_rate": packet_r,
                    "mean_packet_rate": mean_r,
                    "median_packet_rate": median_r,
                    "max_packet_rate": max_r,
                    "maximum_packet_rate": max_r,
                    "status": pred_label,
                    "last_seen": now_str,
                    "first_seen": now_str,
                    "packet_count": packets_count,
                    "completed_windows": 2,
                    "intrusion_count": 1 if pred_label == "INTRUSION" else 0,
                    "rate_history": deque(maxlen=MAX_RATE_HISTORY)
                }

            dev = self.devices[ip]
            dev["packet_rate"] = packet_r
            dev["mean_packet_rate"] = mean_r
            dev["median_packet_rate"] = median_r
            dev["max_packet_rate"] = max_r
            dev["maximum_packet_rate"] = max_r
            dev["status"] = pred_label
            dev["last_seen"] = now_str
            dev["packet_count"] += packets_count
            dev["completed_windows"] += 1
            dev["rate_history"].append({"timestamp": now_str, "rate": packet_r})

            if pred_label == "INTRUSION":
                dev["intrusion_count"] += 1
                self.alerts.appendleft({
                    "timestamp": now_str,
                    "device_ip": ip,
                    "device_name": name,
                    "endpoint_type": endpoint_type,
                    "packet_rate": packet_r,
                    "mean_packet_rate": mean_r,
                    "median_packet_rate": median_r,
                    "maximum_packet_rate": max_r,
                    "prediction": "INTRUSION",
                    "status": "ML PREDICTION: INTRUSION"
                })
            return dev

        # LIVE MODE LOGIC:
        if ip not in self.devices:
            self.devices[ip] = {
                "ip": ip,
                "name": name,
                "endpoint_type": endpoint_type,
                "packet_rate": window_rate,
                "mean_packet_rate": window_rate,
                "median_packet_rate": window_rate,
                "max_packet_rate": window_rate,
                "maximum_packet_rate": window_rate,
                "status": "OBSERVING",
                "last_seen": now_str,
                "first_seen": now_str,
                "packet_count": packets_count,
                "completed_windows": 0,
                "intrusion_count": 0,
                "rate_history": deque(maxlen=MAX_RATE_HISTORY)
            }

        dev = self.devices[ip]
        dev["packet_count"] += packets_count
        dev["last_seen"] = now_str
        dev["packet_rate"] = window_rate

        # Append completed observation window rate
        dev["rate_history"].append({
            "timestamp": now_str,
            "rate": window_rate
        })
        dev["completed_windows"] = len(dev["rate_history"])

        rates = [item["rate"] for item in dev["rate_history"]]
        mean_r, median_r, max_r = compute_lightweight_features(rates)

        dev["mean_packet_rate"] = mean_r
        dev["median_packet_rate"] = median_r
        dev["max_packet_rate"] = max_r
        dev["maximum_packet_rate"] = max_r

        # Minimum Observation Requirement
        if dev["completed_windows"] < MIN_OBSERVATION_WINDOWS:
            dev["status"] = "OBSERVING"
        else:
            # Predict via SVM Model Service
            pred_info = model_service.predict(mean_r, median_r, max_r)
            pred = pred_info.get("prediction", "NORMAL")
            dev["status"] = pred

            if pred == "INTRUSION":
                dev["intrusion_count"] += 1
                alert_event = {
                    "timestamp": now_str,
                    "device_ip": ip,
                    "device_name": name,
                    "endpoint_type": endpoint_type,
                    "packet_rate": window_rate,
                    "mean_packet_rate": mean_r,
                    "median_packet_rate": median_r,
                    "maximum_packet_rate": max_r,
                    "prediction": "INTRUSION",
                    "status": "ML PREDICTION: INTRUSION"
                }
                self.alerts.appendleft(alert_event)

        return dev

    def record_traffic_snapshot(self):
        now_str = datetime.now().strftime("%H:%M:%S")
        dev_list = list(self.devices.values())
        if not dev_list:
            self.traffic_history.append({
                "timestamp": now_str,
                "total_packet_rate": 0.0,
                "average_packet_rate": 0.0,
                "active_devices": 0,
                "active_intrusions": 0
            })
            return

        total_rate = sum(d["packet_rate"] for d in dev_list)
        avg_rate = round(total_rate / len(dev_list), 2) if dev_list else 0.0
        intrusions = sum(1 for d in dev_list if d["status"] == "INTRUSION")

        self.traffic_history.append({
            "timestamp": now_str,
            "total_packet_rate": round(total_rate, 2),
            "average_packet_rate": avg_rate,
            "active_devices": len(dev_list),
            "active_intrusions": intrusions
        })

    def get_summary(self):
        dev_list = list(self.devices.values())
        formatted_devices = []
        normal_count = 0
        intrusion_count = 0
        observing_count = 0
        local_count = 0
        external_count = 0
        total_rate = 0.0

        for d in dev_list:
            item = dict(d)
            item["rate_history"] = list(d["rate_history"])
            formatted_devices.append(item)

            if d.get("endpoint_type") == "EXTERNAL":
                external_count += 1
            else:
                local_count += 1

            if d["status"] == "INTRUSION":
                intrusion_count += 1
            elif d["status"] == "OBSERVING":
                observing_count += 1
            else:
                normal_count += 1

            total_rate += d["packet_rate"]

        avg_rate = round(total_rate / len(dev_list), 2) if dev_list else 0.0

        return {
            "total_devices": len(dev_list),
            "local_endpoints": local_count,
            "external_endpoints": external_count,
            "observing_devices": observing_count,
            "normal_devices": normal_count,
            "active_intrusions": intrusion_count,
            "average_packet_rate": avg_rate,
            "total_packet_rate": round(total_rate, 2),
            "packets_analyzed": self.packets_analyzed,
            "devices": formatted_devices,
            "alerts": list(self.alerts),
            "traffic_history": list(self.traffic_history)
        }

device_tracker = DeviceTracker()


