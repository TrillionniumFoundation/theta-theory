# Referee Report

**Manuscript:** *A Conditional Theory of \(\theta\)-Expectations from Deterministic Billiards*  
**Source reviewed:** `main.tex`  
**Repository state reviewed:** `main` at commit `08aac05e51577bcd2f2ec5a6aef2a960a8d3ef9d`  
**Standard applied:** Annals of Mathematics / Inventiones Mathematicae / Journal of the AMS / Acta Mathematica  
**Recommendation:** **Reject without an invitation to resubmit in the present form**

## 1. Summary and overall assessment

The manuscript proposes a long conditional chain

\[
\text{dispersing billiard geometry}
\Longrightarrow
\text{spectral/response package}
\Longrightarrow
\text{deterministic HJB homogenization}
\Longrightarrow
\theta\text{-expectation and representations}.
\]

The current version is considerably more honest than a manuscript claiming that this entire chain follows from finite-horizon dispersing geometry alone. The abstract and introductory “conditional standard” explicitly state that five analytic properties are assumed rather than proved. That clarification is important.

It is also fatal to the paper's claim to be a first-principles construction from deterministic billiards. The assumptions labelled (A1)–(A5) contain essentially every hard theorem needed for the advertised conclusion: the anisotropic spectral package, suspension/non-lattice estimates, moving-boundary response, a mechanically coherent prelimit equation, and the compactness/contact/residual/comparison closure needed for homogenization. Once these are assumed, the remaining argument is principally a formal organization of standard corrector, Green–Kubo, viscosity, linearization, Feynman–Kac, BSDE, and Girsanov ideas.

At the level of the four journals named above, a conditional synthesis can be publishable only if the abstract implication itself is a deep, sharply formulated theorem that is not already encoded in its hypotheses, or if the paper verifies the hypotheses in a genuinely new and important class. This manuscript does neither. No concrete billiard/port family is shown to satisfy the complete admissibility package. In particular, the manuscript does not establish the moving-singularity and homogenization bridges on which the title and motivation depend.

## 2. Principal mathematical objections

### 2.1 The main result is an assumption-to-conclusion ledger, not a billiard theorem

The manuscript itself states that the result is “an assumption-to-conclusion reduction” and that it does not derive (A1)–(A5) from ordinary dispersing geometry. That is the accurate mathematical status.

The difficulty is not merely that some technical hypotheses are left to future work. The hypotheses cover the central content:

1. a spectral gap and reduced resolvent on suitable anisotropic spaces;
2. a suspension resolvent/non-lattice package;
3. differentiability under moving singularities, including the trace terms required by the coefficient calculus;
4. existence and coherence of the singularly scaled prelimit Hamilton–Jacobi problem;
5. exactly the compactness, admissible contact selection, residual convergence, and comparison closure needed to identify the HJB limit.

Assumption (A5), as described throughout the paper, is particularly close to the desired homogenization conclusion. A theorem of the form “if the perturbed-test residual vanishes, contacts are admissible, compactness holds, and comparison holds, then the relaxed limits converge to the unique viscosity solution” is a standard viscosity closure scheme. It is not a derivation of those properties from billiard dynamics.

The paper therefore cannot be advertised as constructing nonlinear expectation from deterministic billiards. It constructs a conditional PDE semigroup from a list of hypotheses, some of which are named after billiard objects.

### 2.2 No model verifies the full package

A top-level existence theorem must exhibit at least one nontrivial instance satisfying every hypothesis. The manuscript does not do so.

The response paper in the same repository gives only source-specific collision-map results in a radial deformation through order two, together with exact-coboundary benchmarks and conditional higher-order statements. It explicitly does not prove a moving-family continuous-time graph-domain theorem or the complete reinsertion estimates required by the monograph. The CM2 bridge note is also explicitly conditional and leaves multiple global gates open. Thus the repository as a whole does not currently supply an example covered by the monograph's principal theorem.

A theorem with an empty or unverified hypothesis class cannot carry the conceptual conclusions claimed here.

### 2.3 The prelimit problem is not established as a well-posed global object

The manuscript repeatedly invokes a mechanically generated “prelimit viscosity-duality solution.” A rigorous theorem would need, at minimum:

- a precise state space and domain for the fast generator with reflections and singular collision sets;
- a definition of viscosity solution compatible with the anisotropic distributional pairing;
- existence, stability, and comparison for the prelimit equation;
- compatibility of the cotangent feedback with the moving billiard fiber;
- a proof that branchwise action identities glue across reflections and singularity refinements in the required topology.

These are not routine bookkeeping details. They are part of the central construction. Stating them inside (A4)–(A5) does not prove them.

### 2.4 The contact argument cannot be justified by a zero-measure observation

Several versions of the argument say that maximizing/contact triples may be chosen away from singular strata because those strata have zero Liouville flux measure. A viscosity maximum is a pointwise object; a set of measure zero can contain every maximizer of a sequence. Measure zero alone gives no admissible-contact selection theorem.

To make this step valid one needs a genuine approximation or penalization result showing that the relevant test inequality can be transferred to regular branches, with quantitative control of the singular boundary contribution. This is one of the hard closure statements currently assumed. It cannot be replaced by “the singular set has zero measure.”

### 2.5 The effective coefficients are not obtained by a complete displayed calculation

The manuscript repeatedly refers to the “complete covariant work observable,” “horizontal covariant work response,” and “full-gradient corrector calculus,” but the principal theorem does not present a self-contained formula from primitive mechanical data to \(D\) and \(H\) with every term typed and every cancellation proved.

The affine-in-\(X\) form
\[
\operatorname{Tr}(D(x,p)X)+H(x,p)
\]
is natural for a diffusion-type limit. It is not, by itself, a deep rigidity theorem. The nontrivial issue is proving that the deterministic prelimit has precisely this limit and that no singular or memory term survives. That issue has been moved into the assumptions.

### 2.6 Positivity of the Green–Kubo tensor requires a precise theorem

The manuscript says that \(D\) is positive semidefinite because it is the limit of deterministic square time integrals. This can be correct after one identifies \(D\) as the asymptotic covariance of an additive functional and proves existence of that limit. But the displayed one-sided correlation integral and the claimed square-integral representation require a careful symmetrization and a weak invariance principle/coboundary argument. Those are not consequences of Liouville invariance alone.

The paper should not slide between a formal Green–Kubo integral, an asymptotic variance, and a positive semidefinite diffusion tensor without proving their equality in the actual observable class.

### 2.7 The nonconvexity example is designed into the port

The proposed finite-response port permits one to prescribe negative quadratic and positive quartic terms in an action read-out and then dominate the response remainder. This shows that a sufficiently flexible constitutive input can manufacture a nonconvex effective Hamiltonian. It does not show that nonconvexity is an emergent theorem of dispersing billiards.

The distinction matters because the manuscript repeatedly presents nonconvexity as a structural output of deterministic chaos. In the construction given, it is chiefly an input through the chosen read-out. At most, the billiard contributes response corrections that must be bounded so the prescribed sign survives.

### 2.8 “\(\theta\)-expectation” is presently a renaming of a nonlinear PDE semigroup

Once comparison holds for the HJB equation, monotonicity, constant preservation, and dynamic consistency of its solution semigroup are standard. Calling this semigroup a new expectation does not create a new mathematical structure.

A new theory would require substantial results specific to the proposed class: a characterization theorem, a representation theorem not reducible to payoff-dependent linearization, a canonical independence notion, a convergence theorem from a verified microscopic model, or a genuinely new calculus. The manuscript currently provides none at the required level.

### 2.9 The downstream representation material is standard and dilutes the paper

The linearity obstruction, payoff-dependent linearization, calibrated diffusion, decoupled BSDE, and Hamiltonian-shift algebra are classical once a smooth HJB solution is fixed. Their inclusion makes the monograph much longer but does not strengthen the missing billiard-to-HJB bridge.

The comparisons with noncommutative probability, robust pricing, and philosophical discussions of deterministic randomness are not appropriate substitutes for a central theorem. They should be removed from any research-paper version.

## 3. Relation to existing work

The established literature already provides major pieces separately:

- Demers–Zhang give spectral stability for broad perturbations of the Lorentz gas, including movements and deformations of scatterers, but continuity of spectral data is not the moving-singularity differentiability theorem assumed here.
- Baladi–Demers–Liverani prove exponential decay and a resonance picture for a fixed finite-horizon Sinai billiard flow, not the parameter-uniform moving-flow response package required here.
- Stenlund–Young–Zhang prove loss of memory for sequential moving-scatterer billiards, not the two-time differentiability and trace-resolvent theory assumed here.
- Kelly–Melbourne prove deterministic homogenization of chaotic fast–slow systems to diffusions under a precise probabilistic limit framework. A billiard HJB theorem would need to surpass this baseline by proving the new feedback/singularity mechanism, not by assuming its closure.

The manuscript does not explain a theorem-level gain over this literature once its admissibility package is unpacked.

## 4. Presentation and auditability

The manuscript is far too long and diffuse for its mathematical content. It combines:

- a conditional billiard framework;
- an HJB homogenization outline;
- a nonlinear-semigroup discussion;
- stochastic representations;
- robust-pricing language;
- philosophical comparisons;
- computational/falsification protocols;
- large technical ledgers.

This makes it difficult to identify what has actually been proved. Statements such as “complete and internally consistent proof” are inappropriate when the main analytic bridges are assumptions.

The source also contains multiple historical layers and parallel manuscripts in the same repository. A submission must have one canonical theorem list and one dependency table that distinguishes:

1. proved from primitive geometry;
2. imported from a cited theorem;
3. assumed;
4. conjectural;
5. verified only in a toy or exact-coboundary class.

## 5. What would be required for a new submission

A viable new paper would need to be fundamentally different.

One possible route is:

1. discard the monograph format;
2. select one concrete billiard/port family;
3. state a single main theorem with no homogenization or response hypothesis that is merely a restatement of the conclusion;
4. prove the moving-flow response and the exact prelimit well-posedness needed for that family;
5. give a complete residual identity and a rigorous admissible-contact lemma;
6. verify comparison and identify the limiting coefficients;
7. remove the standard BSDE/Girsanov and philosophical material.

An alternative is an abstract homogenization paper, but then the title should not claim a construction from billiards, the billiard discussion should be an unverified application program, and the abstract theorem must be stated in a clean general framework with hypotheses demonstrably weaker than its conclusion.

## 6. Recommendation

The manuscript is not close to the standard of the four journals named above. Its strongest honest statement is that it organizes a conditional research program. That may be useful internally, but it is not a publishable top-tier theorem.

**Recommendation: reject without invitation to resubmit in the present form.**
