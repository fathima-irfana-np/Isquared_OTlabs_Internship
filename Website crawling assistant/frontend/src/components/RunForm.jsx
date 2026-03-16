const PlayIcon = () => (
  <svg width="13" height="13" fill="none" stroke="currentColor" strokeWidth="2.5" viewBox="0 0 24 24">
    <polygon points="5 3 19 12 5 21 5 3" />
  </svg>
)

export default function RunForm({ url, pages, onUrl, onPages, onRun, disabled }) {
  return (
    <div className="card form-card">
      <div className="form-row">
        <div>
          <label className="flabel" htmlFor="url">Target URL</label>
          <div className="finput-wrap">
            <span className="finput-icon">
              <svg width="13" height="13" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
                <circle cx="12" cy="12" r="10" />
                <path d="M2 12h20M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z" />
              </svg>
            </span>
            <input
              id="url" className="finput" type="url"
              placeholder="https://example.com"
              value={url} onChange={e => onUrl(e.target.value)}
              disabled={disabled} autoComplete="url"
              onKeyDown={e => e.key === 'Enter' && !disabled && url.trim() && onRun()}
            />
          </div>
        </div>
        <div>
          <label className="flabel" htmlFor="pages">Pages (max 30)</label>
          <input
            id="pages" className="finput no-icon" type="number"
            min={1} max={30} value={pages}
            onChange={e => onPages(Math.min(30, Math.max(1, Number(e.target.value))))}
            disabled={disabled}
          />
        </div>
      </div>

      <div style={{ marginTop: 16, display: 'flex', justifyContent: 'flex-end' }}>
        <button
          className="btn-run-all"
          disabled={disabled || !url.trim()}
          onClick={onRun}
        >
          {disabled
            ? <><span className="spinner" /> Running Pipeline…</>
            : <><PlayIcon /> Run Pipeline</>}
        </button>
      </div>
    </div>
  )
}