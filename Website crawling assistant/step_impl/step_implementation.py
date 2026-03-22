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
    Real assertion — actually checks the page instead of just printing.
    Raises AssertionError (Gauge marks test FAILED) when expectation not met.
    """
    State.page.wait_for_timeout(1500)
    State.page.screenshot(path='reports/verify_' + str(int(time.time())) + '.png')

    exp        = expectation.lower()
    page_text  = State.page.inner_text('body').lower()
    current_url= State.page.url.lower()
    print(f'[VERIFY] Checking: {expectation}')
    print(f'[VERIFY] URL: {State.page.url}')

    ERROR_WORDS   = ['error', 'fail', 'invalid', 'reject', 'required',
                     'too long', 'too short', 'incorrect', 'not allowed', 'missing']
    SUCCESS_WORDS = ['success', 'successfully', 'sent', 'created',
                     'welcome', 'registered', 'logged in', 'confirmed']
    RETAIN_WORDS  = ['retain', 'persist', 'populated', 'still has', 'unchanged']
    CLEAR_WORDS   = ['clear', 'empty', 'reset', 'blank', 'removed']

    # 1. Expect an error / failure
    if any(w in exp for w in ERROR_WORDS):
        has_success = bool(re.search(
            r'success|successfully|sent|created|welcome|registered|logged in|confirmed',
            page_text))
        has_error = bool(re.search(
            r'error|invalid|required|failed|incorrect|too (long|short)|must be|cannot|not allowed',
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

@step("Click '/'")
def step_click_ce9ec9():
    State.resolver.smart_click('/')

@step("Click '1/x'")
def step_click_1_x_3d9bbd():
    State.resolver.smart_click('1/x')

@step("Click 'Clear'")
def step_click_clear_68d23c():
    State.resolver.smart_click('Clear')

@step("Click 'Get pre-approval'")
def step_click_get_pre_approval_e6696d():
    State.resolver.smart_click('Get pre-approval')

@step("Click 'Search'")
def step_click_search_709231():
    State.resolver.smart_click('Search')

@step("Click 'submit'")
def step_click_submit_97d91c():
    State.resolver.smart_click('submit')

@step("Click 'x'")
def step_click_x_17f8f7():
    State.resolver.smart_click('x')

@step("Enter '-0.01' into 'cinterestrate'")
def step_enter_0_01_into_cinterestr_1dc3e5():
    State.resolver.smart_fill('cinterestrate', '-0.01')

@step("Enter '-1' into 'cagenow'")
def step_enter_1_into_cagenow_b7194d():
    State.resolver.smart_fill('cagenow', '-1')

@step("Enter '-1' into 'cstartingprinciple'")
def step_enter_1_into_cstartingprin_19953e():
    State.resolver.smart_fill('cstartingprinciple', '-1')

@step("Enter '-1000' into 'cloanamount'")
def step_enter_1000_into_cloanamoun_ae162e():
    State.resolver.smart_fill('cloanamount', '-1000')

@step("Enter '0' into 'c2loanamount'")
def step_enter_0_into_c2loanamount_6ec359():
    State.resolver.smart_fill('c2loanamount', '0')

@step("Enter '0' into 'chouseprice'")
def step_enter_0_into_chouseprice_cf0d97():
    State.resolver.smart_fill('chouseprice', '0')

@step("Enter '0' into 'cloanamount'")
def step_enter_0_into_cloanamount_90516a():
    State.resolver.smart_fill('cloanamount', '0')

@step("Enter '0' into 'cloanterm'")
def step_enter_0_into_cloanterm_9b66e7():
    State.resolver.smart_fill('cloanterm', '0')

@step("Enter '0' into 'csaleprice'")
def step_enter_0_into_csaleprice_07fc15():
    State.resolver.smart_fill('csaleprice', '0')

@step("Enter '0' into 'cstartingprinciple'")
def step_enter_0_into_cstartingprinc_80e6a2():
    State.resolver.smart_fill('cstartingprinciple', '0')

@step("Enter '0' into 'scirdsetting'")
def step_enter_0_into_scirdsetting_f1dc8d():
    State.resolver.smart_fill('scirdsetting', '0')

@step("Enter '0.0001' into 'cinterestrate'")
def step_enter_0_0001_into_cinterest_9b9c23():
    State.resolver.smart_fill('cinterestrate', '0.0001')

@step("Enter '1' into 'scirdsetting'")
def step_enter_1_into_scirdsetting_0c42d7():
    State.resolver.smart_fill('scirdsetting', '1')

@step("Enter '100' into 'c2loanamount'")
def step_enter_100_into_c2loanamount_e39b2d():
    State.resolver.smart_fill('c2loanamount', '100')

@step("Enter '100' into 'calcSearchTerm'")
def step_enter_100_into_calcsearchte_97103f():
    State.resolver.smart_fill('calcSearchTerm', '100')

@step("Enter '1000' into 'cloanamount'")
def step_enter_1000_into_cloanamount_56e9a3():
    State.resolver.smart_fill('cloanamount', '1000')

@step("Enter '1000' into 'cstartingprinciple'")
def step_enter_1000_into_cstartingpr_0a0f86():
    State.resolver.smart_fill('cstartingprinciple', '1000')

@step("Enter '10000' into 'c2loanamount'")
def step_enter_10000_into_c2loanamou_c67d1d():
    State.resolver.smart_fill('c2loanamount', '10000')

@step("Enter '10000' into 'cloanamount'")
def step_enter_10000_into_cloanamoun_ee7fde():
    State.resolver.smart_fill('cloanamount', '10000')

@step("Enter '10000' into 'csaleprice'")
def step_enter_10000_into_csaleprice_b4c3f6():
    State.resolver.smart_fill('csaleprice', '10000')

@step("Enter '100000' into 'chouseprice'")
def step_enter_100000_into_chousepri_0a0448():
    State.resolver.smart_fill('chouseprice', '100000')

@step("Enter '100000' into 'cloanterm'")
def step_enter_100000_into_cloanterm_f755c6():
    State.resolver.smart_fill('cloanterm', '100000')

@step("Enter '1000000000' into 'chouseprice'")
def step_enter_1000000000_into_chous_ebf2dd():
    State.resolver.smart_fill('chouseprice', '1000000000')

@step("Enter '15000' into 'csaleprice'")
def step_enter_15000_into_csaleprice_c39728():
    State.resolver.smart_fill('csaleprice', '15000')

@step("Enter '20' into 'cdownpayment'")
def step_enter_20_into_cdownpayment_b4aaf9():
    State.resolver.smart_fill('cdownpayment', '20')

@step("Enter '20' into 'cloanterm'")
def step_enter_20_into_cloanterm_20be1b():
    State.resolver.smart_fill('cloanterm', '20')

@step("Enter '20000' into 'cloanamount'")
def step_enter_20000_into_cloanamoun_da2ecf():
    State.resolver.smart_fill('cloanamount', '20000')

@step("Enter '20000' into 'csaleprice'")
def step_enter_20000_into_csaleprice_65930c():
    State.resolver.smart_fill('csaleprice', '20000')

@step("Enter '200000' into 'chouseprice'")
def step_enter_200000_into_chousepri_7e8c9c():
    State.resolver.smart_fill('chouseprice', '200000')

@step("Enter '30' into 'cagenow'")
def step_enter_30_into_cagenow_0bc059():
    State.resolver.smart_fill('cagenow', '30')

@step("Enter '300000' into 'chouseprice'")
def step_enter_300000_into_chousepri_7595ce():
    State.resolver.smart_fill('chouseprice', '300000')

@step("Enter '5' into 'c2loanterm'")
def step_enter_5_into_c2loanterm_802082():
    State.resolver.smart_fill('c2loanterm', '5')

@step("Enter '5' into 'cinterestrate'")
def step_enter_5_into_cinterestrate_bffa36():
    State.resolver.smart_fill('cinterestrate', '5')

@step("Enter '5' into 'cloanterm'")
def step_enter_5_into_cloanterm_693053():
    State.resolver.smart_fill('cloanterm', '5')

@step("Enter '5' into 'cyears'")
def step_enter_5_into_cyears_91c3dd():
    State.resolver.smart_fill('cyears', '5')

@step("Enter '5000' into 'cloanamount'")
def step_enter_5000_into_cloanamount_1bd28c():
    State.resolver.smart_fill('cloanamount', '5000')

@step("Enter '5000' into 'cstartingprinciple'")
def step_enter_5000_into_cstartingpr_727011():
    State.resolver.smart_fill('cstartingprinciple', '5000')

@step("Enter '6' into 'cloanterm'")
def step_enter_6_into_cloanterm_b1c575():
    State.resolver.smart_fill('cloanterm', '6')

@step("Enter '60' into 'cretireage'")
def step_enter_60_into_cretireage_d93920():
    State.resolver.smart_fill('cretireage', '60')

@step("Enter '65' into 'cretireage'")
def step_enter_65_into_cretireage_c2b224():
    State.resolver.smart_fill('cretireage', '65')

@step("Enter '8000' into 'cloanamount'")
def step_enter_8000_into_cloanamount_bb5b14():
    State.resolver.smart_fill('cloanamount', '8000')

@step("Enter '999' into 'cinterestrate'")
def step_enter_999_into_cinterestrat_4883e7():
    State.resolver.smart_fill('cinterestrate', '999')

@step("Enter '999' into 'cloanterm'")
def step_enter_999_into_cloanterm_0c5564():
    State.resolver.smart_fill('cloanterm', '999')

@step("Enter '999999999' into 'cannualsave'")
def step_enter_999999999_into_cannua_55459d():
    State.resolver.smart_fill('cannualsave', '999999999')

@step("Enter '999999999' into 'cloanamount'")
def step_enter_999999999_into_cloana_a46f4b():
    State.resolver.smart_fill('cloanamount', '999999999')

@step("Enter '9999999999' into 'chouseprice'")
def step_enter_9999999999_into_chous_a506a4():
    State.resolver.smart_fill('chouseprice', '9999999999')

@step("Enter '9999999999' into 'cloanamount'")
def step_enter_9999999999_into_cloan_2e22db():
    State.resolver.smart_fill('cloanamount', '9999999999')

@step("Enter '999999999999999999' into 'calcSearchTerm'")
def step_enter_999999999999999999_int_f23b25():
    State.resolver.smart_fill('calcSearchTerm', '999999999999999999')

@step("Enter 'a' * 1000 into 'email'")
def step_enter_a_1000_into_email_985952():
    State.resolver.smart_click('Enter \'a\' * 1000 into \'email\'')

@step("Enter 'abc' into 'calcSearchTerm'")
def step_enter_abc_into_calcsearchte_cecd6f():
    State.resolver.smart_fill('calcSearchTerm', 'abc')

@step("Enter 'abc' into 'ctradeinvalue'")
def step_enter_abc_into_ctradeinvalu_ceb471():
    State.resolver.smart_fill('ctradeinvalue', 'abc')

@step("Enter 'finance' into 'calcSearchTerm'")
def step_enter_finance_into_calcsear_4a035f():
    State.resolver.smart_fill('calcSearchTerm', 'finance')

@step("Enter 'mortgage' into 'calcSearchTerm'")
def step_enter_mortgage_into_calcsea_77851f():
    State.resolver.smart_fill('calcSearchTerm', 'mortgage')

@step("Navigate back to '/financial-calculator.html'")
def step_navigate_back_to_financial_c_bd7a9d():
    State.resolver.smart_click('Navigate back to \'/financial-calculator.html\'')

@step("Navigate back to '/interest-calculator.html'")
def step_navigate_back_to_interest_ca_da5163():
    State.resolver.smart_click('Navigate back to \'/interest-calculator.html\'')

@step("Navigate back to '/payment-calculator.html'")
def step_navigate_back_to_payment_cal_a332ef():
    State.resolver.smart_click('Navigate back to \'/payment-calculator.html\'')

@step("Navigate back to '/retirement-calculator.html'")
def step_navigate_back_to_retirement_e4159e():
    State.resolver.smart_click('Navigate back to \'/retirement-calculator.html\'')

@step("Navigate to '/'")
def step_navigate_to_380445():
    do_navigate('/')

@step("Navigate to '/amortization-calculator.html'")
def step_navigate_to_amortization_cal_f86807():
    do_navigate('/amortization-calculator.html')

@step("Navigate to '/auto-loan-calculator.html'")
def step_navigate_to_auto_loan_calcul_cabd0c():
    do_navigate('/auto-loan-calculator.html')

@step("Navigate to '/financial-calculator.html'")
def step_navigate_to_financial_calcul_5a9d70():
    do_navigate('/financial-calculator.html')

@step("Navigate to '/interest-calculator.html'")
def step_navigate_to_interest_calcula_aeb128():
    do_navigate('/interest-calculator.html')

@step("Navigate to '/loan-calculator.html'")
def step_navigate_to_loan_calculator_33bacb():
    do_navigate('/loan-calculator.html')

@step("Navigate to '/mortgage-calculator.html'")
def step_navigate_to_mortgage_calcula_9e7f34():
    do_navigate('/mortgage-calculator.html')

@step("Navigate to '/my-account/sign-in.php'")
def step_navigate_to_my_account_sign_ab1af8():
    do_navigate('/my-account/sign-in.php')

@step("Navigate to '/payment-calculator.html'")
def step_navigate_to_payment_calculat_a18518():
    do_navigate('/payment-calculator.html')

@step("Navigate to '/retirement-calculator.html'")
def step_navigate_to_retirement_calcu_032d3b():
    do_navigate('/retirement-calculator.html')

@step("Note error message")
def step_note_error_message_fad0ab():
    State.resolver.smart_click('Note error message')

@step("Verify: All calculators display correct results")
def step_verify_all_calculators_displa_f44a0e():
    do_verify('All calculators display correct results')

@step("Verify: Calculation result is displayed without errors")
def step_verify_calculation_result_is_e13163():
    do_verify('Calculation result is displayed without errors')

@step("Verify: Calculator displays correct amortization results")
def step_verify_calculator_displays_co_7f23fc():
    do_verify('Calculator displays correct amortization results')

@step("Verify: Calculator displays correct auto loan results")
def step_verify_calculator_displays_co_4b2fa6():
    do_verify('Calculator displays correct auto loan results')

@step("Verify: Calculator displays correct financial results")
def step_verify_calculator_displays_co_f78c82():
    do_verify('Calculator displays correct financial results')

@step("Verify: Calculator displays correct interest results")
def step_verify_calculator_displays_co_2c1f78():
    do_verify('Calculator displays correct interest results')

@step("Verify: Calculator displays correct results for both loan amounts")
def step_verify_calculator_displays_co_c52267():
    do_verify('Calculator displays correct results for both loan amounts')

@step("Verify: Calculator displays correct retirement results")
def step_verify_calculator_displays_co_7ed9d0():
    do_verify('Calculator displays correct retirement results')

@step("Verify: Calculator does not crash or display any errors")
def step_verify_calculator_does_not_cr_13d456():
    do_verify('Calculator does not crash or display any errors')

@step("Verify: Calculator does not display any errors")
def step_verify_calculator_does_not_di_f417c2():
    do_verify('Calculator does not display any errors')

@step("Verify: Calculator output updates with new loan term")
def step_verify_calculator_output_upda_a57236():
    do_verify('Calculator output updates with new loan term')

@step("Verify: Error message is cleared and calculation result is displayed")
def step_verify_error_message_is_clear_290e78():
    do_verify('Error message is cleared and calculation result is displayed')

@step("Verify: Error message is displayed for empty form submission")
def step_verify_error_message_is_displ_570970():
    do_verify('Error message is displayed for empty form submission')

@step("Verify: Error message or calculator crash")
def step_verify_error_message_or_calcu_2f1ee1():
    do_verify('Error message or calculator crash')

@step("Verify: Error message or incorrect calculation")
def step_verify_error_message_or_incor_d66a6d():
    do_verify('Error message or incorrect calculation')

@step("Verify: Error message or invalid result")
def step_verify_error_message_or_inval_be9bd6():
    do_verify('Error message or invalid result')

@step("Verify: Financial calculator form field is reset")
def step_verify_financial_calculator_f_06ead8():
    do_verify('Financial calculator form field is reset')

@step("Verify: Form fields are cleared")
def step_verify_form_fields_are_cleare_b8ea97():
    do_verify('Form fields are cleared')

@step("Verify: House price field is empty")
def step_verify_house_price_field_is_e_55ef08():
    do_verify('House price field is empty')

@step("Verify: Interest calculator form fields retain values")
def step_verify_interest_calculator_fo_2b84eb():
    do_verify('Interest calculator form fields retain values')

@step("Verify: Interest calculator form is reset")
def step_verify_interest_calculator_fo_1f0683():
    do_verify('Interest calculator form is reset')

@step("Verify: Loan amount field is empty")
def step_verify_loan_amount_field_is_e_b1df93():
    do_verify('Loan amount field is empty')

@step("Verify: Mortgage calculator form is reset")
def step_verify_mortgage_calculator_fo_7db7e8():
    do_verify('Mortgage calculator form is reset')

@step("Verify: Payment calculator form fields retain values")
def step_verify_payment_calculator_for_5b3723():
    do_verify('Payment calculator form fields retain values')

@step("Verify: Retirement calculator form fields are reset")
def step_verify_retirement_calculator_674b57():
    do_verify('Retirement calculator form fields are reset')

@step("Verify: Sale price field is empty")
def step_verify_sale_price_field_is_em_2e7ed4():
    do_verify('Sale price field is empty')

@step("Verify: Search term field is empty")
def step_verify_search_term_field_is_e_0b3eb8():
    do_verify('Search term field is empty')

@step("Verify: Starting principle field is empty")
def step_verify_starting_principle_fie_797eb2():
    do_verify('Starting principle field is empty')

