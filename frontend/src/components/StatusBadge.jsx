import React from 'react';

export default function StatusBadge({ status }) {
  if (status === 'OBSERVING') {
    return (
      <span className="lumi-badge lumi-badge-info">
        <span className="pulse-dot" style={{ backgroundColor: 'var(--accent-primary)' }} />
        <span>OBSERVING</span>
      </span>
    );
  }

  const isIntrusion = status === 'INTRUSION' || status === 'ACTIVE_INTRUSION';

  return (
    <span className={`lumi-badge ${isIntrusion ? 'badge-pulse-red' : 'badge-pulse-green'}`}>
      <span className="pulse-dot" />
      <span>{isIntrusion ? 'INTRUSION FLAGGED' : 'NORMAL'}</span>
    </span>
  );
}
