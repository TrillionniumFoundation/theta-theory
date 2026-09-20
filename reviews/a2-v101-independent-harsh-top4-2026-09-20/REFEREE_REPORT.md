# Independent harsh referee report on A2 revision 101

**Manuscript:** *Projective polynomial observations: finite spectral calibration and divisorial entrances*  
**Reviewed revision branch:** revision/a2-v101-finite-metric-divisorial-contact-2026-09-20  
**Reviewed exact source head:** d1654974140410eb356240d3121c5f36267a89d2  
**Principal entrypoint:** papers/A2-v17-boundary-information-coarsening/rigidity_v101.tex  
**Principal article source:** papers/A2-v17-boundary-information-coarsening/article/v101/paper.tex  
**Controlling prior report:** reviews/a2-v100-independent-harsh-top4-2026-09-20/REFEREE_REPORT.md  
**Controlling prior review commit:** c05195ef73bd3c5c8185928920926baf2d38df2c  
**Prior reviewed paper head:** 7407ad098cac70ac07bb7d9d01f562890041cada  
**Independent review branch:** review/a2-v101-independent-harsh-top4-2026-09-20  
**Date:** 2026-09-20

## 1. Recommendation

**Recommendation for an Annals / Acta / Inventiones / JAMS-level general mathematics journal: reject in the present form.**

This is again **not** a correctness rejection.

Revision 101 is mathematically stronger than revision 100. The authors did not answer the previous report merely by adding prose, manifests, or another abstract framework. They added two substantive pieces:

1. a finite constrained-cost determination theorem for the full-rank binary leading spectral fibre, including quantitative stability; and
2. a real divisorial contact formula for isolated Nash remote germs, including the leading metric unit.

They also added a theorem-level Puiseux-residue comparison with coordinate real tropicalization, replaced the previous assumed filtered conjugacy limit by a finite-weighted-jet condition, made the fixed-format convention explicit, and clarified finite-family versus infinite-family monomialization.

Those are serious responses.

The top-four problem is now narrower and more revealing. The new finite-calibration theorem is valid-looking, but it is not yet the intrinsic finite-information theorem that the previous reports were asking for. It starts from the same profiled quadratic form \(Q_\theta\) already present in the multiplicity theorem, recovers that matrix by polarization of specially constrained value functions, and then invokes the already proved multiplicity decoder to recover the leading fibre. The scalar costs are defined by constraining latent root sums and variances inside the parameter space; they are not scalar observables canonically read from the original data. Moreover, at the full-rank centres under consideration the central observation already identifies the full parameter \(\theta\), after which \(Q_\theta\) can be computed directly. Thus the theorem is a useful finite representation of an already known local quadratic geometry, not yet a new information principle for the observation model.

The divisorial theorem is, in my view, the strongest new mathematics in v101. It gives a clean real-arc formula and a leading-constant formula after simultaneous principalization of the residual and time ideals. But at the level currently stated, its exponent is a real Łojasiewicz/contact exponent extracted by standard principalization/valuative machinery, while the leading constant depends on the chosen observation norm through resolved units. The manuscript has not yet isolated what is new relative to the classical integral-closure, normalized-blow-up, Rees-valuation, and real-analytic Łojasiewicz framework strongly enough to justify the claimed general-journal scale.

Revision 101 therefore improves the mathematics materially without yet making the conceptual jump required for the stated journal class.

## 2. Scope of this report

I reviewed the exact source head

d1654974140410eb356240d3121c5f36267a89d2

on revision/a2-v101-finite-metric-divisorial-contact-2026-09-20.

Relative to v100, the mathematical additions are concentrated in:

- article/v101/finite_metric.tex;
- article/v101/real_residue.tex;
- article/v101/divisorial_contact.tex;
- article/v101/format_and_dependencies.tex;
- the new principal paper wrapper and references.

I also checked the controlling v100 referee report, the v101 response, the source manifest, the finite exact diagnostic record, the diagnostic script, the native-build wrapper, the full-rank inverse used by the finite-calibration proof, the inherited multiplicity theorem and its profiled matrix, the v100 canonical weighted-tangent theorem, and the inherited singular-entrance theorem.

I treated repository diagnostics as evidence for the finite examples only. I did not treat them as proof of the universal statements.

My standard remains deliberately severe. The question is not whether this is a serious paper. It is whether the paper has reached the concentration, novelty, inevitability, and depth expected of a top-four general mathematics journal.

## 3. Executive diagnosis

Revision 101 closes many literal objections from v100.

The real/positive tropical comparison is now theorem-level rather than bibliographic hand-waving. The finite-jet naturality theorem is cleaner than the previous version because the convergence of conjugates is derived rather than assumed. The fixed-format convention is explicit. The finite-family principalization issue is correctly separated from any impossible simultaneous monomialization of an infinite polynomial ring. The remote exponent is now tied to a residual/time ideal pair and accessible real divisors rather than merely to one-variable semialgebraic Puiseux behavior.

The remaining problem is not missing infrastructure.

It is that the paper's new central theorem still depends too heavily on information already encoded in the older full-rank local inverse and multiplicity theorem.

The conceptual chain is:

1. full-rank exact identification gives a locally invertible coefficient/stochastic parametrization;
2. the inherited multiplicity analysis gives the profiled positive-definite quadratic form \(Q_\theta\);
3. the new constrained value functions recover entries of \(Q_\theta\) by polarization;
4. the inherited multiplicity theorem then decodes the same \(Q_\theta\) into the leading root fibre.

This is mathematically coherent. It is also much closer to a finite readout of an already established quadratic normal form than to a new structural classification.

The strongest path forward is now visible: either make the finite scalar datum genuinely intrinsic to the observation law, with a necessity/minimality or nontrivial compression theorem, or make the divisorial contact theorem substantially sharper and more canonical relative to the classical Łojasiewicz/integral-closure theory.

## 4. What revision 101 genuinely fixes

A harsh report should record what has actually been repaired.

### 4.1 R100.1: real/positive tropical positioning is materially better

Theorem thm:v101-residue identifies the positive-real weighted tangent relation with residues of bounded weighted Puiseux points. The signed nonzero-coordinate part is then explicitly identified with a fixed-weight coordinate signed-valuation fibre.

This is the theorem-level comparison the previous report requested.

The manuscript also correctly distinguishes:

- positive degeneration parameter;
- positive coordinate orthant;
- coordinate signed valuation;
- residue magnitudes;
- observation-unit section;
- spectral decoder;
- full inverse-limit real analytification.

That is a substantial conceptual cleanup.

### 4.2 R100.2/R100.3: the paper now has a model-specific finite scalar sufficiency theorem

Theorem thm:v101-finite is not the generic distance-function reconstruction theorem from v100. It uses the actual binary coefficient inverse, a finite list of retained root statistics, profiling over all nuisance parameters, and a concrete decoder.

That is a genuine improvement over v100.

### 4.3 R100.4: entrance order is now tied to residual/time singularity data

Theorem thm:v101-divisorial identifies the exponent with a supremum of residual-order/time-order ratios and with a maximum over accessible divisorial ratios in a simultaneous monomial presentation.

This is much more informative than merely saying that the minimized distance is a semialgebraic one-variable germ with rational Puiseux order.

### 4.4 R100.5: fixed format is explicit

Definition def:v101-format now records variable dimensions, observation/target dimensions, atom count, polynomial degree, syntax length, and coefficient encoding conventions.

This closes an important ambiguity in the effectivity claims.

### 4.5 R100.6: finite-family monomialization is stated correctly

The manuscript no longer risks suggesting that one modification principalizes every scalar polynomial simultaneously. The x-cy example makes the limitation explicit.

### 4.6 R100.7: direct and general proofs are separated more honestly

The dependency appendix says clearly that the direct full-rank multiplicity, cubic-fibre, and wall arguments do not require the general atlas.

This is the right statement.

### 4.7 The response package is disciplined

The v101 response does not claim journal acceptance, does not claim that finite arithmetic proves universal theorems, and does not pretend that a workflow definition is a native build result.

That discipline should be preserved.

## 5. Main objection I: the finite-calibration theorem is not yet an intrinsic finite-information theorem

This is the central issue in v101.

The new theorem defines

\[
c_\theta(v)
=
\lim_{t\downarrow0}
\frac{4}{t^2}
\min_{\xi\in B_\theta(t;v)}
h_w(F_T(\xi),P_\theta)^2,
\]

where \(B_\theta(t;v)\) imposes exact constraints on retained latent root coordinates such as centred cluster variances and signed endpoint sums.

The theorem then proves

\[
c_\theta(v)=v^{\mathsf T}Q_\theta v
\]

and recovers \(Q_\theta\) from \(c_\theta(e_i)\) and \(c_\theta(e_i+e_j)\).

This is correct-looking. But the information interpretation is much weaker than the title and abstract suggest.

### 5.1 The scalar "calibrations" are constrained latent value functions

The experiment actually observes probability arrays at the clocks.

The new scalar datum is not a scalar statistic of that observed array. It is the optimum of a new constrained optimization problem over the model, where the constraint is expressed in terms of latent root sums and variances.

To query \(c_\theta(e_i)\), one must know which latent cluster is being marked, which multiplicity regime one is in, which coordinate is a variance versus a signed sum, and how to impose that latent constraint while minimizing over every remaining model variable.

That is mathematically legitimate as a value function.

It is not yet an operational finite calibration observable.

The manuscript should not slide between these two meanings.

### 5.2 The theorem assumes the discrete pattern as part of the datum

The finite datum is

\[
\mathfrak C_\theta
=
(\mathcal P;c_\theta(e_i),c_\theta(e_i+e_j)).
\]

Thus the theorem does not recover the multiplicity/boundary pattern from the scalar costs. It is given the marked pattern in advance.

This is especially important because the decoder is pattern dependent.

A top-four finite-information theorem would be stronger if the finite scalar data themselves determined the relevant stratum, or if the manuscript proved that the pattern is an unavoidable finite side datum.

### 5.3 At these centres the full observation already identifies theta

Lemma lem:fullrank is much stronger than a mere local rank statement.

Under the hypotheses used in the finite-calibration section, sufficiently close observations recover coefficient and stochastic parameters with error bounded by a constant times observation error, and exact competitors have the same component polynomials and stochastic parameters up to permutation.

Therefore the centre observation already determines the full centre parameter \(\theta\).

Once \(\theta\) is known, the score matrix, the profiling matrix, and \(Q_\theta\) are explicitly computable.

This weakens the information-theoretic force of the finite-calibration theorem substantially. The theorem does not show that a small observable scalar summary replaces inaccessible high-dimensional information. It shows that a positive-definite matrix already determined by the identified centre can also be recovered from finitely many specially designed constrained value functions.

That is a useful representation theorem, not yet a new identifiability theorem.

### 5.4 No necessity, minimality, or lower bound is proved

The manuscript wisely says that the datum need not be minimal.

But without a necessity statement, the count \(k(k+1)/2\), and hence the headline \(d(2d+1)\) bound, has limited conceptual meaning.

It is simply the number of entries of a symmetric matrix recovered by polarization.

A stronger theorem would address at least one of the following:

- minimal number of scalar oracle queries;
- lower bounds under a natural class of scalar probes;
- characterization of all scalar probe families sufficient to recover the fibre;
- generic reduction below \(k(k+1)/2\);
- impossibility of using only unconstrained observable scalar statistics;
- finite scalar recovery without supplying the marked pattern.

Without such a result, the theorem is finite-dimensional linear algebra wrapped around a nontrivial but already known local normal form.

## 6. Main objection II: the proof of the headline theorem is structurally downstream of the result it is supposed to elevate

The most revealing step in the proof is the invocation of Theorem thm:mult-atlas to identify the whole-model leading sets by the decoder and the constraint

\[
v^{\mathsf T}Q_\theta v\le4.
\]

That older theorem already contains the substantive geometric statement:

- which root coordinates survive;
- which are order \(t^{1/2}\) versus order \(t\);
- what cone constraints apply;
- how nuisance directions are profiled;
- why \(Q\) is positive definite;
- how the complete leading root set is realized.

The v101 theorem proves that specially constrained value functions recover this same \(Q\).

So the logic is not:

> finite scalar data unexpectedly force a new spectral geometry.

It is:

> the previous analysis already produces a quadratic spectral geometry, and finite quadratic probes recover its matrix.

Again, this is correct.

But it means the finite-calibration theorem is not an independent new spine of the paper. Its geometric content is downstream of the multiplicity theorem, and its reconstruction content is polarization.

The manuscript should present it as a finite readout theorem for the established local normal form unless a stronger independent statement is proved.

## 7. Main objection III: the real-residue comparison is now correctly positioned, but it is still mostly a standard semialgebraic/Puiseux equivalence

Theorem thm:v101-residue is a good theorem to include.

The proof uses two standard directions:

1. an algebraic Puiseux point gives a convergent semialgebraic positive-real arc after ramification; and
2. a point in the positive weighted tangent closure gives a semialgebraic curve, hence a Puiseux germ after reparametrization.

This is exactly the comparison one should make.

But the theorem does not yet extract a new structural consequence from real tropicalization.

The manuscript correctly notes that coordinate signed valuation forgets residue magnitudes and that the observation-unit section plus spectral decoder retain additional metric data. That distinction is important. It is also conceptually expected: valuation records leading exponents and signs, while units carry metric normalization.

The question left open is:

> What new theorem about the observation problem follows because this extra residue/unit data is retained?

At present the answer is essentially that it is needed to recover the sharp metric fibre. That was already known from the positive-unit separation discussion.

For a top-four contribution, I would want the comparison to force something new, for example:

- a classification of liftable faces for this observation relation;
- a finite tropical/residue invariant equivalent to the spectral fibre;
- a theorem showing which parts of the fibre are determined by signed valuation and which require residue units;
- a functorial statement relating the full family of observation coordinates to real analytification, not only one fixed coordinate valuation fibre.

### 7.1 Finite-jet naturality is cleaner but still associated-graded geometry

Theorem thm:v101-filtered is an improvement over v100 because it derives the filtered limit from weighted Taylor support conditions.

But once a Nash isomorphism and its inverse are filtered in both directions, the convergence to weighted initial maps and compatibility with composition are standard associated-graded behavior.

I see no immediate correctness problem.

I also do not see top-four novelty in this theorem by itself.

## 8. Main objection IV: the divisorial theorem is the strongest new mathematics, but its novelty relative to classical Łojasiewicz/integral-closure theory is still not isolated sharply enough

Theorem thm:v101-divisorial deserves to remain central.

The manuscript simultaneously principalizes the residual ideal

\[
\mathfrak a=(R_1,\ldots,R_M)
\]

and the time ideal

\[
\mathfrak t=(\delta),
\]

then defines

\[
\rho=\max \frac{b_i}{a_i}
\]

over accessible real divisors.

It proves the real-arc characterization

\[
\rho
=
\sup_\gamma
\frac{\operatorname{ord}(\mathfrak a\circ\gamma)}
{\operatorname{ord}(\delta\circ\gamma)}
\]

and derives the leading constant from the maximum of the resolved unit ratio.

This is substantial.

But the exposition itself acknowledges that the exponent is a relative Łojasiewicz contact exponent and that integral closure controls the arc orders.

That puts the result directly in classical territory.

### 8.1 The paper must say what is new beyond the classical valuative formula

The current discussion cites Lejeune-Jalabert and Teissier, but the mathematical positioning remains too compressed.

Classical integral-closure theory already relates orders along arcs, normalized blow-ups, divisorial data, rationality, and Łojasiewicz exponents.

Therefore the manuscript must identify precisely which of the following is new:

- restriction to accessible real sectors;
- simultaneous treatment of feasibility inequalities;
- the positive-time denominator ideal;
- the exact norm-dependent leading coefficient;
- compatibility with the observation model;
- uniformity in a parameter family;
- interaction with identification walls.

If the new content is the accessible-real restriction plus the metric-unit constant, then that should be the theorem's advertised contribution, and the classical divisorial exponent formula should be presented as the underlying mechanism rather than as if the entire package were new.

### 8.2 "Accessible real divisors" are useful but not yet a canonical geometric object

The theorem proves presentation independence of the numerical exponent by passing to the intrinsic arc supremum.

Good.

But the set of accessible coordinate divisors depends on the chosen real monomial presentation. The theorem does not identify a canonical minimal set of divisorial valuations, such as an appropriate real analogue of Rees valuations, that computes the exponent.

Thus the formula is invariant numerically without yet giving a canonical divisorial classification.

A stronger theorem would identify an intrinsic finite set of valuations or explain why no such refinement is possible in the real-feasible category.

### 8.3 The leading coefficient is metric data, not an ideal invariant

The manuscript says this correctly.

The exponent is controlled by the residual/time ideals, while the leading coefficient depends on the norm through the resolved unit.

That is an important distinction.

It also means that the theorem does not by itself produce a singularity invariant rich enough to classify the actual entrance asymptotics. The metric unit has to be carried as additional structure.

This is not a flaw. It is a limit on what the theorem accomplishes.

### 8.4 The theorem is a single-germ result, while the paper's broader rhetoric is family/global

The inherited semialgebraic theorem has family stratification and uniform remainder statements.

The new divisorial theorem is stated for a fixed isolated Nash remote germ.

A top-four strengthening would connect these levels: construct the relevant divisorial/contact data uniformly on strata, describe how it changes across walls, or show that only finitely many intrinsic divisor types occur in fixed format.

That would turn the new theorem from a local reinterpretation into a genuine organizing principle.

## 9. Main objection V: the paper remains too cumulative for the level of the new conceptual gain

The v101 principal paper imports substantial v98, v99, and v100 material, then adds four new v101 modules, while a full v100 archive is also preserved separately.

Repository preservation is sensible.

Journal presentation is a different question.

The principal article still reads as a historical accumulation of every successful layer rather than as a single theorem-driven argument.

The authors have improved the order: direct model results now come before the general atlas. But the paper still carries:

- full-rank multiplicity analysis;
- exact cubic fibre;
- two walls;
- remote structure;
- geometric wall machinery;
- critical examples;
- real atlas;
- canonical weighted tangent;
- real residue comparison;
- joint separation;
- valuative separation;
- singular entrances;
- divisorial contact;
- general foundations;
- format/effectivity material;
- arithmetic outputs.

That amount of material can be justified only if one theorem visibly unifies it.

I do not yet see such a theorem.

The finite-calibration theorem is too downstream of the old \(Q\)-geometry. The divisorial theorem governs one part of the remote theory but not the full local multiplicity/cubic story. The real-tropical theorem positions an object but does not unify the two main mechanisms.

This is now an architectural rather than a correctness problem.

## 10. Detailed correctness assessment of the new v101 material

I did not find a direct counterexample to the new principal statements.

### 10.1 Finite calibration

The positive definiteness of \(Q_\theta\) is consistent with the inherited coefficient inverse and the independence of the partial-fraction coefficient directions.

The upper-bound construction realizes prescribed variance coordinates by actual real root configurations and keeps strictly positive stochastic variables feasible at sufficiently small \(t\).

The lower-bound argument uses the full-rank inverse to force all coefficient and stochastic errors to order \(t\), then uses cluster coefficient control to obtain the required \(t^{1/2}\) root scale at repeated interior roots.

This is plausible and consistent with the inherited multiplicity proof.

The main issue is not an evident mathematical gap. It is the structural dependence discussed above.

### 10.2 Quantitative stability

The radial comparison follows from

\[
(1-\vartheta)Q\le Q'\le(1+\vartheta)Q
\]

and the decoder homogeneity.

The exponent \(\beta=\gamma/2\) is consistent with the fact that the retained variance coordinate is quadratic in the repeated-root displacement.

The matrix error bound from noisy polarized costs is elementary but correct.

### 10.3 Real residue comparison

For semialgebraic germs and rational weights, the equivalence between weighted tangent limits and residues of algebraic Puiseux points is consistent with real curve selection and Puiseux parametrization.

The distinction between exact weight and higher valuation for zero residue coordinates is important and correctly stated.

### 10.4 Finite-jet naturality

The weighted Taylor expansion argument is standard and appears sound under the stated bi-filtered hypotheses on the map and inverse.

The inverse initial maps being mutual polynomial inverses follows naturally from the rescaled identities.

### 10.5 Divisorial contact

The weighted-average argument

\[
\frac{\sum b_i\beta_i}{\sum a_i\beta_i}
\le
\max_i \frac{b_i}{a_i}
\]

is correct on a simultaneous monomial chart.

The level-set identity

\[
\max_{\delta=\text{fixed}}\frac{\delta^\rho}{\|R\|}
=
\frac{\delta^\rho}{d(\delta)}
\]

is exact.

Compactness plus continuity of the resolved unit ratio gives the asserted leading constant provided the real-sector principalization and accessibility statements are made with the required properness and surjectivity.

I would ask the authors to formalize that setup more explicitly, but I do not currently have a counterexample.

### 10.6 Fixed-format exponent bound

The quantifier-elimination argument gives a bounded-degree algebraic relation for the minimum graph. A Puiseux leading exponent is then a ratio of differences of monomial exponents, so a computable numerator/denominator bound follows.

This is credible at the stated non-complexity level.

## 11. Reproducibility audit

The repository discipline remains good, but exact-head native closure is still incomplete.

### 11.1 Exact reviewed source head

The reviewed source commit is

d1654974140410eb356240d3121c5f36267a89d2.

The commit message itself correctly says that native success is not inferred from the workflow definition.

### 11.2 No committed v101 runtime receipt is present at the reviewed revision head

The branch does not contain

revisions/a2-v101/native/RUNTIME_RECEIPT.json.

The committed LOCAL_VALIDATION.json explicitly states:

- principal native build executed locally: false;
- archive native build executed locally: false;
- complete native build executed locally: false;
- remote native success observed: false.

Therefore exact-head native compilation is not durably established by the reviewed branch.

### 11.3 Available status interfaces do not establish a successful run

The combined status query returned no statuses for the reviewed source SHA.

The available workflow-run query is limited to pull-request-triggered runs and returned none. I do not infer from that restricted interface that no push-triggered run occurred.

The supported conclusion is narrower: no successful source-head-bound runtime receipt is committed on the reviewed revision head.

### 11.4 The exact finite diagnostic is useful but narrow

The v101 exact check verifies a degree-two full-rank repeated-root example with two retained variance coordinates, exact profiling, three polarization probes, and feasible recovery curves.

It does not test:

- the linear regime;
- endpoint cones;
- mixed endpoint/repeated retained coordinates;
- the universal compact-uniform error bounds;
- the real-residue theorem;
- the divisorial theorem beyond several explicit contact ratios;
- the fixed-format theorem.

The script itself says so, which is appropriate.

## 12. Disposition of the v100 requests

### R100.1 — Exact relationship to real/positive tropical geometry

**Substantially answered at the fixed-coordinate residue level.**

The paper now gives an exact Puiseux-residue comparison and distinguishes it from full real analytification.

The remaining issue is no longer missing comparison. It is missing consequence: the comparison has not yet yielded a new structural theorem of sufficient depth.

### R100.2 — Replace generic quadratic reconstruction as headline structure

**Answered literally, but only partially at the conceptual level.**

The new finite-calibration theorem is model specific.

However, it still recovers an already known profiled matrix by polarization and then invokes the older decoder.

### R100.3 — Strengthen scalar separation / finite scalar information

**Partially answered.**

The paper gives finite scalar sufficiency, which is stronger than the v100 distance-function theorem.

But the scalar probes are latent constrained value functions and the marked pattern is supplied. No necessity/minimality or genuinely observable finite summary theorem is proved.

### R100.4 — Turn entrance orders into singularity geometry

**Substantially answered.**

The residual/time ideal pair, arc order, accessible divisors, and metric unit now give a real singularity-geometric interpretation.

The remaining issue is novelty and canonicality relative to classical Łojasiewicz/integral-closure theory, plus lack of a uniform family-level divisorial classification.

### R100.5 — Define fixed format

**Answered.**

### R100.6 — Tighten monomial-presentation wording

**Answered.**

### R100.7 — Make general/concrete dependency explicit

**Answered.**

The paper now states correctly that the direct binary/cubic results do not require the general atlas.

### R100.8 — Complete durable exact-head validation

**Not yet answered.**

The workflow exists, but the reviewed branch has no committed successful runtime receipt.

### R100.9 — Stop adding infrastructure unless it proves mathematics

**Mostly answered.**

The new revision adds real mathematics rather than another certificate layer.

## 13. Revisions required before reconsideration at the same journal class

### R101.1 — Clarify the status of the finite scalar datum

State explicitly whether the quantities \(c_\theta(v)\) are:

- observable statistics;
- controllable physical calibration experiments;
- oracle values;
- or theoretical constrained value functions on latent parameter space.

At present "calibration" suggests more operational accessibility than the definition provides.

### R101.2 — Prove a genuinely intrinsic finite-information theorem

A result that would materially improve the paper would do at least one of the following:

- recover the leading fibre from finitely many scalar functions of the observable law itself;
- recover the marked pattern from the same scalar datum;
- prove a lower bound or minimality theorem for a natural class of probes;
- characterize exactly which finite scalar probe families determine the quotient form;
- show that the finite datum is invariantly defined without choosing latent cluster coordinates;
- produce a finite scalar invariant that remains meaningful when the centre is not first fully reconstructed.

Merely repolarizing the already known \(Q_\theta\) is not enough.

### R101.3 — Separate the genuinely new part of the divisorial theorem from classical Łojasiewicz theory

The paper should compare the exponent formula explicitly with:

- integral closure;
- normalized blow-up and Rees valuations;
- classical Łojasiewicz exponents;
- real-analytic arc criteria.

Then state exactly what the manuscript adds: real accessibility, feasibility sectors, metric units, parameter-family uniformity, or some combination.

### R101.4 — Make the divisorial data canonical or prove why only the numerical exponent can be canonical

If possible, identify a canonical finite collection of real-accessible divisorial valuations computing \(\rho\).

If not, say explicitly that the divisor set is presentation dependent while the arc supremum is intrinsic, and formulate the theorem around the intrinsic object.

### R101.5 — Connect divisorial contact to a new wall-classification theorem

The current theorem reinterprets known entrance exponents.

A stronger result would show that the residual/time divisorial data classify possible wall openings, bifurcations, or leading coefficients in a nontrivial family of polynomial observation models.

That would genuinely unify the general theorem with the concrete cubic analysis.

### R101.6 — Reduce historical accumulation in the principal narrative

The repository may preserve every prior source.

The journal article should be organized around the smallest set of theorems needed to expose the conceptual spine.

This does not require deleting results from the repository. It requires deciding which results are principal and which are supporting or companion material.

### R101.7 — Complete source-bound native validation

Run the principal/archive/complete native build for the exact source head and preserve the receipt and hashes durably on the revision branch.

This is not a mathematical acceptance condition, but the repository itself makes exact-head reproducibility part of the review package.

## 14. Editorial comments

1. The phrase "finite calibration" should be qualified unless the constrained latent value functions can actually be generated from externally controllable experiments.

2. The abstract should say that the marked multiplicity pattern is part of the finite datum.

3. The statement "at most d(2d+1) scalar calibrations suffice" is mathematically true as a symmetric-matrix entry count, but it should not be presented as a sample-complexity or measurement-complexity theorem.

4. The finite-calibration proof should explicitly distinguish what is new from what is imported from thm:mult-atlas.

5. The real-residue theorem should be described as an exact comparison theorem, not as a new real tropical fundamental theorem. The current text mostly does this correctly.

6. The divisorial theorem should define the proper real modification and the accessible sector structure more formally before the theorem statement.

7. The role of the norm in the leading coefficient should be emphasized early: the exponent is ideal/contact data, the coefficient is metric-unit data.

8. The paper should avoid using repository preservation policy as a reason to keep every historical theorem in the principal exposition.

9. The exact diagnostic matrices are useful evidence but should remain subordinate to the theorem.

10. The title is now better aligned with the new mathematics than the v100 title, but "finite spectral calibration" still sounds more operational than the current definition warrants.

## 15. Originality and depth assessment

The strongest mathematics in the full article now appears to be divided between two spines.

The first is the concrete binary/cubic inverse geometry:

- exact full-rank identification;
- multiplicity-dependent spectral modulus;
- exact rank-deficient cubic fibre;
- inverse through channel-rank loss;
- weight and endpoint walls;
- exact critical-shell behavior.

The second is the new remote-contact interpretation:

- semialgebraic entrance asymptotics;
- residual/time divisorial contact;
- real-accessible arc criterion;
- metric-unit leading constant.

The v101 finite-calibration theorem provides a finite encoding of the first spine's quadratic local geometry, but does not yet reorganize it.

The real-residue theorem correctly locates the weighted object relative to real tropicalization, but does not yet reorganize either spine.

A top-four article normally needs one statement after which the surrounding machinery looks inevitable.

Revision 101 has not yet reached that point.

## 16. Final assessment

Revision 101 is a serious and mathematically meaningful response to revision 100.

It fixes the nearest-literature positioning, replaces a generic distance-function reconstruction lemma with a genuinely model-specific finite scalar sufficiency statement, derives filtered naturality from finite jets, turns the remote exponent into a residual/time divisorial contact quantity, and makes the fixed-format conventions precise.

I found no direct contradiction in the new principal theorems.

Nevertheless, I still recommend **rejection in the present form** for an Annals / Acta / Inventiones / JAMS-level general mathematics journal.

The decisive reason is now precise.

The new finite-calibration theorem does not yet provide an intrinsic finite observable invariant of the experiment. It recovers the already established profiled matrix \(Q_\theta\) by polarization of specially constrained latent value functions and then invokes the already established multiplicity decoder. At the full-rank centres in question, the observation already identifies \(\theta\), so \(Q_\theta\) is directly computable once the centre is recovered.

The new divisorial theorem is stronger and potentially more important, but its genuinely new content relative to classical Łojasiewicz/integral-closure/resolution theory has not yet been isolated at the level required for a top-four claim.

The next revision should therefore not add another layer of generality.

It should make one of the two new ideas unavoidable:

1. prove a finite scalar theorem that is genuinely intrinsic, observable, necessary, or minimal; or
2. turn the residual/time divisorial contact into a canonical and genuinely new classification theorem for remote identification walls.

If either succeeds, the large existing body of exact binary/cubic mathematics could support a much stronger submission.
