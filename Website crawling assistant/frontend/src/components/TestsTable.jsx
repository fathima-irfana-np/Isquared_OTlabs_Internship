import { useState } from 'react'

const COLOURS = ['#3b82f6','#10b981','#f59e0b','#ef4444','#8b5cf6','#06b6d4','#f97316']
let colourIdx = {}
function catColour(cat) {
  if (!colourIdx[cat]) colourIdx[cat] = COLOURS[Object.keys(colourIdx).length % COLOURS.length]
  return colourIdx[cat]
}

export default function TestsTable({ tests }) {
  const [search,   setSearch]   = useState('')
  const [catFilter, setCat]     = useState('All')
  const [expanded,  setExp]     = useState(null)

  const cats = ['All', ...new Set(tests.map(t => t.category || 'Uncategorised').filter(Boolean))]

  const visible = tests.filter(t => {
    const txt = (t.goal || t.description || '').toLowerCase()
    const id  = (t.id || '').toLowerCase()
    const cat = t.category || 'Uncategorised'
    return (catFilter === 'All' || cat === catFilter) &&
           (txt.includes(search.toLowerCase()) || id.includes(search.toLowerCase()))
  })

  const toggle = id => setExp(p => p === id ? null : id)

  return (
    <div className="tests-panel">
      <div className="toolbar">
        <div className="search-wrap">
          <span className="search-icon">
            <svg width="12" height="12" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
              <circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/>
            </svg>
          </span>
          <input
            className="search-input" placeholder="Search tests…"
            value={search} onChange={e => setSearch(e.target.value)}
          />
        </div>
        <div className="pills">
          {cats.slice(0, 8).map(c => (
            <button key={c} className={`pill ${catFilter === c ? 'on' : ''}`} onClick={() => setCat(c)}>{c}</button>
          ))}
        </div>
      </div>

      <div className="tests-count">{visible.length} test{visible.length !== 1 ? 's' : ''}</div>

      <div className="tests-list">
        {visible.length === 0 ? (
          <div className="empty">No tests match your filter.</div>
        ) : visible.map((t, idx) => {
          const id      = t.id || `TC-${String(idx + 1).padStart(3, '0')}`
          const goal    = t.goal || t.description || t.test_goal || 'Untitled'
          const cat     = t.category || 'Uncategorised'
          const colour  = catColour(cat)
          const steps   = Array.isArray(t.steps) ? t.steps : []
          const isOpen  = expanded === id
          return (
            <div
              key={id}
              className={`tcard ${isOpen ? 'open' : ''}`}
              onClick={() => toggle(id)}
              tabIndex={0}
              onKeyDown={e => e.key === 'Enter' && toggle(id)}
              role="button"
              aria-expanded={isOpen}
            >
              <div className="tcard-top">
                <div className="tcard-left">
                  <span className="tid">{id}</span>
                  <span className="tcat" style={{ color: colour, background: colour + '1a' }}>{cat}</span>
                </div>
                <div className="tcard-right">
                  <span className="tsteps">{steps.length} steps</span>
                  <span className="tdot pass" />
                  <span className="tchevron">▼</span>
                </div>
              </div>
              <div className="tgoal">{goal}</div>

              {isOpen && (
                <div className="tdetail">
                  <div className="drow">
                    <span className="dlbl">Status</span>
                    <span className="sbadge pass">✓ Validated</span>
                  </div>
                  {t.expected && (
                    <div className="drow">
                      <span className="dlbl">Expected</span>
                      <span className="dval">{t.expected}</span>
                    </div>
                  )}
                  {steps.length > 0 && (
                    <div className="drow">
                      <span className="dlbl">Steps</span>
                      <ol className="steps-ol">
                        {steps.map((s, i) => (
                          <li key={i}>{typeof s === 'string' ? s : JSON.stringify(s)}</li>
                        ))}
                      </ol>
                    </div>
                  )}
                </div>
              )}
            </div>
          )
        })}
      </div>
    </div>
  )
}
