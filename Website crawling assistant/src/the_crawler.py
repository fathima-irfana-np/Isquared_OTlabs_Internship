import time
import json
import os
from collections import deque
from datetime import datetime
from urllib.parse import urlparse, urljoin

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# -------------------------------------------------
# DRIVER SETUP
# -------------------------------------------------

def create_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    return webdriver.Chrome(options=options)


# -------------------------------------------------
# SMART LABEL EXTRACTION
# -------------------------------------------------

def get_label(el):
    for attr in ["aria-label", "placeholder", "name", "title", "data-value"]:
        value = el.get_attribute(attr)
        if value:
            return value.strip()

    text = (el.text or "").strip()
    if text:
        return text[:80]  # Cap long text content

    val = el.get_attribute("value")
    if val:
        return val.strip()

    # Fallback to id attribute
    el_id = el.get_attribute("id")
    if el_id:
        return el_id.strip()

    return "unnamed_element"


# -------------------------------------------------
# FORM VALIDATION EXTRACTION
# -------------------------------------------------

def extract_validation(el):
    return {
        "required": el.get_attribute("required") is not None,
        "pattern": el.get_attribute("pattern"),
        "min": el.get_attribute("min"),
        "max": el.get_attribute("max"),
        "maxlength": el.get_attribute("maxlength")
    }


# -------------------------------------------------
# ELEMENT CLASSIFICATION
# -------------------------------------------------

def classify_element(el):
    tag = el.tag_name.lower()
    input_type = (el.get_attribute("type") or "").lower()
    role = (el.get_attribute("role") or "").lower()
    has_click = el.get_attribute("onclick") is not None

    if tag == "a":
        return "navigation"
    if tag == "button":
        return "action"
    if tag == "select":
        return "dropdown"
    if tag == "textarea":
        return "form_input"
    if tag == "label":
        return "form_label"
    if tag == "input":
        if input_type in ["text", "email", "password", "number", "search",
                          "tel", "url", "date", "time", "range", "color", "file"]:
            return "form_input"
        if input_type in ["submit", "button"]:
            return "action"
        if input_type in ["checkbox", "radio"]:
            return "selection"

    # Styled spans, divs, tds acting as buttons
    if role in ["button", "tab", "switch", "menuitem"]:
        return "action"
    if role in ["link"]:
        return "navigation"
    if role in ["checkbox", "radio"]:
        return "selection"
    if has_click and tag in ["span", "div", "td", "li"]:
        return "action"

    return "other"


# -------------------------------------------------
# ELEMENT EXTRACTION
# -------------------------------------------------

def extract_elements(driver):
    selectors = ",".join([
        "a[href]", "button", "input", "select", "textarea",
        "[role='button']", "[role='link']", "[role='tab']",
        "[role='checkbox']", "[role='menuitem']", "[role='switch']",
        "[onclick]", "[tabindex]", "label[for]",
    ])

    elements = driver.find_elements(By.CSS_SELECTOR, selectors)
    results = []
    seen = set()

    for el in elements:
        try:
            if not el.is_displayed():
                continue

            tag = el.tag_name.lower()
            href = el.get_attribute("href")
            label = get_label(el)

            unique_key = (tag, label, href)
            if unique_key in seen:
                continue
            seen.add(unique_key)

            results.append({
                "type": tag,
                "role": classify_element(el),
                "label": label,
                "href": href,
                "id": el.get_attribute("id"),
                "name": el.get_attribute("name"),
                "visible": el.is_displayed(),
                "enabled": el.is_enabled(),
                "validation": extract_validation(el)
            })

        except:
            continue

    return results


# -------------------------------------------------
# MAIN CRAWLER
# -------------------------------------------------

def crawl_site():

    start_url = input("Enter website URL: ").strip()
    if not start_url.startswith("http"):
        start_url = "https://" + start_url

    max_depth = int(input("Enter max depth: "))
    max_pages = int(input("Enter max pages: "))

    driver = create_driver()

    results = {
        "crawl_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "pages": []
    }

    visited = set()
    queue = deque()
    queue.append((start_url, 0))

    base_domain = urlparse(start_url).netloc

    def normalize_url(u):
        """Strip fragments, trailing slashes, and sort query params."""
        p = urlparse(u)
        path = p.path.rstrip("/") or "/"
        # Sort query params for consistency
        params = sorted(p.query.split("&")) if p.query else []
        clean = p.scheme + "://" + p.netloc + path
        if params:
            clean += "?" + "&".join(params)
        return clean

    while queue and len(visited) < max_pages:

        url, depth = queue.popleft()

        if depth > max_depth:
            continue

        if url in visited:
            continue

        print(f"Crawling: {url} (Depth {depth})")
        visited.add(url)

        try:
            driver.get(url)

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )

            time.sleep(1.5)

            page_data = {
                "page_url": driver.current_url,
                "page_title": driver.title,
                "elements": []
            }

            # Extract elements from main page
            page_data["elements"].extend(extract_elements(driver))

            # Extract from iframes
            iframes = driver.find_elements(By.TAG_NAME, "iframe")
            for iframe in iframes:
                try:
                    driver.switch_to.frame(iframe)
                    page_data["elements"].extend(extract_elements(driver))
                    driver.switch_to.default_content()
                except:
                    driver.switch_to.default_content()

            results["pages"].append(page_data)

            # Collect internal links safely
            links = driver.find_elements(By.TAG_NAME, "a")
            for link in links:
                try:
                    href = link.get_attribute("href")
                    if not href:
                        continue

                    full_url = urljoin(url, href)
                    parsed = urlparse(full_url)

                    if parsed.netloc == base_domain:
                        clean_url = normalize_url(full_url)
                        if clean_url not in visited:
                            queue.append((clean_url, depth + 1))

                except:
                    continue

        except Exception as e:
            print(f"⚠ Error on {url}: {e}")

    driver.quit()

    os.makedirs("data", exist_ok=True)
    filename = "data/crawl_results.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print("\nCrawl finished")
    print("Pages Crawled:", len(results["pages"]))


if __name__ == "__main__":
    crawl_site()