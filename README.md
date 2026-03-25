# AI-Powered Autonomous Web Testing & Intelligence

This repository houses a sophisticated ecosystem for autonomous website exploration, UI analysis, and automated test generation. The core of this system is the **Website Crawling Assistant**, supported by specialized modules for intelligent data extraction and interactive knowledge retrieval.

---

## 🎯 Primary Project: Website Crawling Assistant
The **Website Crawling Assistant** is an end-to-end engine designed to "understand" any website and automatically generate executable test suites. It moves beyond simple crawling by using AI to classify UI elements and map out user flows.

### 🏗️ Architecture & Core Components
- **The Voyager (Crawler)**: Located in `src/the_crawler.py`. Uses **Playwright** to recursively navigate through a target domain, capturing the structural DOM and visual state of every page.
- **The Analyst (UI Enricher)**: Found in `src/enrich_crawl_for_ai.py`. This component processes raw crawl data, stripping noise and classifying elements (Buttons, Inputs, Dropdowns) to create an "AI Snapshot" of the site's interaction surface.
- **The Architect (Test Generator)**: Comprises `src/ai_test_generator_grok.py` and `src/ai_step_generator.py`.
  - It uses LLMs to design logical test cases based on the site's UI density.
  - It then **deterministically generates Python code** for Gauge step implementations, ensuring 100% reliable execution.
- **The Validator**: `src/validator.py` ensures that the generated tests align with the actual discovered UI elements.

### 🛠️ Tech Stack
- **Automation**: Playwright, Gauge, Taiko.
- **Intelligence**: Grok API / Ollama (Local).
- **Core**: Python 3.8+, Node.js.

---

## 🛰️ Support Modules

To enable the primary engine's success, two specialized support modules provide foundational data and accessibility:

### 1. Intelligent Data Extraction (`selenium_ollama_scraper`)
**Role**: *Heavy-duty Scraping Foundation*
- Before the main crawler begins, this module can be used to perform deep-tissue scraping of complex, dynamic websites using **Selenium**.
- **AI-Powered Summarization**: Uses local models (like `codellama`) to generate per-page summaries, helping the main engine identify which paths are most critical for testing.
- **Outputs**: Generates structured JSON and human-readable TXT reports of the site's content.

### 2. Interactive Contextual AI (`Instant Support Agent`)
**Role**: *The Knowledge Interface*
- Once the Crawler has mapped a site, this module provides a **Retrieval-Augmented Generation (RAG)** interface for that data.
- **Support Interface**: Users can chat with the "learned" knowledge of the website. It uses **FAISS** index for lightning-fast retrieval and **LangChain** to ensure the AI only answers based on the crawled context.
- **Dual Interface**: Offers both a CLI and a **Streamlit** web app for interacting with the site's intelligence.

---

## 🚀 Getting Started

### Prerequisites
1. **Ollama (Local AI)**: Download from [ollama.com](https://ollama.com/).
   - Pull required models: `phi:latest`, `nomic-embed-text`, `codellama:7b-instruct`.
2. **Environment**: Ensure Python 3.8+ and Node.js are installed.

### Setup & Execution
Each component is designed to be modular. Follow these steps for a full end-to-end run:

1. **Initialize the Crawler**:
   ```bash
   cd "Website crawling assistant"
   npm install
   python src/the_crawler.py --url "https://your-target.com"
   ```
2. **Generate Tests**:
   ```bash
   python src/enrich_crawl_for_ai.py
   python src/ai_test_generator_grok.py
   python src/ai_step_generator.py
   ```
3. **Run the Test Suite**:
   ```bash
   gauge run specs/
   ```

---

> [!IMPORTANT]
> **Legacy Note**: Directories labeled `111` or `222` are experimental/duplicate versions. For current development and production-ready code, please use the root directories mentioned above.

*Developed as part of the I² OT Labs Internship Program.*
