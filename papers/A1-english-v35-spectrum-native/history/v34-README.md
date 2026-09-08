# A1 v34 — attainable information at exponent collisions

**Current main article:** *Attainable information and causal compression at exponent collisions*, Qian Qi, 8 September 2026.

This is the full revision directory for `revision/a1-english-v34-attainment-blackwell-2026-09-08`. It is based on reviewed manuscript commit `e7dfc3a0e1c8d7a9d3be6b7f52944c5c7c59bb0c` and responds to the v33 independent report at `7643c3532ea9f70eaa3010cd13abcb58c1c31a8f`. It is not a replacement of the repository's main branch or the old v33 directory.

## Reading entry points

`main.tex` is the complete main-article entry. It centers the collision-uniform all-budget theorem and includes all original exact-information, geometric, finite-compatibility, precision and exact-example proofs. The revised controller section is stated for general finite-cell experiments and identifies the one-step domain exactly as a Blackwell postprocessing region.

`companions.tex` remains the complete companion entry, unchanged from the reviewed tree. Its structural, exact-kernel, uncertainty, effective, graph, occupation and regenerative developments retain their separate assumptions. Read `RESPONSE_TO_REFEREE_V34.md` for the pointwise response and `PROOF_LEDGER_V34.md` for the mathematical dependency map. `PRESERVATION_V34.json` records the source-tree baseline and selected unchanged proof blobs.

The current changed modules are `v34/introduction.tex`, `v34/moment_controllers.tex`, `v34/comparison.tex` and `v34/references_main.tex`. The inherited `v33/` modules are preserved, even where the new main now selects their v34 counterparts. Stable theorem labels containing `v33` are intentional and do not designate a different active manuscript.

## Build and checks

From this directory in a complete checkout:

```sh
python build.py --manuscript-commit "$(git rev-parse HEAD)"
python v34/verify_revision.py > /tmp/a1-v34-checks.json
python -O v34/verify_revision.py > /tmp/a1-v34-checks-optimized.json
cmp /tmp/a1-v34-checks.json /tmp/a1-v34-checks-optimized.json
python v34/smoke_test.py
```

The native `build.py` wrapper is retained and invokes `revision-v32/build_native.py` on this directory, compiling both `main.tex` and `companions.tex` and stabilizing cross-volume exports. Its historical output location is `revision-v32/native-build/`. That path is a builder convention, not a claim that this is the v32 manuscript.

The smoke test compiles only changed modules and the new abstract, using explicit stubs for external references. It is not the native build. The exact finite diagnostics test consistency, not optimal-controller classification or mathematical priority. `VALIDATION_V34.json` reports what was actually executed in this preparation session. The complete native v34 two-volume build was not executed in that session. Earlier `verification-v33/` and other inherited receipts describe their respective historical versions only.

No numerical tolerance, diagnostic count or compilation receipt is offered as the proof of the main theorem. Its complete proof chain remains in the native TeX sources.
