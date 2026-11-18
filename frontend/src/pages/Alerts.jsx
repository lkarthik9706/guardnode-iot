import React, { useState } from 'react';
import { ShieldCheck, Download } from 'lucide-react';
import StatusBadge from '../components/StatusBadge';

export default function Alerts({ mode, isMonitoring, alerts = [], isLoading, onShowToast }) {
  const isLiveCaptureUnavailable = mode === 'LIVE' && !isMonitoring;
  const displayAlerts = isLiveCaptureUnavailable ? [] : alerts;

  const [filterSeverity, setFilterSeverity] = useState('ALL');

  const handleExport = () => {
    if (displayAlerts.length === 0) {
      onShowToast?.("No alerts to export.");
      return;
    }
    const jsonStr = JSON.stringify(displayAlerts, null, 2);
    const blob = new Blob([jsonStr], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `guardnode-alerts-${Date.now()}.json`;
    link.click();
    URL.revokeObjectURL(url);
    onShowToast?.("Alerts log exported successfully.");
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.4rem' }}>
      {/* Top Header & Actions */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '0.75rem' }}>
        <div>
          <h1 style={{ fontSize: '1.35rem', fontWeight: 600, color: 'var(--text-primary)', letterSpacing: '-0.025em' }}>
            Intrusion Alerts & Incidents
          </h1>
          <p style={{ fontSize: '0.78rem', color: 'var(--text-secondary)', marginTop: '0.2rem' }}>
            Historical record of anomalous packet arrival rates flagged by the SVM detector
          </p>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <button
            onClick={handleExport}
            className="btn-outline"
          >
            <Download size={13} />
            Export Log
          </button>
          <span className="lumi-badge lumi-badge-intrusion">
            {displayAlerts.length} Recorded Alerts
          </span>
        </div>
      </div>

      {isLiveCaptureUnavailable && (
        <div className="lumi-card lumi-card-alert" style={{ padding: '0.85rem 1.15rem', color: 'var(--status-intrusion)', fontSize: '0.82rem', fontWeight: 600 }}>
          Live packet capture is unavailable. No live traffic is being analyzed.
        </div>
      )}

      {/* Main Table Card */}
      <div className="lumi-card" style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '0.5rem' }}>
          <div style={{ fontSize: '0.82rem', fontWeight: 600, color: 'var(--text-primary)' }}>
            Threat Incident Registry
          </div>

          <div style={{ display: 'flex', gap: '4px' }}>
            {['ALL', 'CRITICAL', 'WARNING'].map((sev) => (
              <button
                key={sev}
                onClick={() => setFilterSeverity(sev)}
                className={`filter-chip ${filterSeverity === sev ? 'active' : ''}`}
              >
                {sev}
              </button>
            ))}
          </div>
        </div>

        <div className="table-wrapper">
          <table className="custom-table">
            <thead>
              <tr>
                <th>Detection Timestamp</th>
                <th>Target Endpoint IP</th>
                <th>Packet Arrival Rate</th>
                <th>SVM Prediction</th>
                <th>Threat Severity</th>
                <th>Detector Architecture</th>
              </tr>
            </thead>
            <tbody>
              {isLoading && displayAlerts.length === 0 ? (
                <tr>
                  <td colSpan={6} style={{ textAlign: 'center', color: 'var(--text-tertiary)', padding: '2.5rem' }}>
                    Loading incident alerts...
                  </td>
                </tr>
              ) : isLiveCaptureUnavailable ? (
                <tr>
                  <td colSpan={6} style={{ textAlign: 'center', color: 'var(--status-intrusion)', padding: '2.5rem', fontWeight: 500 }}>
                    Live packet capture is unavailable. No live traffic is being analyzed.
                  </td>
                </tr>
              ) : displayAlerts.length === 0 ? (
                <tr>
                  <td colSpan={6} style={{ textAlign: 'center', color: 'var(--text-secondary)', padding: '3rem' }}>
                    <div style={{
                      width: 42,
                      height: 42,
                      borderRadius: 'var(--radius-pill)',
                      background: 'var(--status-normal-bg)',
                      color: 'var(--status-normal)',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      margin: '0 auto 0.75rem auto'
                    }}>
                      <ShieldCheck size={22} strokeWidth={2.2} />
                    </div>
                    <div style={{ fontWeight: 600, color: 'var(--text-primary)', fontSize: '0.92rem' }}>No Active Intrusion Alerts</div>
                    <div style={{ fontSize: '0.78rem', color: 'var(--text-tertiary)', marginTop: '0.2rem' }}>
                      All network endpoint packet arrival rates are currently within baseline thresholds.
                    </div>
                  </td>
                </tr>
              ) : (
                displayAlerts.map((alert, idx) => (
                  <tr key={idx} style={{ background: 'rgba(244, 63, 94, 0.02)' }}>
                    <td style={{ fontFamily: 'var(--font-mono)', fontSize: '0.8rem', color: 'var(--text-tertiary)' }}>
                      {alert.detection_time || alert.timestamp || 'Just now'}
                    </td>
                    <td style={{ fontFamily: 'var(--font-mono)', fontWeight: 600, color: 'var(--status-intrusion)' }}>
                      {alert.device_ip}
                    </td>
                    <td style={{ fontFamily: 'var(--font-mono)', fontWeight: 600, color: 'var(--status-intrusion)' }}>
                      {alert.packet_rate} <span style={{ fontSize: '0.72rem', fontWeight: 400, color: 'var(--text-tertiary)' }}>pkt/s</span>
                    </td>
                    <td>
                      <StatusBadge status="INTRUSION" />
                    </td>
                    <td>
                      <span className="lumi-badge lumi-badge-intrusion" style={{ fontSize: '0.68rem', padding: '0.12rem 0.45rem' }}>
                        CRITICAL
                      </span>
                    </td>
                    <td style={{ fontSize: '0.78rem', color: 'var(--accent-primary)', fontFamily: 'var(--font-mono)' }}>
                      {alert.svm_model || 'LinearSVC (3 Features)'}
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
