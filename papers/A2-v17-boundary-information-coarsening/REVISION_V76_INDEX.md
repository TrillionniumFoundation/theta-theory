# A2 revision 76 — relative determinants and phase-weighted smooth inversion

**Date:** September 17, 2026. **Author:** Qian Qi.

This revision responds to the v75 independent report at `ab44ba96a9fceeaa69bf4dbc98e5bfdd33b0cb5c`. Its unchanged mathematical baseline is the frozen v75 source `89d5a3aa3e9f00a806d48f19f6f6831770184d76`.

## Reading entries

- `rigidity.tex`: complete principal English article, with corrected proof transitions, dimension-free off-diagonal determinant comparison, matrix-envelope inversion, phase-dependent sufficient order, and integrated conditioning.
- `main.tex`: full English technical manuscript, preserving the entire inherited analytical, geometric and statistical programme and incorporating the new results.
- `two_collision.tex`: unchanged native companion.
- `RESPONSE_TO_REFEREE_V76.md`: point-by-point disposition of P1, C1, E1–E3 and preservation of M1–M6.
- `HISTORICAL_DERIVATION_AUDIT_V76.md`: derivation sources, reading scope and dependency chain.

## Reproduction

Run `python tools/check_revision_v76.py` and `python -O tools/check_revision_v76.py`; the JSON outputs should agree. Run `python tools/build_revision_v76.py --output-dir /an/empty/directory/outside/the/manuscript`. The build requires Git, Python with SymPy, latexmk, a standard LaTeX installation including the retained preamble packages, and Poppler `pdfinfo`.

The builder freezes the clean committed manuscript subtree, runs inherited and current finite checks, builds all three entries separately with source-matched auxiliary files, and records source/PDF hashes and recorder dependencies. Repository native products are placed under `deliveries/a2-v76/<source-commit>/`; their own ledger gives the actual source SHA and verification result. No build, finite test, preservation count or editorial recommendation is a formal proof certificate.
