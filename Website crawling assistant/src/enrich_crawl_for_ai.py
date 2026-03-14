import json
import os
from collections import defaultdict
from urllib.parse import urlparse

INPUT_FILE = "data/crawl_results.json"
OUTPUT_FILE = "data/ai_exploration_snapshot.json"

MAX_LINKS_PER_PAGE = 20


# -------------------------------------------------
# Utilities
# -------------------------------------------------

def clean_label(label):
    if not label:
        return None

    label = label.strip()

    if label.lower() in ["unnamed", "unnamed_element"]:
        return None

    # Remove extremely long noisy labels (graphs, blocks)
    if len(label) > 120:
        return None

    # Remove pure symbol junk except common UI controls
    if len(label) == 1 and label not in ["=", "+", "-", "*", "/"]:
        return None

    return label


def is_anchor_link(href):
    return href.endswith("#") if href else False


def is_external_link(href, domain):
    if not href:
        return False
    parsed = urlparse(href)
    return parsed.netloc and parsed.netloc != domain


def meaningful_element(label, el_id, name):
    return any([label, el_id, name])


# -------------------------------------------------
# Classification
# -------------------------------------------------

def classify_elements(elements, page_domain):
    ui_groups = defaultdict(list)
    seen_links = set()

    for el in elements:
        tag = el.get("type")
        role = el.get("role")
        href = el.get("href")
        el_id = el.get("id")
        name = el.get("name")
        validation = el.get("validation", {})

        label = clean_label(el.get("label"))

        if not meaningful_element(label, el_id, name):
            continue

        final_label = label or el_id or name

        el_repr = {
            "type": tag,
            "role": role,
            "label": final_label
        }

        # Keep meaningful validation only
        if validation:
            filtered_validation = {
                k: v for k, v in validation.items()
                if v not in [None, "", False]
            }
            if filtered_validation:
                el_repr["validation"] = filtered_validation

        # ---------------- LINKS ----------------
        if href:
            if is_external_link(href, page_domain):
                continue

            if is_anchor_link(href):
                continue

            if href in seen_links:
                continue

            seen_links.add(href)
            el_repr["href"] = href
            ui_groups["links"].append(el_repr)

        # ---------------- BUTTONS ----------------
        elif tag == "button" or role == "action":
            ui_groups["buttons"].append(el_repr)

        # ---------------- INPUTS ----------------
        elif tag == "input" and role in ["form_input", "selection"]:
            ui_groups["inputs"].append(el_repr)

        # ---------------- DROPDOWNS ----------------
        elif tag == "select":
            ui_groups["dropdowns"].append(el_repr)

        # Ignore svg/visual-only elements
        elif tag in ["svg", "path", "g"]:
            continue

        else:
            ui_groups["other_clickables"].append(el_repr)

    # Limit excessive navigation links
    if "links" in ui_groups:
        ui_groups["links"] = ui_groups["links"][:MAX_LINKS_PER_PAGE]

    return dict(ui_groups)


# -------------------------------------------------
# Page Intelligence (Domain Agnostic)
# -------------------------------------------------

def infer_page_type(inputs_count, buttons_count, links_count):
    if inputs_count >= 3:
        return "form-heavy"

    if buttons_count >= 3 and inputs_count > 0:
        return "interactive"

    if links_count > inputs_count:
        return "navigation-heavy"

    return "content"


def compute_interaction_score(ui_groups):
    score = 0
    score += len(ui_groups.get("inputs", [])) * 3
    score += len(ui_groups.get("dropdowns", [])) * 2
    score += len(ui_groups.get("buttons", [])) * 2
    return score


# -------------------------------------------------
# Main
# -------------------------------------------------

def main():
    if not os.path.exists(INPUT_FILE):
        print(f"Error: {INPUT_FILE} not found.")
        return

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        crawl_data = json.load(f)

    pages = crawl_data.get("pages", [])
    enriched_pages = []

    for page in pages:
        url = page.get("page_url", "")
        title = page.get("page_title", "")
        parsed = urlparse(url)
        domain = parsed.netloc

        raw_elements = page.get("elements", [])
        ui_inventory = classify_elements(raw_elements, domain)

        inputs_count = len(ui_inventory.get("inputs", []))
        buttons_count = len(ui_inventory.get("buttons", []))
        links_count = len(ui_inventory.get("links", []))

        page_type = infer_page_type(inputs_count, buttons_count, links_count)
        interaction_score = compute_interaction_score(ui_inventory)

        enriched_pages.append({
            "page_context": {
                "url": url,
                "title": title,
                "domain": domain,
                "page_path": parsed.path or "/",
                "page_type": page_type,
                "interaction_score": interaction_score,
                "ui_density": len(raw_elements)
            },
            "ui_inventory": ui_inventory
        })

    ai_snapshot = {
        "metadata": {
            "source": "selenium_exploratory_crawler",
            "generated_at": crawl_data.get("crawl_timestamp"),
            "total_pages": len(enriched_pages)
        },
        "pages": enriched_pages
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(ai_snapshot, f, indent=2)

    print("✅ Generic AI snapshot created.")
    print(f"Pages processed: {len(enriched_pages)}")


if __name__ == "__main__":
    main()