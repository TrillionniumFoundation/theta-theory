# Response to the v8 referee — A1 English revision 9

**Controlling report:** `reviews/a1-english-v8-2026-09-06/REFEREE_REPORT.md` at `5f52bf456272b53bcb4df8d949effd2ab59bb79f`.  
**Reviewed submission:** `5d3d7e04b172f98bddfd037c488d93d516d20a98`.  
**New principal:** `papers/A1-english-v9/main.tex`.  
**New title:** *Sparse observation algebras and memory across exponent collisions*.

We thank the referee for separating the correctness findings from the negative editorial recommendation, and for expressly closing the previous attainable-geometry and causal-compatibility objections. This revision starts from those closures. It does not replace the theorem with weaker claims or characterize the research program as impossible. All 34 predecessor result labels and all 33 predecessor proof blocks remain in the new principal; every pre-existing repository path is left unchanged.

The principal change is mathematical. The new theorem replaces the one-parameter affine family by an arbitrary compact set of calibrations in the open one-step exponent chamber. Additive sum collisions may lie in the interior, meet each other, or be approached with arbitrarily high contact order. The calibration set need not be an analytic or semialgebraic family, nor be a path. Resolution is specified intrinsically by maximal Vandermonde products of the actual future exponent nodes. We prove attainable transversality for all repeated-node Newton flags and make the resulting sharp profile causally compatible. A tree allocation theorem then determines pathwise phases from pairwise collision orders.

## E8.1 — Identify the new mathematical assertion, not a list of classical mechanisms

**Change:** Introduction, `thm:resolution-main`; Section `sec:collision-geometry`, especially `lem:newton-attainment`, `thm:intrinsic-checkpoint` and `thm:intrinsic-streaming`.

Finite Leja ordering, divided differences, Hermite interpolation, real integral-geometric entropy bounds and finite-horizon error propagation are explicitly treated as classical. The elementary finite Leja determinant estimates are supplied in full because their zero-pivot form is used, not because a new interpolation algorithm is claimed. The exposition does not count these inputs as independent advances.

The geometric assertion is instead this: at one interior binomial command tuple, the normalized product tangent is transverse to every initial Newton flag, including arbitrary multisets with repeated nodes, with a lower singular-value bound uniform over the compact calibration chamber and all finite orderings. An initial list of divided-difference functionals spans a complete Hermite evaluation space; adjoining the constant allows the strict mixed/confluent pairing to be applied. Normalization loses precisely one rank. This direct collision statement precedes the compactness argument.

The acquired-history lower bound retains all-failure evidence. The upper bound covers the entire reachable image, whose bounded-format dimension is at most the past capacity; it does not substitute the local minorized cube for that image. The intrinsic maximal determinant products identify the resulting scales independently of a chosen collision path. The online proof stores only a reachable raw-moment representative index and uses no reciprocal exponent gaps.

These statements are the proposed mathematical strengthening to be assessed. We do not infer originality or journal significance merely from the length of the manuscript, the number of labels or successful diagnostics.

## E8.2 — Broaden the class while keeping quantitative resource statements exact

**Change:** Theorems `thm:resolution-main`, `thm:intrinsic-checkpoint`, `thm:intrinsic-streaming`; Corollary `cor:intrinsic-bits`; abstract and scope section.

Let the one-step exponent vector a range over a compact subset K of 0<a1<...<a(r−1), with one fixed full-rank coefficient matrix defining uniformly positive cells. Normalize all future sum exponents into a fixed unit interval. For each m and l, let V(m,l;a) be the largest absolute Vandermonde product among l positive formal future labels, retaining coincident labels. Set p=min(n(r−1),q_m). The new law is

    checkpoint regret  ≍  max_(1≤l≤p) (V(m,l;a)/M)^(2/l),
    streaming regret   ≍  max over n+m=N of the checkpoint profile.

The constants are uniform in a and M, including at additive collisions. The one-step exponent vector itself remains in an open rank-preserving chamber; this assumption is explicit, not a claim about one-step rank loss. The codebook may depend on the known a, prior and M. There is one stage-compatible transducer for each such experiment, not one calibration-blind codebook. The lower bounds use prefixes of a common uniform-command exploration law and a fixed product-probe menu whose trials are counted.

The fixed full-support prior and fixed horizon are retained. In particular the technical note's concentrating-prior example correctly precludes a uniform positive lower constant over all full-support priors. The new result does not claim such a constant, a horizon-uniform complexity theorem, an effective synthesis procedure or a matching lower bound for arbitrary control tasks. No limitation is concealed by replacing an exact resource definition with a broader slogan. The genuine enlargement is from affine-path scales to intrinsic collision geometry throughout K.

## E8.3 — Supply a structural consequence beyond another affine horizon

**Change:** Theorem `thm:collision-tree` and Corollary `cor:two-parameter`.

The collision-tree theorem determines all resolution exponents on a path directly from pairwise orders of exponent differences. The lth exponent is the minimum, over l selected leaves, of the sum of their pairwise collision orders. Those orders define a nested cluster tree; a finite min-convolution recurrence computes the entire profile. The ordinary affine list is recovered when orders are one within each limiting cluster and zero between clusters. Nonaffine orders of contact are not encoded by that affine multiplicity list.

The two-parameter application uses A(u,v)={0,1,2+u,3+v} in a positive four-cell experiment. Three collision lines meet at the origin. With rho=max(|u|,|v|) and tau=min(|u|,|v−u|,|v−2u|), the full five-trial streaming profile is

    max { M^(−1/3), rho^(1/2) M^(−1/4),
          (rho^2 tau)^(2/9) M^(−2/9) }.

The exact peak has dimension nine away from the lines, eight on a line away from the origin, and six at the origin. Along u=theta, v=theta+theta^k for any integer k≥2, the crossover budgets have orders theta^(−6) and theta^(−(8k−2)). The contact order changes the resolution law without changing the limiting multiplicities. This is an application of the new intrinsic theorem, not an extrapolation of the predecessor's affine result. It also includes negative parameters and exact interior collision loci in one uniform statement.

The tree theorem and the collision arrangement remain consequences of the same attainable geometry. We do not count the inherited ticket identity as an independent source of depth, and do not claim that any particular extension guarantees a four-journal editorial outcome. The subsequent referee can assess the stronger result itself.

## P8.1 — Put the quantifiers in the statements

**Implemented.** The introduction, abstract and new streaming theorem state: for the fixed experiment, prior and horizon, there exist constants c,C; for every known calibration and every integer M, there exists one M-label transducer compatible with every stage. The old affine streaming theorem also now says explicitly that the filter may depend on calibration and M. The compact-chamber constants may depend on the prior. No joint measurable or computable selection of codebooks over K is asserted or needed.

## P8.2 — Pin the cited versions

**Implemented.** The bibliography specifies Zhang–Kileel, arXiv:2311.05116v4, 6 June 2025, Lemma 2.18, printed p. 11. The Comte–Halupczok entry now includes *Compositio Mathematica* 161 (2025), no. 5, 959–992, DOI 10.1112/S0010437X25007031, and retains the precise preprint equations (4)–(5) used for the real variations and entropy inequality. `REFERENCE_AUDIT.md` records the primary-source checks and distinguishes that real input from the paper's nonarchimedean results. Leja, Bos–De Marchi–Sommariva–Vianello and de Boor are credited for the additional classical interpolation context.

## P8.3 — State the final classification first

**Implemented.** `thm:resolution-main` is the first named theorem of the introduction. It gives the intrinsic checkpoint and causal classification, the query/acquisition convention, the quantifier order and the scope of uniformity. The exact predecessor follows as its algebraic and attainable foundation. The old full-future and affine proofs and all concrete comparisons remain explicit subsidiary developments; none is deleted to make room for the new theorem. Editorial correspondence, reproducibility instructions and the proof ledger are outside the principal mathematical narrative.

## P8.4 — Make the standalone omission explicit

**Implemented by packaging the exact required predecessor input.** The proposed automatic source-generation and inherited-test rewrite could not be published because the tool blocked those script writes; neither blocked script is part of this delivery. We instead retain the original v8 test program unchanged and include its exact sibling `papers/A1-english-v7/sections/` input in the standalone review archive. The repository already contains that input. A fresh execution in the packaged layout runs all 256 inherited v8 assertions, with no missing-predecessor omission. This follows the referee's explicit alternative of packaging the required predecessor input rather than modifying the conditional assertion.

The new v9 suite additionally checks the source-pinned v8 label and proof-hash metadata packaged in `validation/V8_PREDECESSOR.json`; this check does not require sibling sources. Local receipts identify the executed inputs and test counts. No fresh GitHub Actions build or remote PDF-publication success is claimed. The complete manuscript sources are committed directly, and the locally built PDF and execution receipts are included in the accompanying review archive.

## Previously closed points and handoff

The v7-to-v8 closures concerning actual failure evidence, the attainable global cover, the dimension truncation, index-only updates, the common decision baseline and the distinction between continuous history encodings and quotient charts are maintained. The original v8 seven-trial result and the technical note's second-order affine example are not relabeled as v9 discoveries. The mechanical experiment keeps its separate counting convention and complete proof.

`PROOF_LEDGER.md` gives the new dependency map. `HISTORICAL_DERIVATION_MAP.md` records which earlier derivations were consulted. Actual finite executions, source hashes and the publication build are recorded separately. This response does not stand in for the proofs, and successful tests do not stand in for the next referee's mathematical judgment.
