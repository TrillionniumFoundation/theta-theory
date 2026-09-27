# Response to Referee r34 — Revision 53

**Article:** General Theta Foundations I: Sharp Noise Thresholds for Stochastic Realizations of Compact Group Experiments.  
**Author:** Qian Qi.  
**Date:** 27 September 2026.  
**Controlling review:** `4b1eb39eacdb741354e8c4faaedb1c3aabb3a14c`, report blob `eabcb8404c98d5094f6e2d9113c67214bce75c91`.  
**Frozen predecessor publication:** `7641901c2ef957542aa50d9918f272ac7a72ca1c` (v52).

The referee found no fatal counterexample to the principal v52 arguments, but judged the breadth, quantitative depth, positioning, and presentation insufficient for the four-journal standard. This revision does not reinterpret that assessment as acceptance. It changes the mathematical center of the article: the former coordinate-interface small-error implication is subsumed by a complete component-oscillation classification for every finite continuous binary-mean interface on a compact matrix group. The previous mathematical content is retained in a separately buildable complete supplement rather than deleted or weakened.

## 1. Main mathematical change

Let H be the compact command closure, K its identity component, and C=H/K its finite component group. For finitely many continuous mean functions f(s,j) on H, define

`epsilon_c = (1/4) max_{s,j,c} [max_{h in c} f(s,j)(h) - min_{h in c} f(s,j)(h)]`.

Theorem `thm:classification53` proves, including equality, that uniformly bounded horizon-dependent clocked stochastic width is possible exactly when epsilon >= epsilon_c. At the boundary one stationary permutation machine on seed/component labels suffices. Below it, the number of cuts of any fixed width is bounded independently of the horizon, even with arbitrary intervening widths. Identity commands are executable, but their stochastic rows need not be identity matrices.

The lower proof is not an unproved appeal to Haar mixing. It contains four explicit steps: a finite executable word law on K with a representation-wide quantization defect; the conditional-centroid identity for a complete independent block; tensor-polynomial conditional calibration; and nonnegative polynomial weights concentrating near both extreme output values. For a continuous, nonpolynomial readout, Stone–Weierstrass is used with a strictly positive error margin and the reduction is written out. The proof never assumes a lower bound on hidden-state masses, a basis condition number, or full observation. It also never promotes moment estimates to total-variation convergence of conditional group distributions.

## 2. Responses to the principal requests

### Breadth and partial interfaces

**Implemented in the main theorem and Theorem `thm:observable53`.** Seeds and queries need not span, and readouts may be nonlinear continuous functions. For linear readouts, the zero-error criterion is finiteness of the action on the reachable space modulo its invisible subspace. The proof explicitly uses normality of K to check all future queries. A fixed-axis example gives an infinite ambient group with an exactly realizable constant interface, contrasted with a visible-plane interface for the same group.

The article additionally treats measure-once unitary probability functions by realification and uniformly bounded groups in GL(D,R) by an invariant inner product. The latter assumes boundedness of the whole group including inverses, not merely of a positive semigroup. A two-state absorbing stochastic realization of a contracting scalar semigroup explains that distinction. No unproved generalization to arbitrary nonorthogonal semigroups is used.

### Sharp positive error

**Implemented with matching upper and lower bounds.** Corollary `cor:circle53` gives exactly epsilon_c=rho/2 for an irrational planar rotation, with or without additional planar orthogonal commands. One fair-output command label attains the boundary. This closes the entire interval that was previously left between the small-error obstruction and the trivial fair decoder for this family. Proposition `prop:torus53` gives an exact sum-of-amplitudes formula when the actual connected closure has independent toral coordinates; proper subtori are explicitly excluded from that simplified formula and remain covered by the general extrema formula.

The factor one quarter is derived from binary mean/TV conversion and the Chebyshev midpoint error, and is tested at equality. It is not an adjusted sufficient constant.

### Stronger quantitative content

**Implemented for the entire subcritical algebraic-circle interval.** Theorem `thm:algebraic53` gives an explicit finite-horizon and occupation inequality, using polynomial localization degree r with r > 2 epsilon/(rho-2 epsilon). A nonzero integer resultant gives a uniform lower bound on every required algebraic power separation. This yields a logarithmic width lower bound for every epsilon<rho/2, not only for the former coordinate-calibration range. The rational Gaussian-integer argument is retained as the sharper special case. An explicit nonrational degree-four unit-circle example has height constant B=8 and a complete irreducibility/non-torsion proof.

The example rho=1/10, epsilon=1/25 uses r=5, Delta=1/150, and A=23364. These values are checked with exact rational arithmetic. The new bound extends the covered error interval and the input class; it does not claim better constants than every inherited low-noise estimate or a sharp width growth rate. The conclusion states one primary remaining quantitative problem, a matching growth law for a fixed algebraic irrational rotation.

For arbitrary real compact matrix data, the general finite word net remains non-effective. No numerical word-length estimate for every such group is inferred from compactness.

### The one-surplus and six-state calculations

**All previous results retained; local quantitative exposition improved.** The companion notes supply the support-function identity, explicitly handle conjugate nonreal stochastic eigenvalues, and include the oblique support-cone diagram and its volume computation. They separate the exact coefficient pi/(1296 sqrt(3)) from the weakened rational 1/1024, and reproduce the finite rational verification of the sufficient horizon 9,216,009.

The unconditional algebraic noise search at that large illustrative horizon has not been executed, and no numerical noise interval is represented as computed. The revision takes the referee's requested substantive-extension route through a complete noise boundary and explicit algebraic-circle inequalities, rather than relabeling a generic elimination procedure as a practical six-state calculation. The earlier six-state theorems remain available without reduction of their statements.

### Reachable-basis conditioning

**Strengthened in Proposition `note:conditioning53`.** The companion notes define A_min as the minimum over the finite set of actual reachable bases, prove attainment, give an exact finite LP computation for supplied algebraic rows, and establish A(B)<=sqrt(r)/sigma_min(B). A two-row example shows why no horizon-uniform bound follows from dimension alone. Every supplied-basis theorem also applies to this intrinsic minimum by choosing a minimizing basis at each selected cut. The new main classification has no conditioning hypothesis at all.

### Classical certificates and resource interpretation

**Separated, credited, and preserved.** Generic projector, Farkas, Putinar, and Lasserre material is in the complete supplement. The notes identify the unweighted SOS multiplier, redundant symmetry counts, and the cost of principal-minor verification. The existing certificate verifier is rerun, but no general certificate-discovery engine is claimed.

The main article places the nonuniform resource table immediately after the model. Clock, horizon, arbitrary real row descriptions, arithmetic, lookup, and exact real sampling are free in the lower bound. The stationary component construction is a mathematical finite-real-table construction, not an effective finite-bit compiler for arbitrary continuous input. The separate rational finite-group compiler and its exact-sampling cost remain in the supplement, with reduced-rational equality and probability-bit versus orbit-height distinctions made explicit.

### Positioning against the closest automata literature

**Rewritten at theorem level.** The article compares fixed group/reversible automata, positive realization, Brodsky–Pippenger, and Blondel–Jeandel–Koiran–Portier with the current model. In particular, Brodsky–Pippenger Theorem 3.6 concerns acceptance of the same cutpoint language with a possibly different cutpoint. It does not assert uniform additive preservation of every numerical probability. Their Theorem 3.3 is explicitly credited for the bounded-error measure-once/group-language characterization. The present occupation and threshold claims are not described as corollaries of those language results.

The comparison states the different uniformity, advice, numerical specification, error, and conclusion. Classical compact closure, Haar, polynomial approximation, and resultant arguments are not presented as newly invented mathematics. This is a targeted primary-source comparison, not exhaustive priority certification.

### Article architecture and preservation

**Implemented as a focused, independently complete article plus a complete supplement and companion notes.** The main article states one classification problem, proves it without forward dependence on an omitted appendix, derives observable and nonlinear consequences, and gives the explicit arithmetic theorem. It is not a page-selection excerpt from a longer document. The complete v52 source set (59 files in its validated source manifest) is copied byte-for-byte under `retained-v52/`; all 33 active inputs and 242 loaded labels are preserved and recompiled. Their original repository paths and all older branches remain unchanged. Publication records actual counts rather than treating planned preservation as verified.

## 3. All thirty local comments

| r34 comment | Resolution and exact location |
|---|---|
| 1. Projection commutation | `note:fixed53` proves P_E h=h P_E and identifies the finite-orbit space with the K-fixed space. |
| 2. Positive-word semigroup | `lem:positive53` defines it explicitly and proves density without executable inverses. |
| 3. Strict net radius | `lem:gap53` chooses eta<g/2 as a separate quantity. |
| 4. Dimension of the moving space | Main Section 2 and companion Section 1 distinguish representation dimension and rule out a nontrivial one-dimensional connected moving representation. |
| 5. Vector decoders versus joint queries | Model and companion Section 1 explicitly treat queries as selectable alternatives; polynomial weighting also adds no query. |
| 6. Occupation endpoints | `eq:occupation53` and `eq:Lk53` count cuts 1 through N and separately account for the fixed prefix. |
| 7. Dependence of B,d,chi | `lem:gap53`, `eq:constants53`, and the effectivity remark list their dependencies. |
| 8. Action-dependent versus universal error | Companion Section 1 records rho s_*/(2 sqrt(D)) and the weaker universal interval separately; the new critical formula supersedes both when applicable. |
| 9. Rational denominator | `thm:algebraic53` assumes c>0 and explains why a nonminimal denominator only weakens the valid bound. |
| 10. Asymptotic constants | Proof of `eq:algrate53` states dependence on algebraic input, rho, and epsilon, not N. |
| 11. Open/closed caps | `lem:separated53` uses open balls at the separating radius and explicitly states the boundary conclusion. |
| 12. Complex eigenvalues | `note:trace53` counts conjugate pairs and bounds real parts of the remaining eigenvalues. |
| 13. Support formula | `note:support53` proves the maximum support-ratio identity. |
| 14. Cone picture | Companion Section 2 includes a schematic oblique cone, its support plane, radius, and perpendicular height. |
| 15. Exact versus weakened beta coefficient | Companion Section 2 separates the omega formula, pi/(1296 sqrt(3)), and 1/1024. |
| 16. Rational horizon arithmetic | Companion subsection 'Exact verification of the illustrative horizon'; inherited exact checker rerun. |
| 17. Intrinsic conditioning | `note:Amin53` and `note:conditioning53`, including exact computation and a divergent two-row example. |
| 18. Whole-suffix error | Companion Section 3 makes the one-time complete-suffix estimate explicit, without epochwise accumulation. |
| 19. Mean versus TV | Model, `eq:critical53`, and the lower proof use delta_0=2 epsilon; exact boundary regressions reject the wrong budget. |
| 20. Unexecuted noisy search | Companion Section 2 and this response explicitly distinguish proved termination from an executed numerical search. |
| 21. Repeated symmetry equations | Companion Section 4 explains deliberate redundant scalar counts. |
| 22. Free SOS term | Companion Section 4 defines sigma_{-1} as the unweighted SOS term. |
| 23. PSD certificate size | Companion Section 4 notes exponential principal-minor count and that an LDL replacement is not implemented. |
| 24. Generic SOS placement | Entirely in the complete supplement and its notes; absent from the main theorem's proof dependencies. |
| 25. Probability bit length | Companion Section 4 distinguishes terminal probability encoding from orbit-coordinate heights. |
| 26. Rational duplicate testing | Companion Section 4 specifies reduced rationals and exact equality in finite-orbit BFS. |
| 27. Resource table location | Main Section 1, immediately following the machine definition. |
| 28. Genuine focused article | New `main.tex` is independently complete; the earlier full article is a separate complete supplement, not a prerequisite hidden behind an excerpt. |
| 29. Published classical references | Main bibliography includes published automata/positive-realization sources and standard books; the literature audit identifies checked primary statements. |
| 30. One primary quantitative question | Main Section 8 states a matching width-growth problem for a fixed algebraic irrational rotation. |

## 4. Dependency and proof status

The new proof chain is self-contained within finite-dimensional compact-group realization. The historical chain from common-row compatibility and reachable sections through finite-orbit reduction and endpoint contraction is recorded in `HISTORY_AND_PIPELINE_AUDIT.md`. The repository Round-Seventeen analytic DAG is copied as a frozen reference and is not used as an unproved premise. In particular, this finite-state result is not assigned closure credit for raw density local limits, stopped LDP, global past kernels, process CLT/Mosco, nonlinear resolvents, QMD/LAN, strict/form response, or labelled posterior contraction.

The written proofs and their claimed scope are listed in `PROOF_STATUS.json`. Exact regression, PDF compilation, label preservation, source hashes, and isolated text/raster reproducibility are build evidence, not independent formal verification or assurance of a journal's editorial judgment. The native source is committed before qualification; the referee-ready branch is published only after the workflow has actually passed.
