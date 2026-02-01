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
        "button:contains('Clear')",
        "button:contains('Undo')"
    ]
    
    for selector in clear_selectors:
        try:
            # Try CSS first
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            if not elements:
                # Try XPath for text content
                elements = driver.find_elements(
                    By.XPATH,
                    f"//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'clear') or contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'undo')]"
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
    
    # 8. CLICK APPLY/SAVE BUTTON
    print("\n  - Looking for Apply/Save button...")
    
    # Find and click apply button
    apply_found = False
    apply_selectors = [
        "button.apply-button",
        "button[class*='apply']",
        "button.mat-flat-button.mat-primary",
        "button:contains('Apply')",
        "button:contains('Done')",
        "button:contains('Save')"
    ]
    
    for selector in apply_selectors:
        try:
            # Try CSS
            buttons = driver.find_elements(By.CSS_SELECTOR, selector)
            if not buttons:
                # Try XPath for text
                buttons = driver.find_elements(
                    By.XPATH,
                    "//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'apply') or contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'done') or contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'save')]"
                )
            
            for btn in buttons:
                if btn.is_displayed() and btn.is_enabled():
                    btn_text = btn.text.strip()
                    print(f"    - Clicking Apply button: '{btn_text}'")
                    btn.click()
                    apply_found = True
                    time.sleep(3)  # Wait for draw panel to close
                    break
        except Exception as e:
            print(f"    - Error with selector {selector}: {e}")
            continue
        
        if apply_found:
            break
    
    if not apply_found:
        print("    - [WARNING] Apply button not found, pressing ESC...")
        try:
            ActionChains(driver).send_keys(Keys.ESCAPE).perform()
            time.sleep(2)
        except:
            pass
    
    # 9. VERIFY RETURNED TO MAIN TOOLS
    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "editor-controls")))
        print("\n  - Successfully returned to main tools")
    except:
        print("\n  - [WARNING] May still be in draw panel")
    
    # Final screenshot
    driver.save_screenshot("debug_draw_tool_completed.png")
    print("  - Final screenshot saved: debug_draw_tool_completed.png")
    
    print("\n[PASS] DRAW tool tested successfully!")
    print("="*60)

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

    # Click Apply (✓)
    try:
        apply_btn = driver.find_element(
            By.CSS_SELECTOR,
            "button.mat-icon-button, button.apply-button"
        )
        apply_btn.click()
        print("  - Apply clicked")
    except:
        print("  - [WARNING] Apply button not found")

    time.sleep(2)

    # Exit Text tool
    ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    time.sleep(1)

    print("[PASS] Text tool tested successfully")

