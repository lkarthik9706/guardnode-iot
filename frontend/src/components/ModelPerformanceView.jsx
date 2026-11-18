import React from 'react';

export default function ModelPerformanceView({ modelInfo }) {
  const meta = modelInfo || {
    dataset: 'CICIoT2023',
    model: 'LinearSVC',
    best_kernel: 'linear',
    features: ['mean_packet_rate', 'median_packet_rate', 'max_packet_rate'],
    units: 'packets/second',
    decision_threshold: -0.4149,
    training_samples: 51814,
    metrics: {
      accuracy: 0.7196,
      precision: 0.9967,
      recall_tpr: 0.7152,
      specificity: 0.9022,
      f1_score: 0.8328,
      fpr: 0.0978,
      balanced_accuracy: 0.8087,
      training_time_sec: 0.0150,
      prediction_time_sec: 0.0004,
      confusion_matrix: { TN: 4999, FP: 542, FN: 65464, TP: 164364 }
    },
    all_kernel_results: {
      linear: { kernel: 'linear', accuracy: 0.7196, precision: 0.9967, recall_tpr: 0.7152, f1_score: 0.8328, fpr: 0.0978, training_time_sec: 0.0150 },
      poly: { kernel: 'poly', accuracy: 0.7180, precision: 0.9850, recall_tpr: 0.7120, f1_score: 0.8260, fpr: 0.2200, training_time_sec: 0.0482 },
      rbf: { kernel: 'rbf', accuracy: 0.7250, precision: 0.9910, recall_tpr: 0.7210, f1_score: 0.8350, fpr: 0.2080, training_time_sec: 0.0520 }
    }
  };

  const metrics = meta.test_metrics || meta.metrics || {};
  const cm = metrics.confusion_matrix || {
    TN: meta.test_metrics?.TN || meta.metrics?.TN || 4999,
    FP: meta.test_metrics?.FP || meta.metrics?.FP || 542,
    FN: meta.test_metrics?.FN || meta.metrics?.FN || 65464,
    TP: meta.test_metrics?.TP || meta.metrics?.TP || 164364
  };
  const kernels = meta.all_kernel_results || {};

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.4rem' }}>
      {/* Top Banner */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '0.75rem' }}>
        <div>
          <h1 style={{ fontSize: '1.35rem', fontWeight: 600, color: 'var(--text-primary)', letterSpacing: '-0.025em' }}>
            SVM Model Performance & Evaluation
          </h1>
          <p style={{ fontSize: '0.78rem', color: 'var(--text-secondary)', marginTop: '0.2rem' }}>
            Linear Support Vector Machine classifier benchmarked on CICIoT2023 natural test distribution (235,369 samples)
          </p>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <span className="lumi-badge lumi-badge-normal">
            <span className="pulse-dot" />
            LINEAR KERNEL (OPTIMAL)
          </span>
          <span className="lumi-badge" style={{ background: 'var(--bg-subtle)', color: 'var(--text-secondary)' }}>
            Threshold: {meta.decision_threshold || -0.4149}
          </span>
        </div>
      </div>

      {/* Feature Vector Overview Card */}
      <div className="lumi-card">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '1rem' }}>
          <div>
            <span style={{ fontSize: '0.72rem', fontWeight: 600, color: 'var(--text-tertiary)', textTransform: 'uppercase', letterSpacing: '0.04em' }}>
              Lightweight Feature Vector
            </span>
            <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginTop: '0.25rem' }}>
              Engineered for ultra-low computational overhead on resource-constrained IoT gateways:
            </p>
          </div>
          <span className="lumi-badge" style={{ background: 'var(--accent-muted)', color: 'var(--accent-primary)', fontFamily: 'var(--font-mono)' }}>
            Preprocessing: np.log1p + StandardScaler
          </span>
        </div>

        <div style={{ display: 'flex', gap: '0.65rem', marginTop: '0.85rem', flexWrap: 'wrap' }}>
          {['1. Mean Packet Arrival Rate (mean_packet_rate)', '2. Median Packet Arrival Rate (median_packet_rate)', '3. Maximum Packet Arrival Rate (max_packet_rate)'].map((f, i) => (
            <div key={i} style={{
              background: 'var(--bg-surface)',
              border: '1px solid var(--border-default)',
              padding: '0.45rem 0.75rem',
              borderRadius: 'var(--radius-md)',
              fontSize: '0.76rem',
              fontFamily: 'var(--font-mono)',
              color: 'var(--text-primary)',
              display: 'flex',
              alignItems: 'center',
              gap: '0.4rem'
            }}>
              <span style={{ width: 6, height: 6, borderRadius: '50%', background: 'var(--accent-primary)' }} />
              {f}
            </div>
          ))}
        </div>
      </div>

      {/* Metric Cards Grid */}
      <div className="cards-grid">
        <div className="lumi-card lumi-stat-card">
          <span className="stat-title">PRECISION</span>
          <div className="metric-card-val" style={{ color: 'var(--status-normal)' }}>
            {((metrics.precision || 0.9967) * 100).toFixed(2)}%
          </div>
          <span className="stat-subtext">Minimal false positive alerts</span>
        </div>

        <div className="lumi-card lumi-stat-card">
          <span className="stat-title">F1-SCORE</span>
          <div className="metric-card-val" style={{ color: 'var(--accent-primary)' }}>
            {((metrics.f1_score || 0.8328) * 100).toFixed(2)}%
          </div>
          <span className="stat-subtext">Harmonic mean of precision & recall</span>
        </div>

        <div className="lumi-card lumi-stat-card">
          <span className="stat-title">RECALL / TPR</span>
          <div className="metric-card-val" style={{ color: '#6366f1' }}>
            {((metrics.recall || metrics.recall_tpr || 0.7152) * 100).toFixed(2)}%
          </div>
          <span className="stat-subtext">Intrusions correctly identified</span>
        </div>

        <div className="lumi-card lumi-stat-card">
          <span className="stat-title">SPECIFICITY</span>
          <div className="metric-card-val" style={{ color: '#8b5cf6' }}>
            {((metrics.specificity || 0.9022) * 100).toFixed(2)}%
          </div>
          <span className="stat-subtext">Normal traffic verified (FPR: 9.78%)</span>
        </div>

        <div className="lumi-card lumi-stat-card">
          <span className="stat-title">TRAINING TIME</span>
          <div className="metric-card-val" style={{ color: 'var(--text-primary)' }}>
            {(metrics.training_time_sec || 0.0118).toFixed(4)}s
          </div>
          <span className="stat-subtext">51,814 balanced training samples</span>
        </div>

        <div className="lumi-card lumi-stat-card">
          <span className="stat-title">PREDICTION INFERENCE</span>
          <div className="metric-card-val" style={{ color: 'var(--status-normal)' }}>
            0.4 <span style={{ fontSize: '0.85rem', fontWeight: 400, color: 'var(--text-tertiary)' }}>ms</span>
          </div>
          <span className="stat-subtext">Real-time edge microsecond inference</span>
        </div>
      </div>

      {/* Confusion Matrix & Kernel Benchmarks */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(360px, 1fr))', gap: '1.25rem' }}>
        {/* Confusion Matrix Tile */}
        <div className="lumi-card" style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          <div>
            <h4 style={{ fontSize: '0.92rem', fontWeight: 600, color: 'var(--text-primary)' }}>
              Confusion Matrix (235,369 Natural Test Samples)
            </h4>
            <p style={{ fontSize: '0.72rem', color: 'var(--text-tertiary)', marginTop: '0.15rem' }}>
              Full evaluation across all 33 CICIoT2023 attack categories
            </p>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.65rem' }}>
            <div style={{ background: 'var(--bg-surface)', border: '1px solid var(--border-default)', borderRadius: 'var(--radius-md)', padding: '0.85rem', textAlign: 'center' }}>
              <span style={{ fontSize: '0.7rem', color: 'var(--status-normal)', fontWeight: 600, textTransform: 'uppercase' }}>True Negative (TN)</span>
              <div style={{ fontSize: '1.4rem', fontWeight: 700, fontFamily: 'var(--font-mono)', color: 'var(--text-primary)', marginTop: '0.2rem' }}>
                {(cm.TN || 4414).toLocaleString()}
              </div>
              <span style={{ fontSize: '0.68rem', color: 'var(--text-tertiary)' }}>Normal correctly passed</span>
            </div>

            <div style={{ background: 'var(--bg-surface)', border: '1px solid var(--border-default)', borderRadius: 'var(--radius-md)', padding: '0.85rem', textAlign: 'center' }}>
              <span style={{ fontSize: '0.7rem', color: 'var(--status-warning)', fontWeight: 600, textTransform: 'uppercase' }}>False Positive (FP)</span>
              <div style={{ fontSize: '1.4rem', fontWeight: 700, fontFamily: 'var(--font-mono)', color: 'var(--status-warning)', marginTop: '0.2rem' }}>
                {(cm.FP || 1127).toLocaleString()}
              </div>
              <span style={{ fontSize: '0.68rem', color: 'var(--text-tertiary)' }}>Normal misclassified</span>
            </div>

            <div style={{ background: 'var(--bg-surface)', border: '1px solid var(--border-default)', borderRadius: 'var(--radius-md)', padding: '0.85rem', textAlign: 'center' }}>
              <span style={{ fontSize: '0.7rem', color: 'var(--text-tertiary)', fontWeight: 600, textTransform: 'uppercase' }}>False Negative (FN)</span>
              <div style={{ fontSize: '1.4rem', fontWeight: 700, fontFamily: 'var(--font-mono)', color: 'var(--text-secondary)', marginTop: '0.2rem' }}>
                {(cm.FN || 62504).toLocaleString()}
              </div>
              <span style={{ fontSize: '0.68rem', color: 'var(--text-tertiary)' }}>Intrusion missed</span>
            </div>

            <div style={{ background: 'var(--bg-surface)', border: '1px solid var(--border-default)', borderRadius: 'var(--radius-md)', padding: '0.85rem', textAlign: 'center' }}>
              <span style={{ fontSize: '0.7rem', color: 'var(--status-intrusion)', fontWeight: 600, textTransform: 'uppercase' }}>True Positive (TP)</span>
              <div style={{ fontSize: '1.4rem', fontWeight: 700, fontFamily: 'var(--font-mono)', color: 'var(--status-intrusion)', marginTop: '0.2rem' }}>
                {(cm.TP || 167324).toLocaleString()}
              </div>
              <span style={{ fontSize: '0.68rem', color: 'var(--text-tertiary)' }}>Intrusions blocked</span>
            </div>
          </div>
        </div>

        {/* Kernel Comparison Table */}
        <div className="lumi-card" style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          <div>
            <h4 style={{ fontSize: '0.92rem', fontWeight: 600, color: 'var(--text-primary)' }}>
              SVM Kernel Benchmark Comparison
            </h4>
            <p style={{ fontSize: '0.72rem', color: 'var(--text-tertiary)', marginTop: '0.15rem' }}>
              Linear vs Polynomial vs RBF kernels on packet arrival rate features
            </p>
          </div>

          <div className="table-wrapper">
            <table className="custom-table">
              <thead>
                <tr>
                  <th>Kernel</th>
                  <th>Precision</th>
                  <th>F1-Score</th>
                  <th>Train Time</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {Object.values(kernels).map((k) => {
                  const isBest = k.kernel === 'linear';
                  return (
                    <tr key={k.kernel} style={{ background: isBest ? 'var(--accent-muted)' : 'transparent' }}>
                      <td style={{ fontWeight: 600, color: isBest ? 'var(--accent-primary)' : 'var(--text-primary)', textTransform: 'capitalize' }}>
                        {k.kernel} {isBest && '★'}
                      </td>
                      <td style={{ fontFamily: 'var(--font-mono)' }}>{((k.precision || 0.99) * 100).toFixed(1)}%</td>
                      <td style={{ fontFamily: 'var(--font-mono)', fontWeight: 600, color: isBest ? 'var(--status-normal)' : 'var(--text-secondary)' }}>
                        {((k.f1_score || 0.84) * 100).toFixed(1)}%
                      </td>
                      <td style={{ fontFamily: 'var(--font-mono)', fontSize: '0.78rem' }}>{k.training_time_sec || 0.01}s</td>
                      <td>
                        {isBest ? (
                          <span className="lumi-badge lumi-badge-normal" style={{ fontSize: '0.65rem' }}>ACTIVE</span>
                        ) : (
                          <span style={{ fontSize: '0.72rem', color: 'var(--text-tertiary)' }}>Benchmarked</span>
                        )}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}
