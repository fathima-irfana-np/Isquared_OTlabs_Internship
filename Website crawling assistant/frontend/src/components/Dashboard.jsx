import { useState } from 'react'
import Charts from './Charts'
import TestsTable from './TestsTable'

const API = 'http://localhost:8001'

const TABS = [
  { id: 'overview', label: 'Overview' },
  { id: 'tests', label: 'Test Cases' },
]

export default function Dashboard({ tests, meta, siteUrl, onReset }) {
  const [tab, setTab] = useState('overview')

  const handlePDF = async () => {
    try {
      const res = await fetch(`${API}/api/download`)
      if (!res.ok) { alert('PDF not ready — run the full pipeline first.'); return }
      const blob = await res.blob()
      const url = URL.createObjectURL(blob)
      const a = Object.assign(document.createElement('a'), { href: url, download: 'test_report.pdf' })
      a.click(); URL.revokeObjectURL(url)
    } catch { alert('Cannot connect to backend.') }
  }

  const total = meta.total_validated || tests.length
  const rejected = meta.total_rejected || 0
  const pages = meta.pages_crawled || 0
  const elements = meta.elements_found || 0
  const rate = meta.validation_rate || (total + rejected > 0 ? Math.round(total / (total + rejected) * 100) : 0)

  const displayUrl = (siteUrl || meta.target_url || '').replace(/^https?:\/\//, '')

  return (
    <div className="dash">
      <div className="dash-header">
        <div>
          <div className="dash-title">Test Report</div>
          <div className="dash-sub">
            {displayUrl && <span className="dash-url">{displayUrl}</span>}
            {displayUrl && ' · '}
            <span>{new Date().toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' })}</span>
          </div>
        </div>
        <div className="dash-actions">
          <button className="btn-dl" onClick={handlePDF}>
            <svg width="14" height="14" fill="none" stroke="currentColor" strokeWidth="2.5" viewBox="0 0 24 24">
              <path d="M12 15V3M6 9l6 6 6-6" /><path d="M3 18h18v3H3z" />
            </svg>
            Download PDF
          </button>
          <button className="btn-sec" onClick={onReset}>
            <svg width="13" height="13" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
              <path d="M1 4v6h6M23 20v-6h-6" /><path d="M20.49 9A9 9 0 0 0 5.64 5.64L1 10m22 4-4.64 4.36A9 9 0 0 1 3.51 15" />
            </svg>
            New Run
          </button>
        </div>
      </div>

      {/* KPIs */}
      <div className="kpi-grid">
        <div className="kpi">
          <div className="kpi-val blue">{pages}</div>
          <div className="kpi-lbl">Pages Crawled</div>
        </div>
        <div className="kpi">
          <div className="kpi-val blue">{elements}</div>
          <div className="kpi-lbl">Elements Found</div>
        </div>
        <div className="kpi">
          <div className="kpi-val">{total + rejected}</div>
          <div className="kpi-lbl">Tests Generated</div>
        </div>
        <div className="kpi">
          <div className="kpi-val green">{total}</div>
          <div className="kpi-lbl">Validated</div>
        </div>
        <div className="kpi">
          <div className={`kpi-val ${rejected > 0 ? 'red' : ''}`}>{rejected}</div>
          <div className="kpi-lbl">Rejected</div>
        </div>
      </div>

      {/* Tabs */}
      <div className="tabs">
        {TABS.map(t => (
          <button key={t.id} className={`tab ${tab === t.id ? 'active' : ''}`} onClick={() => setTab(t.id)}>
            {t.label}
            {t.id === 'tests' && <span className="tab-cnt">{total}</span>}
          </button>
        ))}
      </div>

      {tab === 'overview' && <Charts tests={tests} meta={meta} />}
      {tab === 'tests' && <TestsTable tests={tests} />}
    </div>
  )
}
