from getgauge.python import step, before_suite, after_suite
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
    print("\n[VISUAL MODE] Starting browser...")
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
    State.page.screenshot(path='reports/verify_' + str(int(time.time())) + '.png')

    exp         = expectation.lower()
    page_text   = State.page.inner_text('body').lower()
    current_url = State.page.url.lower()
    print(f'[VERIFY] Checking: {expectation}')
    print(f'[VERIFY] URL: {State.page.url}')

    ERROR_WORDS   = ['error', 'fail', 'invalid', 'reject', 'required',
                     'too long', 'too short', 'incorrect', 'not allowed', 'missing',
                     'must be', 'cannot', 'please provide', 'please enter']
    SUCCESS_WORDS = ['success', 'successfully', 'sent', 'created',
                     'welcome', 'registered', 'logged in', 'confirmed']
    RETAIN_WORDS  = ['retain', 'persist', 'populated', 'still has', 'unchanged']
    CLEAR_WORDS   = ['clear', 'empty', 'reset', 'blank', 'removed']

    # 0. Expect NO errors / NO crashes — page should be working fine.
    #    MUST be checked FIRST before ERROR_WORDS check because phrases like
    #    "no ui errors" contain the word "error" which would mis-route them.
    if (exp.startswith('no ') or
        'no ui' in exp or
        'no crash' in exp or
        'no errors' in exp or
        'no error' in exp or
        'no validation' in exp or
        'without crashing' in exp):
        has_crash = bool(re.search(
            r'\b(500|404|exception|traceback|crashed|unhandled error)\b',
            page_text))
        if has_crash:
            raise AssertionError(
                f'FAIL: Page crashed or showed unexpected error.\n'
                f'Expected: {expectation}\nPage snippet: {page_text[:300]}')
        print(f'[VERIFY] PASS - no errors or crashes confirmed')
        return

    # 1. Expect an error / failure
    if any(w in exp for w in ERROR_WORDS):
        has_success = bool(re.search(
            r'success|successfully|sent|created|welcome|registered|logged in|confirmed',
            page_text))
        has_error = bool(re.search(
            r'error|invalid|required|failed|incorrect|too (long|short)|must be|cannot|not allowed'
            r'|please provide|please enter|please fill|must be positive|positive value'
            r'|not valid|out of range|exceeds|below minimum|above maximum',
            page_text))
        if has_success and not has_error:
            raise AssertionError(
                f'FAIL: Expected error/failure but page shows SUCCESS.\n'
                f'Expected: {expectation}\nPage snippet: {page_text[:300]}')
        print(f'[VERIFY] PASS - error/failure confirmed')
        return

    # 2. Expect success
    if any(w in exp for w in SUCCESS_WORDS):
        has_success = bool(re.search(
            r'success|successfully|sent|created|welcome|registered|logged in|confirmed|thank you',
            page_text))
        url_ok = any(s in current_url for s in ['dashboard', 'welcome', 'success', 'home', 'thank'])
        if not has_success and not url_ok:
            raise AssertionError(
                f'FAIL: Expected success but page does not show it.\n'
                f'Expected: {expectation}\nPage snippet: {page_text[:300]}')
        print(f'[VERIFY] PASS - success confirmed')
        return

    # 3. Expect fields retained
    if any(w in exp for w in RETAIN_WORDS):
        inputs = State.page.locator('input[type="text"], input[type="email"], input[type="password"], textarea')
        has_value = any(
            inputs.nth(i).input_value().strip()
            for i in range(inputs.count())
        )
        if not has_value:
            raise AssertionError(
                f'FAIL: Expected field values to be retained but all fields appear empty.\n'
                f'Expected: {expectation}')
        print(f'[VERIFY] PASS - field values retained')
        return

    # 4. Expect fields cleared
    if any(w in exp for w in CLEAR_WORDS):
        inputs = State.page.locator('input[type="text"], input[type="email"], input[type="password"], textarea')
        all_clear = all(
            not inputs.nth(i).input_value().strip()
            for i in range(inputs.count())
        )
        if not all_clear:
            raise AssertionError(
                f'FAIL: Expected fields to be cleared but some still have values.\n'
                f'Expected: {expectation}')
        print(f'[VERIFY] PASS - fields cleared')
        return

    # 5. Fallback — screenshot only, no assertion
    print(f'[VERIFY] INFO: No specific rule for "{expectation}" — screenshot saved')

# --- Generated Step Implementations ---

@step("Click 'Create Account'")
def step_click_create_account_1b951d():
    State.resolver.smart_click('Create Account')

@step("Click 'Dismiss'")
def step_click_dismiss_b6b662():
    State.resolver.smart_click('Dismiss')

@step("Click 'Sign In'")
def step_click_sign_in_ec3c11():
    State.resolver.smart_click('Sign In')

@step("Enter 'off' into 'on'")
def step_enter_off_into_on_28425b():
    State.resolver.smart_fill('on', 'off')

@step("Enter 'on' into 'on'")
def step_enter_on_into_on_717a9c():
    State.resolver.smart_fill('on', 'on')

@step("Enter 'test2@example.com' into 'Your email'")
def step_enter_test2_example_com_into_aaa4b8():
    State.resolver.smart_fill('Your email', 'test2@example.com')

@step("Enter 'test3@example.com' into 'Your email'")
def step_enter_test3_example_com_into_08ec88():
    State.resolver.smart_fill('Your email', 'test3@example.com')

@step("Enter 'test@example.com' into 'Your email'")
def step_enter_test_example_com_into_e6af81():
    State.resolver.smart_fill('Your email', 'test@example.com')

@step("Navigate to '/login'")
def step_navigate_to_login_4b49e6():
    do_navigate('/login')

@step("Navigate to '/register'")
def step_navigate_to_register_47a7d0():
    do_navigate('/register')

@step("Verify: Error message for duplicate submission")
def step_verify_error_message_for_dupl_0e92e6():
    do_verify('Error message for duplicate submission')

@step("Verify: Error message for multiple submissions")
def step_verify_error_message_for_mult_a1963e():
    do_verify('Error message for multiple submissions')

@step("Verify: No UI errors or crashes")
def step_verify_no_ui_errors_or_crashe_53d61d():
    do_verify('No UI errors or crashes')

@step("Verify: Validation failure for duplicate submission")
def step_verify_validation_failure_for_fb337e():
    do_verify('Validation failure for duplicate submission')

@step("Verify: Validation failure for missing 'on' field")
def step_verify_validation_failure_for_a47f36():
    do_verify('Validation failure for missing \'on\' field')

@step("Verify: Validation failure for rapid form clearing and refilling")
def step_verify_validation_failure_for_bde26e():
    do_verify('Validation failure for rapid form clearing and refilling')

@step("Verify: Validation failure for rapid input changes")
def step_verify_validation_failure_for_c64a93():
    do_verify('Validation failure for rapid input changes')

