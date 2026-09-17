#!/usr/bin/env python3
"""Build all three entries with inherited and v76 independent diagnostics."""
import build_revision_v56 as engine
engine.DIAGNOSTICS=(*engine.DIAGNOSTICS,'check_inherited_v73_on_baseline.py','check_revision_v74.py','check_revision_v75.py','check_revision_v76.py')
if __name__=='__main__': engine.main()
