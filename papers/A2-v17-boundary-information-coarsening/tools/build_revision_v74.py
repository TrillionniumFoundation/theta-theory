#!/usr/bin/env python3
"""Build all complete v74 entries from frozen native Git source objects."""
import build_revision_v56 as engine
engine.DIAGNOSTICS=(*engine.DIAGNOSTICS,'check_inherited_v73_on_baseline.py','check_revision_v74.py')
if __name__=='__main__':
    engine.main()
