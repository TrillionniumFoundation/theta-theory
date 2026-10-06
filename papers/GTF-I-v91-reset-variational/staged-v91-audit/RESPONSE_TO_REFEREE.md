# Response to the referee — General Theta Foundations I, v91 / R60

We thank the referee for the detailed verification of the preceding exact hierarchy and for identifying the unit-reset reduction as the decisive point requiring fuller exposition. We retain the paper's topic, all earlier mathematical results, and its four-leading-general-journal objective. The response strengthens the mathematics in two directions: an exact optimization principle for arbitrary finite two-call measurement experiments, and an equal-hypothesis-prior hierarchy on the same finite devices. The earlier referee's significance judgment remains in the frozen report for reconsideration; it is not represented as acceptance.

The controlling external report is `cf13712c54e9ef0c9c54a240b1f26efc78cc3568`, blob `dceb7c7d0c3e862ed494cdb46a0c50ec56bea5ed`. The controlling pipeline audit is `e4e72a512bf747e7bd190196cd8dc3db35689e3c`, blob `fc282d8e45e7ebf93e8897a3c9d407090f76ffd3`. Both reviewed v90 at `906e6e12841816f07e4ca31137690fd18bb65853`.

## Principal mathematical response

Primary Section 15 (source module 83) now gives a self-contained operational model and a complete, constructive branch normal form. Theorem `resetvariational91` applies to arbitrary finite experiments and arbitrary bounded rewards, not just to the designed ensemble: it identifies the exact reset optimum with a common-barycenter concave-envelope problem, proves attainment and bounds the number of instrument outcomes and receiver dimensions needed for an optimum. Theorem `resetdual91` gives an attained dual, with contact and spectral optimality conditions. The feedback corollary separates label feedback from receiver-instrument feedback.

Primary Section 17 (module 84) proves the equal-prior values `1/2+t^2(d-1)/(2d(d+1))`, `1/2+t^2(d-1)/(2d^2)` and `1/2+t^2/(2d)`. A centered filtered-swap inequality bounds the entire reset class. The same seven qubit devices give `7/12<5/8<3/4`; no tuning of the binary prior is needed. A further corollary gives an open perturbation neighborhood in the channels, prior and latent law. The previously proved biased-prior theorem is preserved in Primary Section 16 (module 82). These are exact finite decision statements; the local profile theorem remains a separate fixed-tube geometric result.

## Required revisions

**R01 — Unit-reset normal form.** Addressed in Primary Section 15, Lemma `resetnormal91`, preceded by Lemma `countable91`. Domain and codomain spaces of all rectangular coefficient and dilation maps are given. Instrument completeness implies the common Gram-matrix barycenter. Mixed preparations are purified on the correct side of the cut; arbitrary old environments stay old. Null histories are never normalized. A support-inverse construction supplies a converse realization, including singular source marginals.

**R02 — Formal optimization classes.** Definition `classes91` is self-contained. It includes public randomization, countable normal instruments, formal null histories, early stopping implemented by a discarded fresh call, final joint readout, and finite-dimensional trace-norm closure of the actual tester tuples. The old hierarchy explicitly refers to this definition. Separable effects are used only as a necessary condition for the classical class, not as an asserted converse characterization.

**R03 — Filtered-swap equality.** Lemma `centeredswap91` separates the trace-norm decomposition, eigenvalue inequality and fidelity inequality. Its equality argument normalizes both positive operators, uses unitary trace-norm maximization and Hilbert–Schmidt equality to prove normalized equality without invertibility, and then uses all d eigenvalues, including zeros, to force the flat spectrum. Nonzero singular factors are excluded directly. The old lemma points to this expanded proof; its original proof text remains.

**R04 — Shared latent index.** Both exact theorem statements repeat that the basis is sampled once and reused twice. They contrast independent redraws, whose averaged two-slot channel is the scalar product channel. This is a channel identity and applies to adaptive as well as entangled-input tests.

**R05 — Explicit qubit tester.** Primary Section 17, subsection `qubitexplicit91`, displays all seven devices, both prior systems, the normalized Bell pairs, normalized antisymmetric input and reference states, receiver blocks with factor 1/4, tester blocks and positive complements, causal partial traces, and every event probability giving both exact triples.

**R06 — Independent priority assessment.** The current comparison is extended to the general variational theorem, concave-envelope antecedents and conic duality. The exact claims to be assessed are listed in `INDEPENDENT_REVIEW_BRIEF.md`. No independent human specialist opinion has been obtained in this revision; this request remains an external assessment rather than a falsely closed item. There is no firstness assertion based on repository dates, successful tests or an unsuccessful search for an equivalent theorem.

**R07 — Conceptual separation.** The introduction distinguishes three levels: fixed-tube local orders with arbitrary hard call resources; exact reset values for arbitrary finite two-call experiments; and exact solutions of the two basis experiments. They share the measurement interface and fresh-preparation cut, but neither local nor example theorem is treated as a premise of the other.

**R08 — Current audit identities.** The active `PROOF_AUDIT.md`, `HISTORY_AND_PIPELINE_AUDIT.md` and `INTERNAL_MATHEMATICAL_REVIEW.md` now identify v91 and cover its actual theorems. Their v90-tree versions, including the older headings noted by the referee, are preserved byte-for-byte in `predecessor-v90-audit/`.

**R09 — Printed numbering.** Current prose uses Primary Sections 15–17 first, followed by source-module identifiers where useful. Stable theorem labels and the generated printed-number/page map prevent confusion between the primary and complete edition. Historical replies retain their original numbering as historical records.

**R10 — Finite design.** The old family is called a weighted exact second-moment family. Weights are real. No algebraic or rational data are required by the decision theorem. The ambient dimension and `d^6+1` support bound are existence bounds, not optimal size or polynomial bit-complexity claims.

**R11 — Robustness quantifiers.** The old statement now specifies the same unhalved diamond bound for the scalar channel and every entire basis channel individually, fixed priors and fixed latent law. The new stability corollary also permits prior and law changes, with explicit total-variation cost. Optimal-class stability is separated from the additional certified preparation defect of one exhibited implementation; the event-probability factor 1/2 is retained.

**R12 — Release semantics.** The predecessor's failed transport, sequential API handoff and successful exact-head check remain separately recorded. The new build and final-head checks must be observed anew. Current records distinguish Actions check runs from the legacy status API and object hashes from human signatures. No anticipated workflow result is a receipt.

**R13 — Journal-facing package.** The standalone journal archive contains exactly the primary, one linked supplement, their active TeX/figure dependencies, a concise reproducibility note and its read-only verifier/manifest. Historical responses, schemas, full research edition, structural article and executable audit trail remain in the research archive rather than the initial journal route. Nothing is deleted from the research record.

**R14 — Scope.** The general theorem now supplies an arbitrary finite-experiment optimum, including arbitrary fixed-pair value problems. It does not assert strict advantage for every pair. The exact separation still concerns a once-selected latent device; no full memory-dimension hierarchy, global POVM-body metric or efficient synthesis result is inferred. Thus the revision extends the proved scope rather than merely changing its language.

**R15 — Wider pipeline.** The A2 replacement, B4 and C2 aggregates, eleven-paper aggregate and whole Theta programme remain logically independent. Their flags remain false in `PROOF_STATUS.json`. No finite-dimensional decision theorem substitutes for the analytic component laws.

## Detailed comments

**D01.** The prior sum and difference appear next to the old theorem's strictness clause; equal priors are explicit in the new game.
**D02.** The first-moment assertion is stated as equality of measurement channels, including arbitrary references.
**D03.** Weighted exact second-moment family is used; an unweighted design is not assumed.
**D04.** The ambient dimension is at most d^6 and support size is an existence bound only.
**D05.** Definition `classes91` uses finite-dimensional trace-norm closure; the normalized separable cone is shown compact and its cone closed.
**D06.** The complete-call cut is I1Y1 versus I2Y2 in the stated Choi order.
**D07.** The equal-payoff proof records that swap and its symmetric/antisymmetric projections are real, while general complex effect transposes remain explicit.
**D08.** All coefficient maps have explicit rectangular domains and codomains; no square-receiver restriction is imposed.
**D09.** Trace-preserving dilation completeness gives the Gram identity, and the countable lemma supplies a remainder branch.
**D10.** Every rule is defined at formal null histories; neither proof divides by branch probability.
**D11.** Positive-part optimization is displayed at the reset upper.
**D12.** The old rigidity observation remains limited to nonrandomized optimal protocols in the selected purified normal form; dilation/readout uniqueness is not claimed.
**D13.** Lemma `countable91` proves the needed positive trace-class tail estimate and normal-instrument truncation.
**D14.** Independent complete acquisitions and subsequent joint reference measurement are explicitly distinguished.
**D15.** The equal-prior theorem emphasizes that feedback is allowed in the upper and unnecessary in the attaining construction; the general concave-envelope corollary explains its possible role outside the example.
**D16.** Proposition `causalnormal91` names the direct physical tester construction, positive complements and causal marginals.
**D17.** The attaining antisymmetric input has trace one and lies in the nonzero antisymmetric subspace for d>=2.
**D18.** The explicit Pauli family includes both output orders, and the cancellation of first moments explains their role.
**D19.** Every probability perturbation retains the half-factor relative to unhalved trace distance.
**D20.** Perturbations may depend on the basis index and alter its effects, provided each entire resulting measurement channel is legal and delta-close.
**D21.** At t=0 both hierarchy theorems explicitly give three values 1/2.
**D22.** Projective t=1 and null branches are covered by the normal form and singular-factor proof.
**D23.** The introduction separates exact dimension-dependent formulas from fixed-tube local constants.
**D24.** Effective width V/N and Q remain call-allocation resources, not Hilbert-space dimensions. The general theorem's receiver bound is stated separately.
**D25.** The individual-policy upper and class-optimum lower remain distinct; a large Q_pi is not an information certificate.
**D26.** All previously relocated labels stay active in the linked supplement and are verified through the current joint source graphs.
**D27.** Actual engine warnings are retained in logs and receipts; no warning-free claim is made before inspection.
**D28.** Actions checks and legacy statuses are distinct in the release record.
**D29.** Reconstructed object identity is not a human signature; unsigned objects are reported as such.
**D30.** The frozen report is an author-requested external assessment, not a commissioned decision of any named journal.

## Preservation and verification boundary

Every v90 native file remains available, and every preceding active mathematical label is checked in the current graphs. Old mathematical paragraphs are unchanged except for registered additive convention paragraphs in the old hierarchy. The structural graph is unchanged. The new finite checkers test algebraic instances and negative controls; the manuscript, not finite replay, supplies the universal proofs. The build receipt, standalone reconstruction and exact final-head receipt record only executions that actually occurred.


## General classical-versus-quantum receiver criterion

Primary Section 15 additionally proves Theorem `classicalroof91`: complete classical readout is exactly the same common-barycenter problem with atoms restricted to rank-one density matrices. A complete first measurement can be spectrally refined without loss, and a rank-one Gram factor carries only a known receiver state; these give both operational directions. Compact graph convexification and the same strictly feasible hypograph dual give attained classical primal and dual optima. Corollary `gapcertificate91` then gives necessary and sufficient certificates of a strict retained-receiver advantage, and all-density dual contacts characterize equality. This extends the R60 breadth response to an exact general comparison criterion, not merely an evaluated example.

The finite receiver dimensions refer to retained registers at the recording cuts, not to all temporary workspaces of a selected implementation of an instrument. The dual majorizations remain universal requirements and are not checked by sampling.
