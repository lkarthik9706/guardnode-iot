import React from 'react';
import { AlertTriangle, Lock, ShieldAlert } from 'lucide-react';

export default function AlertsLogView({ alerts, onShowToast }) {
  const handleIsolateClick = () => {
    onShowToast("Device isolation is not implemented in this version.");
  };

  return (
    <div className="cyber-card" style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h3 style={{ fontSize: '1.1rem', fontWeight: 700, color: '#F8FAFC', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <AlertTriangle size={20} color="#FF2A6D" />
            INTRUSION ALERTS LOG
          </h3>
          <p style={{ fontSize: '0.8rem', color: '#94A3B8' }}>
            Log of detected anomalous packet arrival rate intrusions on local IoT subnet
          </p>
        </div>
        <span style={{ fontSize: '0.75rem', color: '#FF2A6D', fontFamily: 'monospace', fontWeight: 700 }}>
          Total Alerts: {alerts.length}
        </span>
      </div>

      <div style={{ overflowX: 'auto' }}>
        <table className="custom-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Device IP</th>
              <th>Device Name</th>
              <th>Packet Rate</th>
              <th>Mean Rate</th>
              <th>Median Rate</th>
              <th>Max Rate</th>
              <th>Detection Time</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            {alerts.length === 0 ? (
              <tr>
                <td colSpan={9} style={{ textAlign: 'center', color: '#64748B', padding: '2rem' }}>
                  No active or recorded intrusion alerts. System traffic baseline is normal.
                </td>
              </tr>
            ) : (
              alerts.map((a, idx) => (
                <tr key={idx}>
                  <td style={{ fontFamily: 'monospace', color: '#64748B' }}>#{a.id || idx + 1}</td>
                  <td style={{ fontFamily: 'monospace', fontWeight: 700, color: '#FF2A6D' }}>{a.device_ip}</td>
                  <td style={{ fontWeight: 600, color: '#F8FAFC' }}>{a.device_name || 'Unknown Device'}</td>
                  <td style={{ fontFamily: 'monospace', color: '#FF2A6D', fontWeight: 700 }}>{a.packet_rate} pkt/s</td>
                  <td style={{ fontFamily: 'monospace', color: '#CBD5E1' }}>{a.mean_packet_rate} pkt/s</td>
                  <td style={{ fontFamily: 'monospace', color: '#CBD5E1' }}>{a.median_packet_rate} pkt/s</td>
                  <td style={{ fontFamily: 'monospace', color: '#CBD5E1' }}>{a.maximum_packet_rate} pkt/s</td>
                  <td style={{ fontFamily: 'monospace', fontSize: '0.8rem', color: '#94A3B8' }}>{a.detection_time}</td>
                  <td>
                    <button
                      onClick={handleIsolateClick}
                      className="btn-outline"
                      style={{ color: '#94A3B8', border: '1px solid #334155', display: 'flex', alignItems: 'center', gap: '0.3rem' }}
                    >
                      <Lock size={12} />
                      Isolate (Demo)
                    </button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
