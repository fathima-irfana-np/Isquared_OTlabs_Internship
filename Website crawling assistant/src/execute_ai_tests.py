import json
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By

TEST_FILE = "data/generated_test_cases.json"
SCREENSHOT_DIR = "screenshots"

os.makedirs(SCREENSHOT_DIR, exist_ok=True)


def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    return webdriver.Chrome(options=options)


def execute_step(driver, step):
    step = step.lower()

    if "click" in step:
        target = step.replace("click", "").strip()
        driver.find_element(
            By.XPATH, f"//*[contains(normalize-space(text()),'{target}')]"
        ).click()

    elif "enter" in step:
        inputs = driver.find_elements(By.TAG_NAME, "input")
        if inputs:
            inputs[0].send_keys("test")

    time.sleep(1)


def main():
    target_url = input("Enter target URL to execute tests: ").strip()
    if not target_url.startswith("http"):
        target_url = "https://" + target_url

    with open(TEST_FILE) as f:
        tests = json.load(f)["generated_tests"]

    driver = setup_driver()
    driver.get(target_url)
    time.sleep(3)

    results = []

    for test in tests:
        test_id = test["id"]
        status = "PASSED"

        try:
            for step in test["steps"]:
                execute_step(driver, step)

        except Exception as e:
            status = "FAILED"
            screenshot = f"{SCREENSHOT_DIR}/{test_id}.png"
            driver.save_screenshot(screenshot)
            results.append({
                "test_id": test_id,
                "status": status,
                "error": str(e),
                "screenshot": screenshot
            })
            continue

        results.append({
            "test_id": test_id,
            "status": status
        })

    driver.quit()

    with open("data/execution_results.json", "w") as f:
        json.dump(results, f, indent=2)

    print("Tests executed. Results saved to execution_results.json")


if __name__ == "__main__":
    main()
