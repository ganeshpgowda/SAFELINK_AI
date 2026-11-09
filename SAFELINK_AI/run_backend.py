"""SafeLink AI - Backend Runner Script.

Starts the FastAPI REST API service on http://127.0.0.1:8000.
"""

import sys
from pathlib import Path
import uvicorn

# Ensure project root is in path
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))


def main():
    print("=" * 60)
    print("  🛡️  SafeLink AI - Starting FastAPI Backend Server")
    print("  API Docs: http://127.0.0.1:8000/docs")
    print("  Health:   http://127.0.0.1:8000/health")
    print("=" * 60)
    uvicorn.run(
        "backend.app:app",
        host="127.0.0.1",
        port=8000,
        reload=False,
        log_level="info"
    )


if __name__ == "__main__":
    main()

