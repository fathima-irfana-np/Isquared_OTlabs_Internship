export default function InputForm({ siteUrl, pageCount, depth, onUrlChange, onPageChange, onDepthChange, onSubmit, disabled }) {
  const handleSubmit = (e) => { e.preventDefault(); onSubmit() }

  return (
    <div className="card form-card">
      <form onSubmit={handleSubmit}>
        <div style={{ display: 'flex', flexWrap: 'nowrap', alignItems: 'flex-end', gap: 12 }}>

          {/* URL */}
          <div style={{ flex: 1, minWidth: 0 }}>
            <label className="form-label" htmlFor="site-url">Target URL</label>
            <div className="input-wrap">
              <span className="input-icon">
                <svg width="14" height="14" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
                  <circle cx="12" cy="12" r="10" />
                  <path d="M2 12h20M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z" />
                </svg>
              </span>
              <input
                id="site-url" className="input-field" type="url"
                placeholder="https://example.com"
                value={siteUrl} onChange={e => onUrlChange(e.target.value)}
                disabled={disabled} required autoComplete="url"
              />
            </div>
          </div>

          {/* Max Pages */}
          <div style={{ flexShrink: 0, width: 120 }}>
            <label className="form-label" htmlFor="page-count">Max Pages</label>
            <select
              id="page-count" className="input-field no-icon"
              value={pageCount} onChange={e => onPageChange(Number(e.target.value))}
              disabled={disabled} style={{ width: '100%' }}
            >
              {Array.from({ length: 30 }, (_, i) => i + 1).map(n => (
                <option key={n} value={n}>{n}</option>
              ))}
            </select>
          </div>

          {/* Max Depth */}
          <div style={{ flexShrink: 0, width: 120 }}>
            <label className="form-label" htmlFor="depth">Max Depth</label>
            <select
              id="depth" className="input-field no-icon"
              value={depth} onChange={e => onDepthChange(Number(e.target.value))}
              disabled={disabled} style={{ width: '100%' }}
            >
              {[1, 2, 3].map(n => (
                <option key={n} value={n}>{n}</option>
              ))}
            </select>
          </div>
        </div>

        <div style={{ marginTop: 18, display: 'flex', justifyContent: 'flex-end' }}>
          <button type="submit" className="btn-primary" disabled={disabled || !siteUrl.trim()} id="run-btn">
            {disabled ? (
              <><span className="spinner" /> Analysing…</>
            ) : (
              <>
                <svg width="14" height="14" fill="none" stroke="currentColor" strokeWidth="2.5" viewBox="0 0 24 24">
                  <polygon points="5 3 19 12 5 21 5 3" />
                </svg>
                Run Analysis
              </>
            )}
          </button>
        </div>
      </form>
    </div>
  )
}
