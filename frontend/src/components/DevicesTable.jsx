import React from 'react';
import { Cpu, Eye } from 'lucide-react';
import StatusBadge from './StatusBadge';

export default function DevicesTable({ devices, onSelectDevice }) {
  return (
    <div className="cyber-card" style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h3 style={{ fontSize: '1rem', fontWeight: 600, color: '#F8FAFC', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <Cpu size={18} color="#00F0FF" />
            OBSERVED NETWORK ENDPOINTS & TELEMETRY
          </h3>
          <p style={{ fontSize: '0.75rem', color: '#94A3B8' }}>
            Real-time visible network hosts monitored by SVM model
          </p>
        </div>
        <span style={{ fontSize: '0.75rem', color: '#94A3B8', fontFamily: 'monospace' }}>
          Total Active: {devices.length} Endpoints
        </span>
      </div>

      <div style={{ overflowX: 'auto' }}>
        <table className="custom-table">
          <thead>
            <tr>
              <th>Endpoint Name</th>
              <th>IP Address</th>
              <th>Type</th>
              <th>Packet Rate</th>
              <th>SVM Status</th>
              <th>Last Seen</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            {devices.length === 0 ? (
              <tr>
                <td colSpan={7} style={{ textAlign: 'center', color: '#64748B', padding: '2rem' }}>
                  No network endpoints detected. Listening for traffic...
                </td>
              </tr>
            ) : (
              devices.map((dev) => {
                const isIntrusion = dev.status === 'INTRUSION';
                return (
                  <tr key={dev.ip}>
                    <td style={{ fontWeight: 600, color: '#F8FAFC' }}>
                      {dev.name || 'Unknown Endpoint'}
                    </td>
                    <td style={{ fontFamily: 'monospace', color: '#00F0FF' }}>
                      {dev.ip}
                    </td>
                    <td>
                      <span style={{
                        fontSize: '0.7rem',
                        fontWeight: 700,
                        padding: '0.15rem 0.45rem',
                        borderRadius: '4px',
                        background: dev.endpoint_type === 'EXTERNAL' ? 'rgba(245, 158, 11, 0.15)' : 'rgba(168, 85, 247, 0.15)',
                        color: dev.endpoint_type === 'EXTERNAL' ? '#F59E0B' : '#A855F7',
                        border: `1px solid ${dev.endpoint_type === 'EXTERNAL' ? 'rgba(245, 158, 11, 0.3)' : 'rgba(168, 85, 247, 0.3)'}`
                      }}>
                        {dev.endpoint_type || 'LOCAL'}
                      </span>
                    </td>
                    <td style={{ fontFamily: 'monospace', fontWeight: 600, color: isIntrusion ? '#FF2A6D' : '#F8FAFC' }}>
                      {dev.packet_rate} pkt/s
                    </td>
                    <td>
                      <StatusBadge status={dev.status} />
                    </td>
                    <td style={{ fontFamily: 'monospace', fontSize: '0.8rem', color: '#94A3B8' }}>
                      {dev.last_seen}
                    </td>
                    <td>
                      <button
                        onClick={() => onSelectDevice(dev)}
                        className="btn-outline"
                        style={{ display: 'flex', alignItems: 'center', gap: '0.3rem' }}
                      >
                        <Eye size={13} />
                        View Details
                      </button>
                    </td>
                  </tr>
                );
              })
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
