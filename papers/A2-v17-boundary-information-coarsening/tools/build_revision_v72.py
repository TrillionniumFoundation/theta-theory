#!/usr/bin/env python3
"""Build all three complete v72 entries with the unchanged frozen-source native engine."""
import build_revision_v56 as engine
engine.DIAGNOSTICS = (*engine.DIAGNOSTICS, 'check_revision_v72.py')
if __name__ == '__main__':
    engine.main()
