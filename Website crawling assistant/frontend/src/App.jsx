import { useState, useRef, useCallback, useEffect } from 'react'
import './index.css'
import Navbar from './components/Navbar'
import Home from './components/Home'
import RunForm from './components/RunForm'
import LiveProgress from './components/LiveProgress'
import Dashboard from './components/Dashboard'

const API = 'http://localhost:8001'

// Enrich raw test data from validated_test_cases.json
function enrichTests(raw) {
  return (raw || []).map((t, i) => ({
    id: t.id || `TC-${String(i + 1).padStart(3, '0')}`,
    goal: t.goal || t.description || t.test_goal || 'Untitled',
    category: t.category || classifyByGoal(t.goal || ''),
    steps: Array.isArray(t.steps) ? t.steps : [],
    expected: t.expected || t.expected_result || '',
    status: 'pass',
  }))
}

// Simple fallback classifier if backend doesn't provide category
const CATS = [
  ['Boundary', /boundar|edge.?case|min\b|max\b|limit|overflow/i],
  ['Negative', /negative|invalid|inject|script|non.?numeric|special.?char/i],
  ['Validation', /validat|error.*message|required|submit.*empty|enforce/i],
  ['Navigation', /navigate|cross.?page|switch.*page|back button/i],
  ['State', /state|persist|retain|preserve|recalcul/i],
  ['Auth', /sign.?in|login|password|auth|credential/i],
  ['Zero/Empty', /\b0\b|empty|blank|zero.*input/i],
]
function classifyByGoal(goal) {
  for (const [name, re] of CATS) if (re.test(goal)) return name
  return 'Functional'
}

// SSE reader — calls onEvt for each parsed event
async function readSSE(res, onEvt, signal) {
  const reader = res.body.getReader()
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
      try { onEvt(JSON.parse(line.slice(5).trim())) } catch { }
    }
  }
}

export default function App() {
  const [url, setUrl] = useState('')
  const [pages, setPages] = useState(10)
  const [view, setView] = useState('home')   // home | running | done
  const [phase, setPhase] = useState('')
  const [pct, setPct] = useState(0)
  const [logs, setLogs] = useState([])
  const [errMsg, setErrMsg] = useState('')
  const [tests, setTests] = useState([])
  const [meta, setMeta] = useState({})
  const abortRef = useRef(null)

  const pushLog = (text, type = 'info') =>
    setLogs(l => [...l.slice(-300), { text, type }])

  // Run a single API endpoint and stream its logs
  const runEndpoint = useCallback(async (endpoint, body = {}) => {
    const ctrl = new AbortController()
    abortRef.current = ctrl

    setPhase(endpoint)
    setPct(5)
    setErrMsg('')

    const res = await fetch(`${API}/api/${endpoint}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
      signal: ctrl.signal,
    })

    if (!res.ok) {
      const err = await res.json().catch(() => ({}))
      throw new Error(err.detail || `Server error ${res.status}`)
    }

    let success = false
    await readSSE(res, evt => {
      if (evt.type === 'log') pushLog(evt.text, 'info')
      if (evt.type === 'phase') pushLog(`→ ${evt.text}`, 'ok')
      if (evt.type === 'error') { pushLog(evt.text, 'err'); setErrMsg(evt.text) }
      if (evt.type === 'done') { success = evt.success; setPct(100) }
    }, ctrl.signal)

    if (!success && !errMsg) throw new Error('Pipeline step failed. Check logs.')
    return success
  }, [errMsg])

  // Full pipeline or single step
  const handleRun = useCallback(async (startEndpoint) => {
    if (!url.trim()) return
    setView('running')
    setLogs([])
    setErrMsg('')
    setTests([])
    setMeta({})
    setPct(0)

    const cleanUrl = url.trim().startsWith('http') ? url.trim() : 'https://' + url.trim()

    try {
      if (startEndpoint === 'crawl') {
        // Full pipeline: crawl → process → report
        pushLog(`Starting full pipeline for ${cleanUrl}`, 'ok')
        setPct(5)
        await runEndpoint('crawl', { url: cleanUrl, max_pages: pages, max_depth: 2 })
        setPct(35)
        pushLog('Crawl complete. Starting processing…', 'ok')

        await runEndpoint('process', {})
        setPct(75)
        pushLog('Processing complete. Generating report…', 'ok')

        await runEndpoint('generate-report', {})
        setPct(100)
        pushLog('Report generated.', 'ok')
      } else {
        // Single step
        const body = startEndpoint === 'crawl'
          ? { url: cleanUrl, max_pages: pages, max_depth: 2 } : {}
        await runEndpoint(startEndpoint, body)
      }

      // Fetch real results
      const r = await fetch(`${API}/api/results`)
      const data = await r.json()
      setTests(enrichTests(data.tests))
      setMeta(data.meta || {})
      setView('done')
    } catch (e) {
      if (e.name === 'AbortError') return
      setErrMsg(e.message)
      // still show dashboard if we have tests
      const r = await fetch(`${API}/api/results`).catch(() => null)
      if (r?.ok) {
        const data = await r.json()
        if (data.tests?.length) {
          setTests(enrichTests(data.tests))
          setMeta(data.meta || {})
          setView('done')
          return
        }
      }
      setView('running')  // stay on progress view showing error
    }
  }, [url, pages, runEndpoint])

  const handleStepRun = useCallback(async (endpoint) => {
    setView('running')
    setLogs([])
    setErrMsg('')
    setPhase(endpoint)
    setPct(0)
    const cleanUrl = url.trim().startsWith('http') ? url.trim() : 'https://' + url.trim()
    const body = endpoint === 'crawl' ? { url: cleanUrl, max_pages: pages, max_depth: 2 } : {}
    try {
      pushLog(`Running: ${endpoint}…`, 'ok')
      await runEndpoint(endpoint, body)
      pushLog('Step complete.', 'ok')
      const r = await fetch(`${API}/api/results`)
      if (r.ok) {
        const data = await r.json()
        if (data.tests?.length) {
          setTests(enrichTests(data.tests))
          setMeta(data.meta || {})
          setView('done')
          return
        }
      }
      // Step done but no results yet — go back to home so user can run next step
      setView('home')
    } catch (e) {
      if (e.name !== 'AbortError') setErrMsg(e.message)
      setView('running')
    }
  }, [url, pages, runEndpoint])

  const reset = () => {
    abortRef.current?.abort()
    setView('home'); setLogs([]); setTests([]); setMeta({})
    setErrMsg(''); setPct(0); setPhase('')
  }

  useEffect(() => () => abortRef.current?.abort(), [])

  const busy = view === 'running'

  return (
    <>
      <Navbar busy={busy} />
      <main>
        {view === 'home' && <Home />}

        {view !== 'done' && (
          <div className="wrap" style={{ paddingBottom: 80 }}>
            <RunForm
              url={url} pages={pages}
              onUrl={setUrl} onPages={setPages}
              onRun={() => handleRun('crawl')}
              // onRun={(ep) => ep === 'crawl' && !phase ? handleRun('crawl') : handleStepRun(ep)}
              disabled={busy}
            />
            {busy && (
              <LiveProgress phase={phase} pct={pct} logs={logs} error={errMsg} />
            )}
            {errMsg && !busy && (
              <div className="err-card" style={{ marginTop: 16 }}>
                <svg width="16" height="16" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
                  <circle cx="12" cy="12" r="10" /><line x1="12" y1="8" x2="12" y2="12" /><line x1="12" y1="16" x2="12.01" y2="16" />
                </svg>
                <div>
                  <div className="err-title">Error</div>
                  <div className="err-msg">{errMsg}</div>
                  <button className="btn-sec" style={{ marginTop: 10, fontSize: '.76rem', padding: '5px 14px' }} onClick={reset}>Reset</button>
                </div>
              </div>
            )}
          </div>
        )}

        {view === 'done' && (
          <div className="wrap" style={{ paddingBottom: 80 }}>
            <Dashboard tests={tests} meta={meta} siteUrl={url} onReset={reset} />
          </div>
        )}
      </main>
      <footer className="footer">QA Engine · Automated Web Testing</footer>
    </>
  )
}
