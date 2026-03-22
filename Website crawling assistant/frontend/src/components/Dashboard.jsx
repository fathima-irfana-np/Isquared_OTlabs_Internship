import { useState, useEffect } from 'react'
import Charts from './Charts'
import TestsTable from './TestsTable'

const API = 'http://localhost:8001'

export default function Dashboard({ tests, meta, siteUrl, onReset }) {
  const [tab, setTab]          = useState('overview')
  const [dlMsg, setDlMsg]      = useState('')
  const [execResults, setExec] = useState({})
  const [execSummary, setSum]  = useState({ passed: 0, failed: 0, total: 0 })

  useEffect(() => {
    fetch(`${API}/api/execution-results`)
      .then(r => r.ok ? r.json() : null)
      .then(data => {
        if (data && data.total > 0) {
          setExec(data.results)
          setSum({ passed: data.passed, failed: data.failed, total: data.total })
        }
      })
      .catch(() => {})
  }, [])

  const download = async () => {
    try {
      const r = await fetch(`${API}/api/download`)
      if (!r.ok) { setDlMsg('PDF not ready — run the full pipeline first.'); return }
      const blob = await r.blob()
      const url  = URL.createObjectURL(blob)
      const a    = document.createElement('a')
      a.href = url; a.download = 'test_report.pdf'; a.click()
      URL.revokeObjectURL(url)
      setDlMsg('')
    } catch { setDlMsg('Download failed.') }
  }

  const domain  = siteUrl?.replace(/^https?:\/\//, '').replace(/\/$/, '') || meta.target_url || ''
  const dateStr = new Date().toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' })

  const enrichedTests = tests.map(t => ({ ...t, execStatus: execResults[t.id] || null }))
  const hasExec = execSummary.total > 0

  const passedTests = enrichedTests.filter(t => t.execStatus === 'passed')
  const failedTests = enrichedTests.filter(t => t.execStatus === 'failed')

  return (
    <div style={{ animation: 'rise .4s ease both' }}>

      {/* ── Header ── */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 24 }}>
        <div>
          <h2 style={{ fontSize: '1.6rem', fontWeight: 800, color: 'var(--text-h)', margin: 0 }}>Test Report</h2>
          <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginTop: 4 }}>
            <span style={{ fontFamily: 'var(--mono)', fontSize: '.75rem', color: 'var(--blue-bright)' }}>{domain}</span>
            <span style={{ color: 'var(--text-dim)' }}>·</span>
            <span style={{ fontSize: '.75rem', color: 'var(--text-muted)' }}>{dateStr}</span>
          </div>
        </div>
        <div style={{ display: 'flex', gap: 10, alignItems: 'center' }}>
          <button className="btn-run-all" style={{ padding: '9px 20px', fontSize: '.82rem' }} onClick={download}>
            <svg width="14" height="14" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24" style={{ marginRight: 6 }}>
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
              <polyline points="7 10 12 15 17 10"/>
              <line x1="12" y1="15" x2="12" y2="3"/>
            </svg>
            Download PDF
          </button>
          <button className="btn-sec" onClick={onReset}>
            <svg width="13" height="13" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24" style={{ marginRight: 5 }}>
              <polyline points="1 4 1 10 7 10"/>
              <path d="M3.51 15a9 9 0 1 0 .49-4.5"/>
            </svg>
            New Run
          </button>
        </div>
      </div>

      {dlMsg && <div style={{ color: '#ef4444', fontSize: '.78rem', marginBottom: 12 }}>{dlMsg}</div>}

      {/* ── KPI cards ── */}
      <div className="kpi-row" style={{ marginBottom: 20 }}>
        {[
          { label: 'Pages Crawled',   value: meta.pages_crawled   ?? 0 },
          { label: 'Elements Found',  value: meta.elements_found  ?? 0 },
          { label: 'Tests Generated', value: meta.total_generated ?? 0 },
          { label: 'Validated',       value: meta.total_validated ?? 0, green: true },
          { label: 'Rejected',        value: meta.total_rejected  ?? 0 },
        ].map(k => (
          <div className="kpi-card" key={k.label}>
            <div className="kpi-val" style={{ color: k.green ? 'var(--green)' : undefined }}>{k.value}</div>
            <div className="kpi-label">{k.label}</div>
          </div>
        ))}
      </div>

      {/* ── Execution result boxes ── */}
      {hasExec && (
        <div style={{ display: 'flex', gap: 12, marginBottom: 20 }}>
          <div style={{
            flex: 1, padding: '14px 20px', borderRadius: 10,
            background: 'rgba(16,185,129,0.1)', border: '1px solid rgba(16,185,129,0.3)',
            display: 'flex', alignItems: 'center', gap: 12,
          }}>
            <span style={{ fontSize: '1.8rem', fontWeight: 800, color: 'var(--green)' }}>{execSummary.passed}</span>
            <div>
              <div style={{ fontSize: '.8rem', fontWeight: 700, color: 'var(--green)' }}>PASSED</div>
              <div style={{ fontSize: '.7rem', color: 'var(--text-muted)' }}>Tests behaved correctly</div>
            </div>
          </div>
          <div style={{
            flex: 1, padding: '14px 20px', borderRadius: 10,
            background: 'rgba(239,68,68,0.1)', border: '1px solid rgba(239,68,68,0.3)',
            display: 'flex', alignItems: 'center', gap: 12,
          }}>
            <span style={{ fontSize: '1.8rem', fontWeight: 800, color: '#ef4444' }}>{execSummary.failed}</span>
            <div>
              <div style={{ fontSize: '.8rem', fontWeight: 700, color: '#ef4444' }}>FAILED</div>
              <div style={{ fontSize: '.7rem', color: 'var(--text-muted)' }}>Bugs found in application</div>
            </div>
          </div>
          <div style={{
            flex: 1, padding: '14px 20px', borderRadius: 10,
            background: 'var(--surface)', border: '1px solid var(--border)',
            display: 'flex', alignItems: 'center', gap: 12,
          }}>
            <span style={{ fontSize: '1.8rem', fontWeight: 800, color: 'var(--text-h)' }}>
              {Math.round((execSummary.passed / execSummary.total) * 100)}%
            </span>
            <div>
              <div style={{ fontSize: '.8rem', fontWeight: 700, color: 'var(--text-body)' }}>PASS RATE</div>
              <div style={{ fontSize: '.7rem', color: 'var(--text-muted)' }}>{execSummary.total} tests executed</div>
            </div>
          </div>
        </div>
      )}

      {/* ── Tabs ── */}
      <div className="tabs" style={{ marginBottom: 20 }}>
        {['overview', 'testcases'].map(t => (
          <button key={t} className={`tab-btn${tab === t ? ' active' : ''}`} onClick={() => setTab(t)}>
            {t === 'overview' ? 'Overview' : (
              <>Test Cases
                <span style={{ marginLeft: 6, fontSize: '.65rem', padding: '1px 7px', borderRadius: 99, background: 'var(--blue)', color: '#fff' }}>
                  {tests.length}
                </span>
              </>
            )}
          </button>
        ))}
      </div>

      {tab === 'overview' && <Charts tests={tests} meta={meta} execResults={execResults} execSummary={execSummary} />}
      {tab === 'testcases' && <TestsTable tests={enrichedTests} />}

      {/* ── Execution Results Breakdown ── */}
      {hasExec && (
        <div style={{ marginTop: 40 }}>
          {/* Divider */}
          <div style={{ height: 1, background: 'var(--border)', marginBottom: 32, opacity: .5 }} />

          <h3 style={{ fontSize: '1.1rem', fontWeight: 800, color: 'var(--text-h)', marginBottom: 6 }}>
            Execution Breakdown
          </h3>
          <p style={{ fontSize: '.8rem', color: 'var(--text-muted)', marginBottom: 24 }}>
            Full list of passed and failed test cases from the last <code style={{ fontFamily: 'var(--mono)', color: 'var(--blue-bright)' }}>gauge run specs/</code>
          </p>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 20 }}>

            {/* PASSED list */}
            <div style={{ border: '1px solid rgba(16,185,129,0.25)', borderRadius: 10, overflow: 'hidden' }}>
              <div style={{
                padding: '12px 16px',
                background: 'rgba(16,185,129,0.1)',
                borderBottom: '1px solid rgba(16,185,129,0.2)',
                display: 'flex', alignItems: 'center', gap: 10,
              }}>
                <span style={{ fontSize: '1rem', fontWeight: 800, color: 'var(--green)' }}>✓</span>
                <span style={{ fontWeight: 700, color: 'var(--green)', fontSize: '.88rem' }}>
                  Passed — {passedTests.length} tests
                </span>
              </div>
              <div style={{ maxHeight: 420, overflowY: 'auto' }}>
                {passedTests.map((t, i) => (
                  <div key={t.id} style={{
                    padding: '9px 16px',
                    borderBottom: i < passedTests.length - 1 ? '1px solid rgba(16,185,129,0.1)' : 'none',
                    display: 'flex', alignItems: 'flex-start', gap: 10,
                    background: i % 2 === 1 ? 'rgba(16,185,129,0.03)' : 'transparent',
                  }}>
                    <span style={{
                      fontFamily: 'var(--mono)', fontSize: '.65rem',
                      color: 'var(--green)', flexShrink: 0, marginTop: 2,
                    }}>{t.id}</span>
                    <span style={{ fontSize: '.76rem', color: 'var(--text-body)' }}>{t.goal}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* FAILED list */}
            <div style={{ border: '1px solid rgba(239,68,68,0.25)', borderRadius: 10, overflow: 'hidden' }}>
              <div style={{
                padding: '12px 16px',
                background: 'rgba(239,68,68,0.1)',
                borderBottom: '1px solid rgba(239,68,68,0.2)',
                display: 'flex', alignItems: 'center', gap: 10,
              }}>
                <span style={{ fontSize: '1rem', fontWeight: 800, color: '#ef4444' }}>✗</span>
                <span style={{ fontWeight: 700, color: '#ef4444', fontSize: '.88rem' }}>
                  Failed — {failedTests.length} bugs found
                </span>
              </div>
              <div style={{ maxHeight: 420, overflowY: 'auto' }}>
                {failedTests.map((t, i) => (
                  <div key={t.id} style={{
                    padding: '9px 16px',
                    borderBottom: i < failedTests.length - 1 ? '1px solid rgba(239,68,68,0.1)' : 'none',
                    display: 'flex', alignItems: 'flex-start', gap: 10,
                    background: i % 2 === 1 ? 'rgba(239,68,68,0.03)' : 'transparent',
                  }}>
                    <span style={{
                      fontFamily: 'var(--mono)', fontSize: '.65rem',
                      color: '#ef4444', flexShrink: 0, marginTop: 2,
                    }}>{t.id}</span>
                    <div>
                      <div style={{ fontSize: '.76rem', color: 'var(--text-body)' }}>{t.goal}</div>
                      <div style={{ fontSize: '.68rem', color: '#ef4444', marginTop: 2 }}>
                        Expected: {t.expected}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

          </div>
        </div>
      )}

    </div>
  )
}