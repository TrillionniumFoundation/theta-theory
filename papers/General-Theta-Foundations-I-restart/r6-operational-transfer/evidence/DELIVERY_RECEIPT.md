# Restart r6 delivery receipt

## Immutable inputs and outputs

The native mathematics was introduced in `e53a2aafd22bb2e9b8a95172c327da7a618dda00`, whose first parent is the canonical restart `18000b21e4bfd89180ccb069e46ac0f21621f34d` and whose second parent preserves the reviewed r5 provenance. The build source is `56df65f55a507d996ef7dc385e4d6d057822ad21`; its only additional change is the clean-runner scalable-font dependency. The native source tree in both commits is `0b3839c841b02a173745d6d4fb3d997712ea9fe0`.

GitHub Actions run `37607345407`, job `112745952771`, completed successfully and published artifact commit `f9785976f1ed8a4ce1bd69c20a6751ff2defeb62` by a non-force push. That commit adds exactly the r6 PDF, TeX log and full hosted build receipt. The 22-page remote PDF has SHA-256 `7831e587f2d604e134b80bf5ef4f6faaffc7fd860d165e5b12625f6b95a2f3f8` and Git blob `7adad97131374b2743ea482263f99365a972f9be`.

The evidence-only commit containing this receipt does not modify the manuscript or built artifacts. Its exact SHA is obtained from Git history and the publication ref readback. This avoids a circular self-hash. The hosted run is bound to the build source above, not falsely described as a CI run on the later evidence commit.

## Reproduction and inspection

Both the local TeX Live 2025/dev environment and the hosted TeX Live 2023 environment passed source inventory, input-recorder, label/citation and normal/optimized Python checks. Each performed two isolated builds with three TeX passes each. Each environment produced byte-identical repeat PDFs. Each regression mode executed 27,027 finite checks, including eight named failure-mechanism controls. The article has 67 labels, 75 reference uses and 17 bibliography entries. No undefined references or overfull boxes were reported.

The PDFs from the two TeX versions differ in bytes; no cross-version byte reproducibility is claimed. Their 22 pagewise extracted texts and 72-dpi rendered page images match exactly. All hosted pages were rendered and inspected, with full-size checks of selected dense theorem pages. The downloaded artifact archive digest also matches the GitHub artifact metadata.

The first hosted run, `37607057464`, failed because the minimal runner lacked scalable T1 fonts for microtype expansion. The next source commit installed `cm-super`; no mathematical text, font files in the repository, or audit thresholds were changed to bypass the failure. A clean Debian/Ubuntu reproduction must include `cm-super` alongside the TeX packages specified by the workflow. No font files are distributed in this delivery.

## Preservation and coverage

The canonical-to-artifact comparison reports additions only, confined to the new workflow, native r6 directory, pinned report copy and the exact r4/r5 sibling trees. The controlling files are unchanged. Canonical and the input r5 review refs were re-read and remain at their pinned heads. No old review, realization or archive ref was updated.

After freezing the native source, the r4 `PIPELINE_DERIVATION.md` at `7c5012b308d3cdd5514913db7d16f6d25545d82b` was also read directly. Its weighted-allocation, terminal-bridge and reset-specific branches remain complementary; this additional pipeline reading is not an independent re-audit of all their proofs. The native `HISTORY_COVERAGE.md` and `SCOPE_AUDIT.md` retain the larger coverage limitations.

The publication targets are the new research, revision and referee-ready r6 operational-transfer refs. Referee-ready means a complete revision package for another external review, not an assertion of top-four acceptance, formal proof verification, or closure of every G1/G3 resource objective. The written general theorem, realizations and remaining mathematical obligations are distinguished in the proof and scope ledgers.
