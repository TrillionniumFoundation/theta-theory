#!/usr/bin/env python3
"""Build all complete v73 entries with source-pinned native provenance."""
import build_revision_v56 as engine
engine.DIAGNOSTICS = (*engine.DIAGNOSTICS, 'check_inherited_v72_on_baseline.py', 'check_revision_v73.py')
if __name__ == '__main__':
    engine.main()
