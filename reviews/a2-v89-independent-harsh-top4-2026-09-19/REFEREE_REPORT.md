# Independent harsh referee report on A2 revision 89

**Review date:** 19 September 2026  
**Repository:** TrillionniumFoundation/theta-theory  
**Reviewed revision branch:** review base material from revision/a2-v89-observable-polynomial-quotient-2026-09-19  
**Reviewed branch head:** 7b4bf68e3d0a974a3c9bc253d103535f4f339f7a  
**Pinned manuscript-source commit:** 3de72a935ce643ea22e522ba7a6c233331d76247  
**Controlling previous referee report:** 47fd795b7e4d80f9fe81e9798e73a05efc7fa8f7  
**Reviewed manuscript:** *Projective polynomial observations: observable conditioning and singular inference*  
**Author:** Qian Qi

## 1. Recommendation

**Recommendation to the editor: reject in the present form at the stated four-leading-general-mathematics-journal level.**

This recommendation is materially different in basis from my recommendation on revision 88.

Revision 89 is a serious mathematical advance over revision 88. The author has not merely added another special observation regime. The revision constructs an observable degree-d condition through the joint coefficient algebra, separates the scalar normalization error from the matrix spectral error, gives a genuinely useful additive global inverse bound, formulates an exact local Jacobian condition on regular charts, proves higher-degree class-minimax and multiplicity-neighbourhood rates, and gives a clean full-span clock count. Several of the central objections in the previous report have therefore been answered in substance.

I did **not** find a short fatal counterexample to the principal new algebraic identities or to the displayed minimax exponents.

That is not enough for the requested journal level. The revision now reaches a point where the remaining problems are not cosmetic. They concern the exact mathematical status of the proposed observable condition, the completeness of the local quotient argument, the breadth of the singularity theory, and the originality comparison with the substantial matrix-polynomial and multiple-eigenvalue conditioning literature. In its present form the article still combines one genuinely interesting observation-specific mechanism with several classical perturbation and testing mechanisms, without yet proving the unifying theorem that would make the package a leading general-mathematics contribution.

I would regard a carefully revised version as a credible candidate for a strong specialist journal in inverse problems, statistics, matrix analysis, or applied analysis. For a four-leading-general-mathematics-journal resubmission, I would require a further structural theorem, not additional finite examples, diagnostics, or another observation law.

## 2. Scope and provenance of this review

I reviewed the v89 source pinned above rather than an earlier A2 revision. The branch head is two documentation/response layers beyond the manuscript-source commit; the response package states, and the repository layout confirms, that the principal v89 manuscript sources are those at commit 3de72a935ce643ea22e522ba7a6c233331d76247.

The principal article is driven by

papers/A2-v17-boundary-information-coarsening/rigidity_v89.tex

and the v89 article modules. I read the new normalization, clock-complexity, observable-conditioning, exact-local-condition, general-quotient, and polynomial-statistics modules, as well as the retained estimator, affine-statistics, affine-residue, relation, and reference modules insofar as they enter the new claims. I also read the response to the v88 report and the build/literature receipts.

The review is a mathematical referee assessment. The finite diagnostic JSON is treated as regression evidence only. It is not proof certification.

At the time of this review, the GitHub Actions run associated with the v89 pull-request head was still reported as queued, with no successful conclusion. I therefore credit the documented local native build as a local build only; I do not credit an independent remote build.

## 3. What v89 has genuinely accomplished

The revision deserves explicit credit before the objections.

### 3.1 The observable polynomial gauge is the right structural direction

The construction in Theorem 3.1 is the strongest new idea in v89.

After normalization recovery, the reduced polynomial matrix has coefficient algebra

C_j = M_j A_0^{-1},

and the complete component polynomials appear as joint eigenvalue tuples. Grouping by complete polynomial rather than by individual root is exactly the right way to survive cross-component root collisions. The associated projectors E_f and weights

W_f = A_0^{-1} E_f

give the resolvent decomposition

M(z)^{-1} = sum_f W_f / f(z).

The normalization perturbation is then transported through a scalar polynomial gauge inside each complete-polynomial block. This is the conceptual content behind the additive susceptibility

B_d + tau^{-1}

rather than a product of normalization and channel losses. This is substantially better than the latent-kappa formulation in v88.

### 3.2 The full-span clock theorem fixes an important overstatement in the older narrative

Proposition 2.6 correctly distinguishes the worst-case 2d+1 clock requirement from the full-polynomial-span regime. The rank bound

rank N_P <= min{d,(s-1)(ell-d-1)}

is useful, and the d+2 sufficiency proof on the full-span class is clean. The paper no longer pretends that the low-functional-rank worst case describes every high-capacity observation curve.

### 3.3 The higher-degree statistical section is no longer merely aspirational

Theorems 9.1–9.3 do real work. In particular, revision 89 supplies:

- a whole-closed-model honest residual confidence construction;
- class-minimax parametric rates on eta_d-bounded semisimple classes;
- adaptive-design lower bounds through conditional relative entropy;
- real-rooted multiplicity neighbourhoods with squared-risk exponent N^{-1/m}.

This is a genuine answer to the previous objection that the sharp statistical theory was essentially affine.

### 3.4 The author now distinguishes three different notions that were previously conflated

The manuscript now separates:

1. the global observable certificate eta_d;
2. the exact infinitesimal local condition on a regular chart;
3. class or neighbourhood minimax risk.

That distinction is mathematically necessary and substantially improves the paper.

## 4. Status of the six structural requests from the v88 report

My assessment of the response is as follows.

| Previous request | v89 status | Referee assessment |
| --- | --- | --- |
| Observable degree-d singular condition | Substantially addressed | Theorem 3.1 is a genuine advance |
| Two-sided local conditioning | Partially addressed | Formula is plausible, but the quotient-chart proof is too compressed |
| Rational realization / interpolation comparison | Partially addressed | Direct predecessors are now acknowledged, but the literature audit is still too narrow |
| Sharp inference beyond d=1 | Substantially addressed | Correctly class-minimax / neighbourhood-minimax, not a complete local theory |
| Broader quotient theorem | Only partially addressed | Theorem 5.1 is classical algebra; Proposition 5.2 is a standard resolvent mechanism |
| Explicit dimension / degree / clock dependence | Addressed at the deterministic-bound level | Proposition 3.2 is useful and appropriately qualified |

Thus v89 has closed several of the previous blockers, but not all of them at the depth needed for the claimed journal level.

## 5. Major objection I: eta_d is an observable certificate, not yet the intrinsic sharp condition

This is now the most important structural issue.

Theorem 3.1 proves that eta_d is observable, has the correct positive set, behaves reasonably under grouping, and yields a global one-sided inverse modulus against the entire closed model. That is valuable.

But the paper does **not** prove that eta_d is the intrinsic condition number of the observation inverse.

Indeed, the manuscript itself correctly acknowledges that the exact local condition is the Jacobian quantity in Theorem 4.1 and that eta_d need not equal it. Nor is eta_d identified, even up to universal equivalence, with a distance to the singular locus, a metric regularity modulus, a smallest singular value of the quotient observation map, or a pointwise minimax modulus.

The lower bounds in Theorems 9.2 and 9.3 do not repair this. Theorem 9.2 proves the minimax order over the class eta_d >= s by embedding a deliberately engineered one-parameter family. This is a legitimate class-minimax lower bound. It does not show that every datum with eta_d(P) approximately s has local statistical difficulty of order 1/(N s^2), or that eta_d is necessary for the global inverse bound at that datum.

This distinction matters because the abstract and section title use the language of “observable conditioning” and “sharp inference in every degree.” The mathematics currently proves:

- a strong global sufficient certificate;
- exact local conditioning on a regular stratum by a different quantity;
- sharp class and neighbourhood rates on selected strata.

That is not yet a unified sharp condition theory.

### What would close this objection

A top-level revision should prove at least one of the following.

1. A two-sided comparison between eta_d and an intrinsic global/local modulus on a natural maximal class.

2. A distance-to-singularity theorem showing that eta_d is equivalent to the distance, in a specified observation geometry, to the normalization/rank singular set.

3. A pointwise or local asymptotic minimax theorem whose lower modulus is controlled by the same observable object appearing in the upper theorem.

4. A proof that no scalar observable condition can do better globally, together with a precise optimality statement for eta_d.

Absent such a theorem, the correct presentation is that eta_d is an observable global certificate, not the sharp intrinsic condition.

## 6. Major objection II: Theorem 4.1 depends on a local quotient theorem that is not proved at top-journal level

The displayed formula

c_2(P) = max_a sqrt([G(J^T J)^{-1}G^T]_{aa})

is not, by itself, the difficult part. Once one has a smooth locally identifiable parameter chart and an injective derivative, it is a standard dual-norm calculation.

The model-specific theorem is the assertion that the chosen coefficient coordinates actually give a smooth local chart for the **quotient model image**, with no nearby representatives outside the chart except component permutations.

The current proof compresses this into essentially two paragraphs:

- joint projectors recover singleton complete-polynomial groups and then the rank-one matrices alpha_b U_b V_b^T;
- if another nearby representation existed, compactness plus the normalization equation and projectors would force the same limit, hence a contradiction.

For a theorem advertised as the exact two-sided local condition, that is too compressed.

The paper should isolate and prove a local quotient-identifiability theorem with the following items explicit.

### 6.1 Local model structure

Specify the parameter manifold, its stochastic constraints, the permutation action, and the open regular stratum. State whether the quotient is a manifold or an orbifold on this stratum.

### 6.2 Uniqueness of nearby representations

Prove that every sufficiently nearby observation in the model has a representative in the chosen chart, unique modulo the finite permutation group. A subsequence/compactness contradiction can be part of the proof, but all possible stabilizers must be excluded explicitly.

### 6.3 Smoothness of the inverse

Show that the recovered normalization, subspaces, joint projectors, coefficient tuples, rank-one factors, stochastic normalizations, and simple component roots depend smoothly on the observation datum in the stated metric.

### 6.4 Cross-component collisions

The manuscript says cross-component root collisions are allowed. This is plausible because the complete component polynomials are distinct and their roots are simple internally, but the proof should explicitly explain why a root collision does not create an additional quotient stabilizer or destroy the differentiability of the aggregate target map.

Once this proposition is proved, Theorem 4.1 becomes convincing. In the current version, the exact equality rests on an important local-geometry assertion that is sketched rather than established with the precision expected at the stated level.

## 7. Major objection III: the literature audit is still not adequate for the new conditioning claims

The response has improved the rational-interpolation discussion by adding Anderson–Antoulas, Beckermann–Labahn, and Mayo–Antoulas. That was necessary.

It is not sufficient for the new headline claims about spectral conditioning, multiple roots, and Hölder exponents.

At minimum the revised paper must confront directly the established literature on polynomial-eigenvalue conditioning and multiple-eigenvalue Hölder conditioning, including, for example:

- F. Tisseur, “Backward error and condition of polynomial eigenvalue problems,” Linear Algebra and its Applications 309 (2000), 339–361, DOI 10.1016/S0024-3795(99)00063-4.
- D. Kressner, M. J. Peláez, and J. Moro, “Structured Hölder Condition Numbers for Multiple Eigenvalues,” SIAM Journal on Matrix Analysis and Applications 31 (2009), 175–201, DOI 10.1137/060672893.
- L. M. Anguas, M. I. Bueno, and F. M. Dopico, “A comparison of eigenvalue condition numbers for matrix polynomials,” Linear Algebra and its Applications 564 (2019), 170–200, DOI 10.1016/j.laa.2018.11.031.
- the standard matrix-polynomial and perturbation monographs and the multiple-eigenvalue perturbation literature cited by those works.

This is not a request for bibliography inflation. The reason is conceptual.

The 1/m sensitivity exponent near multiple roots, resolvent exclusion, and multiple-eigenvalue Hölder conditioning are not new phenomena. The novelty, if the paper is to claim it, lies in transporting **observation error through the projective normalization and latent stochastic structure** into a spectral perturbation problem, and in proving statistical consequences for that experiment.

The article should therefore make a theorem-by-theorem distinction between:

1. classical matrix-polynomial spectral sensitivity;
2. the new projective-normalization gauge;
3. the new observable coefficient-algebra quantity;
4. the statistical experiment and its least-favourable paths.

Until this comparison is done, I cannot assess the degree of novelty of the conditioning section with the confidence required for a four-leading-general-journal recommendation.

## 8. Major objection IV: the global proof of Theorem 3.1 is plausible but too compressed at several decisive transitions

I did not find an immediate algebraic contradiction in the proof. The resolved inverse and the gauge identity appear correct.

However, the proof passes too quickly over the points where a global closed-model statement is won.

### 8.1 Degree preservation along both homotopies

The argument states that leading coefficients stay invertible because the scalar leading coefficients in the gauge are close to one, the gauge leading inverse is controlled by B_d, and H_d is a small relative perturbation.

This needs a standalone quantitative lemma. The theorem is global against competitors that may initially have singular channels. The proof should specify exactly which smallness condition in delta, B_d, and tau guarantees invertibility along:

- M + u(Mbar_r-M);
- Mbar_r + sH.

That lemma should also state explicitly that det has degree exactly kd throughout.

### 8.2 Passage from reduced competitor roots to the component root multiset

The current proof says that an invertible leading coefficient of the reduced competitor forces the reduced channel factors to be invertible, hence the determinant roots are exactly the competitor component roots.

This is true under the fixed-capacity factorization, but it is a crucial bridge from an arbitrary matrix-polynomial perturbation to the statistical target. It deserves a separate lemma with the dimensions, ranks, and determinant factorization written out.

### 8.3 Cluster refinement

The 1/m refinement is stated for separated clusters containing at most m roots of each component, while arbitrary cross-component collisions are allowed.

The proof should define the cluster system precisely and give the uniform lower bound for every scalar component polynomial on the complement. The current argument is mathematically plausible but too terse to serve as the definitive theorem on which the higher-degree statistical section rests.

### 8.4 Semicontinuity at grouping changes

The lower semicontinuity argument for B_d is credible, but the proof relies on clustering joint tuples and, in one sentence, permits taking a compact subsequence of latent parameters to justify it. Since B_d is advertised as representation-free, it would be cleaner to prove this entirely in the observable coefficient algebra, or else state a separate representation compactness lemma.

These are not reasons by themselves to reject a specialist-journal paper. They are reasons not to treat Theorem 3.1 as fully publication-ready at the stated standard.

## 9. Major objection V: the “general quotient” section does not yet supply the broader structural theorem suggested by its placement

Theorem 5.1 is a clean statement, but mathematically it is a scalar-denominator rational-interpolation divisibility module. The article itself correctly calls it classical.

Proposition 5.2 then gives a resolvent bound for a regular square polynomial matrix without simultaneous diagonalization. Again, the mechanism is classical: Laurent expansion, normalization perturbation, Neumann exclusion, argument-principle root counting.

The genuinely new additive cancellation law of the paper still uses the simultaneous semisimple joint coefficient algebra of the stochastic diagonal model.

Therefore v89 has not yet shown that the central additive observation-level mechanism survives in a genuinely noncommuting or nondiagonalizable quotient class.

The section is useful background and a legitimate robustness check. It does **not**, in its current form, raise the main theorem to a general theory of rational matrix quotients.

For a top-four resubmission, the author should either:

- prove an observation-level additive normalization law for a materially broader noncommuting class; or
- demote the general quotient section from a headline structural advance and present it as a classical comparison/extension.

## 10. Major objection VI: the singularity theory remains a collection of separate strata rather than a unified geometry

The paper now treats several singular mechanisms correctly and separately:

- normalization failure tau -> 0;
- channel-rank loss;
- within-component root multiplicity;
- semisimple cross-component collisions;
- affine complete collapse.

But their intersections remain unclassified.

Theorem 9.3 explicitly assumes regular normalization and full-rank channels. Theorem 4.1 also lives on a regular normalization/full-rank stratum with simple roots within each component. Theorem 9.2 gives a semisimple signal class. The affine families separately treat channel-product and collapse losses.

Thus the article has a **catalogue of sharp regimes**, not yet a singularity normal form for the whole observation map.

This is the main reason I still do not see a four-leading-general-journal theorem.

A genuinely structural next result would stratify the quotient model near a general singular datum and determine how:

- normalization-kernel dimension;
- channel-rank defect;
- polynomial multiplicity;
- equality of complete component polynomials;
- cross-component root collision

combine to determine the local inverse exponent and statistical rate.

It is not necessary that the final answer be one closed-form scalar condition. But the paper needs a theorem explaining the interaction of the singular mechanisms, rather than treating only their clean separated faces.

## 11. Assessment of the statistical claims

The statistical section is much stronger than in v88, but its claims should remain exactly at the level proved.

### 11.1 Theorem 9.1

The upper bound follows naturally from the deterministic modulus and finite categorical concentration. I have no major objection to the stated order for fixed experiment dimensions and clocks.

### 11.2 Theorem 9.2

The lower construction is clever and useful. In particular, it avoids obtaining a degree-d result by simply multiplying an affine experiment by a common polynomial factor.

However, the result is a minimax theorem over the class eta_d >= s. Its lower bound is witnessed by a special family near a weak channel-product direction. This proves the class order. It does not make eta_d a pointwise sharp condition at all members of the class.

I recommend changing broad prose such as “sharp inference in every degree” whenever it could be read as a complete local characterization. “Sharp class-minimax rates in every fixed degree” would be more accurate.

### 11.3 Theorem 9.3

The moving-real-root construction is a real improvement. It correctly avoids the false idea that arbitrary constant coefficient perturbations of an m-fold real root remain real rooted.

The theorem should nevertheless be presented as what it is: a neighbourhood minimax theorem on a regular-normalization/full-rank component-multiplicity stratum. It does not describe intersections with the other singular boundaries.

### 11.4 Adaptive clocks

The conditional KL chain-rule argument is an appropriate way to extend the lower bounds to parameter-independent adaptive clock policies. I found no hidden fixed-design assumption in the displayed argument.

## 12. Clock-complexity comments

The distinction between the 2d+1 worst-case count and the d+2 full-span count is important.

I would, however, resist any suggestion that the paper has now solved the general clock-complexity problem. For intermediate functional span s, Proposition 2.6 gives a useful rank upper bound but not a complete necessary-and-sufficient classification.

That is entirely acceptable if stated explicitly. It becomes a problem only if the introduction suggests that the two endpoint counts exhaust the design theory.

## 13. Detailed proof and presentation comments

### 13.1 Positive local fibre

In Lemma 2.2, the phrase about choosing “disjoint brackets” around each root should say explicitly that disjointness is required within each scalar component polynomial, not across different components. Cross-component roots are allowed to coincide.

The later finite-valued continuous-path argument is the correct way to handle the aggregate collision issue.

### 13.2 Root perturbation lemma

The linear stability through cross-component collisions is credible because simplicity is imposed within each scalar polynomial. The exposition should write the componentwise lower bound

|f_b(z)| >= c_nu min{1, dist(z,Z(f_b))}

and then pass to the global distance, rather than saying vaguely that “the other factors” stay bounded below. This would remove an avoidable ambiguity at shared roots.

### 13.3 Frame invariance of B_d

The orthogonal frame-invariance calculation is correct and should remain explicit. It is one of the points that makes the certificate genuinely observable rather than a disguised latent factor norm.

### 13.4 Exact local Fisher metric

The categorical Fisher metric should be stated as the diagonal form restricted to the probability-simplex tangent space. The displayed ambient diagonal matrix is positive definite, so the formula is harmless, but the statistical geometry would be cleaner if the tangent constraint were made explicit.

### 13.5 General quotient root count

In Proposition 5.2, state explicitly that invertibility of the leading coefficient makes det M a scalar polynomial of degree exactly kd, so “the kd numerator roots” is not merely a convention.

### 13.6 Exact arithmetic

The estimator is honestly described as an exact-arithmetic stability theorem. I support that qualification. The paper should not add numerical-complexity language unless it proves thresholded rank/root selection in finite precision.

### 13.7 Confidence-region computation

The paper correctly separates information-theoretic confidence inversion from computational tractability. That distinction should be kept.

## 14. Reproducibility and repository evidence

The repository organization is careful and substantially better than in early rounds.

I credit the following:

- the v89 source is pinned by commit;
- the response distinguishes manuscript source from later documentation;
- source hashes are recorded;
- the local native build is documented;
- the finite diagnostics are explicitly described as non-formal evidence;
- the author discloses that the new diagnostic script itself was not uploaded.

I do **not** treat the diagnostic JSON as independently reproducible while the generating script is absent.

I also do **not** credit a completed GitHub Actions build at the reviewed v89 head: the relevant run was still queued at my readback and had no successful conclusion.

Neither point is a mathematical rejection reason. They matter only because the repository devotes substantial space to validation evidence. If that evidence remains part of the submission package, the new diagnostic script should be committed and the native workflow should complete successfully.

## 15. Editorial assessment of novelty and significance

My present reading is that the paper contains one potentially publishable structural idea of real interest:

**projective normalization error can be transported through the recovered joint coefficient algebra without paying a second multiplicative latent-channel condition loss.**

The rest of the paper develops this idea through clock identification, matrix-polynomial perturbation, explicit estimation, and statistical lower bounds.

That is a coherent paper.

The difficulty at the four-leading-general-journal level is that much of the surrounding machinery is classical once the gauge has been constructed:

- rational interpolation and common-factor modules;
- matrix-polynomial resolvent exclusion;
- Hölder root sensitivity at multiplicities;
- Jacobian local condition formulas on regular charts;
- Le Cam/Pinsker two-point minimax lower bounds.

The manuscript has not yet shown that its new gauge principle generates a sufficiently broad theorem beyond the simultaneously semisimple stochastic model, nor has it identified the exact singularity geometry of that model itself.

For those reasons the conceptual reach remains below the requested level.

## 16. What would materially change my assessment

I would not recommend another revision that merely adds more regimes. A renewed top-four review should be justified by at least one of the following structural advances.

### 16.1 Intrinsic sharpness of the observable condition

Prove a two-sided theorem identifying eta_d, or a refined observable replacement, with the actual inverse modulus or local asymptotic difficulty on a large natural class.

### 16.2 Unified singularity normal form

Give a stratified theorem describing the joint effect of normalization defect, rank loss, complete-polynomial collisions, and internal multiplicity.

### 16.3 Genuinely broader additive quotient theorem

Extend the additive normalization mechanism, not merely the resolvent argument, to a noncommuting/nondiagonalizable matrix-rational class.

### 16.4 Complete local quotient proof plus local minimax equivalence

Turn Theorem 4.1 into a rigorous quotient-manifold theorem and connect its exact condition directly to a local statistical lower bound in the same observation metric.

Any one of these, if executed at full strength and positioned against the established conditioning literature, could materially change the editorial assessment.

## 17. Required corrections even for a specialist-journal version

Before publication anywhere at a high level, I would require:

1. a full local quotient-identifiability proposition supporting Theorem 4.1;
2. expansion of the critical homotopy/rank steps in Theorem 3.1;
3. a substantially deeper matrix-polynomial and multiple-eigenvalue conditioning literature comparison;
4. narrower wording around “sharp” whenever only class-minimax or neighbourhood-minimax sharpness is proved;
5. explicit separation between the new observation-gauge contribution and classical spectral perturbation machinery;
6. either reproducible upload of the new diagnostics or removal of any implication that the recorded JSON can be independently regenerated from the branch.

## 18. Final assessment

Revision 89 is the strongest A2 version I have reviewed.

Unlike v88, it does answer the central mathematical criticism that the general degree-d result was tied to an unobservable latent channel condition. The joint-projector construction is substantive. The full-span clock theorem and the degree-d statistical lower bounds are also meaningful additions.

I nevertheless recommend **rejection in the present form at the four-leading-general-mathematics-journal level**.

The reason is no longer that the paper lacks a degree-d observable theory. It now has one. The reason is that the proposed observable condition has not been shown to be intrinsically sharp, the exact local theorem rests on an underdeveloped quotient-chart argument, the singular mechanisms are not unified, the noncommuting extension does not carry the central additive mechanism, and the novelty comparison omits directly relevant multiple-eigenvalue and matrix-polynomial conditioning literature.

This is a serious paper with a real core idea. It is not yet, in my judgment, a paper whose present theorem package establishes the breadth and structural finality expected at the stated journal level.

---

*This is an owner-requested independent external-referee-style assessment of the repository manuscript. It is not a journal-commissioned report and does not represent an editorial decision.*
