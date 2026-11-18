import React from 'react';
import {
  LayoutDashboard,
  Cpu,
  AlertTriangle,
  Settings,
  Shield,
  Network,
  BarChart3
} from 'lucide-react';

export default function Sidebar({ activeTab, onTabChange, alertsCount = 0 }) {
  const navSections = [
    {
      title: 'Monitoring',
      items: [
        { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
        { id: 'network', label: 'Subnet Topology', icon: Network },
      ]
    },
    {
      title: 'Security Intelligence',
      items: [
        { id: 'devices', label: 'Endpoints', icon: Cpu },
        {
          id: 'alerts',
          label: 'Intrusion Alerts',
          icon: AlertTriangle,
          badge: alertsCount > 0 ? alertsCount : null
        },
        { id: 'model', label: 'SVM Performance', icon: BarChart3 },
      ]
    },
    {
      title: 'System',
      items: [
        { id: 'settings', label: 'Configuration', icon: Settings },
      ]
    }
  ];

  return (
    <aside className="app-sidebar">
      <div>
        {/* Workspace Pill (Lumi sidebar-01 header) */}
        <div className="sidebar-header">
          <div className="sidebar-workspace-pill">
            <div style={{
              width: 28,
              height: 28,
              borderRadius: 'var(--radius-md)',
              background: 'linear-gradient(135deg, var(--accent-primary), #6366f1)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: '#fff',
              boxShadow: 'var(--shadow-sm)'
            }}>
              <Shield size={16} strokeWidth={2.4} />
            </div>
            <div style={{ flex: 1, minWidth: 0 }}>
              <div style={{ fontSize: '0.86rem', fontWeight: 600, color: 'var(--text-primary)', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                GuardNode IoT
              </div>
              <div style={{ fontSize: '0.7rem', color: 'var(--text-tertiary)', display: 'flex', alignItems: 'center', gap: '0.3rem' }}>
                <span style={{ width: 5, height: 5, borderRadius: '50%', backgroundColor: 'var(--status-normal)' }}></span>
                Edge Cluster 01
              </div>
            </div>
          </div>
        </div>

        {/* Grouped Navigation */}
        <nav style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
          {navSections.map((section, sIdx) => (
            <div key={sIdx}>
              <div className="nav-section-title">{section.title}</div>
              <ul className="nav-list">
                {section.items.map((item) => {
                  const Icon = item.icon;
                  const isActive = activeTab === item.id;
                  return (
                    <li
                      key={item.id}
                      className={`nav-item ${isActive ? 'active' : ''}`}
                      onClick={() => onTabChange(item.id)}
                    >
                      <div className="nav-item-left">
                        <Icon size={16} strokeWidth={isActive ? 2.2 : 1.8} />
                        <span>{item.label}</span>
                      </div>
                      {item.badge && (
                        <span className="nav-count-badge">
                          {item.badge}
                        </span>
                      )}
                    </li>
                  );
                })}
              </ul>
            </div>
          ))}
        </nav>
      </div>

      {/* Model Spec Card (Lumi footer pattern) */}
      <div className="sidebar-footer-card">
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.35rem' }}>
          <span style={{ fontSize: '0.72rem', fontWeight: 600, color: 'var(--text-secondary)', textTransform: 'uppercase', letterSpacing: '0.04em' }}>
            LinearSVC Model
          </span>
          <span className="lumi-badge lumi-badge-normal" style={{ padding: '0.1rem 0.4rem', fontSize: '0.65rem' }}>
            ONLINE
          </span>
        </div>
        <p style={{ fontSize: '0.72rem', color: 'var(--text-tertiary)', lineHeight: 1.35 }}>
          Feature extraction on 3 packet arrival rate windows
        </p>
        <div style={{
          marginTop: '0.5rem',
          paddingTop: '0.5rem',
          borderTop: '1px solid var(--border-subtle)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          fontSize: '0.69rem',
          color: 'var(--text-secondary)'
        }}>
          <span>CICIoT2023 Trained</span>
          <span style={{ fontFamily: 'var(--font-mono)', color: 'var(--accent-primary)' }}>33 Attacks</span>
        </div>
      </div>
    </aside>
  );
}
