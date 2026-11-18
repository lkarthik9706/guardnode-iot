const isDev = window.location.hostname === "localhost" && window.location.port === "5173";
const API_BASE_URL = isDev ? "http://localhost:8000/api" : `${window.location.origin}/api`;

async function fetchJSON(endpoint, options = {}) {
  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      ...options,
      headers: {
        "Content-Type": "application/json",
        ...(options.headers || {}),
      },
    });
    if (!response.ok) {
      const errData = await response.json().catch(() => ({}));
      throw new Error(errData.detail || `HTTP Error ${response.status}: ${response.statusText}`);
    }
    return await response.json();
  } catch (error) {
    console.error(`[API Error] ${endpoint}:`, error.message);
    throw error;
  }
}

export async function getHealth() {
  return await fetchJSON("/health");
}

export async function getStatus() {
  return await fetchJSON("/status");
}

export async function getModel() {
  return await fetchJSON("/model");
}

export async function getDevices() {
  return await fetchJSON("/devices");
}

export async function getTraffic() {
  return await fetchJSON("/traffic");
}

export async function getAlerts() {
  return await fetchJSON("/alerts");
}

export async function getInterfaces() {
  return await fetchJSON("/interfaces");
}

export async function startMonitoring(iface = "default") {
  return await fetchJSON("/monitor/start", {
    method: "POST",
    body: JSON.stringify({ interface: iface }),
  });
}

export async function stopMonitoring() {
  return await fetchJSON("/monitor/stop", {
    method: "POST",
  });
}

export async function predictTraffic(features) {
  return await fetchJSON("/predict", {
    method: "POST",
    body: JSON.stringify(features),
  });
}

export async function setMode(mode, iface = "default") {
  return await fetchJSON("/mode", {
    method: "POST",
    body: JSON.stringify({ mode, interface: iface }),
  });
}
