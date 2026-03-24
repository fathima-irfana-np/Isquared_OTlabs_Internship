import { useEffect, useRef } from 'react'

const PHASES = [
  { id: 'crawl', label: 'Crawl Site' },
  { id: 'process', label: 'Process & Test' },
  { id: 'execute', label: 'Run Tests' },
  { id: 'report', label: 'Build Report' },
]

export default function LiveProgress({ phase, pct, logs, error }) {
  const termRef = useRef(null)

  // Auto-scroll to bottom as new logs arrive
  useEffect(() => {
    if (termRef.current) {
      termRef.current.scrollTop = termRef.current.scrollHeight
    }
  }, [logs])

  const phaseIdx = PHASES.findIndex(p => p.id === phase)

  return (
    <div style={{ marginTop: 20, animation: 'rise .4s ease both' }}>

      {/* Step indicator */}
      <div style={{ display: 'flex', gap: 8, marginBottom: 16 }}>
        {PHASES.map((p, i) => {
          const done = i < phaseIdx
          const active = i === phaseIdx
          return (
            <div key={p.id} style={{
              flex: 1, padding: '10px 14px', borderRadius: 8,
              border: `1px solid ${active ? 'var(--blue-bright)' : done ? 'rgba(16,185,129,0.35)' : 'var(--border)'}`,
              background: active ? 'rgba(37,99,235,0.1)' : done ? 'rgba(16,185,129,0.07)' : 'var(--surface)',
              display: 'flex', alignItems: 'center', gap: 10,
              transition: 'all 0.4s ease',
            }}>
              <span style={{
                width: 22, height: 22, borderRadius: '50%', flexShrink: 0,
                display: 'flex', alignItems: 'center', justifyContent: 'center',
                fontSize: '.65rem', fontFamily: 'var(--mono)', fontWeight: 700,
                background: active ? 'var(--blue)' : done ? 'var(--green)' : 'var(--surface-3)',
                color: '#fff', transition: 'background 0.4s ease',
              }}>
                {done ? '✓' : i + 1}
              </span>
              <span style={{
                fontSize: '.8rem', fontWeight: 600,
                color: active ? 'var(--text-h)' : done ? 'var(--green)' : 'var(--text-muted)',
                transition: 'color 0.4s ease',
              }}>
                {p.label}
              </span>
              {active && <span className="spinner" style={{ marginLeft: 'auto' }} />}
              {done && (
                <span style={{ marginLeft: 'auto', fontSize: '.7rem', color: 'var(--green)', fontFamily: 'var(--mono)' }}>
                  done
                </span>
              )}
            </div>
          )
        })}
      </div>

      {/* Progress bar */}
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 6 }}>
        <span style={{ fontFamily: 'var(--mono)', fontSize: '.7rem', color: 'var(--text-muted)' }}>
          Overall Progress
        </span>
        <span style={{ fontFamily: 'var(--mono)', fontSize: '.7rem', color: 'var(--text-muted)' }}>
          {pct}%
        </span>
      </div>
      <div style={{ height: 4, background: 'rgba(255,255,255,0.06)', borderRadius: 2, overflow: 'hidden', marginBottom: 14 }}>
        <div style={{
          height: '100%',
          width: `${pct}%`,
          background: 'linear-gradient(90deg, var(--blue), var(--cyan))',
          borderRadius: 2,
          transition: 'width 0.6s ease',
        }} />
      </div>

      {/* Console log panel */}
      <div style={{
        background: '#030609',
        border: '1px solid var(--border)',
        borderRadius: 10,
        overflow: 'hidden',
      }}>
        {/* Console title bar */}
        <div style={{
          display: 'flex', alignItems: 'center', gap: 8,
          padding: '10px 16px',
          borderBottom: '1px solid var(--border)',
          background: 'rgba(255,255,255,0.02)',
        }}>
          <span style={{ width: 10, height: 10, borderRadius: '50%', background: '#ef4444', display: 'inline-block' }} />
          <span style={{ width: 10, height: 10, borderRadius: '50%', background: '#f59e0b', display: 'inline-block' }} />
          <span style={{ width: 10, height: 10, borderRadius: '50%', background: '#10b981', display: 'inline-block' }} />
          <span style={{ marginLeft: 8, fontFamily: 'var(--mono)', fontSize: '.68rem', color: 'var(--text-muted)' }}>
            pipeline — live output
          </span>
          {logs.length > 0 && (
            <span style={{ marginLeft: 'auto', fontFamily: 'var(--mono)', fontSize: '.65rem', color: 'var(--text-dim)' }}>
              {logs.filter(l => l.type !== 'sep').length} lines
            </span>
          )}
        </div>

        {/* Log lines */}
        <div
          ref={termRef}
          style={{
            padding: '12px 16px',
            height: 340,
            overflowY: 'auto',
            fontFamily: 'var(--mono)',
            fontSize: '.72rem',
            lineHeight: 1.7,
            color: '#6b7fa8',
          }}
        >
          {logs.length === 0 ? (
            <span style={{ color: 'var(--text-dim)' }}>
              {'>'} Waiting for pipeline to start…
            </span>
          ) : (
            logs.map((l, i) => {
              if (l.type === 'sep') {
                return (
                  <div key={i} style={{
                    color: '#3b82f6',
                    borderTop: '1px solid rgba(59,130,246,0.15)',
                    marginTop: 10, marginBottom: 6,
                    paddingTop: 8,
                    fontSize: '.7rem',
                    letterSpacing: '.06em',
                  }}>
                    {l.text}
                  </div>
                )
              }
              if (!l.text) return <div key={i} style={{ height: 6 }} />
              return (
                <div key={i} style={{
                  color: l.type === 'ok' ? '#10b981'
                    : l.type === 'err' ? '#ef4444'
                      : '#8b9fc8',
                  wordBreak: 'break-all',
                }}>
                  <span style={{ color: 'var(--text-dim)', userSelect: 'none' }}>{'> '}</span>
                  {l.text}
                </div>
              )
            })
          )}
          {/* Blinking cursor */}
          <span style={{
            display: 'inline-block', width: 7, height: 13,
            background: 'var(--blue-bright)', marginLeft: 4,
            animation: 'blink 1.1s step-end infinite',
            verticalAlign: 'middle',
          }} />
        </div>
      </div>

      <style>{`
        @keyframes blink { 0%,100%{opacity:1} 50%{opacity:0} }
      `}</style>
    </div>
  )
}