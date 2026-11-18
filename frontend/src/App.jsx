import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import ToastNotification from './components/ToastNotification';
import DeviceDetailsModal from './components/DeviceDetailsModal';

import Dashboard from './pages/Dashboard';
import Devices from './pages/Devices';
import Alerts from './pages/Alerts';
import SettingsPage from './pages/Settings';
import ModelPerformanceView from './components/ModelPerformanceView';
import NetworkMapView from './components/NetworkMapView';

import {
  getStatus,
  getInterfaces,
  getModel,
  startMonitoring,
  stopMonitoring,
  setMode
} from './services/api';

export default function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [mode, setModeState] = useState('DEMO');
  const [isMonitoring, setIsMonitoring] = useState(true);
  const [scapyError, setScapyError] = useState(null);
  const [isConnected, setIsConnected] = useState(true);
  const [isLoading, setIsLoading] = useState(true);
  const [activeInterface, setActiveInterface] = useState('default');
  const [interfaces, setInterfaces] = useState([]);
  const [modelInfo, setModelInfo] = useState(null);

  // Telemetry state
  const [summaryData, setSummaryData] = useState({
    total_devices: 0,
    normal_devices: 0,
    active_intrusions: 0,
    average_packet_rate: 0,
    total_packet_rate: 0,
    packets_analyzed: 0,
    devices: [],
    alerts: [],
    traffic_history: []
  });

  const [selectedDevice, setSelectedDevice] = useState(null);
  const [toastMessage, setToastMessage] = useState(null);

  const showToast = (msg) => {
    setToastMessage(msg);
    setTimeout(() => {
      setToastMessage(null);
    }, 4500);
  };

  // Fetch telemetry data from FastAPI backend
  const fetchTelemetry = async () => {
    try {
      const statusRes = await getStatus();
      if (statusRes) {
        setIsConnected(true);
        setModeState(statusRes.mode || 'DEMO');
        setIsMonitoring(statusRes.monitoring ?? false);
        if (statusRes.interface) setActiveInterface(statusRes.interface);
        setScapyError(statusRes.scapy_error || null);

        if (statusRes.summary) {
          setSummaryData(statusRes.summary);
        }
      }
    } catch (err) {
      setIsConnected(false);
    } finally {
      setIsLoading(false);
    }
  };

  const loadInterfacesList = async () => {
    try {
      const res = await getInterfaces();
      if (res && Array.isArray(res) && res.length > 0) {
        setInterfaces(res);
        // Automatically default to the primary active network adapter
        const preferred = res.find(i => i.is_active && i.id !== 'default') || res[0];
        if (activeInterface === 'default' || !activeInterface || activeInterface.includes('3A3284BF') || activeInterface.includes('BCFAFEE5')) {
          setActiveInterface(preferred.id);
        }
      }
    } catch (err) {}
  };

  const loadModelDetails = async () => {
    try {
      const res = await getModel();
      if (res) {
        setModelInfo(res);
      }
    } catch (err) {}
  };

  // Initial load & interfaces
  useEffect(() => {
    loadInterfacesList();
    loadModelDetails();
    fetchTelemetry();

    // Poll every 3 seconds for live/demo updates
    const interval = setInterval(() => {
      fetchTelemetry();
    }, 3000);

    return () => clearInterval(interval);
  }, []);

  const handleToggleMode = async (targetMode) => {
    try {
      const res = await setMode(targetMode, activeInterface);
      if (res && res.status === 'success') {
        setModeState(res.mode);
        setIsMonitoring(res.is_monitoring);
        setScapyError(res.scapy_error || null);
        if (res.mode === 'LIVE' && !res.is_monitoring) {
          showToast(res.scapy_error || "Live packet capture is unavailable. No live traffic is being analyzed.");
        } else {
          showToast(`Switched to ${res.mode} MODE.`);
        }
        fetchTelemetry();
      }
    } catch (err) {
      showToast(err.message || "Failed to switch mode. Is FastAPI backend running?");
    }
  };

  const handleSelectInterface = async (iface) => {
    setActiveInterface(iface);
    const targetName = interfaces.find(i => i.id === iface)?.name || iface;
    showToast(`Interface selected: ${targetName}`);
    if (mode === 'LIVE') {
      try {
        const res = await startMonitoring(iface);
        if (res && res.status === 'started') {
          setIsMonitoring(true);
          setScapyError(null);
          fetchTelemetry();
        }
      } catch (err) {
        showToast(err.message || "Failed to switch live capture interface.");
      }
    }
  };

  const handleStartMonitoring = async () => {
    try {
      const res = await startMonitoring(activeInterface);
      if (res && res.status === 'started') {
        setIsMonitoring(true);
        setScapyError(null);
        showToast(`Monitoring ACTIVE on interface: ${activeInterface}`);
      }
    } catch (err) {
      setIsMonitoring(false);
      const errMsg = err.message || "Live packet capture is unavailable. No live traffic is being analyzed.";
      setScapyError(errMsg);
      showToast(errMsg);
    } finally {
      fetchTelemetry();
    }
  };

  const handleStopMonitoring = async () => {
    try {
      await stopMonitoring();
      setIsMonitoring(false);
      showToast("Monitoring STOPPED.");
    } catch (err) {
      showToast("Failed to stop monitoring.");
    } finally {
      fetchTelemetry();
    }
  };

  const alertsCount = summaryData?.active_intrusions || (summaryData?.alerts ? summaryData.alerts.length : 0);

  return (
    <div className="app-container">
      <Sidebar
        activeTab={activeTab}
        onTabChange={setActiveTab}
        alertsCount={alertsCount}
      />

      <div className="main-wrapper">
        <Header
          mode={mode}
          isMonitoring={isMonitoring}
          isConnected={isConnected}
          interfaces={interfaces}
          activeInterface={activeInterface}
          onSelectInterface={handleSelectInterface}
          onStartMonitoring={handleStartMonitoring}
          onStopMonitoring={handleStopMonitoring}
          onToggleMode={handleToggleMode}
          onShowToast={showToast}
          scapyError={scapyError}
          activeTab={activeTab}
        />

        {!isConnected && (
          <div style={{
            background: 'var(--status-intrusion-bg)',
            borderBottom: '1px solid var(--status-intrusion-border)',
            padding: '0.6rem 1.75rem',
            color: 'var(--status-intrusion)',
            fontSize: '0.82rem',
            fontWeight: 500,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between'
          }}>
            <span>Backend server disconnected. Run <code>python -m uvicorn backend.main:app --port 8000</code> to activate real-time telemetry.</span>
            <button
              onClick={fetchTelemetry}
              className="btn-destructive"
              style={{ padding: '0.2rem 0.6rem', fontSize: '0.72rem' }}
            >
              Retry Connection
            </button>
          </div>
        )}

        <main className="content-scrollable">
          {activeTab === 'dashboard' && (
            <Dashboard
              mode={mode}
              isMonitoring={isMonitoring}
              scapyError={scapyError}
              summaryData={summaryData}
              isLoading={isLoading}
              onSelectDevice={setSelectedDevice}
              onShowToast={showToast}
            />
          )}

          {activeTab === 'devices' && (
            <Devices
              mode={mode}
              isMonitoring={isMonitoring}
              scapyError={scapyError}
              devices={summaryData.devices || []}
              isLoading={isLoading}
              onSelectDevice={setSelectedDevice}
            />
          )}

          {activeTab === 'alerts' && (
            <Alerts
              mode={mode}
              isMonitoring={isMonitoring}
              scapyError={scapyError}
              alerts={summaryData.alerts || []}
              isLoading={isLoading}
              onShowToast={showToast}
            />
          )}

          {activeTab === 'network' && (
            <NetworkMapView
              devices={summaryData.devices || []}
              onSelectDevice={setSelectedDevice}
            />
          )}

          {activeTab === 'model' && (
            <ModelPerformanceView
              modelInfo={modelInfo}
            />
          )}

          {activeTab === 'settings' && (
            <SettingsPage
              interfaces={interfaces}
              activeInterface={activeInterface}
              onSelectInterface={handleSelectInterface}
              onStartMonitoring={handleStartMonitoring}
              onStopMonitoring={handleStopMonitoring}
              isMonitoring={isMonitoring}
              onShowToast={showToast}
            />
          )}
        </main>

        <footer className="app-statusbar">
          <div style={{ display: 'flex', alignItems: 'center', gap: '1.25rem' }}>
            <span style={{ display: 'flex', alignItems: 'center', gap: '0.45rem' }}>
              <span className="pulse-dot" style={{ backgroundColor: isMonitoring ? 'var(--status-normal)' : 'var(--status-intrusion)' }} />
              STATUS: {isMonitoring ? `ACTIVE (${mode})` : `STOPPED (${mode})`}
            </span>
            <span style={{ color: 'var(--border-strong)' }}>|</span>
            <span style={{ color: 'var(--text-secondary)' }}>PACKETS ANALYZED: {summaryData.packets_analyzed || 0}</span>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', color: 'var(--text-tertiary)' }}>
            <span>ADAPTER: <strong style={{ color: 'var(--text-primary)' }}>{activeInterface}</strong></span>
            <span style={{ color: 'var(--border-strong)' }}>|</span>
            <span style={{ color: 'var(--status-normal)' }}>
              MODEL: LinearSVC (Mean, Median, Max Arrival Rates)
            </span>
          </div>
        </footer>
      </div>

      <DeviceDetailsModal device={selectedDevice} onClose={() => setSelectedDevice(null)} />
      <ToastNotification message={toastMessage} onClose={() => setToastMessage(null)} />
    </div>
  );
}
