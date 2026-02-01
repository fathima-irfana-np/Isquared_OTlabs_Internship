from getgauge.python import step, before_suite, after_suite
from playwright.sync_api import sync_playwright
from step_impl.resolver import SmartResolver
import os

class State:
    playwright = None
    browser = None
    page = None
    resolver = None

@before_suite
def setup():
    State.playwright = sync_playwright().start()
    State.browser = State.playwright.chromium.launch(headless=True)
    State.page = State.browser.new_page()
    State.resolver = SmartResolver(State.page)

@after_suite
def teardown():
    if State.browser:
        State.browser.close()
    if State.playwright:
        State.playwright.stop()

# --- Intent-Driven Mappings (Using SmartResolver) ---

@step("Navigate to the Scientific Calculator page")
def nav_sci():
    State.page.goto("https://www.calculator.net/scientific-calculator.html")

@step("Navigate to the BMI Calculator page")
def nav_bmi():
    State.page.goto("https://www.calculator.net/bmi-calculator.html")

@step("Navigate to the Math Calculators page")
def nav_math():
    State.page.goto("https://www.calculator.net/math-calculator.html")

@step("Ensure calculator is in degree mode")
def deg_mode():
    State.resolver.smart_click("Deg")

@step("Enter sin(90)")
def enter_sin_90_intent():
    State.page.keyboard.type("sin(90)")

@step("Enter sin(90) again")
def enter_sin_90_again_intent():
    State.page.keyboard.type("sin(90)")

@step("Enter invalid input (e.g. 'abc')")
def enter_invalid():
    State.page.keyboard.type("abc")

@step("Navigate to the BMI Calculator page while input is still present")
def nav_bmi_with_input():
    State.page.goto("https://www.calculator.net/bmi-calculator.html")

@step("Interact with the Search button while input is still present")
def interact_search():
    State.resolver.smart_click("Search")

@step("Toggle calculator mode to radian without clearing input")
def toggle_rad():
    State.resolver.smart_click("Rad")

@step("Toggle calculator mode to degree without clearing input")
def toggle_deg():
    State.resolver.smart_click("Deg")

@step("Toggle calculator mode to standard")
def toggle_std():
    State.resolver.smart_click("Standard")

@step("Toggle calculator mode to scientific")
def toggle_sci():
    State.resolver.smart_click("Scientific")

@step("Clear calculator input")
def clear_input():
    # AC is the usual clear for scientific calcs
    if not State.resolver.smart_click("AC"):
        State.resolver.smart_click("C")

@step("Return to the Scientific Calculator page")
def return_to_sci():
    State.page.goto("https://www.calculator.net/scientific-calculator.html")

@step("Press '='")
def press_eq():
    State.page.keyboard.press("Enter")

@step("Press '+'")
def press_plus():
    State.page.keyboard.type("+")

@step("Press '-'")
def press_minus():
    State.page.keyboard.type("-")

@step("Observe displayed result or error behavior")
def observe():
    State.page.wait_for_timeout(1000)
    print("Intent: Observation sequence...")

@step("Enter height and weight")
def height_weight():
    State.resolver.smart_fill("Height", "180")
    State.resolver.smart_fill("Weight", "75")
