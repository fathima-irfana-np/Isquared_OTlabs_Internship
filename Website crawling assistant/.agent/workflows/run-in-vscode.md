---
description: How to run Gauge tests in VS Code
---
To run the Gauge tests directly in VS Code, follow these steps:

### 1. Install the Gauge Extension
Make sure you have the official **Gauge** extension installed in VS Code:
- Open extensions (Ctrl+Shift+X)
- Search for "Gauge" and install the one by `getgauge`.

### 2. Open a Specification File
Open your `.spec` file:
[ai_exploration.spec](file:///c:/Users/fathi/.gemini/antigravity/scratch/Internship/Website%20crawling%20assistant/specs/ai_exploration.spec)

### 3. Use the Inline "Run" Buttons
Once the extension is active, you will see small blue text links above each scenario and at the top of the file:
- **Run Spec**: Runs all scenarios in the file.
- **Run Scenario**: Runs only that specific scenario.
- **Debug Scenario**: Allows you to set breakpoints in your Python code and debug.

### 4. Alternative: Using the Terminal
You can always run the tests via the VS Code integrated terminal:
1. Open the terminal (Ctrl+`)
2. Run the command:
   ```powershell
   gauge run specs/ai_exploration.spec
   ```

### 5. Viewing Results and Logs
After running, you can see exactly how the **Intent-Driven Engine** worked:

- **Terminal Logs**: Look at the VS Code terminal (bottom panel). You will see messages like:
  - `Propagating Click Intent: 'Deg'`
  - `Propagating Fill Intent: 'Height' -> '180'`
  This confirms that the engine is dynamically resolving the UI at runtime.

- **HTML Report**:
  1. Find the file: [ai_exploration.html](file:///c:/Users/fathi/.gemini/antigravity/scratch/Internship/Website crawling assistant/reports/html-report/specs/ai_exploration.html)
  2. **Right-click** it in the File Explorer and select **"Open with Live Server"** (if installed) or simply **"Open to the Side"**.
  3. This report contains screenshots and the pass/fail status of every intent.

### 6. Code Navigation
- You can **Ctrl+Click** on any step in your `.spec` file to jump directly to the Python implementation in `step_impl/step_implementation.py`.
