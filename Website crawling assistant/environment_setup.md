# Environment Setup Guide

If you are seeing red lines in your Python files, it is likely because your virtual environment (`venv`) is corrupt or not selected in your IDE. Follow these steps to fix it.

## 1. Recreate your Virtual Environment

The current `venv` folder appears to be broken. You should recreate it:

1.  Open your terminal in the project root (`Website crawling assistant`).
2.  Delete the broken `venv` folder (if you can't delete it, just skip to step 3).
3.  Run the following commands:
    ```powershell
    # Remove existing venv (if needed)
    Remove-Item -Recurse -Force venv
    
    # Create a fresh virtual environment
    python -m venv venv
    
    # Activate the virtual environment
    .\venv\Scripts\activate
    
    # Install dependencies
    pip install -r requirements.txt
    ```

## 2. Select the Correct Interpreter in VS Code

Once the environment is recreated, you must tell VS Code to use it:

1.  Open any `.py` file (like `src/the_crawler.py`).
2.  Press `Ctrl + Shift + P` to open the Command Palette.
3.  Type `Python: Select Interpreter` and press Enter.
4.  Select the interpreter that starts with `./venv` or matches your project path.

## 3. Frontend Dependencies

If you see red lines in your `frontend` files:

1.  Open your terminal and navigate to the `frontend` folder:
    ```powershell
    cd frontend
    ```
2.  Install the dependencies:
    ```powershell
    npm install
    ```

After these steps, the "red lines" should disappear!
