import Logo from './Logo'

export default function Navbar() {
  return (
    <nav className="navbar">
      <div className="navbar-inner">
        <a href="#" className="navbar-brand" aria-label="QA Engine Home">
          <Logo size={34} />
          <span className="brand-text">QA<span> Engine</span></span>
        </a>
        <div>
          <span className="nav-pill">v2.0 · BETA</span>
        </div>
      </div>
    </nav>
  )
}
