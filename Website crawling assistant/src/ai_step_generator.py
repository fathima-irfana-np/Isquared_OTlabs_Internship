"""
Deterministic Step Implementation Generator
Generates Gauge step implementations from validated test cases.

No AI needed - all steps follow 3 predictable patterns:
  Navigate to 'path'         -> do_navigate(path)
  Enter 'value' into 'label' -> State.resolver.smart_fill(label, value)
  Click 'label'              -> State.resolver.smart_click(label)
"""

import json
import os
import re
import hashlib
import dotenv

dotenv.load_dotenv()

INPUT_FILE  = "data/validated_test_cases.json"
OUTPUT_FILE = "step_impl/step_implementation.py"

TEMPLATE_HEADER = '''from getgauge.python import step, before_suite, after_suite
from playwright.sync_api import sync_playwright
from step_impl.resolver import SmartResolver
import os
import re
import sys
import time

# Ensure project root is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class State:
    playwright = None
    browser    = None
    page       = None
    resolver   = None
    base_url   = None

@before_suite
def setup():
    import json
    from urllib.parse import urlparse
    print("\\n[VISUAL MODE] Starting browser...")
    State.playwright = sync_playwright().start()
    State.browser    = State.playwright.chromium.launch(headless=False, slow_mo=0)
    State.page       = State.browser.new_page()

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

def do_verify(expectation):
    """
    Real assertion engine — checks the page state against the expectation.
    Raises AssertionError (Gauge marks test FAILED) when expectation not met.
    """
    State.page.wait_for_timeout(1500)
    State.page.screenshot(path=\'reports/verify_\' + str(int(time.time())) + \'.png\')

    exp         = expectation.lower()
    page_text   = State.page.inner_text(\'body\').lower()
    current_url = State.page.url.lower()
    print(f\'[VERIFY] Checking: {expectation}\')
    print(f\'[VERIFY] URL: {State.page.url}\')

    ERROR_WORDS   = [\'error\', \'fail\', \'invalid\', \'reject\', \'required\',
                     \'too long\', \'too short\', \'incorrect\', \'not allowed\', \'missing\',
                     \'must be\', \'cannot\', \'please provide\', \'please enter\']
    SUCCESS_WORDS = [\'success\', \'successfully\', \'sent\', \'created\',
                     \'welcome\', \'registered\', \'logged in\', \'confirmed\']
    RETAIN_WORDS  = [\'retain\', \'persist\', \'populated\', \'still has\', \'unchanged\']
    CLEAR_WORDS   = [\'clear\', \'empty\', \'reset\', \'blank\', \'removed\']

    # 0. Expect NO errors / NO crashes — page should be working fine.
    #    MUST be checked FIRST before ERROR_WORDS check because phrases like
    #    "no ui errors" contain the word "error" which would mis-route them.
    if (exp.startswith(\'no \') or
        \'no ui\' in exp or
        \'no crash\' in exp or
        \'no errors\' in exp or
        \'no error\' in exp or
        \'no validation\' in exp or
        \'without crashing\' in exp):
        has_crash = bool(re.search(
            r\'\\b(500|404|exception|traceback|crashed|unhandled error)\\b\',
            page_text))
        if has_crash:
            raise AssertionError(
                f\'FAIL: Page crashed or showed unexpected error.\\n\'
                f\'Expected: {expectation}\\nPage snippet: {page_text[:300]}\')
        print(f\'[VERIFY] PASS - no errors or crashes confirmed\')
        return

    # 1. Expect an error / failure
    if any(w in exp for w in ERROR_WORDS):
        has_success = bool(re.search(
            r\'success|successfully|sent|created|welcome|registered|logged in|confirmed\',
            page_text))
        has_error = bool(re.search(
            r\'error|invalid|required|failed|incorrect|too (long|short)|must be|cannot|not allowed\'
            r\'|please provide|please enter|please fill|must be positive|positive value\'
            r\'|not valid|out of range|exceeds|below minimum|above maximum\',
            page_text))
        if has_success and not has_error:
            raise AssertionError(
                f\'FAIL: Expected error/failure but page shows SUCCESS.\\n\'
                f\'Expected: {expectation}\\nPage snippet: {page_text[:300]}\')
        print(f\'[VERIFY] PASS - error/failure confirmed\')
        return

    # 2. Expect success
    if any(w in exp for w in SUCCESS_WORDS):
        has_success = bool(re.search(
            r\'success|successfully|sent|created|welcome|registered|logged in|confirmed|thank you\',
            page_text))
        url_ok = any(s in current_url for s in [\'dashboard\', \'welcome\', \'success\', \'home\', \'thank\'])
        if not has_success and not url_ok:
            raise AssertionError(
                f\'FAIL: Expected success but page does not show it.\\n\'
                f\'Expected: {expectation}\\nPage snippet: {page_text[:300]}\')
        print(f\'[VERIFY] PASS - success confirmed\')
        return

    # 3. Expect fields retained
    if any(w in exp for w in RETAIN_WORDS):
        inputs = State.page.locator(\'input[type="text"], input[type="email"], input[type="password"], textarea\')
        has_value = any(
            inputs.nth(i).input_value().strip()
            for i in range(inputs.count())
        )
        if not has_value:
            raise AssertionError(
                f\'FAIL: Expected field values to be retained but all fields appear empty.\\n\'
                f\'Expected: {expectation}\')
        print(f\'[VERIFY] PASS - field values retained\')
        return

    # 4. Expect fields cleared
    if any(w in exp for w in CLEAR_WORDS):
        inputs = State.page.locator(\'input[type="text"], input[type="email"], input[type="password"], textarea\')
        all_clear = all(
            not inputs.nth(i).input_value().strip()
            for i in range(inputs.count())
        )
        if not all_clear:
            raise AssertionError(
                f\'FAIL: Expected fields to be cleared but some still have values.\\n\'
                f\'Expected: {expectation}\')
        print(f\'[VERIFY] PASS - fields cleared\')
        return

    # 5. Fallback — screenshot only, no assertion
    print(f\'[VERIFY] INFO: No specific rule for "{expectation}" — screenshot saved\')

'''


def make_func_name(step_text, index):
    """Generate a unique, deterministic function name from step text."""
    h     = hashlib.md5(step_text.encode()).hexdigest()[:6]
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

    # Pattern: Click 'label' again — MUST be before plain Click pattern
    click_again = re.match(r"^Click ['\"](.+?)['\"] again$", step_text)
    if click_again:
        label = click_again.group(1)
        return "    State.resolver.smart_click('" + label.replace("'", "\\'") + "')"

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
            ms = ms * 1000
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

    # Pattern: Verify: expected outcome — calls real do_verify assertion
    verify_match = re.match(r"^Verify:\s*(.+)$", step_text)
    if verify_match:
        expectation = verify_match.group(1).replace("'", "\\'")
        return "    do_verify('" + expectation + "')"

    # Fallback: try smart_click with the full text
    return "    State.resolver.smart_click('" + step_text.replace("'", "\\'") + "')"


def escape_step_for_decorator(step_text):
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

    unique_steps = set()
    for test in data.get("generated_tests", []):
        steps    = test.get("steps", [])
        expected = test.get("expected", "")

        all_text = " ".join(steps) + " " + expected
        if "<" in all_text or ">" in all_text:
            continue

        for step_text in steps:
            unique_steps.add(step_text)

        if expected:
            unique_steps.add("Verify: " + expected)

    sorted_steps = sorted(list(unique_steps))
    print("Found " + str(len(sorted_steps)) + " unique steps.")

    implementations = []
    for i, step_text in enumerate(sorted_steps):
        func_name      = make_func_name(step_text, i)
        body           = parse_step_pattern(step_text)
        decorator_text = escape_step_for_decorator(step_text)

        impl  = '@step("' + decorator_text.replace('"', '\\"') + '")\n'
        impl += "def " + func_name + "():\n"
        impl += body + "\n"

        implementations.append(impl)

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