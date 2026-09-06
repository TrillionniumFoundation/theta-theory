# A1 English v5 — finite-horizon information states

**Manuscript:** *Finite-Horizon Information States of Calibrated Experiments: Realization, memory–decision laws, and mechanical response*.

Author: Qian Qi. Revision date: 6 September 2026.

## Controlling source and revision entrance

This revision responds to `reviews/a1-english-v4-2026-09-06/REFEREE_REPORT.md` on review branch `review/a1-english-v4-harsh-referee-2026-09-06`, pinned at `58796c768d14c280020d05916feb946db8fb25ab`. Its reviewed manuscript is **exactly** `papers/A1-english-v4/` at `e4b10bf7acebf38dbcfb466b3ee4cf30bb77b381`, directory tree `6f02757c8db44826ceeb9de097999cd60e4470ce`. The similarly named earlier v4 sibling is not the controlling source.

Canonical new branch: `revision/a1-english-v5-finite-horizon-decision-law-2026-09-06`.

Start with `main.tex`, then `RESPONSE_TO_REFEREE.md` and `PROOF_LEDGER.md`. `SOURCE_MANIFEST.json` identifies preserved blobs and the new files. The ordinary checked-in source tree compiles directly; no orphan tree, encoded source archive, or workflow materialization step is required.

## Mathematical revision

The center of the paper is now an attainable **state–memory–decision law**, rather than a list of valid but separately motivated additions:

* A fixed four-symbol detector and four-entry lookup comparator have an explicitly invertible calibration matrix. No arbitrary angle-dependent gate or programmable inverse-CDF family is needed for this class.
* With full polynomial degree q, n observed cartridges and m future cartridges, the exact observable-future decision dimension is **d = q min(n,m)**. A causal implementation has the tent-shaped profile q min(n,N−n). The qn full-posterior theorem remains intact for richer terminal loss classes.
* A fixed observable Brier-score query task has matching minimax finite-memory regret bounds **constant × M^(−2/d)**, including randomized codes with no historical side channel. The query is revealed after encoding. A separate theorem proves the same exponent for unconditional expected regret under one fixed random exploration rule, not merely a worst-command conditional family. Both types of failed trial are charged. An explicit contraction argument makes the attainable lower-bound ball quantitatively checkable from calibration and prior moments.
* The same four-entry query convention and the same resource budget give d = 3 min(n,m) with the collision sign and d = 2 min(n,m) after sign erasure. The sharp exponent changes under removal of the structural feature.
* An independent two-cartridge score comparison has a strictly positive **zero-acceptance-cost** value of that sign, with an exact covariance formula. It is not the old acceptance-cost-saving witness.
* The referee's fixed-space n(r−1) product dimension and full-horizon two-arc argument are incorporated with explicit attribution, full proofs and Borel implementation details.

These results concern the declared finite calibrated class and checkpoint memory model. They do not purport to prove finite-energy hardware complexity, a horizon-uniform bit constant, an arbitrary hidden-parameter-loss quotient, or long-orbit response.

## Preservation

The entire reviewed v4 tree is retained byte-for-byte as `retained-v4/`; its tree identity is the one above. The branch also retains the original `papers/A1-english-v4/`, review reports and historical repository tree, because the revision commit descends from the controlling review HEAD.

All **22 inherited principal labels** remain in the integrated manuscript. The **20 component proof-bearing statements** are in ten unchanged source blobs; the two overview closure statements are presented in Appendix B. The original complete overview, provenance narrative, tests, validation receipts and foundation companion are also retained in `retained-v4/`. The stability estimates and their proofs remain; their historical execution narrative has been moved out of the mathematical presentation, not erased from the archive. The old adaptive theorem, all 64 comparison entries and its full-class proof remain in the paper, with its binary cost-saving mechanism explicitly distinguished from the new central results.

The main text now has **34 principal theorem/proposition/lemma labels** (22 retained and 12 new, including one overview). Counts are navigation, not a significance claim or a verification certificate.

## Reproduction and actual validation status

From this directory:

```sh
python tests/test_v5.py
python build_and_verify.py --audit
python build_and_verify.py --build
```

Python requires SymPy. PDF construction requires `latexmk` and a standard LaTeX installation with the packages declared in `main.tex`. The audit checks the input graph, references, citation keys, inherited component blob identities and the 22-label preservation contract. The build command additionally compiles the complete manuscript and writes its own `validation/V5_BUILD.json` receipt; it does not treat an old PDF receipt as current.

**Executed in this authoring session:** `tests/test_v5.py`, 50/50 exact rational or symbolic finite diagnostics, recorded in `validation/V5_CHECKS.json`. The script's SHA-256 is in that receipt. Displayed floating values are only renderings of exact interval bounds. The rational calibration proxy used by some finite span diagnostics is explicitly labelled, while the physical calibration determinant and physical positive-gain enclosure are checked separately.

**Not represented as executed by that receipt:** the 39-check referee program, the inherited author test suites, a full manuscript PDF build, a PDF visual review, proof-assistant verification, an exhaustive priority search, or independent referee acceptance. `validation/V5_STATUS.json` records the authoring-session boundary; later actual build receipts, if generated, must be identified separately rather than silently substituted.

The original referee script is preserved at the repository review path and was read for its exact certificate and binary ablation; no current rerun is claimed. The internal report and this revision are research-review materials, not journal decisions. The present package is ready for another substantive referee examination of the written proofs.
