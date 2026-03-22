import { useState } from 'react'

const COLOURS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#06b6d4', '#f97316']
let colourIdx = {}
function catColour(cat) {
  if (!colourIdx[cat]) colourIdx[cat] = COLOURS[Object.keys(colourIdx).length % COLOURS.length]
  return colourIdx[cat]
}

export default function TestsTable({ tests }) {
  const [search, setSearch] = useState('')
  const [catFilter, setCat] = useState('All')
  const [statusFilter, setStatus] = useState('All')
  const [expanded, setExp] = useState(null)

  const cats = ['All', ...new Set(tests.map(t => t.category || 'Uncategorised').filter(Boolean))]
  const hasExec = tests.some(t => t.execStatus)

  const visible = tests.filter(t => {
    const txt = (t.goal || t.description || '').toLowerCase()
    const id = (t.id || '').toLowerCase()
    const cat = t.category || 'Uncategorised'
    const matchSearch = !search || txt.includes(search.toLowerCase()) || id.includes(search.toLowerCase())
    const matchCat = catFilter === 'All' || cat === catFilter
    const matchStatus = statusFilter === 'All' || t.execStatus === statusFilter.toLowerCase()
    return matchSearch && matchCat && matchStatus
  })

  return (
    <div>
      {/* Filters */}
      <div style={{ display: 'flex', gap: 10, marginBottom: 16, flexWrap: 'wrap' }}>
        <div className="finput-wrap" style={{ flex: 1, minWidth: 200 }}>
          <span className="finput-icon">
            <svg width="12" height="12" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
              <circle cx="11" cy="11" r="8" /><line x1="21" y1="21" x2="16.65" y2="16.65" />
            </svg>
          </span>
          <input
            className="finput" placeholder="Search tests…"
            value={search} onChange={e => setSearch(e.target.value)}
            style={{ fontSize: '.78rem' }}
          />
        </div>

        {/* Status filter — only show if gauge was run */}
        {hasExec && (
          <div style={{ display: 'flex', gap: 6 }}>
            {['All', 'Passed', 'Failed'].map(s => (
              <button key={s} onClick={() => setStatus(s)} style={{
                padding: '5px 14px', borderRadius: 6, fontSize: '.72rem', fontWeight: 600,
                border: `1px solid ${statusFilter === s
                  ? s === 'Passed' ? 'var(--green)' : s === 'Failed' ? '#ef4444' : 'var(--blue)'
                  : 'var(--border)'}`,
                background: statusFilter === s
                  ? s === 'Passed' ? 'rgba(16,185,129,0.15)' : s === 'Failed' ? 'rgba(239,68,68,0.15)' : 'rgba(37,99,235,0.15)'
                  : 'var(--surface)',
                color: statusFilter === s
                  ? s === 'Passed' ? 'var(--green)' : s === 'Failed' ? '#ef4444' : 'var(--blue-bright)'
                  : 'var(--text-muted)',
                cursor: 'pointer',
              }}>{s}</button>
            ))}
          </div>
        )}
      </div>

      {/* Category pills */}
      <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap', marginBottom: 16 }}>
        {cats.map(c => (
          <button key={c} onClick={() => setCat(c)} style={{
            padding: '3px 12px', borderRadius: 99, fontSize: '.7rem', fontWeight: 600,
            border: `1px solid ${catFilter === c ? catColour(c) : 'var(--border)'}`,
            background: catFilter === c ? catColour(c) + '22' : 'transparent',
            color: catFilter === c ? catColour(c) : 'var(--text-muted)',
            cursor: 'pointer',
          }}>{c}</button>
        ))}
      </div>

      {/* Test cards */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
        {visible.length === 0 && (
          <div style={{ color: 'var(--text-muted)', fontSize: '.8rem', padding: '20px 0', textAlign: 'center' }}>
            No tests match your filters.
          </div>
        )}
        {visible.map(t => {
          const open = expanded === t.id
          const isFailed = t.execStatus === 'failed'
          const isPassed = t.execStatus === 'passed'
          const color = catColour(t.category || 'Uncategorised')

          return (
            <div key={t.id} style={{
              border: `1px solid ${isFailed ? 'rgba(239,68,68,0.35)' : isPassed ? 'rgba(16,185,129,0.25)' : 'var(--border)'}`,
              borderRadius: 8,
              background: isFailed ? 'rgba(239,68,68,0.05)' : isPassed ? 'rgba(16,185,129,0.04)' : 'var(--surface)',
              overflow: 'hidden',
            }}>
              {/* Card header */}
              <div
                onClick={() => setExp(open ? null : t.id)}
                style={{ padding: '10px 14px', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: 10 }}
              >
                {/* Exec status badge */}
                {t.execStatus && (
                  <span style={{
                    padding: '2px 8px', borderRadius: 4, fontSize: '.62rem', fontWeight: 700,
                    flexShrink: 0,
                    background: isFailed ? 'rgba(239,68,68,0.2)' : 'rgba(16,185,129,0.2)',
                    color: isFailed ? '#ef4444' : 'var(--green)',
                    border: `1px solid ${isFailed ? 'rgba(239,68,68,0.4)' : 'rgba(16,185,129,0.4)'}`,
                  }}>
                    {isFailed ? '✗ FAIL' : '✓ PASS'}
                  </span>
                )}

                <span style={{ fontFamily: 'var(--mono)', fontSize: '.7rem', color: 'var(--text-dim)', flexShrink: 0 }}>
                  {t.id}
                </span>
                <span style={{
                  fontSize: '.82rem', fontWeight: 600,
                  color: isFailed ? '#ef4444' : isPassed ? 'var(--green)' : 'var(--text-h)',
                  flex: 1,
                }}>
                  {t.goal}
                </span>
                <span style={{
                  padding: '2px 9px', borderRadius: 99, fontSize: '.65rem', fontWeight: 600,
                  background: color + '18', color, border: `1px solid ${color}44`, flexShrink: 0,
                }}>
                  {t.category}
                </span>
                <svg width="12" height="12" fill="none" stroke="currentColor" strokeWidth="2"
                  viewBox="0 0 24 24" style={{
                    flexShrink: 0, color: 'var(--text-dim)',
                    transform: open ? 'rotate(180deg)' : 'none', transition: 'transform .2s'
                  }}>
                  <polyline points="6 9 12 15 18 9" />
                </svg>
              </div>

              {/* Expanded content */}
              {open && (
                <div style={{
                  padding: '0 14px 14px',
                  borderTop: `1px solid ${isFailed ? 'rgba(239,68,68,0.2)' : 'var(--border)'}`,
                }}>
                  <div style={{ marginTop: 10 }}>
                    <div style={{ fontSize: '.68rem', color: 'var(--text-dim)', fontFamily: 'var(--mono)', marginBottom: 6 }}>
                      STEPS
                    </div>
                    {(t.steps || []).map((s, i) => (
                      <div key={i} style={{ display: 'flex', gap: 10, marginBottom: 4 }}>
                        <span style={{ fontFamily: 'var(--mono)', fontSize: '.68rem', color: 'var(--blue-bright)', flexShrink: 0 }}>
                          {String(i + 1).padStart(2, '0')}
                        </span>
                        <span style={{ fontSize: '.78rem', color: 'var(--text-body)' }}>{s}</span>
                      </div>
                    ))}
                  </div>
                  <div style={{
                    marginTop: 10, padding: '8px 12px', borderRadius: 6,
                    background: isFailed ? 'rgba(239,68,68,0.08)' : 'rgba(255,255,255,0.03)',
                    border: `1px solid ${isFailed ? 'rgba(239,68,68,0.2)' : 'var(--border)'}`,
                  }}>
                    <span style={{ fontSize: '.68rem', color: 'var(--text-dim)', fontFamily: 'var(--mono)' }}>
                      EXPECTED
                    </span>
                    <div style={{ fontSize: '.78rem', color: isFailed ? '#ef4444' : 'var(--text-body)', marginTop: 3 }}>
                      {t.expected}
                    </div>
                    {isFailed && (
                      <div style={{ fontSize: '.72rem', color: '#ef4444', marginTop: 6, fontWeight: 600 }}>
                        !! Application did not meet expected behavior - potential bug detected
                      </div>
                    )}
                  </div>
                </div>
              )}
            </div>
          )
        })}
      </div>
    </div>
  )
}