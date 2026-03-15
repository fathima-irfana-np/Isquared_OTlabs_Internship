import { useEffect, useRef } from 'react'

export default function OrbProgress({ stages, currentStage, doneStages, progressPct, logs = [] }) {
  const radius = 108
  const circ = 2 * Math.PI * radius
  const offset = circ - (progressPct / 100) * circ

  const logsEndRef = useRef(null)

  useEffect(() => {
    if (logsEndRef.current) {
      logsEndRef.current.scrollIntoView({ behavior: 'smooth' })
    }
  }, [logs])

  const messages = [
    'Exploring your website…',
    'Reading page structure…',
    'Generating test scenarios…',
    'Checking test accuracy…',
    'Preparing test scripts…',
    'Building step logic…',
    'Creating your report…',
  ]

  const currentMsg = progressPct === 100
    ? 'Analysis complete!'
    : currentStage >= 0
      ? messages[currentStage] || 'Working…'
      : 'Starting…'

  return (
    <div style={{ display: 'flex', gap: 24, alignItems: 'stretch', minHeight: 460 }}>

      {/* LEFT: Orb */}
      <div className="card" style={{ flex: 1, minWidth: 320, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', padding: '32px 20px', background: 'rgba(255,255,255,0.02)' }}>
        <p className="orb-stage-label">Analysing your website</p>

        <div className="orb-scene" style={{ margin: '20px 0 40px' }}>
          <div className="orb-ring" />
          <div className="orb-ring-2" />

          <svg className="orb-svg" viewBox="0 0 260 260">
            <defs>
              <linearGradient id="orbGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stopColor="#1a56ff" />
                <stop offset="100%" stopColor="#00cfff" />
              </linearGradient>
            </defs>
            <circle className="orb-track" cx="130" cy="130" r={radius} />
            <circle
              className="orb-fill"
              cx="130" cy="130" r={radius}
              strokeDasharray={circ}
              strokeDashoffset={offset}
            />
          </svg>

          <div className="orb-core">
            <span className="orb-pct">{progressPct}%</span>
            <span className="orb-status-text">
              {progressPct === 100 ? 'Done' : 'Running'}
            </span>
          </div>
        </div>

        <p style={{
          fontSize: '0.95rem',
          color: 'var(--cyan)',
          marginBottom: 10,
          fontWeight: 600,
          textAlign: 'center',
        }}>
          {currentMsg}
        </p>
        <p style={{
          fontSize: '0.8rem',
          color: 'var(--text-m)',
          opacity: 0.65,
          textAlign: 'center',
          margin: 0,
        }}>
          This may take a few minutes. Please keep this tab open.
        </p>
      </div>

      {/* RIGHT: Live Terminal */}
      <div className="card" style={{ flex: 1.2, minWidth: 340, background: '#09090b', border: '1px solid rgba(255,255,255,0.08)', borderRadius: 16, display: 'flex', flexDirection: 'column', overflow: 'hidden', padding: 0 }}>
        <div style={{ padding: '12px 16px', borderBottom: '1px solid rgba(255,255,255,0.08)', display: 'flex', alignItems: 'center', gap: 8, background: '#121214' }}>
          <div style={{ width: 10, height: 10, borderRadius: '50%', background: '#f43f5e' }} />
          <div style={{ width: 10, height: 10, borderRadius: '50%', background: '#f59e0b' }} />
          <div style={{ width: 10, height: 10, borderRadius: '50%', background: '#22d3a0' }} />
          <span style={{ marginLeft: 12, fontSize: '0.75rem', color: 'var(--text-m)', fontFamily: 'var(--font-mono)', textTransform: 'uppercase', letterSpacing: 1 }}>Live Pipeline Log</span>
        </div>

        <div style={{ flex: 1, padding: '16px 20px', overflowY: 'auto', fontFamily: 'var(--font-mono)', fontSize: '0.78rem', color: '#a1a1aa', lineHeight: 1.6, display: 'flex', flexDirection: 'column', gap: 4, maxHeight: 400 }}>
          {logs.length === 0 ? (
            <div style={{ opacity: 0.5 }}>Waiting for pipeline to start...</div>
          ) : (
            logs.map((log, i) => {
              const cleanLog = log.replace(/\u001b\[0m/g, '').replace(/\u001b\[.*?m/g, '') // Strip basic ANSI
              return (
                <div key={i} style={{ wordBreak: 'break-word', paddingBottom: 2 }}>
                  <span style={{ color: '#00cfff', marginRight: 8, userSelect: 'none' }}>❯</span>
                  {cleanLog}
                </div>
              )
            })
          )}
          <div ref={logsEndRef} style={{ paddingBottom: 10 }} />
        </div>
      </div>
    </div>
  )
}
