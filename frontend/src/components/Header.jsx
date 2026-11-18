import React, { useState } from 'react';
import { Shield, Radio, Server, Play, Square, Palette, ChevronDown, Check } from 'lucide-react';

export default function Header({
  mode,
  isMonitoring,
  isConnected,
  interfaces = [],
  activeInterface,
  onSelectInterface,
  onStartMonitoring,
  onStopMonitoring,
  onToggleMode,
  onShowToast,
  activeTab = 'dashboard'
}) {
  const [showThemeMenu, setShowThemeMenu] = useState(false);
  const [currentTheme, setCurrentTheme] = useState(() => {
    return document.documentElement.getAttribute('data-theme') || 'lagoon';
  });

  const themes = [
    { id: 'lagoon', name: 'Lumi Lagoon (Sky)', color: '#0ea5e9' },
    { id: 'celeste', name: 'Lumi Celeste (Indigo)', color: '#818cf8' },
    { id: 'canopy', name: 'Lumi Canopy (Emerald)', color: '#10b981' },
    { id: 'light', name: 'Lumi Clean (Light)', color: '#0284c7' },
  ];

  const handleSelectTheme = (themeId) => {
    document.documentElement.setAttribute('data-theme', themeId);
    setCurrentTheme(themeId);
    setShowThemeMenu(false);
    onShowToast?.(`Theme switched to ${themeId.toUpperCase()}`);
  };

  const getBreadcrumb = (tab) => {
    switch (tab) {
      case 'dashboard': return 'Dashboard Overview';
      case 'devices': return 'Monitored Endpoints';
      case 'alerts': return 'Intrusion Alerts';
      case 'network': return 'Subnet Topology';
      case 'model': return 'SVM Model Performance';
      case 'settings': return 'System Settings';
      default: return 'Monitoring';
    }
  };

  return (
    <header className="app-header">
      {/* Brand & Breadcrumbs */}
      <div className="header-title-group">
        <div className="brand-icon">
          <Shield size={17} strokeWidth={2.4} />
        </div>
        <div>
          <div className="brand-title">
            GuardNode
            <span className="brand-pill">IoT IDS</span>
          </div>
          <div className="brand-subtitle" style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
            <span>Network Security</span>
            <span style={{ color: 'var(--text-disabled)' }}>/</span>
            <span style={{ color: 'var(--text-secondary)' }}>{getBreadcrumb(activeTab)}</span>
          </div>
        </div>
      </div>

      {/* Controls & Status Bar */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.85rem', flexWrap: 'wrap' }}>
        {/* Backend Connection Status */}
        <div className="lumi-badge" style={{
          background: isConnected ? 'var(--status-normal-bg)' : 'var(--status-intrusion-bg)',
          color: isConnected ? 'var(--status-normal)' : 'var(--status-intrusion)',
          borderColor: isConnected ? 'var(--status-normal-border)' : 'var(--status-intrusion-border)',
        }}>
          <span className="pulse-dot" style={{ backgroundColor: isConnected ? 'var(--status-normal)' : 'var(--status-intrusion)' }} />
          <span>{isConnected ? 'FASTAPI CONNECTED' : 'BACKEND OFFLINE'}</span>
        </div>

        {/* Interface Selector (when in LIVE mode) */}
        {mode === 'LIVE' && (
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.45rem' }}>
            <span style={{ fontSize: '0.75rem', color: 'var(--text-tertiary)', fontWeight: 500 }}>Interface:</span>
            <select
              value={activeInterface}
              onChange={(e) => onSelectInterface(e.target.value)}
              className="lumi-select"
              style={{ minWidth: '220px', maxWidth: '320px' }}
            >
              {interfaces.map((iface) => (
                <option key={iface.id} value={iface.id}>
                  {iface.name}
                </option>
              ))}
            </select>

            {isMonitoring ? (
              <button
                onClick={onStopMonitoring}
                className="btn-destructive"
                style={{ padding: '0.35rem 0.65rem', fontSize: '0.75rem' }}
                title="Stop packet capture"
              >
                <Square size={12} fill="currentColor" />
                Stop
              </button>
            ) : (
              <button
                onClick={onStartMonitoring}
                className="btn-primary"
                style={{ padding: '0.35rem 0.65rem', fontSize: '0.75rem' }}
                title="Start packet capture"
              >
                <Play size={12} fill="currentColor" />
                Start
              </button>
            )}
          </div>
        )}

        {/* DEMO / LIVE Mode Segmented Control */}
        <div className="lumi-segmented">
          <button
            onClick={() => onToggleMode('DEMO')}
            className={`lumi-segmented-btn ${mode === 'DEMO' ? 'active' : ''}`}
          >
            <Radio size={12} />
            DEMO
          </button>
          <button
            onClick={() => onToggleMode('LIVE')}
            className={`lumi-segmented-btn ${mode === 'LIVE' ? 'active' : ''}`}
          >
            <Server size={12} />
            LIVE
          </button>
        </div>

        {/* Monitoring State Badge */}
        <div className={`lumi-badge ${isMonitoring ? 'badge-pulse-green' : 'badge-pulse-red'}`}>
          <span className="pulse-dot" />
          <span>{isMonitoring ? `${mode}: ACTIVE` : `${mode}: PAUSED`}</span>
        </div>

        {/* Lumi Theme Dropdown */}
        <div style={{ position: 'relative' }}>
          <button
            onClick={() => setShowThemeMenu(!showThemeMenu)}
            className="btn-outline"
            style={{ padding: '0.32rem 0.6rem' }}
            title="Lumi Theme"
          >
            <Palette size={13} />
            <span style={{ textTransform: 'capitalize' }}>{currentTheme}</span>
            <ChevronDown size={11} />
          </button>

          {showThemeMenu && (
            <div style={{
              position: 'absolute',
              top: 'calc(100% + 6px)',
              right: 0,
              background: 'var(--bg-surface)',
              border: '1px solid var(--border-default)',
              borderRadius: 'var(--radius-lg)',
              padding: '0.35rem',
              minWidth: '190px',
              boxShadow: 'var(--shadow-elevated)',
              zIndex: 100,
              display: 'flex',
              flexDirection: 'column',
              gap: '2px'
            }}>
              <div style={{ fontSize: '0.68rem', fontWeight: 600, color: 'var(--text-tertiary)', padding: '0.3rem 0.6rem', textTransform: 'uppercase' }}>
                Lumi Color Palette
              </div>
              {themes.map((t) => (
                <button
                  key={t.id}
                  onClick={() => handleSelectTheme(t.id)}
                  style={{
                    background: currentTheme === t.id ? 'var(--bg-subtle)' : 'transparent',
                    border: 'none',
                    color: 'var(--text-primary)',
                    padding: '0.45rem 0.65rem',
                    borderRadius: 'var(--radius-md)',
                    fontSize: '0.78rem',
                    cursor: 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    width: '100%',
                    textAlign: 'left'
                  }}
                >
                  <span style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                    <span style={{ width: 8, height: 8, borderRadius: '50%', backgroundColor: t.color }} />
                    {t.name}
                  </span>
                  {currentTheme === t.id && <Check size={13} color="var(--accent-primary)" />}
                </button>
              ))}
            </div>
          )}
        </div>
      </div>
    </header>
  );
}
