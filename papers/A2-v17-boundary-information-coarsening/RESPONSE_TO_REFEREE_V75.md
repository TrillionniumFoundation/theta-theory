# Response to the referee on A2, revision 74

**Manuscript:** *Boundary laws and smooth contact rigidity of periodic dispersing billiards*  
**Author:** Qian Qi  
**Revision:** 75, September 17, 2026  
**Report answered:** `reviews/a2-v74-independent-harsh-top4-2026-09-17/REFEREE_REPORT.md`, commit `1ad828fd3cec7d39881fa4bb31d14423c4fd35da`.  
**Source compared:** `c52fa361108a0f716d9e89017cd97eea71b0f3da`, manuscript tree `48787e35d236d4a896abe328d78eff0ef154fdee`.

We thank the referee for distinguishing the examination of the mathematical arguments from the judgment of their significance. The report does not identify a new fatal error in the moment reconstruction or its principal smooth and physical dependencies. We therefore do not present this revision as a solution of an additional theorem gap. Its principal change is a reconstruction of the article around the two analytic steps on which its significance rests. The conditioning calculation suggested in the report and the definite navigation correction are incorporated separately.

The intended journal article is now `rigidity.tex`. It has one introductory principal theorem: the relatively normalized physical law and the actual smooth contact inverse, including finite-smoothness stability. The complete technical manuscript remains `main.tex`; it includes all previous proof modules, as well as the previously principal-only alternating-channel statement and graph-support lemma. The two-collision entry remains `two_collision.tex`. No original manuscript path has been deleted. All seven changed originals have exact archived copies; the other inherited files are unchanged. The preservation manifest covers all 992 frozen baseline files. The active label audit retains all 1,423 labels previously reachable from the three entries. These are structural checks, not mathematical proof certificates.

## R74-E1 and R74-P3: the principal mechanism and its significance

**Action:** replace the accumulated principal introduction by `article/00r_principal_introduction_v75.tex` and its single abstract. The opening now states the problem before the refinements: can an exponentially rare endpoint law determine a reflecting arc as a smooth function, rather than determine only its Taylor coefficients? Theorem `thm:v75-main` states the complete central conclusion. The first part of the article contains every proof used in that theorem.

The claimed analytic contribution is the following combination, not the algebraic extraction performed after it.

First, the observation comes from an actual finite-time Liouville experiment whose phase volume decays exponentially with the returning flight number. The comparison therefore has to be relative before conditioning. The periodic Jacobi cofactor formula gives the exact reference twist, and two-ended localization controls the determinant perturbation on a collar that does not shrink with the flight number. Fixed-order derivatives survive the localization. The endpoint momenta and residual-time factor are restored in the physical phase-volume calculation. An absolute action estimate divided by a vanishing success probability is not a substitute. Section 2 contains the complete calculation, including the distinction between smooth fixed-order bounds and analytic extensions.

Second, action jets alone cannot determine smooth contacts: flat perturbations would remain invisible. The argument first identifies the positive quadratic parameters globally and then aligns finitely many signed contact jets. The stationary envelope is evaluated on actual later visits, with a one-step contraction having multiplicative constant one. On differences of order m, the later-visit contribution has norm at most `6 a^m/(1-a^m)`. Choosing a finite m makes the initial-contact multiplication dominate the tail. This is a functional argument on actual smooth graphs, not an inference from equality of Taylor series. The terminal term is controlled before passage to the half-line limit. Sections 3–5 contain these arguments, the polynomial correction needed for stability, and a realized flat contact perturbation.

These two steps are necessary in different ways. A relative law without the functional inverse would stop at an action invariant; jet inversion without the physical comparison would not identify what the given rare experiment observes. The combined result identifies complete smooth contact germs without supplied curvature, a separately calibrated local amplitude, reflection symmetry, analyticity, or prior closeness between two candidates. It includes quantitative finite-smoothness control on a fixed positive class. The class-dependent inverse order, marked polygon and locality of the target remain explicit.

The observation refinements are now a second part rather than successive principal theorems in the introduction. They answer practical mathematical questions about the same invariant: whether one offset may be unreported, what the success count adds, and which paired profiles suffice in the limiting law. The exact low-rank cancellation is attributed as classical. The statistical results remain sufficient upper bounds, not a new general optimality principle. This changes the hierarchy without weakening any theorem.

We offer this sharper mechanism and its full proofs as the basis for reconsideration. We do not claim that revising the exposition obliges a positive editorial decision, or that a successful build answers the significance objection.

## R74-E2: comparison with the literature

**Action:** the new introduction contains one delimited comparison, rather than repeating different versions throughout the principal article.

The corrected planar Noakes–Stoyanov theorem concerns global determination of finite unions of strictly convex obstacles from exterior travel-time or scattering-length data. It is not described as an analytic-only result. De Simoi–Kaloshin–Leguil concern marked lengths for analytic open billiards with additional assumptions; Finamore–Leguil concern an enriched marked length spectrum for finite-horizon Sinai billiards. Our experiment supplies a marked internal periodic polygon and tangent frames, and observes conditional endpoint laws. Its smooth conclusion concerns the visited germs. We make no same-data dominance or whole-boundary smooth-rigidity claim.

The locality and equal-area completion argument is kept in the principal article because it establishes the precise spatial scope of the invariant by constructing actual tables. It is not used to dismiss the inverse problem. The flat contact perturbation has the complementary role: it exhibits information present in the full local law but absent from every contact/action Taylor jet. The primary-source comparison was checked against the cited manuscripts; it is targeted and is not an exhaustive priority certification.

## R74-E3: the architecture of the principal article

**Action:** replace historical accumulation by the following proof dependency structure.

| Principal component | Necessary role |
|---|---|
| Introduction and one principal theorem | State the experiment, hypotheses, conclusion and two analytic steps without a stack of nested headlines. |
| Relative boundary law | Derive the differentiated physical law at its exponentially small scale, including exact normalization. |
| Measured coordinates and stationary envelope | Relate the observations to actual graphs and provide signed jet inversion and the envelope identity. |
| Positive quadratic inverse | Obtain global curvature identification, rather than infer injectivity from a nonsingular derivative. |
| Smooth contact inverse | Control actual flat differences and obtain finite-smoothness stability. |
| Locality and completions | Prove the exact spatial scope and preserve the converse direction on actual tables. |
| Single law; complete record; moments | Develop observation refinements of the same invariant with their proofs and retained finite-flight defects. |
| Two-offset finite-preparation appendix | Give the common sampling foundation and preserve the route through normal-incidence phases. |

Only the exact core prefixes of the periodic contact and positive-curvature modules are used in the principal article. Their original unsplit files remain unchanged and active in the full technical manuscript. The analytic Banach inverse, global analytic continuation, finite stopping, alternating channels, intrinsic multichannel observations, lattice/registration, calibration and coarsening arguments remain in that full entry. They are not prerequisites of the central smooth theorem. Six explicit `F` references in the principal entry identify extensions or comparisons; `DEPENDENCY_MAP_V75.json` records their roles.

The old principal-only local mechanism theorem and graph-support lemma are not merely archived. They are inserted into the active full manuscript. The complete technical entry is therefore not replaced by an abridgment. The smaller principal entry and full entry have deliberately different purposes, not different versions of the central theorem. Source-matched native products are delivered together for review.

## R74-P1: omitted moment section in the organization paragraph

**Action:** corrected both routes. The retained full introduction `article/00i_main_thesis_v70.tex` now explicitly names moment reconstruction, the finite-flight rank defect, the charged one-dimensional derivative estimate and its budget balance. The new principal introduction contains the same route in its current section hierarchy. Cross-references use labels rather than obsolete page or section numbers.

## R74-P2: explicit gate-conditioning calculation

**Action:** added the proved remark `rem:v75-conditioning` in `article/10j_conditioning_example_v75.tex`, included immediately after geometric nondegeneracy in the moment section and linked from both introductions.

For `f(u,v)=(d+pu-pv)/(4 R^2 d)` on `[-R,R]^2`, with `d>2|p|R` and nonzero p, direct integration gives

`H = [[1,-pR^2/(3d)],[pR^2/(3d),0]]`,

`det H = p^2 R^4/(9 d^2)`.

The inverse matrix is also displayed, so the deterioration is visible without interpreting a determinant alone. We attribute the calculation to the memorandum. It is explicitly an algebraic rank-two model, not an asserted positive-curvature billiard realization. Coordinate rescaling changes moment units and does not remove physical class dependence.

## R74-M1–M7: preservation of the examined statements and qualifications

| Comment | Disposition in revision 75 |
|---|---|
| M1, exact reconstruction | The full nonsymmetric factorization and derivative estimate are retained. The introduction calls the cancellation classical; it is not advertised as a new rigidity mechanism. |
| M2, nondegeneracy | The fixed positive oblique class and full gate are unchanged. The affine example supplements, rather than replaces, the signed covariance proof. No normal-incidence uniformity is inferred. |
| M3, finite-rank defect | The actual finite record is compared with its rank-two limit before reconstruction. The exponential defect remains. Paired weights, full-gate normalization, and the distinction from exact finite sufficiency are stated in the opening and proof. |
| M4, geometric/area interface | Curvatures are recovered before profile comparison. The exact central area formula uses the actual finite fitted density and the same success gate. The logarithmic twist factor `1+N` remains. |
| M5, one-dimensional estimation | The bias, variance, Bernstein envelope, interpolation grid and deterministic post-acceptance coordinate perturbation bounds are retained in full. Exact tags and gate membership remain hypotheses. |
| M6, measurable actual-table fit | The countable dense image and near-minimum selection remain. The fit returns an actual table, but no effective enumeration or polynomial running-time claim is added. The success-count and latent mark argument is unchanged. |
| M7, budget exponents | The displayed exponents and returning-flight balance remain subject to their count, bandwidth, small-error and fixed-class conditions. Every failed preparation is charged. No lower bound or minimax assertion is introduced. |

The report's positive examination of these interfaces is not represented as certification of the separate analytic/global catalogue. Their preservation and compilation are verifiable facts; a fresh theorem-by-theorem assessment of that entire catalogue is a different task.

## Verification and proposed re-examination

The revision includes an optimization-safe checker for all 992 inherited file records, exact core slicing, preservation of the 1,423 old active labels, reference/bibliography consistency, and the affine determinant/inverse. A positive rank-three perturbation invisible to the four first-moment profiles is a negative control against overstating finite compression. Existing revision-74 and restored historical diagnostics are also run. These finite diagnostics do not replace the proofs of uniform analytic or statistical estimates.

The native build freezes the actual source commit, compiles all three entries from that frozen tree, and records imported auxiliary provenance, logs and object hashes. The delivery receipt distinguishes the source commit from later product and documentation commits. The visual inspection record identifies its coverage separately.

The next review should assess whether the single central theorem, its complete physical-to-functional proof, and the explicit role of its observation consequences now make a convincing mathematical case. We have not converted the report into a requirement to solve unknown reset measures, noisy gates, minimax lower bounds, unmarked recovery or remote smooth-boundary determination. None is a repair of the stated theorem.
