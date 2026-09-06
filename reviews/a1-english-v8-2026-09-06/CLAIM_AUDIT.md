# Claim audit — A1 English v8

**Submission:** `5d3d7e04b172f98bddfd037c488d93d516d20a98`.  
**Scope:** all 34 principal result labels and the two operational definitions.  
**Meaning of disposition:** “No blocking defect identified” records a mathematical reading under the printed assumptions, not formal verification, exhaustive priority checking, or a publication endorsement.

All paths below are relative to `papers/A1-english-v8/` at the submission SHA. Section filenames without a directory prefix refer to `sections/`. Numbers and PDF pages come from the fresh three-pass build. The main [REFEREE_REPORT.md](REFEREE_REPORT.md) separates the editorial recommendation from these technical findings.

## A. Exact experiment and attainable rank

| Number / page | Label and source location | Audit finding |
|---|---|---|
| 1.1 / 2 | `thm:main`; `sections/01_introduction.tex:30–54` | Future equivalence, normalized attainable rank, continuous-encoding dimension and causal peak are supported by Sections 2–3. Generic rank is not a uniform conditioning statement. No blocking defect identified. |
| 2.1 / 5 | `lem:interior`; `02_experiments.tex:25–48` | A linear right inverse of the spanning calibration gives an actual open failure-factor neighborhood. The positive r-cell construction spans the claimed space. |
| 2.2 / 6 | `def:future`; `02_experiments.tex:61–70` | Common future-only rules cannot read a discarded prefix or seed. This is the necessary operational quantifier, not equivalence for arbitrary past-dependent tasks. |
| 2.3 / 6 | `prop:tests`; `02_experiments.tex:78–106` | Actual nonadaptive failure products span the future monomials. An adaptive future word still has a product likelihood along its branch. All probe trials are counted. |
| 3.1 / 7 | `lem:mixed-moment`; `03_transversality.tex:5–46` | Generalized Vandermonde signs and the determinant integral give strict mixed minors for full-support priors. Prior densities are unnecessary. |
| 3.2 / 7 | `lem:binomial-tangent`; `03_transversality.tex:48–88` | Complementary products form a basis in t^D. Interior exponent strings are disjoint; the tangent has n(r−1)+1 monomials and contains the product. |
| 3.3 / 8 | `thm:rank`; `03_transversality.tex:90–149` | Normalization removes exactly the product direction. Global rank caps, a nonzero rational minor and a projected local section justify genericity and local attainment. |
| 3.4 / 9 | `thm:causal`; `03_transversality.tex:151–197` | Invariance of domain gives the continuous-encoding lower bound. Ordered normalized factors or future moments give the upper state and one-way causal switch. Not a global quotient chart. |
| 4.1 / 9 | `prop:three`; `04_observation_algebra.tex:13–51` | The principal homogeneous binomial relation and its injective multiplication give the Hilbert function. Irrational exponent ratio gives distinct sums. |
| 4.2 / 10 | `cor:sparse-example`; `04_observation_algebra.tex:53–73` | The sparse sumsets and asymmetric dimension profile follow from the general formulas. The originating referee example is credited. |

## B. Full-future confluence and inherited streaming

| Number / page | Label and source location | Audit finding |
|---|---|---|
| 5.1 / 11 | `thm:confluent-law`; `05_confluence.tex:78–111,320–351` | Supported under its full-future inequality and positive future length. Uniform metric scales, acquired-history cube and integer-budget rectangle estimates match. |
| 5.2 / 12 | `lem:confluent-positive`; `05_confluence.tex:117–160` | Complete exponential-polynomial blocks are a Chebyshev system. The sign and determinant-integration argument prove the collision rank directly. |
| 5.3 / 12 | `lem:observable-scales`; `05_confluence.tex:162–217` | Positive base exponents bound logarithmic jets at zero. Exact Newton interpolation gives a fixed full-column-rank probe matrix times the scale diagonal. |
| 5.4 / 13 | `lem:uniform-patch`; `05_confluence.tex:219–285` | Common witness, compact least singular value, local inverse and complementary-coordinate integration give a uniform subprobability cube retaining failure evidence. |
| 5.5 / 14 | `lem:rectangle`; `05_confluence.tex:288–318` | Floor allocation respects at most M cells. Projection and union-of-balls give every initial-axis lower bound. Zero side lengths may be omitted. |
| 6.1 / 15 | `def:finite-state`; `06_streaming.tex:8–25` | Persistent state is an index; clock and fixed real program are read-only. Old commands/seeds are not free. Workspace, precision and effective synthesis are outside the model. |
| 6.2 / 16 | `lem:lipschitz`; `06_streaming.tex:42–77` | Interpolated positive factors or posterior mixtures control denominators on line segments. Changeover and moment updates are Lipschitz on the relevant compact sets. |
| 6.3 / 16 | `thm:stream-upper`; `06_streaming.tex:79–135` | Reachable grid representatives and the full repeated-error recurrence implement a genuine streaming upper bound. Exact history exists only in the analysis. |
| 6.4 / 17 | `thm:stream-lower`; `06_streaming.tex:137–217` | One prescribed continuous-command experiment minorizes a projected attainable ball. Query timing and independent coins are handled. The exponent and bit law follow for fixed N. |
| 6.5 / 18 | `thm:control-bound`; `06_streaming.tex:219–259` | Uniform state-Lipschitz Bellman objectives and greedy representative actions yield the separate, weaker control-loss power. No continuity of an optimizer or matching arbitrary-task lower bound is required. |

## C. New attainable-filtration extension

The eight results below are in `sections/06a_attainable_filtration.tex`.

| Number / page | Label and source lines | Audit finding |
|---|---|---|
| 7.1 / 19 | `thm:attainable-checkpoint`; 35–53,295–329 | Initial-flag minorization supplies the lower bound; a bounded-format cover of the complete scaled reachable image supplies the upper bound. The truncated dimension, not the ambient future dimension, controls the last exponent. No blocking defect identified. |
| 7.2 / 20 | `thm:general-uniform-streaming`; 55–93,375–423 | Stage-specific reachable raw codebooks, nonsingular physical updates and repeated quantization prove the maximum-stage law for any fixed horizon in the admitted affine interval. One common exploration law supports all checkpoint lower bounds. Clarify that “single” means all stages for each known calibration and budget, not calibration-blind codebooks. |
| 7.3 / 20 | `lem:tame-rectangle`; 95–178 | Real variations vanish above dimension p. Uniform component bounds and projected-zonotope volume give the anisotropic entropy polynomial. Budget inversion, recentering, zero widths and Borel ties are addressed. A classical geometric consequence, not a newly established universal entropy principle. |
| 7.4 / 21 | `lem:attainable-format`; 180–225 | Moment integrals are coefficients of polynomial command maps. Fixed format is independent of their values and does not require semialgebraic dependence on calibration or a prior density. Prior-normalized factors give the dimension cap. |
| 7.5 / 22 | `lem:attained-flag`; 227–293 | Sorted prefixes consist of complete initial cluster blocks. Strict mixed/confluent pairing, the exact normalization rank loss and the acquired-history inverse argument prove the required uniform p-dimensional minorization. |
| 7.6 / 23 | `lem:raw-uniform-update`; 331–373 | Formal exponent addition closes the shrinking moment update. Report positivity controls quotient derivatives on posterior mixtures, including coincident labels. No inverse power of calibration appears. |
| 7.7 / 24 | `cor:general-bit-profile`; 425–448 | Solving all stage/axis inequalities and rounding M to a power of two gives the stated additive-O(1) bit law. At zero only terms of order zero survive. |
| 7.8 / 25 | `cor:seven-trial`; 450–519 | Six strong and two weak attainable axes give the stated two-regime law. Earlier stages' crude dimension caps and duplicate-tolerant raw updates justify the entire [0,1/2] interval despite longer-sumset collisions. The v7 boundary is resolved, not ignored. |

## D. Five-trial, decision and mechanical consequences

| Number / page | Label and source location | Audit finding |
|---|---|---|
| 8.1 / 26 | `thm:uniform-streaming`; `07_uniform_resolution.tex:50–82,141–241` | Explicit two/four-factor coordinates, the physical five-coordinate peak and the shrinking raw update supply the uniform five-trial rate. It is consistent with the general theorem. |
| 8.2 / 27 | `lem:five-patch`; `07_uniform_resolution.tex:85–139` | The common command witness is interior; confluent positivity proves the limiting rank. The displayed rational minor is correct but is not substituted for the all-prior argument. |
| 8.3 / 29 | `cor:uniform-bits`; `07_uniform_resolution.tex:243–269` | Two-regime inversion and the infimum defining the high-resolution lower-constant scale give the printed formulas. Scope is the fixed five-trial experiment. |
| 9.1 / 30 | `prop:ticket-identity`; `08_sequential_value.tex:28–64` | The independently priced threshold rule gives an exact half-squared-loss identity for the same encoder. It is a transfer, not an independent geometric theory. |
| 9.2 / 30 | `thm:resolved-value`; `08_sequential_value.tex:86–163` | The same-task exact erasure identity and cube minorization give the quadratic weak-direction value. The comparator receives the entire specified exact statistic, not an arbitrary four-dimensional encoding. |
| 9.3 / 31 | `cor:necessary-budget`; `08_sequential_value.tex:174–206` | The exact same-baseline difference E_theta−L_M gives both sides of the first-crossing budget order. Correctly credited to the v7 note. It is not an exact integer threshold or an equal-compressed-budget equality. |
| 10.1 / 33 | `thm:finite-bit-value`; `09_common_risk.tex:104–181` | Conditional means and finite partitions give the exact common-risk optimum; deterministic encoding suffices under squared loss. Weighted merge identities and the strict uncompressed gain are consistent with the separately counted mechanical experiment. |
| 10.2 / 34 | `cor:threshold`; `09_common_risk.tex:183–243` | At zero amplitude, equal-sign means admit an optimal nonsplitting partition; finite strict separation from splitting competitors and continuity yield the small-amplitude M≤3 threshold. Four states recover the strict gain. The zero-memory and small-amplitude limits are not conflated. |

## E. Unnumbered material and boundaries

The counted mechanical setup at `09_common_risk.tex:7–77` includes insertion failures, the at-most-one-collision regime, the collision Jacobian, positive report probabilities and the stated coefficient determinant. It is not silently substituted for the comparator-thinned experiment used by the rank and streaming results. The direct derivation was checked; this review does not re-audit every larger historical mechanical construction.

The zero-forecast estimate and the dependence of constants on horizon, margin and prior at `06_streaming.tex:261–287` are material limitations, not contradictions. The final scope section maintains the distinction between the present observable future-only task and arbitrary hidden-parameter terminal losses. No theorem about the latter is inferred.

The nine additions to the previous result inventory consist of the eight Section 7 labels and Corollary 9.3. They are components and consequences of one principal extension, not nine independent claims of top-journal depth. The report's negative editorial recommendation is compatible with every technical disposition above.
