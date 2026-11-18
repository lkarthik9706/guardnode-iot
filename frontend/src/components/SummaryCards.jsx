import React from 'react';
import { Cpu, CheckCircle2, AlertOctagon, Activity } from 'lucide-react';

export default function SummaryCards({ totalDevices, normalDevices, activeIntrusions, averagePacketRate }) {
  const cards = [
    {
      title: 'Devices Detected',
      badge: 'ONLINE',
      badgeColor: '#00F0FF',
      value: totalDevices,
      unit: '',
      icon: Cpu,
      color: '#F8FAFC'
    },
    {
      title: 'Normal Traffic',
      badge: 'SECURE',
      badgeColor: '#10B981',
      value: normalDevices,
      unit: '',
      icon: CheckCircle2,
      color: '#10B981'
    },
    {
      title: 'Active Intrusions',
      badge: 'THREAT',
      badgeColor: activeIntrusions > 0 ? '#FF2A6D' : '#64748B',
      value: activeIntrusions,
      unit: '',
      icon: AlertOctagon,
      color: activeIntrusions > 0 ? '#FF2A6D' : '#F8FAFC',
      isAlert: activeIntrusions > 0
    },
    {
      title: 'Avg Packet Rate',
      badge: 'REAL-TIME',
      badgeColor: '#3B82F6',
      value: averagePacketRate,
      unit: 'pkt/s',
      icon: Activity,
      color: '#3B82F6'
    },
  ];

  return (
    <div className="cards-grid">
      {cards.map((card, idx) => {
        const Icon = card.icon;
        return (
          <div key={idx} className={`cyber-card ${card.isAlert ? 'cyber-card-alert' : ''}`}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
                <Icon size={16} color={card.badgeColor} />
                <span style={{ fontSize: '0.8rem', fontWeight: 600, color: '#94A3B8' }}>
                  {card.title}
                </span>
              </div>
              <span style={{
                fontSize: '0.65rem',
                fontWeight: 700,
                color: card.badgeColor,
                background: `${card.badgeColor}15`,
                border: `1px solid ${card.badgeColor}40`,
                padding: '0.15rem 0.45rem',
                borderRadius: '4px',
                letterSpacing: '0.05em'
              }}>
                {card.badge}
              </span>
            </div>
            <div className="metric-card-val" style={{ color: card.color }}>
              {card.value}{' '}
              {card.unit && <span style={{ fontSize: '0.85rem', color: '#94A3B8', fontWeight: 400 }}>{card.unit}</span>}
            </div>
          </div>
        );
      })}
    </div>
  );
}
