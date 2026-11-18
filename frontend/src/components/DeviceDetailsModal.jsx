import React from 'react';
import { X, Cpu, Activity } from 'lucide-react';
import { ResponsiveContainer, AreaChart, Area, XAxis, YAxis, Tooltip, CartesianGrid } from 'recharts';
import StatusBadge from './StatusBadge';

export default function DeviceDetailsModal({ device, onClose }) {
  if (!device) return null;

  const isIntrusion = device.status === 'INTRUSION' || device.status === 'ACTIVE_INTRUSION';
  const historyData = device.rate_history && device.rate_history.length > 0
    ? device.rate_history
    : [
        { timestamp: device.last_seen || '00:00:00', rate: device.packet_rate || 0 }
      ];

  const strokeColor = isIntrusion ? 'var(--status-intrusion)' : 'var(--accent-primary)';
  const fillColor = isIntrusion ? 'var(--status-intrusion)' : 'var(--accent-primary)';

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        {/* Modal Header */}
        <div style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'flex-start',
          borderBottom: '1px solid var(--border-default)',
          paddingBottom: '0.85rem',
          marginBottom: '1.25rem'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
            <div style={{
              width: 38,
              height: 38,
              borderRadius: 'var(--radius-lg)',
              background: isIntrusion ? 'var(--status-intrusion-bg)' : 'var(--accent-muted)',
              border: `1px solid ${isIntrusion ? 'var(--status-intrusion-border)' : 'var(--border-subtle)'}`,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: isIntrusion ? 'var(--status-intrusion)' : 'var(--accent-primary)'
            }}>
              <Cpu size={20} strokeWidth={2} />
            </div>

            <div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <h3 style={{ fontSize: '1.1rem', fontWeight: 600, color: 'var(--text-primary)', letterSpacing: '-0.02em' }}>
                  {device.name || 'Unknown Endpoint'}
                </h3>
                <span className="lumi-badge" style={{
                  background: device.endpoint_type === 'EXTERNAL' ? 'var(--status-warning-bg)' : 'var(--bg-subtle)',
                  color: device.endpoint_type === 'EXTERNAL' ? 'var(--status-warning)' : 'var(--text-secondary)',
                  fontSize: '0.68rem',
                  padding: '0.12rem 0.45rem'
                }}>
                  {device.endpoint_type || 'LOCAL'}
                </span>
              </div>
              <p style={{ fontSize: '0.82rem', fontFamily: 'var(--font-mono)', color: 'var(--accent-primary)', marginTop: '0.15rem' }}>
                IPv4: {device.ip}
              </p>
            </div>
          </div>

          <button
            onClick={onClose}
            className="btn-outline"
            style={{ padding: '0.35rem', borderRadius: 'var(--radius-md)' }}
            title="Close dialog"
          >
            <X size={16} />
          </button>
        </div>

        {/* Telemetry Feature Tiles */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '0.75rem', marginBottom: '1.4rem' }}>
          <div style={{ background: 'var(--bg-card)', border: '1px solid var(--border-default)', borderRadius: 'var(--radius-md)', padding: '0.75rem' }}>
            <span style={{ fontSize: '0.72rem', color: 'var(--text-tertiary)', textTransform: 'uppercase', letterSpacing: '0.04em' }}>SVM Prediction</span>
            <div style={{ marginTop: '0.35rem' }}>
              <StatusBadge status={device.status} />
            </div>
          </div>

          <div style={{ background: 'var(--bg-card)', border: '1px solid var(--border-default)', borderRadius: 'var(--radius-md)', padding: '0.75rem' }}>
            <span style={{ fontSize: '0.72rem', color: 'var(--text-tertiary)', textTransform: 'uppercase', letterSpacing: '0.04em' }}>Current Arrival Rate</span>
            <div style={{
              fontSize: '1.25rem',
              fontWeight: 700,
              fontFamily: 'var(--font-mono)',
              color: isIntrusion ? 'var(--status-intrusion)' : 'var(--accent-primary)',
              marginTop: '0.2rem'
            }}>
              {device.packet_rate} <span style={{ fontSize: '0.75rem', fontWeight: 400, color: 'var(--text-tertiary)' }}>pkt/s</span>
            </div>
          </div>

          <div style={{ background: 'var(--bg-card)', border: '1px solid var(--border-default)', borderRadius: 'var(--radius-md)', padding: '0.75rem' }}>
            <span style={{ fontSize: '0.72rem', color: 'var(--text-tertiary)', textTransform: 'uppercase', letterSpacing: '0.04em' }}>Feature: Mean Rate</span>
            <div style={{ fontSize: '1rem', fontWeight: 600, fontFamily: 'var(--font-mono)', color: 'var(--text-primary)', marginTop: '0.2rem' }}>
              {device.mean_packet_rate ?? 0} <span style={{ fontSize: '0.75rem', color: 'var(--text-tertiary)' }}>pkt/s</span>
            </div>
          </div>

          <div style={{ background: 'var(--bg-card)', border: '1px solid var(--border-default)', borderRadius: 'var(--radius-md)', padding: '0.75rem' }}>
            <span style={{ fontSize: '0.72rem', color: 'var(--text-tertiary)', textTransform: 'uppercase', letterSpacing: '0.04em' }}>Feature: Median Rate</span>
            <div style={{ fontSize: '1rem', fontWeight: 600, fontFamily: 'var(--font-mono)', color: 'var(--text-primary)', marginTop: '0.2rem' }}>
              {device.median_packet_rate ?? 0} <span style={{ fontSize: '0.75rem', color: 'var(--text-tertiary)' }}>pkt/s</span>
            </div>
          </div>

          <div style={{ background: 'var(--bg-card)', border: '1px solid var(--border-default)', borderRadius: 'var(--radius-md)', padding: '0.75rem' }}>
            <span style={{ fontSize: '0.72rem', color: 'var(--text-tertiary)', textTransform: 'uppercase', letterSpacing: '0.04em' }}>Feature: Max Rate</span>
            <div style={{
              fontSize: '1rem',
              fontWeight: 700,
              fontFamily: 'var(--font-mono)',
              color: isIntrusion ? 'var(--status-intrusion)' : 'var(--text-primary)',
              marginTop: '0.2rem'
            }}>
              {device.maximum_packet_rate ?? device.max_packet_rate ?? 0} <span style={{ fontSize: '0.75rem', color: 'var(--text-tertiary)' }}>pkt/s</span>
            </div>
          </div>

          <div style={{ background: 'var(--bg-card)', border: '1px solid var(--border-default)', borderRadius: 'var(--radius-md)', padding: '0.75rem' }}>
            <span style={{ fontSize: '0.72rem', color: 'var(--text-tertiary)', textTransform: 'uppercase', letterSpacing: '0.04em' }}>Last Seen Telemetry</span>
            <div style={{ fontSize: '0.92rem', fontWeight: 500, fontFamily: 'var(--font-mono)', color: 'var(--text-secondary)', marginTop: '0.25rem' }}>
              {device.last_seen || 'Active'}
            </div>
          </div>
        </div>

        {/* Small Rate History Graph */}
        <div>
          <h4 style={{
            fontSize: '0.8rem',
            fontWeight: 600,
            color: 'var(--text-secondary)',
            marginBottom: '0.65rem',
            display: 'flex',
            alignItems: 'center',
            gap: '0.4rem',
            textTransform: 'uppercase',
            letterSpacing: '0.04em'
          }}>
            <Activity size={14} color="var(--accent-primary)" />
            Observed Packet Arrival Frequencies
          </h4>

          <div style={{
            width: '100%',
            height: 190,
            background: 'var(--bg-card)',
            borderRadius: 'var(--radius-lg)',
            padding: '0.75rem',
            border: '1px solid var(--border-default)'
          }}>
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={historyData}>
                <defs>
                  <linearGradient id="modalGradient" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor={fillColor} stopOpacity={0.25} />
                    <stop offset="95%" stopColor={fillColor} stopOpacity={0.0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="var(--border-subtle)" vertical={false} />
                <XAxis dataKey="timestamp" stroke="var(--text-tertiary)" fontSize={10} tickLine={false} />
                <YAxis stroke="var(--text-tertiary)" fontSize={10} tickLine={false} unit=" pkt/s" />
                <Tooltip
                  contentStyle={{
                    background: 'var(--bg-surface)',
                    border: '1px solid var(--border-default)',
                    borderRadius: 'var(--radius-md)',
                    fontSize: '11px',
                    color: 'var(--text-primary)',
                    fontFamily: 'var(--font-mono)'
                  }}
                />
                <Area type="monotone" dataKey="rate" stroke={strokeColor} strokeWidth={2} fill="url(#modalGradient)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
}
