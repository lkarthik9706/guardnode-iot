const isDev = window.location.hostname === "localhost" && window.location.port === "5173";
const API_BASE = isDev ? "http://127.0.0.1:8000/api" : `${window.location.origin}/api`;
const wsProtocol = window.location.protocol === "https:" ? "wss:" : "ws:";
const WS_BASE = isDev ? "ws://127.0.0.1:8000/ws/live" : `${wsProtocol}//${window.location.host}/ws/live`;

export async function fetchStatus() {
  try {
    const res = await fetch(`${API_BASE}/status`);
    return await res.json();
  } catch (err) {
    console.error("API status error:", err);
    return null;
  }
}

export async function fetchDevices() {
  try {
    const res = await fetch(`${API_BASE}/devices`);
    return await res.json();
  } catch (err) {
    return [];
  }
}

export async function fetchModelInfo() {
  try {
    const res = await fetch(`${API_BASE}/model`);
    return await res.json();
  } catch (err) {
    return null;
  }
}

export async function fetchInterfaces() {
  try {
    const res = await fetch(`${API_BASE}/interfaces`);
    return await res.json();
  } catch (err) {
    return [];
  }
}

export async function setMode(mode, iface = "default") {
  try {
    const res = await fetch(`${API_BASE}/mode`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ mode, interface: iface }),
    });
    return await res.json();
  } catch (err) {
    return { status: "error", message: err.message };
  }
}

export function connectWebSocket(onMessage, onError) {
  let ws = new WebSocket(WS_BASE);

  ws.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data);
      onMessage(data);
    } catch (err) {
      console.error("WS JSON parse error:", err);
    }
  };

  ws.onerror = (err) => {
    if (onError) onError(err);
  };

  ws.onclose = () => {
    // Retry connection after 3s
    setTimeout(() => {
      connectWebSocket(onMessage, onError);
    }, 3000);
  };

  return ws;
}
