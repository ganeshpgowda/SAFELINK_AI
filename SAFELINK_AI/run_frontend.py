"""SafeLink AI - Frontend Runner Script.

Launches the Streamlit Web Application on http://localhost:8501.
"""

import sys
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
FRONTEND_APP = BASE_DIR / "frontend" / "app.py"
PYTHON_EXE = BASE_DIR / ".venv" / "Scripts" / "python.exe"


def main():
    print("=" * 60)
    print("  🛡️  SafeLink AI - Launching Streamlit Frontend")
    print(f"  Target: {FRONTEND_APP}")
    print("=" * 60)
    
    cmd = [
        str(PYTHON_EXE if PYTHON_EXE.exists() else sys.executable),
        "-m", "streamlit", "run",
        str(FRONTEND_APP),
        "--server.headless=true"
    ]
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\nSafeLink AI Frontend stopped.")


if __name__ == "__main__":
    main()

