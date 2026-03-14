import subprocess
import sys
from pathlib import Path

PYTHON = sys.executable
BASE_DIR = Path(__file__).parent

# print("STEP 1: Crawling site")
# subprocess.run([PYTHON, BASE_DIR / "the_crawler.py"], check=True)

# print("STEP 2: Enriching crawl results")
# subprocess.run([PYTHON, BASE_DIR / "enrich_crawl_for_ai.py"], check=True)

# print("STEP 3: Generating test cases using AI")
# subprocess.run([PYTHON, BASE_DIR / "ai_test_generator_grok.py"], check=True)

print("STEP 4: Validating and deduplicating test cases")
subprocess.run([PYTHON, BASE_DIR / "validator.py"], check=True)

print("STEP 5: Converting AI test cases JSON to Gauge specs")
subprocess.run([PYTHON, BASE_DIR / "json_to_gauge.py"], check=True)

print("STEP 6: Generating step implementations using AI")
subprocess.run([PYTHON, BASE_DIR / "ai_step_generator.py"], check=True)

print("Pipeline complete.")
print("Gauge specs generated in /specs, and implementations updated in /step_impl")