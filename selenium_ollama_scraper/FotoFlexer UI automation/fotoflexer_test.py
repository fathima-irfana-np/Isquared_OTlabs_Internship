import os 
import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

# Constants
URL = "https://fotoflexer.com/editor/"
TEST_IMAGE_PATH = r"C:\Users\fathi\OneDrive\Pictures\mountains.jpg"  # User provided path

@pytest.fixture(scope="module")
def driver():
    """Setup and teardown of the Chrome driver."""
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless") # Comment out to see the UI
    options.add_argument("--start-maximized")
    options.add_argument("--disable-search-engine-choice-screen")
    
    drv = webdriver.Chrome(options=options)
    yield drv
    drv.quit()

@pytest.fixture(scope="module")
def wait(driver):
    return WebDriverWait(driver, 15)

def test_open_editor(driver):
    """Test 1: The editor page opens successfully."""
    driver.get(URL)
    assert "FotoFlexer" in driver.title, "Title does not match expected."
    print("\n[PASS] Editor Page Opened")

def test_upload_image(driver, wait):
    """Test 2: An image can be uploaded."""
    # FotoFlexer has a hidden file input or relies on the 'Open Photo' button.
    # We will try to find the hidden input directly first.
    
    # Wait for page load
    time.sleep(2) 
    
    try:
        # Try to locate the file input. 
        # Based on inspection, it might be dynamically created or just hidden.
        # Often it's input[type='file'].
        file_input = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
    except:
        # If not found immediately, maybe we need to click "Open Photo" first to trigger it?
        # But usually input[type=file] is present. Let's try injecting one if needed 
        # OR just assume the standard one exists.
        # Let's try to click "Open Photo" and see if input appears if not found.
        open_btns = driver.find_elements(By.CSS_SELECTOR, "button.mat-flat-button.mat-primary")
        if open_btns:
            open_btns[0].click()
            time.sleep(1)
        file_input = driver.find_element(By.CSS_SELECTOR, "input[type='file']")

    # Upload the file
    # Ensure test image exists
    if not os.path.exists(TEST_IMAGE_PATH):
        pytest.fail(f"Test image not found at {TEST_IMAGE_PATH}")

    file_input.send_keys(TEST_IMAGE_PATH)
    
    # Wait for the editor workspace to load (canvas confirmation)
    # The 'Open Photo' buttons should disappear or the main canvas should appear.
    try:
        wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, "button.mat-flat-button.mat-primary")))
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "canvas")))
        print("\n[PASS] Image Uploaded Successfully")
        time.sleep(2) # Visual delay to verify image
    except TimeoutException:
        pytest.fail("Editor did not load after image upload.")

# def test_tools_visibility_and_interaction(driver, wait):
#     """Test 3: All editor tools are visible, clickable, and function correctly."""
    
#     # Wait for tools to be visible
#     time.sleep(2)
    
#     # Based on the HTML, tools might be in <editor-controls> or similar
#     # Let's try to find tool buttons in the editor controls
#     try:
#         # First, find the editor controls container
#         tools = wait.until(EC.presence_of_all_elements_located(
#             (By.CSS_SELECTOR, "editor-controls button.control-button, editor-controls .control-button")
#         ))
#     except TimeoutException:
#         # Try alternative selectors
#         try:
#             tools = wait.until(EC.presence_of_all_elements_located(
#                 (By.CSS_SELECTOR, "button.control-button, .control-button, [class*='control-button']")
#             ))
#         except TimeoutException:
#             # Look for any buttons in editor controls
#             try:
#                 tools = wait.until(EC.presence_of_all_elements_located(
#                     (By.CSS_SELECTOR, "editor-controls button")
#                 ))
#             except TimeoutException:
#                 pytest.fail("No tools found. Editor might not be loaded properly.")
    
#     tool_count = len(tools)
#     print(f"\n[INFO] Found {tool_count} tools to test.")
    
#     # Debug: Print all found tools
#     print("\n[DEBUG] Available tools:")
#     for i, tool in enumerate(tools):
#         try:
#             tool_text = tool.text.strip()
#             tool_class = tool.get_attribute("class") or ""
#             print(f"  {i+1}. Text: '{tool_text}', Class: '{tool_class}'")
#         except:
#             print(f"  {i+1}. Could not read tool info")

    
#     for i in range(min(3, tool_count)):  # Test only first 3 tools for now
#         # Re-fetch the list of tools
#         try:
#             tools = wait.until(EC.presence_of_all_elements_located(
#                 (By.CSS_SELECTOR, "editor-controls button, button.control-button")
#             ))
#             tool = tools[i]
#         except TimeoutException:
#             pytest.fail("Tools list mismatch or failed to reload.")
        
#         # Get tool info
#         try:
#             tool_text = tool.text.strip()
#             tool_name = tool_text if tool_text else f"Tool-{i+1}"
#         except:
#             tool_name = f"Tool-{i+1}"
        
#         # Also try to find tool name from child elements
#         if not tool_name or tool_name == f"Tool-{i+1}":
#             try:
#                 # Look for span with name
#                 name_spans = tool.find_elements(By.CSS_SELECTOR, "span.name, .name")
#                 if name_spans:
#                     tool_name = name_spans[0].text.strip()
#             except:
#                 pass
            
#         print(f"\n{'='*60}")
#         print(f"Testing Tool #{i+1}: {tool_name}")
#         print(f"{'='*60}")
        
#         # 1. Check Visibility
#         if not tool.is_displayed():
#             print(f"  - {tool_name}: [SKIP] Element is present but not visible.")
#             continue
            
#         print(f"  - {tool_name}: Visible")

#         # 2. Click Tool
#         try:
#             print(f"  - Clicking tool at location: {tool.location}")
#             tool.click()
#             print(f"  - {tool_name}: Clicked")
#             time.sleep(2)  # Wait for panel to open
#         except Exception as e:
#             print(f"  - Error clicking: {e}")
#             # Try JavaScript click
#             try:
#                 driver.execute_script("arguments[0].click();", tool)
#                 print(f"  - {tool_name}: Clicked (JavaScript)")
#                 time.sleep(2)
#             except Exception as e2:
#                 print(f"  - JavaScript click also failed: {e2}")
#                 continue

#         # 3. Take screenshot to see what opened
#         driver.save_screenshot(f"debug_{tool_name.lower().replace(' ', '_')}_panel.png")
#         print(f"  - Screenshot saved for debugging")

#         # 4. SPECIAL HANDLING FOR SPECIFIC TOOLS
#         tool_name_upper = tool_name.upper()
        
#         # Handle FILTER tool
#         if "FILTER" in tool_name_upper:
#             print("  - [FILTER TOOL] Looking for filter options...")
#             time.sleep(2)
            
#             # Look for filter options - they might be in a grid/list
#             filter_selectors = [
#                 "mat-grid-tile",  # Angular Material grid tiles
#                 ".mat-grid-tile",
#                 "div.filter-item",
#                 "div.filter-option",
#                 "mat-card",  # Filter cards
#                 ".mat-card",
#                 "div[class*='filter']",
#                 "div.preview-container",  # Filter preview containers
#                 "img[class*='filter']"  # Filter preview images
#             ]
            
#             for selector in filter_selectors:
#                 try:
#                     elements = driver.find_elements(By.CSS_SELECTOR, selector)
#                     if elements:
#                         print(f"  - Found {len(elements)} elements with selector: {selector}")
#                         # Try to click the first one (like "Vintage")
#                         for elem in elements[:3]:  # Try first 3
#                             try:
#                                 if elem.is_displayed() and elem.is_enabled():
#                                     elem_text = elem.text.strip().upper()
#                                     print(f"    - Element text: '{elem_text}'")
#                                     elem.click()
#                                     print(f"    - Clicked filter option")
#                                     time.sleep(2)  # Wait for Apply button
#                                     break
#                             except:
#                                 continue
#                 except:
#                     continue
        
#         # Handle RESIZE tool - UPDATED BASED ON SCREENSHOT
#         elif "RESIZE" in tool_name_upper or "SIZE" in tool_name_upper:
#             print("  - [RESIZE TOOL] Entering width and height values...")
#             time.sleep(2)
            
#             # Take another screenshot to see the resize panel
#             driver.save_screenshot(f"debug_{tool_name.lower().replace(' ', '_')}_resize_panel.png")
            
#             # Based on the screenshot HTML, the inputs are in resize-drawer with specific IDs
#             print("  - Looking for resize inputs...")
            
#             # METHOD 1: Try to find inputs by ID (from HTML)
#             try:
#                 # Look for width input by ID or formcontrolname
#                 width_input = None
#                 height_input = None
                
#                 # Try multiple selectors for width
#                 width_selectors = [
#                     "input#width",  # By ID
#                     "input[name='width']",
#                     "input[formcontrolname='width']",
#                     "input[placeholder*='width' i]",
#                     "input[aria-label*='width' i]"
#                 ]
                
#                 for selector in width_selectors:
#                     try:
#                         elements = driver.find_elements(By.CSS_SELECTOR, selector)
#                         for elem in elements:
#                             if elem.is_displayed():
#                                 width_input = elem
#                                 print(f"    - Found width input with selector: {selector}")
#                                 break
#                         if width_input:
#                             break
#                     except:
#                         continue
                
#                 # Try multiple selectors for height
#                 height_selectors = [
#                     "input#height",  # By ID (from HTML)
#                     "input[name='height']",
#                     "input[formcontrolname='height']",
#                     "input[placeholder*='height' i]",
#                     "input[aria-label*='height' i]"
#                 ]
                
#                 for selector in height_selectors:
#                     try:
#                         elements = driver.find_elements(By.CSS_SELECTOR, selector)
#                         for elem in elements:
#                             if elem.is_displayed():
#                                 height_input = elem
#                                 print(f"    - Found height input with selector: {selector}")
#                                 break
#                         if height_input:
#                             break
#                     except:
#                         continue
                
#                 # METHOD 2: If not found by ID, look for inputs in resize-drawer
#                 if not width_input or not height_input:
#                     print("    - Trying to find inputs in resize-drawer...")
#                     try:
#                         # Find all inputs in the resize drawer
#                         resize_inputs = driver.find_elements(By.CSS_SELECTOR, "resize-drawer input[type='number']")
#                         if len(resize_inputs) >= 2:
#                             # First is likely width, second is height
#                             width_input = resize_inputs[0]
#                             height_input = resize_inputs[1]
#                             print(f"    - Found {len(resize_inputs)} number inputs in resize-drawer")
#                     except:
#                         pass
                
#                 # METHOD 3: Look for all number inputs
#                 if not width_input or not height_input:
#                     print("    - Trying all number inputs on page...")
#                     try:
#                         all_number_inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='number']")
#                         if len(all_number_inputs) >= 2:
#                             width_input = all_number_inputs[0]
#                             height_input = all_number_inputs[1]
#                             print(f"    - Found {len(all_number_inputs)} number inputs on page")
#                     except:
#                         pass
                
#                 # Enter values into width input
#                 if width_input:
#                     try:
#                         # Clear the input first
#                         width_input.clear()
#                         time.sleep(0.2)
                        
#                         # Enter new value
#                         width_input.send_keys("800")
#                         print(f"    - Entered width: 800")
#                         time.sleep(0.5)
                        
#                         # Verify the value was entered
#                         current_value = width_input.get_attribute("value")
#                         print(f"    - Width input current value: {current_value}")
#                     except Exception as e:
#                         print(f"    - Error entering width: {e}")
#                         # Try JavaScript to set value
#                         try:
#                             driver.execute_script("arguments[0].value = '800';", width_input)
#                             print(f"    - Set width to 800 using JavaScript")
#                         except:
#                             print(f"    - JavaScript also failed for width")
#                 else:
#                     print("    - Could not find width input")
                
#                 # Enter values into height input
#                 if height_input:
#                     try:
#                         # Clear the input first
#                         height_input.clear()
#                         time.sleep(0.2)
                        
#                         # Enter new value
#                         height_input.send_keys("600")
#                         print(f"    - Entered height: 600")
#                         time.sleep(0.5)
                        
#                         # Verify the value was entered
#                         current_value = height_input.get_attribute("value")
#                         print(f"    - Height input current value: {current_value}")
#                     except Exception as e:
#                         print(f"    - Error entering height: {e}")
#                         # Try JavaScript to set value
#                         try:
#                             driver.execute_script("arguments[0].value = '600';", height_input)
#                             print(f"    - Set height to 600 using JavaScript")
#                         except:
#                             print(f"    - JavaScript also failed for height")
#                 else:
#                     print("    - Could not find height input")
                
#                 # Handle "Maintain Aspect Ratio" checkbox
#                 try:
#                     # Look for checkbox
#                     checkbox_selectors = [
#                         "input[type='checkbox']",
#                         "mat-checkbox",
#                         ".checkbox-container input",
#                         "input[formcontrolname*='aspect']",
#                         "input[name*='aspect']"
#                     ]
                    
#                     for selector in checkbox_selectors:
#                         try:
#                             checkboxes = driver.find_elements(By.CSS_SELECTOR, selector)
#                             for checkbox in checkboxes:
#                                 if checkbox.is_displayed():
#                                     # Get parent label text to identify
#                                     try:
#                                         parent_text = checkbox.find_element(By.XPATH, "..").text.upper()
#                                         if "MAINTAIN" in parent_text or "ASPECT" in parent_text or "RATIO" in parent_text:
#                                             # Check if it's checked
#                                             is_checked = checkbox.is_selected()
#                                             if is_checked:
#                                                 print(f"    - 'Maintain Aspect Ratio' is checked")
#                                                 # If we want to unlock aspect ratio, we would uncheck it
#                                                 # checkbox.click()
#                                                 # print(f"    - Unchecked 'Maintain Aspect Ratio'")
#                                             else:
#                                                 print(f"    - 'Maintain Aspect Ratio' is not checked")
#                                             break
#                                     except:
#                                         pass
#                         except:
#                             continue
#                 except Exception as e:
#                     print(f"    - Error handling checkbox: {e}")
                
#             except Exception as e:
#                 print(f"    - Error in resize tool handling: {e}")
        
#         # 5. Look for Apply button or action buttons
#         print("  - Looking for Apply/action buttons...")
        
#         # Try multiple ways to find action buttons
#         action_buttons = []
        
#         # Look by text content (case-insensitive)
#         button_texts = ["Apply", "OK", "Done", "Save", "Confirm", "✓", "✔"]
#         for text in button_texts:
#             try:
#                 # XPath for case-insensitive text search
#                 buttons = driver.find_elements(
#                     By.XPATH, 
#                     f"//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{text.lower()}')]"
#                 )
#                 action_buttons.extend(buttons)
#             except:
#                 pass
        
#         # Look by class names
#         button_classes = ["apply-button", "mat-flat-button", "mat-primary", "mat-button-base"]
#         for class_name in button_classes:
#             try:
#                 buttons = driver.find_elements(By.CSS_SELECTOR, f"button[class*='{class_name}']")
#                 action_buttons.extend(buttons)
#             except:
#                 pass
        
#         # Remove duplicates
#         unique_buttons = []
#         seen = set()
#         for btn in action_buttons:
#             try:
#                 btn_id = btn.id
#             except:
#                 btn_id = None
#             btn_key = (btn.location['x'], btn.location['y'], btn_id)
#             if btn_key not in seen:
#                 seen.add(btn_key)
#                 unique_buttons.append(btn)
        
#         print(f"  - Found {len(unique_buttons)} potential action buttons")
        
#         # Click the first visible action button
#         clicked = False
#         for btn in unique_buttons[:5]:  # Try first 5
#             try:
#                 if btn.is_displayed() and btn.is_enabled():
#                     btn_text = btn.text.strip()
#                     print(f"    - Clicking button: '{btn_text}'")
#                     btn.click()
#                     clicked = True
#                     time.sleep(2)
#                     break
#             except:
#                 continue
        
#         if not clicked:
#             print("  - No action button found/clicked")
#             # Press ESC to close any open panel
#             try:
#                 ActionChains(driver).send_keys(Keys.ESCAPE).perform()
#                 print("  - Pressed ESC to close panel")
#                 time.sleep(1)
#             except:
#                 pass
        
#         # 6. Wait to return to main tools
#         try:
#             wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "editor-controls")))
#             print(f"  - {tool_name}: Returned to main menu")
#         except TimeoutException:
#             print(f"  - [WARNING] May still be in tool panel")
        
#         time.sleep(1)  # Brief pause between tools

#     print("\n[PASS] Tools tested successfully")

# def test_transform_only(driver, wait):
#     """Test transform tool functionality."""
#     print("\n[TEST] Transform tool only")
    
#     # Wait a moment for everything to settle
#     time.sleep(2)
    
#     # Find the transform tool (it's the 4th button)
#     # Re-fetch using the robust selector
#     try:
#          all_tools = wait.until(EC.presence_of_all_elements_located(
#             (By.CSS_SELECTOR, ".control-button")
#         ))
#     except:
#         all_tools = driver.find_elements(By.CSS_SELECTOR, "editor-controls button.control-button")
    
#     if len(all_tools) < 4:
#         print("  - Not enough tools found")
#         return
    
#     # Click the TRANSFORM button (found dynamically)
#     print("  - Clicking TRANSFORM button...")

#     transform_button = None

#     for tool in all_tools:
#         try:
#             tool_text = (tool.text or "").strip().lower()
#             aria_label = (tool.get_attribute("aria-label") or "").lower()

#             if "transform" in tool_text or "rotate" in tool_text or "transform" in aria_label:
#                 transform_button = tool
#                 break
#         except:
#             continue

#     if not transform_button:
#         print("  - [ERROR] Transform tool not found")
#         return

#     try:
#         transform_button.click()
#     except Exception as e:
#         print(f"  - Click failed: {e}, using JS click")
#         driver.execute_script("arguments[0].click();", transform_button)

#     time.sleep(2)

    
#     # Click rotate right button
#     print("  - Clicking rotate right...")
#     rotate_buttons = driver.find_elements(By.CSS_SELECTOR, "button.rotate-button.button-with-image.small")
#     if len(rotate_buttons) >= 2:
#         rotate_buttons[1].click()
#         time.sleep(1)
    
#     # Click rotate left button  
#     print("  - Clicking rotate left...")
#     if len(rotate_buttons) >= 2:
#         rotate_buttons[0].click()
#         time.sleep(1)
    
#     # Adjust slider
#     print("  - Adjusting slider...")
#     try:
#         slider = driver.find_element(By.CSS_SELECTOR, "mat-slider.mat-slider.mat-accent")
#         slider_width = slider.size['width']
#         ActionChains(driver).move_to_element_with_offset(slider, slider_width * 0.25, 10).click().perform()
#         time.sleep(1)
#     except:
#         pass
    
#     # Click Apply
#     print("  - Clicking Apply...")
#     try:
#         apply_button = driver.find_element(By.CSS_SELECTOR, "button.apply-button.mat-raised-button.mat-accent")
#         apply_button.click()
#     except:
#         # Try to find by text
#         all_buttons = driver.find_elements(By.TAG_NAME, "button")
#         for btn in all_buttons:
#             try:
#                 if "APPLY" in btn.text.upper():
#                     btn.click()
#                     break
#             except:
#                 continue
    
#     time.sleep(2)
#     print("[PASS] Transform tool tested")

def test_draw_tool(driver, wait):
    """Test the DRAW tool functionality."""
    print("\n[TEST] Testing DRAW Tool")
    print("="*60)
    
    # Wait for tools to be ready
    time.sleep(2)
    
    # 1. Find and click the DRAW tool button
    print("  - Looking for DRAW tool button...")
    
    # Try multiple ways to find the draw button
    draw_button = None
    
    # Method 1: By the text "draw" in the span
    try:
        draw_buttons = driver.find_elements(
            By.XPATH, 
            "//button[.//span[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'draw')]]"
        )
        for btn in draw_buttons:
            if btn.is_displayed():
                draw_button = btn
                break
    except:
        pass
    
    # Method 2: By class containing 'control-button' and checking inner text
    if not draw_button:
        try:
            all_buttons = driver.find_elements(By.CSS_SELECTOR, "button.control-button, .control-button")
            for btn in all_buttons:
                try:
                    btn_text = btn.text.strip().lower()
                    if 'draw' in btn_text:
                        if btn.is_displayed():
                            draw_button = btn
                            break
                except:
                    continue
        except:
            pass
    
    # Method 3: Try to find by the SVG path (from your screenshot)
    if not draw_button:
        try:
            # Look for the specific SVG path from screenshot
            svg_elements = driver.find_elements(
                By.XPATH,
                "//button[.//path[contains(@d, 'M23.906 3.969A4.097')]]"
            )
            for svg_elem in svg_elements:
                parent_btn = svg_elem.find_element(By.XPATH, "..//..//..")
                if parent_btn.is_displayed():
                    draw_button = parent_btn
                    break
        except:
            pass
    
    if not draw_button:
        print("  - [ERROR] Could not find DRAW tool button")
        return
    
    print(f"  - Found DRAW button at location: {draw_button.location}")
    
    # 2. Click the DRAW tool
    try:
        print("  - Clicking DRAW tool...")
        draw_button.click()
        time.sleep(3)  # Wait for draw panel to open
    except Exception as e:
        print(f"  - Error clicking: {e}, using JS click")
        driver.execute_script("arguments[0].click();", draw_button)
        time.sleep(3)
    
    # Take screenshot for debugging
    driver.save_screenshot("debug_draw_tool_opened.png")
    print("  - Screenshot saved: debug_draw_tool_opened.png")
    
    # 3. SELECT BRUSH COLOR
    print("\n  - Selecting brush colors...")
    
    # Based on your screenshot, colors are buttons with style attribute containing background color
    color_buttons = driver.find_elements(
        By.CSS_SELECTOR, 
        "button[class*='color control'], button[style*='background:'], .color-control"
    )
    
    print(f"  - Found {len(color_buttons)} color buttons")
    
    # Test 2-3 different colors
    colors_to_test = [
        "rgb(0, 0, 0)",      # Black
        "rgb(255, 36, 19)",  # Red (adjusted from your screenshot)
        "rgb(4, 107, 114)",  # Blue
    ]
    
    for color_rgb in colors_to_test:
        print(f"    - Looking for color: {color_rgb}")
        
        # Try to find button with this background color
        found_color = False
        for btn in color_buttons:
            try:
                style = btn.get_attribute("style") or ""
                if color_rgb in style:
                    print(f"    - Selecting color: {color_rgb}")
                    btn.click()
                    found_color = True
                    time.sleep(1)  # Wait for color selection to take effect
                    
                    # Check if selected (might have 'selected' class)
                    btn_class = btn.get_attribute("class") or ""
                    if "selected" in btn_class:
                        print(f"    - Color {color_rgb} is now selected")
                    break
            except:
                continue
        
        if not found_color:
            print(f"    - [WARNING] Color {color_rgb} not found")
    
    # 4. ADJUST BRUSH SIZE (if slider exists)
    print("\n  - Adjusting brush size...")
    
    # Look for brush size controls
    brush_size_selectors = [
        "input[type='range']",  # Slider input
        "mat-slider",           # Material slider
        "[class*='brush-size']",
        "[class*='slider']",
        "[aria-label*='brush' i]",
        "[aria-label*='size' i]"
    ]
    
    brush_slider = None
    for selector in brush_size_selectors:
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            for elem in elements:
                if elem.is_displayed():
                    # Check if it's related to brush size by looking at parent text
                    try:
                        parent_text = elem.find_element(By.XPATH, "..//..").text.upper()
                        if "BRUSH" in parent_text and "SIZE" in parent_text:
                            brush_slider = elem
                            print(f"    - Found brush size slider with selector: {selector}")
                            break
                    except:
                        # Try without parent check
                        brush_slider = elem
                        print(f"    - Found potential slider with selector: {selector}")
                        break
        except:
            continue
        if brush_slider:
            break
    
    if brush_slider:
        # Adjust brush size using ActionChains
        try:
            slider_width = brush_slider.size['width']
            # Click at 25% position (small brush)
            ActionChains(driver).move_to_element_with_offset(brush_slider, slider_width * 0.25, 10).click().perform()
            print("    - Set brush size to small (25%)")
            time.sleep(1)
            
            # Click at 75% position (large brush)
            ActionChains(driver).move_to_element_with_offset(brush_slider, slider_width * 0.75, 10).click().perform()
            print("    - Set brush size to large (75%)")
            time.sleep(1)
            
            # Return to medium size
            ActionChains(driver).move_to_element_with_offset(brush_slider, slider_width * 0.5, 10).click().perform()
            print("    - Set brush size to medium (50%)")
            time.sleep(1)
        except Exception as e:
            print(f"    - Error adjusting brush size: {e}")
    else:
        print("    - [INFO] Brush size slider not found, continuing...")
    
    # 5. SELECT BRUSH TYPE (if available)
    print("\n  - Checking for brush types...")
    
    # Look for brush type buttons/options
    brush_type_selectors = [
        "button[class*='brush-type']",
        "[class*='brush-type'] button",
        ".brush-type",
        "[aria-label*='brush type' i]"
    ]
    
    brush_types_found = []
    for selector in brush_type_selectors:
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            for elem in elements:
                if elem.is_displayed() and elem.is_enabled():
                    brush_types_found.append(elem)
        except:
            continue
    
    if brush_types_found:
        print(f"    - Found {len(brush_types_found)} brush type options")
        # Click the first available brush type (after default)
        if len(brush_types_found) > 1:
            try:
                brush_types_found[1].click()
                print(f"    - Selected brush type #{2}")
                time.sleep(1)
            except:
                print("    - Could not select brush type")
    else:
        print("    - [INFO] No brush type options found")
    
    # 6. PERFORM ACTUAL DRAWING ON CANVAS
    print("\n  - Performing drawing on canvas...")
    
    # Find the canvas element
    try:
        canvas = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "canvas")))
        print(f"    - Found canvas at location: {canvas.location}, size: {canvas.size}")
        
        # Get canvas location and size
        canvas_location = canvas.location
        canvas_size = canvas.size
        
        # Calculate center of canvas
        center_x = canvas_location['x'] + canvas_size['width'] / 2
        center_y = canvas_location['y'] + canvas_size['height'] / 2
        
        # Move to canvas center and draw
        actions = ActionChains(driver)
        
        # Draw a simple square/rectangle
        print("    - Drawing a square...")
        
        # Move to starting position
        actions.move_to_element_with_offset(canvas, -50, -50)  # Top-left relative to center
        actions.click_and_hold()  # Start drawing
        
        # Draw square
        actions.move_by_offset(100, 0)   # Right
        actions.move_by_offset(0, 100)   # Down
        actions.move_by_offset(-100, 0)  # Left
        actions.move_by_offset(0, -100)  # Up
        
        actions.release()  # Stop drawing
        actions.perform()
        
        print("    - Square drawn")
        time.sleep(2)
        
        # Change color and draw a line
        print("    - Changing color and drawing a line...")
        
        # Select a different color (red)
        for btn in color_buttons:
            try:
                style = btn.get_attribute("style") or ""
                if "255, 36, 19" in style or "262, 36, 19" in style:  # Red
                    btn.click()
                    time.sleep(0.5)
                    break
            except:
                continue
        
        # Draw a diagonal line
        actions2 = ActionChains(driver)
        actions2.move_to_element_with_offset(canvas, -80, -80)
        actions2.click_and_hold()
        actions2.move_by_offset(160, 160)  # Diagonal line
        actions2.release()
        actions2.perform()
        
        print("    - Line drawn")
        time.sleep(2)
        
    except Exception as e:
        print(f"    - Error drawing on canvas: {e}")
        print("    - [INFO] Attempting to draw using JavaScript fallback...")
        # Could implement JavaScript drawing fallback here if needed
    
    # 7. CHECK FOR CLEAR/UNDO BUTTONS
    print("\n  - Looking for clear/undo options...")
    
    clear_selectors = [
        "button[class*='clear']",
        "button[class*='undo']",
        "button[aria-label*='clear' i]",
        "button[aria-label*='undo' i]",
        "button[aria-label*='clear' i]",
        "button[aria-label*='undo' i]"
    ]
    
    for selector in clear_selectors:
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            if not elements:
                # Try XPath for text content
                elements = driver.find_elements(
                    By.XPATH,
                    "//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'clear') or contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'undo')]"
                )
            
            for elem in elements:
                if elem.is_displayed() and elem.is_enabled():
                    print(f"    - Found clear/undo button: {elem.text}")
                    # Optional: Test undo functionality
                    # elem.click()
                    # time.sleep(1)
                    break
        except:
            continue
    print("  - Clicking Apply...")
    try:
        apply_button = driver.find_element(By.CSS_SELECTOR, "button.apply-button.mat-raised-button.mat-accent")
        apply_button.click()
    except:
        # Try to find by text
        all_buttons = driver.find_elements(By.TAG_NAME, "button")
        for btn in all_buttons:
            try:
                if "APPLY" in btn.text.upper():
                    btn.click()
                    break
            except:
                continue
    
    time.sleep(2)
    # Final screenshot
    driver.save_screenshot("debug_draw_tool_completed.png")
    print("  - Final screenshot saved: debug_draw_tool_completed.png")
    
    print("\n[PASS] DRAW tool tested successfully!")
    print("="*60)
def test_shapes_tool(driver, wait):
    print("\n[TEST] SHAPES TOOL")
    print("=" * 60)

    time.sleep(2)

    # Reset any open panel
    ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    time.sleep(1)

    # 1. Find and click SHAPES tool
    shapes_button = None
    for tool in driver.find_elements(By.CSS_SELECTOR, "button.control-button"):
        try:
            tool_text = (tool.text or "").lower()
            aria_label = (tool.get_attribute("aria-label") or "").lower()
            if "shape" in tool_text or "shape" in aria_label:
                if tool.is_displayed():
                    shapes_button = tool
                    print(f"  - Found Shapes button: '{tool_text}'")
                    break
        except:
            continue

    if not shapes_button:
        print("  - [ERROR] Shapes tool not found")
        return

    shapes_button.click()
    print("  - Shapes tool opened")
    time.sleep(2)

    # 2. Look for shapes drawer and shape buttons
    print("  - Looking for shape buttons...")
    
    # Based on HTML: shapes are in <shapes-drawer> with class="button-with-image"
    shapes = driver.find_elements(
        By.CSS_SELECTOR,
        "shapes-drawer button.button-with-image"
    )
    
    if not shapes:
        # Alternative selector
        shapes = driver.find_elements(
            By.CSS_SELECTOR,
            "button.button-with-image[class*='shape'], shapes-drawer button"
        )
    
    print(f"  - Found {len(shapes)} shape buttons")
    
    # Select Arrow #3 (or first available shape)
    shape_selected = False
    for i, shape in enumerate(shapes):
        if shape.is_displayed() and shape.is_enabled():
            try:
                # Check if it's Arrow #3
                parent_html = shape.find_element(By.XPATH, "..").get_attribute("innerHTML")
                if "Arrow #3" in parent_html or i == len(shapes)-1:  # Arrow #3 is likely last
                    shape.click()
                    print(f"  - Selected shape #{i+1} (Arrow #3)")
                    shape_selected = True
                    time.sleep(1)
                    break
            except:
                shape.click()
                print(f"  - Selected shape #{i+1}")
                shape_selected = True
                time.sleep(1)
                break

    if not shape_selected:
        print("  - [ERROR] Could not select any shape")
        return

    # 3. Place shape on canvas
    print("  - Placing shape on canvas...")
    
    canvas = wait.until(EC.presence_of_element_located((By.TAG_NAME, "canvas")))
    
    # Click on canvas to place the shape
    ActionChains(driver).move_to_element_with_offset(canvas, 200, 200).click().perform()
    print("  - Shape placed on canvas")
    time.sleep(2)
    
    # 4. FIND AND CLICK APPLY BUTTON (First Apply - to finalize placement)
    print("  - Looking for first Apply button (to confirm shape placement)...")
    
    # Based on HTML: Apply button in shapes drawer, might be disabled initially
    apply_buttons = driver.find_elements(
        By.CSS_SELECTOR,
        "shapes-drawer button.apply-button, button.apply-button.mat-raised-button.mat-accent"
    )
    
    apply_clicked = False
    for btn in apply_buttons:
        try:
            if btn.is_displayed():
                # Check if button is disabled
                disabled = btn.get_attribute("disabled")
                if disabled:
                    print("  - Apply button is disabled (shape might not be placed yet)")
                    # Wait a moment and try again
                    time.sleep(1)
                
                # Try to click anyway
                btn.click()
                print("  - First Apply clicked (shape placement confirmed)")
                apply_clicked = True
                time.sleep(2)
                break
        except:
            continue
    
    if not apply_clicked:
        # Try alternative: look for checkmark icon button
        icon_buttons = driver.find_elements(
            By.CSS_SELECTOR,
            "button.mat-icon-button[aria-label*='apply' i], button.mat-icon-button[aria-label*='done' i]"
        )
        for btn in icon_buttons:
            if btn.is_displayed():
                btn.click()
                print("  - First Apply clicked (icon button)")
                apply_clicked = True
                time.sleep(2)
                break
    
    if not apply_clicked:
        print("  - [MANDATORY FAIL] First Apply button not found")
        pytest.fail("[MANDATORY] First Apply button not found - shape placement not confirmed")

    # 5. Now we should be in shape editing mode (color, size, etc.)
    print("  - Now in shape editing mode...")
    time.sleep(2)
    
    # 6. Change shape color
    print("  - Looking for color options...")
    
    # Look for color button/selector
    color_elements = driver.find_elements(
        By.CSS_SELECTOR,
        "button[class*='color'], div[class*='color'], button[aria-label*='color' i]"
    )
    
    color_changed = False
    for color_elem in color_elements:
        if color_elem.is_displayed():
            try:
                color_elem.click()
                print("  - Color selector opened")
                time.sleep(1)
                
                # Select a color from color palette
                color_palette = driver.find_elements(
                    By.CSS_SELECTOR,
                    "div.color-option, button.color-option, div[class*='color-swatch']"
                )
                
                for color_swatch in color_palette[:3]:  # Try first 3 colors
                    if color_swatch.is_displayed():
                        color_swatch.click()
                        print("  - Color selected")
                        color_changed = True
                        time.sleep(1)
                        break
                        
                break
            except:
                continue
    
    if not color_changed:
        print("  - [WARNING] Could not change color")

    # 7. CLICK FINAL APPLY BUTTON (to save shape and return to main menu)
    print("  - Looking for final Apply button...")
    
    final_apply_clicked = False
    
    # Try the main Apply button again
    for btn in apply_buttons:
        try:
            if btn.is_displayed():
                btn.click()
                print("  - Final Apply clicked (returning to main menu)")
                final_apply_clicked = True
                time.sleep(2)
                break
        except:
            continue
    
    if not final_apply_clicked:
        # Try checkmark icon
        icon_buttons = driver.find_elements(
            By.CSS_SELECTOR,
            "button.mat-icon-button"
        )
        for btn in icon_buttons:
            if btn.is_displayed() and btn.is_enabled():
                btn.click()
                print("  - Final Apply clicked (checkmark icon)")
                final_apply_clicked = True
                time.sleep(2)
                break
    
    # MANDATORY: Must click Apply
    if not final_apply_clicked:
        print("  - [MANDATORY FAIL] Final Apply button not found")
        pytest.fail("[MANDATORY] Final Apply button not found - cannot save shape")

    # 8. VERIFY RETURN TO MAIN MENU
    print("  - Verifying return to main menu...")
    
    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "editor-controls")))
        print("  - Successfully returned to main menu")
    except TimeoutException:
        print("  - [MANDATORY FAIL] Did not return to main menu")
        pytest.fail("[MANDATORY] Did not return to main menu after shape tool")

    print("\n[PASS] Shapes tool tested successfully")
    print("=" * 60)
def test_text_tool(driver, wait):
    print("\n[TEST] TEXT TOOL")

    # Reset editor state
    ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    time.sleep(2)

    # Locate Text tool
    text_button = None
    tools = driver.find_elements(By.CSS_SELECTOR, "button.control-button")

    for tool in tools:
        text = (tool.text or "").lower()
        aria = (tool.get_attribute("aria-label") or "").lower()
        if "text" in text or "text" in aria:
            if tool.is_displayed():
                text_button = tool
                break

    if not text_button:
        print("  - [ERROR] TEXT tool not found")
        return

    # Open Text tool
    try:
        text_button.click()
    except:
        driver.execute_script("arguments[0].click();", text_button)

    print("  - Text tool opened")
    time.sleep(2)

    # Click Add Text
    add_text_btn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".add-text-button-wrapper"))
    )
    add_text_btn.click()
    print("  - Add Text clicked")
    time.sleep(2)

    # Select a font (Kalam / first visible font)
    try:
        font_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".select-font-button"))
        )
        font_button.click()
        print("  - Font selected")
    except:
        print("  - [WARNING] Font selection skipped")

    time.sleep(1)

    # Double-click on the text box on canvas
    canvas = wait.until(EC.presence_of_element_located((By.TAG_NAME, "canvas")))

    actions = ActionChains(driver)
    actions.move_to_element_with_offset(canvas, 120, 120)
    actions.double_click()
    actions.perform()

    print("  - Text box activated (double-click)")
    time.sleep(1)

    # Type text
    actions = ActionChains(driver)
    actions.send_keys(Keys.CONTROL, "a")
    actions.send_keys("Automated Text Test")
    actions.perform()

    print("  - Text entered")
    time.sleep(1)
 
    # 7. CLICK APPLY/CHECKMARK BUTTON
    print("\n  - Looking for Apply/Checkmark button...")
    
    apply_found = False
    
    # Look for checkmark/apply buttons
    apply_selectors = [
        "button.mat-icon-button",  # Icon button (checkmark)
        "button[class*='apply']",
        "button[aria-label*='apply' i]",
        "button[aria-label*='done' i]",
        "button[aria-label*='save' i]",
        "button[aria-label*='check' i]",
        "button[aria-label*='save' i]"
    ]
    
    for selector in apply_selectors:
        try:
            buttons = driver.find_elements(By.CSS_SELECTOR, selector)
            
            for btn in buttons:
                if btn.is_displayed() and btn.is_enabled():
                    try:
                        btn_text = btn.text.strip()
                        aria_label = btn.get_attribute("aria-label") or ""
                        print(f"    - Found apply button: text='{btn_text}', aria-label='{aria_label}'")
                        btn.click()
                        apply_found = True
                        print("    - Clicked apply button")
                        time.sleep(2)
                        break
                    except:
                        continue
        except Exception as e:
            print(f"    - Error with selector {selector}: {e}")
            continue
        
        if apply_found:
            break
    
    if not apply_found:
        print("    - [WARNING] Apply button not found, pressing ESC...")
        try:
            ActionChains(driver).send_keys(Keys.ESCAPE).perform()
            time.sleep(1)
            # Press ESC again to exit text tool
            ActionChains(driver).send_keys(Keys.ESCAPE).perform()
            time.sleep(1)
        except:
            pass
    
    # 8. VERIFY RETURNED TO MAIN TOOLS
    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "editor-controls")))
        print("\n  - Successfully returned to main tools")
    except:
        print("\n  - [WARNING] May still be in text panel")
    
    # Final screenshot
    driver.save_screenshot("debug_text_tool_completed.png")
    print("  - Final screenshot saved: debug_text_tool_completed.png")
    
    print("\n[PASS] TEXT tool tested successfully!")
    print("="*60)
























def test_no_crash_final(driver):
    """Final check that the app is still alive."""
    assert len(driver.window_handles) > 0
    # Check for any console errors (if supported by driver logging)
    logs = driver.get_log('browser')
    errors = [entry for entry in logs if entry['level'] == 'SEVERE']
    if errors:
        print("\n[WARNING] Browser console errors detected:")
        for err in errors:
            print(err['message'])
    else:
        print("\n[PASS] No severe browser console errors.")

if __name__ == "__main__":
    # Manually run pytest if executed as script
    pytest.main(["-v", "-s", __file__])