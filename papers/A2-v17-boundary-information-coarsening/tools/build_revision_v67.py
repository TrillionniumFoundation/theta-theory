#!/usr/bin/env python3
"""Build all three v67 entries from frozen Git source, including v67 diagnostics."""
import build_revision_v56 as engine
engine.DIAGNOSTICS = (*engine.DIAGNOSTICS, 'check_revision_v67.py')
if __name__ == '__main__':
    engine.main()
