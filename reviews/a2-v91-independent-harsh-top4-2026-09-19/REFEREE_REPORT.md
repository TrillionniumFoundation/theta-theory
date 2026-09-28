# Independent harsh referee report on A2 revision 91

**Review date:** 19 September 2026  
**Repository:** TrillionniumFoundation/theta-theory  
**Reviewed revision branch:** revision/a2-v91-integrated-quotient-geometry-2026-09-19  
**Reviewed branch head:** d1acb5d047a3c32b2c676ebe76ca0a64f8952ed2  
**Canonical manuscript alignment commit:** 382bdd0f62c1e89b3c8d92b779bba6d64e835680  
**Previous revision base:** revision/a2-v90-intrinsic-local-minimax-flag-gauge-2026-09-19 at 361e74157b45944b29e7d026b43255c6f2748388  
**Controlling earlier review consulted:** review/a2-v89-independent-harsh-top4-2026-09-19  
**Reviewed manuscript:** *Projective polynomial observations: intrinsic geometry and additive normalization*  
**Author:** Qian Qi

## 1. Recommendation

**Recommendation to the editor: reject in the present form at the stated four-leading-general-mathematics-journal level.**

This recommendation should not be read as a repetition of the v89 report. Revision 91 is substantially stronger than revision 89, and revisions 90--91 have in fact answered most of the concrete mathematical objections in that report.

In particular, the author has now supplied:

- an explicit local quotient-identification theorem, with analytic recovery of every nearby closed-model representation modulo the finite component permutation action;
- an exact local inverse condition on that quotient;
- an exact local asymptotic minimax constant in the same Fisher geometry, including cross-component root collisions;
- the previously missing quantitative homotopy, degree-preservation, competitor-rank and grouping lemmas for the global observable inverse theorem;
- an additive normalization gauge for noncommuting, possibly defective coefficient algebras admitting a common invariant flag;
- a materially improved comparison with the classical matrix-polynomial, multiple-eigenvalue and rational-realization literature;
- an intrinsic Hellinger-neighbourhood modulus defined at every point of the closed stochastic model, with a two-sided minimax comparison and a semialgebraic/Puiseux arc exponent;
- a sharp anchored square-root law for real-rooted internal multiplicities, explicitly distinguished from the slower fixed-neighbourhood moving-pair rates.

I did not find a short counterexample invalidating the principal v90--v91 theorems. The regular quotient and local minimax results are now credible mathematical theorems rather than programmatic claims, and the additive flag theorem is a genuine extension beyond the simultaneously semisimple diagonal model.

The reason for the present recommendation is therefore narrower and more serious from an editorial point of view. The manuscript now has several correct structural layers, but the claimed unification at arbitrary singular model points is achieved by introducing a generic variational modulus whose existence and rational asymptotic exponent follow from compactness, two-point testing, and semialgebraic geometry. This is an exact description of the decision problem, but it is not yet a model-specific singularity theorem. It does not identify the exponent, leading constant, or local normal form in terms of the normalization defect, channel-rank defect, equality pattern of component polynomials, internal root multiplicities, and their intersections. The paper therefore still stops just before the theorem that would turn a strong specialist contribution into a convincing leading-general-mathematics contribution.

There is also one concrete repository defect: the v91 verification program at the reviewed head cannot execute its own source-audit path because it requires revisions/a2-v91/SOURCE_MANIFEST.json, while that file is absent from the branch. I found no GitHub Actions run attached to the reviewed head. This does not determine the mathematical recommendation, but it invalidates any claim that the committed v91 verifier is currently reproducible as stated.

## 2. Scope and provenance

I reviewed the exact v91 branch head d1acb5d047a3c32b2c676ebe76ca0a64f8952ed2, not main and not an earlier A2 branch.

Relative to v90, v91 is seven commits ahead. The new v91 material consists principally of:

- article/v91/paper.tex;
- article/v91/intrinsic_modulus.tex;
- article/v91/literature.tex;
- article/v91/references.tex;
- the canonical rigidity_v91.tex entry point;
- revisions/a2-v91/verify_a2_v91.py.

I also reread the v89 observable theorem and statistics, the v90 local quotient theorem, the v90 local asymptotic minimax theorem, the v90 global-proof details, and the v90 noncommuting flag-gauge theorem because the v91 claims depend directly on them.

The finite Python diagnostics are treated only as diagnostics. They are not a substitute for proof. In the present branch they cannot be run through source_audit without adding the missing manifest.

## 3. What revisions 90--91 genuinely fix

The author deserves explicit credit here. Several objections that were major in v89 are no longer valid objections to v91.

### 3.1 The local quotient theorem is now a theorem

Theorem 4.1 in the current architecture isolates the correct regular parameter manifold in monic coefficient coordinates, proves that the component-permutation action is free, identifies the exact fibre, and constructs an ambient analytic recovery map.

The key recovery chain is now explicit:

1. tau(P)>0 recovers the unique monic normalizer q.
2. Interpolation recovers K.
3. Rank k of the leading coefficient forces full-rank competing channels.
4. The recovered coefficient algebra has distinct joint tuples.
5. Rank-one joint projectors isolate alpha_b U_b V_b^T.
6. Total, row and column sums recover alpha_b, U_b and V_b.
7. Riesz projectors in a separating linear combination give analytic local recovery.
8. Every nearby closed-model representative is one of the finitely many component permutations.

This is the missing model-specific content behind the Jacobian condition formula. Cross-component root collisions are handled at the level of complete component polynomials, where no stabilizer is introduced merely because scalar roots coincide.

I no longer regard the local quotient argument as a fatal gap.

### 3.2 The exact local statistical theorem is materially stronger than the old class lower bounds

The local Fisher object

V = G(J^T H_{P,w}J)^{-1}G^T

now has two precise interpretations:

- the deterministic radial inverse condition is the maximum square root of its diagonal entries;
- the local asymptotic minimax constant is E||N(0,V)||_infinity^2.

The Gaussian quotient lemma is the important additional step at root collisions. The manuscript does not differentiate the sorting map. It instead works with the finite permutation quotient of equal-base-value root groups and shows that the quotient cannot reduce the worst-case Gaussian location risk.

This is a real improvement. It supplies a pointwise sharp local theorem on the full regular quotient, not merely a testing family establishing a class order.

### 3.3 The global inverse proof has been repaired at the places where v89 was too compressed

The added lemmas on the two leading-coefficient homotopies, the reduced competitor determinant, componentwise cluster bounds, and observable grouping semicontinuity are the correct repairs.

In particular, the paper now explicitly proves:

- when the leading coefficients remain invertible along both homotopies;
- why every determinant has degree exactly kd;
- why small observation error forces even an initially singular competitor to have full-rank reduced channels;
- why the kd roots counted by the homotopy are exactly the competitor component roots;
- why cluster constants require only within-component separation and not cross-component separation;
- why the lower semicontinuity of B_d can be proved inside the observable coefficient algebra.

I no longer object that the main global theorem hides its decisive closed-model transitions in prose.

### 3.4 The noncommuting extension is no longer merely a classical resolvent paragraph

The flag-gauge theorem is a substantive new layer.

The scalar interpolation gauge preserves an invariant flag because it acts entrywise and commutes with constant changes of basis. In a common triangular form, the normalizer perturbation first moves only the scalar diagonal polynomials, while the remaining unrestricted matrix error is subsequently charged through the finite triangular inverse expansion.

This yields the two-scale estimate

d_infinity(Z(M),Z(M'))
  <= C{(delta/tau)^(1/d) + (B_triangle delta)^(1/(kd))},

and its cluster/path refinement.

The positive noncommuting defective example shows that this is not just a reformulation of the original diagonal stochastic model.

This substantially answers the v89 request for a genuinely broader additive quotient statement.

### 3.5 The literature positioning is now much more responsible

The v91 literature section explicitly separates:

- classical matrix-polynomial condition numbers;
- classical multiple-eigenvalue and Hoelder sensitivity;
- classical rational interpolation and realization;
- classical LAN/minimax theory;
- classical semialgebraic projection and Puiseux expansion;

from the observation-level pullback and the additive normalization gauge.

That is the right distinction. In particular, the paper no longer presents reciprocal multiplicity exponents, Laurent exclusion, triangular inverse expansions, or the Gram-matrix formula itself as new mathematics.

The bibliography now includes the principal conditioning references whose absence was a major concern in v89.

## 4. Status of the main v89 objections

My current assessment is:

| v89 issue | v91 status | Current assessment |
| --- | --- | --- |
| Global eta_d not an intrinsic sharp condition | Partly resolved | V_H is sharp on the regular quotient and omega_P is exact at arbitrary points, but there is still no theorem relating these objects into one model-specific condition theory |
| Local quotient theorem too compressed | Resolved in substance | The v90 analytic quotient theorem is now a credible proof |
| Conditioning literature inadequate | Resolved in substance | v91 directly positions the work against the relevant classical theory |
| Global observable proof transitions too compressed | Resolved in substance | v90 supplies the missing homotopy, degree, competitor and grouping lemmas |
| No genuinely broader additive noncommuting theorem | Substantially resolved | The common-flag theorem is meaningful, though not a general noncommutative classification |
| Singular mechanisms not unified | Reframed, not fully resolved | omega_P gives an exact variational modulus on every intersection, but not a model-specific singularity normal form or explicit invariant classification |

The final row is now the central editorial issue.

## 5. Major objection I: the arbitrary-point “intrinsic modulus” is exact but largely generic

The most important new v91 construction is

omega_P(t)
 = diam{Lambda(theta): h_w(F(theta),P) <= t}.

Theorem 10.1 then proves, at t_N = c/sqrt(N),

(3/32) omega_P(t_N)^2
 <= local minimax squared risk
 <= omega_P(t_N)^2.

I believe this theorem is essentially correct. The upper bound is the diameter bound for a constant local decision; the lower bound takes a diameter-attaining pair and uses Hellinger product control and a two-point test.

The issue is not correctness. The issue is mathematical content relative to the journal level being claimed.

Once the local experiment is defined as a shrinking metric ball and omega_P is defined to be the diameter of the target image of that same ball, a risk comparison by constant decision plus a two-point diameter pair is a general decision-theoretic device. It is not specific to projective polynomial observations. An analogous statement can be written for a very large class of compact statistical inverse problems.

Likewise, the statement that omega_P has a rational leading exponent follows because the closed model, the Hellinger constraints, and the bottleneck target are semialgebraic. Quantifier elimination makes the graph semialgebraic; one-variable semialgebraic functions have Puiseux-type leading behaviour.

This is mathematically clean, and it is useful as a universal envelope. But it should not be confused with a structural classification of this model's singularities.

The paper currently moves from a difficult unanswered question

“what happens when normalization failure, channel-rank loss, component-polynomial collisions and root multiplicities intersect?”

to the exact but implicit answer

“the answer is the diameter of all targets lying in a small observation ball, whose semialgebraic graph has some rational exponent.”

That is a valid characterization. It is not yet the model-specific theorem that the previous development suggests.

### What would change my assessment

The paper needs to compute or characterize omega_P in terms of intrinsic algebraic data on at least one genuinely intersecting singular family, not merely on the regular-normalization/full-rank multiplicity stratum.

For example, a leading-general-journal theorem could identify a finite collection of observable defect data and prove that they determine:

- the local exponent;
- the relevant tangent or arc cone;
- the leading modulus constant or its sharp variational representation;
- the transition laws when two singular mechanisms meet.

At present the exponent a_P exists and is “computable in principle” through quantifier elimination. That is not the same as understanding it.

## 6. Major objection II: v91 still does not compute the hard intersections

The paper correctly says that it is not claiming that kernel dimension, rank and multiplicity integers alone determine a_P. I agree with that caution.

But after this caution, the only explicit new calculation of the arbitrary-point modulus is the anchored multiplicity theorem, and that theorem assumes:

- strictly positive full-rank channels;
- strict weights;
- tau(P)>0;
- pairwise distinct complete component polynomials;
- roots in the interior.

Thus it intentionally excludes three of the most important singular mechanisms:

1. normalization-kernel enlargement;
2. channel-rank loss;
3. equality of complete component polynomials.

The theorem permits internal root multiplicity and cross-component scalar-root collision, but those are precisely the intersections for which the coefficient recovery remains regular.

Consequently the central “all intersections” theorem is still the implicit omega_P definition, while the explicit exponent calculation is carried out on a comparatively controlled singular stratum.

This is the main gap between “a complete framework” and “a complete singularity theory.”

### A particularly important missing test case

The manuscript should analyze at least one datum where tau=0 and a channel rank is simultaneously lost, or where tau=0 coincides with equality of complete component polynomials and an internal multiple root.

For such a point, the paper should determine the actual admissible-arc order from the model equations rather than invoking quantifier elimination abstractly.

Without such a computation, I cannot tell whether the proposed geometry reveals a new interaction law or merely packages the interaction into an optimization problem.

## 7. Major objection III: three condition objects coexist without a theorem relating them

The paper now contains three different conditioning objects:

1. eta_d(P), the global observable certificate on the regular recovered algebra;
2. V_H(P), the exact differential/Fisher object on the regular quotient;
3. omega_P(t), the arbitrary-point nonlinear Hellinger-ball target diameter.

Each is legitimate in its own regime.

The manuscript is also careful not to assert false equivalences among them.

But a leading structural paper should now explain how they fit together mathematically.

On the regular quotient, one expects omega_P(t) to have a linear first-order law determined by the appropriate metric version of V_H. The current manuscript proves the anchored simple-root exponent t and separately proves the V_H radial condition, but it does not formulate a theorem identifying the leading constant of omega_P(t) with the exact local metric condition, nor does it give a transition theorem from the regular differential object to singular Puiseux arcs.

Likewise, eta_d remains a global sufficient certificate rather than the sharp condition. The new omega_P construction does not establish a quantitative comparison between eta_d and the true global or local modulus.

This leaves the conceptual architecture as a stack of correct layers rather than one theorem.

### What is needed

At minimum I would want a theorem of the following type:

- on the regular quotient, omega_P(t)/t converges to an explicitly stated functional of V_H in the Hellinger metric;
- approaching a singular stratum, the breakdown of that linear law is described by a model-specific tangent/arc object;
- eta_d is compared quantitatively with that intrinsic modulus on a maximal natural class, with a precise statement of where equivalence fails.

The manuscript has essentially all the ingredients for the regular part. It has not yet assembled them into the promised intrinsic condition theory.

## 8. Major objection IV: the flag theorem is valuable, but its “noncommutative” reach should not be overstated

Theorem 7.1 genuinely allows noncommuting and defective coefficient matrices.

However, it requires a common complete invariant flag over C, equivalently simultaneous triangularizability of the recovered coefficient family.

That is a meaningful enlargement, but it is still a highly structured noncommutative class.

Moreover:

- B_triangle is an upper certificate;
- the flag-path exponent nu_Q is explicitly not asserted to be the minimal pole order;
- cancellations may improve the exponent;
- no matching lower theorem is given;
- the arbitrary competitor need not preserve the flag, but the true recovered algebra must.

Thus the theorem proves that the additive normalization principle survives one important nonsemisimple extension. It does not classify general noncommuting matrix-polynomial quotients.

The exposition is mostly honest about this. I recommend making the limitation even more visible in the abstract and introduction. “Noncommuting, defective coefficient algebras with an invariant flag” is correct. Any shorter phrase suggesting arbitrary noncommutative algebras would not be.

For the stated journal level, a substantially stronger result would identify when a structured normalization perturbation admits an additive decomposition without assuming simultaneous triangularizability, or else prove sharpness of the flag-path law on a natural class.

## 9. Major objection V: the anchored multiplicity theorem uses a recovery theorem outside its stated hypotheses

This is a concrete proof-writing issue, not merely an editorial one.

Theorem “Local quotient identification” defines its regular stratum using simple component roots.

The proof of Theorem “The anchored multiplicity exponent” then says:

> The analytic coefficient recovery in Theorem [quotient-chart] uses distinct complete polynomial tuples, not simplicity of their scalar roots. Apply its construction before root extraction, in ambient monic-coefficient coordinates.

I agree with the mathematical idea. The normalization and joint-projector recovery of component polynomial coefficients should continue to work at an internal repeated root, provided tau>0, channels remain full rank, and complete component polynomials remain distinct.

But the theorem being cited does not state that coefficient-level extension. Its parameter manifold and conclusion are formally restricted to the simple-root stratum.

At a repeated real root, the real-rooted coefficient set is itself singular/boundary-like; it is not the same open manifold used in the quotient theorem.

This should be repaired by isolating a separate proposition:

**Coefficient-level quotient recovery at repeated roots.**  
Under tau>0, full-rank positive channels, strict weights, and distinct complete component polynomial coefficient tuples, every nearby closed-model datum has a unique nearby component-coefficient representation modulo permutations, and that coefficient representation is the restriction of an ambient analytic recovery map. No simple-root assumption is required.

With that lemma in place, the anchored theorem becomes clean. In the current text, the proof relies on a true-looking fact that is not actually covered by the theorem cited.

I regard this as repairable, but a top-level submission should not leave it implicit.

## 10. Major objection VI: “computable in principle by quantifier elimination” is not a usable geometric classification

Corollary 10.2 states that, with real algebraic input, the exponent is computable in principle by quantifier elimination and one-variable algebraic branch analysis.

This is formally reasonable.

But the phrase risks overstating what has been achieved. Quantifier elimination is a universal existence algorithm for semialgebraic questions; it does not identify a tractable invariant of the observation model.

The paper explicitly disclaims a polynomial-time bound, which is good. I would go further and distinguish:

- effective decidability in real algebraic geometry;
- a closed-form or finite symbolic invariant specific to the model;
- a practically computable condition number.

Only the first has been established for arbitrary singular points.

At the four-leading-general-journal level, the interesting problem is not whether real algebraic geometry can in principle eliminate the latent variables. It is what the elimination means in the intrinsic algebra of this observation problem.

## 11. The local asymptotic minimax theorem: current assessment

I examined the new local theorem with particular care because it is one of the strongest claims in the paper.

### 11.1 LAN calculation

The categorical experiment has positive cell floors on the regular quotient. The score, information matrix and uniform bounded-local-parameter Taylor expansion are standard and correctly specialized.

The information matrix is

I = J^T H_{P,w} J.

Since J has full column rank and H is positive on the simplex tangent space, I is positive definite.

### 11.2 Efficient local estimator

The minimum-distance argument gives the expected first-order expansion. The manuscript supplies the missing moment control needed for squared sup-norm risk, including the fallback event.

I have no major objection to this part.

### 11.3 Collisions and the Gaussian quotient

The finite-permutation quotient is the right object at cross-component scalar-root collisions.

The translation argument in the Gaussian location experiment is clever: finite priors can be shifted so that the coordinate ranges within each collision block become disjoint in a fixed order, after which quotient loss equals labelled sup-norm loss.

Because the local minimax theorem takes R to infinity only after N to infinity, each finite translated prior is admissible at some finite R. This avoids an apparent conflict between a large Gaussian translation and the local parameterization.

I therefore regard the equality with E||N(0,V)||_infinity^2 as plausible and substantially justified.

This is one of the strongest pieces of v91 and should be foregrounded more than the generic semialgebraic modulus theorem.

## 12. The arbitrary-point minimax theorem: technical comments

Although I consider its novelty limited, the theorem itself is mostly clean.

### 12.1 Zero cells

Using Hellinger rather than KL is the correct choice at arbitrary closed-model points. The two-point proof avoids likelihood-ratio denominators and therefore survives zero cells.

### 12.2 Product Hellinger bound

With n_j/N <= 2w_j eventually and a pair lying in the same t_N ball,

h_w(F(theta),F(theta')) <= 2t_N.

This gives the stated 8Nt_N^2 product bound. The chosen constant c ensures the total variation bound required for the testing constant.

### 12.3 Exact fibre diameter

The distinction between omega_P(0)=0 and omega_P(0)>0 is essential. If the exact fibre has multiple spectral targets, no shrinking observation neighbourhood can remove that nonidentifiability. The theorem captures this correctly.

### 12.4 Puiseux exponent

The semialgebraic argument is appropriate because all clock denominators are uniformly positive, the root/stochastic parameter constraints are polynomial, square roots can be introduced as nonnegative auxiliary variables, and bottleneck matching is a finite minimum over permutations.

I do not object to the rational-exponent existence statement.

My objection is only that this is a generic semialgebraic envelope, not yet a structural solution of the specific singularity problem.

## 13. Anchored versus moving multiplicity rates

The paper's distinction here is important and, in my view, correct.

For a fixed real-rooted polynomial with a multiple root, coefficient perturbations constrained to remain real-rooted cannot move an anchored multiple root by the unrestricted complex 1/m law. The sum-of-squares identity forces an O(sqrt(epsilon)) root displacement, and splitting two copies symmetrically realizes that exponent.

By contrast, the fixed-neighbourhood minimax theorem compares two moving alternatives whose mutual coefficient separation is order u^m while each may sit order u^2 away from the multiple-root base. For m>2, those alternatives do not fit in an N^{-1/2} shrinking observation ball around the base at the scale used by the moving-pair lower bound.

This resolves an apparent contradiction between N^{-1/2} anchored squared-risk order and N^{-1/m} fixed-neighbourhood squared-risk order.

This is a good piece of the revision.

The remaining issue is that it computes one singular face after excluding the normalization and rank singularities.

## 14. Global observable conditioning: current status

The eta_d theorem remains a useful result.

The complete-polynomial joint projectors are the right decomposition. In particular, scalar roots shared by different component polynomials should not force a split of the resolvent residue at the root level.

The additive quantity

B_d + tau^{-1}

captures the central mechanism of the paper: the scalar normalization error is treated before the arbitrary matrix error, so it is not multiplied by a second latent-channel condition loss.

The v90 technical lemmas now make the global proof substantially more convincing.

However, eta_d is still not shown to be the intrinsic sharp condition of the inverse problem. The paper now has V_H and omega_P for sharp local statements instead. That is a perfectly acceptable mathematical architecture for a specialist paper, but the title and broad “intrinsic geometry” narrative should not imply that eta_d itself has acquired a two-sided optimality theorem.

## 15. Clock complexity

The distinction between the 2d+1 worst-case clock count and the d+2 full-span count remains valuable.

The paper correctly avoids claiming a complete classification for intermediate functional span.

I would retain the endpoint results, but I would not make “sharp clock counts” sound universal unless the introduction explicitly says “sharp in the stated worst-case and full-span endpoint classes.”

## 16. Editorial novelty after the v91 repairs

At this stage the manuscript has several good theorems. The editorial question is no longer whether there is enough mathematics for publication somewhere. There is.

The question is whether the contribution has the structural finality and breadth expected of one of the four leading general mathematics journals.

My current decomposition is:

### Clearly observation-specific and potentially novel

- the scalar-normalization recovery problem from probability observations;
- the complete-polynomial joint-projector gauge;
- the additive separation of normalization and arbitrary matrix perturbation;
- the extension of that additive separation to common-flag noncommuting algebras;
- the exact quotient/Fisher treatment of the unordered spectral target in this controlled categorical experiment.

### Largely classical once the observation map is fixed

- polynomial resolvent exclusion;
- argument-principle root counting;
- Hoelder root sensitivity at multiplicities;
- Gram-matrix differential condition formulas;
- LAN and local asymptotic minimax transfer;
- two-point testing;
- semialgebraic quantifier elimination and Puiseux exponents.

The paper is strongest when it proves a new structural fact about how projective normalization interacts with the recovered coefficient algebra.

It is weakest when generic mathematical machinery is presented as if it completes the singular geometry.

A successful leading-general-journal version should deepen the former rather than continue adding layers of the latter.

## 17. A concrete route that could materially change the recommendation

I would not recommend another revision whose main addition is a further general-purpose modulus definition, a larger diagnostic script, or another isolated singular regime.

A materially different version should prove one of the following.

### 17.1 Model-specific singular normal form

At a nontrivial intersection involving at least two of:

- normalization kernel;
- rank defect;
- equality of complete component polynomials;
- internal multiplicity;
- cross-component collision;

derive a local normal form of the observation map modulo the component permutation action and compute omega_P(t) from that normal form.

### 17.2 Observable arc invariant

Replace “quantifier elimination computes a_P in principle” by an explicit finite invariant or optimization over algebraic data recoverable from P, and prove that this invariant equals the admissible-arc exponent.

### 17.3 Sharp common-flag theory

For the noncommuting flag theorem, prove matching lower constructions showing when the path exponent nu_Q is sharp, characterize cancellations that reduce it, and relate the result to the arbitrary-point observation modulus.

### 17.4 A bridge theorem among eta_d, V_H and omega_P

Prove the regular first-order expansion of omega_P in terms of V_H and a precise degeneration theorem explaining how it transitions to fractional powers at singular points. Quantify how eta_d bounds or fails to bound that intrinsic modulus.

Any one of these would make the paper much more structurally complete.

## 18. Concrete reproducibility defect at the reviewed head

The branch contains:

revisions/a2-v91/verify_a2_v91.py

The program says it can be run as a finite diagnostic and source audit. In source_audit it executes:

manifest_path = Path(__file__).with_name("SOURCE_MANIFEST.json")
manifest = json.loads(manifest_path.read_text())

But the directory revisions/a2-v91 at the reviewed branch head contains only verify_a2_v91.py.

There is no SOURCE_MANIFEST.json at that path.

Therefore the committed verifier fails on the source-audit path before it can produce its advertised result.

This is not a hypothetical concern and does not require a numerical disagreement: the required file is absent from the exact reviewed tree.

The branch-head commit message is “A2 v91: add executable source, quotient Fisher, flag and singular-rate diagnostics,” so the inconsistency is particularly unfortunate.

I also found no GitHub Actions workflow run associated with the exact reviewed head SHA.

### Required repository correction

Either:

1. commit the manifest with the exact active-source SHA256 values and inherited Git blob identities expected by the script; or
2. remove the manifest dependency and make the script derive/check the source inventory in a self-contained way.

Then run the script from a clean checkout and record the output generated from the pinned head.

The diagnostic program correctly states that it is not a formal proof checker. That qualification should remain.

## 19. Smaller mathematical and expository comments

### 19.1 State the coefficient-level repeated-root recovery theorem separately

Do not make Theorem “anchored multiplicity exponent” rely on an extension of Theorem “local quotient identification” that is only described inside the proof.

### 19.2 Separate three meanings of “intrinsic”

The paper uses “intrinsic” for:

- representation-free observability;
- quotient-coordinate invariance;
- an exact decision-theoretic modulus.

These are related but not identical. Define them once and use the term more sparingly.

### 19.3 Avoid presenting the variational definition as a closed-form solution

omega_P is an excellent organizing object. It is not itself an explicit answer to the singular geometry.

### 19.4 Clarify the scope of “global”

The eta_d estimate is global against all closed-model competitors from a fixed regular true datum. The arbitrary-point omega theorem is local in a shrinking observation neighbourhood. These are different uses of “global” and “local.”

### 19.5 Keep the exact arithmetic qualification

The direct estimator remains an exact-arithmetic stability construction. Nothing in v91 turns it into a finite-precision complexity theorem.

### 19.6 Keep the confidence-set computational qualification

The whole-model confidence set is information-theoretic. Its definition does not by itself provide an efficient global optimizer over the latent closed model.

### 19.7 The title is defensible, but the abstract should distinguish theorem types

The current title is better than earlier versions. In the abstract, however, I would distinguish:

- exact regular-quotient geometry;
- implicit arbitrary-singular-point modulus;
- explicit anchored multiplicity computation.

That distinction would reduce the risk that a reader interprets the Puiseux existence theorem as a complete explicit singular classification.

## 20. What I would regard as publishable now

Ignoring the stated top-four target, I regard the present manuscript as having a serious publishable mathematical core after repairs.

A strong specialist version could be built around:

1. normalization identification and clock complexity;
2. observable joint-projector additive inverse stability;
3. the exact regular quotient and local Fisher/minimax geometry;
4. the common-flag noncommuting extension;
5. selected singular minimax regimes.

For that purpose, the generic arbitrary-point modulus could be presented as a useful closure theorem rather than the culmination of the paper.

At the much higher stated general-journal level, the manuscript still needs a theorem that explains the singular geometry rather than merely defining its optimal modulus.

## 21. Final assessment

Revision 91 is the strongest A2 version I have reviewed.

The previous report's central technical criticisms have, to a substantial extent, been answered. The quotient theorem is now explicit; the local minimax constant is genuinely sharp; the global inverse proof has the missing quantitative lemmas; the conditioning literature is treated responsibly; and the additive mechanism now survives an important noncommuting defective common-flag extension.

I therefore do **not** reject v91 because it is technically unfinished in the same way as v89.

I reject it at the stated four-leading-general-mathematics-journal level because the final “arbitrary singularity” layer remains implicit and generic. The model-specific hard problem has been encoded into omega_P and its semialgebraic arc minimization rather than solved in terms of the algebraic and statistical defects that make this observation model distinctive.

The paper now shows that an exact modulus exists everywhere and that its exponent is rational. It does not yet show what that exponent is, or why, at the genuinely difficult intersections of the normalization, rank, component-equality and multiplicity singularities.

That is the remaining structural theorem I would require before reconsidering the manuscript at the stated level.

The broken v91 source-audit manifest should also be corrected immediately, but it is secondary to the mathematical recommendation.

---

*This is an owner-requested independent external-referee-style assessment of the repository manuscript. It is not a journal-commissioned report and does not represent an editorial decision.*