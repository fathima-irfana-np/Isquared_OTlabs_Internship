const CARDS = [
  {
    icon: <svg width="17" height="17" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24"><path d="M21 16V8a2 2 0 0 0-1-1.73L13 2.27a2 2 0 0 0-2 0L4 6.27A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><polyline points="3.27 6.96 12 12.01 20.73 6.96"/><line x1="12" y1="22.08" x2="12" y2="12"/></svg>,
    title: 'Deep Crawl',
    desc: 'Traverses every reachable page, extracting all interactive elements.',
  },
  {
    icon: <svg width="17" height="17" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24"><path d="M9 3H5a2 2 0 0 0-2 2v4m6-6h10a2 2 0 0 1 2 2v4M9 3v18m0 0h10a2 2 0 0 0 2-2V9M9 21H5a2 2 0 0 1-2-2V9m0 0h18"/></svg>,
    title: 'Test Generation',
    desc: 'Adversarial, boundary, and edge-case tests — generated and validated.',
  },
  {
    icon: <svg width="17" height="17" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>,
    title: 'PDF Report',
    desc: 'Full QA report with test listings, coverage stats, and validation results.',
  },
]

export default function Home() {
  return (
    <section className="home">
      <div className="wrap">
        <div className="home-badge">
          <span className="badge-dot" />
          Automated · Validated · Zero Setup
        </div>
        <h1 className="home-h">
          Automated QA Testing<br />
          <span className="hl">for Any Website</span>
        </h1>
        <p className="home-sub">
          Enter a URL, run the pipeline, and get a full set of validated test cases
          and a professional QA report — completely automated.
        </p>
        <div className="home-cards">
          {CARDS.map(c => (
            <div className="hcard" key={c.title}>
              <div className="hcard-icon">{c.icon}</div>
              <div className="hcard-title">{c.title}</div>
              <div className="hcard-desc">{c.desc}</div>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
