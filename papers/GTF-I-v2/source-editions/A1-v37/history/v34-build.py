#!/usr/bin/env python3
"""Build the integrated v32 volumes; preserve the historical v30 builder separately."""
from pathlib import Path
import runpy
import sys

root = Path(__file__).resolve().parent
script = root / 'revision-v32' / 'build_native.py'
sys.path.insert(0, str(script.parent))
sys.argv = [str(script), str(root), *sys.argv[1:]]
runpy.run_path(str(script), run_name='__main__')
