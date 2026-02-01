
import py_compile
import sys

try:
    py_compile.compile(r'c:\Users\fathi\.gemini\antigravity\scratch\selenium_ollama_scraper\UI AUTOMATION\fotoflexer_test.py', doraise=True)
    print("SUCCESS")
except py_compile.PyCompileError as e:
    print("CAUGHT PyCompileError")
    # The actual exception is in e.exc_value
    err = e.exc_value
    print(f"Error Type: {type(err)}")
    if hasattr(err, 'lineno'):
        print(f"Line: {err.lineno}")
    if hasattr(err, 'offset'):
        print(f"Offset: {err.offset}")
    if hasattr(err, 'text'):
        print(f"Text: {repr(err.text)}")
    print(f"Message: {err}")
except Exception as e:
    print(f"GENERIC EXCEPTION: {type(e)} {e}")
