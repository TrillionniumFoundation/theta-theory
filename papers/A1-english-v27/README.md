# A1 v27 — whole prediction curves and finite acquisition menus

**Principal manuscript:** `main.tex`  
**Revision branch:** `revision/a1-english-v27-uniform-policy-curves-2026-09-08`  
**Referee response:** `RESPONSE_TO_REFEREE.md`  
**Proof dependencies:** `PROOF_LEDGER.md`

This is the English revision answering the independent v26 report committed at `19fbf4fe0e7495afd537de73a63670a9cf5616e0`. The report is retained in `reviews/a1-english-v26-harsh-independent-2026-09-07/REFEREE_REPORT.md`. The reviewed submission is `a2e5d3737085241137211f1cf21393d5bcafa1ce`.

## What is in the revision

The complete principal manuscript retains all v26 analytic, attained-information, collision, causal-memory, graph, selection, separator and phase inputs. It adds three mathematical developments.

* One deterministic order is selected independently of predictive budget and codebook and dominates the entire prediction curve of a fixed resolution-blind randomized/history-dependent acquisition rule. The converse allows a full-history scheduler and finite-prefix decoder; the upper bound uses the original charged model.
* Menus of at most K such rules are characterized, to within bounded additive bits uniformly over resolutions, by menus of at most K deterministic orders. Their optimal uniform-resolution excess has a finite minimax formula and an analytic-contact-order leading law. The actual three-edge experiment is evaluated for one and two reusable configurations.
* An actual positive two-trial experiment is fully evaluated: acquired posterior law, exact finite-label scalar reduction, sharp asymptotic average-risk coefficient, and a complete same-decoder comparison of first-block and complete-word separator certificates.

The acquisition law, rather than only the text of an algorithm, is fixed in the whole-curve and menu results. Reading budget-dependent compressed states can change that law and is not silently admitted. Predictive encoders may be redesigned at every resolution. No common nested codebook, growing-graph uniform constant, or general sharp separator constant is claimed.

## Source layout and preservation

This directory is a **repository-native source overlay**, not an isolated archive of every inherited file. The full reviewed source remains unchanged at `../A1-english-v26/`, in the same branch. `main.tex` includes all its prior proof modules and the new files under `v27/`. The original companion manuscript is retained, not replaced by a summary. `references-v27.tex` preserves the reviewed bibliography and appends the classical quantization reference.

For a self-contained build directory, `build_v27.py` copies the native v26 tree and overlays this directory. It does not edit the original v26 directory. Use the default output directory below; any custom output should be outside the inherited source tree. The immutable source and review identifiers are in `NATIVE_SOURCE_RECORD.json`.

The new mathematical files are `v27/uniform_policy.tex`, `v27/policy_menus.tex` and `v27/evaluated_model.tex`; `v27/introduction.tex` states the quantifiers and the decoder-model comparison. The unchanged earlier proof ledger remains at `../A1-english-v26/PROOF_LEDGER.md` and is referenced, rather than silently discarded, by the v27 ledger.

From the repository root, source preservation can be inspected with:

```sh
git diff --exit-code 19fbf4fe0e7495afd537de73a63670a9cf5616e0 HEAD -- \
  papers/A1-english-v26 \
  reviews/a1-english-v26-harsh-independent-2026-09-07
```

## Reproduce the arithmetic checks

The diagnostic uses only the Python standard library. It includes exact rational identities, enumeration of all 24 star orders and the finite affine arrangement for menus, and a rational enclosure of the sharp integral constant. It does not verify the general theorems by testing examples.

```sh
cd papers/A1-english-v27
python3 diagnostics_v27.py --output DIAGNOSTICS_V27.json
python3 -O diagnostics_v27.py --output DIAGNOSTICS_V27_OPTIMIZED.json
cmp DIAGNOSTICS_V27.json DIAGNOSTICS_V27_OPTIMIZED.json
```

Every check uses an explicit exception rather than `assert`. A successful output records the exact certificate coefficient, the rational sharp-coefficient enclosure and the finite-menu results. Timestamps are deliberately excluded from the diagnostic JSON so normal and optimized executions can be compared byte for byte.

## Materialize and build both native volumes

With Python 3 and a TeX installation containing the packages used by the inherited preamble:

```sh
python3 build_v27.py --materialize-only
python3 build_v27.py
```

The output is under `build-v27/native/`, including the complete inherited companion source. The build alternates three passes of each volume, exporting theorem labels but not foreign bibliography numbers between them. A staging-only `xr-hyper` compatibility conversion removes the newer `nocite` option after the external auxiliary files have been restricted to labels. It does not alter mathematical proof text. Its occurrences are recorded.

`build-v27/BUILD_RECORD_V27.json` reports the actual engine, pass return codes, source hashes, unresolved-reference checks and generated PDF hashes. Failure or an unavailable engine is recorded as failure/not completed, not as a pass. Overfull-box messages are recorded for subsequent inspection. Native compilation does not by itself certify visual layout; both PDFs still require page inspection.

No fresh native two-volume compilation or PDF visual-inspection certificate is embedded merely by publishing this source. Historical v26 diagnostic and build files that appear in the materialized tree remain historical. The current build's own record, not those earlier files, determines its execution status.

## Review status

The point-by-point response distinguishes established mathematical additions from the referee's editorial assessment of significance. It does not mark the manuscript accepted or independently approved. The original submission and review branches are left available for comparison. No merge, approval, branch-protection change or permission change is part of this source revision.
