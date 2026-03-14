import json
from pathlib import Path

INPUT_FILE = Path("data/validated_test_cases.json")
SPECS_DIR = Path("specs")

SPECS_DIR.mkdir(exist_ok=True)

with INPUT_FILE.open("r", encoding="utf-8") as f:
    data = json.load(f)

# Build Gauge spec
spec_content = "# AI Exploratory Tests\n"
skipped = 0

for test in data["generated_tests"]:
    steps = test.get("steps", [])
    expected = test.get("expected", "")
    goal = test.get("goal", "Untitled")
    test_id = test.get("id", "")

    # Skip tests with angle brackets (Gauge treats <text> as dynamic params)
    all_text = " ".join(steps) + " " + expected
    if "<" in all_text or ">" in all_text:
        skipped += 1
        continue

    spec_content += "\n## " + test_id + ": " + goal + "\n"
    for step in steps:
        spec_content += "* " + step + "\n"

    # Add expected result as a final Verify step
    if expected:
        spec_content += "* Verify: " + expected + "\n"

spec_file = SPECS_DIR / "ai_exploration.spec"
spec_file.write_text(spec_content, encoding="utf-8")

print("Gauge spec created:", spec_file)
if skipped:
    print("Skipped", skipped, "test(s) with angle brackets")

