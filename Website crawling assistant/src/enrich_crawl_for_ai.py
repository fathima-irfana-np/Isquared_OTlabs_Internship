import json
from collections import defaultdict
from urllib.parse import urlparse

INPUT_FILE = "data/crawl_results.json"
OUTPUT_FILE = "data/ai_exploration_snapshot.json"


def normalize_text(text):
    return text.strip() if text and text != "unnamed_element" else None


def classify_elements(elements):
    ui_groups = defaultdict(list)

    for el in elements:
        tag = el.get("type")
        text = normalize_text(el.get("text"))
        href = el.get("href")
        el_id = el.get("id")
        action = el.get("action")

        if href:
            ui_groups["links"].append(text or href)
        elif tag == "button":
            ui_groups["buttons"].append(text or el_id)
        elif tag == "input":
            ui_groups["inputs"].append(text or el_id)
        elif action:
            ui_groups["interactive_widgets"].append(text or el_id)
        else:
            ui_groups["unknown_clickables"].append(text or el_id)

    for k in ui_groups:
        ui_groups[k] = sorted(set(filter(None, ui_groups[k])))

    return dict(ui_groups)


def infer_page_context(functional_elements, state_transitions):
    urls = [t["from"] for t in state_transitions] if state_transitions else []
    base_url = urls[0] if urls else "unknown"

    parsed = urlparse(base_url)

    return {
        "url": base_url,
        "domain": parsed.netloc,
        "page_path": parsed.path or "/",
        "ui_density": len(functional_elements)
    }


def derive_available_actions(ui_groups):
    actions = []

    if ui_groups.get("links"):
        actions.append("navigate via links")

    if ui_groups.get("buttons"):
        actions.append("trigger button actions")

    if ui_groups.get("inputs"):
        actions.append("enter data into input fields")

    if ui_groups.get("interactive_widgets"):
        actions.append("interact with dynamic UI elements")

    return actions


def main():
    with open(INPUT_FILE, "r") as f:
        crawl_data = json.load(f)

    functional_elements = crawl_data.get("functional_elements", [])
    state_transitions = crawl_data.get("state_transitions", [])

    ui_inventory = classify_elements(functional_elements)
    page_context = infer_page_context(functional_elements, state_transitions)
    available_actions = derive_available_actions(ui_inventory)

    ai_snapshot = {
        "metadata": {
            "source": "selenium_exploratory_crawler",
            "generated_from": INPUT_FILE
        },
        "page_context": page_context,
        "ui_inventory": ui_inventory,
        "available_actions": available_actions,
        "state_transitions": state_transitions,
        "exploration_hints": {
            "focus_areas": [
                "form validation",
                "navigation consistency",
                "dynamic UI behavior",
                "error handling"
            ],
            "unknown_risks": [
                "authentication flows",
                "hidden UI states",
                "async race conditions"
            ]
        }
    }

    with open(OUTPUT_FILE, "w") as f:
        json.dump(ai_snapshot, f, indent=2)

    print(f" Generic AI snapshot created: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
