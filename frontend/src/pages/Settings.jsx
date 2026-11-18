import React from 'react';
import { Server, Cpu, Play, Square } from 'lucide-react';

export default function SettingsPage({
  interfaces = [],
  activeInterface,
  onSelectInterface,
  onStartMonitoring,
  onStopMonitoring,
  isMonitoring
}) {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.4rem' }}>
      {/* Header */}
      <div>
        <h1 style={{ fontSize: '1.35rem', fontWeight: 600, color: 'var(--text-primary)', letterSpacing: '-0.025em' }}>
          System Settings & Model Configuration
        </h1>
        <p style={{ fontSize: '0.78rem', color: 'var(--text-secondary)', marginTop: '0.2rem' }}>
          GuardNode IoT hardware parameters, network capture adapters, and inference pipeline
        </p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(360px, 1fr))', gap: '1.25rem' }}>
        {/* Network Capture Card */}
        <div className="lumi-card" style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.55rem', borderBottom: '1px solid var(--border-subtle)', paddingBottom: '0.75rem' }}>
            <Server size={18} color="var(--accent-primary)" />
            <div>
              <h3 style={{ fontSize: '0.92rem', fontWeight: 600, color: 'var(--text-primary)' }}>
                Network Capture Adapter
              </h3>
              <p style={{ fontSize: '0.72rem', color: 'var(--text-tertiary)' }}>
                Physical or virtual NIC listened by Scapy daemon
              </p>
            </div>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
            <label style={{ fontSize: '0.78rem', fontWeight: 500, color: 'var(--text-secondary)' }}>
              Active Network Adapter
            </label>
            <select
              value={activeInterface}
              onChange={(e) => onSelectInterface(e.target.value)}
              className="lumi-select"
              style={{ width: '100%' }}
            >
              {interfaces.map((iface) => (
                <option key={iface.id} value={iface.id}>
                  {iface.name} ({iface.id})
                </option>
              ))}
            </select>
            <p style={{ fontSize: '0.72rem', color: 'var(--text-tertiary)', lineHeight: 1.4 }}>
              Note: Live capture mode requires network administrator privileges for raw socket promiscuous capture. In DEMO MODE, traffic is automatically streamed from the CICIoT2023 evaluation dataset.
            </p>
          </div>

          <div style={{ marginTop: 'auto', paddingTop: '0.5rem', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <span style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>Capture State:</span>
            {isMonitoring ? (
              <button
                onClick={onStopMonitoring}
                className="btn-destructive"
                style={{ padding: '0.35rem 0.75rem', fontSize: '0.78rem' }}
              >
                <Square size={12} fill="currentColor" />
                Stop Capture
              </button>
            ) : (
              <button
                onClick={onStartMonitoring}
                className="btn-primary"
                style={{ padding: '0.35rem 0.75rem', fontSize: '0.78rem' }}
              >
                <Play size={12} fill="currentColor" />
                Start Capture
              </button>
            )}
          </div>
        </div>

        {/* Machine Learning Model Card */}
        <div className="lumi-card" style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.55rem', borderBottom: '1px solid var(--border-subtle)', paddingBottom: '0.75rem' }}>
            <Cpu size={18} color="var(--status-normal)" />
            <div>
              <h3 style={{ fontSize: '0.92rem', fontWeight: 600, color: 'var(--text-primary)' }}>
                SVM Classifier Pipeline
              </h3>
              <p style={{ fontSize: '0.72rem', color: 'var(--text-tertiary)' }}>
                Trained production artifacts and hyperparameter configuration
              </p>
            </div>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.65rem', fontSize: '0.78rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', padding: '0.45rem 0.6rem', background: 'var(--bg-surface)', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-subtle)' }}>
              <span style={{ color: 'var(--text-tertiary)' }}>Classifier Architecture:</span>
              <span style={{ fontWeight: 600, fontFamily: 'var(--font-mono)', color: 'var(--text-primary)' }}>LinearSVC (Scikit-Learn)</span>
            </div>

            <div style={{ display: 'flex', justifyContent: 'space-between', padding: '0.45rem 0.6rem', background: 'var(--bg-surface)', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-subtle)' }}>
              <span style={{ color: 'var(--text-tertiary)' }}>Model File:</span>
              <span style={{ fontFamily: 'var(--font-mono)', color: 'var(--accent-primary)' }}>models/svm_model.pkl</span>
            </div>

            <div style={{ display: 'flex', justifyContent: 'space-between', padding: '0.45rem 0.6rem', background: 'var(--bg-surface)', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-subtle)' }}>
              <span style={{ color: 'var(--text-tertiary)' }}>Feature Scaler:</span>
              <span style={{ fontFamily: 'var(--font-mono)', color: 'var(--accent-primary)' }}>models/scaler.pkl</span>
            </div>

            <div style={{ display: 'flex', justifyContent: 'space-between', padding: '0.45rem 0.6rem', background: 'var(--bg-surface)', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-subtle)' }}>
              <span style={{ color: 'var(--text-tertiary)' }}>Decision Threshold:</span>
              <span style={{ fontFamily: 'var(--font-mono)', fontWeight: 600, color: 'var(--status-normal)' }}>0.0396 (Balanced)</span>
            </div>

            <div style={{ display: 'flex', justifyContent: 'space-between', padding: '0.45rem 0.6rem', background: 'var(--bg-surface)', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-subtle)' }}>
              <span style={{ color: 'var(--text-tertiary)' }}>Preprocessing:</span>
              <span style={{ fontFamily: 'var(--font-mono)', color: 'var(--text-secondary)' }}>np.log1p + StandardScaler</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
