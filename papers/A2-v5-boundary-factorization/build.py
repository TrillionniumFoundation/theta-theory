#!/usr/bin/env python3
"""Build the complete v5 article and preserved companion, checking inputs and references."""
from pathlib import Path
import runpy
runpy.run_path(str(Path(__file__).resolve().parent / "v5" / "build_native.py"), run_name="__main__")
