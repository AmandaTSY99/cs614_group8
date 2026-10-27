#!/usr/bin/env python3
"""
System C FastAPI Microservice Launcher.
Ensures repo root is on sys.path so you can run from anywhere.
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import uvicorn

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("STARTING SYSTEM C ENTERPRISE FASTAPI GATEWAY")
    print("=" * 70)
    print("Swagger Interactive Docs: http://localhost:8000/docs")
    print("Health Check:             http://localhost:8000/")
    print("Press CTRL+C to stop.\n")
    uvicorn.run("src.system_c.api:app", host="0.0.0.0", port=8000, reload=True)
