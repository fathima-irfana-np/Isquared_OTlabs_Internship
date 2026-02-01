import re
import time
from playwright.sync_api import Page, Locator

class SmartResolver:
    def __init__(self, page: Page):
        self.page = page

    def resolve_actionable_element(self, intent: str, roles=None, find_input=False):
        """
        Heuristically finds an element based on intent text.
        Tries roles like 'button', 'link', 'textbox' if provided.
        """
        # 1. Try direct role match (exact text)
        if roles:
            for role in roles:
                try:
                    loc = self.page.get_by_role(role, name=re.compile(f"^{intent}$", re.IGNORECASE), include_hidden=False)
                    if loc.count() > 0:
                        return loc.first
                except:
                    continue

        # 2. Try by label/placeholder/text
        # If we are looking for an input (find_input=True), we favor get_by_label
        if find_input:
            try:
                loc = self.page.get_by_label(intent, exact=False)
                if loc.count() > 0: return loc.first
                loc = self.page.get_by_placeholder(intent, exact=False)
                if loc.count() > 0: return loc.first
            except: pass

        # 3. Generic text match
        try:
            loc = self.page.get_by_text(intent, exact=False)
            if loc.count() > 0:
                # If we need an input but found a <td> or <span>, we must look "near" it
                found = loc.first
                tag = found.evaluate("el => el.tagName.toLowerCase()")
                if find_input and tag not in ["input", "textarea", "select"]:
                    # Look for nearest input inside the parent row or container
                    # We can use the 'near' locator if supported, but simple relative selection is often faster
                    return self.page.locator("input, textarea, select").filter(has_not=self.page.get_by_text(intent)).near(found).first
                return found
        except:
            pass

        return None

    def smart_click(self, intent: str):
        print(f"Propagating Click Intent: '{intent}'")
        el = self.resolve_actionable_element(intent, roles=["button", "link", "tab"])
        if el:
            el.click()
            self.page.wait_for_load_state("domcontentloaded")
            return True
        return False

    def smart_fill(self, intent: str, value: str):
        print(f"Propagating Fill Intent: '{intent}' -> '{value}'")
        el = self.resolve_actionable_element(intent, find_input=True)
        if el:
            try:
                el.fill(value)
                return True
            except Exception as e:
                print(f"Fill failed on resolved element, trying manual type: {e}")
                el.focus()
                self.page.keyboard.type(value)
                return True
        return False
