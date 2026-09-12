"""Runs the FastAPI server with uvicorn, from this file's directory."""

import os
import subprocess
import sys

import config

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

print("Starting FastAPI server...")
print(f"Serving on http://{config.HOST}:{config.PORT}")

try:
    subprocess.run(
        ["uvicorn", "main:app", "--reload", "--host", config.HOST, "--port", str(config.PORT)],
        check=True,
    )
except Exception as e:
    print(f"Error running server: {e}")
    sys.exit(1)
