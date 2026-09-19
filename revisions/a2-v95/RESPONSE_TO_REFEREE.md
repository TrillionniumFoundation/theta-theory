# Response to the referee on A2 revision 94

## Source pin and scope

This revision responds to `reviews/a2-v94-independent-harsh-top4-2026-09-19/REFEREE_REPORT.md` at commit `dbbad2d84c6a3b358bddabf84dc16f0b09b38634`. The reviewed manuscript head is `5e01e5a2d6e93ef4c1e2619707608626fdc0f6cf`. The revision is based on the review commit, so the controlling report and its manuscript remain in the ancestry without alteration.

The new complete entrypoint is `papers/A2-v17-boundary-information-coarsening/rigidity_v95.tex`. The title is *Projective polynomial observations: real valuations and identifiable singularities*. The principal additions are in `article/v95/finite_newton.tex`, `cubic_geometry.tex`, and `cubic_leading.tex`. All 25 mathematical and bibliography input modules of the reviewed manuscript remain active, byte-for-byte unchanged; the normalization theorem formerly inside its main file is retained verbatim in `article/v95/global_statements.tex`. The old entrypoints also remain unchanged.

The report accepted the substantive repairs concerning nonlinear admissible germs, metric transport, and the whole-model cubic fibre. We retain those arguments. This revision addresses the new theorem-strength objections by pursuing the report's Options A, B, and C together. It does not substitute a venue change, a negative conclusion, or an unproved generality claim for those additions.

## 1. Finite singular-germ data, rather than optimized envelopes

**Report sections 4, 10, 13, and Option A.** The new Theorem “Finite real-valuative Newton formula” takes a defining formula for the actual observation--spectral graph as its input. On a compact real lift it forms the polynomial functions

- G: the squared weighted Hellinger distance;
- H(r,a): the squared modulus of each cluster coefficient.

A real uniformization and simultaneous normal-crossing construction produce finitely many integer orders a(i), b(r,a,i). The coefficient order is the minimum of b/a over accessible real divisors, and the spectral order is the minimum of b/[a(m(r)-a)] over the cluster weights. These integers are produced before any observation-ball maximum is constructed. The proof supplies both the monomial inequality and an admissible transversal attaining the minimum.

The real-locus qualification is essential. We do not use complex exceptional divisors without checking that they contain accessible real points. For algebraic input the construction is described through basic closed pieces, bounded square-slack lifts, resolution, recursion on uncovered lower-dimensional singular loci, and real feasibility tests. Components on which a function is identically zero are handled separately. This retains singular parameter fibres and active inequalities.

The weighted-specialization proposition then imposes integral powers after writing the rational exponent p/q. It takes the **real closure**, with all model coordinates retained until after closure, and projects to the leading observation and coefficient coordinates. It outputs a quantifier-free description of the joint leading fibre. A final compact root-matching program yields an isolating polynomial and interval for the algebraic leading diameter. The input encoding, cluster isolation, complex coordinates, rational powers, root permutations, and output types are stated explicitly.

This is not a claim to have invented resolution or the valuative computation of a Łojasiewicz exponent. Those classical mechanisms are explicitly credited. The additional objects are the accessible real probability graph, the cluster weights, and the joint weighted spectral specialization. The singular example with observation order four and target-root order three demonstrates the nonimmersed formula directly.

## 2. Classification and stability of the cubic family

**Report sections 5, 11, and Option B.** The special equality s=2r/3 has been replaced by the two-parameter family

    f(z)=z(z-r)^2,  g(z)=(z-s)^3,  0<s<r<D.

The “Complete admissible pencil” lemma determines all c for which (1-c)f+cg has all roots in [0,D]. Its discriminant is

    c(c-1)^2(r-s)^3[(r+3s)(2r-3s)^2 c - 4r^3].

For s<=2r/3 the admissible pencil consists only of f and g. For s>2r/3 define z*=rs/(3s-2r) and c*=4r^3/[(r+3s)(2r-3s)^2]. An additional closed interval [c*,cD] occurs exactly when z*<=D, with cD given by the displayed rational endpoint formula in the paper.

The exact-fibre theorem incorporates the weight floor rather than confusing real-root admissibility with stochastic feasibility. An additional spectral value exists **if and only if** s>2r/3, z*<=D, and c*<=(1-alpha)/alpha*. It gives every additional component pair and constructs the corresponding positive stochastic columns. This is a whole-closed-model statement, not just a fibre calculation within a chosen parametrization.

In particular, the region

    0<s<2rD/(3D-r),  0<r<D

is open and spectrally identifiable. The old relation s=2r/3 is strictly inside this region. The quantitative recovery theorem is uniform on compact subsets with the stated margins. It persists under perturbations of clocks, strict weights, V, and positive U; a rank-two perturbation of U can remove its rank defect while retaining the same root order. Conversely, the paper constructs an exact stochastic fibre when the endpoint root is moved into the interior. This identifies the active boundary as the isolation mechanism and separates it from the old tuned relation.

The classification is for the explicitly stated double-root/triple-root boundary family. It is not advertised as a classification of every binary cubic model or every multiplicity pattern. A model-wide stratification as in Option D is not used as an unsupported additional claim.

## 3. The complete leading coefficient fibre and its exact constant

**Report section 6, section 14, and Option C.** The new leading-fibre theorem identifies the surviving cluster polynomials at scale sqrt(t) as

    z,  z^2-X,  z^3-Yz-Z,
    X,Y>=0,  J(X,Y)<=4,  27 Z^2<=4 Y^3.

The score map S is written explicitly in the original probability coordinates. Its variables include the endpoint motion a>=0, two cluster-sum motions, all five free non-root parameter derivatives, and the splitting variables X,Y. The Fisher inner product has exactly the Hellinger convention used throughout the paper.

After orthogonal projection off the seven free nuisance directions, the remaining cost is

    J(X,Y)=min_{a>=0} ||a p0+X px+Y py||_I^2.

Its explicit piecewise quadratic formula is displayed. The proof establishes coercivity on the nonnegative quadrant using whole-model coefficient recovery, not an inverse ambient Fisher matrix. It proves necessity from arbitrary closed-model competitors and sufficiency by constructing actual stochastic root arcs for every point in the fibre, including repeated-root extrema and radial limits on the observation-ball boundary.

Two fixed finite least-squares programs give positive numbers kappa_x and kappa_y. The exact leading diameter is

    C_P=max{sqrt(2) kappa_x^(-1/4), 2 sqrt(2/3) kappa_y^(-1/4)}.

This computation contains no inverse observation-ball optimization. The leading triple fibre is not exhausted by the symmetric split. At fixed Y the triples (-2h,h,h) and (-h,-h,2h), h=sqrt(Y/3), attain a diameter 2 sqrt(Y/3) while having the same leading observation score. Their score differs only in a higher-order cubic coefficient. The symmetric split proves the exponent but does not attain this complete triple-fibre diameter. Minimizing nuisance directions and the other cluster is also part of the stated program.

The resulting constant is a proved finite variational formula with its full feasible set and attaining arcs identified. Sample floating-point values in the diagnostics are illustrative evaluations, not an assertion that numerical arithmetic has verified the theorem or computed an exact algebraic number.

## 4. Expanded whole-model proof details

**Report section 8.** The proof now displays

    B'_coef=V' diag(alpha') F'_coef,
    beta/2 <= sigma_2(B'_coef) <= sigma_min(V') ||diag(alpha')F'_coef||.

The compact uniform upper bound M on the last norm yields ||V'^{-1}||<=2M/beta. Multiplying by inverse weights gives a uniform bound for L'=diag(alpha')^{-1}V'^{-1}. The exact identity F'=L'B+L'(B'-B) distinguishes the fixed span from the error; monicity normalizes the affine coefficients and the bound on L' controls their size. If both rows approached the same endpoint polynomial, sigma_2(F') would be O(delta), contradicting the lower singular-value bound for B'.

The normalization proof writes qE=eK, then q E^T 1=eB and the multiplication by diag(alpha,gamma)^{-1} V^{-1}. Bezout's identity supplies q|e from coprimality. Thus no full-rank first-channel result is being applied at rank loss.

A further step recovers the entire non-root parameter vector at order O(delta): fixed coefficient functionals dual to f,g recover each rank-one coefficient matrix A_b, and its entry sums and normalized marginals recover weights and channel columns. This additional bound is what justifies the exhaustive leading-score calculation; uncontrolled nuisance drift is not silently excluded.

## 5. Novelty and mathematical organization

**Report sections 7, 9, and 15.6.** The introduction now states the proposition-by-proposition boundary with classical work. Bierstone--Milman supply uniformization and resolution; Bivià-Ausina--Encinas supply the classical ideal-theoretic valuation calculation; Lee--Pham give direct semialgebraic metric-regularity context; Hà's 2026 preprint is identified as a preprint and is not a required technical input to the proof. The stochastic pencil classification and the complete constrained Fisher program are distinguished from these general mechanisms.

The main text has a single dependency chain: model -> finite real-valuative data -> cubic classification and quantitative recovery -> full leading fibre and constant. The preserved appendices are reordered by dependence: additive recovery and clocks; intrinsic moduli and composed jets; quotient/inference/algorithms; structured singular perturbations; relations and literature. Version identifiers remain internal source paths and labels, not mathematical headings. No old theorem or proof module is removed from the complete manuscript.

## 6. Remaining specific requests

| Report item | Revision action |
|---|---|
| 12: statistical interpretation | The abstract, introduction, model definition, and final theorem explicitly use a specified shrinking oracle neighbourhood. The two-point proof and limiting risk bounds are supplied; no global adaptation is claimed. |
| 13: effective output | Algebraic input, real graph lift, cluster isolation, integer rescaling, real closure, complex roots and matchings, and algebraic-number output are specified in the effective-fibre proposition. |
| 14: meanings of exactness | The proved asymptotic, explicit leading program, and finite numerical regressions are distinguished. Diagnostics are never called proof verification. |
| 15.1: coefficient norm | Euclidean coefficient norms and stacked Frobenius norms are fixed at the start of the cubic classification. |
| 15.2: determinant degree | The discussion before the appendices explicitly states that the invertible leading matrix fixes the determinant degree locally. |
| 15.3: cluster semialgebraicity | Unique semialgebraic choice is separated from analytic inversion in the finite-data section. |
| 15.4: zero in the leading fibre | The effective-fibre proof uses the exact-fibre representative in every observation ball. |
| 15.5: whole versus pointed | X_loc is reserved for a restricted compact local model; omission of X means the entire closed stochastic model. |
| 15.6: chronology-free writing | The new mathematical headings contain no revision labels; the dependency order, not revision chronology, organizes the complete manuscript. |
| 16: exact-head reproducibility | The branch-scoped workflow audits runtime HEAD, source hashes, every inherited active input, the retained entrypoint theorem, the actual compiled .fls graph, and the full log. Artifacts carry the actual commit SHA. |

## 7. Execution evidence and review hand-off

The new core was locally compiled from `core_v95.tex`: 12 pages, no undefined references or citations, no duplicate labels, and no overfull boxes. Its scope is visibly marked on the first page. All 120 finite pencil-grid checks passed, as did the exact symbolic discriminant/derivative identities, score finite differences, one-sided projection checks, stochastic fibre transformation, and leading triple-shape checks. `LOCAL_VALIDATION.json` and `local_diagnostics_v95.json` record this evidence.

The full inherited-appendix manuscript was **not compiled locally**, and a repository exact-HEAD audit was **not executed in the local staging directory**. The native workflow is provided for those separate checks. A queued workflow or a core-only PDF is not a successful full build. Its eventual exact-head receipt and workflow conclusion must be inspected before recording the complete manuscript as compiled.

The three new theorem-level arguments are offered for independent referee scrutiny. Compilation and finite regression evidence do not certify their mathematical correctness, and the revision does not pre-empt an editorial assessment of significance.
