import React from 'react';
import { Cpu, Activity, ShieldCheck } from 'lucide-react';

export default function StatusBar({ mode, isMonitoring, modelInfo }) {
  const bestKernel = modelInfo?.best_kernel ? modelInfo.best_kernel.toUpperCase() : 'LINEAR';

  return (
    <footer className="app-statusbar">
      <div style={{ display: 'flex', alignItems: 'center', gap: '1.5rem' }}>
        <span style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
          <span style={{ width: 8, height: 8, borderRadius: '50%', background: isMonitoring ? '#10B981' : '#FF2A6D' }}></span>
          STATUS: {isMonitoring ? `ACTIVE (${mode} MODE)` : 'PAUSED'}
        </span>

        <span style={{ color: '#334155' }}>|</span>

        <span style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', color: '#94A3B8' }}>
          <Cpu size={13} color="#00F0FF" />
          CPU: 2.4% | MEM: 48.2 MB
        </span>
      </div>

      <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
        <span style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', color: '#10B981' }}>
          <ShieldCheck size={14} />
          MODEL: SVM {bestKernel} (Mean, Median, Max Pkt Rates)
        </span>
      </div>
    </footer>
  );
}
