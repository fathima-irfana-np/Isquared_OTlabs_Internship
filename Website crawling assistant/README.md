# 🕷️ AI-Powered Exploratory Test Generator

An automated pipeline that **crawls any website**, uses **AI to generate adversarial test cases**, validates them against the real UI, and produces **executable Gauge test specs** with Playwright — all with a 3-layer anti-hallucination defense.

Comes with a **React web dashboard** for running the pipeline visually and viewing results.

---

## 📋 Table of Contents

- [How It Works](#how-it-works)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Quick Start (Step-by-Step)](#quick-start-step-by-step)
- [Running the Web Dashboard (UI)](#running-the-web-dashboard-ui)
- [Running the Pipeline via CLI](#running-the-pipeline-via-cli)
- [Running Tests with Gauge](#running-tests-with-gauge)
- [Project Structure](#project-structure)
- [Output Files](#output-files)
- [Troubleshooting](#troubleshooting)

---

## How It Works

The pipeline has **7 stages** that transform a website URL into executable test specs:

```
Website URL
    │
    ▼
┌──────────────────────────────┐
│ 1. Crawl (Selenium)          │ → crawl_results.json
│ 2. Enrich (Snapshot Builder) │ → ai_exploration_snapshot.json
│ 3. Generate (Groq LLM)      │ → generated_test_cases.json
│ 4. Validate (Anti-Halluc.)   │ → validated_test_cases.json
│ 5. Convert (JSON → Gauge)    │ → specs/ai_exploration.spec
│ 6. Step Gen (Deterministic)  │ → step_impl/step_implementation.py
│ 7. Report (PDF)              │ → reports/test_report.pdf
└──────────────────────────────┘
```

### Anti-Hallucination Defense (3 Layers)

| Layer | Strategy |
|-------|----------|
| **Layer 1** | 70B parameter model (`llama-3.3-70b-versatile`) for better instruction following |
| **Layer 2** | Page-grouped label whitelist injected into prompts — constrains AI vocabulary |
| **Layer 3** | Post-generation validator checks every label and path against the real snapshot |

---

## Tech Stack

| Component | Technology |
|-----------|------------|
| Web Crawling | Selenium WebDriver (headless Chrome) |
| AI / LLM | Groq API (`llama-3.3-70b-versatile`) |
| Test Framework | [Gauge](https://gauge.org/) |
| Browser Automation | [Playwright](https://playwright.dev/python/) |
| PDF Reports | fpdf2 |
| Backend API | FastAPI + Uvicorn |
| Frontend Dashboard | React + Vite |
| Language | Python 3.10+ |

---

## Prerequisites

Make sure you have all of these installed **before** starting:

| Tool | How to check | Install link |
|------|-------------|--------------|
| **Python 3.10+** | `python --version` | [python.org](https://www.python.org/downloads/) |
| **Node.js 18+** | `node --version` | [nodejs.org](https://nodejs.org/) |
| **npm** | `npm --version` | Comes with Node.js |
| **Google Chrome** | Open Chrome | [google.com/chrome](https://www.google.com/intl/en/chrome/) |
| **Git** | `git --version` | [git-scm.com](https://git-scm.com/) |

You will also need:
- **Groq API Key** — sign up free at [console.groq.com](https://console.groq.com/) and create an API key.

---

## Quick Start (Step-by-Step)

### Step 1 — Clone the Repository

```cmd
git clone https://github.com/<your-username>/website-crawling-assistant.git
cd website-crawling-assistant
```

### Step 2 — Create a Python Virtual Environment

Open **CMD** (Command Prompt) in the project folder and run:

```cmd
python -m venv venv
```

Then **activate** it:

```cmd
venv\Scripts\activate
```

> ✅ You should see `(venv)` at the start of your terminal prompt. **Every time you open a new CMD window, you must activate the venv again.**

### Step 3 — Install Python Dependencies

```cmd
pip install -r requirements.txt
```

### Step 4 — Install Playwright Browsers

```cmd
playwright install chromium
```

### Step 5 — Install Gauge and Plugins

```cmd
npm install -g @getgauge/cli
gauge install python
gauge install html-report
```

Verify it works:

```cmd
gauge --version
```

### Step 6 — Install Node.js Dependencies (Root)

```cmd
npm install
```

### Step 7 — Install Frontend Dependencies

```cmd
cd frontend
npm install
cd ..
```

### Step 8 — Configure Your API Key

Create a file called `.env` inside the `src\` folder with this content:

```
GROQ_API_KEY=your_groq_api_key_here
```

> 🔑 Get a free key from [console.groq.com](https://console.groq.com/keys). Sign up → API Keys → Create API Key.

### Step 9 — Select the Python Interpreter in VS Code (Optional)

If using VS Code:

1. Open any `.py` file.
2. Press `Ctrl + Shift + P` → type **"Python: Select Interpreter"**.
3. Select the interpreter from `.\venv\Scripts\python.exe`.

---

## Running the Web Dashboard (UI)

The project has a **React frontend** and a **FastAPI backend** that together provide a web dashboard for running the pipeline.

### Start the Backend API Server

Open a terminal in the project root and run:

```cmd
python src/api_server.py
```

This starts the API server at **http://localhost:8001**.

### Start the Frontend Dev Server

Open a **second terminal** in the project root and run:

```cmd
cd frontend
npm run dev
```

This starts the React app at **http://localhost:5173** (Vite default).

### Use the Dashboard

1. Open **http://localhost:5173** in your browser.
2. Enter a website URL, page count, and depth.
3. Click through the pipeline stages:
   - **Crawl** — crawls the website with Selenium
   - **Process** — enriches data + generates + validates test cases
   - **Execute** — runs the Gauge tests (you'll see a browser pop up)
   - **Report** — generates a PDF report
4. View results and download the report from the dashboard.

> 💡 **Both terminals must stay running** (API backend + frontend dev server) while using the dashboard.

---

## Running the Pipeline via CLI

You can also run everything from the command line without the web dashboard.

### Option A: Run Each Stage Individually (Recommended for first run)

```cmd
python src/the_crawler.py
python src/enrich_crawl_for_ai.py
python src/ai_test_generator_grok.py
python src/validator.py
python src/json_to_gauge.py
python src/ai_step_generator.py
python src/report_generator.py
```

### Option B: Run Stages 4–6 via Pipeline Script

If you already have crawl data and generated tests:

```cmd
python src/run_tester.py
```

This runs the validation → Gauge conversion → step generation pipeline.

---

## Running Tests with Gauge

After the pipeline has generated the spec and step implementations:

```cmd
gauge run specs/
```

> **Note:** Tests launch a **visible Chromium browser** (`headless=False`) with a 2-second slow motion so you can observe the test execution.

---

## Project Structure

```
├── src/
│   ├── the_crawler.py            # Stage 1: Selenium web crawler
│   ├── enrich_crawl_for_ai.py    # Stage 2: Crawl data → AI snapshot
│   ├── ai_test_generator_grok.py # Stage 3: LLM test case generation
│   ├── validator.py              # Stage 4: Anti-hallucination validator
│   ├── json_to_gauge.py          # Stage 5: JSON → Gauge spec converter
│   ├── ai_step_generator.py      # Stage 6: Step implementation generator
│   ├── report_generator.py       # Stage 7: PDF report builder
│   ├── run_tester.py             # Pipeline orchestrator (stages 4-6)
│   ├── api_server.py             # FastAPI backend (serves the dashboard)
│   └── .env                      # API keys (not committed to git)
├── frontend/                     # React + Vite web dashboard
│   ├── src/                      # React components
│   ├── package.json              # Frontend dependencies
│   └── vite.config.js            # Vite configuration
├── step_impl/
│   ├── step_implementation.py    # Auto-generated Playwright step code
│   ├── resolver.py               # SmartResolver — heuristic element finder
│   └── __init__.py
├── specs/
│   └── ai_exploration.spec       # Auto-generated Gauge test scenarios
├── data/                         # Pipeline intermediate data files
├── reports/                      # Generated PDF reports
├── manifest.json                 # Gauge project configuration
├── package.json                  # Node.js dependencies (Gauge)
├── requirements.txt              # Python dependencies
└── .gitignore
```

---

## Output Files

| File | Description |
|------|-------------|
| `data/crawl_results.json` | Raw crawl data with all interactive elements |
| `data/ai_exploration_snapshot.json` | Enriched, AI-optimized site snapshot |
| `data/generated_test_cases.json` | Raw AI-generated test cases |
| `data/validated_test_cases.json` | Tests that passed anti-hallucination validation |
| `data/rejected_test_cases.json` | Rejected tests with failure reasons |
| `specs/ai_exploration.spec` | Executable Gauge test specification |
| `step_impl/step_implementation.py` | Playwright step implementations |
| `reports/test_report.pdf` | Professional PDF test report |

---

## Troubleshooting

### "Red lines" in VS Code

Your Python interpreter isn't set correctly. See [Step 9](#step-9--select-the-python-interpreter-in-vs-code-optional) — select the `venv` interpreter.

### `ModuleNotFoundError: No module named 'selenium'` (or any other module)

Make sure your virtual environment is **activated** (`(venv)` in your prompt) and run:

```cmd
pip install -r requirements.txt
```

### `playwright install` fails

Try running CMD **as Administrator** (right-click → Run as administrator):

```cmd
playwright install chromium
```

### Chrome not found by Selenium

Make sure Google Chrome is installed. Selenium uses it for the crawling stage.

### Groq API rate limit errors

The AI generation stage (Stage 3) has built-in rate limiting. If you still hit rate limits, wait a few minutes and re-run `python src/ai_test_generator_grok.py`.

### Frontend can't connect to the backend

Make sure the API server is running (`python src/api_server.py`) **before** using the frontend. The frontend expects the API at `http://localhost:8001`.

### Gauge tests fail to run

1. Verify Gauge is installed: `gauge --version`
2. Verify plugins: `gauge install python` and `gauge install html-report`
3. Make sure `specs/ai_exploration.spec` and `step_impl/step_implementation.py` exist (run the pipeline first).

---

## License

This project is licensed under the **Apache License 2.0** — see the [LICENSE](LICENSE) file for details.

Developed as part of an internship at OTLabs / iSquared.
