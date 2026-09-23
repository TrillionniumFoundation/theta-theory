# Independent External Harsh Referee Report

## General Theta Foundations I: Adaptive Testing and Collision-Sensitive Comparison — Revision v17

**Author:** Qian Qi  
**Repository:** TrillionniumFoundation/theta-theory  
**Reviewed branch:** revision/general-theta-foundations-i-v17-intrinsic-adaptive-testing-referee-ready-2026-09-23  
**Canonical article:** 59 pages  
**Canonical mathematical source identity:** f93ab1a6c8c5255a3398f1884c5af05d65ced73a  
**Final PDF/evidence publication identity:** 978800e2f1d8678291d7a4b1f0dcc4396235f8b5  
**Immediate predecessor reviewed:** v16, revision/general-theta-foundations-i-v16-constructive-causal-certification-referee-ready-2026-09-23  
**Controlling predecessor report:** b59d8527c8edc0361be3085604bcf3a920dbfbda, report blob e5da7aad09a5a5df84b16d6e8daa76e5dc7054c0  
**Review date:** 23 September 2026  
**Requested standard:** Annals of Mathematics / Inventiones Mathematicae / Journal of the AMS / Acta Mathematica level  
**Review type:** independent, external-referee-style, pipeline-aware harsh audit

**Provenance note.** This is an owner-requested, AI-assisted external-referee-style report, not a report commissioned by a journal. I reviewed the frozen v17 canonical source, the three principal new theorem modules, the response/proof/history ledgers, the exact-certificate and build records, the clean-source architecture, the predecessor v16 reports, the typed eleven-component dependency graph, and the historical B4 and C2 closure sources to which the manuscript itself points. I also independently recomputed the central rational polynomial identity in the three-weight certificate and the decisive rational inequalities in the two-sphere collision construction. Repository checks and executable diagnostics were treated as reproducibility evidence, not as substitutes for mathematical proof.

---

# Recommendation

## Reject in the present form at the requested top-four general-mathematics standard

This is a substantially stronger manuscript than v16. Several objections in the previous report have been answered in the literal and mathematically meaningful sense. In particular:

- the old row-dependent polynomial transform is no longer presented as the only “dual” object;
- the paper now defines an independently feasible adaptive-test class on the original nonconvex behavior image;
- an existence-size theorem is stated in observable behavior dimension rather than raw simulator-row dimension;
- the strict-margin boundary is stated correctly;
- a genuine private/hidden/visible separation is realized in one physical model;
- the informative physical signal is genuinely created by a collision and vanishes when that collision is removed;
- the effective-enumeration quantifiers are now explicit;
- the canonical submission is a clean self-contained source tree rather than a journal object assembled transitively across historical revision directories;
- the manuscript now proves a whole-process posterior stability theorem and a microscopic Gaussian-observation sufficient condition instead of merely invoking a finite-dimensional/tightness heuristic.

These are real improvements. I do not find a simple fatal algebraic error in the three principal new theorem groups I checked.

The top-four obstacle has therefore moved. It is no longer primarily one of correctness or presentation. It is one of mathematical depth, nontriviality, and program-level significance.

The new adaptive “duality” is correct, but once the verifier is allowed to evaluate a pre-chosen function at the fully revealed candidate behavior, the infinite-dimensional variational identity becomes nearly tautological: a partition of unity approximates the pointwise maximum, and the probability-measure side reduces to minimizing the integral of that maximum, attained by a point mass. The finite-level theorem is then a clean Bernstein/binomial approximation plus a Carathéodory moment-support reduction. This is useful, but it is not yet a structural duality theory of finite-memory causal behavior.

The new hard-sphere theorem is genuinely collision-sensitive, but it is a deliberately engineered two-particle, one-collision transducer of a pre-planted binary mark/report correlation. It closes the predecessor's literal “interaction-sensitive example” objection, but it does not reach the particle-uniform, recollision, kinetic-scaling, or nonlinear-semigroup difficulty that the repository's own B4 program declares as the hard downstream gate.

The new optional-projection theorem is also correct in spirit and useful, but its mechanism is marked total variation plus Bayes' formula, maximal inequalities, maximal coupling, Girsanov/KL and Pinsker. It assumes a common latent marginal and, in the physical specialization, changes the observation function while keeping the microscopic flow and latent state on one fixed probability space. This is far from the repository's historical C2 theorem on changing microscopic paths, likelihood processes, limiting stochastic exponentials, Girsanov/BSDE limits, strict duality, form response, memory response, and rigidity.

Finally, the nearest filtered-comparison priority boundary, Norberg (2002), remains explicitly unresolved at proof level. The manuscript is commendably honest about this, but honesty does not remove the publication-level novelty uncertainty.

My assessment is therefore not “another minor revision.” The paper now needs one theorem of substantially greater structural force: either a genuinely nontrivial resource-sensitive separation/duality/classification theorem, or a physical/downstream theorem that survives a hard scaling limit and actually discharges one of the declared B4/C2 gates.

---

# 1. Exact mathematical delta from v16

The v17 revision adds three principal mathematical packages.

## 1.1 Independent adaptive testing on the nonconvex behavior image

The new section adaptive-testing.tex works with a compact behavior image \(B\), affine discrepancies \(f_1,\ldots,f_m\), and
\[
F(b)=\max_i f_i(b),\qquad \delta=\min_{b\in B}F(b).
\]
An adaptive test is a continuous function
\[
\kappa:B\to\Delta_m
\]
chosen before the candidate \(b\), but evaluated after that candidate behavior is revealed. Its score is
\[
G(b,\kappa)=\sum_i\kappa_i(b)f_i(b).
\]

Theorem v17-dual proves
\[
\delta
=\sup_{\kappa\in C(B,\Delta_m)}\min_{b\in B}G(b,\kappa)
=\min_{\mu\in\mathcal P(B)}\sup_{\kappa}
\int_B G(b,\kappa)\,d\mu(b).
\]

Theorem v17-degree then chooses a bounded observable chart of affine dimension \(a\) and diameter \(R\), introduces tensor Bernstein tests of coordinatewise degree \(n\), and obtains
\[
0\le \delta-d_n\le {4Ra\over\sqrt n},
\]
with at most \((n+1)^a\) occupied test coefficients and an attained moment-dual minimizer supported on at most \((n+2)^a\) points.

The section also gives a small explicit three-weight nonlinear certificate for the private two-report example.

## 1.2 Collision-sensitive marked resource separation

The new finite reference experiment correlates a binary actual mark \(W\) and a binary report variable \(B\), uses a later gate \(A\), and proves at width \((1,1)\)
\[
\delta^{\rm p}=\delta^{\rm v}_r
=\sqrt{5/2}-{9\over8},
\qquad
\delta^{\rm h}_2={1\over8}.
\]

A full-dimensional two-sphere preparation then encodes \(B\) in the impact orientation and \(W\) in a conserved longitudinal mode. For \(d\in[9/10,11/10]\), one nongrazing collision produces a transverse tagged-velocity signal; for \(d\le2/5\), no such collision occurs during acquisition. Gaussian threshold reports transfer the finite marked separation to the physical model with error below \(1/300\).

## 1.3 Whole-process optional-projection stability

For equivalent joint laws \(P,Q\) with the same latent marginal, Theorem v17-optional controls
\[
E_Q\sup_{t\le T}|M_t^P-M_t^Q|^2
\]
by a constant times \(\|P-Q\|_{\rm TV}\), and constructs a latent-preserving maximal coupling with a corresponding whole-process estimate.

The physical specialization observes the same invariant hard-sphere flow through
\[
Y_t=\int_0^t h(\Phi_s Z)\,ds+\sigma B_t
\]
and approximants \(h_n\). Girsanov/KL plus Pinsker gives joint total-variation convergence from \(L^2(\mu)\) approximation of \(h\), hence whole-time convergence of optional projections.

These additions are real. The question is whether their structural content is commensurate with the requested venue and with the title “General Theta Foundations I.”

---

# 2. Status of the major v16 objections

It is important not to recycle the predecessor report mechanically. My assessment of the old blockers is as follows.

| Predecessor issue | v17 status |
|---|---|
| E16-R2.1: subtract the nearest polynomial-positivity literature | **Substantially addressed.** The paper now names and distinguishes de Klerk–Laurent, Laurent–Slot and de Klerk–Vera and does not claim generic Bernstein/Positivstellensatz technology as new. |
| E16-R2.2: either stop calling the row hierarchy a dual or construct an independent variational object | **Formally addressed, but replaced by a new significance problem.** The new adaptive class is independently feasible; however the resulting infinite-dimensional identity is much less nontrivial than the word “duality” suggests. |
| E16-R2.3: intrinsic certificate complexity | **Partially addressed.** There is now an intrinsic behavior-dimension existence-size bound for adaptive tests and moment support. There is still no intrinsic bound for finding the chart, describing/minimizing over the nonconvex feasible set, rational bit complexity, or verification cost. |
| E16-R2.4: strict-margin boundary | **Addressed.** The manuscript now clearly separates strict Bernstein certificates, Borel attainment, continuous suprema, finite-level attainment, and exact semialgebraic boundary decision. |
| E16-R2.5: genuine private/hidden/visible physical separation | **Addressed at fixed finite-particle scale.** The new marked scattering example separates the signatures. |
| E16-R2.6: make the physical observable interaction-sensitive | **Addressed literally.** Removing the collision removes the information and the deficiency gap. |
| E16-R2.7: isolate what is inherited from v15/v16 | **Addressed.** The submission now states that the stateless physical transfer principle is inherited and identifies the new modules. |
| E16-R2.8: effective quantifiers | **Addressed.** The uniform algorithmic inputs are stated explicitly. |
| E16-R2.9: close one hard downstream theorem or narrow the foundational claim | **Not closed.** v17 supplies one scoped sufficient C2 input, not a historical C2 closure; B4 remains fully open at the hard kinetic level. |
| E16-R2.10: proof-level Norberg crosswalk | **Open by the authors' own statement.** |

Thus v17 deserves credit: it has genuinely moved the paper. The remaining rejection is not justified by pretending those improvements do not exist.

---

# 3. The new “adaptive testing duality” is correct but structurally close to a tautology

This is now the central conceptual issue.

The manuscript's test class is extremely rich:
\[
\kappa\in C(B,\Delta_m).
\]
Although \(\kappa\) is “chosen before” the candidate, its value is evaluated at the fully revealed candidate \(b\). Therefore the verifier can pre-program an approximate pointwise argmax rule.

The proof of Theorem v17-dual is exactly this observation. The open sets
\[
U_i=\{b:f_i(b)>F(b)-\eta\}
\]
cover \(B\). A partition of unity subordinate to this cover produces a continuous \(\kappa\) satisfying
\[
F(b)-\eta<G(b,\kappa)\le F(b).
\]
Hence the first equality follows.

The second equality is even more revealing:
\[
\sup_\kappa\int G(b,\kappa)\,d\mu(b)
=\int F(b)\,d\mu(b).
\]
Therefore
\[
\min_{\mu\in\mathcal P(B)}
\sup_\kappa\int G\,d\mu
=
\min_{\mu\in\mathcal P(B)}
\int F\,d\mu
=
\min_{b\in B}F(b),
\]
and the minimizer may simply be a point mass at a minimizer of \(F\).

This theorem is valid. But it does not expose a hidden dual geometry of the causal-resource set. It works for an arbitrary compact set \(B\), and the affine structure of the \(f_i\) is not needed for the partition-of-unity identity itself. The nonconvexity of \(B\) does not become tractable through a new separation theorem; instead the verifier is strengthened so that it can adapt its mixture of tests to the revealed candidate law.

That is a legitimate verification game. It is not, in my view, yet a top-four-level duality theorem.

The phrase “independent adaptive testing duality” risks overstating what is happening. The test is independent of the simulator's randomization in the sense relevant to the paper, but its evaluation has full candidate-behavior access. Once that access is granted, pointwise selection is the whole mechanism.

A genuinely structural result would constrain the verifier in a way that makes the dual class itself nontrivial: for example, finite-memory/causal information constraints on the tester, restricted observation of the behavior, a universal continuation-state condition, a norm-dual characterization of the nonconvex behavior image, or a separation theorem whose feasibility does not collapse to pointwise argmax after full law revelation.

At minimum the exposition should make the mathematical strength of the information convention unmistakable. At the requested venue, I would prefer a title such as “revealed-behavior adaptive-test representation” unless a genuinely nontrivial resource-sensitive dual object is added.

---

# 4. The behavior-dimension theorem is a clean approximation theorem, not yet an intrinsic complexity theory

Theorem v17-degree is the strongest genuinely quantitative new finite statement, and I believe the displayed rate is supported by the proof.

The chart gives
\[
|\ell_i(x)-\ell_i(y)|
\le 4R\sum_j|x_j-y_j|.
\]
Choosing at each Bernstein grid point \(\alpha/n\) an index maximizing \(\ell_i\), and writing \(A_j\sim{\rm Bin}(n,x_j)\), gives the standard regret estimate
\[
\max_i\ell_i(x)-E\ell_{i_A}(x)
\le
8R\sum_jE|A_j/n-x_j|
\le {4Ra\over\sqrt n}.
\]
The support bound on the moment side then follows by preserving monomials of coordinatewise degree at most \(n+1\) and applying Carathéodory.

This is a useful and correctly scoped theorem. It fixes a genuine weakness in v16: the existence size is controlled by observable behavior dimension rather than by all stochastic row coordinates.

But the manuscript itself correctly admits what the theorem does not control:

- it does not give the cost of finding the chart;
- it does not bound rational chart bit length;
- it does not give the complexity of describing the nonconvex feasible set \(C\);
- it does not bound the cost of computing \(\min_C\) of the resulting score;
- it does not give intrinsic coefficient-bit complexity for a strict positivity certificate;
- it does not produce a polynomial-time algorithm;
- it does not establish lower bounds or sharpness of the \((n+1)^a\) or \(4Ra/\sqrt n\) dependence.

These are not peripheral omissions. They are exactly where “intrinsic constructive theory” would become structurally strong.

The current theorem says, roughly: if one measures the behavior image in its observable quotient, then a pointwise best-test rule can be approximated by a Bernstein-smoothed selector with the usual binomial concentration rate. That is a clean approximation statement. Its ingredients are classical and transparent.

To reach the level suggested by the paper's framing, one would want at least one of the following:

1. a lower bound showing that a dependence of order \(\varepsilon^{-2}\), exponential in behavior dimension, or some width-dependent analogue is unavoidable;
2. a sharp support theorem tied to the causal state complexity of the simulator rather than merely to a polynomial moment dimension;
3. an intrinsic bit-complexity theorem for rational finite experiments;
4. a classification of when finite-width behavior images admit bounded-degree nonlinear separators;
5. an equivalence between positive deficiency, approximate causal congruence, and a finite-state/continuation-state invariant;
6. a complexity dichotomy in horizon, width, or behavior dimension.

Without such a result, the new theorem is informative but not yet a new architecture of the subject.

---

# 5. The small three-weight certificate is exact and useful, but it is a witness, not the missing structural theorem

I independently checked the main algebra behind Proposition v17-smallcertificate.

With
\[
u=pq,\qquad v=(1-p)(1-q),\qquad
J(t)=3t^2-2t^3,
\]
the proposed weights are feasible. After the change of variables
\[
a=(p+q-1)^2,\qquad b=(p-q)^2,
\]
the deposited polynomial identity for \(64G\) is exact.

The derivative decomposition
\[
16\,\partial_bG
=
4a^3+6a^2c+12ab^2+24abc+12ac^2
+8b^3+30b^2c+30bc^2+9c^3,
\quad c=1-a-b,
\]
is also exact and nonnegative on the simplex.

The listed seventeen degree-16 Bernstein coefficients reconstruct the univariate polynomial exactly, and their minimum is indeed
\[
{351\over349440}={9\over8960}.
\]

This is good exact mathematics and good reproducibility practice. It also makes the failure of constant tests vivid.

But this proposition cannot carry the significance burden of the paper. It demonstrates existence of a small nonlinear witness for one two-bit example. It does not characterize the geometry of the general resource image, determine a minimal test degree, prove a lower bound, or identify a canonical finite-memory invariant.

The paper should preserve the example, but not confuse its exactness with structural depth.

---

# 6. The collision theorem is a genuine correction to v16, but it remains a two-particle finite-experiment embedding

I regard the new collision section as mathematically much better than the v16 collective-mode example.

The physical signal is now genuinely produced by collision geometry. The proof establishes a uniform first collision for \(d\in[9/10,11/10]\), controls the impact normal, and obtains a transverse tagged-velocity margin. In the small-diameter regime \(d\le2/5\), the same preparation and detector remain collision-free during acquisition and the signal disappears.

The key rational estimate is nontrivial but elementary. In particular,
\[
-{3\over200}
+{1443\over1000}{87\over220}
> {1\over2},
\]
as required for the transverse velocity bound.

The resulting physical deficiencies really do separate:
\[
\delta^{\rm p},\delta^{\rm v}>9/20,
\qquad
\delta^{\rm h}_2<13/100,
\]
for the stated noise and diameter interval. This answers the predecessor's literal objection that the physical model did not use the private/hidden/visible architecture.

However, one must be precise about what the collision is doing.

The binary correlation between \(B\) and the actual mark \(W\) is already planted in the preparation:
\[
P(B=b,W=w)=5/16 \text{ or } 3/16.
\]
The mark \(W\) is encoded in the longitudinal center-of-mass velocity. The bit \(B\) is encoded in the impact orientation. The collision then transduces \(B\) into an observable transverse tagged velocity. It does not generate the \(B\)-\(W\) correlation.

Likewise, the hidden-selector advantage is already the finite-information phenomenon of retaining one hidden persistent bit across two reports. The physical mechanics provide a realization of the finite marked experiment; they do not generate a new many-body memory law.

This distinction matters for significance.

The theorem uses:

- exactly two labeled spheres;
- one isolated nongrazing collision;
- no recollision chain;
- no particle-number-uniform estimate;
- no Boltzmann–Grad regime;
- no kinetic scaling;
- no singular many-body limit;
- no feedback force on the mechanics;
- a gate that only suppresses or exposes a later sensor;
- a threshold detector designed around a robust post-collision sign.

The geometric-similarity statement rescales a solved two-body configuration. It is not an asymptotic physical scaling theorem.

Therefore I would describe v17 as proving a **collision-sensitive physical realization of a finite causal resource gap**. That is a meaningful theorem. I would not describe it as a hard microscopic-to-macroscopic bridge.

A top-four Route-B theorem would need something qualitatively stronger: a resource separation stable as particle number grows, a collision-network or recollision phenomenon, a Boltzmann–Grad/kinetic limit, or a theorem that supplies a genuine hypothesis of the declared B4 nonlinear semigroup program.

---

# 7. The optional-projection theorem is useful, but the historical C2 gap remains large

The optional-stability section is also a real improvement.

Under equivalent joint laws \(P,Q\) with the same latent marginal, the proof writes
\[
D={dP\over dQ},\qquad
D_t=E_Q[D\mid\mathcal F_t^Y],
\]
and uses Bayes' formula to express the difference of posterior martingales through the martingales
\[
A_t=E_Q[(D-1)f\mid\mathcal F_t^Y],
\qquad
B_t=D_t-1.
\]
Weak \(L^1\) maximal inequalities give a tail bound, which integrates to the constant \(80\). Conditional maximal coupling over the common latent variable adds the disagreement contribution and yields \(84\).

The microscopic specialization is equally transparent. Conditional on \(Z\), the two observation laws differ only in deterministic Brownian drifts. Therefore
\[
D_{\rm KL}(P_n\|P)
=
{1\over2\sigma^2}
E_\nu\int_0^T|(h_n-h)(\Phi_sZ)|^2\,ds,
\]
and invariance plus \(d\nu/d\mu\le C\) gives the claimed \(L^2\)-to-TV estimate by Pinsker. The graph-core approximation is supplied by orbit mollification.

I find this argument mathematically plausible and appropriately caveated.

But it does not close the hard C2 theorem described elsewhere in this same repository.

The historical C2 Round-17 source asks, among other things, for:

- weighted strict duality;
- covariant type-(B) resolvent response under a varying Hilbert/form realization;
- dissipative compressed resolvent and memory response;
- model-specific rigidity;
- convergence of changing microscopic paths and likelihood ratios;
- identification of the limiting projected likelihood as a stochastic exponential;
- compatibility with Girsanov and bounded risk-sensitive BSDE representations.

V17 proves something narrower:

- one common latent state \(Z\);
- one fixed microscopic flow \(\Phi_t\);
- observation functions \(h_n\to h\);
- Gaussian observation noise;
- joint total variation on the latent-output law;
- whole-process posterior convergence under that strong joint-law control.

In particular, it does not prove convergence of a changing microscopic path \(X^\varepsilon\), a changing likelihood process \(L^\varepsilon\), or a limiting BSDE representation. It changes the sensor observable while holding the latent dynamics fixed.

This is a legitimate sufficient input for one piece of C2. The pipeline graph correctly records it as such. It is not the hard C2 closure.

The manuscript should resist any rhetoric suggesting otherwise. Its own current wording is mostly disciplined; the publication-level issue is that the resulting theorem is still too far from the programmatic burden attached to “Foundations.”

---

# 8. Pipeline audit: GTF-I remains an interface/certification layer, not yet the theorem-generating foundation of the eleven-paper chain

The typed pipeline graph is unusually useful here because it prevents rhetorical overreach.

The eleven components remain A1, A2, A3, A4, B1, B2, B3, B4, C1, C2, D1. Every recorded field of the form
\[
\text{full historical target closed by v17}
\]
remains false.

That is the correct metadata state.

The B4 historical source is especially revealing. Its Round-17 closure contains, among other things:

- an exact law–hierarchy realization;
- a dynamic collision action;
- state-dependent control transfer;
- compact dynamic-action sublevels;
- a kinetic Nisio semigroup;
- a nonlinear resolvent;
- full range and \(m\)-dissipativity;
- comparison;
- one action-sublevel graph-core hierarchy corrector sequence;
- nonlinear Trotter–Kato/kinetic convergence.

The new v17 physical theorem supplies none of these hard nonlinear scaling objects. It supplies a fixed two-particle acquisition consumer with a collision-sensitive finite signal.

Likewise, the C2 historical source contains a strict-duality theorem, covariant form response, compressed-memory response, rigidity, and a changing-filtration path/likelihood theorem. V17 supplies one sufficient optional-projection edge under stronger, more concrete assumptions.

The paper is therefore best understood as:

> a finite-resource comparison and certification interface that can consume model-specific analytic inputs while preserving declared state/randomization budgets, now augmented with one intrinsic test-size theorem, one collision-sensitive finite-particle realization, and one posterior-stability criterion.

That is a coherent research contribution.

It is still not:

> a first-principles theorem from which the hard A/B/C/D mathematical chain follows.

This distinction is not a demand that Paper I literally prove all ten later papers. A foundational first paper need not close every downstream theorem. But at top-four level it should introduce a principle whose downstream leverage is mathematically deep enough to reorganize those problems. The current pipeline remains mostly a typed interface graph: it records where model-specific results may plug in, while the difficult results themselves remain independent.

The graph checker is honest that it verifies source identity and declared contracts rather than analytic truth. That disclaimer should remain prominent.

---

# 9. The nearest filtered-comparison priority boundary is still unresolved

The manuscript's literature section has improved materially. It now makes theorem-level comparisons with nearby positivity results and gives a precise comparison with Weisshaupt's adapted stochastic-operator framework.

However, the Norberg issue remains open by the authors' own explicit statement.

Norberg, “Comparison of Statistical Experiments with Filtered Probability Spaces,” Statistics & Risk Modeling 20 (2002), 1–28, DOI 10.1524/strm.2002.20.14.1, is not a remote citation. Its published description places it directly in sequential comparison of stochastic-process experiments with successive actions and risk-comparison criteria.

The unresolved questions identified in the manuscript are exactly the right ones:

1. What is Norberg's exact filtered deficiency?
2. What randomization/adapted operators are admissible?
3. What persistent information may they retain?
4. What is free and what is charged?
5. How are actions timed relative to observations?
6. What risk criteria are equivalent?
7. Can finite private/hidden/visible state constraints be inserted into that framework?
8. Which present theorem remains genuinely new after that insertion is analyzed?

Until the original proof-level text is compared definition-by-definition and theorem-by-theorem, the paper cannot close the most direct historical priority boundary around its conceptual core.

I do **not** infer from the missing crosswalk that Norberg already contains the present theorem. That would be unjustified. The point is the opposite: the current submission itself does not yet know enough to make the strongest novelty judgment.

The Paull–Unger/state-minimization original-text audit also remains incomplete, although that issue is less central than Norberg for this paper.

For a top-four submission, the nearest priority boundary cannot remain explicitly unresolved.

---

# 10. The clean journal architecture is now substantially fixed

One major predecessor objection should be retired.

The v17 canonical article now has a self-contained local TeX source tree. The 256-page complete-development object is explicitly archival, not something a journal referee must read to understand the 59-page canonical article. The submission source ZIP compiles without traversing historical revision directories.

This is a real improvement.

The repository still contains extensive provenance, manifests, build receipts, source closures, negative controls, and historical preservation machinery. That is acceptable as research infrastructure so long as the journal article itself does not require repository archaeology to identify its theorem spine.

The current v17 architecture largely satisfies that requirement.

I would still encourage a conventional submission version to reduce the amount of repository/history language in the mathematical narrative, but this is no longer a blocking objection.

---

# 11. Reproducibility is excellent; it does not change the significance judgment

The deposited evidence is unusually careful:

- exact rational coefficients;
- explicit negative controls;
- source hashes;
- clean-source compilation;
- predecessor-diagnostic reruns;
- source-bound build receipts;
- page/render checks;
- physical error enclosures;
- preservation maps;
- typed dependency records.

This deserves credit.

But none of the following implications is valid:

- many exact checks \(\Rightarrow\) deep theorem;
- clean source provenance \(\Rightarrow\) top-four novelty;
- a small coefficient file \(\Rightarrow\) intrinsic complexity classification;
- a verified two-particle collision \(\Rightarrow\) kinetic scaling;
- a pipeline edge \(\Rightarrow\) proof of the downstream analytic theorem.

The manuscript itself generally knows this. The review recommendation should therefore turn on the mathematics, not on the exceptional quality of the engineering around it.

---

# 12. Major blocking requirements for another top-four-level review

I would regard the following as the current blockers.

## E17.1 — Replace the revealed-candidate tautology by a genuinely constrained dual/separation theorem

Either rename Theorem v17-dual to reflect that it is a revealed-behavior adaptive-test representation, or add a theorem whose dual class is nontrivial under the relevant causal/resource information constraints.

A major theorem should explain the nonconvex resource image rather than recover \(\max_i f_i(b)\) by a pre-programmed pointwise selector after \(b\) is revealed.

Possible directions include:

- a causal tester with its own memory/information budget;
- a universal continuation-state dual;
- a nonlinear Hahn–Banach/separation theorem adapted to finite causal state;
- a resource norm/gauge whose dual has operational meaning;
- a characterization of when hidden/visible/private behavior classes admit finite-dimensional separating families.

## E17.2 — Turn intrinsic existence size into intrinsic complexity or sharp structure

The bound \(4Ra/\sqrt n\) and support counts are useful but not enough.

At least one of the following is needed:

- sharpness/lower bounds;
- representation-independent bit complexity;
- a width/horizon/dimension complexity law;
- minimal test degree/support;
- a tractable class with an explicit algorithmic bound;
- a complexity dichotomy;
- an equivalence between certificate complexity and causal state complexity.

Without this, “intrinsic” remains an existence-size statement rather than a constructive structural theory.

## E17.3 — Go beyond a two-particle finite-experiment embedding if the physical bridge is to carry top-four significance

The new collision theorem should be retained. But for the physical route to carry the paper, one needs a theorem involving genuinely hard interaction structure, for example:

- particle-number-uniform resource separation;
- a collision network rather than one isolated collision;
- robustness through recollisions;
- Boltzmann–Grad or kinetic scaling;
- a nontrivial hydrodynamic/kinetic observation limit;
- an acquisition theorem whose feedback affects a genuine interacting dynamics;
- a result that supplies one of the hard B4 hypotheses.

The current geometric-similarity statement is not a substitute for such a limit.

## E17.4 — Close one hard downstream analytic gate, not merely one scoped interface edge

A convincing top-four path would be to prove one theorem that materially reduces the declared B4/C2 burden.

Examples:

- an action-sublevel compactness + nonlinear resolvent/comparison theorem usable by B4;
- a particle-uniform hierarchy corrector;
- a nonlinear Trotter–Kato step;
- a changing-microscopic-path optional-projection theorem with likelihood/stochastic-exponential identification;
- a genuine C2 strict-duality/form-response/rigidity theorem.

V17's Gaussian-observation posterior stability is a useful lemma but not an adequate substitute for these.

## E17.5 — Complete the Norberg proof-level crosswalk

The exact filtered-deficiency/operator/action model in Norberg must be inspected from the original and compared against the manuscript's private/hidden/visible finite-state conventions.

The paper should then state precisely which theorem is new after that subtraction.

---

# 13. Technical and expository comments

1. **Rename or qualify “duality.”** The infinite-dimensional identity is powered by revealed-candidate pointwise selection. The current name suggests a deeper dual geometry than the proof provides.

2. **State explicitly that affine structure is unnecessary for the first representation theorem.** This would help readers see where causal geometry actually enters: not in the partition-of-unity identity, but in the finite polynomial/chart approximation and in the concrete resource images.

3. **Distinguish three complexities everywhere.**  
   (i) size of a behavior-space adaptive test;  
   (ii) cost of verifying its minimum over the nonconvex feasible behavior set;  
   (iii) row-coordinate positivity-certificate size.  
   The current manuscript mostly does this, but the abstract and summary language can still be read too broadly.

4. **Do not imply sharpness of \(4Ra/\sqrt n\).** No matching lower bound is supplied.

5. **The moment-support bound is an existence theorem.** A Carathéodory reduction of moments is not by itself a computationally accessible dual optimizer.

6. **Keep the strict-margin boundary prominent.** The paper has fixed this; do not regress in future revisions.

7. **In the collision theorem, emphasize that the \(B\)-\(W\) correlation is in the preparation.** The collision reveals \(B\); it does not create the mark correlation.

8. **Call the gate an acquisition gate.** This is already done and is accurate. It should not be rhetorically upgraded to feedback control of the mechanics.

9. **Geometric similarity is not a kinetic limit.** The manuscript states this correctly; keep the distinction in the abstract/press-summary layer as well.

10. **The no-collision regime is a strong control.** Preserve it. It is the best evidence that the physical signal is genuinely interaction-sensitive.

11. **The optional theorem's common-latent/common-space hypothesis should remain adjacent to every program-level claim.** It is much stronger than generic convergence of changing experiments.

12. **Equivalence matters.** The posterior identity is proved under equivalent joint laws. If singular limits are relevant downstream, they require separate work.

13. **The physical optional theorem changes the observation function, not the microscopic dynamics.** This should be stated whenever it is advertised as a “changing-filtration microscopic limit.”

14. **Do not let graph-core language hide the simplicity of the sensor approximation.** Orbit mollification is a legitimate domain construction, but the stochastic convergence result still comes from Gaussian drift stability.

15. **The clean source tree is a success.** Preserve this architecture in later revisions rather than reintroducing transitive journal-source dependencies.

16. **Keep provenance outside the theorem narrative where possible.** Commit hashes and branch ancestry belong in the reproducibility package, not in the conceptual argument.

17. **The exact finite witness and the physical theorem should be presented as examples/applications unless stronger classification/scaling results are added.**

18. **The literature audit should distinguish “not found” from “does not exist.”** The current Norberg language does this correctly.

19. **Avoid measuring novelty by certificate byte size.** The 17-coefficient example is attractive, but its small serialization is not an invariant mathematical complexity theorem.

20. **The title remains ambitious.** If the hard downstream and structural blockers remain open, a narrower title centered on finite causal resource comparison would better match the proved theorem scale.

---

# 14. What would change the recommendation

V17 has now answered enough of the predecessor report that another iteration of “add one more finite example and one more verification layer” will not materially improve the top-four case.

Two routes could.

## Route A — A true structural theory of finite causal resources

A theorem of the following type would materially change my assessment:

- characterize the nonconvex behavior image up to an operational equivalence;
- identify an intrinsic continuation-state invariant;
- prove a resource-sensitive nonlinear separation theorem under causal tester constraints;
- give sharp dimension/width laws;
- derive upper and lower certificate-complexity bounds in intrinsic parameters;
- classify private/hidden/visible separations rather than exhibit isolated witnesses.

Then the current adaptive hierarchy and collision example would become convincing corollaries of a larger theory.

## Route B — A hard physical/downstream theorem

Alternatively, retain the finite theory as an interface and prove one serious microscopic-to-macroscopic result:

- a particle-uniform collision-sensitive resource gap;
- a Boltzmann–Grad/kinetic limit preserving the resource separation;
- a B4 dynamic-action/Nisio/resolvent theorem;
- a hierarchy corrector and nonlinear semigroup convergence;
- or a C2 changing-path/likelihood/optional-projection theorem with stochastic-exponential and BSDE identification.

Then the current finite certificate machinery would acquire much greater significance because it would certify a genuinely difficult analytic phenomenon.

---

# 15. Positive aspects that should be preserved

A harsh report should not erase genuine progress.

1. The manuscript now keeps the private feasible image nonconvex without pretending that free convexification preserves the resource model.

2. The test-size theorem is stated in observable behavior dimension rather than redundant simulator-row dimension.

3. The paper distinguishes test existence size from verification complexity and avoids a false polynomial-time claim.

4. The small nonlinear witness is exact and independently checkable.

5. The physical example now produces different private/hidden/visible values at the same retained register width.

6. The collision/no-collision comparison genuinely demonstrates interaction sensitivity at the fixed two-particle level.

7. The mark is an actual source/target latent variable rather than a post hoc simulator coin.

8. The algorithmic theorem now states the uniform computability hypotheses needed for termination.

9. The optional-projection theorem controls the whole posterior process, not only finitely many checkpoints.

10. The latent-preserving convergence coupling is explicitly separated from executable causal simulation.

11. The pipeline graph honestly leaves all full historical closure flags false.

12. The paper now credits the inherited v15 physical transfer principle instead of relabeling it as new.

13. The nearest positivity literature is treated seriously.

14. The Norberg gap is acknowledged rather than papered over.

15. The canonical article has a conventional clean source tree.

16. The reproducibility package is unusually strong.

These are all worth keeping.

---

# 16. Final assessment

V17 is the strongest version of General Theta Foundations I that I have inspected.

It is no longer fair to criticize it as merely a repository wrapper around inherited material. It contains new proofs, a new quantitative behavior-space approximation theorem, a new exact resource-sensitive physical example, and a new posterior-process stability theorem. Several prior objections are genuinely closed.

I nevertheless recommend rejection at the requested Annals/Inventiones/JAMS/Acta standard.

The reason is now concentrated and mathematical.

The adaptive-test “duality” becomes easy because the verifier is allowed to evaluate a pre-chosen pointwise selector at the fully revealed behavior. The behavior-dimension theorem is a useful Bernstein/binomial approximation theorem but does not yet become an intrinsic complexity/classification theory. The collision theorem is a robust two-particle realization of a finite binary experiment, not a hard many-body or kinetic bridge. The optional-projection theorem is a strong-law stability lemma under common-latent joint-TV control, not the historical changing-path C2 theorem. The eleven-paper graph still records every full historical target as open. And the nearest filtered-deficiency priority boundary remains unresolved at proof level.

The manuscript has therefore advanced from “technically credible interface theory with major missing examples” to “technically credible interface theory with several good examples and quantitative lemmas.” That is real progress.

It is still short of a theorem that changes the architecture of the subject.

## Recommendation: Reject at the requested top-four general-mathematics venue in the present form.

A future version would merit a genuinely new top-four-level review if it closes E17.1 plus E17.2, or if it instead proves an E17.3/E17.4 theorem of genuine scaling/downstream depth and completes the Norberg crosswalk.
