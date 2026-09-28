#!/usr/bin/env python3
"""Build all complete v70 entries from frozen Git sources."""
import build_revision_v56 as engine
engine.DIAGNOSTICS = (*engine.DIAGNOSTICS, 'check_revision_v70.py')
if __name__ == '__main__':
    engine.main()
