import time
import json
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException

def get_element_info(el):
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

def find_all_elements(driver, selectors):
    all_elements = []
    
    all_elements.extend(driver.find_elements(By.CSS_SELECTOR, ", ".join(selectors)))
    
    iframes = driver.find_elements(By.TAG_NAME, "iframe")
    
    for i, iframe in enumerate(iframes):
        try:
            driver.switch_to.frame(iframe)
            
            iframe_elements = driver.find_elements(By.CSS_SELECTOR, ", ".join(selectors))
            all_elements.extend(iframe_elements)
            
            driver.switch_to.default_content()
        except:
            try:
                driver.switch_to.default_content()
            except:
                pass
            continue
    
    return all_elements

def crawl_site():
    target_url = input("Enter the URL to crawl : ")
    
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)
    
    results = {
        "crawl_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "functional_elements": [],
        "state_transitions": []
    }

    try:
        driver.get(target_url)
        print(f"Waiting 1 minute for any manual login/auth...")
        time.sleep(10)
        
        initial_url = driver.current_url

        selectors = [
            "a[href]", "button", "input[type='button']", "input[type='submit']",
            "[onclick]", "[role='button']", "[role='tab']"
        ]
        
        raw_elements = find_all_elements(driver, selectors)
        
        print(f"Found {len(raw_elements)} potential elements including iframes. Starting exploration...")
        
        for i in range(len(raw_elements)):
          
            current_elements = find_all_elements(driver, selectors)
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
    filename = "data/crawl_results.json"
    with open(filename, "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\nCrawl complete! Results saved to {filename}")
    print(f"Identified {len(results['state_transitions'])} state transitions.")

if __name__ == "__main__":
    print("--- Exploratory State Crawler ---")
    print("Limitations: Won't bypass CAPTCHAs or heavy OAuth.")
    crawl_site()
