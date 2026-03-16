export default function Navbar({ busy }) {
  return (
    <nav className="nav">
      <div className="nav-inner">
        <a href="#" className="nav-brand">
          <div className="nav-logo">
            <svg width="16" height="16" fill="none" stroke="#3b82f6" strokeWidth="2" viewBox="0 0 24 24">
              <path d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0 1 12 2.944a11.955 11.955 0 0 1-8.618 3.04A12.02 12.02 0 0 0 3 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/>
            </svg>
          </div>
          <span className="nav-name">QA<span> Engine</span></span>
        </a>
        <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
          {busy && (
            <div className="nav-status">
              <div className="status-dot" style={{ background: '#f59e0b', boxShadow: '0 0 8px rgba(245,158,11,0.6)' }} />
              Running
            </div>
          )}
          <span className="nav-tag">v2.0</span>
        </div>
      </div>
    </nav>
  )
}
