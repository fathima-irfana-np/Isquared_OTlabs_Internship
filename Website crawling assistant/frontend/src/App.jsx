import { useState, useRef, useCallback, useEffect } from 'react'
import './index.css'
import Navbar       from './components/Navbar'
import Home         from './components/Home'
import RunForm      from './components/RunForm'
import LiveProgress from './components/LiveProgress'
import Dashboard    from './components/Dashboard'

const API = 'http://localhost:8001'

function enrichTests(raw) {
  return (raw || []).map((t, i) => ({
    id:       t.id || `TC-${String(i + 1).padStart(3, '0')}`,
    goal:     t.goal || t.description || t.test_goal || 'Untitled',
    category: t.category || classifyByGoal(t.goal || ''),
    steps:    Array.isArray(t.steps) ? t.steps : [],
    expected: t.expected || t.expected_result || '',
    status:   'pass',
  }))
}

const CATS = [
  ['Boundary',    /boundar|edge.?case|min\b|max\b|limit|overflow/i],
  ['Negative',    /negative|invalid|inject|script|non.?numeric|special.?char/i],
  ['Validation',  /validat|error.*message|required|submit.*empty|enforce/i],
  ['Navigation',  /navigate|cross.?page|switch.*page|back button/i],
  ['State',       /state|persist|retain|preserve|recalcul/i],
  ['Auth',        /sign.?in|login|password|auth|credential/i],
  ['Zero/Empty',  /\b0\b|empty|blank|zero.*input/i],
]
function classifyByGoal(goal) {
  for (const [name, re] of CATS) if (re.test(goal)) return name
  return 'Functional'
}

async function readSSE(res, onEvt, signal) {
  const reader  = res.body.getReader()
  const decoder = new TextDecoder()
  let buf = ''
  while (true) {
    if (signal?.aborted) break
    const { done, value } = await reader.read()
    if (done) break
    buf += decoder.decode(value, { stream: true })
    const parts = buf.split('\n\n')
    buf = parts.pop()
    for (const part of parts) {
      const line = part.trim()
      if (!line.startsWith('data:')) continue
      try { onEvt(JSON.parse(line.slice(5).trim())) } catch {}
    }
  }
}

export default function App() {
  const [url,      setUrl]      = useState('')
  const [pages,    setPages]    = useState(10)
  const [running,  setRunning]  = useState(false)
  const [phase,    setPhase]    = useState('crawl')
  const [pct,      setPct]      = useState(0)
  const [logs,     setLogs]     = useState([])
  const [errMsg,   setErrMsg]   = useState('')
  const [tests,    setTests]    = useState([])
  const [meta,     setMeta]     = useState({})
  const [done,     setDone]     = useState(false)
  const abortRef     = useRef(null)
  const consoleRef   = useRef(null)  // ref to scroll into view
  const dashboardRef = useRef(null)  // ref to scroll into view

  const pushLog = useCallback((text, type = 'info') =>
    setLogs(l => [...l, { text, type }]), [])

  const pushSep = useCallback((label) =>
    setLogs(l => [...l, { text: `── ${label} ──`, type: 'sep' }]), [])

  const runEndpoint = useCallback(async (endpoint, body = {}, signal) => {
    const res = await fetch(`${API}/api/${endpoint}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
      signal,
    })
    if (!res.ok) {
      const err = await res.json().catch(() => ({}))
      throw new Error(err.detail || `Server error ${res.status}`)
    }
    return new Promise((resolve, reject) => {
      readSSE(res, evt => {
        if (evt.type === 'log')   pushLog(evt.text, 'info')
        if (evt.type === 'phase') pushLog(evt.text, 'ok')
        if (evt.type === 'error') pushLog(evt.text, 'err')
        if (evt.type === 'done') {
          if (evt.success) resolve(true)
          else reject(new Error('Step failed'))
        }
      }, signal).then(() => resolve(true)).catch(reject)
    })
  }, [pushLog])

  const handleRun = useCallback(async () => {
    if (!url.trim() || running) return
    const ctrl = new AbortController()
    abortRef.current = ctrl
    const cleanUrl = url.trim().startsWith('http') ? url.trim() : 'https://' + url.trim()

    setRunning(true)
    setDone(false)
    setLogs([])
    setErrMsg('')
    setTests([])
    setMeta({})
    setPct(0)
    setPhase('crawl')

    // scroll to console panel
    setTimeout(() => consoleRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' }), 100)

    try {
      // STEP 1 — CRAWL
      pushSep('STEP 1 — CRAWLING WEBSITE')
      pushLog(`Website URL: ${cleanUrl}`, 'ok')
      setPhase('crawl')
      setPct(5)
      await runEndpoint('crawl', { url: cleanUrl, max_pages: pages, max_depth: 2 }, ctrl.signal)
      setPct(33)
      pushLog('✓ Crawl complete.', 'ok')
      pushLog('', 'info')
      await new Promise(r => setTimeout(r, 3000))

      // STEP 2 — PROCESS
      pushSep('STEP 2 — PROCESSING & GENERATING TESTS')
      setPhase('process')
      setPct(36)
      await runEndpoint('process', {}, ctrl.signal)
      setPct(75)
      pushLog('✓ Processing complete.', 'ok')
      pushLog('', 'info')
      await new Promise(r => setTimeout(r, 3000))

      // STEP 3 — REPORT
      pushSep('STEP 3 — BUILDING PDF REPORT')
      setPhase('report')
      setPct(78)
      await runEndpoint('generate-report', {}, ctrl.signal)
      setPct(100)
      pushLog('✓ Report generated.', 'ok')

      // fetch results
      const r    = await fetch(`${API}/api/results`)
      const data = await r.json()
      setTests(enrichTests(data.tests))
      setMeta(data.meta || {})
      setDone(true)
      setRunning(false)

      // scroll to dashboard after short pause
      await new Promise(r => setTimeout(r, 800))
      dashboardRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' })
      } catch (e) {
  if (e.name === 'AbortError') return
  pushLog(`✗ ${e.message}`, 'err')
  setErrMsg(e.message)
  setRunning(false)
}
  }, [url, pages, running, runEndpoint, pushLog, pushSep])

  const handleReset = () => {
    abortRef.current?.abort()
    setRunning(false)
    setDone(false)
    setLogs([])
    setTests([])
    setMeta({})
    setErrMsg('')
    setPct(0)
    setPhase('crawl')
    setUrl('')
    setPages(10)
    // scroll back to top
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  useEffect(() => () => abortRef.current?.abort(), [])

  return (
    <>
      <Navbar busy={running} />

      <main>
        {/* ── HERO — always visible ── */}
        <Home />

        {/* ── INPUT FORM — always visible ── */}
        <div className="wrap" style={{ paddingBottom: 32 }}>
          <RunForm
            url={url} pages={pages}
            onUrl={setUrl} onPages={setPages}
            onRun={handleRun}
            disabled={running}
          />
        </div>

        {/* ── CONSOLE — visible once pipeline starts ── */}
        {(running || logs.length > 0) && (
          <div className="wrap" ref={consoleRef} style={{ paddingBottom: 40, scrollMarginTop: 80 }}>
            <LiveProgress
              phase={phase}
              pct={pct}
              logs={logs}
              error={errMsg}
            />
          </div>
        )}

        {/* ── DASHBOARD — visible once pipeline completes ── */}
        {done && (
          <div className="wrap" ref={dashboardRef} style={{ paddingBottom: 80, scrollMarginTop: 80 }}>
            {/* divider */}
            <div style={{
              height: 1, background: 'var(--border)',
              margin: '8px 0 32px', opacity: .5,
            }} />
            <Dashboard
              tests={tests}
              meta={meta}
              siteUrl={url}
              onReset={handleReset}
            />
          </div>
        )}
      </main>

      <footer className="footer">QA Engine · Automated Web Testing</footer>
    </>
  )
}