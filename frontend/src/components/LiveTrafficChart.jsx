import React from 'react';
import { ResponsiveContainer, AreaChart, Area, XAxis, YAxis, Tooltip, ReferenceLine, CartesianGrid } from 'recharts';
import { Activity } from 'lucide-react';

export default function LiveTrafficChart({ trafficHistory }) {
  // Ensure we have data format
  const data = trafficHistory.length > 0
    ? trafficHistory
    : [
        { timestamp: '10:00:00', total_packet_rate: 45, average_packet_rate: 22 },
        { timestamp: '10:00:02', total_packet_rate: 60, average_packet_rate: 30 },
        { timestamp: '10:00:04', total_packet_rate: 850, average_packet_rate: 425 },
        { timestamp: '10:00:06', total_packet_rate: 120, average_packet_rate: 60 }
      ];

  const currentRate = data[data.length - 1]?.total_packet_rate || 0;

  return (
    <div className="cyber-card" style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h3 style={{ fontSize: '1rem', fontWeight: 600, color: '#F8FAFC', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <Activity size={18} color="#00F0FF" />
            LIVE PACKET ARRIVAL RATE
          </h3>
          <p style={{ fontSize: '0.75rem', color: '#94A3B8' }}>
            Real-time aggregate network traffic arrival rate (packets/sec)
          </p>
        </div>
        <div style={{ textAlign: 'right' }}>
          <span style={{ fontSize: '0.75rem', color: '#94A3B8' }}>Current Rate: </span>
          <span style={{ fontSize: '1.2rem', fontWeight: 700, fontFamily: 'monospace', color: currentRate > 300 ? '#FF2A6D' : '#00F0FF' }}>
            {currentRate} pkt/s
          </span>
        </div>
      </div>

      <div style={{ width: '100%', height: 260 }}>
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={data} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
            <defs>
              <linearGradient id="rateGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#00F0FF" stopOpacity={0.4} />
                <stop offset="95%" stopColor="#00F0FF" stopOpacity={0.0} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#1E293B" />
            <XAxis dataKey="timestamp" stroke="#64748B" fontSize={11} tickLine={false} />
            <YAxis stroke="#64748B" fontSize={11} tickLine={false} unit=" pkt/s" />
            <Tooltip
              contentStyle={{ background: '#0F172A', borderColor: '#334155', borderRadius: '8px', fontSize: '12px', color: '#FFF' }}
              itemStyle={{ color: '#00F0FF' }}
            />
            <ReferenceLine y={300} label={{ value: 'Intrusion Threshold (300 pkt/s)', fill: '#FF2A6D', fontSize: 11 }} stroke="#FF2A6D" strokeDasharray="3 3" />
            <Area type="monotone" dataKey="total_packet_rate" stroke="#00F0FF" strokeWidth={2} fillOpacity={1} fill="url(#rateGradient)" />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
