"""
FastAPI backend for the AI Exploratory Test Generator.
Runs the 7-stage Python pipeline and streams progress via Server-Sent Events.
"""

import asyncio
import json
import os
import queue
import subprocess
import sys
import threading
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel

# ── Paths ────────────────────────────────────────────────────────
SRC_DIR  = Path(__file__).parent
BASE_DIR = SRC_DIR.parent

# Load .env so GROQ_API_KEY is available to subprocesses
try:
    from dotenv import load_dotenv
    load_dotenv(SRC_DIR / ".env")
except ImportError:
    pass

PYTHON = sys.executable

# ── App ──────────────────────────────────────────────────────────
app = FastAPI(title="AI Test Generator API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Pipeline stages ──────────────────────────────────────────────
STAGES = [
    (1, "Website Crawling",                "the_crawler.py"),
    (2, "Enriching Snapshot",              "enrich_crawl_for_ai.py"),
    (3, "AI Test Generation",              "ai_test_generator_grok.py"),
    (4, "Anti-Hallucination Validation",   "validator.py"),
    (5, "Converting to Gauge Specs",       "json_to_gauge.py"),
    (6, "Generating Step Implementations", "ai_step_generator.py"),
    (7, "Building PDF Report",             "report_generator.py"),
]

# Only one pipeline at a time
_pipeline_lock = threading.Lock()


# ── Pipeline runner (runs in background thread) ──────────────────
def _run_pipeline(url: str, max_pages: int, max_depth: int, eq: queue.Queue):
    try:
        for stage_id, stage_name, script in STAGES:
            eq.put({"stage": stage_id, "name": stage_name, "status": "running"})

            stdin_data = None
            if stage_id == 1:
                # Crawler reads: URL, depth, pages from stdin
                stdin_data = f"{url}\n{max_depth}\n{max_pages}\n"

            # Use Popen to stream output
            proc = subprocess.Popen(
                [PYTHON, str(SRC_DIR / script)],
                stdin=subprocess.PIPE if stdin_data else None,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                cwd=str(BASE_DIR),
                encoding='utf-8',
                errors='replace'
            )

            if stdin_data and proc.stdin:
                proc.stdin.write(stdin_data)
                proc.stdin.flush()
                proc.stdin.close()

            # Read line by line and stream
            for line in proc.stdout:
                line = line.strip()
                if line:
                    eq.put({"stage": stage_id, "name": stage_name, "status": "running", "log": line})

            proc.wait()

            if proc.returncode != 0:
                eq.put({"stage": stage_id, "name": stage_name,
                        "status": "error", "error": f"Stage crashed with exit code {proc.returncode}"})
                eq.put({"complete": True, "success": False})
                return

            eq.put({"stage": stage_id, "name": stage_name, "status": "done"})

        eq.put({"complete": True, "success": True})

    except Exception as e:
        eq.put({"complete": True, "success": False, "error": str(e)})
    finally:
        eq.put(None)  # sentinel — stop the stream


# ── Request model ────────────────────────────────────────────────
class RunRequest(BaseModel):
    url: str
    max_pages: int = 10
    max_depth: int = 2


# ── Endpoints ────────────────────────────────────────────────────

@app.post("/api/run")
async def run_pipeline(body: RunRequest):
    """Start the pipeline and stream stage progress as SSE."""
    if not _pipeline_lock.acquire(blocking=False):
        raise HTTPException(409, "A pipeline run is already in progress.")

    eq: queue.Queue = queue.Queue()

    threading.Thread(
        target=_run_pipeline,
        args=(body.url, body.max_pages, body.max_depth, eq),
        daemon=True,
    ).start()

    async def event_stream():
        try:
            while True:
                try:
                    event = eq.get_nowait()
                except queue.Empty:
                    await asyncio.sleep(0.15)
                    continue

                if event is None:
                    break
                yield f"data: {json.dumps(event)}\n\n"
        finally:
            _pipeline_lock.release()

    return StreamingResponse(event_stream(), media_type="text/event-stream")


@app.get("/api/results")
async def get_results():
    """Return validated test cases + pipeline metadata."""
    validated_path = BASE_DIR / "data" / "validated_test_cases.json"
    rejected_path  = BASE_DIR / "data" / "rejected_test_cases.json"
    snapshot_path  = BASE_DIR / "data" / "ai_exploration_snapshot.json"

    if not validated_path.exists():
        return {"generated_tests": [], "meta": {}}

    with open(validated_path, encoding="utf-8") as f:
        data = json.load(f)
    validated = data.get("generated_tests", [])

    rejected_count = 0
    if rejected_path.exists():
        with open(rejected_path, encoding="utf-8") as f:
            rejected_count = len(json.load(f).get("rejected_tests", []))

    pages_count = 0
    if snapshot_path.exists():
        with open(snapshot_path, encoding="utf-8") as f:
            pages_count = json.load(f).get("metadata", {}).get("total_pages", 0)

    total = len(validated) + rejected_count
    pass_rate = round(len(validated) / max(total, 1) * 100, 1) if total else 0

    return {
        "generated_tests": validated,
        "meta": {
            "total_validated":      len(validated),
            "total_rejected":       rejected_count,
            "total_generated":      total,
            "pages_crawled":        pages_count,
            "validation_pass_rate": pass_rate,
        },
    }


@app.get("/api/report")
async def get_report():
    """Download the generated PDF report."""
    report_path = BASE_DIR / "reports" / "test_report.pdf"
    if not report_path.exists():
        raise HTTPException(404, "Report not yet generated. Run the pipeline first.")
    return FileResponse(str(report_path), filename="test_report.pdf",
                        media_type="application/pdf")


@app.get("/api/health")
async def health():
    return {"status": "ok", "pipeline_busy": not _pipeline_lock.acquire(blocking=False)
            or (_pipeline_lock.release() or False)}


if __name__ == "__main__":
    import uvicorn
    print("Starting AI Test Generator API on http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
