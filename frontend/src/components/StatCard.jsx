import React from 'react';
import { Cpu, CheckCircle2, AlertOctagon, Activity } from 'lucide-react';

export default function StatCard({ totalDevices, normalDevices, activeIntrusions, averagePacketRate }) {
  const cards = [
    {
      title: 'Monitored Endpoints',
      value: totalDevices ?? 0,
      unit: '',
      subtext: 'Active IoT nodes on subnet',
      icon: Cpu,
      accentColor: 'var(--accent-primary)',
      isAlert: false
    },
    {
      title: 'Normal Traffic Nodes',
      value: normalDevices ?? 0,
      unit: '',
      subtext: 'Operating within baseline rates',
      icon: CheckCircle2,
      accentColor: 'var(--status-normal)',
      isAlert: false
    },
    {
      title: 'Active Intrusions',
      value: activeIntrusions ?? 0,
      unit: '',
      subtext: (activeIntrusions || 0) > 0 ? 'Abnormal packet rate flagged' : 'Zero malicious threats',
      icon: AlertOctagon,
      accentColor: (activeIntrusions || 0) > 0 ? 'var(--status-intrusion)' : 'var(--text-tertiary)',
      isAlert: (activeIntrusions || 0) > 0
    },
    {
      title: 'Avg Packet Arrival Rate',
      value: typeof averagePacketRate === 'number' ? averagePacketRate.toFixed(1) : (averagePacketRate ?? 0),
      unit: 'pkt/s',
      subtext: 'Rolling observation window',
      icon: Activity,
      accentColor: '#6366f1',
      isAlert: false
    },
  ];

  return (
    <div className="cards-grid">
      {cards.map((card, idx) => {
        const Icon = card.icon;
        return (
          <div
            key={idx}
            className={`lumi-card lumi-stat-card ${card.isAlert ? 'lumi-card-alert' : ''}`}
          >
            <div className="stat-header">
              <span className="stat-title">{card.title}</span>
              <div
                className="stat-icon-wrapper"
                style={{ color: card.accentColor }}
              >
                <Icon size={16} strokeWidth={2} />
              </div>
            </div>

            <div>
              <div
                className="metric-card-val"
                style={{ color: card.isAlert ? 'var(--status-intrusion)' : 'var(--text-primary)' }}
              >
                {card.value}
                {card.unit && <span className="metric-card-unit">{card.unit}</span>}
              </div>
              <div className="stat-subtext" style={{ marginTop: '0.4rem' }}>
                {card.isAlert ? (
                  <span style={{ color: 'var(--status-intrusion)', fontWeight: 600 }}>
                    ● Immediate attention required
                  </span>
                ) : (
                  <span>{card.subtext}</span>
                )}
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
}
