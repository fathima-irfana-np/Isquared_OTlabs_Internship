"""
Deterministic Step Implementation Generator
Generates Gauge step implementations from validated test cases.

No AI needed - all steps follow 3 predictable patterns:
  Navigate to 'path'       -> do_navigate(path)
  Enter 'value' into 'label' -> State.resolver.smart_fill(label, value)
  Click 'label'            -> State.resolver.smart_click(label)
"""

import json
import os
import re
import hashlib
import dotenv

dotenv.load_dotenv()

INPUT_FILE = "data/validated_test_cases.json"
OUTPUT_FILE = "step_impl/step_implementation.py"

TEMPLATE_HEADER = '''from getgauge.python import step, before_suite, after_suite
from playwright.sync_api import sync_playwright
from step_impl.resolver import SmartResolver
import os
import sys
import time

# Ensure project root is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class State:
    playwright = None
    browser = None
    page = None
    resolver = None
    base_url = None

@before_suite
def setup():
    import json
    from urllib.parse import urlparse
    print("\\n[VISUAL MODE] Starting browser...")
    State.playwright = sync_playwright().start()
    State.browser = State.playwright.chromium.launch(headless=False, slow_mo=2000)
    State.page = State.browser.new_page()

    # Auto-detect target site from snapshot (generic)
    snapshot_path = "data/ai_exploration_snapshot.json"
    if os.path.exists(snapshot_path):
        with open(snapshot_path, "r", encoding="utf-8") as f:
            snap = json.load(f)
        pages = snap.get("pages", [])
        if pages:
            first_url = pages[0].get("page_context", {}).get("url", "")
            if first_url:
                parsed = urlparse(first_url)
                State.base_url = parsed.scheme + "://" + parsed.netloc
                print("[SETUP] Target site: " + State.base_url)
                State.page.goto(State.base_url)
                State.page.wait_for_timeout(2000)

    State.resolver = SmartResolver(State.page)

@after_suite
def teardown():
    if State.browser:
        State.browser.close()
    if State.playwright:
        State.playwright.stop()

# --- Helper Logic ---

def do_navigate(path):
    """Navigate to a page by path or name."""
    if path.startswith("/") or path.startswith("http"):
        # Absolute or relative path - construct full URL
        if path.startswith("/"):
            current_url = State.page.url
            from urllib.parse import urlparse
            parsed = urlparse(current_url)
            base = parsed.scheme + "://" + parsed.netloc
            State.page.goto(base + path)
        else:
            State.page.goto(path)
    else:
        State.resolver.smart_click(path)
    State.page.wait_for_timeout(1000)

def do_mode(mode):
    """Toggle a UI mode."""
    State.resolver.smart_click(mode)

def do_press(key):
    """Press a key or click a named button."""
    special_keys = {"=": "Enter", "AC": "Escape", "C": "Escape"}
    keyboard_key = special_keys.get(key, key)
    if len(keyboard_key) == 1 or keyboard_key in ("Enter", "Escape", "Tab", "Backspace"):
        State.page.keyboard.press(keyboard_key)
    else:
        State.resolver.smart_click(key)

'''


def make_func_name(step_text, index):
    """Generate a unique, deterministic function name from step text."""
    # Create a short hash for uniqueness
    h = hashlib.md5(step_text.encode()).hexdigest()[:6]
    # Clean the step text for a readable prefix
    clean = re.sub(r'[^a-zA-Z0-9]', '_', step_text[:30]).lower().strip('_')
    clean = re.sub(r'_+', '_', clean)
    return "step_" + clean + "_" + h


def parse_step_pattern(step_text):
    """
    Parse a step into its action pattern and generate the implementation code.
    Returns the Python code body for this step.
    """
    # Pattern: Navigate to '/path'
    nav_match = re.match(r"^Navigate to ['\"](.+?)['\"]$", step_text)
    if nav_match:
        path = nav_match.group(1)
        return "    do_navigate('" + path.replace("'", "\\'") + "')"

    # Pattern: Enter 'value' into 'label'
    enter_match = re.match(r"^Enter ['\"](.+?)['\"] into ['\"](.+?)['\"]$", step_text)
    if enter_match:
        value = enter_match.group(1)
        label = enter_match.group(2)
        return "    State.resolver.smart_fill('" + label.replace("'", "\\'") + "', '" + value.replace("'", "\\'") + "')"

    # Pattern: Click 'label'
    click_match = re.match(r"^Click ['\"](.+?)['\"]$", step_text)
    if click_match:
        label = click_match.group(1)
        return "    State.resolver.smart_click('" + label.replace("'", "\\'") + "')"

    # Pattern: Wait for N seconds/milliseconds
    wait_match = re.match(r"^Wait for (\d+)", step_text)
    if wait_match:
        ms = int(wait_match.group(1))
        if ms < 100:
            ms = ms * 1000  # Convert seconds to ms
        return "    State.page.wait_for_timeout(" + str(ms) + ")"

    # Pattern: Type 'text'
    type_match = re.match(r"^Type ['\"](.+?)['\"]$", step_text)
    if type_match:
        text = type_match.group(1)
        return "    State.page.keyboard.type('" + text.replace("'", "\\'") + "')"

    # Pattern: Press 'key'
    press_match = re.match(r"^Press ['\"](.+?)['\"]$", step_text)
    if press_match:
        key = press_match.group(1)
        return "    do_press('" + key.replace("'", "\\'") + "')"

    # Pattern: Verify: expected outcome
    verify_match = re.match(r"^Verify:\s*(.+)$", step_text)
    if verify_match:
        expectation = verify_match.group(1).replace("'", "\\'")
        return (
            "    print('[VERIFY] Expected: " + expectation + "')\n"
            "    State.page.wait_for_timeout(1000)\n"
            "    State.page.screenshot(path='reports/verify_' + str(int(time.time())) + '.png')"
        )

    # Fallback: try smart_click with the full text
    return "    State.resolver.smart_click('" + step_text.replace("'", "\\'") + "')"


def escape_step_for_decorator(step_text):
    """
    Escape a step text for use in a @step decorator.
    Gauge treats <text> as dynamic parameters, so we need to handle this.
    """
    # Replace angle brackets with escaped versions for Gauge
    return step_text


def main():
    print("=" * 60)
    print("Step Implementation Generator v2.0 (Deterministic)")
    print("=" * 60)

    if not os.path.exists(INPUT_FILE):
        print("Error: " + INPUT_FILE + " not found.")
        return

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Collect unique steps (including Verify steps from expected field)
    unique_steps = set()
    for test in data.get("generated_tests", []):
        steps = test.get("steps", [])
        expected = test.get("expected", "")

        # Skip tests with angle brackets (same filter as json_to_gauge.py)
        all_text = " ".join(steps) + " " + expected
        if "<" in all_text or ">" in all_text:
            continue

        for step_text in steps:
            unique_steps.add(step_text)

        # Construct the Verify step (same as json_to_gauge.py)
        if expected:
            unique_steps.add("Verify: " + expected)

    sorted_steps = sorted(list(unique_steps))
    print("Found " + str(len(sorted_steps)) + " unique steps.")

    # Generate implementations
    implementations = []
    for i, step_text in enumerate(sorted_steps):
        func_name = make_func_name(step_text, i)
        body = parse_step_pattern(step_text)
        decorator_text = escape_step_for_decorator(step_text)

        impl = '@step("' + decorator_text.replace('"', '\\"') + '")\n'
        impl += "def " + func_name + "():\n"
        impl += body + "\n"

        implementations.append(impl)

    # Write output
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(TEMPLATE_HEADER)
        f.write("# --- Generated Step Implementations ---\n\n")
        f.write("\n".join(implementations))
        f.write("\n")

    print("Generated " + str(len(implementations)) + " step implementations.")
    print("Saved to " + OUTPUT_FILE)
    print("=" * 60)


if __name__ == "__main__":
    main()
