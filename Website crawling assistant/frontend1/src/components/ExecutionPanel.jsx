import { useState } from 'react'

export default function ExecutionPanel({ tests }) {
  const [selected, setSelected] = useState(tests[0]?.id || null)
  const test = tests.find(t => t.id === selected)

  return (
    <div style={{ display: 'flex', gap: 0, minHeight: 420 }}>

      {/* Left: test list */}
      <div style={{
        width: 240, flexShrink: 0, overflowY: 'auto', maxHeight: 520,
        borderRight: '1px solid rgba(255,255,255,0.07)', paddingRight: 12,
      }}>
        {tests.map(t => (
          <button key={t.id} onClick={() => setSelected(t.id)} style={{
            display: 'block', width: '100%', textAlign: 'left',
            padding: '9px 12px', marginBottom: 4, borderRadius: 8,
            border: 'none', cursor: 'pointer',
            background: selected === t.id ? 'rgba(0,207,255,0.12)' : 'transparent',
            color: selected === t.id ? 'var(--cyan)' : 'var(--text-m)',
          }}>
            <div style={{ fontFamily: 'var(--font-mono)', fontWeight: 600, fontSize: '0.82rem', marginBottom: 2 }}>{t.id}</div>
            <div style={{ fontSize: '0.74rem', opacity: 0.65, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>{t.goal}</div>
          </button>
        ))}
      </div>

      {/* Right: step detail */}
      {test ? (
        <div style={{ flex: 1, paddingLeft: 24 }}>
          <h3 style={{ margin: '0 0 4px', fontSize: '0.9rem', color: 'var(--text-h)' }}>{test.id}</h3>
          <p style={{ margin: '0 0 18px', fontSize: '0.84rem', color: 'var(--text-m)' }}>{test.goal}</p>

          {(test.steps || []).map((step, i) => (
            <div key={i} style={{
              display: 'flex', gap: 12, alignItems: 'flex-start',
              padding: '10px 0', borderBottom: '1px solid rgba(255,255,255,0.05)',
            }}>
              <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.78rem', color: 'var(--cyan)', minWidth: 28, paddingTop: 2, flexShrink: 0 }}>
                {String(i + 1).padStart(2, '0')}
              </span>
              <span style={{ fontSize: '0.87rem', color: 'var(--text-h)', lineHeight: 1.5 }}>{step}</span>
            </div>
          ))}

          {test.expected && (
            <div style={{
              marginTop: 18, padding: '10px 14px', borderRadius: 8,
              background: 'rgba(34,211,160,0.08)', border: '1px solid rgba(34,211,160,0.2)',
            }}>
              <span style={{ color: '#22d3a0', fontWeight: 600, fontSize: '0.82rem' }}>✓ Expected: </span>
              <span style={{ fontSize: '0.85rem', color: 'var(--text-m)' }}>{test.expected}</span>
            </div>
          )}

          <p style={{ marginTop: 20, fontSize: '0.76rem', color: 'var(--text-m)', opacity: 0.55 }}>
            Run in Gauge: <code style={{ fontFamily: 'var(--font-mono)' }}>gauge run specs/</code>
          </p>
        </div>
      ) : (
        <div style={{ flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--text-m)' }}>
          Select a test to view its steps
        </div>
      )}
    </div>
  )
}
