#!/usr/bin/env python3
"""Build the three complete v71 manuscripts using the preserved native engine."""
import build_revision_v56 as engine
engine.DIAGNOSTICS = (*engine.DIAGNOSTICS, 'check_revision_v71.py')
if __name__ == '__main__':
    engine.main()
