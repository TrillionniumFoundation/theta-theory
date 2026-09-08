#!/usr/bin/env python3
"""Prepare the native v26 source without restoring an earlier entry point."""
from pathlib import Path
import subprocess
import sys

if __name__ == '__main__':
    subprocess.run([sys.executable, str(Path(__file__).with_name('build.py')), '--prepare-only'], check=True)
