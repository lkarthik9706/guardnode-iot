import React from 'react';
import { Info, X } from 'lucide-react';

export default function ToastNotification({ message, onClose }) {
  if (!message) return null;

  return (
    <div className="toast-notification">
      <div style={{
        width: 24,
        height: 24,
        borderRadius: 'var(--radius-pill)',
        background: 'var(--accent-muted)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        color: 'var(--accent-primary)',
        flexShrink: 0
      }}>
        <Info size={14} strokeWidth={2.4} />
      </div>
      <span style={{ fontSize: '0.82rem', fontWeight: 500, color: 'var(--text-primary)' }}>
        {message}
      </span>
      <button
        onClick={onClose}
        style={{
          background: 'transparent',
          border: 'none',
          color: 'var(--text-tertiary)',
          cursor: 'pointer',
          padding: '0.2rem',
          borderRadius: 'var(--radius-sm)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center'
        }}
      >
        <X size={14} />
      </button>
    </div>
  );
}
