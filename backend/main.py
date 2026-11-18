import os
import json
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from backend.ml.model_service import model_service
from backend.monitoring.interface_manager import detect_network_interfaces
from backend.monitoring.device_tracker import device_tracker
from backend.monitoring.demo_engine import demo_engine
from backend.monitoring.packet_monitor import packet_monitor

app = FastAPI(
    title="GUARDNODE IoT — Lightweight Intrusion Detection System API",
    version="1.0.0",
    description="Backend API for local network packet rate monitoring and SVM intrusion classification."
)

# CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# State variable: "DEMO" or "LIVE"
system_state = {
    "mode": "DEMO",
    "is_monitoring": True,
    "active_interface": "default"
}

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in list(self.active_connections):
            try:
                await connection.send_json(message)
            except Exception:
                self.disconnect(connection)

ws_manager = ConnectionManager()

def sync_broadcast(data: dict):
    """Bridge sync monitoring callbacks to async WebSocket broadcast if connected."""
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            asyncio.run_coroutine_threadsafe(ws_manager.broadcast(data), loop)
    except Exception:
        pass

# Attach callbacks
demo_engine.broadcast_callback = sync_broadcast
packet_monitor.broadcast_callback = sync_broadcast

# Start demo engine by default
demo_engine.start()

class ModeRequest(BaseModel):
    mode: str  # "LIVE" or "DEMO"
    interface: str = "default"

class MonitorStartRequest(BaseModel):
    interface: str = "default"

class PredictRequest(BaseModel):
    mean_packet_rate: float
    median_packet_rate: float
    max_packet_rate: float

@app.get("/api/health")
def health_check():
    is_mon = packet_monitor.is_running if system_state["mode"] == "LIVE" else demo_engine.is_running
    system_state["is_monitoring"] = is_mon
    return {
        "status": "healthy",
        "system": "GuardNode IoT IDS",
        "model_loaded": model_service.is_loaded,
        "mode": system_state["mode"],
        "is_monitoring": is_mon
    }

@app.get("/api/interfaces")
def get_interfaces():
    """Detect and return available local network interfaces."""
    return detect_network_interfaces()

@app.get("/api/status")
def get_status():
    if system_state["mode"] == "LIVE":
        is_mon = packet_monitor.is_running
        system_state["is_monitoring"] = is_mon
        summary = device_tracker.get_summary()
        return {
            "monitoring": is_mon,
            "mode": "LIVE",
            "interface": system_state["active_interface"],
            "devices_detected": summary["total_devices"],
            "packets_analyzed": summary["packets_analyzed"],
            "model_loaded": model_service.is_loaded,
            "scapy_error": packet_monitor.error_message,
            "summary": summary
        }
    else:
        is_mon = demo_engine.is_running
        system_state["is_monitoring"] = is_mon
        summary = device_tracker.get_summary()
        return {
            "monitoring": is_mon,
            "mode": "DEMO",
            "interface": system_state["active_interface"],
            "devices_detected": summary["total_devices"],
            "packets_analyzed": summary["packets_analyzed"],
            "model_loaded": model_service.is_loaded,
            "scapy_error": None,
            "summary": summary
        }

@app.post("/api/monitor/start")
def start_monitoring(req: MonitorStartRequest):
    """Starts packet monitoring process on selected interface."""
    system_state["active_interface"] = req.interface

    if system_state["mode"] == "DEMO":
        packet_monitor.stop()
        device_tracker.clear()
        demo_engine.start()
        system_state["is_monitoring"] = True
        return {"status": "started", "interface": req.interface, "mode": "DEMO"}
    else:
        demo_engine.stop()
        device_tracker.clear()
        success, msg = packet_monitor.start(req.interface)
        if not success:
            system_state["is_monitoring"] = False
            raise HTTPException(status_code=400, detail=msg)
        system_state["is_monitoring"] = True
        return {"status": "started", "interface": req.interface, "mode": "LIVE"}

@app.post("/api/monitor/stop")
def stop_monitoring():
    """Stops packet capture safely."""
    system_state["is_monitoring"] = False
    demo_engine.stop()
    packet_monitor.stop()
    return {"status": "stopped"}

@app.post("/api/mode")
def set_mode(req: ModeRequest):
    target_mode = req.mode.upper()
    if target_mode not in ["LIVE", "DEMO"]:
        raise HTTPException(status_code=400, detail="Mode must be LIVE or DEMO")

    system_state["mode"] = target_mode
    system_state["active_interface"] = req.interface

    if target_mode == "DEMO":
        packet_monitor.stop()
        device_tracker.clear()
        demo_engine.start()
        system_state["is_monitoring"] = True
    else:
        demo_engine.stop()
        device_tracker.clear()
        success, msg = packet_monitor.start(req.interface)
        system_state["is_monitoring"] = packet_monitor.is_running

        if not success:
            print(f"[WARNING] Live capture failed: {msg}")

    return {
        "status": "success",
        "mode": system_state["mode"],
        "is_monitoring": system_state["is_monitoring"],
        "scapy_error": packet_monitor.error_message
    }

@app.get("/api/devices")
def get_devices():
    summary = device_tracker.get_summary()
    return summary["devices"]

@app.get("/api/devices/{ip}")
def get_device_detail(ip: str):
    devs = device_tracker.devices
    if ip not in devs:
        raise HTTPException(status_code=404, detail="Device not found")
    d = dict(devs[ip])
    d["rate_history"] = list(devs[ip]["rate_history"])
    return d

@app.get("/api/traffic")
def get_traffic():
    summary = device_tracker.get_summary()
    return {
        "average_packet_rate": summary["average_packet_rate"],
        "total_packet_rate": summary["total_packet_rate"],
        "traffic_history": summary["traffic_history"]
    }

@app.get("/api/demo/traffic")
def get_demo_traffic():
    """Explicit endpoint for demo traffic data."""
    summary = device_tracker.get_summary()
    return {
        "source": "CICIoT2023 Demo Stream",
        "average_packet_rate": summary["average_packet_rate"],
        "total_packet_rate": summary["total_packet_rate"],
        "traffic_history": summary["traffic_history"]
    }

@app.get("/api/alerts")
def get_alerts():
    summary = device_tracker.get_summary()
    return summary["alerts"]

@app.get("/api/model")
def get_model_info():
    if model_service.metadata:
        return model_service.metadata
    return {
        "model_type": "Support Vector Machine (SVM)",
        "best_kernel": "linear",
        "features": ["mean_packet_rate", "median_packet_rate", "max_packet_rate"],
        "units": "packets/second",
        "status": "Trained model metadata available"
    }

@app.post("/api/predict")
def predict_endpoint(req: PredictRequest):
    return model_service.predict(
        mean_packet_rate=req.mean_packet_rate,
        median_packet_rate=req.median_packet_rate,
        max_packet_rate=req.max_packet_rate
    )

@app.post("/api/demo/predict")
def demo_predict_endpoint(req: PredictRequest):
    """Explicit endpoint for demo prediction testing."""
    return model_service.predict(
        mean_packet_rate=req.mean_packet_rate,
        median_packet_rate=req.median_packet_rate,
        max_packet_rate=req.max_packet_rate
    )

@app.websocket("/ws/live")
async def websocket_live(websocket: WebSocket):
    await ws_manager.connect(websocket)
    summary = device_tracker.get_summary()
    await websocket.send_json(summary)
    try:
        while True:
            data = await websocket.receive_text()
            if data == "ping":
                await websocket.send_text("pong")
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)

# Mount built frontend static files for monolithic / single-port deployment
frontend_dist = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend", "dist"))
if os.path.exists(frontend_dist):
    app.mount("/", StaticFiles(directory=frontend_dist, html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)
