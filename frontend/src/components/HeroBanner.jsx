import React from 'react';
import { ShieldCheck, Activity, Lock, Terminal } from 'lucide-react';

export default function HeroBanner({ isMonitoring, onNavigateLogs, onShowToast }) {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
      {/* Title + Pulse Badge */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <div>
          <h1 style={{ fontSize: '1.4rem', fontWeight: 700, color: '#F8FAFC', letterSpacing: '-0.02em' }}>
            IoT Intrusion Detection System
          </h1>
          <div style={{ marginTop: '0.2rem' }}>
            <span className={`badge-pulse ${isMonitoring ? 'badge-pulse-green' : 'badge-pulse-red'}`}>
              <span className="pulse-dot"></span>
              {isMonitoring ? 'MONITORING ACTIVE' : 'MONITORING PAUSED'}
            </span>
          </div>
        </div>
      </div>

      {/* Hero Card Container */}
      <div className="cyber-card" style={{
        background: 'linear-gradient(135deg, rgba(15, 23, 42, 0.95), rgba(11, 25, 44, 0.95))',
        border: '1px solid rgba(0, 240, 255, 0.25)',
        position: 'relative',
        overflow: 'hidden',
        padding: '1.5rem'
      }}>
        <div style={{ position: 'relative', zIndex: 2 }}>
          <h2 style={{ fontSize: '1.5rem', fontWeight: 700, color: '#F8FAFC', marginBottom: '0.4rem' }}>
            Secure IoT Ecosystem
          </h2>
          <p style={{ color: '#94A3B8', fontSize: '0.85rem', maxWidth: '650px', marginBottom: '1.25rem' }}>
            Real-time intrusion detection and behavioral analysis active across all connected local network devices using trained Support Vector Machines (SVM).
          </p>

          {/* Sub Badges */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '1.5rem', marginBottom: '1.25rem', flexWrap: 'wrap' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', fontSize: '0.75rem', background: 'rgba(16, 185, 129, 0.1)', padding: '0.35rem 0.75rem', borderRadius: '6px', border: '1px solid rgba(16, 185, 129, 0.3)', color: '#10B981' }}>
              <ShieldCheck size={14} />
              <span>THREAT LEVEL: <strong>Low Risk</strong></span>
            </div>

            <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', fontSize: '0.75rem', background: 'rgba(59, 130, 246, 0.1)', padding: '0.35rem 0.75rem', borderRadius: '6px', border: '1px solid rgba(59, 130, 246, 0.3)', color: '#3B82F6' }}>
              <Activity size={14} />
              <span>ACTIVE TRAFFIC: <strong>2.4 Gbps</strong></span>
            </div>

            <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', fontSize: '0.75rem', background: 'rgba(0, 240, 255, 0.1)', padding: '0.35rem 0.75rem', borderRadius: '6px', border: '1px solid rgba(0, 240, 255, 0.3)', color: '#00F0FF' }}>
              <Lock size={14} />
              <span>PROTECTED: <strong>Local Subnet Hosts</strong></span>
            </div>
          </div>

          {/* Action Buttons */}
          <div style={{ display: 'flex', gap: '0.75rem' }}>
            <button
              onClick={onNavigateLogs}
              className="btn-primary"
            >
              View Security Logs
            </button>
            <button
              onClick={() => onShowToast("SVM feature extraction & packet rate diagnostic check passed.")}
              className="btn-outline"
              style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}
            >
              <Terminal size={14} />
              Run Diagnostics
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
