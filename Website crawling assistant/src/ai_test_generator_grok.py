"""
AI Test Generator — Generic Exploratory Test Case Engine
Uses Groq API to generate grounded, non-hallucinated test cases
from any website's exploration snapshot.

Anti-Hallucination Strategy:
  Layer 1: Model upgrade (llama-3.3-70b-versatile)
  Layer 2: Label whitelist injection (constrains AI vocabulary)
  Layer 3: Post-generation validation (see validator.py)
"""

import json
import re
import os
import time
import random
import requests
import dotenv

dotenv.load_dotenv()

# ── Configuration ──────────────────────────────────────────────
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_ENDPOINT = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama-3.3-70b-versatile"  # Layer 1: 70B model for better instruction following

INPUT_FILE = "data/ai_exploration_snapshot.json"
OUTPUT_FILE = "data/generated_test_cases.json"

MAX_PROMPT_CHARS = 60000   # 70B model supports 131K tokens (~500K chars)
MAX_TOKENS = 4096
NUM_BATCHES = 6            # 6 batches × ~10 tests = ~60 raw tests
BATCH_DELAY_SEC = 45       # Delay between batches for rate limiting


# ── Layer 2: Page-Grouped Whitelist Extraction ────────────────

def extract_whitelist(snapshot):
    """
    Extracts valid labels GROUPED BY PAGE.
    Each page lists its own inputs and buttons, preventing cross-page mixing.
    """
    page_vocab = []

    for page in snapshot.get("pages", []):
        ctx = page.get("page_context", {})
        path = ctx.get("page_path") or ctx.get("url", "")
        if not path:
            continue

        inventory = page.get("ui_inventory", {})
        inputs = []
        buttons = []

        for el in inventory.get("inputs", []):
            label = el.get("label", "")
            if label and label not in ("unnamed", "unnamed_element", ""):
                inputs.append(label)

        for el in inventory.get("buttons", []):
            label = el.get("label", "")
            if label and label not in ("unnamed", "unnamed_element", ""):
                buttons.append(label)

        # Only include pages with interactive elements
        if inputs or buttons:
            page_vocab.append({
                "page": path,
                "inputs": sorted(set(inputs)),
                "buttons": sorted(set(buttons)),
            })

    return page_vocab


def build_snapshot_context(snapshot):
    """
    Builds a compact, AI-friendly representation of the snapshot.
    Generic: works with any site structure.
    """
    pages_summary = []
    for page in snapshot.get("pages", []):
        ctx = page.get("page_context", {})
        inventory = page.get("ui_inventory", {})

        # Only include pages with interactive elements
        inputs = inventory.get("inputs", [])
        buttons = inventory.get("buttons", [])
        if not inputs and not buttons:
            continue

        page_info = {
            "path": ctx.get("page_path") or ctx.get("url"),
            "title": ctx.get("title", ""),
            "inputs": [],
            "buttons": []
        }

        for el in inputs:
            entry = {"label": el.get("label")}
            val = el.get("validation", {})
            clean_val = {k: v for k, v in val.items() if v and v is not True}
            if clean_val:
                entry["validation"] = clean_val
            page_info["inputs"].append(entry)

        for el in buttons:
            page_info["buttons"].append({"label": el.get("label")})

        pages_summary.append(page_info)

    return pages_summary


# Each batch is assigned a distinct adversarial exploration category.
# This guarantees structural diversity across all batches — not just topical variation.
BATCH_FOCUSES = [
    {
        "name": "Input Torture & Field Poisoning",
        "brief": (
            "Attack input fields with edge-case values:\n"
            "- Paste-style long strings (999999999, 0.000001, -0.01)\n"
            "- Special characters and dangerous strings (e.g. spaces-only, 0, -1, alphanumerics)\n"
            "- Exceeding min/max limits by 1 step (e.g. max+1, min-1)\n"
            "- Cross-field contamination: fill one field, copy into another with extra chars\n"
            "- Empty or whitespace-only required fields before submitting\n"
            "DO NOT repeat negative input tests. Focus on DIFFERENT fields each test."
        )
    },
    {
        "name": "State Transitions & Form Abandonment",
        "brief": (
            "Test how the app handles partial or interrupted user flows:\n"
            "- Fill 50-80%  of a form then navigate away via a link, then return\n"
            "- Fill all fields, click Calculate, then modify a single field and recalculate (does output update?)\n"
            "- Navigate forward to result, hit browser back, check if form resets or retains values\n"
            "- Change a value mid-form without submitting, navigate away, return (state persistence?)\n"
            "- Submit, see result, then change inputs without clearing result first"
        )
    },
    {
        "name": "Boundary Value Analysis",
        "brief": (
            "Probe every numeric input at its limits:\n"
            "- Exact minimum allowed value\n"
            "- Exact maximum allowed value\n"
            "- One below minimum (min - 1)\n"
            "- One above maximum (max + 1)\n"
            "- Zero where non-zero is expected\n"
            "- A very large number (e.g. 9999999999)\n"
            "- A very small decimal (e.g. 0.0001)\n"
            "Each test case should target a DIFFERENT input field."
        )
    },
    {
        "name": "Multi-Step Interaction & Navigation Chaos",
        "brief": (
            "Test complex navigation sequences:\n"
            "- Navigate to page A, fill form, navigate to page B, navigate back to A (are values retained?)\n"
            "- Navigate to page A, change mode/tab to page B, return to A via breadcrumb\n"
            "- Open the same calculator twice in sequence and verify independent operation\n"
            "- Fill inputs on page A, use a navigation link to jump to a related page mid-flow\n"
            "- Use a link in the header/footer to interrupt an in-progress calculation\n"
            "Each test MUST involve navigating between at least 2 different pages."
        )
    },
    {
        "name": "Mode Switching & UI State Dances",
        "brief": (
            "Stress-test toggle/mode buttons and UI state changes:\n"
            "- Switch between two calculation modes on the same page\n"
            "- Enter values in mode A, switch to mode B, switch back (are values retained?)\n"
            "- Click a toggle/tab before all fields are filled, then fill and submit\n"
            "- Rapidly apply and unapply a mode, check for UI flicker or race conditions\n"
            "- Click a mode button that changes labels — do old values still map to new labels?\n"
            "Only test pages that have multiple tabs, toggles, or mode switches."
        )
    },
    {
        "name": "Error Recovery & Validation Resilience",
        "brief": (
            "Test how the app handles and recovers from error states:\n"
            "- Submit empty form, note error, fix only one field, submit again\n"
            "- Submit with invalid value, correct it, submit again — does error clear properly?\n"
            "- Trigger a calculation error (e.g. divide by zero scenario), then provide valid input\n"
            "- Clear all fields after a successful calculation, submit empty\n"
            "- Enter valid data, click Clear/Reset, verify all fields and result are cleared\n"
            "Focus on the APP'S RESPONSE TO RECOVERY, not just the initial bad input."
        )
    },
]


def build_prompt(snapshot, batch_index, total_batches):
    """
    Builds a category-driven adversarial prompt.
    Each batch targets a distinct exploration focus for structural diversity.
    Generic: no site-specific terminology.
    """
    page_vocab = extract_whitelist(snapshot)
    context = build_snapshot_context(snapshot)
    context_text = json.dumps(context, indent=1)

    if len(context_text) > MAX_PROMPT_CHARS:
        context_text = context_text[:MAX_PROMPT_CHARS]

    # Rotate through exploration categories
    focus = BATCH_FOCUSES[batch_index % len(BATCH_FOCUSES)]

    # Format whitelist as PAGE-GROUPED constraint block
    wl_lines = ["PAGE-SPECIFIC VOCABULARY (ONLY use elements listed under the page you navigate to):"]
    for pv in page_vocab:
        wl_lines.append(f"  Page '{pv['page']}':")
        if pv["inputs"]:
            wl_lines.append("    Inputs: " + ", ".join(pv["inputs"]))
        if pv["buttons"]:
            wl_lines.append("    Buttons: " + ", ".join(pv["buttons"]))
    wl_block = "\n".join(wl_lines)

    start_id = batch_index * 10 + 1

    return (
        f"You are generating batch {batch_index + 1} of {total_batches} exploratory test cases.\n"
        "\n"
        "ROLE: Senior SDET performing adversarial exploratory testing. Your goal is to BREAK the app.\n"
        "\n"
        "=== STRICT RULES (violations are automatically rejected) ===\n"
        "1. Each test targets ONE page. Only use input/button labels listed under THAT page.\n"
        "   BAD: Navigate to '/loan-calculator.html' then Click 'sin' (sin is on '/' not on '/loan-calculator.html')\n"
        "   GOOD: Navigate to '/loan-calculator.html' then Click 'Calculate' (Calculate is listed under that page)\n"
        "2. Every page path MUST be from the vocabulary below.\n"
        "3. Generate exactly 8-10 test cases. Each must be unique in goal AND step sequence.\n"
        "4. Each test must have 3-6 concrete, executable steps.\n"
        "5. Do NOT repeat tests from other batches. No password/login tests unless site has auth pages.\n"
        "\n"
        f"=== THIS BATCH FOCUS: {focus['name']} ===\n"
        f"{focus['brief']}\n"
        "\n"
        f"{wl_block}\n"
        "\n"
        "APPLICATION CONTEXT:\n"
        f"{context_text}\n"
        "\n"
        "OUTPUT FORMAT (JSON only — no prose, no markdown, no explanations):\n"
        "{\n"
        '  "generated_tests": [\n'
        "    {\n"
        f'      "id": "ET-{start_id:02d}",\n'
        '      "goal": "one-line adversarial goal",\n'
        '      "steps": ["Navigate to \'/path\'", "Enter \'value\' into \'exact_label\'", "Click \'exact_label\'"],\n'
        '      "expected": "precise observable outcome"\n'
        "    }\n"
        "  ]\n"
        "}"
    )


# ── API Layer with Resilience ──────────────────────────────────

def repair_json(json_str):
    """Repairs common AI JSON output issues."""
    json_str = json_str.strip()

    # Strip markdown fences
    if json_str.startswith("```"):
        json_str = re.sub(r'^```(?:json)?\s*|\s*```$', '', json_str, flags=re.MULTILINE)

    # Fix unclosed brackets using stack
    stack = []
    for ch in json_str:
        if ch == '{': stack.append('}')
        elif ch == '[': stack.append(']')
        elif ch in '}]' and stack and stack[-1] == ch:
            stack.pop()
    json_str += "".join(reversed(stack))

    return json_str


def call_groq(prompt, retries=5, base_delay=10):
    """Calls Groq API with exponential backoff for rate limits."""
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are a test case generator. Output ONLY valid JSON. No markdown, no explanations."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.4,  # Slight creativity for diverse batches
        "max_tokens": MAX_TOKENS
    }

    for attempt in range(retries):
        try:
            response = requests.post(GROQ_ENDPOINT, headers=headers, json=payload, timeout=90)

            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]

            elif response.status_code == 429:
                wait = (base_delay * (2 ** attempt)) + random.uniform(1, 3)
                print(f"   ⏳ Rate limit hit. Waiting {wait:.0f}s... (attempt {attempt + 1}/{retries})")
                time.sleep(wait)
                continue

            else:
                print(f"   ❌ API Error {response.status_code}: {response.text[:200]}")
                response.raise_for_status()

        except requests.exceptions.Timeout:
            print(f"   ⏳ Timeout. Retrying... (attempt {attempt + 1}/{retries})")
            time.sleep(base_delay)
            continue

    raise RuntimeError(f"Failed after {retries} attempts.")


def parse_ai_output(raw_output):
    """Extracts and parses JSON from AI output."""
    start = raw_output.find("{")
    end = raw_output.rfind("}") + 1
    if start == -1 or end == 0:
        raise ValueError("No JSON object found in AI output")

    raw_json = raw_output[start:end]

    try:
        return json.loads(raw_json)
    except json.JSONDecodeError:
        repaired = repair_json(raw_json)
        return json.loads(repaired)


# ── Main Pipeline ──────────────────────────────────────────────

def main():
    print("=" * 60)
    print("🚀 AI Exploratory Test Generator v2.0 (Anti-Hallucination)")
    print("=" * 60)

    if not os.path.exists(INPUT_FILE):
        print(f"❌ Error: {INPUT_FILE} not found.")
        return

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        snapshot = json.load(f)

    # Show whitelist summary
    page_vocab = extract_whitelist(snapshot)
    total_inputs = sum(len(pv["inputs"]) for pv in page_vocab)
    total_buttons = sum(len(pv["buttons"]) for pv in page_vocab)
    print(f"📋 Whitelist: {len(page_vocab)} pages, {total_inputs} inputs, {total_buttons} buttons (page-grouped)")

    all_tests = []

    for batch in range(NUM_BATCHES):
        print(f"\n── Batch {batch + 1}/{NUM_BATCHES} ──")
        prompt = build_prompt(snapshot, batch, NUM_BATCHES)

        try:
            raw_output = call_groq(prompt)
            parsed = parse_ai_output(raw_output)
            batch_tests = parsed.get("generated_tests", [])

            # Re-number IDs to avoid duplicates across batches
            for i, test in enumerate(batch_tests):
                test["id"] = f"ET-{batch * 10 + i + 1:02d}"

            all_tests.extend(batch_tests)
            print(f"   ✅ Got {len(batch_tests)} tests (total: {len(all_tests)})")

        except Exception as e:
            print(f"   ❌ Batch {batch + 1} failed: {str(e)}")

        # Rate limit delay between batches (skip after last batch)
        if batch < NUM_BATCHES - 1:
            print(f"   ⏳ Waiting {BATCH_DELAY_SEC}s before next batch...")
            time.sleep(BATCH_DELAY_SEC)

    # Save all generated tests
    output = {"generated_tests": all_tests}
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

    print(f"\n{'=' * 60}")
    print(f"✅ Complete: {len(all_tests)} raw test cases saved to {OUTPUT_FILE}")
    print(f"📌 Next: Run 'python src/validator.py' to validate against snapshot")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
