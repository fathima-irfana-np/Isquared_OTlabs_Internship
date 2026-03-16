import { useEffect, useRef } from 'react'

const PHASE_LABELS = {
  crawl: 'Step 1 — Crawling Website',
  process: 'Step 2 — Processing & Generating Tests',
  report: 'Step 3 — Building PDF Report',
}

const PHASE_ORDER = ['crawl', 'process', 'report']

export default function LiveProgress({ phase, pct, logs, error }) {
  const termRef = useRef(null)

  useEffect(() => {
    if (termRef.current) termRef.current.scrollTop = termRef.current.scrollHeight
  }, [logs])

  const label = PHASE_LABELS[phase] || 'Running…'
  const phaseIndex = PHASE_ORDER.indexOf(phase)

  return (
    <div className="progress-wrap">
      {/* Step indicators */}
      <div style={{ display: 'flex', gap: 8, marginBottom: 18 }}>
        {PHASE_ORDER.map((p, i) => {
          const done = i < phaseIndex
          const active = i === phaseIndex
          return (
            <div key={p} style={{
              flex: 1, padding: '8px 12px', borderRadius: 8,
              border: `1px solid ${active ? 'var(--blue-bright)' : done ? 'rgba(16,185,129,0.4)' : 'var(--border)'}`,
              background: active ? 'rgba(37,99,235,0.1)' : done ? 'rgba(16,185,129,0.08)' : 'var(--surface)',
              display: 'flex', alignItems: 'center', gap: 8,
            }}>
              <span style={{
                width: 20, height: 20, borderRadius: '50%', flexShrink: 0,
                display: 'flex', alignItems: 'center', justifyContent: 'center',
                fontSize: '.65rem', fontFamily: 'var(--mono)',
                background: active ? 'var(--blue)' : done ? 'var(--green)' : 'var(--surface-3)',
                color: '#fff',
              }}>
                {done ? '✓' : i + 1}
              </span>
              <span style={{
                fontSize: '.75rem', fontWeight: 600,
                color: active ? 'var(--text-h)' : done ? 'var(--green)' : 'var(--text-muted)',
              }}>
                {p === 'crawl' ? 'Crawl' : p === 'process' ? 'Process & Test' : 'Build Report'}
              </span>
              {active && <span className="spinner" style={{ marginLeft: 'auto' }} />}
            </div>
          )
        })}
      </div>

      {/* Current phase label + progress */}
      <div className="progress-header">
        <div className="progress-phase">
          {label}
        </div>
        <span className="progress-pct">{pct}%</span>
      </div>

      <div className="progress-bar-track">
        <div className="progress-bar-fill" style={{ width: `${pct}%` }} />
      </div>

      {/* Error */}
      {error && (
        <div className="err-card" style={{ marginBottom: 12 }}>
          <svg width="16" height="16" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
            <circle cx="12" cy="12" r="10" /><line x1="12" y1="8" x2="12" y2="12" /><line x1="12" y1="16" x2="12.01" y2="16" />
          </svg>
          <div>
            <div className="err-title">Pipeline Error</div>
            <div className="err-msg">{error}</div>
          </div>
        </div>
      )}

      {/* Live log terminal */}
      <div className="terminal" ref={termRef}>
        {logs.length === 0
          ? <span style={{ color: 'var(--text-dim)' }}>Waiting for output…</span>
          : logs.map((l, i) => (
            <div key={i} className={`t-line ${l.type}`}>{l.text}</div>
          ))
        }
      </div>
    </div>
  )
}