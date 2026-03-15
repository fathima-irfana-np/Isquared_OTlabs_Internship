const BATCH_FOCUSES = [
  { batch: '1', name: 'Input Torture & Field Poisoning', desc: 'Edge-case values, special chars, empty required fields.' },
  { batch: '2', name: 'State Transitions & Form Abandonment', desc: 'Partial fills, navigate-away-return, state persistence.' },
  { batch: '3', name: 'Boundary Value Analysis', desc: 'Exact min, max, zero, +1/-1 boundaries on numeric inputs.' },
  { batch: '4', name: 'Multi-Step Navigation Chaos', desc: 'Fill on page A, jump to B, return to A — state survival?' },
  { batch: '5', name: 'Mode Switching & UI State Dances', desc: 'Toggle modes mid-fill, switch tabs, check value retention.' },
  { batch: '6', name: 'Error Recovery & Validation Resilience', desc: 'Submit empty, fix one field, resubmit; clear after success.' },
]

export default function ReportSummary({ tests, meta = {}, siteUrl }) {
  const total = meta.total_generated || tests.length
  const valid = meta.total_validated || tests.length
  const rejected = meta.total_rejected || 0
  const pages = meta.pages_crawled || '—'
  const passRate = meta.validation_pass_rate || (total > 0 ? 100 : 0)

  const Row = ({ label, value, accent }) => (
    <div style={{ display: 'flex', justifyContent: 'space-between', padding: '9px 0', borderBottom: '1px solid rgba(255,255,255,0.06)', fontSize: '0.87rem' }}>
      <span style={{ color: 'var(--text-m)' }}>{label}</span>
      <span style={{ color: accent || 'var(--text-h)', fontWeight: 600 }}>{value}</span>
    </div>
  )

  return (
    <div style={{ display: 'flex', gap: 20, flexWrap: 'wrap' }}>

      {/* Pipeline Summary */}
      <div style={{ flex: 1, minWidth: 260, background: 'rgba(255,255,255,0.03)', borderRadius: 12, padding: '18px 20px', border: '1px solid rgba(255,255,255,0.07)' }}>
        <h3 style={{ margin: '0 0 14px', fontSize: '0.9rem', color: 'var(--text-h)', fontWeight: 700 }}>Pipeline Results</h3>
        <Row label="Target Site" value={siteUrl || '—'} />
        <Row label="Pages Crawled" value={pages} />
        <Row label="Tests Generated (raw)" value={total} />
        <Row label="Tests Validated" value={valid} accent="#22d3a0" />
        <Row label="Tests Rejected" value={rejected} accent={rejected > 0 ? '#f43f5e' : undefined} />
        <Row label="Validation Pass Rate" value={`${passRate}%`} accent="#00cfff" />
        <div style={{ marginTop: 14, padding: '10px 14px', borderRadius: 8, background: 'rgba(0,207,255,0.07)', border: '1px solid rgba(0,207,255,0.15)', fontSize: '0.8rem', color: 'var(--text-m)' }}>
          ✓ All {valid} validated tests reference real UI elements from the crawl snapshot.
        </div>
      </div>

      {/* Batch Strategy */}
      <div style={{ flex: 2, minWidth: 300, background: 'rgba(255,255,255,0.03)', borderRadius: 12, padding: '18px 20px', border: '1px solid rgba(255,255,255,0.07)' }}>
        <h3 style={{ margin: '0 0 14px', fontSize: '0.9rem', color: 'var(--text-h)', fontWeight: 700 }}>Adversarial Batch Strategy</h3>
        {BATCH_FOCUSES.map(b => (
          <div key={b.batch} style={{ display: 'flex', gap: 12, marginBottom: 12 }}>
            <span style={{ background: 'rgba(0,207,255,0.12)', color: 'var(--cyan)', borderRadius: 6, padding: '2px 8px', fontSize: '0.78rem', fontWeight: 700, flexShrink: 0, alignSelf: 'flex-start' }}>
              B{b.batch}
            </span>
            <div>
              <div style={{ fontSize: '0.84rem', color: 'var(--text-h)', fontWeight: 600, marginBottom: 1 }}>{b.name}</div>
              <div style={{ fontSize: '0.78rem', color: 'var(--text-m)' }}>{b.desc}</div>
            </div>
          </div>
        ))}
      </div>

      {/* How to run */}
      <div style={{ width: '100%', background: 'rgba(255,255,255,0.03)', borderRadius: 12, padding: '18px 20px', border: '1px solid rgba(255,255,255,0.07)' }}>
        <h3 style={{ margin: '0 0 10px', fontSize: '0.9rem', color: 'var(--text-h)', fontWeight: 700 }}>Run Tests in Gauge</h3>
        <code style={{ display: 'block', fontFamily: 'var(--font-mono)', fontSize: '0.85rem', color: 'var(--cyan)', background: 'rgba(0,0,0,0.3)', padding: '10px 14px', borderRadius: 8 }}>
          gauge run specs/
        </code>
        <p style={{ margin: '8px 0 0', fontSize: '0.8rem', color: 'var(--text-m)' }}>
          Tests launch a visible Chromium browser with 2s slow-motion so you can observe execution.
        </p>
      </div>
    </div>
  )
}
