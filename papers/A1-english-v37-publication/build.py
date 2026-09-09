#!/usr/bin/env python3
"""Build the complete v37 main article and companion from native sources."""
from pathlib import Path
import subprocess
import sys

if __name__ == "__main__":
    root = Path(__file__).resolve().parent
    raise SystemExit(subprocess.call([
        sys.executable, str(root / "v35/build_native.py"),
        "--source-root", str(root), "--edition", "v37", *sys.argv[1:]
    ]))
