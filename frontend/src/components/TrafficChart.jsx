import React from 'react';
import {
  ResponsiveContainer,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  Tooltip,
  ReferenceLine,
  CartesianGrid
} from 'recharts';
import { Activity, AlertTriangle } from 'lucide-react';

export default function TrafficChart({ trafficHistory = [], isLoading, isLiveCaptureUnavailable, scapyError }) {
  if (isLiveCaptureUnavailable) {
    return (
      <div className="lumi-card lumi-card-alert" style={{ display: 'flex', flexDirection: 'column', gap: '1rem', minHeight: '340px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div>
            <h3 style={{ fontSize: '0.92rem', fontWeight: 600, color: 'var(--text-primary)', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <Activity size={17} color="var(--status-intrusion)" />
              LIVE PACKET ARRIVAL RATE
            </h3>
            <p style={{ fontSize: '0.74rem', color: 'var(--text-tertiary)', marginTop: '0.15rem' }}>
              Real-time aggregate network traffic arrival rate (packets/sec)
            </p>
          </div>
          <span className="lumi-badge lumi-badge-intrusion">CAPTURE UNAVAILABLE</span>
        </div>

        <div style={{
          height: 250,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          textAlign: 'center',
          gap: '0.65rem',
          background: 'rgba(244, 63, 94, 0.03)',
          borderRadius: 'var(--radius-lg)',
          border: '1px dashed var(--status-intrusion-border)',
          padding: '1.5rem'
        }}>
          <AlertTriangle size={24} color="var(--status-intrusion)" />
          <div style={{ fontWeight: 600, fontSize: '0.9rem', color: 'var(--status-intrusion)' }}>
            Live packet capture is unavailable. No live traffic is being analyzed.
          </div>
          <div style={{ fontSize: '0.78rem', color: 'var(--text-secondary)', maxWidth: '480px' }}>
            {scapyError || 'Please select a functional network capture adapter in Settings, or toggle to DEMO MODE to stream simulated traffic.'}
          </div>
        </div>
      </div>
    );
  }

  const data = Array.isArray(trafficHistory) && trafficHistory.length > 0 ? trafficHistory : [];
  const currentRate = data.length > 0 ? data[data.length - 1]?.total_packet_rate || 0 : 0;
  const isHigh = currentRate > 300;

  return (
    <div className="lumi-card" style={{ display: 'flex', flexDirection: 'column', gap: '1rem', minHeight: '340px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '0.75rem' }}>
        <div>
          <h3 style={{ fontSize: '0.92rem', fontWeight: 600, color: 'var(--text-primary)', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <Activity size={17} color="var(--accent-primary)" />
            LIVE PACKET ARRIVAL RATE STREAM
          </h3>
          <p style={{ fontSize: '0.74rem', color: 'var(--text-tertiary)', marginTop: '0.15rem' }}>
            Aggregated packet inter-arrival frequencies analyzed across rolling observation windows
          </p>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
          <div style={{ textAlign: 'right' }}>
            <span style={{ fontSize: '0.72rem', color: 'var(--text-tertiary)', display: 'block' }}>Current Window</span>
            <span style={{
              fontSize: '1.25rem',
              fontWeight: 700,
              fontFamily: 'var(--font-mono)',
              color: isHigh ? 'var(--status-intrusion)' : 'var(--accent-primary)'
            }}>
              {currentRate} <span style={{ fontSize: '0.75rem', fontWeight: 400, color: 'var(--text-secondary)' }}>pkt/s</span>
            </span>
          </div>
          <span className={`lumi-badge ${isHigh ? 'badge-pulse-red' : 'badge-pulse-green'}`}>
            <span className="pulse-dot" />
            {isHigh ? 'THRESHOLD EXCEEDED' : 'NOMINAL RATE'}
          </span>
        </div>
      </div>

      {isLoading && data.length === 0 ? (
        <div style={{ height: 250, display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--text-tertiary)', fontSize: '0.84rem' }}>
          Initializing telemetry stream...
        </div>
      ) : data.length === 0 ? (
        <div style={{ height: 250, display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--text-tertiary)', fontSize: '0.84rem' }}>
          Awaiting network packets...
        </div>
      ) : (
        <div style={{ width: '100%', height: 260 }}>
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={data} margin={{ top: 12, right: 12, left: -20, bottom: 0 }}>
              <defs>
                <linearGradient id="lumiRateGradient" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="var(--accent-primary)" stopOpacity={0.28} />
                  <stop offset="95%" stopColor="var(--accent-primary)" stopOpacity={0.0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="var(--border-subtle)" vertical={false} />
              <XAxis
                dataKey="timestamp"
                stroke="var(--text-tertiary)"
                fontSize={11}
                tickLine={false}
                axisLine={{ stroke: 'var(--border-default)' }}
              />
              <YAxis
                stroke="var(--text-tertiary)"
                fontSize={11}
                tickLine={false}
                axisLine={{ stroke: 'var(--border-default)' }}
                unit=" pkt/s"
              />
              <Tooltip
                contentStyle={{
                  background: 'var(--bg-surface)',
                  border: '1px solid var(--border-default)',
                  borderRadius: 'var(--radius-md)',
                  fontSize: '12px',
                  color: 'var(--text-primary)',
                  boxShadow: 'var(--shadow-elevated)',
                  fontFamily: 'var(--font-mono)'
                }}
                itemStyle={{ color: 'var(--accent-primary)' }}
                formatter={(val) => [`${val} pkt/s`, 'Arrival Rate']}
              />
              <ReferenceLine
                y={300}
                stroke="var(--status-intrusion)"
                strokeDasharray="4 4"
                label={{
                  value: 'Intrusion Threshold (300 pkt/s)',
                  fill: 'var(--status-intrusion)',
                  fontSize: 11,
                  position: 'top'
                }}
              />
              <Area
                type="monotone"
                dataKey="total_packet_rate"
                stroke="var(--accent-primary)"
                strokeWidth={2}
                fillOpacity={1}
                fill="url(#lumiRateGradient)"
                isAnimationActive={false}
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      )}
    </div>
  );
}
