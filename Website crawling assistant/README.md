# 🕷️ AI-Powered Exploratory Test Generator

An automated pipeline that **crawls any website**, uses **AI to generate adversarial test cases**, validates them against the real UI, and produces **executable Gauge test specs** with Playwright — all with a 3-layer anti-hallucination defense.

---

## 📋 Table of Contents

- [How It Works](#how-it-works)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Pipeline](#running-the-pipeline)
- [Running Tests with Gauge](#running-tests-with-gauge)
- [Project Structure](#project-structure)
- [Output Files](#output-files)

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
|-----------|-----------|
| Web Crawling | Selenium WebDriver (headless Chrome) |
| AI / LLM | Groq API (`llama-3.3-70b-versatile`) |
| Test Framework | [Gauge](https://gauge.org/) |
| Browser Automation | [Playwright](https://playwright.dev/python/) |
| PDF Reports | fpdf2 |
| Language | Python 3.10+ |

---

## Prerequisites

- **Python 3.10+**
- **Node.js** (for Gauge)
- **Google Chrome** (for Selenium crawling)
- **Gauge** — install from [gauge.org](https://gauge.org/get-started/)
- **Groq API Key** — get one from [console.groq.com](https://console.groq.com/)

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/website-crawling-assistant.git
cd website-crawling-assistant
```

### 2. Create and activate a Python virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
pip install selenium fpdf2 python-dotenv
```

### 4. Install Playwright browsers

```bash
playwright install chromium
```

### 5. Install Gauge and plugins

```bash
# Install Gauge (if not already installed)
npm install -g @getgauge/cli

# Install Gauge plugins
gauge install python
gauge install html-report
```

### 6. Install Node dependencies

```bash
npm install
```

---

## Configuration

Create a `.env` file inside the `src/` directory:

```env
GROQ_API_KEY=your_groq_api_key_here
```

---

## Running the Pipeline

### Option A: Run Each Stage Individually (Recommended for first run)

```bash
# Stage 1: Crawl the website
# You will be prompted for: URL, max depth, max pages
python src/the_crawler.py

# Stage 2: Enrich crawl data for AI consumption
python src/enrich_crawl_for_ai.py

# Stage 3: Generate test cases using AI (takes ~5 mins due to rate limiting)
python src/ai_test_generator_grok.py

# Stage 4: Validate generated tests against the snapshot
python src/validator.py

# Stage 5: Convert validated tests to Gauge spec format
python src/json_to_gauge.py

# Stage 6: Generate step implementations
python src/ai_step_generator.py

# Stage 7: Generate PDF report
python src/report_generator.py
```

### Option B: Run Stages 4–6 via Pipeline Script

If you already have crawl data and generated tests:

```bash
python src/run_tester.py
```

This runs the validation → Gauge conversion → step generation pipeline.

---

## Running Tests with Gauge

After the pipeline has generated the spec and step implementations:

```bash
# Run all generated tests
gauge run specs/

# Run a specific spec file
gauge run specs/ai_exploration.spec
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
│   └── .env                      # API keys (not committed)
├── step_impl/
│   ├── step_implementation.py    # Auto-generated Playwright step code
│   ├── resolver.py               # SmartResolver — heuristic element finder
│   └── __init__.py
├── specs/
│   └── ai_exploration.spec       # Auto-generated Gauge test scenarios
├── data/                         # Pipeline intermediate data files
├── reports/                      # Generated PDF reports
├── manifest.json                 # Gauge project configuration
├── package.json                  # Node.js dependencies
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

## License

This project is licensed under the **Apache License 2.0** — see the [LICENSE](LICENSE) file for details.

Developed as part of an internship at OTLabs / iSquared.
