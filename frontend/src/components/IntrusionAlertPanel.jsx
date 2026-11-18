import React from 'react';
import { AlertOctagon, ShieldAlert, Lock } from 'lucide-react';

export default function IntrusionAlertPanel({ latestAlert, onShowToast }) {
  if (!latestAlert) return null;

  const handleIsolateClick = () => {
    onShowToast("Device isolation is not implemented in this version.");
  };

  return (
    <div className="cyber-card cyber-card-alert" style={{ position: 'relative', overflow: 'hidden' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', borderBottom: '1px solid rgba(255, 42, 109, 0.3)', paddingBottom: '0.75rem', marginBottom: '1rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
          <div style={{ padding: '0.5rem', background: 'rgba(255, 42, 109, 0.2)', borderRadius: '8px', color: '#FF2A6D' }}>
            <AlertOctagon size={24} />
          </div>
          <div>
            <h3 style={{ color: '#FF2A6D', fontSize: '1.1rem', fontWeight: 700, letterSpacing: '0.05em' }}>
              INTRUSION DETECTED
            </h3>
            <p style={{ color: '#94A3B8', fontSize: '0.8rem' }}>
              High-frequency anomalous packet arrival rate detected by Support Vector Machine (SVM)
            </p>
          </div>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <button
            onClick={handleIsolateClick}
            className="btn-primary btn-disabled"
            title="Feature disabled in current capstone build"
          >
            <Lock size={14} />
            Isolate Device (Demo Only)
          </button>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(160px, 1fr))', gap: '1rem' }}>
        <div>
          <span style={{ fontSize: '0.75rem', color: '#94A3B8' }}>Target Device IP</span>
          <div style={{ fontSize: '1.1rem', fontWeight: 700, fontFamily: 'monospace', color: '#FFF' }}>
            {latestAlert.device_ip}
          </div>
          <div style={{ fontSize: '0.75rem', color: '#64748B' }}>{latestAlert.device_name}</div>
        </div>

        <div>
          <span style={{ fontSize: '0.75rem', color: '#94A3B8' }}>Packet Arrival Rate</span>
          <div style={{ fontSize: '1.1rem', fontWeight: 700, fontFamily: 'monospace', color: '#FF2A6D' }}>
            {latestAlert.packet_rate} pkt/s
          </div>
        </div>

        <div>
          <span style={{ fontSize: '0.75rem', color: '#94A3B8' }}>Mean Packet Rate</span>
          <div style={{ fontSize: '0.95rem', fontWeight: 600, fontFamily: 'monospace', color: '#CBD5E1' }}>
            {latestAlert.mean_packet_rate} pkt/s
          </div>
        </div>

        <div>
          <span style={{ fontSize: '0.75rem', color: '#94A3B8' }}>Median Packet Rate</span>
          <div style={{ fontSize: '0.95rem', fontWeight: 600, fontFamily: 'monospace', color: '#CBD5E1' }}>
            {latestAlert.median_packet_rate} pkt/s
          </div>
        </div>

        <div>
          <span style={{ fontSize: '0.75rem', color: '#94A3B8' }}>Maximum Packet Rate</span>
          <div style={{ fontSize: '0.95rem', fontWeight: 600, fontFamily: 'monospace', color: '#CBD5E1' }}>
            {latestAlert.maximum_packet_rate} pkt/s
          </div>
        </div>

        <div>
          <span style={{ fontSize: '0.75rem', color: '#94A3B8' }}>Detection Details</span>
          <div style={{ fontSize: '0.8rem', color: '#F8FAFC' }}>
            Time: <span style={{ fontFamily: 'monospace' }}>{latestAlert.detection_time}</span>
          </div>
          <div style={{ fontSize: '0.75rem', color: '#00F0FF', marginTop: '0.2rem' }}>
            {latestAlert.svm_model} ({Math.round((latestAlert.confidence || 0.95) * 100)}% score)
          </div>
        </div>
      </div>
    </div>
  );
}
