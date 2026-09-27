# Response to Revision 57 / r38 — Revision 58

Controlling report: `5b2fb03f87a6b28bddcef51d498a0c78429bfa22`, blob `c530ec0f755d2aa9a9d23b3d99dc4675fcacc679`. Base publication: `0e07470b9693a2789af00222f063e715a83ff454`.

The revision adds complete mathematical proofs, a fixed rational input and a constructive compiler. It does not change the journal target, suppress the logarithmic gap, or delete prior results. Actual build evidence, written proofs, imported theorems and independent priority assessment are distinct.

## Main response

### R38 10.1 — Theorem-level priority comparison

The focused comparison sections and LITERATURE_AUDIT.md give a twelve-area comparison with the relevant hypotheses and output notions. Fijalkow–Paperman is cited as Theorem 10 in the original PDF; the experimental HTML renumbers it as Theorem 4.4. Its deterministic K-preserving argument is credited explicitly, so state-bound preservation alone is not claimed as a new phenomenon. Brodsky–Pippenger Theorems 3.3 and 3.6 and Lemma 3.5 are compared with the full legal-output profile, rather than treated as irrelevant merely because they concern automata. This is an author-side audit, not external priority clearance.

### R38 10.2 — Two independent articles without deleting mathematics

quantitative.tex and structural.tex are independent proof-complete articles. The former leads with the least-orbit-rank theorem and the explicit rational robust separation; the latter develops clock removal and physical finite actions. main.tex is the complete research edition and retains every active v57 label and proof, including arithmetic and profinite results. All 181 predecessor native files remain byte-identical. The older higher-dimensional transcendental endpoint is in the complete edition appendix, not a hidden dependency of the new rational theorem.

### R38 10.3 — Exact quantifier inventory

The quantitative introduction distinguishes horizon-specific rows, every conditional-centroid direction, legal matrix decoders, and exact pointwise profiles. The structural introduction distinguishes same width, same closed error, randomized initialization and arbitrary intervening widths. The proof-status inventory separates inherited structural theorems from new v58 theorems. No classical rank, semigroup, homogeneous-space or spectral-gap theorem is rebranded as an invention.

### R38 10.4 — Effectivity, decision, minimization and construction

Proposition rankcompute58 computes a rank invariant from supplied algebraic infinitesimal matrices, not a group closure or spectral gap. The new rationalcompiler58 actually constructs a realization from the fixed rational experiment, unlike the retained supplied-realization compiler. The finite-group existential-real theorem, compact-group closure procedures and general minimization remain distinct. Runtime is polynomial in N and inverse accuracy for the special compiler, not in their binary lengths; its naive triple search is not described as practical at large sizes.

### R38 10.5 — The logarithmic gap

The converse remains N/log(N+2) in the rational qubit example and (N/log(N+2))^(p*/2) generally. It is stated in the abstract, theorem and conclusion. We have not proved its necessity or removed it. The new class-wide improvement is the removal of a separate uniform-cap assumption: minimal infinitesimal orbit rank supplies its optimal uniform exponent for every fixed-point-free compact connected Lie representation.

### R38 10.6 — Explicit finite-input endpoint

Theorem rationalseparation58 displays U,V and P0 with rational real and imaginary entries. The elementary modulo-five quaternion lemma proves a free triple; squared generators give a free pair, and the third generator proves that the rational pure seed has trivial stabilizer. Thus every exact cut has 2*3^t-1 labels. The same lower profile holds at epsilon <= 625^(-N)/16. No dense-free existence theorem or transcendental seed is used for this example. The positive-error lower bound alone imports Bourgain–Gamburd for the exact displayed alphabet; its gap constant is not computed.

### R38 10.7 — Legal outputs

Both the new separation theorem and the compiler state the legal set D_2 and Frobenius norm. The matrix and tomography sections keep the affine legal image, not a full-simplex replacement. Fair bits sample hidden labels only; a numerical density-matrix decoder is not a quantum preparation. The full-output result is not marketed as a scalar cut-point language separation.

### R38 10.8 — Independent analytic pipeline

FROZEN_PIPELINE_LEDGER.md and FROZEN_PIPELINE_HISTORY.md are retained exactly. All A2 replacement, B4/C2 aggregate, eleven-paper and whole-program flags remain false. The present orbit and realization theorems neither assume nor discharge the raw local-limit, stopped LDP, global-past-kernel, Mosco/Nisio, filtering, changing-filtration response or labelled posterior gates.

## All thirty-six local comments

### R38 local 01 — Command width

The focused model immediately excludes a sampled answer register; every advertised label, including unused padding, remains counted.

### R38 local 02 — Dependencies

A single Dependence of constants remark at the end of section 16 collects the metric, representation, cap, spectral, hull and tolerance data.

### R38 local 03 — Three dimensions

The executable-gap proof now explicitly distinguishes D=dim G from the cap exponent p and target-orbit dimension q. The new theorem uses p_* for the least orbit dimension.

### R38 local 04 — Metric

The ball-average calculation repeats that the group is compact connected Lie and its Riemannian metric is fixed and bi-invariant.

### R38 local 05 — Chronological order

The existing iid reversal sentence is retained: reversing a finite list of identically distributed independent letters preserves its law.

### R38 local 06 — Integer occupation bound

The proof now displays L_k = B_k(1 + ceil(c^(-1) k^(2/p) log(1/zeta))) before asymptotic inversion.

### R38 local 07 — Smooth orbit

The shared geometric remark identifies the embedded homogeneous quotient G/G_z0 and its real dimension.

### R38 local 08 — Inradius

The hull proof names its positive inradius r0; the dependence remark specifies its role in converting additive to multiplicative support loss.

### R38 local 09 — Finite selections

The common-row proof explicitly chooses barycentric coordinates for each finite command–vertex pair independently. The new rational compiler makes these choices by exact triple enumeration.

### R38 local 10 — Norm

The uniform-orbit theorem retains Euclidean error on Q; the new class-wide corollary restates that same norm.

### R38 local 11 — Two chordal metrics

The Grassmannian statement now gives dist_pr(P,Q)=||P-Q||_F/sqrt(2) before its exact rank-one formula.

### R38 local 12 — Arbitrary cap center

The existing proof chooses a member of the nonempty target ball; the added reminder makes clear that no spectrum of the arbitrary center is used.

### R38 local 13 — Dimension constants

The matrix section and the new all-representation theorem explicitly disclaim dimension-uniform constants.

### R38 local 14 — Matrix normalization

The matrix theorem retains r_d=sqrt(1-1/d) and zeta=a-epsilon/r_d in its statement. The rational theorem fixes d=2 and displays the threshold 1/sqrt(2).

### R38 local 15 — Slack

The matrix-section reminder explicitly identifies half-error amplitude slack. The rational fair-bit proof separately budgets amplitude loss and row rounding.

### R38 local 16 — Explicit adjacent blocks

The matrix section now displays the rational adjacent-SU(2) blocks and gives the torus/Lie-bracket generation proof.

### R38 local 17 — Actual spectral alphabet

The gap theorem is applied to the displayed dense algebraic set, with laziness when an absolute L2 bound is needed. The proof never transfers a gap from an unrelated set.

### R38 local 18 — Tomography norm

The reconstruction norm on the affine span remains defined in the tomography subsection before its affine-isometry assertion.

### R38 local 19 — TV constants

The upper and lower TV/Frobenius constants remain adjacent to the reconstruction identity.

### R38 local 20 — One suffix

The independent extreme-profile text emphasizes one fixed injective suffix; the robust rational proof uses the same cut argument with separated decoder caps.

### R38 local 21 — Nonempty alphabet

The independent profile proof explicitly mentions a fixed letter in the nonempty alphabet for monotonicity.

### R38 local 22 — Older existential example

The first sentence of the older free-endpoint theorem now labels the seed transcendental and the generators existentially selected. The new rational example is logically separate.

### R38 local 23 — Two imports

The older appendix keeps dense-free existence and spectral gap separate. The new finite-input example uses neither dense-free existence nor a transcendental argument.

### R38 local 24 — Liouville appendix

The entire older higher-dimensional endpoint, including the Liouville proof, is moved to the complete edition appendix. It is not loaded by the focused rational paper.

### R38 local 25 — Algebraic encoding

The positive-precision section specifies defining polynomials, isolating intervals for real and imaginary parts, and the PSD square-root characterization.

### R38 local 26 — Bits versus time

The generic compiler discussion repeats that output bit length is not a runtime estimate. The special rational compiler gives its own explicit triple-search runtime bound.

### R38 local 27 — Fair bits

All compiler descriptions distinguish hidden-label draws from quantum-state preparation and sampled terminal measurements.

### R38 local 28 — Trivial exact bound

The inherited existential-real proof still normalizes k at or above |G||S| to an immediate yes instance before constructing a polynomial formula.

### R38 local 29 — Hardness citation

The finite-group theorem retains the exact Shitov Theorem 2 complexity citation; its statement was checked in the primary arXiv text.

### R38 local 30 — Ramsey placement

The explicit coarse Ramsey estimate and its proof now form a separate remark, with every old equation label preserved.

### R38 local 31 — Neutral decoder

The stationarization proof retains the neutral table inside the decoder; the concluding remark states that it is neither identity nor assumed idempotent.

### R38 local 32 — Row action

The physical-equivariance convention remark states right action of probability rows and explains the inverse physical coordinate.

### R38 local 33 — Coarse bound

The same remark separates seed-times-coset deterministic storage from the unrestricted stochastic minimum.

### R38 local 34 — Periods

The phase convention remark distinguishes block period p, physical quotient order q dividing p, and the exact-return gcd; no one is silently substituted for another.

### R38 local 35 — Independent proof closure

Both focused introductions state that their proofs are complete without predecessor PDFs. The complete research edition and earlier rendered manuscripts are preservation/provenance deliverables, not missing forward dependencies.

### R38 local 36 — Bibliographic roles

Every inherited bibliography item is retained and grouped by semigroup/positive realization, automata/series, compact groups/orbits, and algebraic computation/complexity.

## Validation and remaining scope

The build binds the readable native sources before qualification, runs the new and all inherited exact regressions in normal and optimized Python, compiles the focused articles and complete research edition, and independently rebuilds a native-only archive. Every old active mathematical label remains loaded in the complete edition. These controls are reproduction evidence, not a formalization of the universal cap theorem, infinite freeness, a numerical spectral-gap certificate, or journal acceptance.

The general online/adaptive observation and irreversible physical-semigroup classification problems are not solved here. The same-width structural theorem retains its eventual approximate-return hypothesis; the nonabelian converse retains its logarithm and non-effective spectral constants. The new finite-input, robust-profile, all-direction geometry and constructive upper results stand on their displayed assumptions rather than on a claim that all neighboring problems are settled.
