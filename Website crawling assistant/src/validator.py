"""
Post-Generation Validator — Layer 3 of Anti-Hallucination Defense
Validates AI-generated test cases against the exploration snapshot.

Generic: Works with any website's snapshot, not site-specific.

Checks:
  1. Label grounding: every element label used in steps must exist in the snapshot
  2. Path grounding: every page path referenced must exist in the snapshot
  3. Structural validity: each test must have id, goal, steps, expected
"""

import json
import os
import re

INPUT_SNAPSHOT = "data/ai_exploration_snapshot.json"
INPUT_TESTS    = "data/generated_test_cases.json"
OUTPUT_VALID   = "data/validated_test_cases.json"
OUTPUT_REJECTED= "data/rejected_test_cases.json"


def build_label_index(snapshot):
    page_labels  = {}
    global_labels= set()
    global_paths = set()

    for page in snapshot.get("pages", []):
        ctx  = page.get("page_context", {})
        path = ""
        for key in ("page_path", "url"):
            val = ctx.get(key, "")
            if val:
                path = val.lower().strip()
                global_paths.add(path)

        page_local = set()
        title = ctx.get("title", "")
        if title:
            page_local.add(title.lower().strip())

        inventory = page.get("ui_inventory", {})
        for category, elements in inventory.items():
            for el in elements:
                label = el.get("label", "")
                if label and label not in ("unnamed", "unnamed_element"):
                    page_local.add(label.lower().strip())
                for alt_key in ("id", "name"):
                    alt = el.get(alt_key, "")
                    if alt:
                        page_local.add(alt.lower().strip())

        if path:
            page_labels[path] = page_local
        global_labels.update(page_local)

    return page_labels, global_labels, global_paths


def extract_ui_labels_from_step(step_text):
    """
    Smartly extract ONLY the UI element labels from a step,
    NOT the test input values.

    Patterns handled:
      "Enter 'VALUE' into 'LABEL'"  → only LABEL is checked
      "Click 'LABEL'"               → LABEL is checked
      "Navigate to 'PATH'"          → PATH is checked (as path, not label)
      "Leave 'LABEL' empty"         → LABEL is checked

    Returns list of (quoted_string, is_path) tuples.
    """
    results = []

    # Pattern: Enter 'value' into 'label'
    # Only extract the LABEL (second quoted string), skip the VALUE (first)
    enter_into = re.match(
        r"(?i)enter\s+['\"]([^'\"]*)['\"](?:\s+\d+\s+times)?\s+into\s+['\"]([^'\"]+)['\"]",
        step_text.strip()
    )
    if enter_into:
        # enter_into.group(1) = the VALUE  → skip
        # enter_into.group(2) = the LABEL  → check this
        label = enter_into.group(2)
        if label.strip():
            results.append((label, False))
        return results

    # Pattern: Copy and paste ... into 'label'
    copy_into = re.search(r"(?i)into\s+['\"]([^'\"]+)['\"]", step_text)
    if copy_into:
        results.append((copy_into.group(1), False))
        return results

    # Pattern: Navigate to 'path'
    nav = re.match(r"(?i)navigate(?:\s+back)?\s+to\s+['\"]([^'\"]+)['\"]", step_text.strip())
    if nav:
        results.append((nav.group(1), True))  # is_path=True
        return results

    # Pattern: Click 'label' / Leave 'label' empty / Select 'label' etc.
    # Extract ALL quoted strings — these are UI labels
    for m in re.finditer(r"['\"]([^'\"]+)['\"]", step_text):
        val = m.group(1).strip()
        if val:
            results.append((val, False))

    return results


def is_test_data(value):
    """
    Returns True if the value is clearly test input data,
    NOT a UI element label. These should never be validated
    against the snapshot.
    """
    v = value.strip()

    # Empty string
    if not v:
        return True

    # Pure numbers, decimals, negative numbers
    if re.match(r'^-?\d+\.?\d*$', v):
        return True

    # Email addresses
    if "@" in v:
        return True

    # Strings with HTML/injection chars
    if any(c in v for c in ['<', '>', ';', '--', '!@#']):
        return True

    # Repeated characters (like 'a' 256 times, or long random strings)
    if len(v) > 30:
        return True

    # Whitespace only
    if v.isspace():
        return True

    # Generic test words that are values, not UI labels
    TEST_WORDS = {
        'invalid', 'valid', 'test', 'abc', 'null', 'undefined',
        'nan', 'true', 'false', 'none', 'on', 'off', 'yes', 'no',
        'new@example.com', 'test@example.com', 'test2@example.com',
        'valid@example.com',
    }
    if v.lower() in TEST_WORDS:
        return True

    # Looks like a test value (spaces only string that somehow passed)
    if re.match(r'^\s+$', v):
        return True

    return False


def validate_test_case(test, page_labels, global_labels, valid_paths):
    issues = []

    # Structural checks
    if not test.get("id"):
        issues.append("Missing 'id'")
    if not test.get("goal"):
        issues.append("Missing 'goal'")
    if not test.get("steps") or not isinstance(test["steps"], list):
        issues.append("Missing or invalid 'steps'")
        return False, issues
    if not test.get("expected"):
        issues.append("Missing 'expected'")
    if len(test.get("steps", [])) < 2:
        issues.append("Too few steps (minimum 2)")

    # Extract target page from first Navigate step
    target_page = None
    for step_text in test.get("steps", []):
        nav_match = re.match(r"(?i)navigate(?:\s+back)?\s+to\s+['\"](.+?)['\"]", step_text)
        if nav_match:
            target_page = nav_match.group(1).lower().strip()
            break

    # Get page-specific labels (fallback to global)
    if target_page and target_page in page_labels:
        valid_labels = page_labels[target_page]
    else:
        valid_labels = global_labels

    # Validate each step
    for i, step_text in enumerate(test.get("steps", [])):
        refs = extract_ui_labels_from_step(step_text)

        for ref, is_path in refs:
            ref_lower = ref.lower().strip()

            if is_path:
                # Validate as a page path
                if ref_lower not in valid_paths:
                    issues.append(f"Step {i+1}: Unknown path '{ref}'")
                continue

            # Skip if it's clearly test data / input value
            if is_test_data(ref):
                continue

            # Validate as a UI label
            if ref_lower not in valid_labels:
                if ref_lower in global_labels:
                    issues.append(
                        f"Step {i+1}: Cross-page label '{ref}' "
                        f"(exists on another page, not '{target_page}')"
                    )
                else:
                    fuzzy = any(ref_lower in vl or vl in ref_lower for vl in valid_labels)
                    if not fuzzy:
                        issues.append(f"Step {i+1}: Hallucinated label '{ref}'")

    return len(issues) == 0, issues


def main():
    print("=" * 60)
    print("🔍 Post-Generation Validator v1.1 (Anti-Hallucination Layer 3)")
    print("=" * 60)

    if not os.path.exists(INPUT_SNAPSHOT):
        print(f"❌ Error: {INPUT_SNAPSHOT} not found.")
        return
    with open(INPUT_SNAPSHOT, "r", encoding="utf-8") as f:
        snapshot = json.load(f)

    if not os.path.exists(INPUT_TESTS):
        print(f"❌ Error: {INPUT_TESTS} not found.")
        return
    with open(INPUT_TESTS, "r", encoding="utf-8") as f:
        test_data = json.load(f)

    page_labels, global_labels, valid_paths = build_label_index(snapshot)
    print(f"📋 Loaded {len(page_labels)} pages, {len(global_labels)} labels, {len(valid_paths)} paths (page-aware)")

    tests = test_data.get("generated_tests", [])
    print(f"📥 Validating {len(tests)} test cases...\n")

    valid_tests    = []
    rejected_tests = []

    for test in tests:
        is_valid, issues = validate_test_case(test, page_labels, global_labels, valid_paths)
        if is_valid:
            valid_tests.append(test)
            print(f"  ✅ {test.get('id', '??')}: {test.get('goal', '')[:60]}")
        else:
            rejected_tests.append({"test": test, "issues": issues})
            print(f"  ❌ {test.get('id', '??')}: {', '.join(issues[:3])}")

    # Deduplication
    seen_steps  = set()
    deduped     = []
    dup_count   = 0
    for test in valid_tests:
        key = "|".join(test.get("steps", []))
        if key in seen_steps:
            dup_count += 1
            print(f"  🔄 {test.get('id', '??')}: Duplicate steps — removed")
        else:
            seen_steps.add(key)
            deduped.append(test)

    valid_tests = deduped
    if dup_count:
        print(f"\n  🧹 Removed {dup_count} duplicate test(s) ({len(valid_tests)} unique remain)")

    # Re-number
    for i, test in enumerate(valid_tests):
        test["id"] = f"VT-{i + 1:02d}"

    with open(OUTPUT_VALID, "w", encoding="utf-8") as f:
        json.dump({"generated_tests": valid_tests}, f, indent=2)

    with open(OUTPUT_REJECTED, "w", encoding="utf-8") as f:
        json.dump({"rejected_tests": rejected_tests}, f, indent=2)

    print(f"\n{'=' * 60}")
    print(f"📊 Results:")
    print(f"   ✅ Valid:    {len(valid_tests)}")
    print(f"   ❌ Rejected: {len(rejected_tests)}")
    print(f"   📁 Valid  → {OUTPUT_VALID}")
    print(f"   📁 Reject → {OUTPUT_REJECTED}")

    if len(valid_tests) >= 50:
        print(f"   🎯 TARGET MET: {len(valid_tests)} ≥ 50 validated test cases!")
    else:
        print(f"   ⚠️  TARGET NOT MET: {len(valid_tests)} < 50. Consider re-running generator.")

    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()