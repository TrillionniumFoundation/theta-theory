#!/usr/bin/env python3
"""Build the complete current A1 main article and companion."""
from pathlib import Path
import subprocess
import sys
if __name__ == "__main__":
    root = Path(__file__).resolve().parent
    raise SystemExit(subprocess.call([sys.executable, str(root / "v35/build_native.py"),
        "--source-root", str(root), *sys.argv[1:]]))
