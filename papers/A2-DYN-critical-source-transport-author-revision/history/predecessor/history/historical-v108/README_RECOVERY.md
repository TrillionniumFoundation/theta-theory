# Historical native rebuild

This directory preserves the complete actual v108 native build closure from baseline commit fb99e4d67ef74912f6c69b05c9abff3207572e7a, article tree e66a1dec484f419d88c05f12a7e2ec5310430448. The 390 immutable build files are 345 TeX and 45 Python files, including all canonical core modules 1–259. Their original bytes are unchanged.

The scoped rebuild_history.py was reconstructed after workspace maintenance and verifies the fixed original source table before running the unchanged tools/assemble_v105.py. The supplement must be compiled before main because the original main imports its external labels. Each is compiled three times, followed by two PDF inspections. The actual accepted post-maintenance execution produced a 26-page main and an 883-page supplement.

Run from this directory with the required Python dependencies available:

    PYTHONDONTWRITEBYTECODE=1 python3 rebuild_history.py

The local executed environment supplied SymPy 1.14.0 and mpmath 1.3.0 through PYTHONPATH. This note does not promise that a different runtime has those dependencies installed.

Actual successful receipt (relative to the current article root):
evidence/current-execution/historical-recovery/20261018T164336583551Z/REBUILD_RECEIPT.json

The preceding missing-dependency failure and incorrect document-order attempt remain in adjacent timestamped directories. The latter's zero return codes did not justify a clean-reference claim; its separate quality assessment records the problem. The corrected successful run has no unresolved/xr/overfull/missing-glyph diagnostics. The original main retains the amsmath foreign-over advisory.

This is a historical source-preservation build, not a newly proved local limit theorem and not the current 147-page author manuscript. No obsolete missing-archive qualification gate is invoked.
