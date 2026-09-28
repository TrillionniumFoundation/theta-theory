# A2 v46 verification ledger

## Local mathematical-source and native checks

The full main and complete companion were compiled with `latexmk -norc -pdf`, `pdflatex -no-shell-escape -recorder`, and a companion-first build order. The successful initial local main has 244 pages and the companion seven. Its main log has five underfull vertical-box notices, no overfull box and no unresolved-reference/citation warning. One preliminary build was interrupted by the local execution timeout; its incomplete generated auxiliaries were removed before the successful clean build. That interrupted invocation is not counted as a successful build. Final source-matched checks are recorded with the retained native delivery.

The baseline was downloaded from the source and native artifacts of v45 run `34829418911`. Its 99-entry active manifest is retained, not reconstructed from an old version number. The v46 source-preservation and mathematical diagnostic scripts passed under ordinary and optimized Python with identical JSON outputs. The independent finite-chain Bellman maximum coefficient error was below 4.5e-16; the 240 Bézout phase tests had maximum error below 3.7e-15. These are finite numerical diagnostic tolerances, not proof guarantees.

Readable-resolution rendering is used to inspect the changed introduction, corrected proof and new section. Final source-matched native delivery, run identity, input hashes, raw logs and fetched Git-object verification are recorded under `deliveries/a2-v46/<actual-source-commit>/`. A source-preparation workflow head and the actual mathematical-source commit are distinguished: the latter is the exact commit passed to the native build and is the directory key for every retained product.

## Reproduction

Run `python -B tools/check_revision_v46.py` and `python -B tools/check_quantized_v46.py`, then repeat with `python -O -B`. For a frozen native build from Git, run `python -B tools/build_submission.py --output-dir <empty-directory-outside-the-manuscript-tree>`. The build exports its actual Git source, checks every active TeX input with the recorder, verifies the companion-generated auxiliary dependency and retains both PDF products and raw evidence.

Publication uses `tools/retain_native_v46.py`, which reuses the preserved actual-object verifier. The products are staged only in a new version-specific delivery subtree, committed on a new products branch, pushed, fetched, and checked as Git blobs; a separate attestation commit records the fetched object identity. No force push or default-branch update is used.

Neither the executable diagnostics, native rendering, input hashes nor publication receipts certify all mathematical theorems. No referee approval or journal acceptance is asserted.
