# Response to r31 — Revision 50

**Manuscript:** General Theta Foundations I: Compatible Simplices and Exact Stochastic Width.  
**Controlling report:** `reviews/general-theta-foundations-i-v49-sign-magnitude-duality-harsh-top4-r31-2026-09-27/REFEREE_REPORT.md`, commit `d9f3273b3575517cc54054a79412fe3d09378fa7`.  
**Reviewed v49 publication:** `0a33f027a9088c4a55542efcd2784de95f43f557`.  
**New work branch:** `revision/general-theta-foundations-i-v50-compatible-simplex-2026-09-27`.

We thank the referee for distinguishing the validity of the two-state theorem from the breadth and significance of its conclusions. This revision accepts that distinction. It does not answer a scope objection by repeating a successful build. It adds a higher-width geometric theorem and its consequences, connects compatibility to the inherited profiles, supplies a genuinely multi-epoch orthogonal application, and explicitly prices the finite tensor certificates. The paper retains its foundational objective and its existing mathematical content. Journal significance and independent priority remain matters for the next referee, not conclusions of the present author response.

## Main mathematical changes

### A. Higher width without an unjustified observable-state projection

`thm:simplex50` proves that, with spanning signed coordinate seeds, all coordinate queries and an identity command, a cut of width exactly the probability-Hankel rank D+1 has no hidden future-response direction. This follows from equality of row spaces and normalized binary column pairs, not from assuming arbitrary positive factorizations live in the observed space. At those cuts the labels are vertices of a full simplex. For separated rank-tight cuts, composition of the actual intervening stochastic rows gives all-word containment even when the intervening widths are arbitrarily large.

The theorem is an if-and-only-if statement for all-rank-tight profiles. It is not asserted at larger widths, where the rank-equality argument fails. This distinction is explicit in the proof and in the introduction.

`thm:occupation50` then gives a new causal obstruction, not just a normal form: if the alphabet contains I and -I, the number m of rank-tight cuts of any exact machine satisfies

    [binom(2D,D)/2^D]^(m-1) <= D! rho^(-D).

This uses the classical simplex difference-body identity at consecutive narrow cuts. Arbitrarily wider intervening registers do not evade it. In the plane it yields `cor:four50`: every signed-permutation alphabet containing I and -I has exact peak four whenever (3/2)^N > 2 rho^(-2). The upper bound is an explicit common-row four-state machine. Adding a swap and a coordinate reflection makes the alphabet noncommuting. For rho=1/10, N>=14 is a sufficient condition, not a claim that 14 is the first such horizon. At each qualifying fixed horizon, compactness gives a strictly positive stability interval in the error; no numerical value for that interval is asserted.

`thm:allhorizon50` characterizes exact rank-tight feasibility at every horizon, despite nonuniform redesign, by one invariant simplex and hence a common permutation action. The generated orthogonal group embeds faithfully in S_(D+1). In the plane at rho<=1/2 this gives the complete all-horizon three-state criterion: containment in the symmetry group of some equilateral triangle. It is a nontrivial width-three result, not a generic semialgebraic decision statement.

### B. A proved connection to distortion and enclosure

`thm:separation50` evaluates both sides of the inherited distortion--dilation comparison on the antipodal alphabet. Every one-direction packet profile and its rate vanish for k>=2, but the D+1-vertex enclosure dilation is exactly D for inradius parameter a<=1/D. The lower bound follows from the barycentric coordinates of zero; a regular simplex attains it. The rank-tight occupation charge is nevertheless positive.

This resolves a concrete sharpness question: the inherited one-sided inequality cannot be reversed or made an equality in general. It also explains why compatibility, not another choice of packet law, is needed in this regime. The arithmetic results are retained in full; they concern different alphabets where distortion and enclosure scales can match. We have not relabelled this separation as a closure of every arithmetic-width problem.

### C. A genuine orthogonal tensor application

`thm:orthogonal50` supplies rational noncommuting orthogonal commands in dimension nine, rational unit seeds, three actual command epochs and one explicitly designated coordinate query. Its eight positive-seed means are (200 rho/357) times the cubic tensor. The exact two-state binary-TV optimum is (100 rho/357)t, with t the isolated real root of 500t^3-375t^2+540t-124.

The five-entry circuit proves the lower bound against every legal two-state machine; a slope-row compiler attains it. For every separate matricization of the three-mode positive-seed tensor we display a bounded rank-one matrix of mean error 1/5 before scaling, strictly below t>0.26. Consequently no collection of separate flattening bounds proves this optimum. Compatibility across the command modes is essential.

The example has only its stated query, not all nine coordinate queries. Its three epochs, ambient dimension, exact rational input, and noncommutativity are explicit. `prop:embedding50` generalizes the word-table encoding but charges its exponential dimension. It is not advertised as an efficient succinct-input algorithm.

### D. Certificate output size and antecedents

`prop:complexity50` gives sign-assignment, extreme-ray, primitive-multiplier, boundary-degree, coefficient-height and algebraic-witness bounds for the explicitly listed rational tensor problem. Sparse certificates remain per chamber. The factor count is threshold-dependent. The shared radical representation and an exact verification route are stated; exponential degrees and fully expanded arithmetic costs are not suppressed.

Section `sec:complexity50` directly compares the exponent matrix, lattice/circuit relations, real sign structure and zero slices with Kahle--Kubjas--Kummer--Rosen. The classical ingredients are credited. The novelty table distinguishes their role from the added controlled-realization conclusions. The simplex volume identity is also explicitly classical; its iterated causal application is the occupation argument.

## Responses to the numbered major requests

| Report item | Response and manuscript location |
|---|---|
| 9.1, split the paper | We have reorganized around compatibility rather than removed the arithmetic or finite-bit results. The new profile-separation theorem supplies the missing mathematical connection. All v49 theorem/proof content remains in the integrated article. Large cumulative archives and redundant historical introductions remain at their original paths and are excluded from the compact referee package. |
| 9.2, tensor/toric literature | Direct comparison in `sec:complexity50`, bibliography entry `KKKR17`, and `LITERATURE_AUDIT.md`; no novelty assigned to Segre circuits themselves. |
| 9.3, precise novelty | The new introduction states the rank-tight regime and its higher-width consequences. The comparison table identifies the closest antecedent, shared mechanism and precise addition for each principal claim. The complete sign--magnitude alternative is always scoped to explicitly listed antisymmetric all-two-state tables. |
| 9.4, extend beyond two states | `thm:simplex50`, `thm:occupation50`, `cor:four50`, `thm:allhorizon50`, and the planar all-horizon criterion. The profile separation answers a second route in the referee's list. No assertion of unrestricted higher-width duality is made. |
| 9.5, higher-order orthogonal application | `thm:orthogonal50`, with an exact strict gap from every separate matrix flattening; rational nine-dimensional noncommuting commands and three actual epochs. |
| 9.6, output complexity | `prop:complexity50` and its proof: <=2^(v-r2) assignments; <=sum_{s<=v+1} binom(m,s) rays; primitive multipliers <=v!; polynomial degree <=(v+1)!; coefficient-height and radical-field bounds; exact witness-verification description. |
| 9.7, software versus theorem | The implementation paragraph, `PROOF_STATUS.json`, build receipt and checker docstrings separate analytic universal claims from executed finite regressions. The generic symbolic algebraic optimizer is not implemented. There is no generic higher-width optimizer. |
| 9.8, title and pipeline | The title now names compatible simplices and exact stochastic width. The series prefix and objective are retained. `HISTORY_AUDIT.md` and `PIPELINE_STATUS.json` distinguish the new local dependency graph from the independent analytic pipeline. |

## Responses to the thirty local comments

| Item | Action |
|---|---|
| 1 | `thm:main49` now defines v=|V_delta| at the tested threshold. |
| 2 | The same theorem and `sec:complexity50` explicitly say sparsity is per rejected chamber. |
| 3 | The support definition displays 0<a_v<=1. |
| 4 | The chamber paragraph explicitly retains surviving inactive entries. |
| 5 | Positive upper endpoint is defined as U_e>0 before the rejection rule. |
| 6 | The incidence vector is renamed nu_e; b_i remains a right-hand-side base. |
| 7 | `prop:complexity50` states that Farkas first supplies a nonzero witness before normalization to a nonempty polytope. |
| 8 | The dual cone's pointedness and the minimal-support extreme-ray argument are explicit. |
| 9 | Effective algebraic input specifies a common primitive element, isolating interval and coefficient coordinates. |
| 10 | Positive real branches are specified in the optimizer and both cubic constructions. |
| 11 | `prop:tight49` now refers to the feasible set in the fixed chamber/stratum, all tests and U_e>0, with endpoints checked separately. |
| 12 | The five circuit entries are displayed next to the old identity and in the new orthogonal proof. |
| 13 | A separate display proves D^2=AC and 4/25<AC<1/4 using rational bounds. |
| 14 | The scaled cubic lower inequality is displayed explicitly. |
| 15 | All-rational means every initialization, transition and decoder coefficient is rational. |
| 16 | Primitivity is retained explicitly in the old proof and stated before the modular argument in the new proof. |
| 17 | The old orthogonal proof names query j=1 and macro-words 0^(t-s), 10^(t-s-1). |
| 18 | The old identity/swap example is explicitly commuting; noncommutativity is provided by the new examples. |
| 19 | The NP-completeness statement repeats the TV/mean factor of two. |
| 20 | The NP-membership proof adds the determinant bit bound, pointedness justification and Schrijver Chapter 10 reference. |
| 21 | Tensor-completion references appear both in the bibliography and literature audit. |
| 22 | The dyadic assertion remains existence below every prescribed larger tolerance, not attainment of arbitrary error values. |
| 23 | `dual_certificate.py --help` exposes both --max-rows and --max-sign-variables. The build executes a zero-sign-limit case and requires exit 2 with feasibility undetermined. |
| 24 | The prior 677/1230-page archives remain untouched outside the compact package. Their preservation is not an assignment to the referee to read them. |
| 25 | Redundant v47/earlier historical introductions stay in old paths, not the current submission. The v49 current theorem summary is retained and retitled within the integrated proof organization. |
| 26 | The arbitrary-table cubic, old commuting orthogonal example and new three-epoch orthogonal example are distinguished in the introduction and proofs. |
| 27 | Gillis--Shitov hardness remains explicitly imported, not a new complexity theorem. |
| 28 | Moment convergence remains inherited candidate verification, not part of the new duality contribution. |
| 29 | No signing credential is available or presumed. This release uses ordinary source-bound Git commits and content hashes, not a falsely claimed signed tag. |
| 30 | A2/B4/C2 and eleven-paper aggregate flags remain false: not established by this revision, not abandoned targets. |

## Preservation, validation and remaining scope

`PRESERVATION_MANIFEST.json` binds every copied v49 source to its original SHA-256 and lists every edited copy. `EXPECTED_V49.json` fixes the original loaded theorem/equation labels. The build rejects a missing original label, altered copied source, normal/optimized disagreement, undefined reference, overfull box, malformed bookmark, CLI resource-limit misclassification, or isolated-core text/raster mismatch. The four finite checker suites run under both ordinary and optimized Python. These are useful regression and publication checks, not an independent referee's proof verification.

All old branches, reviews and manuscript paths are unchanged. The rank-tight higher-width theorem does not solve arbitrary width, the finite table algorithm is not polynomial in a succinct horizon, exact algebraic row sampling is not a uniform finite-bit cost theorem, and the positive error interval in the four-state corollary is qualitative. These are explicit boundaries of the proved statements, not a reduction of the mathematical objectives. The next review can now assess the added geometric theorems and their applications rather than an unchanged two-state claim.
