from playwright.sync_api import sync_playwright

def run_canary():
    print("Starting python canary test...")
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            print("Navigating to calculator.net...")
            page.goto('https://www.calculator.net/scientific-calculator.html', timeout=30000)
            title = page.title()
            print(f"Page title: {title}")
            if 'Scientific Calculator' in title:
                print("PYTHON_CANARY_SUCCESS")
            else:
                print("PYTHON_CANARY_FAILURE: title mismatch")
            browser.close()
        except Exception as e:
            print(f"PYTHON_CANARY_ERROR: {e}")

if __name__ == "__main__":
    run_canary()
