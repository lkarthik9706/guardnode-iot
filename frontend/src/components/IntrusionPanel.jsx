import React from 'react';
import { AlertOctagon, ShieldCheck, Lock } from 'lucide-react';

export default function IntrusionPanel({ latestAlert, onShowToast }) {
  const hasIntrusion = Boolean(latestAlert);

  if (!hasIntrusion) {
    return (
      <div className="lumi-card" style={{
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
        padding: '2rem 1.5rem',
        textAlign: 'center',
        height: '100%',
        minHeight: '340px'
      }}>
        <div style={{
          width: 48,
          height: 48,
          borderRadius: 'var(--radius-xl)',
          background: 'var(--status-normal-bg)',
          border: '1px solid var(--status-normal-border)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          color: 'var(--status-normal)',
          marginBottom: '1rem'
        }}>
          <ShieldCheck size={26} strokeWidth={2.2} />
        </div>
        <h3 style={{ color: 'var(--text-primary)', fontSize: '1.05rem', fontWeight: 600, letterSpacing: '-0.02em' }}>
          Subnet Secure
        </h3>
        <p style={{ color: 'var(--text-tertiary)', fontSize: '0.78rem', marginTop: '0.4rem', maxWidth: '260px', lineHeight: 1.4 }}>
          All active network endpoints are operating within normal baseline packet arrival rates.
        </p>
        <div style={{ marginTop: '1.25rem' }}>
          <span className="lumi-badge lumi-badge-normal">
            <span className="pulse-dot" />
            <span>0 ACTIVE BREACHES</span>
          </span>
        </div>
      </div>
    );
  }

  const handleIsolateClick = () => {
    onShowToast?.("Device isolation is not implemented in this version.");
  };

  return (
    <div className="lumi-card lumi-card-alert" style={{ display: 'flex', flexDirection: 'column', gap: '0.9rem', minHeight: '340px' }}>
      {/* Alert Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '1px solid var(--status-intrusion-border)', paddingBottom: '0.65rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <AlertOctagon size={18} color="var(--status-intrusion)" />
          <h3 style={{ color: 'var(--status-intrusion)', fontSize: '0.88rem', fontWeight: 700, letterSpacing: '0.02em' }}>
            ML INTRUSION FLAGGED
          </h3>
        </div>
        <span className="lumi-badge lumi-badge-intrusion" style={{ fontSize: '0.68rem', padding: '0.15rem 0.5rem' }}>
          CRITICAL
        </span>
      </div>

      {/* Target Device */}
      <div style={{ background: 'var(--bg-surface)', padding: '0.75rem', borderRadius: 'var(--radius-md)', border: '1px solid var(--border-default)' }}>
        <div style={{ fontSize: '0.7rem', color: 'var(--text-tertiary)', textTransform: 'uppercase', letterSpacing: '0.04em' }}>Target Endpoint</div>
        <div style={{ fontSize: '1.15rem', fontWeight: 700, fontFamily: 'var(--font-mono)', color: 'var(--text-primary)', marginTop: '0.15rem' }}>
          {latestAlert.device_ip}
        </div>
        <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', marginTop: '0.1rem' }}>
          {latestAlert.device_name || 'IoT Endpoint'}
        </div>
      </div>

      {/* Model & Confidence */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.5rem' }}>
        <div style={{ background: 'var(--bg-surface)', padding: '0.55rem', borderRadius: 'var(--radius-md)', border: '1px solid var(--border-subtle)' }}>
          <span style={{ fontSize: '0.68rem', color: 'var(--text-tertiary)', display: 'block' }}>Detector</span>
          <span style={{ fontSize: '0.8rem', fontWeight: 600, color: 'var(--accent-primary)', marginTop: '0.1rem', display: 'block' }}>
            LinearSVC
          </span>
        </div>
        <div style={{ background: 'var(--bg-surface)', padding: '0.55rem', borderRadius: 'var(--radius-md)', border: '1px solid var(--border-subtle)' }}>
          <span style={{ fontSize: '0.68rem', color: 'var(--text-tertiary)', display: 'block' }}>Anomaly Class</span>
          <span style={{ fontSize: '0.8rem', fontWeight: 600, color: 'var(--status-intrusion)', marginTop: '0.1rem', display: 'block' }}>
            DDoS / Flood
          </span>
        </div>
      </div>

      {/* Extracted Features */}
      <div style={{ background: 'var(--bg-surface)', padding: '0.75rem', borderRadius: 'var(--radius-md)', border: '1px solid var(--border-default)', display: 'flex', flexDirection: 'column', gap: '0.45rem' }}>
        <div style={{ fontSize: '0.7rem', fontWeight: 600, color: 'var(--text-tertiary)', textTransform: 'uppercase', letterSpacing: '0.04em', borderBottom: '1px solid var(--border-subtle)', paddingBottom: '0.25rem' }}>
          Feature Extraction
        </div>

        <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.74rem' }}>
          <span style={{ color: 'var(--text-secondary)' }}>Mean Packet Rate:</span>
          <span style={{ fontFamily: 'var(--font-mono)', fontWeight: 600, color: 'var(--text-primary)' }}>
            {latestAlert.mean_packet_rate} pkt/s
          </span>
        </div>

        <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.74rem' }}>
          <span style={{ color: 'var(--text-secondary)' }}>Median Packet Rate:</span>
          <span style={{ fontFamily: 'var(--font-mono)', fontWeight: 600, color: 'var(--text-primary)' }}>
            {latestAlert.median_packet_rate} pkt/s
          </span>
        </div>

        <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.74rem' }}>
          <span style={{ color: 'var(--text-secondary)' }}>Max Packet Rate:</span>
          <span style={{ fontFamily: 'var(--font-mono)', fontWeight: 700, color: 'var(--status-intrusion)' }}>
            {latestAlert.maximum_packet_rate} pkt/s
          </span>
        </div>
      </div>

      {/* Isolation Action */}
      <button
        onClick={handleIsolateClick}
        className="btn-destructive btn-disabled"
        style={{ width: '100%', marginTop: 'auto' }}
        title="Quarantine endpoint traffic"
      >
        <Lock size={13} />
        ISOLATE ENDPOINT
      </button>
    </div>
  );
}
