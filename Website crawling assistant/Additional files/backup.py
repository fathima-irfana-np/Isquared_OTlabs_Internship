# import time
# import json
# from datetime import datetime
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.common.exceptions import WebDriverException

# def get_element_info(el):
#     """Extracts clean, meaningful data from a Selenium element."""
#     tag = el.tag_name
#     text = (el.text or el.get_attribute("aria-label") or el.get_attribute("value") or "").strip()[:50]
#     href = el.get_attribute("href")
#     onclick = el.get_attribute("onclick")
#     eid = el.get_attribute("id")
    
#     clean_id = eid if eid and len(eid) < 30 and "ext-gen" not in eid else None
    
#     return {
#         "type": tag,
#         "text": text if text else "unnamed_element",
#         "href": href if href and not href.startswith(("javascript", "#")) else None,
#         "id": clean_id,
#         "action": onclick[:50] if onclick else None
#     }

# def crawl_site():
#     target_url = input("Enter the URL to crawl (e.g., https://todolistme.net/): ")
    
#     options = webdriver.ChromeOptions()
#     driver = webdriver.Chrome(options=options)
    
#     results = {
#         "crawl_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#         "functional_elements": [],
#         "state_transitions": []
#     }

#     try:
#         driver.get(target_url)
#         print(f"Waiting 18 seconds for any manual login/auth...")
#         time.sleep(60)
        
#         initial_url = driver.current_url

#         selectors = [
#             "a[href]", "button", "input[type='button']", "input[type='submit']",
#             "[onclick]", "[role='button']", "[role='tab']"
#         ]
#         raw_elements = driver.find_elements(By.CSS_SELECTOR, ", ".join(selectors))
        
#         print(f"Found {len(raw_elements)} potential elements. Starting exploration...")

#         for i in range(len(raw_elements)):
          
#             current_elements = driver.find_elements(By.CSS_SELECTOR, ", ".join(selectors))
#             if i >= len(current_elements): break
            
#             el = current_elements[i]
#             if not el.is_displayed(): continue
            
#             info = get_element_info(el)
#             results["functional_elements"].append(info)
          
#             try:
#                 el.click()
#                 time.sleep(1) 
                
#                 new_url = driver.current_url
#                 if new_url != initial_url:
#                     results["state_transitions"].append({
#                         "from": initial_url,
#                         "to": new_url,
#                         "via": info["text"]
#                     })
                  
#                     driver.back()
#                     time.sleep(1)
#             except Exception:
#                 continue 

#     except Exception as e:
#         print(f"Crawl stopped: {e}")
#     finally:
#         driver.quit()

#     # Save to JSON
#     filename = "crawl_results.json"
#     with open(filename, "w") as f:
#         json.dump(results, f, indent=2)
    
#     print(f"\nCrawl complete! Results saved to {filename}")
#     print(f"Identified {len(results['state_transitions'])} state transitions.")

# if __name__ == "__main__":
#     print("--- Exploratory State Crawler ---")
#     print("Limitations: Won't bypass CAPTCHAs or heavy OAuth.")
#     crawl_site()




























































# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import json
# import time

# class PerfectClickableCrawler:
#     def __init__(self):
#         self.driver = webdriver.Chrome()
#         self.driver.set_window_size(1366, 768)
#         self.results = {
#             "metadata": {"crawled_at": time.strftime("%Y-%m-%d %H:%M:%S")},
#             "clickables_found": [],
#             "navigation_flows": [],
#             "crawl_issues": [],
#             "summary": {"total_clickables": 0, "crawled": 0, "failed": 0}
#         }
#         self.wait = WebDriverWait(self.driver, 2)
        
#     def crawl_site(self, url, crawl_time=60):
#         """Main crawl function with 18-second login period"""
#         print(f"\n{'='*60}")
#         print(f"🚀 Starting crawl: {url}")
#         print(f"{'='*60}")
        
#         # Open the webpage
#         self.driver.get(url)
        
#         # Always wait 18 seconds for any possible login
#         print("⏳ 18-second universal wait period (for login/auth if needed)...")
#         for i in range(18, 0, -1):
#             print(f"\r⏰ {i} seconds remaining...", end="")
#             time.sleep(1)
#         print("\r" + " " * 30 + "\r✅ Login period complete")
        
#         # Start crawling clickables
#         print("\n🔍 Starting clickable discovery...")
#         start_time = time.time()
        
#         while time.time() - start_time < crawl_time:
#             try:
#                 # Find all clickables
#                 clickables = self.find_all_clickables()
#                 print(f"📊 Found {len(clickables)} clickable elements")
                
#                 # Process each clickable
#                 for element in clickables:
#                     if self.should_skip_element(element):
#                         continue
                    
#                     result = self.test_clickable(element)
#                     if result:
#                         self.results["clickables_found"].append(result)
#                         self.results["summary"]["crawled"] += 1
                        
#                         # Record navigation flow
#                         if result.get("navigation_result") and result["navigation_result"] != "same_page":
#                             self.results["navigation_flows"].append({
#                                 "from": self.driver.current_url,
#                                 "to": result["navigation_result"],
#                                 "via": result["element_info"]["text"][:50],
#                                 "element_type": result["element_type"]
#                             })
#                     else:
#                         self.results["summary"]["failed"] += 1
                
#                 self.results["summary"]["total_clickables"] = len(clickables)
                
#                 # Take a short break between scans
#                 time.sleep(2)
                
#             except Exception as e:
#                 self.record_issue("Crawl loop error", str(e))
#                 break
        
#         self.driver.quit()
#         return self.results
    
#     def find_all_clickables(self):
#         """Find ALL machine-readable clickable elements"""
#         clickables = []
        
#         # 🔘 Basic Elements
#         clickables.extend(self.driver.find_elements(By.TAG_NAME, "button"))
#         clickables.extend(self.driver.find_elements(By.TAG_NAME, "a"))
#         clickables.extend(self.driver.find_elements(By.CSS_SELECTOR, "input[type='button'], input[type='submit'], input[type='reset']"))
#         clickables.extend(self.driver.find_elements(By.CSS_SELECTOR, "input[type='checkbox'], input[type='radio']"))
        
#         # 🧭 Navigation Elements
#         clickables.extend(self.driver.find_elements(By.CSS_SELECTOR, "nav a, nav button"))
#         clickables.extend(self.driver.find_elements(By.CSS_SELECTOR, "[role='tab'], [role='tabpanel']"))
#         clickables.extend(self.driver.find_elements(By.CSS_SELECTOR, ".pagination a, .pagination button"))
#         clickables.extend(self.driver.find_elements(By.CSS_SELECTOR, ".breadcrumb a"))
        
#         # 🪟 UI State Components
#         clickables.extend(self.driver.find_elements(By.CSS_SELECTOR, "[data-toggle='modal'], [data-target]"))
#         clickables.extend(self.driver.find_elements(By.CSS_SELECTOR, ".accordion-button, [aria-expanded]"))
        
#         # 🧮 Form Elements
#         clickables.extend(self.driver.find_elements(By.CSS_SELECTOR, "select option"))
#         clickables.extend(self.driver.find_elements(By.CSS_SELECTOR, "input[type='file']"))
        
#         # 📊 Data Components
#         clickables.extend(self.driver.find_elements(By.CSS_SELECTOR, "table a, table button"))
#         clickables.extend(self.driver.find_elements(By.CSS_SELECTOR, "[data-sort], [aria-sort]"))
        
#         # ⚙️ Settings
#         clickables.extend(self.driver.find_elements(By.CSS_SELECTOR, "[data-theme], [data-mode]"))
#         clickables.extend(self.driver.find_elements(By.CSS_SELECTOR, "select[name='language'] option"))
        
#         # Generic clickable elements
#         clickables.extend(self.driver.find_elements(By.CSS_SELECTOR, "[onclick], [role='button']"))
#         clickables.extend(self.driver.find_elements(By.CSS_SELECTOR, ".btn, .button, .clickable"))
        
#         # Filter to visible and enabled elements only
#         filtered = []
#         for element in clickables:
#             try:
#                 if element.is_displayed() and element.is_enabled():
#                     # Get position and size
#                     location = element.location
#                     size = element.size
#                     if size['width'] > 0 and size['height'] > 0:
#                         filtered.append(element)
#             except:
#                 continue
        
#         return filtered
    
#     def should_skip_element(self, element):
#         """Check if element should be skipped"""
#         try:
#             # Skip hidden or disabled
#             if not element.is_displayed() or not element.is_enabled():
#                 return True
            
#             # Skip if too small (likely decorative)
#             size = element.size
#             if size['width'] < 10 or size['height'] < 10:
#                 return True
            
#             # Skip if covered by another element
#             return False
            
#         except:
#             return True
    
#     def test_clickable(self, element):
#         """Test a single clickable element and extract data"""
#         try:
#             # Extract element info BEFORE clicking
#             element_info = self.extract_element_info(element)
#             element_type = self.classify_element_type(element)
            
#             print(f"  Testing: {element_type} - '{element_info.get('text', '')[:30]}'")
            
#             # Scroll to element
#             self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
#             time.sleep(0.3)
            
#             # Record current state BEFORE click
#             before_url = self.driver.current_url
#             before_title = self.driver.title
            
#             # Click the element
#             try:
#                 element.click()
#             except:
#                 # Fallback: JavaScript click
#                 self.driver.execute_script("arguments[0].click();", element)
            
#             # Wait for potential changes
#             time.sleep(1.5)
            
#             # Record state AFTER click
#             after_url = self.driver.current_url
#             after_title = self.driver.title
            
#             # Determine navigation result
#             navigation_result = self.analyze_navigation(before_url, after_url, before_title, after_title)
            
#             # Create result object
#             result = {
#                 "element_type": element_type,
#                 "element_info": element_info,
#                 "navigation_result": navigation_result,
#                 "before_state": {
#                     "url": before_url,
#                     "title": before_title[:50]
#                 },
#                 "after_state": {
#                     "url": after_url,
#                     "title": after_title[:50]
#                 },
#                 "timestamp": time.strftime("%H:%M:%S"),
#                 "success": True
#             }
            
#             # If navigation happened, give time for page to settle
#             if navigation_result != "same_page":
#                 time.sleep(2)
            
#             return result
            
#         except Exception as e:
#             error_msg = str(e)[:100]
#             self.record_issue(f"Failed to test element", error_msg)
#             return None
    
#     def extract_element_info(self, element):
#         """Extract JSON-able information from element"""
#         info = {}
        
#         try:
#             # Basic properties
#             info["tag"] = element.tag_name
            
#             # Text content
#             text = element.text.strip()
#             if text:
#                 info["text"] = text[:100]
            
#             # Attributes
#             info["id"] = element.get_attribute("id") or ""
#             info["name"] = element.get_attribute("name") or ""
            
#             # Classes
#             classes = element.get_attribute("class") or ""
#             if classes:
#                 info["classes"] = [c.strip() for c in classes.split() if c.strip()]
            
#             # Href for links
#             if element.tag_name == "a":
#                 info["href"] = element.get_attribute("href") or ""
            
#             # Type for inputs
#             input_type = element.get_attribute("type") or ""
#             if input_type:
#                 info["input_type"] = input_type
            
#             # ARIA attributes
#             role = element.get_attribute("role") or ""
#             if role:
#                 info["role"] = role
            
#             # Data attributes
#             for attr in ["data-toggle", "data-target", "data-action"]:
#                 value = element.get_attribute(attr) or ""
#                 if value:
#                     info[attr] = value
            
#             # Position and size
#             location = element.location
#             size = element.size
#             info["position"] = {"x": location["x"], "y": location["y"]}
#             info["size"] = {"width": size["width"], "height": size["height"]}
            
#         except Exception as e:
#             info["extraction_error"] = str(e)[:50]
        
#         return info
    
#     def classify_element_type(self, element):
#         """Classify element into one of your categories"""
#         tag = element.tag_name.lower()
#         role = element.get_attribute("role") or ""
#         element_type = element.get_attribute("type") or ""
#         classes = element.get_attribute("class") or ""
        
#         # 🔘 Basic Elements
#         if tag == "button":
#             return "button"
#         elif tag == "a":
#             return "link"
#         elif tag == "input" and element_type in ["checkbox", "radio"]:
#             return "checkbox_radio"
#         elif tag == "input" and element_type in ["button", "submit", "reset"]:
#             return "input_button"
        
#         # 🧭 Navigation
#         elif "nav" in classes or role in ["tab", "navigation"]:
#             return "navigation"
#         elif "pagination" in classes:
#             return "pagination"
#         elif "breadcrumb" in classes:
#             return "breadcrumb"
        
#         # 🪟 UI State Components
#         elif "modal" in classes or "dialog" in role:
#             return "modal_trigger"
#         elif "accordion" in classes or "expanded" in role:
#             return "accordion"
        
#         # 🧮 Form Elements
#         elif tag == "select":
#             return "dropdown"
#         elif tag == "input" and element_type == "file":
#             return "file_upload"
        
#         # 📊 Data Components
#         elif "table" in classes or tag == "table":
#             return "table_element"
#         elif "sort" in classes or "sort" in role:
#             return "sort_control"
        
#         # ⚙️ Settings
#         elif "theme" in classes or "language" in classes:
#             return "settings_control"
        
#         # Generic
#         elif role == "button":
#             return "aria_button"
#         elif "btn" in classes or "button" in classes:
#             return "styled_button"
        
#         else:
#             return "generic_clickable"
    
#     def analyze_navigation(self, before_url, after_url, before_title, after_title):
#         """Analyze what happened after click"""
#         if before_url != after_url:
#             return "new_page"
#         elif before_title != after_title:
#             return "title_changed"
#         else:
#             return "same_page"
    
#     def record_issue(self, issue_type, details):
#         """Record why something couldn't be crawled"""
#         issue = {
#             "type": issue_type,
#             "details": details[:200],
#             "timestamp": time.strftime("%H:%M:%S"),
#             "url": self.driver.current_url
#         }
#         self.results["crawl_issues"].append(issue)
#         print(f"⚠️  {issue_type}: {details[:50]}")

# def main():
#     # Sites list (removed WhatsApp as requested)
#     sites = [
#         {"name": "TODO List", "url": "https://todolistme.net/"},
#         {"name": "Google Apps", "url": "https://docs.google.com/"},
#         {"name": "Outlook", "url": "https://outlook.office.com/"},
#         {"name": "QR Generator", "url": "https://www.the-qrcode-generator.com/"},
#         {"name": "Calculator", "url": "https://www.calculator.net/"},
#         {"name": "TCS Calculator", "url": "https://tcsion.com/OnlineAssessment/ScientificCalculator/Calculator.html"},
#         {"name": "CalculatorSoup", "url": "https://www.calculatorsoup.com/calculators/math/basic.php"},
#         {"name": "Telegram", "url": "https://www.telegram.org/apps"}
#     ]
    
#     print("🌐 PERFECT CLICKABLE CRAWLER")
#     print("=" * 60)
    
#     # Show sites
#     for i, site in enumerate(sites, 1):
#         print(f"{i}. {site['name']}")
    
#     # Get selection
#     choice = input("\nSelect site (1-8): ").strip()
#     if not choice.isdigit() or int(choice) < 1 or int(choice) > 8:
#         print("Invalid choice!")
#         return
    
#     selected = sites[int(choice) - 1]
    
#     # Ask for crawl time
#     crawl_time = input("Crawl time in seconds (default 60): ").strip()
#     crawl_time = int(crawl_time) if crawl_time.isdigit() else 60
    
#     # Run crawler
#     crawler = PerfectClickableCrawler()
#     results = crawler.crawl_site(selected["url"], crawl_time)
    
#     # Save results
#     filename = f"clickables_{selected['name'].lower().replace(' ', '_')}.json"
#     with open(filename, "w", encoding="utf-8") as f:
#         json.dump(results, f, indent=2, ensure_ascii=False)
    
#     # Print summary
#     print(f"\n{'='*60}")
#     print("✅ CRAWL COMPLETE!")
#     print(f"{'='*60}")
#     print(f"📊 RESULTS SUMMARY:")
#     print(f"   • Total clickables found: {results['summary']['total_clickables']}")
#     print(f"   • Successfully crawled: {results['summary']['crawled']}")
#     print(f"   • Failed attempts: {results['summary']['failed']}")
#     print(f"   • Navigation flows recorded: {len(results['navigation_flows'])}")
#     print(f"   • Issues encountered: {len(results['crawl_issues'])}")
#     print(f"\n💾 Results saved to: {filename}")
    
#     # Show some example data
#     if results["clickables_found"]:
#         print(f"\n📝 SAMPLE CLICKABLE DATA:")
#         for i, clickable in enumerate(results["clickables_found"][:3], 1):
#             print(f"   {i}. {clickable['element_type']}: '{clickable['element_info'].get('text', '')[:30]}'")
#             print(f"      → {clickable['navigation_result']}")
    
#     # Show issues if any
#     if results["crawl_issues"]:
#         print(f"\n⚠️  CRAWL ISSUES (Why some elements couldn't be crawled):")
#         for issue in results["crawl_issues"][:5]:
#             print(f"   • {issue['type']}: {issue['details'][:50]}")

# if __name__ == "__main__":
#     main()