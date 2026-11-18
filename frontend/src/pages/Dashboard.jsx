import React from 'react';
import { AlertOctagon, Terminal } from 'lucide-react';
import StatCard from '../components/StatCard';
import TrafficChart from '../components/TrafficChart';
import IntrusionPanel from '../components/IntrusionPanel';
import DeviceTable from '../components/DeviceTable';

export default function Dashboard({
  mode,
  isMonitoring,
  scapyError,
  summaryData,
  isLoading,
  onSelectDevice,
  onShowToast
}) {
  const isLiveCaptureUnavailable = mode === 'LIVE' && !isMonitoring;

  const totalDevices = isLiveCaptureUnavailable ? 0 : (summaryData?.total_devices ?? 0);
  const normalDevices = isLiveCaptureUnavailable ? 0 : (summaryData?.normal_devices ?? 0);
  const activeIntrusions = isLiveCaptureUnavailable ? 0 : (summaryData?.active_intrusions ?? 0);
  const averagePacketRate = isLiveCaptureUnavailable ? 0 : (summaryData?.average_packet_rate ?? 0);
  const trafficHistory = isLiveCaptureUnavailable ? [] : (summaryData?.traffic_history ?? []);
  const devices = isLiveCaptureUnavailable ? [] : (summaryData?.devices ?? []);
  const alerts = isLiveCaptureUnavailable ? [] : (summaryData?.alerts ?? []);

  const latestAlert = alerts.length > 0 ? alerts[0] : null;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.4rem' }}>
      {/* Top Banner & Quick Controls */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '0.75rem' }}>
        <div>
          <h1 style={{ fontSize: '1.35rem', fontWeight: 600, color: 'var(--text-primary)', letterSpacing: '-0.025em' }}>
            System Dashboard
          </h1>
          <p style={{ fontSize: '0.78rem', color: 'var(--text-secondary)', marginTop: '0.2rem' }}>
            Lightweight IoT intrusion monitoring with LinearSVC arrival rate feature vectors
          </p>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <button
            onClick={() => onShowToast?.("SVM feature extraction & packet rate diagnostic check passed.")}
            className="btn-outline"
          >
            <Terminal size={13} />
            Run Diagnostic
          </button>
          <span className="lumi-badge lumi-badge-normal">
            <span className="pulse-dot" />
            TELEMETRY STREAMING
          </span>
        </div>
      </div>

      {/* Capture Unavailable Warning Banner */}
      {isLiveCaptureUnavailable && (
        <div className="lumi-card lumi-card-alert" style={{
          display: 'flex',
          alignItems: 'center',
          gap: '1rem',
          padding: '1rem 1.25rem'
        }}>
          <div style={{
            width: 36,
            height: 36,
            borderRadius: 'var(--radius-pill)',
            background: 'var(--status-intrusion-bg)',
            color: 'var(--status-intrusion)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            flexShrink: 0
          }}>
            <AlertOctagon size={20} />
          </div>
          <div style={{ flex: 1 }}>
            <h4 style={{ color: 'var(--status-intrusion)', fontSize: '0.9rem', fontWeight: 600 }}>
              Live packet capture is unavailable. No live traffic is being analyzed.
            </h4>
            {scapyError && (
              <p style={{ color: 'var(--text-secondary)', fontSize: '0.78rem', marginTop: '0.2rem' }}>
                {scapyError}
              </p>
            )}
          </div>
        </div>
      )}

      {/* Top 4 Summary Metric Cards */}
      <StatCard
        totalDevices={totalDevices}
        normalDevices={normalDevices}
        activeIntrusions={activeIntrusions}
        averagePacketRate={averagePacketRate}
      />

      {/* Middle Grid: Live Traffic Stream Chart & Threat Anomaly Panel */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: activeIntrusions > 0 ? '1fr 340px' : '1fr',
        gap: '1.25rem',
        alignItems: 'stretch'
      }}>
        <TrafficChart
          trafficHistory={trafficHistory}
          isLoading={isLoading}
          isLiveCaptureUnavailable={isLiveCaptureUnavailable}
          scapyError={scapyError}
        />
        <IntrusionPanel latestAlert={latestAlert} onShowToast={onShowToast} />
      </div>

      {/* Bottom Table: Monitored Subnet Endpoints */}
      <DeviceTable
        devices={devices}
        onSelectDevice={onSelectDevice}
        isLoading={isLoading}
        isLiveCaptureUnavailable={isLiveCaptureUnavailable}
      />
    </div>
  );
}
