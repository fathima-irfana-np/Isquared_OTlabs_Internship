import asyncio
import json
import queue
import subprocess
import sys
import threading
import time
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel

SRC_DIR  = Path(__file__).parent
BASE_DIR = SRC_DIR.parent

try:
    from dotenv import load_dotenv
    load_dotenv(SRC_DIR / ".env")
except ImportError:
    pass

PYTHON = sys.executable

app = FastAPI(title="QA Engine API", version="2.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

_pipeline_lock = threading.Lock()


def _stream_script(script: str, stdin_data, eq: queue.Queue, label: str):
    """
    Run python script with -u (unbuffered) so every print() line
    streams to the frontend immediately in real time.
    """
    proc = subprocess.Popen(
        [PYTHON, "-u", str(SRC_DIR / script)],
        stdin=subprocess.PIPE if stdin_data else None,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        cwd=str(BASE_DIR),
        encoding="utf-8",
        errors="replace",
    )
    if stdin_data and proc.stdin:
        proc.stdin.write(stdin_data)
        proc.stdin.flush()
        proc.stdin.close()

    for line in proc.stdout:
        line = line.rstrip()
        if line:
            eq.put({"type": "log", "phase": label, "text": line})

    proc.wait()
    return proc.returncode


def _make_stream(runner_fn):
    if not _pipeline_lock.acquire(blocking=False):
        raise HTTPException(409, "Another pipeline job is already running.")

    eq: queue.Queue = queue.Queue()

    def target():
        try:
            runner_fn(eq)
        except Exception as e:
            eq.put({"type": "error", "text": str(e)})
            eq.put({"type": "done", "success": False})
        finally:
            eq.put(None)

    threading.Thread(target=target, daemon=True).start()

    async def event_stream():
        try:
            while True:
                try:
                    evt = eq.get_nowait()
                except queue.Empty:
                    await asyncio.sleep(0.05)
                    continue
                if evt is None:
                    break
                yield f"data: {json.dumps(evt)}\n\n"
        finally:
            _pipeline_lock.release()

    return StreamingResponse(event_stream(), media_type="text/event-stream")


class CrawlRequest(BaseModel):
    url: str
    max_pages: int = 10
    max_depth: int = 2

class EmptyRequest(BaseModel):
    pass


@app.post("/api/crawl")
async def run_crawl(body: CrawlRequest):
    url = body.url.strip()
    if not url.startswith("http"):
        url = "https://" + url

    def runner(eq):
        eq.put({"type": "phase", "phase": "crawl", "text": f"Starting crawler → {url}"})
        rc = _stream_script(
            "the_crawler.py",
            f"{url}\n{body.max_depth}\n{body.max_pages}\n",
            eq, "crawl",
        )
        if rc != 0:
            eq.put({"type": "error", "text": f"Crawler exited with code {rc}"})
            eq.put({"type": "done", "success": False})
        else:
            eq.put({"type": "done", "success": True, "phase": "crawl"})

    return _make_stream(runner)


@app.post("/api/process")
async def run_process(body: EmptyRequest = None):
    def runner(eq):
        eq.put({"type": "phase", "phase": "process", "text": "Starting processing pipeline…"})
        time.sleep(3)
        rc = _stream_script("run_tester.py", None, eq, "process")
        if rc != 0:
            eq.put({"type": "error", "text": f"Processing exited with code {rc}"})
            eq.put({"type": "done", "success": False})
        else:
            eq.put({"type": "done", "success": True, "phase": "process"})

    return _make_stream(runner)


@app.post("/api/generate-report")
async def run_report(body: EmptyRequest = None):
    def runner(eq):
        eq.put({"type": "phase", "phase": "report", "text": "Building PDF report…"})
        time.sleep(3)
        rc = _stream_script("report_generator.py", None, eq, "report")
        if rc != 0:
            eq.put({"type": "error", "text": f"Report generator exited with code {rc}"})
            eq.put({"type": "done", "success": False})
        else:
            eq.put({"type": "done", "success": True, "phase": "report"})

    return _make_stream(runner)


@app.get("/api/results")
async def get_results():
    validated_path = BASE_DIR / "data" / "validated_test_cases.json"
    rejected_path  = BASE_DIR / "data" / "rejected_test_cases.json"
    snapshot_path  = BASE_DIR / "data" / "ai_exploration_snapshot.json"

    if not validated_path.exists():
        return {"tests": [], "meta": {}}

    with open(validated_path, encoding="utf-8") as f:
        vdata = json.load(f)
    tests = vdata.get("generated_tests", [])

    rejected_count = 0
    if rejected_path.exists():
        with open(rejected_path, encoding="utf-8") as f:
            rejected_count = len(json.load(f).get("rejected_tests", []))

    pages_count = 0
    elements_count = 0
    target_url = ""
    if snapshot_path.exists():
        with open(snapshot_path, encoding="utf-8") as f:
            snap = json.load(f)
        pages_count = snap.get("metadata", {}).get("total_pages", 0)
        for page in snap.get("pages", []):
            for items in page.get("ui_inventory", {}).values():
                elements_count += len(items)
        first_page = snap.get("pages", [{}])[0] if snap.get("pages") else {}
        target_url = first_page.get("page_context", {}).get("url", "")

    total_gen = len(tests) + rejected_count
    val_rate  = round(len(tests) / max(total_gen, 1) * 100, 1) if total_gen else 0

    return {
        "tests": tests,
        "meta": {
            "target_url":      target_url,
            "pages_crawled":   pages_count,
            "elements_found":  elements_count,
            "total_generated": total_gen,
            "total_validated": len(tests),
            "total_rejected":  rejected_count,
            "validation_rate": val_rate,
        },
    }


@app.get("/api/download")
async def download_report():
    report_path = BASE_DIR / "reports" / "test_report.pdf"
    if not report_path.exists():
        raise HTTPException(404, "Report not yet generated.")
    return FileResponse(str(report_path), filename="test_report.pdf", media_type="application/pdf")


@app.get("/api/health")
async def health():
    busy = not _pipeline_lock.acquire(blocking=False)
    if not busy:
        _pipeline_lock.release()
    return {"status": "ok", "busy": busy}


if __name__ == "__main__":
    import uvicorn
    print("QA Engine API → http://localhost:8001")
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="info")