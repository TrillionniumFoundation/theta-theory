#!/usr/bin/env python3
"""Run the checked-in Round 41 materializer after repairing one frozen-source anchor.

The reviewed Round 39 source wraps the words ``The true`` across a physical
line.  The bootstrap materializer was intentionally stored before source
materialization; this wrapper applies that single literal repair in memory and
executes the otherwise immutable generator.
"""
from pathlib import Path

path = Path(__file__).with_name("materialize_round41.py")
code = path.read_text(encoding="utf-8")
old = 'r"""The true transient cross term is at most\\n'
new = 'r"""The\\ntrue transient cross term is at most\\n'
if code.count(old) != 1:
    raise SystemExit(f"expected exactly one frozen-source anchor, found {code.count(old)}")
code = code.replace(old, new, 1)
exec(compile(code, str(path), "exec"), {"__name__": "__main__", "__file__": str(path)})
