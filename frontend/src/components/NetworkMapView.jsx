import React from 'react';
import { Router, ShieldAlert, Laptop, Globe } from 'lucide-react';

export default function NetworkMapView({ devices = [], onSelectDevice }) {
  const routerNode = { ip: '192.168.1.1', name: 'Edge Gateway (GuardNode)', type: 'router' };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.4rem' }}>
      {/* Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '0.75rem' }}>
        <div>
          <h1 style={{ fontSize: '1.35rem', fontWeight: 600, color: 'var(--text-primary)', letterSpacing: '-0.025em' }}>
            Local Subnet Topology & Threat Map
          </h1>
          <p style={{ fontSize: '0.78rem', color: 'var(--text-secondary)', marginTop: '0.2rem' }}>
            Real-time visual node connectivity and intrusion classification relative to Edge Gateway
          </p>
        </div>

        <span className="lumi-badge" style={{ background: 'var(--bg-subtle)', color: 'var(--text-secondary)' }}>
          Subnet: 192.168.1.0/24
        </span>
      </div>

      {/* Topology Canvas */}
      <div className="lumi-card" style={{
        minHeight: '520px',
        padding: '2.5rem 1.5rem',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        gap: '3rem',
        background: 'radial-gradient(ellipse at center, var(--bg-surface) 0%, var(--bg-card) 100%)',
        position: 'relative',
        overflow: 'hidden'
      }}>
        {/* Gateway Router Node */}
        <div style={{
          background: 'var(--bg-surface)',
          border: '1px solid var(--accent-primary)',
          boxShadow: '0 0 25px var(--accent-glow), var(--inner-highlight)',
          borderRadius: 'var(--radius-xl)',
          padding: '1rem 1.75rem',
          display: 'flex',
          alignItems: 'center',
          gap: '1rem',
          zIndex: 2
        }}>
          <div style={{
            width: 42,
            height: 42,
            borderRadius: 'var(--radius-lg)',
            background: 'var(--accent-muted)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: 'var(--accent-primary)'
          }}>
            <Router size={24} strokeWidth={2.2} />
          </div>
          <div>
            <div style={{ fontWeight: 600, color: 'var(--text-primary)', fontSize: '0.95rem' }}>{routerNode.name}</div>
            <div style={{ fontSize: '0.75rem', fontFamily: 'var(--font-mono)', color: 'var(--accent-primary)' }}>{routerNode.ip}</div>
          </div>
          <span className="lumi-badge lumi-badge-normal" style={{ marginLeft: '0.75rem', fontSize: '0.68rem' }}>
            IDS ACTIVE
          </span>
        </div>

        {/* Subnet Nodes Grid */}
        <div style={{
          display: 'flex',
          flexWrap: 'wrap',
          justifyContent: 'center',
          gap: '1.25rem',
          maxWidth: '1100px',
          width: '100%',
          zIndex: 2
        }}>
          {devices.length === 0 ? (
            <div style={{ color: 'var(--text-tertiary)', fontSize: '0.85rem' }}>
              Scanning subnet for connected IoT hardware...
            </div>
          ) : (
            devices.map((dev) => {
              const isIntrusion = dev.status === 'INTRUSION' || dev.status === 'ACTIVE_INTRUSION';
              const isExternal = dev.endpoint_type === 'EXTERNAL';

              return (
                <div
                  key={dev.ip}
                  onClick={() => onSelectDevice?.(dev)}
                  style={{
                    background: isIntrusion ? 'rgba(244, 63, 94, 0.05)' : 'var(--bg-surface)',
                    border: `1px solid ${isIntrusion ? 'var(--status-intrusion-border)' : 'var(--border-default)'}`,
                    boxShadow: isIntrusion ? '0 0 20px rgba(244, 63, 94, 0.15)' : 'var(--shadow-card)',
                    borderRadius: 'var(--radius-lg)',
                    padding: '1.1rem',
                    width: '230px',
                    display: 'flex',
                    flexDirection: 'column',
                    gap: '0.65rem',
                    cursor: 'pointer',
                    transition: 'all 0.15s ease'
                  }}
                  onMouseEnter={(e) => {
                    e.currentTarget.style.transform = 'translateY(-2px)';
                    e.currentTarget.style.borderColor = isIntrusion ? 'var(--status-intrusion)' : 'var(--border-strong)';
                  }}
                  onMouseLeave={(e) => {
                    e.currentTarget.style.transform = 'translateY(0)';
                    e.currentTarget.style.borderColor = isIntrusion ? 'var(--status-intrusion-border)' : 'var(--border-default)';
                  }}
                >
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <div style={{
                      width: 28,
                      height: 28,
                      borderRadius: 'var(--radius-md)',
                      background: isIntrusion ? 'var(--status-intrusion-bg)' : 'var(--bg-subtle)',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      color: isIntrusion ? 'var(--status-intrusion)' : 'var(--text-secondary)'
                    }}>
                      {isIntrusion ? <ShieldAlert size={15} /> : isExternal ? <Globe size={15} /> : <Laptop size={15} />}
                    </div>
                    <span className={`lumi-badge ${isIntrusion ? 'badge-pulse-red' : 'badge-pulse-green'}`} style={{ fontSize: '0.68rem', padding: '0.12rem 0.45rem' }}>
                      <span className="pulse-dot" />
                      {isIntrusion ? 'THREAT' : 'NORMAL'}
                    </span>
                  </div>

                  <div>
                    <div style={{ fontSize: '0.86rem', fontWeight: 600, color: 'var(--text-primary)', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                      {dev.name || 'IoT Endpoint'}
                    </div>
                    <div style={{ fontSize: '0.75rem', fontFamily: 'var(--font-mono)', color: 'var(--accent-primary)', marginTop: '0.1rem' }}>
                      {dev.ip}
                    </div>
                  </div>

                  <div style={{
                    fontSize: '0.72rem',
                    background: 'var(--bg-card)',
                    border: '1px solid var(--border-subtle)',
                    padding: '0.35rem 0.55rem',
                    borderRadius: 'var(--radius-sm)',
                    fontFamily: 'var(--font-mono)',
                    color: isIntrusion ? 'var(--status-intrusion)' : 'var(--text-secondary)',
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center'
                  }}>
                    <span>Rate:</span>
                    <span style={{ fontWeight: 600 }}>{dev.packet_rate} pkt/s</span>
                  </div>
                </div>
              );
            })
          )}
        </div>
      </div>
    </div>
  );
}
