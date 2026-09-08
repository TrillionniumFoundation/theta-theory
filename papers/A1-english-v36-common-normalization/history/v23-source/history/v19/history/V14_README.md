# A1, English revision 14

**Attainable information geometry across exponent collisions**  
Author: Qian Qi  
Date: 6 September 2026

This is the complete English revision responding to the latest A1 v13 report.
The principal manuscript is `main.pdf`; its editable entry point is `main.tex`.
The complete proof text is compiled, including the retained appendices.

## Immutable basis

- Controlling review: `00b0844a7c2fb16b3231abf163d5004fd9e253cd`,
  `reviews/a1-english-v13-common-moment-2026-09-06/`.
- Reviewed submission: `fc6465b86fbc7ee6a4e8f3ccfb54ea32a64dc8b6`,
  `papers/A1-english-v13/`.
- Revision branch: `revision/a1-english-v14-geometric-response-2026-09-06`.

The review reports no new blocking mathematical or implementation defect in
its examined chain. This revision addresses E13.1--E13.3, rather than reopening
closed precision, horizon or common-name diagnostics.

## Reading order

Theorem 1.1 states the geometric classification. Its main argument culminates
in Lemma 5.2 and Theorems 5.3--5.4: actual positive histories attain every
truncated collision flag, a separate global cover controls the entire image,
and a causal recurrence realizes the same profile.

Section 6 proves a further geometric distinction. The prior ambiguity body
has all the Newton widths, without the acquired-history dimension truncation.
Lemma 6.1 constructs a bounded dual; Proposition 6.2 gives the simultaneous
body inclusions and widths; Corollary 6.3 resolves the residual uncertainty
under exact lower-moment information. A collision invisible to the three-trial
memory exponent remains visible in a vanishing prior-uncertainty direction.
This local known-calibration problem is explicitly distinguished from the
imperfect common-name problem.

Theorem 7.1 retains the joint prior-and-calibration common-name minimax law,
including its interior/slack hypotheses. The complete numerical realization
statement is Theorem H.9. All compiler contracts, resource accounting and
request-conformance proofs remain in Appendices H--K. Historical algebraic,
confluent, decision and common-risk results remain in Appendices A--G.
The principal narrative is not a sequence of implementation repair notes.

## Referee materials and reproducibility

`RESPONSE_TO_REFEREE.md` answers E13.1--E13.3 point by point.
`PROOF_LEDGER.md` gives mathematical dependencies and stable source labels.
`HISTORICAL_DERIVATION_MAP.md` records actual historical sources consulted.
`LITERATURE_VERIFICATION.md` separates checked primary inputs from priority
claims. `NUMERICAL_EVIDENCE.md` and `VISUAL_INSPECTION.md` state the evidence
boundary. The `history/` records preserve earlier versions of the replaced
editorial documents and build scripts.

From this directory, with Python 3 and a standard AMS-capable LaTeX installation:

```sh
python3 validate.py
# For a source-only preservation check:
python3 build.py --prepare-only
# For a separate three-pass PDF build:
python3 build.py
```

`validate.py` verifies the source manifest, reruns four unchanged author suites
and the new exact-rational suite, and rebuilds the PDF. The optional
`--prior-review` additionally executes the original v13 review probe against
its pinned v13 source directory; it requires the full repository. A standalone
v14 package does not need adjacent historical directories for its own tests.

The source-preservation checker retains all 74 complete v13 proof blocks and
all 77 complete theorem/lemma/proposition/corollary statements byte for byte.
The manuscript has 77 proof blocks and 80 named results after the three new
results. These counts certify source preservation, not mathematical truth or
journal suitability. No older source directory, review, main branch or other
paper is replaced or deleted.
