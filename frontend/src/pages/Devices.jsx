import React, { useState } from 'react';
import { Eye, Search, Laptop, Globe, ShieldAlert } from 'lucide-react';
import StatusBadge from '../components/StatusBadge';

export default function Devices({ mode, isMonitoring, scapyError, devices = [], isLoading, onSelectDevice }) {
  const isLiveCaptureUnavailable = mode === 'LIVE' && !isMonitoring;
  const displayDevices = isLiveCaptureUnavailable ? [] : devices;

  const [searchTerm, setSearchTerm] = useState('');
  const [filterType, setFilterType] = useState('ALL');

  const filtered = displayDevices.filter((dev) => {
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

  const localCount = displayDevices.filter(d => d.endpoint_type !== 'EXTERNAL').length;
  const externalCount = displayDevices.filter(d => d.endpoint_type === 'EXTERNAL').length;
  const intrusionCount = displayDevices.filter(d => d.status === 'INTRUSION' || d.status === 'ACTIVE_INTRUSION').length;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.4rem' }}>
      {/* Top Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '0.75rem' }}>
        <div>
          <h1 style={{ fontSize: '1.35rem', fontWeight: 600, color: 'var(--text-primary)', letterSpacing: '-0.025em' }}>
            Monitored Network Endpoints
          </h1>
          <p style={{ fontSize: '0.78rem', color: 'var(--text-secondary)', marginTop: '0.2rem' }}>
            Active local subnet and external devices evaluated by the packet arrival rate classifier
          </p>
        </div>

        <span className="lumi-badge" style={{ background: 'var(--bg-subtle)', color: 'var(--text-secondary)' }}>
          {displayDevices.length} Total Nodes Detected
        </span>
      </div>

      {/* Mini Stats Ribbon */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '0.85rem' }}>
        <div className="lumi-card" style={{ padding: '0.85rem 1.1rem' }}>
          <span style={{ fontSize: '0.72rem', color: 'var(--text-tertiary)' }}>Total Observed</span>
          <div style={{ fontSize: '1.4rem', fontWeight: 700, fontFamily: 'var(--font-mono)', color: 'var(--text-primary)', marginTop: '0.15rem' }}>
            {displayDevices.length}
          </div>
        </div>

        <div className="lumi-card" style={{ padding: '0.85rem 1.1rem' }}>
          <span style={{ fontSize: '0.72rem', color: 'var(--text-tertiary)' }}>Local Subnet Devices</span>
          <div style={{ fontSize: '1.4rem', fontWeight: 700, fontFamily: 'var(--font-mono)', color: 'var(--accent-primary)', marginTop: '0.15rem' }}>
            {localCount}
          </div>
        </div>

        <div className="lumi-card" style={{ padding: '0.85rem 1.1rem' }}>
          <span style={{ fontSize: '0.72rem', color: 'var(--text-tertiary)' }}>External Hosts</span>
          <div style={{ fontSize: '1.4rem', fontWeight: 700, fontFamily: 'var(--font-mono)', color: 'var(--status-warning)', marginTop: '0.15rem' }}>
            {externalCount}
          </div>
        </div>

        <div className="lumi-card" style={{ padding: '0.85rem 1.1rem' }}>
          <span style={{ fontSize: '0.72rem', color: 'var(--text-tertiary)' }}>Intrusions Detected</span>
          <div style={{ fontSize: '1.4rem', fontWeight: 700, fontFamily: 'var(--font-mono)', color: intrusionCount > 0 ? 'var(--status-intrusion)' : 'var(--status-normal)', marginTop: '0.15rem' }}>
            {intrusionCount}
          </div>
        </div>
      </div>

      {isLiveCaptureUnavailable && (
        <div className="lumi-card lumi-card-alert" style={{ padding: '0.85rem 1.15rem', color: 'var(--status-intrusion)', fontSize: '0.82rem', fontWeight: 600 }}>
          Live packet capture is unavailable. No live traffic is being analyzed.
        </div>
      )}

      {/* Main Table Card */}
      <div className="lumi-card" style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
        {/* Search & Filter Toolbar */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '0.75rem' }}>
          <div style={{ position: 'relative' }}>
            <Search size={14} color="var(--text-tertiary)" style={{ position: 'absolute', left: 9, top: 9 }} />
            <input
              type="text"
              placeholder="Filter by name or IP..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="lumi-input"
              style={{ paddingLeft: '1.75rem', width: '220px' }}
            />
          </div>

          <div style={{ display: 'flex', gap: '4px', flexWrap: 'wrap' }}>
            {['ALL', 'NORMAL', 'INTRUSION', 'LOCAL', 'EXTERNAL'].map((type) => (
              <button
                key={type}
                onClick={() => setFilterType(type)}
                className={`filter-chip ${filterType === type ? 'active' : ''}`}
              >
                {type}
              </button>
            ))}
          </div>
        </div>

        {/* Table Container */}
        <div className="table-wrapper">
          <table className="custom-table">
            <thead>
              <tr>
                <th>Endpoint Identifier</th>
                <th>IP Address</th>
                <th>Network Scope</th>
                <th>Current Rate</th>
                <th>SVM Classifier</th>
                <th>Last Seen</th>
                <th style={{ textAlign: 'right' }}>Actions</th>
              </tr>
            </thead>
            <tbody>
              {isLoading && displayDevices.length === 0 ? (
                <tr>
                  <td colSpan={7} style={{ textAlign: 'center', color: 'var(--text-tertiary)', padding: '2.5rem' }}>
                    Scanning active network endpoints...
                  </td>
                </tr>
              ) : isLiveCaptureUnavailable ? (
                <tr>
                  <td colSpan={7} style={{ textAlign: 'center', color: 'var(--status-intrusion)', padding: '2.5rem', fontWeight: 500 }}>
                    Live packet capture is unavailable. No live traffic is being analyzed.
                  </td>
                </tr>
              ) : filtered.length === 0 ? (
                <tr>
                  <td colSpan={7} style={{ textAlign: 'center', color: 'var(--text-tertiary)', padding: '2.5rem' }}>
                    No network endpoints found matching filter.
                  </td>
                </tr>
              ) : (
                filtered.map((dev) => {
                  const isIntrusion = dev.status === 'INTRUSION' || dev.status === 'ACTIVE_INTRUSION';
                  const isExternal = dev.endpoint_type === 'EXTERNAL';
                  return (
                    <tr key={dev.ip}>
                      <td style={{ fontWeight: 600, color: 'var(--text-primary)' }}>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                          <div style={{
                            width: 26,
                            height: 26,
                            borderRadius: 'var(--radius-sm)',
                            background: isIntrusion ? 'var(--status-intrusion-bg)' : 'var(--bg-subtle)',
                            color: isIntrusion ? 'var(--status-intrusion)' : 'var(--text-secondary)',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            flexShrink: 0
                          }}>
                            {isIntrusion ? <ShieldAlert size={14} /> : isExternal ? <Globe size={14} /> : <Laptop size={14} />}
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
                      <td style={{ fontFamily: 'var(--font-mono)', fontWeight: 600, color: isIntrusion ? 'var(--status-intrusion)' : 'var(--text-primary)' }}>
                        {dev.packet_rate} <span style={{ fontSize: '0.72rem', fontWeight: 400, color: 'var(--text-tertiary)' }}>pkt/s</span>
                      </td>
                      <td>
                        <StatusBadge status={dev.status} />
                      </td>
                      <td style={{ fontFamily: 'var(--font-mono)', fontSize: '0.78rem', color: 'var(--text-tertiary)' }}>
                        {dev.last_seen || 'Active'}
                      </td>
                      <td style={{ textAlign: 'right' }}>
                        <button
                          onClick={() => onSelectDevice(dev)}
                          className="btn-outline"
                          style={{ padding: '0.25rem 0.6rem' }}
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
    </div>
  );
}
