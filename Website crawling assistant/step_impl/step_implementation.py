from getgauge.python import step, before_suite, after_suite
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
    print("\n[VISUAL MODE] Starting browser...")
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

@step("Copy and paste 'test@example.com ' with extra space into 'Your email'")
def step_copy_and_paste_test_example_c_157369():
    State.resolver.smart_click('Copy and paste \'test@example.com \' with extra space into \'Your email\'')

@step("Enter '   ' into 'Your email'")
def step_enter_into_your_email_46e276():
    State.resolver.smart_fill('Your email', '   ')

@step("Enter ' test@example.com ' into 'Your email'")
def step_enter_test_example_com_int_54d3a5():
    State.resolver.smart_fill('Your email', ' test@example.com ')

@step("Enter '!@#$%^&*()' into 'Your email'")
def step_enter_into_your_1e8f6b():
    State.resolver.smart_fill('Your email', '!@#$%^&*()')

@step("Enter '-1' into 'Your email'")
def step_enter_1_into_your_email_b48da7():
    State.resolver.smart_fill('Your email', '-1')

@step("Enter '0' into 'Your email'")
def step_enter_0_into_your_email_491b19():
    State.resolver.smart_fill('Your email', '0')

@step("Enter '0' into 'on'")
def step_enter_0_into_on_25da23():
    State.resolver.smart_fill('on', '0')

@step("Enter '0.0001' into 'Your email'")
def step_enter_0_0001_into_your_emai_556ebd():
    State.resolver.smart_fill('Your email', '0.0001')

@step("Enter '1' into 'Your email'")
def step_enter_1_into_your_email_39581d():
    State.resolver.smart_fill('Your email', '1')

@step("Enter '2147483647' into 'Your email'")
def step_enter_2147483647_into_your_dea1cb():
    State.resolver.smart_fill('Your email', '2147483647')

@step("Enter '2147483648' into 'Your email'")
def step_enter_2147483648_into_your_7f1b44():
    State.resolver.smart_fill('Your email', '2147483648')

@step("Enter '9999999999' into 'Your email'")
def step_enter_9999999999_into_your_f3ada5():
    State.resolver.smart_fill('Your email', '9999999999')

@step("Enter '9999999999' into 'on'")
def step_enter_9999999999_into_on_7acc06():
    State.resolver.smart_fill('on', '9999999999')

@step("Enter '999999999999999999999999999999999999999999999999999999999999999' into 'Your email'")
def step_enter_99999999999999999999999_7be92e():
    State.resolver.smart_fill('Your email', '999999999999999999999999999999999999999999999999999999999999999')

@step("Enter 'a' 256 times into 'Your email'")
def step_enter_a_256_times_into_your_b81729():
    State.resolver.smart_click('Enter \'a\' 256 times into \'Your email\'')

@step("Enter 'a' into 'Your email'")
def step_enter_a_into_your_email_92ba8b():
    State.resolver.smart_fill('Your email', 'a')

@step("Enter 'new@example.com' into 'Your email'")
def step_enter_new_example_com_into_00b8d8():
    State.resolver.smart_fill('Your email', 'new@example.com')

@step("Enter 'on' into 'on'")
def step_enter_on_into_on_717a9c():
    State.resolver.smart_fill('on', 'on')

@step("Enter 'test2@example.com' into 'Your email'")
def step_enter_test2_example_com_into_aaa4b8():
    State.resolver.smart_fill('Your email', 'test2@example.com')

@step("Enter 'test@example.com' into 'Your email'")
def step_enter_test_example_com_into_e6af81():
    State.resolver.smart_fill('Your email', 'test@example.com')

@step("Leave 'Your email' empty")
def step_leave_your_email_empty_5ae48c():
    State.resolver.smart_click('Leave \'Your email\' empty')

@step("Navigate back to '/'")
def step_navigate_back_to_786072():
    State.resolver.smart_click('Navigate back to \'/\'')

@step("Navigate back to '/login'")
def step_navigate_back_to_login_c1b103():
    State.resolver.smart_click('Navigate back to \'/login\'')

@step("Navigate back to '/register'")
def step_navigate_back_to_register_b10cd6():
    State.resolver.smart_click('Navigate back to \'/register\'')

@step("Navigate back to '/services'")
def step_navigate_back_to_services_579b43():
    State.resolver.smart_click('Navigate back to \'/services\'')

@step("Navigate back to '/services/weddings'")
def step_navigate_back_to_services_we_0a81fb():
    State.resolver.smart_click('Navigate back to \'/services/weddings\'')

@step("Navigate to '/'")
def step_navigate_to_380445():
    do_navigate('/')

@step("Navigate to '/about'")
def step_navigate_to_about_97ffc4():
    do_navigate('/about')

@step("Navigate to '/login'")
def step_navigate_to_login_4b49e6():
    do_navigate('/login')

@step("Navigate to '/register'")
def step_navigate_to_register_47a7d0():
    do_navigate('/register')

@step("Navigate to '/services'")
def step_navigate_to_services_8eccd6():
    do_navigate('/services')

@step("Navigate to '/services/weddings'")
def step_navigate_to_services_wedding_994342():
    do_navigate('/services/weddings')

@step("Verify: Email value retained")
def step_verify_email_value_retained_dbb26c():
    print('[VERIFY] Expected: Email value retained')
    State.page.wait_for_timeout(1000)
    State.page.screenshot(path='reports/verify_' + str(int(time.time())) + '.png')

@step("Verify: Error message or input field rejection")
def step_verify_error_message_or_input_9cc258():
    print('[VERIFY] Expected: Error message or input field rejection')
    State.page.wait_for_timeout(1000)
    State.page.screenshot(path='reports/verify_' + str(int(time.time())) + '.png')

@step("Verify: Error message or login failure")
def step_verify_error_message_or_login_128399():
    print('[VERIFY] Expected: Error message or login failure')
    State.page.wait_for_timeout(1000)
    State.page.screenshot(path='reports/verify_' + str(int(time.time())) + '.png')

@step("Verify: Form field is cleared")
def step_verify_form_field_is_cleared_d7554f():
    print('[VERIFY] Expected: Form field is cleared')
    State.page.wait_for_timeout(1000)
    State.page.screenshot(path='reports/verify_' + str(int(time.time())) + '.png')

@step("Verify: Form field is updated")
def step_verify_form_field_is_updated_a4e89e():
    print('[VERIFY] Expected: Form field is updated')
    State.page.wait_for_timeout(1000)
    State.page.screenshot(path='reports/verify_' + str(int(time.time())) + '.png')

@step("Verify: Form field retains value")
def step_verify_form_field_retains_val_ce7afc():
    print('[VERIFY] Expected: Form field retains value')
    State.page.wait_for_timeout(1000)
    State.page.screenshot(path='reports/verify_' + str(int(time.time())) + '.png')

@step("Verify: Form fields are cleared")
def step_verify_form_fields_are_cleare_b8ea97():
    print('[VERIFY] Expected: Form fields are cleared')
    State.page.wait_for_timeout(1000)
    State.page.screenshot(path='reports/verify_' + str(int(time.time())) + '.png')

@step("Verify: Form fields retain values")
def step_verify_form_fields_retain_val_520aee():
    print('[VERIFY] Expected: Form fields retain values')
    State.page.wait_for_timeout(1000)
    State.page.screenshot(path='reports/verify_' + str(int(time.time())) + '.png')

@step("Verify: Form submission fails")
def step_verify_form_submission_fails_733922():
    print('[VERIFY] Expected: Form submission fails')
    State.page.wait_for_timeout(1000)
    State.page.screenshot(path='reports/verify_' + str(int(time.time())) + '.png')

@step("Verify: Input field acceptance")
def step_verify_input_field_acceptance_88fab4():
    print('[VERIFY] Expected: Input field acceptance')
    State.page.wait_for_timeout(1000)
    State.page.screenshot(path='reports/verify_' + str(int(time.time())) + '.png')

@step("Verify: Labels change correctly")
def step_verify_labels_change_correctl_31f9b1():
    print('[VERIFY] Expected: Labels change correctly')
    State.page.wait_for_timeout(1000)
    State.page.screenshot(path='reports/verify_' + str(int(time.time())) + '.png')

@step("Verify: Login fails")
def step_verify_login_fails_0c8de9():
    print('[VERIFY] Expected: Login fails')
    State.page.wait_for_timeout(1000)
    State.page.screenshot(path='reports/verify_' + str(int(time.time())) + '.png')

@step("Verify: Login form resets")
def step_verify_login_form_resets_ba1d6e():
    print('[VERIFY] Expected: Login form resets')
    State.page.wait_for_timeout(1000)
    State.page.screenshot(path='reports/verify_' + str(int(time.time())) + '.png')

@step("Verify: Login page is displayed with previously entered email")
def step_verify_login_page_is_displaye_c6f2b1():
    print('[VERIFY] Expected: Login page is displayed with previously entered email')
    State.page.wait_for_timeout(1000)
    State.page.screenshot(path='reports/verify_' + str(int(time.time())) + '.png')

@step("Verify: Login page is displayed without errors")
def step_verify_login_page_is_displaye_bcb1fd():
    print('[VERIFY] Expected: Login page is displayed without errors')
    State.page.wait_for_timeout(1000)
    State.page.screenshot(path='reports/verify_' + str(int(time.time())) + '.png')

@step("Verify: Login page is re-displayed with previously entered email")
def step_verify_login_page_is_re_displ_e41f1c():
    print('[VERIFY] Expected: Login page is re-displayed with previously entered email')
    State.page.wait_for_timeout(1000)
    State.page.screenshot(path='reports/verify_' + str(int(time.time())) + '.png')

@step("Verify: No UI errors or crashes")
def step_verify_no_ui_errors_or_crashe_53d61d():
    print('[VERIFY] Expected: No UI errors or crashes')
    State.page.wait_for_timeout(1000)
    State.page.screenshot(path='reports/verify_' + str(int(time.time())) + '.png')

@step("Verify: No UI flicker or errors")
def step_verify_no_ui_flicker_or_error_b256a5():
    print('[VERIFY] Expected: No UI flicker or errors')
    State.page.wait_for_timeout(1000)
    State.page.screenshot(path='reports/verify_' + str(int(time.time())) + '.png')

@step("Verify: No duplicate submissions")
def step_verify_no_duplicate_submissio_29b9a3():
    print('[VERIFY] Expected: No duplicate submissions')
    State.page.wait_for_timeout(1000)
    State.page.screenshot(path='reports/verify_' + str(int(time.time())) + '.png')

@step("Verify: Register page is re-displayed with previously entered email")
def step_verify_register_page_is_re_di_965f8d():
    print('[VERIFY] Expected: Register page is re-displayed with previously entered email')
    State.page.wait_for_timeout(1000)
    State.page.screenshot(path='reports/verify_' + str(int(time.time())) + '.png')

@step("Verify: Registration form is populated with previously entered email")
def step_verify_registration_form_is_p_19175b():
    print('[VERIFY] Expected: Registration form is populated with previously entered email')
    State.page.wait_for_timeout(1000)
    State.page.screenshot(path='reports/verify_' + str(int(time.time())) + '.png')

@step("Verify: Services page has independent email input")
def step_verify_services_page_has_inde_fb20d4():
    print('[VERIFY] Expected: Services page has independent email input')
    State.page.wait_for_timeout(1000)
    State.page.screenshot(path='reports/verify_' + str(int(time.time())) + '.png')

@step("Verify: Services page is displayed with original email input")
def step_verify_services_page_is_displ_f3075a():
    print('[VERIFY] Expected: Services page is displayed with original email input')
    State.page.wait_for_timeout(1000)
    State.page.screenshot(path='reports/verify_' + str(int(time.time())) + '.png')

@step("Verify: Services page is displayed without errors")
def step_verify_services_page_is_displ_d23653():
    print('[VERIFY] Expected: Services page is displayed without errors')
    State.page.wait_for_timeout(1000)
    State.page.screenshot(path='reports/verify_' + str(int(time.time())) + '.png')

@step("Verify: State retained correctly")
def step_verify_state_retained_correct_423f18():
    print('[VERIFY] Expected: State retained correctly')
    State.page.wait_for_timeout(1000)
    State.page.screenshot(path='reports/verify_' + str(int(time.time())) + '.png')

@step("Verify: Weddings page has independent email input")
def step_verify_weddings_page_has_inde_3ebc5c():
    print('[VERIFY] Expected: Weddings page has independent email input')
    State.page.wait_for_timeout(1000)
    State.page.screenshot(path='reports/verify_' + str(int(time.time())) + '.png')

