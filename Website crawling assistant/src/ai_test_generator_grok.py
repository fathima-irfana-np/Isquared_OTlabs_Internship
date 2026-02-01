import json
import requests
import os

GROQ_API_KEY = #your key here,noww
GROQ_ENDPOINT = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama-3.1-8b-instant"

INPUT_FILE = "data/ai_exploration_snapshot.json"
OUTPUT_FILE = "data/generated_test_cases.json"

MAX_PROMPT_CHARS = 8000
MAX_TOKENS = 3000 # Increased to prevent truncated JSON

def repair_json_structure(json_str):
    """
    Attempts to fix common AI truncation errors like missing 
    closing brackets for arrays and objects.
    """
    json_str = json_str.strip()
    
    # Check if the list was not closed
    if json_str.count('[') > json_str.count(']'):
        json_str += "]"
    
    # Check if the main object was not closed
    if json_str.count('{') > json_str.count('}'):
        json_str += "}"
        
    return json_str

def build_prompt(snapshot):
    snapshot_text = json.dumps(snapshot, indent=2)
    snapshot_text = snapshot_text[:MAX_PROMPT_CHARS]

    return f"""
You are an expert UI-based exploratory software tester.

You are given a structured JSON snapshot of a web application's UI, including:
- interactive elements
- navigation paths
- visible controls
- state transitions

Your task is to generate DEEP UI exploratory test cases.

Focus on:
- UI mode switches (e.g. toggles, tabs, degree/radian, themes)
- State changes during interaction (changing modes mid-input)
- Interrupting user flows (navigation during input)
- Reusing UI state across actions
- Edge-case sequences, not just single actions

DO NOT generate generic tests like "verify page loads".
Each test MUST explore UI behavior across multiple steps.

IMPORTANT:
- Generate ONLY valid JSON
- Do NOT include explanations or extra text
- Use realistic UI terminology from the snapshot
- Each test must include state change or UI mutation

Output format:
{{
  "generated_tests": [
    {
        {
  "id": "ET-01",
  "goal": "Explore switching between degree and radian modes during calculation",
  "steps": [
    "Navigate to the Scientific Calculator page",
    "Ensure calculator is in degree mode",
    "Enter sin(90)",
    "Toggle calculator mode to radian without clearing input",
    "Press '='",
    "Observe displayed result or error behavior"
  ],
  "expected": "Calculator handles mode switching gracefully or displays a clear error"
}

    }
  ]
}}

Here is the application snapshot:
{snapshot_text}
"""


def call_groq(prompt):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are a senior QA engineer. Output valid JSON only."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3,
        "max_tokens": MAX_TOKENS
    }

    response = requests.post(GROQ_ENDPOINT, headers=headers, json=payload, timeout=60)
    
    if response.status_code != 200:
        print(f"Groq API Error: {response.text}")
        response.raise_for_status()
        
    return response.json()["choices"][0]["message"]["content"]

def main():
    print("🔹 Loading exploration snapshot...")
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        snapshot = json.load(f)

    print("🔹 Requesting AI test generation...")
    ai_output = call_groq(build_prompt(snapshot))

    start = ai_output.find("{")
    end = ai_output.rfind("}") + 1
    raw_json = ai_output[start:end]
    
    try:
        final_json = json.loads(raw_json)
    except json.JSONDecodeError:
        print("⚠️ Detected malformed JSON, attempting repair...")
        repaired = repair_json_structure(raw_json)
        final_json = json.loads(repaired)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(final_json, f, indent=2)

    print(f" Success: Generated test cases saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()