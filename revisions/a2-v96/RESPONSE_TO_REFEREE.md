# Response to the controlling A2 referee report

## Source pin and the scope of this revision

The controlling report is `reviews/a2-v94-independent-harsh-top4-2026-09-19/REFEREE_REPORT.md`, at review commit `dbbad2d84c6a3b358bddabf84dc16f0b09b38634`. Its reviewed manuscript head is `5e01e5a2d6e93ef4c1e2619707608626fdc0f6cf`. No later A2 report was found in the review branches inspected for this revision. Revision 95 already responded to that report with real-valuative Newton data, a rank-one cubic classification, and a leading Fisher program. We use its exact head `ebb796e49ca51a62b90d92ec0d09819cfe8d00a4` as the baseline rather than silently treating revision 94 as the latest manuscript.

This revision is on the separate branch `revision/a2-v96-uniform-stratified-spectral-laws-2026-09-20`. Its complete entrypoint is `papers/A2-v17-boundary-information-coarsening/rigidity_v96.tex`. The title is *Projective polynomial observations: real valuations and stratified spectral laws*. All inherited mathematical and bibliography inputs remain active and byte-identical; all old entrypoints and reports remain unchanged. The new main text organizes the argument by mathematical dependence, with the earlier direct calculations and global theory in appendices.

The substantive new step is not another pointwise envelope theorem. We give an explicit classification across both channel ranks, a uniform normal form on the full identifiable portion of the named family, and a finite sign partition with rational formulas for the fourth power of the leading constant. Complete proofs are supplied for independent scrutiny; we do not equate their presentation, compilation, or regression checks with an independent certification of correctness or journal significance.

## 1. Singular finite data and the boundary with classical theory

**Report sections 4, 7, 10, 13; Option A.** The finite real-valuative theorem and real weighted specialization from revision 95 remain in the main text unchanged. Their inputs are the defining real observation--spectral graph, squared Hellinger distance, and squared cluster coefficients; their outputs retain accessible real divisors and the joint leading fibre. Classical uniformization, resolution, divisor orders, and semialgebraic elimination remain explicitly credited.

The new family theorem goes beyond existence of those data: its identification test is a finite list of signs in the original model parameters, and its leading constant is obtained by eight finite support tests and one comparison. No optimized coefficient envelope or fitted Puiseux exponent is an input to that calculation. The introduction now distinguishes the general real-valuative construction, the model-specific classification, and the elementary quadratic minimization used to evaluate the constant.

## 2. Complete identification across both ranks and the weight-isolated region

**Report sections 5 and 11; Option B.** In `article/v96/family.tex`, Theorem `thm:family-classification-v96` treats the named family

    f=z(z-r)^2, g=(z-s)^3, 0<s<r<D,

with arbitrary positive first channel U, positive invertible second channel V, strict weights, and at least seven clocks. Competitors range over the entire closed binary cubic model, not just this family. Set

    B=(3D-r)s-2rD,
    E=(1-alpha)(r+3s)(2r-3s)^2-4 alpha_* r^3.

The exact spectral fibre is a singleton if and only if

    det U != 0, or B < 0, or E < 0.

On the complementary rank-one set the theorem gives every extra pair `(f,(1-c)f+cg)` and its exact closed feasible interval, including equality cases. It constructs the positive stochastic columns and admissible weights realizing each pair. The region `B>=0, E<0` is now included: it is isolated by the weight floor although the root pencil alone has additional admissible polynomials. All rank-two centres are included, not merely a small perturbation of a selected rank-one centre.

The normalization argument is explicitly independent of the first-channel rank. At rank two, the recovered matrix polynomial yields the aggregate spectral polynomial through its determinant. At rank one, the second marginal, cubic discriminant, endpoint constraint and weight condition yield the necessary-and-sufficient classification. The statement is a classification of this entire named boundary double/triple-root family; it is not advertised as a classification of unrelated multiplicity patterns.

## 3. A uniform whole-model normal form, including changes of rank

**Report sections 4, 5, 10 and 11; Option D within the stated family.** Lemma `lem:uniform-inverse-v96` proves a coefficient and non-root parameter inverse for every closed-model competitor near every centre of a compact subset of the identifiable set. The proof covers rank-two centres by a simple-eigenvalue reconstruction and rank-one centres by quantitative marginal inversion and local pencil isolation. Whole-model fibre compactness excludes remote pencil alternatives even in the weight-isolated region. A finite neighbourhood cover makes the constants uniform across ranks.

In `article/v96/uniform_normal_form.tex`, Theorem `thm:uniform-normal-v96` proves the quantitative set statement

    d_H(R_theta(t), L_theta) <= C_H sqrt(t)

uniformly on each compact H in the identifiable set. Here R_theta(t) is the rescaled root image of the entire observation ball. The proof uses exact competitor root coordinates, a uniform Taylor remainder in coefficient coordinates, and actual stochastic arcs with a radial correction. It does not infer family uniformity by exchanging a pointwise limit with a supremum.

Consequently,

    omega_theta(t)=C(theta) sqrt(t)+O_H(t).

This improves the previous fixed-datum little-oh statement to a linear absolute remainder, valid across identified rank changes. The complete leading set remains

    z, z^2-X, z^3-Yz-Z,
    X,Y>=0, J_theta(X,Y)<=4, 27 Z^2<=4 Y^3,

but the score now allows distinct first-channel columns. All seven free nuisance variables and the one-sided endpoint motion are retained. Feasible coercivity is proved from actual admissible arcs and the coefficient inverse, rather than from an assumed nonsingular ambient Fisher matrix.

## 4. A finite parameter partition and exact leading constants

**Report section 6, sections 13--14; Options C and D.** In `article/v96/active_sets.tex`, Theorem `thm:phase-partition-v96` eliminates the two nonnegative least-squares problems explicitly. The seven-column nuisance Gram matrix is proved invertible even at rank one. After its Schur complement, each of the two programs has four possible supports. Invertible support Gram matrices, nonnegative supported variables and inactive derivative inequalities give exact rational sign tests.

The proof deals with singular two-column Gram matrices by choosing a minimizer of minimal positive support; such a support is independent. Hence no candidate is lost at rank one. Ties and zero supported coefficients are included. On the resulting finite semialgebraic partition,

    C^4=max{4/kappa_x, 64/(9 kappa_y)},

with switching sign `9 kappa_y-16 kappa_x`. Each selected expression is rational in the original root, channel, weight and clock parameters. A finite real-analytic stratification refines these sign classes. C is continuous across active-set boundaries and across channel-rank changes inside the identifiable set. The uniform remainder holds on compact sets crossing these boundaries, not only within a single stratum.

The proof identifies the diameter-extremizing triples `(-2h,h,h)` and `(-h,-h,2h)`, with the same leading score and opposite centred cubic coefficients. The actual-arc construction realizes them, with all minimizing nuisance variables. Thus the symmetric triple split is not mistaken for the full extremal mechanism.

Example `ex:exact-constant-v96` gives two rational data. For the rank-one datum, exact arithmetic yields

    C^4=78550423766145732273576408862601811503774391446
        /385279214348552940073664077156875,
    3778.707<C<3778.708.

Changing only the second first-channel column to `(2/5,3/5)` gives a rank-two, triple-dominant datum with `59.970<C<59.971`. `EXACT_CONSTANTS.json` records both rational Gram matrices, support solutions and fourth powers. The intervals are certified by rational fourth-power comparisons, not numerical error bars.

## 5. Detailed proof requests and statistical quantifiers

**Report section 8 and sections 12--15.** The new inverse proof displays the normalization marginal identity, the singular-value bound controlling the competitor's inverse channel, the bounded affine-pencil reduction, and recovery of weights and channels from coefficient matrices. Coprimality and the seven-clock degree count are explicit. The coefficient norm and Hellinger normalization are fixed at the start of the family argument.

The free score columns are proved independent by feasible coercivity. The endpoint is retained as a one-sided variable throughout; positive observed cells do not erase a latent inequality constraint. The new uniform risk corollary keeps the experiment explicitly centred on a specified shrinking oracle neighbourhood. It provides uniform two-point and constant-decision bounds with an O(N^(-1/4)) remainder after multiplication by sqrt(N); it does not claim an unknown-centre adaptive estimator or honest global confidence procedure.

## 6. Article structure and preservation

**Report section 9 and section 15.6.** The complete main text follows one chain:

    real graph -> finite valuation data -> exact family classification
    -> uniform spectral normal form -> finite phase formulas.

The previous rank-one proofs remain active as complementary appendices. Additive normalization, clock recovery, intrinsic moduli, quotient/inference results and structured singular perturbations follow by dependency. The source paths retain version provenance, but the mathematical headings do not describe a revision chronology. No inherited mathematical file is edited or removed, and no old result is silently substituted by a narrower theorem.

## 7. Execution evidence and its limits

The standalone `family_core_v96.tex` reading copy compiled locally to eight pages. Its first page explicitly states that it is not the complete manuscript. The final log has no undefined references or citations, duplicate labels, or overfull boxes; all eight pages were rendered and visually inspected. Finite symbolic identities, four identified test configurations, eight active-set comparisons, twelve actual-arc remainder checks across ranks, a fibre transformation and triple-diameter checks passed. Both rational examples were evaluated with exact arithmetic. These are finite regressions, not proof certification.

The complete inherited-appendix manuscript was not compiled in the local staging directory. That directory is not a full repository checkout, so an exact-HEAD repository audit was not executed there. The branch-scoped workflow performs those separate checks: it rejects any inherited edit, verifies the new-source hashes and every inherited active input, compiles the complete entrypoint, then checks its actual `.fls` graph and full log. Artifacts and runtime receipts are identified by the actual commit SHA. A queued workflow is not a successful build; its final conclusion must be inspected before calling the full manuscript compiled.

The revision therefore supplies a new classification and uniform-stratification argument for further independent referee review, with the mathematical assertions, exact algebraic evaluations, finite diagnostics and full-build status kept distinct.
