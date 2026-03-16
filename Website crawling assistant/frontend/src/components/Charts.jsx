const COLOURS = [
  '#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#06b6d4', '#f97316'
]

function ValidationRing({ validated, rejected }) {
  const total = validated + rejected
  const rate = total > 0 ? Math.round((validated / total) * 100) : 0
  const r = 44
  const circ = 2 * Math.PI * r
  const fill = (rate / 100) * circ
  const full = rate === 100

  // Ring colour: red→amber→green based on rate
  const ringColor = rate >= 80 ? '#10b981' : rate >= 50 ? '#f59e0b' : '#ef4444'

  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 16 }}>
      <div style={{ position: 'relative', width: 160, height: 160 }}>
        <svg viewBox="0 0 110 110" width="160" height="160">
          {/* Background track */}
          <circle
            cx="55" cy="55" r={r}
            fill="none"
            stroke="rgba(255,255,255,0.06)"
            strokeWidth="10"
          />
          {/* Fill arc */}
          <circle
            cx="55" cy="55" r={r}
            fill="none"
            stroke={ringColor}
            strokeWidth="10"
            strokeDasharray={full ? `${circ} 0` : `${fill} ${circ}`}
            strokeDashoffset={circ * 0.25}
            strokeLinecap={full ? "butt" : "round"}
            style={{ transition: 'stroke-dasharray 1s ease, stroke 0.5s ease' }}
          />
          {/* Centre text */}
          <text
            x="55" y="49"
            textAnchor="middle"
            fill="#f1f5ff"
            fontSize="17"
            fontWeight="800"
            fontFamily="Outfit, sans-serif"
          >
            {rate}%
          </text>
          <text
            x="55" y="63"
            textAnchor="middle"
            fill="#4b5a7a"
            fontSize="7"
            fontFamily="JetBrains Mono, monospace"
          >
            VALIDATED
          </text>
        </svg>
      </div>

      {/* Legend */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: 8, width: '100%' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '.78rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 8, color: 'var(--text-body)' }}>
            <span style={{ width: 8, height: 8, borderRadius: '50%', background: '#10b981', flexShrink: 0, display: 'inline-block' }} />
            Validated
          </div>
          <span style={{ fontFamily: 'var(--mono)', fontSize: '.72rem', color: 'var(--text-muted)' }}>{validated}</span>
        </div>
        {rejected > 0 && (
          <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '.78rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 8, color: 'var(--text-body)' }}>
              <span style={{ width: 8, height: 8, borderRadius: '50%', background: '#ef4444', flexShrink: 0, display: 'inline-block' }} />
              Rejected
            </div>
            <span style={{ fontFamily: 'var(--mono)', fontSize: '.72rem', color: 'var(--text-muted)' }}>{rejected}</span>
          </div>
        )}
        <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '.78rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 8, color: 'var(--text-body)' }}>
            <span style={{ width: 8, height: 8, borderRadius: '50%', background: '#4b5a7a', flexShrink: 0, display: 'inline-block' }} />
            Total
          </div>
          <span style={{ fontFamily: 'var(--mono)', fontSize: '.72rem', color: 'var(--text-muted)' }}>{total}</span>
        </div>
      </div>
    </div>
  )
}

export default function Charts({ tests, meta }) {
  const catMap = {}
  tests.forEach(t => {
    const cat = t.category || 'Uncategorised'
    if (!catMap[cat]) catMap[cat] = { total: 0, color: COLOURS[Object.keys(catMap).length % COLOURS.length] }
    catMap[cat].total++
  })
  const cats = Object.entries(catMap).sort((a, b) => b[1].total - a[1].total)
  const maxCat = cats[0]?.[1].total || 1

  return (
    <div className="charts-grid" style={{ marginBottom: 22 }}>
      {/* Validation ring */}
      <div className="chart-card">
        <div className="chart-title">Validation Result</div>
        <ValidationRing
          validated={meta.total_validated || tests.length}
          rejected={meta.total_rejected || 0}
        />
      </div>

      {/* Category bars */}
      <div className="chart-card">
        <div className="chart-title">Test Categories</div>
        <div className="cat-list">
          {cats.slice(0, 8).map(([name, d]) => {
            const pct = Math.round((d.total / maxCat) * 100)
            return (
              <div className="cat-row" key={name}>
                <div className="cat-head">
                  <span className="cat-name-lbl" style={{ color: d.color }}>{name}</span>
                  <span className="cat-frac">{d.total} test{d.total !== 1 ? 's' : ''}</span>
                </div>
                <div className="cat-track">
                  <div className="cat-fill" style={{ width: `${pct}%`, background: d.color }} />
                </div>
              </div>
            )
          })}
          {cats.length === 0 && (
            <div style={{ fontSize: '.78rem', color: 'var(--text-muted)', fontFamily: 'var(--mono)' }}>
              No category data
            </div>
          )}
        </div>
      </div>
    </div>
  )
}