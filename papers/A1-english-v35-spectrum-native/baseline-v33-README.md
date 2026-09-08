# A1 English v33 — moment controllers

**Attainable information, exponent collisions, and finite-state realization**  
Qian Qi · September 8, 2026

This is the revision responding to the v32 independent referee report at
`60c5b116a2c002dfd8056a351a87d7014d8c78e1`. The reviewed manuscript is
`e712437fe13cf29978715d3f16d825eadb450fea`, directory
`papers/A1-english-v32-causal-certificates`.

## Reading order

`main.tex` is the complete main article. The executed build has **35 pages**.
`companions.tex` contains the complete additional developments, **159 pages**.
The main article retains the full collision classification and its proofs,
and adds an exact common-controller representation in the original
shared-latent, per-report charged model. The companion retains the graph,
occupation, regenerative, exact-kernel, structural and effective proofs
under their stated, distinct resource conventions.

The new central statements are Theorems 8.3 (exact finite-moment common
controller), 8.6 (deterministic realization of the entire mean-risk vector),
8.7 (polyhedral updates for scalarized risks), and 8.8 (compact collision
transfer). Theorem 11.4 separates numerical precision from the intrinsic
collision profile. Theorem 12.1 and Corollary 12.2 give an analytically
solved continuous-command two-label experiment and an executed rational
lower/upper certificate covering all admissible stochastic encoders.

`RESPONSE_TO_REFEREE_V33.md` responds to the five principal objections.
`PROOF_LEDGER_V33.md` records dependencies and retained quantifiers.
`MODEL_AND_COMPARISON_V33.md` separates information models and the precise
finite-approximation comparisons used in Section 13.

## Reproduce

From this directory, with Python 3.10+ and a TeX installation providing
`pdflatex`, `amsart`, Latin Modern, `mathtools`, `mathrsfs`, `geometry`,
`microtype`, `booktabs`, `xr-hyper` and `hyperref`:

```sh
python v33/build_revision.py
python v33/certify_instance.py > verification-v33/EXACT_CERTIFICATE.json
python -O v33/certify_instance.py > verification-v33/EXACT_CERTIFICATE.optimized.json
cmp verification-v33/EXACT_CERTIFICATE.json verification-v33/EXACT_CERTIFICATE.optimized.json
```

The build compiles both full volumes, regenerates external labels and
checks reference convergence, undefined references/citations, duplicate
labels and overfull boxes. It does not substitute a short theorem packet
for either volume. `verification-v33/BUILD_RECEIPT.json` records the actual
six successful compiler invocations, hashes of 79 active TeX inputs and
the two generated PDFs. `SESSION_CHECKS.json` records visual inspection,
exact splitting of the inherited v32 new-results chapter, and the two
identical arithmetic executions. Build logs and PDFs are supplied in the
conversation review package; regenerating them requires no network.

Only **verification-v33** records execution for this revision. Inherited
CI/diagnostic/status files elsewhere in this directory are historical and
must not be read as v33 CI results. The recorded build ran locally; no
successful GitHub Actions run is claimed. The arithmetic evaluates the
analytic global certificate, not the general exhaustive controller net;
no formal proof-assistant verification is claimed.

## Preservation and scope

The native directory tree is based on the entire reviewed v32 directory.
No inherited proof source or historical derivation is deleted. Original
entrypoints are retained in `v33/inherited_entrypoints/`. The concatenation
of `v33/finite_compatibility.tex` and `v33/delayed_use.tex` equals
`v32/new_results.tex` byte for byte. The latter delayed-use model is now
in the companion, where its block-charging convention is explicit.
The original collision theorem is not weakened. Purification concerns
mean checkpoint risks, not risk at each history or a public persistent
seed. The moment formula is exact but nonconvex; its coefficient
calculation and global solution are not claimed polynomial-time.
