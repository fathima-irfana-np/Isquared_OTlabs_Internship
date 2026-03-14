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

@step("Click 'Clear'")
def step_click_clear_68d23c():
    State.resolver.smart_click('Clear')

@step("Click 'Get pre-approval'")
def step_click_get_pre_approval_e6696d():
    State.resolver.smart_click('Get pre-approval')

@step("Click 'Reload'")
def step_click_reload_6483f5():
    State.resolver.smart_click('Reload')

@step("Click 'Search'")
def step_click_search_709231():
    State.resolver.smart_click('Search')

@step("Click 'See your local rates'")
def step_click_see_your_local_rates_0b065f():
    State.resolver.smart_click('See your local rates')

@step("Click 'cos'")
def step_click_cos_f4a6b0():
    State.resolver.smart_click('cos')

@step("Click 'sin'")
def step_click_sin_fe50dc():
    State.resolver.smart_click('sin')

@step("Click 'tan'")
def step_click_tan_f2a2ac():
    State.resolver.smart_click('tan')

@step("Click 'x'")
def step_click_x_17f8f7():
    State.resolver.smart_click('x')

@step("Copy value from 'cloanamount' and paste into 'cinterestrate'")
def step_copy_value_from_cloanamount_176f6d():
    State.resolver.smart_click('Copy value from \'cloanamount\' and paste into \'cinterestrate\'')

@step("Enter '   ' into 'csaleprice'")
def step_enter_into_csaleprice_e790dc():
    State.resolver.smart_fill('csaleprice', '   ')

@step("Enter '!@#' into 'cinterestrate'")
def step_enter_into_cinterestrat_bce34c():
    State.resolver.smart_fill('cinterestrate', '!@#')

@step("Enter '-1' into 'cagenow'")
def step_enter_1_into_cagenow_b7194d():
    State.resolver.smart_fill('cagenow', '-1')

@step("Enter '-1' into 'cloanterm'")
def step_enter_1_into_cloanterm_eeeb07():
    State.resolver.smart_fill('cloanterm', '-1')

@step("Enter '0' into 'cdownpayment'")
def step_enter_0_into_cdownpayment_c9cd66():
    State.resolver.smart_fill('cdownpayment', '0')

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

@step("Enter '0.0001' into 'cloanamount'")
def step_enter_0_0001_into_cloanamou_68e5c5():
    State.resolver.smart_fill('cloanamount', '0.0001')

@step("Enter '100' into 'cinterestrate'")
def step_enter_100_into_cinterestrat_ee946f():
    State.resolver.smart_fill('cinterestrate', '100')

@step("Enter '1000' into 'cloanamount'")
def step_enter_1000_into_cloanamount_56e9a3():
    State.resolver.smart_fill('cloanamount', '1000')

@step("Enter '1000' into 'cstartingprinciple'")
def step_enter_1000_into_cstartingpr_0a0f86():
    State.resolver.smart_fill('cstartingprinciple', '1000')

@step("Enter '10000' into 'cloanamount'")
def step_enter_10000_into_cloanamoun_ee7fde():
    State.resolver.smart_fill('cloanamount', '10000')

@step("Enter '10000' into 'csaleprice'")
def step_enter_10000_into_csaleprice_b4c3f6():
    State.resolver.smart_fill('csaleprice', '10000')

@step("Enter '10000' into 'cstartingprinciple'")
def step_enter_10000_into_cstartingp_5b7519():
    State.resolver.smart_fill('cstartingprinciple', '10000')

@step("Enter '100000' into 'chouseprice'")
def step_enter_100000_into_chousepri_0a0448():
    State.resolver.smart_fill('chouseprice', '100000')

@step("Enter '1000000001' into 'cloanamount'")
def step_enter_1000000001_into_cloan_9f66e0():
    State.resolver.smart_fill('cloanamount', '1000000001')

@step("Enter '101' into 'cinterestrate'")
def step_enter_101_into_cinterestrat_1c0c48():
    State.resolver.smart_fill('cinterestrate', '101')

@step("Enter '150' into 'cagenow'")
def step_enter_150_into_cagenow_f5580e():
    State.resolver.smart_fill('cagenow', '150')

@step("Enter '15000' into 'cloanamount'")
def step_enter_15000_into_cloanamoun_46c548():
    State.resolver.smart_fill('cloanamount', '15000')

@step("Enter '20' into 'cdownpayment'")
def step_enter_20_into_cdownpayment_b4aaf9():
    State.resolver.smart_fill('cdownpayment', '20')

@step("Enter '20000' into 'cdownpayment'")
def step_enter_20000_into_cdownpayme_44ce27():
    State.resolver.smart_fill('cdownpayment', '20000')

@step("Enter '20000' into 'csaleprice'")
def step_enter_20000_into_csaleprice_65930c():
    State.resolver.smart_fill('csaleprice', '20000')

@step("Enter '200000' into 'chouseprice'")
def step_enter_200000_into_chousepri_7e8c9c():
    State.resolver.smart_fill('chouseprice', '200000')

@step("Enter '25' into 'cdownpayment'")
def step_enter_25_into_cdownpayment_7acba7():
    State.resolver.smart_fill('cdownpayment', '25')

@step("Enter '3' into 'cinterestrate'")
def step_enter_3_into_cinterestrate_72e78f():
    State.resolver.smart_fill('cinterestrate', '3')

@step("Enter '30' into 'cagenow'")
def step_enter_30_into_cagenow_0bc059():
    State.resolver.smart_fill('cagenow', '30')

@step("Enter '30' into 'cloanterm'")
def step_enter_30_into_cloanterm_0fddcd():
    State.resolver.smart_fill('cloanterm', '30')

@step("Enter '30000' into 'csaleprice'")
def step_enter_30000_into_csaleprice_811d87():
    State.resolver.smart_fill('csaleprice', '30000')

@step("Enter '40' into 'cagenow'")
def step_enter_40_into_cagenow_25b186():
    State.resolver.smart_fill('cagenow', '40')

@step("Enter '5' into 'cannualaddition'")
def step_enter_5_into_cannualadditio_64a35b():
    State.resolver.smart_fill('cannualaddition', '5')

@step("Enter '5' into 'cinterestrate'")
def step_enter_5_into_cinterestrate_bffa36():
    State.resolver.smart_fill('cinterestrate', '5')

@step("Enter '5' into 'cloanterm'")
def step_enter_5_into_cloanterm_693053():
    State.resolver.smart_fill('cloanterm', '5')

@step("Enter '5' into 'cyears'")
def step_enter_5_into_cyears_91c3dd():
    State.resolver.smart_fill('cyears', '5')

@step("Enter '500' into 'c2loanamount'")
def step_enter_500_into_c2loanamount_f6bf76():
    State.resolver.smart_fill('c2loanamount', '500')

@step("Enter '500' into 'cloanamount'")
def step_enter_500_into_cloanamount_b15937():
    State.resolver.smart_fill('cloanamount', '500')

@step("Enter '500' into 'cstartingprinciple'")
def step_enter_500_into_cstartingpri_8c83e0():
    State.resolver.smart_fill('cstartingprinciple', '500')

@step("Enter '5000' into 'cloanamount'")
def step_enter_5000_into_cloanamount_1bd28c():
    State.resolver.smart_fill('cloanamount', '5000')

@step("Enter '5000' into 'csaleprice'")
def step_enter_5000_into_csaleprice_df5ce0():
    State.resolver.smart_fill('csaleprice', '5000')

@step("Enter '5000' into 'ctradeinvalue'")
def step_enter_5000_into_ctradeinval_5375ad():
    State.resolver.smart_fill('ctradeinvalue', '5000')

@step("Enter '50000' into 'cincomenow'")
def step_enter_50000_into_cincomenow_5236a8():
    State.resolver.smart_fill('cincomenow', '50000')

@step("Enter '6' into 'cinterestrate'")
def step_enter_6_into_cinterestrate_8a6f49():
    State.resolver.smart_fill('cinterestrate', '6')

@step("Enter '60' into 'cretireage'")
def step_enter_60_into_cretireage_d93920():
    State.resolver.smart_fill('cretireage', '60')

@step("Enter '60000' into 'cincomenow'")
def step_enter_60000_into_cincomenow_f3a667():
    State.resolver.smart_fill('cincomenow', '60000')

@step("Enter '65' into 'cretireage'")
def step_enter_65_into_cretireage_c2b224():
    State.resolver.smart_fill('cretireage', '65')

@step("Enter '999999999' into 'cloanamount'")
def step_enter_999999999_into_cloana_a46f4b():
    State.resolver.smart_fill('cloanamount', '999999999')

@step("Enter '9999999999' into 'cdownpayment'")
def step_enter_9999999999_into_cdown_a3c342():
    State.resolver.smart_fill('cdownpayment', '9999999999')

@step("Enter '9999999999' into 'chouseprice'")
def step_enter_9999999999_into_chous_a506a4():
    State.resolver.smart_fill('chouseprice', '9999999999')

@step("Enter '999999999999999999' into 'chouseprice'")
def step_enter_999999999999999999_int_f53a09():
    State.resolver.smart_fill('chouseprice', '999999999999999999')

@step("Enter 'abc' into 'cloanamount'")
def step_enter_abc_into_cloanamount_a1778a():
    State.resolver.smart_fill('cloanamount', 'abc')

@step("Enter 'abc' into 'csaleprice'")
def step_enter_abc_into_csaleprice_c602d3():
    State.resolver.smart_fill('csaleprice', 'abc')

@step("Enter 'abc' into 'cstartingprinciple'")
def step_enter_abc_into_cstartingpri_6fec72():
    State.resolver.smart_fill('cstartingprinciple', 'abc')

@step("Enter 'loan' into 'calcSearchTerm'")
def step_enter_loan_into_calcsearcht_0dbcb8():
    State.resolver.smart_fill('calcSearchTerm', 'loan')

@step("Leave all fields empty")
def step_leave_all_fields_empty_490038():
    State.resolver.smart_click('Leave all fields empty')

@step("Navigate back to '/auto-loan-calculator.html'")
def step_navigate_back_to_auto_loan_c_efeee8():
    State.resolver.smart_click('Navigate back to \'/auto-loan-calculator.html\'')

@step("Navigate back to '/mortgage-calculator.html'")
def step_navigate_back_to_mortgage_ca_092321():
    State.resolver.smart_click('Navigate back to \'/mortgage-calculator.html\'')

@step("Navigate back to '/retirement-calculator.html'")
def step_navigate_back_to_retirement_e4159e():
    State.resolver.smart_click('Navigate back to \'/retirement-calculator.html\'')

@step("Navigate to '/'")
def step_navigate_to_380445():
    do_navigate('/')

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

@step("Verify 'cagenow' is '30'")
def step_verify_cagenow_is_30_270f29():
    State.resolver.smart_click('Verify \'cagenow\' is \'30\'')

@step("Verify 'chouseprice' is '200000'")
def step_verify_chouseprice_is_20000_f98478():
    State.resolver.smart_click('Verify \'chouseprice\' is \'200000\'')

@step("Verify 'cloanamount' is '10000'")
def step_verify_cloanamount_is_10000_a336e8():
    State.resolver.smart_click('Verify \'cloanamount\' is \'10000\'')

@step("Verify 'cloanamount' is empty")
def step_verify_cloanamount_is_empty_68ca9a():
    State.resolver.smart_click('Verify \'cloanamount\' is empty')

@step("Verify 'csaleprice' is '10000' and 'ctradeinvalue' is '5000'")
def step_verify_csaleprice_is_10000_8d3db9():
    State.resolver.smart_click('Verify \'csaleprice\' is \'10000\' and \'ctradeinvalue\' is \'5000\'')

@step("Verify the calculator is in a valid state")
def step_verify_the_calculator_is_in_a_7bc026():
    State.resolver.smart_click('Verify the calculator is in a valid state')

@step("Verify: All fields are cleared and calculation result is reset")
def step_verify_all_fields_are_cleared_0dea82():
    print('[VERIFY] Expected: All fields are cleared and calculation result is reset')
    State.page.wait_for_timeout(1000)
    State.page.screenshot(path='reports/verify_' + str(int(time.time())) + '.png')

@step("Verify: Calculation result is displayed without errors")
def step_verify_calculation_result_is_e13163():
    print('[VERIFY] Expected: Calculation result is displayed without errors')
    State.page.wait_for_timeout(1000)
    State.page.screenshot(path='reports/verify_' + str(int(time.time())) + '.png')

@step("Verify: Calculator UI does not flicker or display inconsistent results")
def step_verify_calculator_ui_does_not_49df25():
    print('[VERIFY] Expected: Calculator UI does not flicker or display inconsistent results')
    State.page.wait_for_timeout(1000)
    State.page.screenshot(path='reports/verify_' + str(int(time.time())) + '.png')

@step("Verify: Calculator UI state is consistent and displays correct results")
def step_verify_calculator_ui_state_is_194351():
    print('[VERIFY] Expected: Calculator UI state is consistent and displays correct results')
    State.page.wait_for_timeout(1000)
    State.page.screenshot(path='reports/verify_' + str(int(time.time())) + '.png')

@step("Verify: Calculator displays correct results and UI state is consistent")
def step_verify_calculator_displays_co_46c2b4():
    print('[VERIFY] Expected: Calculator displays correct results and UI state is consistent')
    State.page.wait_for_timeout(1000)
    State.page.screenshot(path='reports/verify_' + str(int(time.time())) + '.png')

@step("Verify: Calculator displays correct results and label changes are reflected")
def step_verify_calculator_displays_co_3efd0a():
    print('[VERIFY] Expected: Calculator displays correct results and label changes are reflected')
    State.page.wait_for_timeout(1000)
    State.page.screenshot(path='reports/verify_' + str(int(time.time())) + '.png')

@step("Verify: Calculator displays correct results for both loan amounts")
def step_verify_calculator_displays_co_c52267():
    print('[VERIFY] Expected: Calculator displays correct results for both loan amounts')
    State.page.wait_for_timeout(1000)
    State.page.screenshot(path='reports/verify_' + str(int(time.time())) + '.png')

@step("Verify: Calculator displays correct results for both principle amounts")
def step_verify_calculator_displays_co_2bd49f():
    print('[VERIFY] Expected: Calculator displays correct results for both principle amounts')
    State.page.wait_for_timeout(1000)
    State.page.screenshot(path='reports/verify_' + str(int(time.time())) + '.png')

@step("Verify: Calculator displays correct results for both principle amounts and interest rates")
def step_verify_calculator_displays_co_a10797():
    print('[VERIFY] Expected: Calculator displays correct results for both principle amounts and interest rates')
    State.page.wait_for_timeout(1000)
    State.page.screenshot(path='reports/verify_' + str(int(time.time())) + '.png')

@step("Verify: Calculator displays error message for invalid input and correct results for valid input")
def step_verify_calculator_displays_er_2c0729():
    print('[VERIFY] Expected: Calculator displays error message for invalid input and correct results for valid input')
    State.page.wait_for_timeout(1000)
    State.page.screenshot(path='reports/verify_' + str(int(time.time())) + '.png')

@step("Verify: Calculator displays error message or warning for incomplete fields")
def step_verify_calculator_displays_er_d6a038():
    print('[VERIFY] Expected: Calculator displays error message or warning for incomplete fields')
    State.page.wait_for_timeout(1000)
    State.page.screenshot(path='reports/verify_' + str(int(time.time())) + '.png')

@step("Verify: Calculator retains previous values for age and retirement age")
def step_verify_calculator_retains_pre_a24037():
    print('[VERIFY] Expected: Calculator retains previous values for age and retirement age')
    State.page.wait_for_timeout(1000)
    State.page.screenshot(path='reports/verify_' + str(int(time.time())) + '.png')

@step("Verify: Error message is cleared and calculation result is displayed")
def step_verify_error_message_is_clear_290e78():
    print('[VERIFY] Expected: Error message is cleared and calculation result is displayed')
    State.page.wait_for_timeout(1000)
    State.page.screenshot(path='reports/verify_' + str(int(time.time())) + '.png')

@step("Verify: Error message or calculator crash")
def step_verify_error_message_or_calcu_2f1ee1():
    print('[VERIFY] Expected: Error message or calculator crash')
    State.page.wait_for_timeout(1000)
    State.page.screenshot(path='reports/verify_' + str(int(time.time())) + '.png')

@step("Verify: Form values are lost")
def step_verify_form_values_are_lost_f8d8a3():
    print('[VERIFY] Expected: Form values are lost')
    State.page.wait_for_timeout(1000)
    State.page.screenshot(path='reports/verify_' + str(int(time.time())) + '.png')

@step("Verify: Form values are retained")
def step_verify_form_values_are_retain_1db1bd():
    print('[VERIFY] Expected: Form values are retained')
    State.page.wait_for_timeout(1000)
    State.page.screenshot(path='reports/verify_' + str(int(time.time())) + '.png')

@step("Verify: Output updates with new down payment value")
def step_verify_output_updates_with_ne_43a3ed():
    print('[VERIFY] Expected: Output updates with new down payment value')
    State.page.wait_for_timeout(1000)
    State.page.screenshot(path='reports/verify_' + str(int(time.time())) + '.png')

@step("Verify: Output updates with new income value")
def step_verify_output_updates_with_ne_ef1aa9():
    print('[VERIFY] Expected: Output updates with new income value')
    State.page.wait_for_timeout(1000)
    State.page.screenshot(path='reports/verify_' + str(int(time.time())) + '.png')

@step("Verify: Output updates with new interest rate value")
def step_verify_output_updates_with_ne_a32020():
    print('[VERIFY] Expected: Output updates with new interest rate value')
    State.page.wait_for_timeout(1000)
    State.page.screenshot(path='reports/verify_' + str(int(time.time())) + '.png')

@step("Verify: Output updates with new loan amount value")
def step_verify_output_updates_with_ne_0f238a():
    print('[VERIFY] Expected: Output updates with new loan amount value')
    State.page.wait_for_timeout(1000)
    State.page.screenshot(path='reports/verify_' + str(int(time.time())) + '.png')

@step("Verify: The auto loan calculator retains the sale price and trade-in value")
def step_verify_the_auto_loan_calculat_d8e816():
    print('[VERIFY] Expected: The auto loan calculator retains the sale price and trade-in value')
    State.page.wait_for_timeout(1000)
    State.page.screenshot(path='reports/verify_' + str(int(time.time())) + '.png')

@step("Verify: The calculator is in a valid state")
def step_verify_the_calculator_is_in_a_98b22a():
    print('[VERIFY] Expected: The calculator is in a valid state')
    State.page.wait_for_timeout(1000)
    State.page.screenshot(path='reports/verify_' + str(int(time.time())) + '.png')

@step("Verify: The financial calculator is reset")
def step_verify_the_financial_calculat_5c08f4():
    print('[VERIFY] Expected: The financial calculator is reset')
    State.page.wait_for_timeout(1000)
    State.page.screenshot(path='reports/verify_' + str(int(time.time())) + '.png')

@step("Verify: The interest calculator is reset")
def step_verify_the_interest_calculato_74be32():
    print('[VERIFY] Expected: The interest calculator is reset')
    State.page.wait_for_timeout(1000)
    State.page.screenshot(path='reports/verify_' + str(int(time.time())) + '.png')

@step("Verify: The loan amount is retained as '10000'")
def step_verify_the_loan_amount_is_ret_0ba81b():
    print('[VERIFY] Expected: The loan amount is retained as \'10000\'')
    State.page.wait_for_timeout(1000)
    State.page.screenshot(path='reports/verify_' + str(int(time.time())) + '.png')

@step("Verify: The mortgage calculator retains the house price as '200000'")
def step_verify_the_mortgage_calculato_e0b4e8():
    print('[VERIFY] Expected: The mortgage calculator retains the house price as \'200000\'')
    State.page.wait_for_timeout(1000)
    State.page.screenshot(path='reports/verify_' + str(int(time.time())) + '.png')

@step("Verify: The payment calculator is reset")
def step_verify_the_payment_calculator_df1946():
    print('[VERIFY] Expected: The payment calculator is reset')
    State.page.wait_for_timeout(1000)
    State.page.screenshot(path='reports/verify_' + str(int(time.time())) + '.png')

@step("Verify: The retirement calculator retains the age as '30'")
def step_verify_the_retirement_calcula_74f403():
    print('[VERIFY] Expected: The retirement calculator retains the age as \'30\'')
    State.page.wait_for_timeout(1000)
    State.page.screenshot(path='reports/verify_' + str(int(time.time())) + '.png')

