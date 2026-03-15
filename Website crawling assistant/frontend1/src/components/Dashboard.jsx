import { useState } from 'react'
import TestsTable from './TestsTable'
import ExecutionPanel from './ExecutionPanel'
import ReportSummary from './ReportSummary'

const TABS = [
  { id: 'tests', label: 'Test Cases', icon: '🧪' },
  { id: 'execution', label: 'Step Viewer', icon: '▶' },
  { id: 'report', label: 'Report', icon: '📄' },
]

export default function Dashboard({ tests, meta = {}, siteUrl, onReset }) {
  const [activeTab, setActiveTab] = useState('tests')

  const total = tests.length
  const rejected = meta.total_rejected || 0
  const pages = meta.pages_crawled || 0
  const passRate = meta.validation_pass_rate || (total > 0 ? 100 : 0)

  return (
    <div className="dashboard" id="dashboard">

      {/* Header */}
      <div className="dashboard-header">
        <div>
          <h2 className="dash-title">Test Dashboard</h2>
          <p className="dash-sub">
            Pipeline complete —{' '}
            <span className="dash-url">{siteUrl.replace(/^https?:\/\//, '') || 'Unknown Site'}</span>
          </p>
        </div>
        <div style={{ display: 'flex', gap: 10, alignItems: 'center' }}>
          <a
            href="/api/report" download="test_report.pdf"
            className="btn-primary"
            style={{ textDecoration: 'none', display: 'flex', alignItems: 'center', gap: 6 }}
          >
            <svg width="13" height="13" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
              <polyline points="7 10 12 15 17 10" /><line x1="12" y1="15" x2="12" y2="3" />
            </svg>
            Download PDF
          </a>
          <button className="btn-secondary" onClick={onReset} id="reset-btn">
            <svg width="13" height="13" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
              <path d="M1 4v6h6M23 20v-6h-6" /><path d="M20.49 9A9 9 0 0 0 5.64 5.64L1 10m22 4-4.64 4.36A9 9 0 0 1 3.51 15" />
            </svg>
            New Analysis
          </button>
        </div>
      </div>

      {/* KPIs */}
      <div className="kpi-strip">
        <div className="kpi-card">
          <div className="kpi-val blue">{total}</div>
          <div className="kpi-label">Tests Validated</div>
        </div>
        <div className="kpi-card">
          <div className="kpi-val red">{rejected}</div>
          <div className="kpi-label">Rejected</div>
        </div>
        <div className="kpi-card">
          <div className="kpi-val green">{pages}</div>
          <div className="kpi-label">Pages Crawled</div>
        </div>
        <div className="kpi-card">
          <div className="kpi-val blue">{passRate}%</div>
          <div className="kpi-label">Validation Rate</div>
        </div>
      </div>

      {/* Tabs */}
      <div className="tab-bar">
        {TABS.map(tab => (
          <button
            key={tab.id}
            className={`tab-btn ${activeTab === tab.id ? 'active' : ''}`}
            onClick={() => setActiveTab(tab.id)}
          >
            <span>{tab.icon}</span>
            {tab.label}
            {tab.id === 'tests' && <span className="tab-count">{total}</span>}
          </button>
        ))}
      </div>

      <div className="tab-content">
        {activeTab === 'tests' && <TestsTable tests={tests} />}
        {activeTab === 'execution' && <ExecutionPanel tests={tests} />}
        {activeTab === 'report' && <ReportSummary tests={tests} meta={meta} siteUrl={siteUrl} />}
      </div>
    </div>
  )
}
