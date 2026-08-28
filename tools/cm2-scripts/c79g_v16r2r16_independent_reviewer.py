#!/usr/bin/env python3
"""r16 reviewer entrypoint.

The underlying checker is read-only and parameterized by explicit successor
and predecessor suffixes.  This entrypoint fixes those descriptors so CI and
the second seed cannot accidentally inspect another namespace.
"""
from __future__ import annotations

import os
import runpy
from pathlib import Path

root = Path(__file__).resolve().parents[1]
os.environ["CM2_SUCCESSOR_SUFFIX"] = "v16r2r16"
os.environ["CM2_PREDECESSOR_SUFFIX"] = "v16r2r15"
runpy.run_path(str(root / "scripts/c79g_v16r2r15_independent_reviewer.py"),
               run_name="__main__")
