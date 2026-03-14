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
INPUT_TESTS = "data/generated_test_cases.json"
OUTPUT_VALID = "data/validated_test_cases.json"
OUTPUT_REJECTED = "data/rejected_test_cases.json"


def build_label_index(snapshot):
    """
    Builds a PER-PAGE index of valid labels and paths.
    Returns: (page_labels_dict, global_labels, global_paths)
    page_labels_dict maps page_path -> set of valid labels on that page.
    """
    page_labels = {}  # path -> set of labels
    global_labels = set()
    global_paths = set()

    for page in snapshot.get("pages", []):
        ctx = page.get("page_context", {})

        # Collect page path
        path = ""
        for key in ("page_path", "url"):
            val = ctx.get(key, "")
            if val:
                path = val.lower().strip()
                global_paths.add(path)

        page_local = set()

        # Collect title
        title = ctx.get("title", "")
        if title:
            page_local.add(title.lower().strip())

        # Collect ALL element labels
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


def extract_references_from_step(step_text):
    """
    Extracts quoted strings from a step (labels, paths, values).
    These are the AI's "claims" about what exists in the UI.
    
    Example: "Enter '50' into 'cagenow'" → ['50', 'cagenow']
    """
    # Match single-quoted or double-quoted strings
    return re.findall(r"['\"]([^'\"]+)['\"]", step_text)


def is_numeric_or_test_value(value):
    """
    Returns True if the value looks like test data (numbers, special chars, etc.)
    rather than an element label. We don't validate test data.
    """
    # Pure numbers, decimals, negative numbers
    if re.match(r'^-?\d+\.?\d*$', value):
        return True
    # Common test data patterns
    if value in ("", " ", "abc", "test", "null", "undefined", "NaN", "true", "false"):
        return True
    # Very short strings (likely single chars or operators)
    if len(value) <= 2:
        return True
    # Email patterns
    if "@" in value:
        return True
    # Strings that look like intentional bad data
    if any(c in value for c in ['<', '>', '!', ';', '--', '"']):
        return True

    return False


def validate_test_case(test, page_labels, global_labels, valid_paths):
    """
    Validates a single test case with PAGE-AWARE label checking.
    Returns (is_valid, list_of_issues).
    """
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

    # Extract the target page from the first Navigate step
    target_page = None
    for step_text in test.get("steps", []):
        nav_match = re.match(r"Navigate to ['\"](.+?)['\"]", step_text)
        if nav_match:
            target_page = nav_match.group(1).lower().strip()
            break

    # Get page-specific labels (or fall back to global if page not found)
    if target_page and target_page in page_labels:
        valid_labels = page_labels[target_page]
    else:
        valid_labels = global_labels  # fallback for unknown pages

    # Content checks: validate every quoted reference in steps
    for i, step_text in enumerate(test.get("steps", [])):
        refs = extract_references_from_step(step_text)

        for ref in refs:
            ref_lower = ref.lower().strip()

            # Skip if it looks like test data, not a label
            if is_numeric_or_test_value(ref):
                continue

            # Check if it's a valid path
            if ref_lower.startswith("/") or "://" in ref_lower:
                if ref_lower not in valid_paths:
                    issues.append(f"Step {i+1}: Unknown path '{ref}'")
                continue

            # Check if label exists on the target page
            if ref_lower not in valid_labels:
                # Check if it exists on another page (cross-page hallucination)
                if ref_lower in global_labels:
                    issues.append(f"Step {i+1}: Cross-page label '{ref}' (exists on another page, not on '{target_page}')")
                else:
                    # Fuzzy fallback
                    fuzzy_match = any(ref_lower in vl or vl in ref_lower for vl in valid_labels)
                    if not fuzzy_match:
                        issues.append(f"Step {i+1}: Hallucinated label '{ref}'")

    return len(issues) == 0, issues


def main():
    print("=" * 60)
    print("🔍 Post-Generation Validator v1.0 (Anti-Hallucination Layer 3)")
    print("=" * 60)

    # Load snapshot
    if not os.path.exists(INPUT_SNAPSHOT):
        print(f"❌ Error: {INPUT_SNAPSHOT} not found.")
        return
    with open(INPUT_SNAPSHOT, "r", encoding="utf-8") as f:
        snapshot = json.load(f)

    # Load generated tests
    if not os.path.exists(INPUT_TESTS):
        print(f"❌ Error: {INPUT_TESTS} not found.")
        return
    with open(INPUT_TESTS, "r", encoding="utf-8") as f:
        test_data = json.load(f)

    # Build validation index (page-aware)
    page_labels, global_labels, valid_paths = build_label_index(snapshot)
    print(f"📋 Loaded {len(page_labels)} pages, {len(global_labels)} labels, {len(valid_paths)} paths (page-aware)")

    tests = test_data.get("generated_tests", [])
    print(f"📥 Validating {len(tests)} test cases...\n")

    valid_tests = []
    rejected_tests = []

    for test in tests:
        is_valid, issues = validate_test_case(test, page_labels, global_labels, valid_paths)

        if is_valid:
            valid_tests.append(test)
            print(f"  ✅ {test.get('id', '??')}: {test.get('goal', '')[:60]}")
        else:
            rejected_tests.append({"test": test, "issues": issues})
            print(f"  ❌ {test.get('id', '??')}: {', '.join(issues[:3])}")
    # ── Deduplication: remove tests with identical step sequences ──
    seen_steps = set()
    deduped_tests = []
    dup_count = 0
    for test in valid_tests:
        step_key = "|".join(test.get("steps", []))
        if step_key in seen_steps:
            dup_count += 1
            print(f"  🔄 {test.get('id', '??')}: Duplicate steps — removed")
        else:
            seen_steps.add(step_key)
            deduped_tests.append(test)

    valid_tests = deduped_tests
    if dup_count:
        print(f"\n  🧹 Removed {dup_count} duplicate test(s) ({len(valid_tests)} unique remain)")

    # Re-number valid tests sequentially
    for i, test in enumerate(valid_tests):
        test["id"] = f"VT-{i + 1:02d}"

    # Save validated tests
    with open(OUTPUT_VALID, "w", encoding="utf-8") as f:
        json.dump({"generated_tests": valid_tests}, f, indent=2)

    # Save rejected tests for debugging
    with open(OUTPUT_REJECTED, "w", encoding="utf-8") as f:
        json.dump({"rejected_tests": rejected_tests}, f, indent=2)

    # Summary
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
