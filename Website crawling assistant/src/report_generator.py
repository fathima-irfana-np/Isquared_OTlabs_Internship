"""
PDF Test Report Generator
Produces a professional QA test report from the pipeline outputs.
Includes execution results from Gauge HTML report.
"""

import json
import os
import re
from datetime import datetime
from fpdf import FPDF
from urllib.parse import urlparse


# ── Configuration ──────────────────────────────────────────────
SNAPSHOT_FILE  = "data/ai_exploration_snapshot.json"
VALIDATED_FILE = "data/validated_test_cases.json"
REJECTED_FILE  = "data/rejected_test_cases.json"
GAUGE_HTML     = "reports/html-report/specs/ai_exploration.html"
OUTPUT_DIR     = "reports"
OUTPUT_PDF     = os.path.join(OUTPUT_DIR, "test_report.pdf")
TOOL_VERSION   = "2.0"

# ── Color Palette ──────────────────────────────────────────────
COLOR_PRIMARY      = (32, 33, 36)
COLOR_HEADER_BG    = (66, 133, 244)
COLOR_HEADER_FG    = (255, 255, 255)
COLOR_TABLE_HEADER = (60, 64, 67)
COLOR_TABLE_ALT    = (241, 243, 244)
COLOR_ACCENT       = (52, 168, 83)
COLOR_MUTED        = (95, 99, 104)
COLOR_BORDER       = (218, 220, 224)
COLOR_PASS         = (52, 168, 83)    # Green
COLOR_FAIL         = (234, 67, 53)    # Red
COLOR_FAIL_BG      = (252, 232, 230)  # Light red background


# ── Parse Gauge HTML for pass/fail results ─────────────────────

def parse_gauge_results(html_path):
    """
    Parse the Gauge HTML report to extract pass/fail per scenario.
    Returns dict: { 'VT-01': 'passed', 'VT-02': 'failed', ... }
    """
    results = {}
    if not os.path.exists(html_path):
        return results
    try:
        with open(html_path, encoding="utf-8") as f:
            content = f.read()
        blocks = re.findall(
            r'<div class="scenario-container (passed|failed)".*?<h3 class="head borderBottom">(.*?)</h3>',
            content, re.DOTALL
        )
        for status, name in blocks:
            # Extract VT-XX id from name like "VT-01: Break the login..."
            m = re.match(r'(VT-\d+)', name.strip())
            if m:
                results[m.group(1)] = status
    except Exception as e:
        print(f"Warning: Could not parse Gauge HTML: {e}")
    return results


# ── Test Classification ────────────────────────────────────────

CATEGORY_RULES = [
    ("Boundary Tests", [
        r"boundar", r"edge.?case", r"min\b", r"max\b", r"limit",
        r"extreme", r"overflow", r"\b0\b.*into", r"99999", r"large",
        r"0\.01", r"0\.1\b", r"\b1\b.*into.*term", r"360"
    ]),
    ("Negative Input Tests", [
        r"negative", r"invalid", r"abc.*into", r"\-\d+.*into",
        r"non.?numeric", r"special.?char", r"script", r"inject"
    ]),
    ("State Persistence Tests", [
        r"state", r"persist", r"retain", r"preserve", r"after.*clear",
        r"clear.*then", r"recalcul", r"update.*value"
    ]),
    ("Navigation & Cross-Page Tests", [
        r"navigate.*then.*navigate", r"cross.?page", r"switch.?page",
        r"multi.?page", r"between.*page"
    ]),
    ("Validation Enforcement Tests", [
        r"validat", r"error.*message", r"required", r"submit.*empty",
        r"without.*fill", r"enforce", r"reject"
    ]),
    ("Authentication Tests", [
        r"sign.?in", r"login", r"password", r"email.*password",
        r"auth", r"credential", r"account"
    ]),
    ("Zero/Empty Input Tests", [
        r"\b0\b.*into", r"empty", r"blank", r"zero.*input",
        r"clear.*all", r"'0'.*into"
    ]),
]


def classify_test(test):
    text = test.get("goal", "").lower()
    steps_text = " ".join(test.get("steps", [])).lower()
    combined = text + " " + steps_text
    for category, patterns in CATEGORY_RULES:
        for pattern in patterns:
            if re.search(pattern, combined):
                return category
    return "General Exploratory Tests"


def get_test_page(test):
    for step in test.get("steps", []):
        m = re.search(r"Navigate to ['\"](.+?)['\"]", step)
        if m:
            return m.group(1)
    return "N/A"


def get_test_target(test):
    for step in test.get("steps", []):
        m = re.search(r"into ['\"](.+?)['\"]", step)
        if m:
            return m.group(1)
    return "N/A"


def safe(text):
    """Encode text safely for fpdf latin-1 - replace ALL non-latin chars."""
    text = str(text)
    text = text.replace(u'—', '-').replace(u'–', '-')
    text = text.replace(u'‘', "'").replace(u'’', "'")
    text = text.replace(u'“', '"').replace(u'”', '"')
    text = text.replace(u'…', '...').replace(u'▾', 'v')
    text = text.replace(u'·', '*')
    return text.encode('latin-1', 'replace').decode('latin-1')


# ── PDF Builder ────────────────────────────────────────────────

class TestReportPDF(FPDF):
    def __init__(self, target_url):
        super().__init__()
        self.target_url = target_url
        self.set_auto_page_break(auto=True, margin=25)

    def header(self):
        if self.page_no() > 1:
            self.set_font("Helvetica", "I", 8)
            self.set_text_color(*COLOR_MUTED)
            self.cell(0, 8, "AI Exploratory Test Report | " + self.target_url, align="L")
            self.cell(0, 8, "Page " + str(self.page_no()), align="R", new_x="LMARGIN", new_y="NEXT")
            self.set_draw_color(*COLOR_BORDER)
            self.line(10, 16, 200, 16)
            self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(*COLOR_MUTED)
        self.cell(0, 10, "Generated by AI Exploratory Test Engine v" + TOOL_VERSION, align="C")

    def section_title(self, title, number=None):
        self.ln(6)
        self.set_fill_color(*COLOR_HEADER_BG)
        self.set_text_color(*COLOR_HEADER_FG)
        self.set_font("Helvetica", "B", 12)
        label = (str(number) + ". " + title) if number else title
        self.cell(0, 10, "  " + label, fill=True, new_x="LMARGIN", new_y="NEXT")
        self.ln(4)
        self.set_text_color(*COLOR_PRIMARY)

    def sub_title(self, title):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(*COLOR_PRIMARY)
        self.cell(0, 7, title, new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def body_text(self, text):
        self.set_font("Helvetica", "", 9)
        self.set_text_color(*COLOR_PRIMARY)
        self.multi_cell(0, 5, safe(text))
        self.ln(2)

    def add_table(self, headers, rows, col_widths=None):
        if col_widths is None:
            col_widths = [190 / len(headers)] * len(headers)
        self.set_font("Helvetica", "B", 9)
        self.set_fill_color(*COLOR_TABLE_HEADER)
        self.set_text_color(*COLOR_HEADER_FG)
        for i, h in enumerate(headers):
            self.cell(col_widths[i], 8, "  " + h, border=1, fill=True)
        self.ln()
        self.set_font("Helvetica", "", 9)
        self.set_text_color(*COLOR_PRIMARY)
        for row_idx, row in enumerate(rows):
            fill = row_idx % 2 == 1
            if fill:
                self.set_fill_color(*COLOR_TABLE_ALT)
            for i, cell in enumerate(row):
                self.cell(col_widths[i], 7, "  " + safe(str(cell)), border=1, fill=fill)
            self.ln()
        self.ln(4)


# ── Report Builder ─────────────────────────────────────────────

def build_report(snapshot, validated, rejected, gauge_results):

    pages = snapshot.get("pages", [])
    target_url = "Unknown"
    if pages:
        first_url = pages[0].get("page_context", {}).get("url", "")
        if first_url:
            parsed = urlparse(first_url)
            target_url = parsed.scheme + "://" + parsed.netloc

    tests          = validated.get("generated_tests", [])
    rejected_tests = rejected.get("rejected_tests", [])

    # Count pass/fail from gauge results
    passed_ids = [k for k, v in gauge_results.items() if v == "passed"]
    failed_ids = [k for k, v in gauge_results.items() if v == "failed"]
    total_executed = len(gauge_results)

    pdf = TestReportPDF(target_url)
    pdf.add_page()

    # ── Section 1: Report Header ──────────────────────────────
    pdf.ln(10)
    pdf.set_font("Helvetica", "B", 22)
    pdf.set_text_color(*COLOR_HEADER_BG)
    pdf.cell(0, 12, "AI Exploratory Test Report", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)
    pdf.set_draw_color(*COLOR_HEADER_BG)
    pdf.set_line_width(0.8)
    pdf.line(60, pdf.get_y(), 150, pdf.get_y())
    pdf.ln(8)

    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(*COLOR_PRIMARY)
    header_data = [
        ("Target Application", target_url),
        ("Report Date", datetime.now().strftime("%B %d, %Y at %H:%M")),
        ("Tool Version", "AI Exploratory Test Engine v" + TOOL_VERSION),
        ("Pages Analyzed", str(len(pages))),
        ("Total Test Cases Generated", str(len(tests) + len(rejected_tests))),
        ("Valid Test Cases", str(len(tests))),
        ("Rejected (Hallucinated)", str(len(rejected_tests))),
    ]
    if total_executed > 0:
        header_data += [
            ("Tests Executed", str(total_executed)),
            ("Passed", str(len(passed_ids))),
            ("Failed (Bugs Found)", str(len(failed_ids))),
        ]

    for label, value in header_data:
        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(70, 7, label + ":", align="R")
        # Color pass/fail values
        if label == "Passed":
            pdf.set_text_color(*COLOR_PASS)
        elif label == "Failed (Bugs Found)":
            pdf.set_text_color(*COLOR_FAIL)
        else:
            pdf.set_text_color(*COLOR_PRIMARY)
        pdf.set_font("Helvetica", "", 10)
        pdf.cell(0, 7, "  " + value, new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(*COLOR_PRIMARY)

    # ── Section 2: Execution Summary ──────────────────────────
    if total_executed > 0:
        pdf.section_title("Execution Results Summary", 2)

        # Big pass/fail boxes
        pdf.ln(2)
        box_y = pdf.get_y()

        # PASSED box
        pdf.set_fill_color(*COLOR_PASS)
        pdf.set_text_color(255, 255, 255)
        pdf.rect(10, box_y, 88, 22, "F")
        pdf.set_font("Helvetica", "B", 18)
        pdf.set_xy(10, box_y + 3)
        pdf.cell(88, 8, str(len(passed_ids)) + " PASSED", align="C", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "", 9)
        pdf.set_xy(10, box_y + 13)
        pdf.cell(88, 6, "Tests behaved correctly", align="C")

        # FAILED box
        pdf.set_fill_color(*COLOR_FAIL)
        pdf.set_text_color(255, 255, 255)
        pdf.rect(102, box_y, 88, 22, "F")
        pdf.set_font("Helvetica", "B", 18)
        pdf.set_xy(102, box_y + 3)
        pdf.cell(88, 8, str(len(failed_ids)) + " FAILED", align="C", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "", 9)
        pdf.set_xy(102, box_y + 13)
        pdf.cell(88, 6, "Bugs found in application", align="C")

        pdf.set_xy(10, box_y + 28)
        pdf.set_text_color(*COLOR_PRIMARY)
        pdf.ln(4)

        # Failed tests list
        if failed_ids:
            pdf.set_font("Helvetica", "B", 10)
            pdf.set_text_color(*COLOR_FAIL)
            pdf.cell(0, 8, safe("  Bugs Found - Failed Test Cases:"), new_x="LMARGIN", new_y="NEXT")
            pdf.set_text_color(*COLOR_PRIMARY)

            failed_tests = [t for t in tests if t.get("id") in failed_ids]
            bug_rows = []
            for t in failed_tests:
                bug_rows.append([
                    t.get("id", ""),
                    safe(t.get("goal", "")[:55]),
                    safe(t.get("expected", "")[:45]),
                ])
            pdf.add_table(
                ["Test ID", "Goal", "Expected (Not Met - Bug)"],
                bug_rows,
                [20, 95, 75]
            )

    # ── Section 3: Application Coverage Summary ───────────────
    pdf.section_title("Application Coverage Summary", 3)

    total_inputs   = 0
    total_buttons  = 0
    total_links    = 0
    total_dropdowns= 0
    pages_with_forms = 0
    for page in pages:
        inv     = page.get("ui_inventory", {})
        inputs  = inv.get("inputs", [])
        buttons = inv.get("buttons", [])
        links   = inv.get("links", [])
        total_inputs   += len(inputs)
        total_buttons  += len(buttons)
        total_links    += len(links)
        for inp in inputs:
            if inp.get("type") == "select":
                total_dropdowns += 1
        if inputs or buttons:
            pages_with_forms += 1

    coverage_rows = [
        ["Pages Crawled",                  str(len(pages))],
        ["Pages with Interactive Elements", str(pages_with_forms)],
        ["Input Fields Identified",         str(total_inputs)],
        ["Buttons Identified",              str(total_buttons)],
        ["Navigation Links",                str(total_links)],
        ["Dropdowns/Selects",               str(total_dropdowns)],
        ["Test Cases Generated",            str(len(tests))],
        ["Validation Pass Rate",            str(round(len(tests) / max(len(tests) + len(rejected_tests), 1) * 100, 1)) + "%"],
    ]
    pdf.add_table(["Metric", "Value"], coverage_rows, [100, 90])

    # ── Section 4: Batch Generation Strategy ──────────────────
    pdf.section_title("Batch Generation Strategy", 4)
    pdf.body_text(
        "Tests were generated in 6 adversarial batches. Each batch focused on a distinct "
        "exploration category to guarantee structural diversity and maximize bug-finding potential."
    )
    batch_focuses = [
        ("1", "Input Torture and Field Poisoning",       "Edge-case values: long strings, special chars, min-1/max+1, empty required fields."),
        ("2", "State Transitions and Form Abandonment",  "Partial fills, navigate-away-return, recalculate after change, state persistence."),
        ("3", "Boundary Value Analysis",                 "Exact min, max, zero, +1/-1 boundaries across every numeric input field."),
        ("4", "Multi-Step Navigation Chaos",             "Fill on page A, jump to B, return to A -- does state survive?"),
        ("5", "Mode Switching and UI State Dances",      "Toggle modes mid-fill, switch tabs, check value retention after mode change."),
        ("6", "Error Recovery and Validation Resilience","Submit empty, fix one field, resubmit; clear after success; recovery flow testing."),
    ]
    pdf.add_table(["Batch", "Category", "Focus"],
                  [[b, name, desc] for b, name, desc in batch_focuses],
                  [15, 65, 110])

    # ── Section 5: Test Coverage Classification ───────────────
    pdf.section_title("Test Coverage Classification", 5)
    category_counts = {}
    test_categories = {}
    for test in tests:
        cat = classify_test(test)
        category_counts[cat] = category_counts.get(cat, 0) + 1
        test_categories[test["id"]] = cat
    sorted_cats = sorted(category_counts.items(), key=lambda x: -x[1])
    pdf.add_table(["Category", "Count"],
                  [[cat, str(cnt)] for cat, cnt in sorted_cats],
                  [130, 60])
    pdf.body_text(
        "Test cases are automatically classified based on their goals and step patterns. "
        "Categories are not mutually exclusive; each test is assigned to its primary category."
    )

    # ── Section 6: Validated Test Cases ───────────────────────
    pdf.section_title("Validated Test Cases", 6)
    pdf.body_text(
        str(len(tests)) + " test cases passed anti-hallucination validation. "
        "All referenced UI elements exist in the application snapshot."
    )
    if total_executed > 0:
        pdf.body_text("Each test is marked PASSED (green) or FAILED (red) based on execution results.")

    for test in tests:
        if pdf.get_y() > 240:
            pdf.add_page()

        test_id   = test.get("id", "??")
        goal      = test.get("goal", "No goal specified")
        steps     = test.get("steps", [])
        expected  = test.get("expected", "N/A")
        page      = get_test_page(test)
        target    = get_test_target(test)
        test_type = test_categories.get(test_id, "General")

        # Determine execution status
        exec_status = gauge_results.get(test_id, None)
        is_failed   = exec_status == "failed"
        is_passed   = exec_status == "passed"

        # Test case header - red bg if failed, green if passed, grey if not run
        if is_failed:
            pdf.set_fill_color(*COLOR_FAIL_BG)
            pdf.set_text_color(*COLOR_FAIL)
        elif is_passed:
            pdf.set_fill_color(232, 245, 233)  # light green
            pdf.set_text_color(*COLOR_PASS)
        else:
            pdf.set_fill_color(233, 236, 239)
            pdf.set_text_color(*COLOR_PRIMARY)

        pdf.set_font("Helvetica", "B", 10)
        status_badge = ""
        if is_failed:
            status_badge = " [FAILED - BUG FOUND]"
        elif is_passed:
            status_badge = " [PASSED]"

        pdf.cell(0, 8,
                 "  " + safe(test_id + "  |  " + goal[:60]) + safe(status_badge),
                 fill=True, new_x="LMARGIN", new_y="NEXT")

        # Metadata row
        pdf.set_font("Helvetica", "", 8)
        pdf.set_text_color(*COLOR_MUTED)
        pdf.cell(63, 6, "  Page: " + safe(page))
        pdf.cell(63, 6, "Target: " + safe(target))
        pdf.cell(63, 6, "Type: " + safe(test_type), new_x="LMARGIN", new_y="NEXT")

        # Steps
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(*COLOR_PRIMARY)
        for i, step_text in enumerate(steps):
            pdf.cell(8, 5, "")
            pdf.cell(0, 5, safe(str(i + 1) + ". " + step_text), new_x="LMARGIN", new_y="NEXT")

        # Expected result
        pdf.set_font("Helvetica", "I", 8)
        if is_failed:
            pdf.set_text_color(*COLOR_FAIL)
        else:
            pdf.set_text_color(*COLOR_ACCENT)
        pdf.cell(0, 5, "  Expected: " + safe(expected[:120]), new_x="LMARGIN", new_y="NEXT")

        # Bug note for failed tests
        if is_failed:
            pdf.set_font("Helvetica", "B", 8)
            pdf.set_text_color(*COLOR_FAIL)
            pdf.cell(0, 5, safe("  !! Application did not meet expected behavior - potential bug detected."),
                     new_x="LMARGIN", new_y="NEXT")

        pdf.ln(3)

    # ── Section 7: Structural Validation Confirmation ─────────
    pdf.section_title("Structural Validation Confirmation", 7)
    pdf.body_text(
        "All " + str(len(tests)) + " test cases were validated against the UI exploration snapshot. "
        "The validation engine verified that:"
    )
    checks = [
        "All referenced UI element labels exist in the application snapshot.",
        "All referenced page paths exist in the crawled page inventory.",
        "No hallucinated or invented element labels were detected.",
        "Each test case has a valid structure: ID, goal, steps (min 2), and expected result.",
    ]
    pdf.set_font("Helvetica", "", 9)
    for check in checks:
        pdf.cell(8, 6, "")
        pdf.set_text_color(*COLOR_ACCENT)
        pdf.set_font("ZapfDingbats", "", 9)
        pdf.cell(5, 6, "4")
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(*COLOR_PRIMARY)
        pdf.cell(0, 6, " " + check, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    if rejected_tests:
        pdf.body_text(str(len(rejected_tests)) + " test case(s) were rejected during validation.")
        for rt in rejected_tests:
            tid    = rt.get("test", {}).get("id", "??")
            issues = rt.get("issues", [])
            pdf.set_font("Helvetica", "", 8)
            pdf.set_text_color(220, 53, 69)
            pdf.cell(0, 5, "  " + tid + ": " + safe(", ".join(issues)[:150]),
                     new_x="LMARGIN", new_y="NEXT")
        pdf.set_text_color(*COLOR_PRIMARY)
        pdf.ln(4)

    # ── Section 8: Appendix ───────────────────────────────────
    pdf.section_title("Appendix", 8)
    pdf.sub_title("Snapshot Statistics")
    appendix_rows = [
        ["Snapshot File",            "ai_exploration_snapshot.json"],
        ["Snapshot Size",            str(os.path.getsize(SNAPSHOT_FILE) if os.path.exists(SNAPSHOT_FILE) else 0) + " bytes"],
        ["Total Pages in Snapshot",  str(len(pages))],
        ["Total Input Fields",       str(total_inputs)],
        ["Total Buttons",            str(total_buttons)],
        ["Total Navigation Links",   str(total_links)],
    ]
    pdf.add_table(["Metric", "Value"], appendix_rows, [100, 90])

    pdf.sub_title("Pipeline Configuration")
    config_rows = [
        ["AI Model",           "llama-3.3-70b-versatile (Groq)"],
        ["Generation Batches", "6"],
        ["Tests per Batch",    "~10"],
        ["Batch Delay",        "30 seconds"],
        ["Validation Engine",  "3-Layer Anti-Hallucination"],
        ["Step Generator",     "Deterministic (Template-Based)"],
    ]
    pdf.add_table(["Parameter", "Value"], config_rows, [100, 90])

    pdf.sub_title("Output Files Reference")
    files_rows = [
        ["Raw Test Cases",       "data/generated_test_cases.json"],
        ["Validated Test Cases", "data/validated_test_cases.json"],
        ["Rejected Test Cases",  "data/rejected_test_cases.json"],
        ["Gauge Specification",  "specs/ai_exploration.spec"],
        ["Step Implementations", "step_impl/step_implementation.py"],
        ["This Report",          "reports/test_report.pdf"],
    ]
    pdf.add_table(["File", "Path"], files_rows, [80, 110])

    return pdf


# ── Main ───────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("PDF Test Report Generator v" + TOOL_VERSION)
    print("=" * 60)

    if not os.path.exists(SNAPSHOT_FILE):
        print("Error: " + SNAPSHOT_FILE + " not found.")
        return
    if not os.path.exists(VALIDATED_FILE):
        print("Error: " + VALIDATED_FILE + " not found.")
        return

    with open(SNAPSHOT_FILE, "r", encoding="utf-8") as f:
        snapshot = json.load(f)
    with open(VALIDATED_FILE, "r", encoding="utf-8") as f:
        validated = json.load(f)

    rejected = {"rejected_tests": []}
    if os.path.exists(REJECTED_FILE):
        with open(REJECTED_FILE, "r", encoding="utf-8") as f:
            rejected = json.load(f)

    # Parse Gauge execution results
    gauge_results = parse_gauge_results(GAUGE_HTML)
    passed_count  = sum(1 for v in gauge_results.values() if v == "passed")
    failed_count  = sum(1 for v in gauge_results.values() if v == "failed")

    tests         = validated.get("generated_tests", [])
    rejected_tests= rejected.get("rejected_tests", [])

    print("Loaded: " + str(len(tests)) + " valid tests, " + str(len(rejected_tests)) + " rejected")
    if gauge_results:
        print("Execution results: " + str(passed_count) + " passed, " + str(failed_count) + " failed")
    else:
        print("No Gauge execution results found - run 'gauge run specs/' first")

    print("Generating PDF report...")
    pdf = build_report(snapshot, validated, rejected, gauge_results)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    pdf.output(OUTPUT_PDF)

    size_kb = os.path.getsize(OUTPUT_PDF) / 1024
    print("Report saved to: " + OUTPUT_PDF + " (" + str(round(size_kb, 1)) + " KB)")
    print("=" * 60)


if __name__ == "__main__":
    main()