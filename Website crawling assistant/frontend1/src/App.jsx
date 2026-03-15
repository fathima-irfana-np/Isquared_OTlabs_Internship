import { useState, useRef } from 'react'
import './index.css'
import Navbar from './components/Navbar'
import Hero from './components/Hero'
import InputForm from './components/InputForm'
import OrbProgress from './components/OrbProgress'
import Dashboard from './components/Dashboard'
import Footer from './components/Footer'

const STAGES = [
  { id: 1, name: 'Website Crawling' },
  { id: 2, name: 'Enriching Snapshot' },
  { id: 3, name: 'AI Test Generation' },
  { id: 4, name: 'Anti-Hallucination Validation' },
  { id: 5, name: 'Converting to Gauge Specs' },
  { id: 6, name: 'Generating Step Implementations' },
  { id: 7, name: 'Building PDF Report' },
]

export default function App() {
  const [status, setStatus] = useState('idle')
  const [siteUrl, setSiteUrl] = useState('')
  const [pageCount, setPageCount] = useState(10)
  const [depth, setDepth] = useState(2)
  const [currentStage, setCurrentStage] = useState(-1)
  const [doneStages, setDoneStages] = useState([])
  const [tests, setTests] = useState([])
  const [meta, setMeta] = useState({})
  const [error, setError] = useState(null)
  const [logs, setLogs] = useState([])
  const readerRef = useRef(null)

  const runPipeline = async () => {
    setStatus('running')
    setCurrentStage(0)
    setDoneStages([])
    setTests([])
    setMeta({})
    setError(null)
    setLogs([])

    try {
      const res = await fetch('/api/run', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url: siteUrl, max_pages: pageCount, max_depth: depth }),
      })

      if (!res.ok) {
        const err = await res.json()
        throw new Error(err.detail || 'Server error')
      }

      const reader = res.body.getReader()
      readerRef.current = reader
      const decoder = new TextDecoder()
      let buffer = ''

      while (true) {
        const { done, value } = await reader.read()
        if (done) break
        buffer += decoder.decode(value, { stream: true })
        const lines = buffer.split('\n')
        buffer = lines.pop()

        for (const line of lines) {
          if (!line.startsWith('data: ')) continue
          try {
            const evt = JSON.parse(line.slice(6))

            if (evt.log) {
              setLogs(prev => [...prev.slice(-99), evt.log])
            }

            if (evt.status === 'running') {
              setCurrentStage(evt.stage - 1)
            } else if (evt.status === 'done') {
              setDoneStages(prev => [...prev, evt.stage - 1])
            } else if (evt.status === 'error') {
              setError(`Stage ${evt.stage} (${evt.name}) failed:\n${evt.error}`)
              setStatus('error')
              return
            }

            if (evt.complete && evt.success) {
              const r = await fetch('/api/results')
              const data = await r.json()
              setTests(data.generated_tests || [])
              setMeta(data.meta || {})
              setCurrentStage(-1)
              setStatus('done')
            }
          } catch (_) { /* skip malformed lines */ }
        }
      }
    } catch (err) {
      setError(err.message || 'Could not connect to API. Is the server running on port 8000?')
      setStatus('error')
    }
  }

  const reset = () => {
    readerRef.current?.cancel()
    readerRef.current = null
    setStatus('idle')
    setCurrentStage(-1)
    setDoneStages([])
    setTests([])
    setMeta({})
    setSiteUrl('')
    setPageCount(10)
    setDepth(2)
    setError(null)
    setLogs([])
  }

  const progressPct = status === 'done' ? 100
    : status === 'running' ? Math.round((doneStages.length / STAGES.length) * 100)
      : 0

  return (
    <>
      <div className="orb orb-1" />
      <div className="orb orb-2" />
      <div className="orb orb-3" />

      <Navbar />

      <main>
        {status === 'idle' && <Hero />}

        <div className="container" style={{ paddingBottom: 80 }}>
          {status !== 'done' && (
            <InputForm
              siteUrl={siteUrl} pageCount={pageCount} depth={depth}
              onUrlChange={setSiteUrl} onPageChange={setPageCount} onDepthChange={setDepth}
              onSubmit={runPipeline} disabled={status === 'running'}
            />
          )}

          {error && (
            <div style={{
              background: 'rgba(244,63,94,0.10)', border: '1px solid rgba(244,63,94,0.3)',
              borderRadius: 12, padding: '14px 18px', color: '#f43f5e',
              marginTop: 16, fontSize: '0.88rem', whiteSpace: 'pre-wrap',
            }}>
              ❌ {error}
            </div>
          )}

          {status === 'running' && (
            <OrbProgress
              stages={STAGES} currentStage={currentStage}
              doneStages={doneStages} progressPct={progressPct}
              logs={logs}
            />
          )}

          {status === 'done' && tests.length > 0 && (
            <Dashboard tests={tests} meta={meta} siteUrl={siteUrl} onReset={reset} />
          )}
        </div>
      </main>

      <Footer />
    </>
  )
}
