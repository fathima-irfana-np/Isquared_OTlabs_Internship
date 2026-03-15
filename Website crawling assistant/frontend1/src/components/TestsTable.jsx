import { useState } from 'react'

// Classify tests by goal/steps text
const CATEGORIES = [
  { name: 'Boundary Values', color: '#00cfff', bg: 'rgba(0,207,255,0.12)', patterns: ['boundar', 'edge', 'min', 'max', 'limit', 'overflow', '9999'] },
  { name: 'Input Torture', color: '#f59e0b', bg: 'rgba(245,158,11,0.12)', patterns: ['invalid', 'special', 'inject', 'torture', 'poison', 'negative', 'xss'] },
  { name: 'State Transitions', color: '#818cf8', bg: 'rgba(129,140,248,0.12)', patterns: ['state', 'persist', 'retain', 'abandon', 'recalcul', 'clear'] },
  { name: 'Navigation', color: '#22d3a0', bg: 'rgba(34,211,160,0.12)', patterns: ['navigat', 'cross', 'back', 'return', 'between', 'page'] },
  { name: 'Mode Switching', color: '#f43f5e', bg: 'rgba(244,63,94,0.12)', patterns: ['mode', 'toggle', 'tab', 'switch', 'flicker'] },
  { name: 'Error Recovery', color: '#60a5fa', bg: 'rgba(96,165,250,0.12)', patterns: ['error', 'recover', 'empty form', 'required', 'validat', 'submit empty'] },
]

function classify(test) {
  const t = (test.goal + ' ' + (test.steps || []).join(' ')).toLowerCase()
  return CATEGORIES.find(c => c.patterns.some(p => t.includes(p)))
    || { name: 'Exploratory', color: '#94a3b8', bg: 'rgba(148,163,184,0.12)' }
}

const TH = { padding: '10px 14px', textAlign: 'left', fontSize: '0.78rem', color: 'var(--text-m)', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.05em', borderBottom: '1px solid rgba(255,255,255,0.08)' }
const TD = { padding: '12px 14px', verticalAlign: 'top', fontSize: '0.87rem' }

export default function TestsTable({ tests }) {
  const [expanded, setExpanded] = useState(null)
  const [search, setSearch] = useState('')
  const [filter, setFilter] = useState('all')

  const categories = [...new Set(tests.map(t => classify(t).name))]
  const filtered = tests.filter(t => {
    const cat = classify(t)
    const matchCat = filter === 'all' || cat.name === filter
    const matchSearch = !search || t.goal.toLowerCase().includes(search.toLowerCase()) || t.id.toLowerCase().includes(search.toLowerCase())
    return matchCat && matchSearch
  })

  return (
    <div>
      {/* Controls */}
      <div style={{ display: 'flex', gap: 10, marginBottom: 16, flexWrap: 'wrap' }}>
        <input
          type="text" placeholder="Search by ID or goal…"
          value={search} onChange={e => setSearch(e.target.value)}
          className="input-field no-icon" style={{ flex: 1, minWidth: 200 }}
        />
        <select value={filter} onChange={e => setFilter(e.target.value)}
          className="input-field no-icon" style={{ width: 'auto' }}>
          <option value="all">All Categories</option>
          {categories.map(c => <option key={c} value={c}>{c}</option>)}
        </select>
        <span style={{ color: 'var(--text-m)', fontSize: '0.82rem', alignSelf: 'center' }}>
          {filtered.length} / {tests.length} tests
        </span>
      </div>

      {/* Table */}
      <div style={{ overflowX: 'auto' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead>
            <tr>
              <th style={TH}>ID</th>
              <th style={TH}>Goal</th>
              <th style={TH}>Category</th>
              <th style={TH}>Steps</th>
              <th style={TH}>Expand</th>
            </tr>
          </thead>
          <tbody>
            {filtered.map(test => {
              const cat = classify(test)
              const isOpen = expanded === test.id
              return (
                <>
                  <tr key={test.id} style={{ borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
                    <td style={TD}>
                      <code style={{ color: 'var(--cyan)', fontSize: '0.82rem' }}>{test.id}</code>
                    </td>
                    <td style={{ ...TD, maxWidth: 340 }}>{test.goal}</td>
                    <td style={TD}>
                      <span style={{ background: cat.bg, color: cat.color, borderRadius: 6, padding: '2px 8px', fontSize: '0.76rem', fontWeight: 600 }}>
                        {cat.name}
                      </span>
                    </td>
                    <td style={{ ...TD, color: 'var(--text-m)' }}>{(test.steps || []).length}</td>
                    <td style={TD}>
                      <button onClick={() => setExpanded(isOpen ? null : test.id)}
                        style={{ background: 'none', border: '1px solid rgba(255,255,255,0.12)', borderRadius: 6, color: 'var(--text-m)', padding: '3px 10px', cursor: 'pointer', fontSize: '0.78rem' }}>
                        {isOpen ? '▲ Hide' : '▼ Steps'}
                      </button>
                    </td>
                  </tr>
                  {isOpen && (
                    <tr key={test.id + '-exp'}>
                      <td colSpan={5} style={{ padding: '10px 14px 18px', background: 'rgba(0,0,0,0.25)' }}>
                        <div style={{ fontFamily: 'var(--font-mono)', fontSize: '0.82rem' }}>
                          {(test.steps || []).map((s, i) => (
                            <div key={i} style={{ padding: '5px 0', borderBottom: '1px solid rgba(255,255,255,0.04)', color: 'var(--text-h)' }}>
                              <span style={{ color: 'var(--cyan)', marginRight: 10 }}>{String(i + 1).padStart(2, '0')}.</span>{s}
                            </div>
                          ))}
                          <div style={{ marginTop: 10, color: '#22d3a0', fontStyle: 'italic', fontFamily: 'inherit' }}>
                            ✓ Expected: {test.expected}
                          </div>
                        </div>
                      </td>
                    </tr>
                  )}
                </>
              )
            })}
          </tbody>
        </table>
        {filtered.length === 0 && (
          <div style={{ textAlign: 'center', padding: 48, color: 'var(--text-m)' }}>No tests match your search.</div>
        )}
      </div>
    </div>
  )
}
