import React from 'react';
import { X, Cpu, Activity, ShieldCheck, AlertOctagon } from 'lucide-react';
import { ResponsiveContainer, AreaChart, Area, XAxis, YAxis, Tooltip, CartesianGrid } from 'recharts';

export default function DeviceDetailModal({ device, onClose }) {
  if (!device) return null;

  const isIntrusion = device.status === 'INTRUSION';
  const historyData = device.rate_history && device.rate_history.length > 0
    ? device.rate_history
    : [
        { timestamp: device.last_seen, rate: device.packet_rate }
      ];

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '1px solid #1E293B', paddingBottom: '0.75rem', marginBottom: '1.25rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <Cpu size={22} color={isIntrusion ? '#FF2A6D' : '#00F0FF'} />
            <div>
              <h3 style={{ fontSize: '1.1rem', fontWeight: 700, color: '#F8FAFC' }}>
                {device.name || 'Unknown Device'}
              </h3>
              <p style={{ fontSize: '0.8rem', fontFamily: 'monospace', color: '#00F0FF' }}>
                IP: {device.ip}
              </p>
            </div>
          </div>

          <button
            onClick={onClose}
            style={{ background: 'transparent', border: 'none', color: '#94A3B8', cursor: 'pointer' }}
          >
            <X size={20} />
          </button>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '1rem', marginBottom: '1.5rem' }}>
          <div style={{ background: '#090E1A', border: '1px solid #1E293B', borderRadius: '8px', padding: '0.75rem' }}>
            <span style={{ fontSize: '0.75rem', color: '#94A3B8' }}>SVM Classification</span>
            <div style={{ marginTop: '0.3rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <span className={`badge-pulse ${isIntrusion ? 'badge-pulse-red' : 'badge-pulse-green'}`}>
                <span className="pulse-dot"></span>
                {device.status}
              </span>
              <span style={{ fontSize: '0.8rem', color: '#64748B' }}>
                Score: {Math.round((device.confidence || 0.95) * 100)}%
              </span>
            </div>
          </div>

          <div style={{ background: '#090E1A', border: '1px solid #1E293B', borderRadius: '8px', padding: '0.75rem' }}>
            <span style={{ fontSize: '0.75rem', color: '#94A3B8' }}>Current Packet Rate</span>
            <div style={{ fontSize: '1.2rem', fontWeight: 700, fontFamily: 'monospace', color: isIntrusion ? '#FF2A6D' : '#00F0FF', marginTop: '0.2rem' }}>
              {device.packet_rate} pkt/s
            </div>
          </div>

          <div style={{ background: '#090E1A', border: '1px solid #1E293B', borderRadius: '8px', padding: '0.75rem' }}>
            <span style={{ fontSize: '0.75rem', color: '#94A3B8' }}>Mean Packet Rate</span>
            <div style={{ fontSize: '1rem', fontWeight: 600, fontFamily: 'monospace', color: '#E2E8F0', marginTop: '0.2rem' }}>
              {device.mean_packet_rate} pkt/s
            </div>
          </div>

          <div style={{ background: '#090E1A', border: '1px solid #1E293B', borderRadius: '8px', padding: '0.75rem' }}>
            <span style={{ fontSize: '0.75rem', color: '#94A3B8' }}>Median Packet Rate</span>
            <div style={{ fontSize: '1rem', fontWeight: 600, fontFamily: 'monospace', color: '#E2E8F0', marginTop: '0.2rem' }}>
              {device.median_packet_rate} pkt/s
            </div>
          </div>

          <div style={{ background: '#090E1A', border: '1px solid #1E293B', borderRadius: '8px', padding: '0.75rem' }}>
            <span style={{ fontSize: '0.75rem', color: '#94A3B8' }}>Maximum Packet Rate</span>
            <div style={{ fontSize: '1rem', fontWeight: 600, fontFamily: 'monospace', color: '#E2E8F0', marginTop: '0.2rem' }}>
              {device.maximum_packet_rate} pkt/s
            </div>
          </div>

          <div style={{ background: '#090E1A', border: '1px solid #1E293B', borderRadius: '8px', padding: '0.75rem' }}>
            <span style={{ fontSize: '0.75rem', color: '#94A3B8' }}>Last Active Timestamp</span>
            <div style={{ fontSize: '1rem', fontWeight: 600, fontFamily: 'monospace', color: '#CBD5E1', marginTop: '0.2rem' }}>
              {device.last_seen}
            </div>
          </div>
        </div>

        {/* Historical Packet Rate Graph */}
        <div style={{ marginTop: '1rem' }}>
          <h4 style={{ fontSize: '0.85rem', fontWeight: 600, color: '#94A3B8', marginBottom: '0.75rem', display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
            <Activity size={15} color="#00F0FF" />
            HISTORICAL PACKET ARRIVAL RATE
          </h4>
          <div style={{ width: '100%', height: 180, background: '#090E1A', borderRadius: '8px', padding: '0.5rem', border: '1px solid #1E293B' }}>
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={historyData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1E293B" />
                <XAxis dataKey="timestamp" stroke="#64748B" fontSize={10} />
                <YAxis stroke="#64748B" fontSize={10} unit=" pkt/s" />
                <Tooltip contentStyle={{ background: '#0F172A', borderColor: '#334155', fontSize: '11px', color: '#FFF' }} />
                <Area type="monotone" dataKey="rate" stroke={isIntrusion ? '#FF2A6D' : '#00F0FF'} fill={isIntrusion ? 'rgba(255, 42, 109, 0.2)' : 'rgba(0, 240, 255, 0.2)'} />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
}
