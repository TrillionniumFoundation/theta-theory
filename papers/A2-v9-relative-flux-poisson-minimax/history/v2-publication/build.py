#!/usr/bin/env python3
"""Build the complete current article and its unchanged companion."""
from pathlib import Path
import subprocess
import sys
if __name__ == "__main__":
    root = Path(__file__).resolve().parent
    raise SystemExit(subprocess.call([sys.executable, str(root/"v2/build_native.py")]))
