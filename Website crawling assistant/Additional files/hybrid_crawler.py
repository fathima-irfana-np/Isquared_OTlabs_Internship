import time
import json
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException

def get_element_info(el):
    """Extracts clean, meaningful data from a Selenium element."""
    tag = el.tag_name
    text = (el.text or el.get_attribute("aria-label") or el.get_attribute("value") or "").strip()[:50]
    href = el.get_attribute("href")
    onclick = el.get_attribute("onclick")
    eid = el.get_attribute("id")
    
    clean_id = eid if eid and len(eid) < 30 and "ext-gen" not in eid else None
    
    return {
        "type": tag,
        "text": text if text else "unnamed_element",
        "href": href if href and not href.startswith(("javascript", "#")) else None,
        "id": clean_id,
        "action": onclick[:50] if onclick else None
    }

def crawl_site():
    target_url = input("Enter the URL to crawl (e.g., https://todolistme.net/): ")
    
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)
    
    results = {
        "crawl_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "functional_elements": [],
        "state_transitions": []
    }

    try:
        driver.get(target_url)
        print(f"Waiting 18 seconds for any manual login/auth...")
        time.sleep(60)
        
        initial_url = driver.current_url

        selectors = [
            "a[href]", "button", "input[type='button']", "input[type='submit']",
            "[onclick]", "[role='button']", "[role='tab']"
        ]
        raw_elements = driver.find_elements(By.CSS_SELECTOR, ", ".join(selectors))
        
        print(f"Found {len(raw_elements)} potential elements. Starting exploration...")

        for i in range(len(raw_elements)):
          
            current_elements = driver.find_elements(By.CSS_SELECTOR, ", ".join(selectors))
            if i >= len(current_elements): break
            
            el = current_elements[i]
            if not el.is_displayed(): continue
            
            info = get_element_info(el)
            results["functional_elements"].append(info)
          
            try:
                el.click()
                time.sleep(1) 
                
                new_url = driver.current_url
                if new_url != initial_url:
                    results["state_transitions"].append({
                        "from": initial_url,
                        "to": new_url,
                        "via": info["text"]
                    })
                  
                    driver.back()
                    time.sleep(1)
            except Exception:
                continue 

    except Exception as e:
        print(f"Crawl stopped: {e}")
    finally:
        driver.quit()

    # Save to JSON
    filename = "crawl_results.json"
    with open(filename, "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\nCrawl complete! Results saved to {filename}")
    print(f"Identified {len(results['state_transitions'])} state transitions.")

if __name__ == "__main__":
    print("--- Exploratory State Crawler ---")
    print("Limitations: Won't bypass CAPTCHAs or heavy OAuth.")
    crawl_site()











# import time
# import json
# from datetime import datetime
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.common.exceptions import WebDriverException

# def get_element_info(el):
#     """Extracts clean, meaningful data from a Selenium element."""
#     try:
#         tag = el.tag_name
#         text = (
#             el.text
#             or el.get_attribute("aria-label")
#             or el.get_attribute("value")
#             or el.get_attribute("title")
#             or ""
#         ).strip()[:50]

#         href = el.get_attribute("href")
#         onclick = el.get_attribute("onclick")
#         eid = el.get_attribute("id")

#         clean_id = eid if eid and len(eid) < 40 and "ext-gen" not in eid else None

#         return {
#             "type": tag,
#             "text": text if text else "unnamed_element",
#             "href": href if href and not href.startswith(("javascript", "#")) else None,
#             "id": clean_id,
#             "action": onclick[:50] if onclick else None
#         }
#     except:
#         return None


# def find_elements_in_all_frames(driver, selectors):
#     """Find elements in main page and all iframes."""
#     elements = []

#     # Main document
#     elements.extend(driver.find_elements(By.CSS_SELECTOR, selectors))

#     # Iframes
#     iframes = driver.find_elements(By.TAG_NAME, "iframe")
#     for i in range(len(iframes)):
#         try:
#             driver.switch_to.frame(i)
#             elements.extend(driver.find_elements(By.CSS_SELECTOR, selectors))
#             driver.switch_to.default_content()
#         except:
#             driver.switch_to.default_content()
#             continue

#     return elements


# def crawl_site():
#     target_url = input("Enter the URL to crawl: ")

#     options = webdriver.ChromeOptions()
#     driver = webdriver.Chrome(options=options)

#     results = {
#         "crawl_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#         "functional_elements": [],
#         "state_transitions": []
#     }

#     try:
#         driver.get(target_url)
#         print("Waiting 60 seconds for manual login/auth...")
#         time.sleep(60)

#         initial_url = driver.current_url

#         selectors = (
#             "a[href], button, input[type='button'], input[type='submit'], "
#             "[onclick], [role='button'], [role='tab']"
#         )

#         raw_elements = find_elements_in_all_frames(driver, selectors)
#         print(f"Found {len(raw_elements)} potential elements across all frames.")

#         for i in range(min(len(raw_elements), 100)):
#             try:
#                 elements = find_elements_in_all_frames(driver, selectors)
#                 if i >= len(elements):
#                     break

#                 el = elements[i]
#                 if not el.is_displayed():
#                     continue

#                 info = get_element_info(el)
#                 if info:
#                     results["functional_elements"].append(info)

#                 el.click()
#                 time.sleep(1)

#                 if driver.current_url != initial_url:
#                     results["state_transitions"].append({
#                         "from": initial_url,
#                         "to": driver.current_url,
#                         "via": info["text"] if info else "unknown"
#                     })
#                     driver.back()
#                     time.sleep(1)

#             except WebDriverException:
#                 continue

#     except Exception as e:
#         print(f"Crawl stopped: {e}")

#     finally:
#         driver.quit()
#         with open("second_crawl_results.json", "w") as f:
#             json.dump(results, f, indent=2)

#         print("\nCrawl complete!")
#         print(f"Functional elements found: {len(results['functional_elements'])}")
#         print(f"State transitions detected: {len(results['state_transitions'])}")


# if __name__ == "__main__":
#     print("--- Exploratory State Crawler (Iframe Enabled) ---")
#     crawl_site()

