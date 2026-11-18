import time
import threading
from collections import defaultdict
from backend.monitoring.device_tracker import device_tracker
from backend.monitoring.feature_extractor import compute_window_rate, WINDOW_SECONDS
from backend.monitoring.interface_manager import resolve_active_interface

SCAPY_AVAILABLE = False
try:
    from scapy.all import sniff, conf
    SCAPY_AVAILABLE = True
except Exception:
    SCAPY_AVAILABLE = False

class PacketMonitor:
    def __init__(self, broadcast_callback=None):
        self.is_running = False
        self.interface = None
        self.thread = None
        self.broadcast_callback = broadcast_callback
        self.window_packet_counts = defaultdict(int)
        self.last_window_time = time.time()
        self.error_message = None
        self.total_packets_captured = 0

    def start(self, interface: str = "default"):
        self.stop()
        # Resolve active physical adapter (guards against dummy WAN miniports)
        resolved_iface = resolve_active_interface(interface)
        self.interface = resolved_iface
        self.error_message = None
        self.is_running = False
        self.total_packets_captured = 0
        self.window_packet_counts.clear()
        self.last_window_time = time.time()

        if not SCAPY_AVAILABLE:
            self.error_message = "Scapy or Npcap is not available. Please install Npcap on Windows for live packet capture."
            print(f"[WARNING] {self.error_message}")
            return False, self.error_message

        # Synchronously attempt test sniff on the resolved interface
        test_kwargs = {"store": False, "timeout": 0.05, "count": 1}
        if resolved_iface and resolved_iface not in ["default", "demo", "loopback"]:
            test_kwargs["iface"] = resolved_iface

        try:
            sniff(**test_kwargs)
        except Exception as e:
            err_str = str(e)
            if "winpcap is not installed" in err_str or "libpcap provider" in err_str:
                self.error_message = "Packet capture could not be started: Npcap / WinPcap driver is not installed on Windows."
            else:
                self.error_message = f"Packet capture could not be started on interface '{resolved_iface}': {err_str}"
            print(f"[ERROR] Scapy capture test failed: {self.error_message}")
            self.is_running = False
            return False, self.error_message

        self.is_running = True
        self.thread = threading.Thread(target=self._sniff_loop, daemon=True)
        self.thread.start()
        print(f"[INFO] Scapy packet monitor started on interface: {resolved_iface} (requested: {interface})")
        return True, "Packet capture started"

    def stop(self):
        self.is_running = False
        print("[INFO] Scapy packet monitor stopped.")
        return {"status": "stopped"}

    def _sniff_loop(self):
        try:
            kwargs = {"prn": self._packet_callback, "store": False, "timeout": 1.0}
            if self.interface and self.interface not in ["default", "demo", "loopback"]:
                kwargs["iface"] = self.interface

            while self.is_running:
                sniff(**kwargs)
                self._evaluate_observation_window()
        except Exception as e:
            err_str = str(e)
            if "winpcap is not installed" in err_str or "libpcap provider" in err_str:
                self.error_message = "Packet capture could not be started: Npcap / WinPcap driver is not installed on Windows."
            else:
                self.error_message = f"Packet capture could not be started on interface '{self.interface}': {err_str}"
            print(f"[ERROR] Scapy capture failure: {e}")
            self.is_running = False

    def _packet_callback(self, pkt):
        try:
            src_ip = None
            if pkt.haslayer("IP"):
                src_ip = pkt["IP"].src
            elif pkt.haslayer("IPv6"):
                src_ip = pkt["IPv6"].src

            if src_ip:
                self.window_packet_counts[src_ip] += 1
                self.total_packets_captured += 1
                device_tracker.increment_packet_count(src_ip)
        except Exception:
            pass

    def _evaluate_observation_window(self):
        now = time.time()
        elapsed = now - self.last_window_time
        
        # Fast initial evaluation after 1.5s for newly detected devices; standard 5s interval thereafter
        has_new_devices = len(device_tracker.devices) > 0 and any(d.get("completed_windows", 0) == 0 for d in device_tracker.devices.values())
        if elapsed < WINDOW_SECONDS and not (elapsed >= 1.5 and has_new_devices):
            return

        self.last_window_time = now

        # Snapshot active counts for the current window and clear buffer
        current_counts = dict(self.window_packet_counts)
        self.window_packet_counts.clear()

        # Combine currently active IPs and already tracked endpoints
        all_ips = set(current_counts.keys()).union(device_tracker.devices.keys())

        for ip in all_ips:
            count = current_counts.get(ip, 0)
            window_rate = compute_window_rate(count, elapsed)
            device_tracker.update_device(
                ip=ip,
                window_rate=window_rate,
                packets_count=count,
                mode="LIVE"
            )

        device_tracker.record_traffic_snapshot()
        summary = device_tracker.get_summary()

        if self.broadcast_callback:
            try:
                self.broadcast_callback(summary)
            except Exception:
                pass

packet_monitor = PacketMonitor()


