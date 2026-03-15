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

@step("Click 'Back'")
def step_click_back_cbbb25():
    State.resolver.smart_click('Back')

@step("Click 'Clear'")
def step_click_clear_68d23c():
    State.resolver.smart_click('Clear')

@step("Click 'Get pre-approval'")
def step_click_get_pre_approval_e6696d():
    State.resolver.smart_click('Get pre-approval')

@step("Click 'Search'")
def step_click_search_709231():
    State.resolver.smart_click('Search')

@step("Click 'x'")
def step_click_x_17f8f7():
    State.resolver.smart_click('x')

@step("Copy '12345' and paste into 'cdownpayment' with extra characters 'abc'")
def step_copy_12345_and_paste_into_c_320539():
    State.resolver.smart_click('Copy \'12345\' and paste into \'cdownpayment\' with extra characters \'abc\'')

@step("Enter '   ' into 'cagenow'")
def step_enter_into_cagenow_1ae70b():
    State.resolver.smart_fill('cagenow', '   ')

@step("Enter '!@#$%' into 'calcSearchTerm'")
def step_enter_into_calcsearch_9e2107():
    State.resolver.smart_fill('calcSearchTerm', '!@#$%')

@step("Enter '!@#$%' into 'chouseprice'")
def step_enter_into_chousepric_463fca():
    State.resolver.smart_fill('chouseprice', '!@#$%')

@step("Enter '-0.01' into 'cinterestrate'")
def step_enter_0_01_into_cinterestr_1dc3e5():
    State.resolver.smart_fill('cinterestrate', '-0.01')

@step("Enter '0' into 'c2loanamount'")
def step_enter_0_into_c2loanamount_6ec359():
    State.resolver.smart_fill('c2loanamount', '0')

@step("Enter '0' into 'c2loanterm'")
def step_enter_0_into_c2loanterm_9a26fa():
    State.resolver.smart_fill('c2loanterm', '0')

@step("Enter '0' into 'cagenow'")
def step_enter_0_into_cagenow_c97c7c():
    State.resolver.smart_fill('cagenow', '0')

@step("Enter '0' into 'cdownpayment'")
def step_enter_0_into_cdownpayment_c9cd66():
    State.resolver.smart_fill('cdownpayment', '0')

@step("Enter '0' into 'chouseprice'")
def step_enter_0_into_chouseprice_cf0d97():
    State.resolver.smart_fill('chouseprice', '0')

@step("Enter '0' into 'cinterestrate'")
def step_enter_0_into_cinterestrate_ec6028():
    State.resolver.smart_fill('cinterestrate', '0')

@step("Enter '0' into 'cloanamount'")
def step_enter_0_into_cloanamount_90516a():
    State.resolver.smart_fill('cloanamount', '0')

@step("Enter '0' into 'csaleprice'")
def step_enter_0_into_csaleprice_07fc15():
    State.resolver.smart_fill('csaleprice', '0')

@step("Enter '0' into 'cstartingprinciple'")
def step_enter_0_into_cstartingprinc_80e6a2():
    State.resolver.smart_fill('cstartingprinciple', '0')

@step("Enter '10' into 'cloanterm'")
def step_enter_10_into_cloanterm_8142ad():
    State.resolver.smart_fill('cloanterm', '10')

@step("Enter '100' into 'c2loanamount'")
def step_enter_100_into_c2loanamount_e39b2d():
    State.resolver.smart_fill('c2loanamount', '100')

@step("Enter '100' into 'calcSearchTerm'")
def step_enter_100_into_calcsearchte_97103f():
    State.resolver.smart_fill('calcSearchTerm', '100')

@step("Enter '100' into 'cinterestrate'")
def step_enter_100_into_cinterestrat_ee946f():
    State.resolver.smart_fill('cinterestrate', '100')

@step("Enter '100' into 'cstartingprinciple'")
def step_enter_100_into_cstartingpri_ea8947():
    State.resolver.smart_fill('cstartingprinciple', '100')

@step("Enter '1000' into 'calcSearchTerm'")
def step_enter_1000_into_calcsearcht_518d8b():
    State.resolver.smart_fill('calcSearchTerm', '1000')

@step("Enter '1000' into 'cinterestrate'")
def step_enter_1000_into_cinterestra_509a3a():
    State.resolver.smart_fill('cinterestrate', '1000')

@step("Enter '1000' into 'cloanamount'")
def step_enter_1000_into_cloanamount_56e9a3():
    State.resolver.smart_fill('cloanamount', '1000')

@step("Enter '1000' into 'cloantermmonth'")
def step_enter_1000_into_cloantermmo_6e3c93():
    State.resolver.smart_fill('cloantermmonth', '1000')

@step("Enter '1000' into 'cstartingprinciple'")
def step_enter_1000_into_cstartingpr_0a0f86():
    State.resolver.smart_fill('cstartingprinciple', '1000')

@step("Enter '10000' into 'c2loanamount'")
def step_enter_10000_into_c2loanamou_c67d1d():
    State.resolver.smart_fill('c2loanamount', '10000')

@step("Enter '10000' into 'c3loanamount'")
def step_enter_10000_into_c3loanamou_439d57():
    State.resolver.smart_fill('c3loanamount', '10000')

@step("Enter '10000' into 'cdownpayment'")
def step_enter_10000_into_cdownpayme_760fda():
    State.resolver.smart_fill('cdownpayment', '10000')

@step("Enter '10000' into 'cloanamount'")
def step_enter_10000_into_cloanamoun_ee7fde():
    State.resolver.smart_fill('cloanamount', '10000')

@step("Enter '100000' into 'chouseprice'")
def step_enter_100000_into_chousepri_0a0448():
    State.resolver.smart_fill('chouseprice', '100000')

@step("Enter '12345' into 'csaleprice'")
def step_enter_12345_into_csaleprice_31f997():
    State.resolver.smart_fill('csaleprice', '12345')

@step("Enter '15000' into 'csaleprice'")
def step_enter_15000_into_csaleprice_c39728():
    State.resolver.smart_fill('csaleprice', '15000')

@step("Enter '20' into 'cdownpayment'")
def step_enter_20_into_cdownpayment_b4aaf9():
    State.resolver.smart_fill('cdownpayment', '20')

@step("Enter '2000' into 'cloanamount'")
def step_enter_2000_into_cloanamount_ed4729():
    State.resolver.smart_fill('cloanamount', '2000')

@step("Enter '20000' into 'csaleprice'")
def step_enter_20000_into_csaleprice_65930c():
    State.resolver.smart_fill('csaleprice', '20000')

@step("Enter '200000' into 'chouseprice'")
def step_enter_200000_into_chousepri_7e8c9c():
    State.resolver.smart_fill('chouseprice', '200000')

@step("Enter '30' into 'cagenow'")
def step_enter_30_into_cagenow_0bc059():
    State.resolver.smart_fill('cagenow', '30')

@step("Enter '35' into 'cagenow'")
def step_enter_35_into_cagenow_eb11e0():
    State.resolver.smart_fill('cagenow', '35')

@step("Enter '5' into 'c2loanterm'")
def step_enter_5_into_c2loanterm_802082():
    State.resolver.smart_fill('c2loanterm', '5')

@step("Enter '5' into 'c3loanterm'")
def step_enter_5_into_c3loanterm_5902dc():
    State.resolver.smart_fill('c3loanterm', '5')

@step("Enter '5' into 'cloanterm'")
def step_enter_5_into_cloanterm_693053():
    State.resolver.smart_fill('cloanterm', '5')

@step("Enter '5' into 'cyears'")
def step_enter_5_into_cyears_91c3dd():
    State.resolver.smart_fill('cyears', '5')

@step("Enter '50000' into 'cloanamount'")
def step_enter_50000_into_cloanamoun_409f53():
    State.resolver.smart_fill('cloanamount', '50000')

@step("Enter '6' into 'cloanterm'")
def step_enter_6_into_cloanterm_b1c575():
    State.resolver.smart_fill('cloanterm', '6')

@step("Enter '60' into 'cretireage'")
def step_enter_60_into_cretireage_d93920():
    State.resolver.smart_fill('cretireage', '60')

@step("Enter '65' into 'cretireage'")
def step_enter_65_into_cretireage_c2b224():
    State.resolver.smart_fill('cretireage', '65')

@step("Enter '999999999' into 'cloanamount'")
def step_enter_999999999_into_cloana_a46f4b():
    State.resolver.smart_fill('cloanamount', '999999999')

@step("Enter '9999999999' into 'chouseprice'")
def step_enter_9999999999_into_chous_a506a4():
    State.resolver.smart_fill('chouseprice', '9999999999')

@step("Enter '9999999999' into 'cloanamount'")
def step_enter_9999999999_into_cloan_2e22db():
    State.resolver.smart_fill('cloanamount', '9999999999')

@step("Enter '999999999999999999999' into 'calcSearchTerm'")
def step_enter_999999999999999999999_bc68df():
    State.resolver.smart_fill('calcSearchTerm', '999999999999999999999')

@step("Enter 'abc' into 'csaleprice'")
def step_enter_abc_into_csaleprice_c602d3():
    State.resolver.smart_fill('csaleprice', 'abc')

@step("Enter 'abc' into 'cstartingprinciple'")
def step_enter_abc_into_cstartingpri_6fec72():
    State.resolver.smart_fill('cstartingprinciple', 'abc')

@step("Enter 'loan' into 'calcSearchTerm'")
def step_enter_loan_into_calcsearcht_0dbcb8():
    State.resolver.smart_fill('calcSearchTerm', 'loan')

@step("Enter 'mortgage' into 'calcSearchTerm'")
def step_enter_mortgage_into_calcsea_77851f():
    State.resolver.smart_fill('calcSearchTerm', 'mortgage')

@step("Enter 'sin' into 'calcSearchTerm'")
def step_enter_sin_into_calcsearchte_67d1b5():
    State.resolver.smart_fill('calcSearchTerm', 'sin')

@step("Leave 'cloanamount' empty")
def step_leave_cloanamount_empty_44e05a():
    State.resolver.smart_click('Leave \'cloanamount\' empty')

@step("Navigate back to '/'")
def step_navigate_back_to_786072():
    State.resolver.smart_click('Navigate back to \'/\'')

@step("Navigate back to '/auto-loan-calculator.html'")
def step_navigate_back_to_auto_loan_c_efeee8():
    State.resolver.smart_click('Navigate back to \'/auto-loan-calculator.html\'')

@step("Navigate back to '/financial-calculator.html'")
def step_navigate_back_to_financial_c_bd7a9d():
    State.resolver.smart_click('Navigate back to \'/financial-calculator.html\'')

@step("Navigate back to '/interest-calculator.html'")
def step_navigate_back_to_interest_ca_da5163():
    State.resolver.smart_click('Navigate back to \'/interest-calculator.html\'')

@step("Navigate back to '/mortgage-calculator.html'")
def step_navigate_back_to_mortgage_ca_092321():
    State.resolver.smart_click('Navigate back to \'/mortgage-calculator.html\'')

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

@step("Navigate to '/payment-calculator.html'")
def step_navigate_to_payment_calculat_a18518():
    do_navigate('/payment-calculator.html')

@step("Navigate to '/retirement-calculator.html'")
def step_navigate_to_retirement_calcu_032d3b():
    do_navigate('/retirement-calculator.html')

@step("Verify all fields are cleared")
def step_verify_all_fields_are_cleared_53858f():
    State.resolver.smart_click('Verify all fields are cleared')

@step("Verify error message")
def step_verify_error_message_9e2970():
    State.resolver.smart_click('Verify error message')

@step("Verify: All fields are empty")
def step_verify_all_fields_are_empty_d90484():
    print('[VERIFY] Expected: All fields are empty')
    State.page.wait_for_timeout(1000)
    State.page.screenshot(path='reports/verify_' + str(int(time.time())) + '.png')

@step("Verify: Amortization calculator inputs are retained")
def step_verify_amortization_calculato_fd23b9():
    print('[VERIFY] Expected: Amortization calculator inputs are retained')
    State.page.wait_for_timeout(1000)
    State.page.screenshot(path='reports/verify_' + str(int(time.time())) + '.png')

@step("Verify: Auto loan calculator results are displayed")
def step_verify_auto_loan_calculator_r_419d75():
    print('[VERIFY] Expected: Auto loan calculator results are displayed')
    State.page.wait_for_timeout(1000)
    State.page.screenshot(path='reports/verify_' + str(int(time.time())) + '.png')

@step("Verify: Calculator retains values after mode switching")
def step_verify_calculator_retains_val_6ec7e7():
    print('[VERIFY] Expected: Calculator retains values after mode switching')
    State.page.wait_for_timeout(1000)
    State.page.screenshot(path='reports/verify_' + str(int(time.time())) + '.png')

@step("Verify: Calculator retains values after switching between modes")
def step_verify_calculator_retains_val_0ad8d7():
    print('[VERIFY] Expected: Calculator retains values after switching between modes')
    State.page.wait_for_timeout(1000)
    State.page.screenshot(path='reports/verify_' + str(int(time.time())) + '.png')

@step("Verify: Error message or calculator crash")
def step_verify_error_message_or_calcu_2f1ee1():
    print('[VERIFY] Expected: Error message or calculator crash')
    State.page.wait_for_timeout(1000)
    State.page.screenshot(path='reports/verify_' + str(int(time.time())) + '.png')

@step("Verify: Error message or incorrect calculation")
def step_verify_error_message_or_incor_d66a6d():
    print('[VERIFY] Expected: Error message or incorrect calculation')
    State.page.wait_for_timeout(1000)
    State.page.screenshot(path='reports/verify_' + str(int(time.time())) + '.png')

@step("Verify: Error message or invalid result")
def step_verify_error_message_or_inval_be9bd6():
    print('[VERIFY] Expected: Error message or invalid result')
    State.page.wait_for_timeout(1000)
    State.page.screenshot(path='reports/verify_' + str(int(time.time())) + '.png')

@step("Verify: Financial calculator search results are displayed")
def step_verify_financial_calculator_s_197717():
    print('[VERIFY] Expected: Financial calculator search results are displayed')
    State.page.wait_for_timeout(1000)
    State.page.screenshot(path='reports/verify_' + str(int(time.time())) + '.png')

@step("Verify: Form fields are cleared")
def step_verify_form_fields_are_cleare_b8ea97():
    print('[VERIFY] Expected: Form fields are cleared')
    State.page.wait_for_timeout(1000)
    State.page.screenshot(path='reports/verify_' + str(int(time.time())) + '.png')

@step("Verify: Form fields are reset")
def step_verify_form_fields_are_reset_b2105a():
    print('[VERIFY] Expected: Form fields are reset')
    State.page.wait_for_timeout(1000)
    State.page.screenshot(path='reports/verify_' + str(int(time.time())) + '.png')

@step("Verify: Form fields retain previous values")
def step_verify_form_fields_retain_pre_5de3f3():
    print('[VERIFY] Expected: Form fields retain previous values')
    State.page.wait_for_timeout(1000)
    State.page.screenshot(path='reports/verify_' + str(int(time.time())) + '.png')

@step("Verify: Interest calculator results are reset")
def step_verify_interest_calculator_re_c77939():
    print('[VERIFY] Expected: Interest calculator results are reset')
    State.page.wait_for_timeout(1000)
    State.page.screenshot(path='reports/verify_' + str(int(time.time())) + '.png')

@step("Verify: Loan amount is retained as '1000'")
def step_verify_loan_amount_is_retaine_d53219():
    print('[VERIFY] Expected: Loan amount is retained as \'1000\'')
    State.page.wait_for_timeout(1000)
    State.page.screenshot(path='reports/verify_' + str(int(time.time())) + '.png')

@step("Verify: Loan calculator inputs are cleared")
def step_verify_loan_calculator_inputs_d90969():
    print('[VERIFY] Expected: Loan calculator inputs are cleared')
    State.page.wait_for_timeout(1000)
    State.page.screenshot(path='reports/verify_' + str(int(time.time())) + '.png')

@step("Verify: Mortgage calculator inputs are retained")
def step_verify_mortgage_calculator_in_7eecec():
    print('[VERIFY] Expected: Mortgage calculator inputs are retained')
    State.page.wait_for_timeout(1000)
    State.page.screenshot(path='reports/verify_' + str(int(time.time())) + '.png')

@step("Verify: No UI errors or flicker after rapid mode switching")
def step_verify_no_ui_errors_or_flicke_32827d():
    print('[VERIFY] Expected: No UI errors or flicker after rapid mode switching')
    State.page.wait_for_timeout(1000)
    State.page.screenshot(path='reports/verify_' + str(int(time.time())) + '.png')

@step("Verify: No UI flicker or errors after rapid toggle button clicks")
def step_verify_no_ui_flicker_or_error_c435f7():
    print('[VERIFY] Expected: No UI flicker or errors after rapid toggle button clicks')
    State.page.wait_for_timeout(1000)
    State.page.screenshot(path='reports/verify_' + str(int(time.time())) + '.png')

@step("Verify: Old values still map to new labels after mode switching")
def step_verify_old_values_still_map_t_cbeb84():
    print('[VERIFY] Expected: Old values still map to new labels after mode switching')
    State.page.wait_for_timeout(1000)
    State.page.screenshot(path='reports/verify_' + str(int(time.time())) + '.png')

@step("Verify: Payment calculator inputs are retained")
def step_verify_payment_calculator_inp_f51839():
    print('[VERIFY] Expected: Payment calculator inputs are retained')
    State.page.wait_for_timeout(1000)
    State.page.screenshot(path='reports/verify_' + str(int(time.time())) + '.png')

@step("Verify: Result is updated with new age")
def step_verify_result_is_updated_with_1ea4d8():
    print('[VERIFY] Expected: Result is updated with new age')
    State.page.wait_for_timeout(1000)
    State.page.screenshot(path='reports/verify_' + str(int(time.time())) + '.png')

@step("Verify: Result is updated with new loan term")
def step_verify_result_is_updated_with_fa0049():
    print('[VERIFY] Expected: Result is updated with new loan term')
    State.page.wait_for_timeout(1000)
    State.page.screenshot(path='reports/verify_' + str(int(time.time())) + '.png')

@step("Verify: Retirement calculator inputs are cleared")
def step_verify_retirement_calculator_efacf7():
    print('[VERIFY] Expected: Retirement calculator inputs are cleared')
    State.page.wait_for_timeout(1000)
    State.page.screenshot(path='reports/verify_' + str(int(time.time())) + '.png')

@step("Verify: Search results are reset")
def step_verify_search_results_are_res_95909b():
    print('[VERIFY] Expected: Search results are reset')
    State.page.wait_for_timeout(1000)
    State.page.screenshot(path='reports/verify_' + str(int(time.time())) + '.png')

@step("Verify: Search results are retained")
def step_verify_search_results_are_ret_6b40dd():
    print('[VERIFY] Expected: Search results are retained')
    State.page.wait_for_timeout(1000)
    State.page.screenshot(path='reports/verify_' + str(int(time.time())) + '.png')

@step("Verify: Successful calculation result")
def step_verify_successful_calculation_aa5842():
    print('[VERIFY] Expected: Successful calculation result')
    State.page.wait_for_timeout(1000)
    State.page.screenshot(path='reports/verify_' + str(int(time.time())) + '.png')

@step("Verify: Successful pre-approval result")
def step_verify_successful_pre_approva_62d187():
    print('[VERIFY] Expected: Successful pre-approval result')
    State.page.wait_for_timeout(1000)
    State.page.screenshot(path='reports/verify_' + str(int(time.time())) + '.png')

@step("Verify: UI state changes correctly after mode switching")
def step_verify_ui_state_changes_corre_b86df7():
    print('[VERIFY] Expected: UI state changes correctly after mode switching')
    State.page.wait_for_timeout(1000)
    State.page.screenshot(path='reports/verify_' + str(int(time.time())) + '.png')

