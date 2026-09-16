# A2, revision 69

**Boundary laws and smooth contact rigidity of periodic dispersing billiards**  
Qian Qi — September 16, 2026.

This revision responds to the v68 report frozen at `33bd2164d68cae0b412407c8176440fe8d7eaa9b`. The historical directory name does not identify the current revision.

The principal article is `rigidity.tex`; `main.tex` is the complete technical manuscript; `two_collision.tex` is the retained companion. All inherited proof inputs remain active. The sole added mathematical input, `article/10e_sampled_smooth_recovery_v69.tex`, turns the smooth inverse's differentiated-density premise into finite-sample complete-profile recovery and an all-preparations-charged fixed-period estimate, with bounded endpoint recording error. The v68 smooth uniqueness and flat-family proofs and the corrected curvature stopping recursion are unchanged.

`RESPONSE_TO_REFEREE_V69.md` answers every report disposition and separates mathematical scope from editorial significance. `HISTORICAL_DERIVATION_AUDIT_V69.md` records the sources actually read; `journal/DEPENDENCY_LEDGER_V69.md` locates assumptions and proofs. `LITERATURE_CHECK_V69.md` records the targeted primary-source comparison, not an exhaustive priority search. Originals of every changed inherited file are in `history/v68-review-baseline/`.

Build from a clean committed checkout:

```sh
python3 -B tools/build_revision_v69.py --output-dir /tmp/a2-v69-native
```

The build order is companion, complete manuscript, principal article, with regenerated external references. The native builder retains PDFs, logs, source hashes, input manifests and its complete source ZIP. It now writes each ZIP permission header from the recorded Git mode, including executable scripts; it never infers source permissions from a read-only build snapshot. Python's `ZipFile.extractall` does not restore these bits: use `tools/verify_source_zip_v69.py ARCHIVE --extract NEW_DIRECTORY` for checked mode-faithful extraction.

The mathematical and archival checkers use explicit failures and run under ordinary and optimized Python. Their finite controls and successful builds are not proof certificates or journal decisions. No source, previous report, A1 manuscript or historical delivery is removed.
