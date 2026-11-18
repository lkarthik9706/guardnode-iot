import React, { useState } from 'react';
import { Cpu, Eye, Search, Laptop, ShieldAlert } from 'lucide-react';
import StatusBadge from './StatusBadge';

export default function DeviceTable({ devices = [], onSelectDevice, isLoading, isLiveCaptureUnavailable }) {
  const [searchTerm, setSearchTerm] = useState('');
  const [filterType, setFilterType] = useState('ALL');

  const filteredDevices = devices.filter((dev) => {
    const matchesSearch =
      (dev.name || '').toLowerCase().includes(searchTerm.toLowerCase()) ||
      (dev.ip || '').toLowerCase().includes(searchTerm.toLowerCase());

    if (!matchesSearch) return false;

    if (filterType === 'NORMAL') return dev.status !== 'INTRUSION' && dev.status !== 'ACTIVE_INTRUSION';
    if (filterType === 'INTRUSION') return dev.status === 'INTRUSION' || dev.status === 'ACTIVE_INTRUSION';
    if (filterType === 'LOCAL') return dev.endpoint_type !== 'EXTERNAL';
    if (filterType === 'EXTERNAL') return dev.endpoint_type === 'EXTERNAL';

    return true;
  });

  return (
    <div className="lumi-card" style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
      {/* Table Header & Controls */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '0.85rem' }}>
        <div>
          <h3 style={{ fontSize: '0.92rem', fontWeight: 600, color: 'var(--text-primary)', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <Cpu size={17} color="var(--accent-primary)" />
            OBSERVED NETWORK ENDPOINTS
          </h3>
          <p style={{ fontSize: '0.74rem', color: 'var(--text-tertiary)', marginTop: '0.15rem' }}>
            Real-time telemetry and inter-arrival packet rates per detected node
          </p>
        </div>

        {/* Search & Filter Toolbar */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', flexWrap: 'wrap' }}>
          <div style={{ position: 'relative' }}>
            <Search size={13} color="var(--text-tertiary)" style={{ position: 'absolute', left: 9, top: 9 }} />
            <input
              type="text"
              placeholder="Search IP or hostname..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="lumi-input"
              style={{ paddingLeft: '1.75rem', width: '180px', fontSize: '0.76rem' }}
            />
          </div>

          <div style={{ display: 'flex', gap: '3px' }}>
            {['ALL', 'NORMAL', 'INTRUSION'].map((type) => (
              <button
                key={type}
                onClick={() => setFilterType(type)}
                className={`filter-chip ${filterType === type ? 'active' : ''}`}
              >
                {type}
              </button>
            ))}
          </div>

          <span className="lumi-badge" style={{ background: 'var(--bg-subtle)', color: 'var(--text-secondary)' }}>
            {filteredDevices.length} / {devices.length} Nodes
          </span>
        </div>
      </div>

      {/* Lumi Data Table Container */}
      <div className="table-wrapper">
        <table className="custom-table">
          <thead>
            <tr>
              <th>Endpoint Identifier</th>
              <th>IP Address</th>
              <th>Network Zone</th>
              <th>Window Rate</th>
              <th>Classifier Status</th>
              <th>Last Seen</th>
              <th style={{ textAlign: 'right' }}>Actions</th>
            </tr>
          </thead>
          <tbody>
            {isLoading && devices.length === 0 ? (
              <tr>
                <td colSpan={7} style={{ textAlign: 'center', color: 'var(--text-tertiary)', padding: '2.5rem' }}>
                  Scanning local network endpoints...
                </td>
              </tr>
            ) : isLiveCaptureUnavailable ? (
              <tr>
                <td colSpan={7} style={{ textAlign: 'center', color: 'var(--status-intrusion)', padding: '2.5rem', fontWeight: 500 }}>
                  Live packet capture is unavailable. No live traffic is being analyzed.
                </td>
              </tr>
            ) : filteredDevices.length === 0 ? (
              <tr>
                <td colSpan={7} style={{ textAlign: 'center', color: 'var(--text-tertiary)', padding: '2.5rem' }}>
                  No network endpoints match current criteria.
                </td>
              </tr>
            ) : (
              filteredDevices.map((dev) => {
                const isIntrusion = dev.status === 'INTRUSION' || dev.status === 'ACTIVE_INTRUSION';
                const isExternal = dev.endpoint_type === 'EXTERNAL';
                return (
                  <tr key={dev.ip}>
                    <td style={{ fontWeight: 600, color: 'var(--text-primary)' }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                        <div style={{
                          width: 24,
                          height: 24,
                          borderRadius: 'var(--radius-sm)',
                          background: isIntrusion ? 'var(--status-intrusion-bg)' : 'var(--bg-subtle)',
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                          color: isIntrusion ? 'var(--status-intrusion)' : 'var(--text-secondary)',
                          flexShrink: 0
                        }}>
                          {isIntrusion ? <ShieldAlert size={13} /> : <Laptop size={13} />}
                        </div>
                        <span>{dev.name || 'Unknown Endpoint'}</span>
                      </div>
                    </td>
                    <td style={{ fontFamily: 'var(--font-mono)', fontSize: '0.82rem', color: 'var(--accent-primary)' }}>
                      {dev.ip}
                    </td>
                    <td>
                      <span className="lumi-badge" style={{
                        background: isExternal ? 'var(--status-warning-bg)' : 'var(--bg-subtle)',
                        color: isExternal ? 'var(--status-warning)' : 'var(--text-secondary)',
                        borderColor: isExternal ? 'var(--status-warning-border)' : 'var(--border-subtle)',
                        fontSize: '0.68rem',
                        padding: '0.15rem 0.45rem'
                      }}>
                        {isExternal ? 'EXTERNAL' : 'LOCAL SUBNET'}
                      </span>
                    </td>
                    <td style={{
                      fontFamily: 'var(--font-mono)',
                      fontWeight: 600,
                      color: isIntrusion ? 'var(--status-intrusion)' : 'var(--text-primary)'
                    }}>
                      {dev.packet_rate} <span style={{ fontSize: '0.72rem', fontWeight: 400, color: 'var(--text-tertiary)' }}>pkt/s</span>
                    </td>
                    <td>
                      <StatusBadge status={dev.status} />
                    </td>
                    <td style={{ fontFamily: 'var(--font-mono)', fontSize: '0.78rem', color: 'var(--text-tertiary)' }}>
                      {dev.last_seen || 'Active now'}
                    </td>
                    <td style={{ textAlign: 'right' }}>
                      <button
                        onClick={() => onSelectDevice(dev)}
                        className="btn-outline"
                        style={{ padding: '0.24rem 0.55rem' }}
                      >
                        <Eye size={12} />
                        Inspect
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
