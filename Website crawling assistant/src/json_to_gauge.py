import json
from pathlib import Path

INPUT_FILE = Path("data/generated_test_cases.json")
SPECS_DIR = Path("specs")

SPECS_DIR.mkdir(exist_ok=True)

# --- Read raw AI output ---
with INPUT_FILE.open("r", encoding="utf-8") as f:
    raw_text = f.read()

# --- Extract valid JSON block ---
start = raw_text.find("{")
end = raw_text.rfind("}") + 1

if start == -1 or end == -1:
    raise ValueError("No JSON object found in AI output")

clean_json = raw_text[start:end]

# --- Parse JSON safely ---
data = json.loads(clean_json)

# --- Convert to Gauge spec ---
spec_content = "# AI Generated UI Exploratory Tests\n\n"

for test in data["generated_tests"]:
    spec_content += f"## {test['goal']}\n\n"
    for step in test["steps"]:
        spec_content += f"* {step}\n"
    spec_content += "\n"

spec_file = SPECS_DIR / "ai_exploration.spec"
spec_file.write_text(spec_content, encoding="utf-8")

print(" Gauge spec created:", spec_file)
