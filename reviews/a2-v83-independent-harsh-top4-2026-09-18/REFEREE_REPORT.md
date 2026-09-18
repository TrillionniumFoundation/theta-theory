# Independent harsh referee report on A2 revision 83

**Manuscript:** *Action rigidity with selective detection*  
**Author:** Qian Qi  
**Review date:** September 18, 2026  
**Reviewed revision branch:** revision/a2-v83-sharp-clocks-global-quotient-2026-09-18  
**Review branch:** review/a2-v83-independent-harsh-top4-2026-09-18  
**Mathematical source commit declared by the revision:** c4867fc79d04db38ea887b66a9fba0965b008f62  
**Controlling preceding referee branch:** review/a2-v82-selective-detector-rigidity-independent-harsh-top4-2026-09-18  
**Controlling preceding referee commit:** b7075ecdeacb42befd55d4c732cbff4706fb4aca  
**Principal article:** papers/A2-v17-boundary-information-coarsening/rigidity_v83.tex  
**Requested standard:** the level expected of *Annals of Mathematics*, *Inventiones Mathematicae*, *Acta Mathematica*, or the *Journal of the American Mathematical Society*.

This is an author-requested independent referee-style report, not a commissioned journal report and not an editorial decision.

I compared the latest v83 revision branch against v82 and against the controlling v82 referee branch. The v83 mathematical source is additive over the v82 review history. I also compared the declared scientific commit c4867fc79d04db38ea887b66a9fba0965b008f62 to the current v83 branch head. The later branch commits modify workflow, verification, proof-ledger, response, requirements, and build-report material, but do not modify the principal v83 mathematical TeX files. Thus the mathematical object under review is well pinned.

I read the v82 referee report, the v83 response, the v83 proof ledger and verification record, the complete self-contained v83 principal article, the nonpolynomial section, the global inverse section, the geometric section, and the v83 bibliography. I also independently rederived the main divided-difference reduction, the two-moment interval inversion, the reduced-operator component formula, the q+2 local ambiguity mechanism, the nonpolynomial kernel identities, the covering synchronization argument, and the localized Hamiltonian ambiguity. I did not perform a formal proof verification and I do not treat the repository regression suite as a proof certificate.

The high-level conclusion is sharper than in the v82 report:

1. v83 is a real mathematical improvement and not merely another layer of exposition;
2. the old v82 permutation/gauge globalization gap has been substantially repaired;
3. the q+3 sharp-clock theorem appears internally coherent, and I do not find a short counterexample to it;
4. the new positive-kernel criterion gives a cleaner conceptual organization than the old five-clock Rolle argument;
5. nevertheless, I still would not recommend publication in any of the four leading general mathematics journals in the present form.

The reason is now primarily one of mathematical depth, natural scope, and theorem hierarchy, not an obvious fatal algebraic error.

---

## 1. Recommendation

**Recommendation at the four-leading-general-journals level: reject in the present form.**

Revision 83 closes several of the strongest correctness and presentation objections from revision 82. In particular, the new paper no longer asks the reader to accept a hand-waved global gluing of locally labelled noisy inverses. It constructs a component covering, centers the continuous gauge, synchronizes local labels through observable channel signatures, proves an exact permutation cocycle under sufficiently small perturbation, and then glues only after those identifications have been fixed. This is a material repair.

The scalar theorem is also stronger. The previous five-clock log-affine theorem has been replaced by a sharp q+3 theorem for polynomial log-detectors, with q+2 local nonidentifiability, and the log-affine case is reduced from five to four clocks. The manuscript also supplies a positive-kernel criterion for codimension-two sampled nuisance spaces and a nonpolynomial exponential example.

These are genuine advances relative to v82.

However, the resulting top-four case remains unconvincing. The central exact theorem is still assembled from three ingredients whose conceptual content is comparatively elementary or classical:

- simultaneous/joint diagonalization of a finite latent factorization;
- annihilation of a finite-dimensional nuisance space by divided differences or equivalent contrasts;
- injectivity of two weighted interval moments when the kernel ratio is strictly monotone.

The global perturbation theorem then adds finite-cover synchronization and partition-of-unity gluing on a fixed reference stratum. This is mathematically competent, but I do not see a theorem of the breadth or depth normally expected for a leading general journal.

The geometric theorem remains substantially conditional. Endpoint gates, canonical coordinates, the relevant return counts, their common deterministic lift, a phase cover, inverse-factor domains, collars, and—when a flow is considered—an existing global section are supplied. Once absolute generating sheets are recovered on such a supplied cover, the Bezout reconstruction of the underlying lift is close to formal. The new unsampled-region ambiguity correctly explains why some acquisition hypothesis is unavoidable, but it does not show that the strong supplied cover in the positive theorem is close to minimal or naturally recoverable from the stated measurements.

Finally, the only new geometric realization remains a deliberately constructed shear/suspension model whose detector and readout architecture is chosen to fit the algebraic theorem. A top-four paper needs either a substantially deeper general theorem or a serious natural application in which the observation model resolves a problem that is independently difficult.

For these reasons I would reject at the requested venue level even if every theorem in the principal article is ultimately correct.

---

## 2. What v83 genuinely fixes

The report should not repeat objections that are no longer accurate.

### 2.1 The v82 noisy gluing objection is substantially closed

The v82 report objected that local spectral inverses were being averaged without a coherent global treatment of permutation and gauge.

V83 now separates:

- local finite-dimensional inversion;
- observable channel-signature matching;
- exact transition permutations on overlaps;
- the permutation cocycle;
- fibrewise centering of the continuous detector gauge;
- gluing only after synchronization;
- a quotient metric over covering isomorphisms.

This is the right architecture. I do not regard the old statement that “smooth gluing functions” alone solve the problem as a fair description of v83.

### 2.2 The connectedness/monodromy issue is addressed correctly

V82 incorrectly leaned on connectedness where simple connectedness or covering triviality was needed. V83 explicitly treats the recovered latent family as a finite covering, distinguishes connectedness from triviality, and provides a three-cycle example over a circle. This is a conceptual improvement.

### 2.3 The four-versus-five clock question is answered

For polynomial log-detectors of degree q, v83 uses two order-(q+1) contrasts. They become two weighted moments of the oriented action interval. Their kernel ratio is

(T_1-s)/(T_{q+3}-s),

which is strictly monotone on the admissible action range. The resulting q+3 global inverse is cleaner than the previous five-clock log-affine argument.

The q+2 lower bound uses a square Jacobian in the polynomial coefficients plus one action while allowing the other action to vary. This is a valid local nonidentifiability mechanism and is enough for a worst-case lower bound.

### 2.4 The manuscript now admits the geometric scope instead of hiding it

The supplied/recovered table is useful. V83 no longer suggests that a global section, a global phase cover, inverse-factor domains, or caustic continuation have been recovered from the endpoint matrices. This is an important correction of scope.

### 2.5 The principal article is now readable as one paper

The 16-page principal article has a coherent theorem order:

1. sharp scalar theorem;
2. latent component reconstruction;
3. global quotient inverse;
4. return-lift consequence;
5. obstruction and physical example.

That is much better than the earlier archive-style presentation.

These improvements are real. They are also why my objections below are different from the controlling v82 objections.

---

## 3. Major concern: the central theorem is still too close to a classical two-moment/Chebyshev mechanism for a top-four general journal

This is the main editorial issue.

The new scalar mechanism is elegant, but after the detector nuisance is annihilated, the hard part is the following two-dimensional map:

(x,y) -> ( integral_y^x w, integral_y^x w r ).

The injectivity criterion is that r be strictly monotone. The Jacobian is the two-function Chebyshev determinant. The polynomial application chooses two consecutive divided differences, for which r is a fractional-linear function of the action variable.

This is a good observation. It also appears very close to classical one-dimensional Chebyshev/moment geometry.

The manuscript itself acknowledges that:

- divided differences are classical;
- the determinant condition is the two-function Chebyshev condition;
- the latent spectral step is classical;
- the generating-function conversion is classical;
- the Bezout identity for powers is elementary.

Once these acknowledgements are made, the burden is to show that the synthesis creates a theorem of genuinely broad mathematical consequence.

At present I do not think it does.

The q+3 theorem gives a sharp sample count for one particular finite-dimensional nuisance family. The positive-kernel theorem gives an iff criterion for one particular codimension-two sampled quotient. The nonpolynomial example shows that the mechanism is not literally polynomial. None of these, in my view, yet elevates the work to the conceptual scale of a top general mathematics journal.

### R83-M1. The paper needs a theorem whose novelty is not exhausted by two-function Chebyshev injectivity plus standard spectral factorization

A credible top-four revision would need at least one of the following kinds of advances:

1. a classification for substantially broader detector function spaces, not only a fixed sampled codimension-two quotient with a positive annihilator kernel;
2. a sharp clock-design theorem in which the deadlines themselves are chosen or optimized under structural constraints;
3. a multi-parameter action or multidimensional endpoint theorem whose inverse is not reducible to an oriented interval;
4. a natural geometric rigidity theorem in which the phase cover or relevant iterate organization is itself recovered;
5. a sharp impossibility theorem showing that the present finite-dimensional detector classes are in a precise sense maximal;
6. a nontrivial global statistical theorem with finite-sample rates, model-order uncertainty, and nuisance misspecification.

Without something of this scale, the present main theorem reads as a polished and useful specialized identifiability result rather than a top-four general-journal theorem.

---

## 4. Major concern: “detector classification” is materially narrower than the title suggests

Theorem thm:v83-classification is mathematically clean, but its scope should be described precisely.

It assumes:

- a fixed finite set of J deadlines;
- a d-dimensional sampled nuisance subspace D inside R^J;
- exactly J=d+2, so the annihilator is two-dimensional;
- the annihilator contains a Cauchy kernel that is positive on the entire action interval;
- the scalar problem concerns one ordered pair of unequal actions.

Under these assumptions, the ratio of the two annihilator kernels being strictly monotone is equivalent to injectivity of the two interval moments.

That is an iff theorem, but it is not yet a classification of detector families in the broader sense suggested by the paper's rhetoric.

### R83-M2. The theorem classifies a fixed sampled codimension-two scalar quotient, not the underlying detector function class

Different continuous detector spaces can have the same sampled subspace at one set of deadlines. Conversely, the same function space can produce different annihilator geometry at different node sets. The theorem therefore classifies the finite evaluation image at the chosen clocks, not the detector family independently of the sampling design.

A stronger result would characterize pairs:

(function space, deadline configuration)

for which action identifiability holds, and then derive the sampled theorem as a corollary.

### R83-M3. The positive-kernel hypothesis is structural and restrictive

The paper correctly says it is not automatic. But then the word “classification” should not be allowed to carry more weight than the theorem proves.

What happens when no annihilator kernel is strictly positive on the action interval?

What happens for annihilator dimension larger than two?

Can more than two contrasts yield global identification even when every two-dimensional subspace fails the stated positive-kernel criterion?

Can one formulate the general condition using total positivity, variation-diminishing properties, or a higher-order Chebyshev system?

These are exactly the questions that would turn the present result into a broad structural theorem.

As written, the result is a useful two-dimensional criterion, not a general classification of selective detection.

---

## 5. Major concern: the “global” stability theorem is global over the base domain but still local to a fixed exact reference stratum

Theorem thm:v83-global is much better than the v82 statement. I believe the distinction between local chart inversion and global quotient reconstruction is now largely correct.

Nevertheless, the word “global” can still be misunderstood.

The theorem fixes:

- one exact reference field;
- one visible rank B;
- one finite chart cover;
- selected nonsingular minors;
- selected spectral combinations;
- selected anchor pairs;
- a reference component covering and its monodromy type;
- quantitative lower bounds r, p_*, sigma_*, delta, gamma, mu, and s_*;
- fixed partition functions.

Only after these choices are fixed is an open C^m neighborhood constructed.

This is a **reference-local perturbation theorem whose output is global over Q**.

It is not a uniform global inverse theorem over the entire model class.

### R83-M4. State this distinction as a theorem-level limitation, not only in surrounding prose

The current text does partly say this, but the title and abstract still risk overselling the conclusion.

I would prefer language such as:

“global-over-Q stability on a fixed quantitative covering stratum”

rather than a bare “global inverse” unless a uniform model-class theorem is proved.

### R83-M5. The reconstruction is not yet an observable finite-data algorithm

The manuscript says exact observations can select admissible minors, spectra, and anchors, and compactness gives a finite cover. It also correctly notes that a finite noisy mesh would require sampling bounds between mesh points.

That caveat is important.

At present, the theorem assumes a C^m matrix field as data. It does not solve the practical problem of certifying the chart margins, rank gap, signature gap, or monodromy from finitely sampled noisy observations.

This is not a correctness objection to the stated functional-analytic theorem. It is a scope objection. The result should not be described as if it were already a robust observation procedure from realistic finite data.

### R83-M6. The quotient metric is useful but reference-dependent

The metric minimizes over isomorphisms of the nearby covering with the fixed covering type. The neighborhood is deliberately shrunk so the transition cocycle cannot change.

This is appropriate locally.

It also means that the theorem does not compare nearby data across rank changes or monodromy changes. The paper says this, but the scientific conclusion should reflect it prominently.

---

## 6. Major concern: the geometric theorem still assumes most of the difficult global geometry

Theorem thm:v83-return remains the weakest part of the top-four case.

It assumes, before the observation theorem is applied:

- endpoint gates in fixed canonical coordinates;
- which two positive return counts r and s are being observed;
- that the recovered sheets belong to powers of one deterministic lift;
- a phase cover sufficient to evaluate a fixed Bezout word;
- inverse-factor domains;
- fixed collars;
- regularity of the relevant mixed Jacobians;
- when a flow is considered, an existing transverse global section.

Under those assumptions, recovering absolute generating sheets is useful. But once the sheets of g^r and g^s are known on all domains needed by the word, the identity

g=(g^r)^u(g^s)^v

is not itself deep.

### R83-M7. The theorem still solves local sheet identification inside a supplied global organization

That is a legitimate inverse problem. It is not yet a global unmarked rigidity theorem.

The difficult questions remain outside the conclusion:

- how the phase cover is obtained from the observation process;
- whether all relevant sheets have been observed;
- whether missing folds or caustics exist;
- whether the supplied gates exhaust the needed iterate;
- whether the observed local powers really belong to one global lift without this being assumed;
- whether the inverse domains required by a negative Bezout exponent are actually observable.

The v83 paper is now honest about these assumptions, which is an improvement. But honesty about a limitation is not the same as overcoming it.

### R83-M8. The new unsampled-region theorem proves only a broad obstruction, not near-optimality of the positive hypotheses

The localized Hamiltonian perturbation is correct and useful. It shows that if an open phase region is not visited by the sampled orbit tubes, then unrestricted smooth exact dynamics can be changed there without changing the sampled lifted iterates.

This proves that some global acquisition condition is necessary.

It does **not** prove that the strong positive assumptions in thm:v83-return are close to necessary.

In particular it does not show that one must supply:

- the exact gate cover used in the theorem;
- the exact inverse-factor domains;
- the common-lift identification;
- the global section;
- the specific collars.

Therefore the negative theorem and positive theorem still leave a large conceptual gap.

A top-four geometric result should narrow that gap.

---

## 7. Major concern: the physical/geometric example remains engineered around the observation model

Proposition prop:v83-shear is a good consistency example. It verifies that the observation hypotheses are not empty, includes an action crossing, and persists under small exact perturbations on restricted orbit tubes.

I do not regard it as a serious geometric application.

The shear

F(x,p)=(x+p^3-p,p)

is explicitly integrable. Its branches, primitive, and action crossing are all available in closed form. The detector rate is then deliberately chosen as a function of p so that the clock responses separate the coincident-action branches. The readout columns are chosen as normalized Vandermonde-type vectors so that full rank is automatic.

This is an excellent test model.

It does not show that the theorem resolves a naturally occurring inverse problem.

### R83-M9. A top-four paper needs at least one application whose difficulty exists independently of this algebraic model

Examples that would materially change my assessment include:

- a nontrivial class of billiards with an observation law derived from a realistic boundary measurement;
- a Reeb or Hamiltonian rigidity theorem where a global return structure follows from independently natural hypotheses;
- a scattering or travel-time problem in which selective detection is a genuine nuisance rather than a designed factor;
- a new rigidity theorem for a known class where previous methods recover only marked or calibrated data and the present method removes those assumptions.

At present the paper has a synthetic model demonstrating consistency, not an application demonstrating depth.

---

## 8. Major concern: the literature positioning is still far too thin for a top-four novelty claim

The principal v83 bibliography contains only seven entries:

- three latent-variable / spectral-identification references;
- de Boor on divided differences;
- Karlin--Studden on Chebyshev systems;
- Geiges on contact topology;
- Marsden--West on generating-function mechanics.

That is not enough for a paper making claims across:

- finite-dimensional inverse problems;
- latent-mixture identifiability;
- Chebyshev and moment geometry;
- sharp sampling complexity;
- nonlinear stability;
- covering-space synchronization;
- symplectic/contact inverse dynamics.

### R83-M10. The novelty audit is not yet credible

The paper needs a substantially deeper comparison with the relevant literature.

For the scalar theorem, the authors should locate the result relative to generalized moment problems, total positivity, T-systems, rational interpolation, and related finite-rate identifiability arguments.

For the latent matrix step, the exact novelty of using two unknown channels with varying mixture weights should be separated from existing observable-operator and tensor-identifiability results.

For the global stability theorem, the paper should compare its quotient/bundle viewpoint with established synchronization, eigenbundle perturbation, and stratified inverse-map methods.

For the geometry, it should situate the result within actual inverse rigidity literature rather than only citing a mechanics reference and a contact-topology textbook.

A top-four referee must be able to tell exactly which theorem is new and why it is not a disguised special case of an established framework. The present bibliography does not provide that confidence.

---

## 9. Major concern: the sharpness theorem is mathematically valid but not as conceptually strong as the paper sometimes suggests

The q+2 lower bound is local.

At a reference point with x != y, the Jacobian with respect to the q+1 polynomial coefficients and one action is nonsingular. Therefore, when the other action is varied, the implicit function theorem gives a local one-parameter level set with unchanged sampled scalar data.

This is enough to prove worst-case nonidentifiability with q+2 clocks.

But it does not describe the global fibre geometry.

### R83-M11. Strengthen the sharpness theorem if it is to carry major editorial weight

The paper would be stronger with:

- an explicit closed-form ambiguity family for general q, or at least q=1;
- a classification of connected components of the q+2 fibre;
- a statement of when additional side conditions remove the ambiguity;
- a minimax lower bound under noise, not only exact nonidentifiability;
- an extension to misspecified detector classes.

As it stands, “sharp q+3” is correct in a worst-case exact-identifiability sense, but the lower bound itself is an elementary local dimension/Jacobian mechanism.

That is useful. It is not, by itself, a top-four-level sharpness theory.

---

## 10. Major concern: the theorem stack remains a synthesis rather than one inevitable rigidity principle

The paper has become much more coherent, but the theorem hierarchy still has a modular character:

1. finite latent matrix factorization;
2. scalar interval inversion;
3. bundle synchronization;
4. exact-lift composition;
5. a synthetic return example.

Each module is understandable.

What is missing is the theorem that makes the reader feel that these modules are manifestations of one unavoidable mathematical structure rather than a successful assembly.

### R83-M12. The paper needs a stronger unifying invariant

The positive-kernel ratio is a candidate, but it currently lives only in the scalar sampled nuisance quotient.

A stronger paper would show that the entire observation problem is controlled by a natural invariant—perhaps a variation index, a total-positivity class, an information-geometric object, or a bundle-valued moment map—and then derive the finite polynomial case, the nonpolynomial case, the covering theorem, and the geometric consequence from that one structure.

At present the synthesis is clever but not inevitable.

That distinction matters at the requested journal level.

---

## 11. Technical comments on correctness and exposition

The following are not all fatal, but they should be repaired in any further revision.

### R83-T1. Tighten the converse proof of Lemma lem:v83-interval

The converse is plausible and I believe it is correct, but the orientation argument is compressed.

For each sufficiently small d, H_d is continuous and injective, hence strictly monotone. To conclude that R is globally monotone, one should explicitly argue on an arbitrary compact subinterval K of I':

1. choose d small enough that K+[0,d] remains in I';
2. use one pair on K where R has unequal values to fix the orientation of H_d for all sufficiently small d;
3. note that H_d/d converges uniformly to R on K;
4. pass to the limit to obtain monotonicity of R on K;
5. exhaust I' by compact intervals.

The current prose sketches this, but a theorem advertised as an iff classification deserves a completely explicit argument.

### R83-T2. Clarify the basis-invariance statement in thm:v83-classification

The determinant sign condition is basis-invariant up to multiplication by the determinant of the basis change.

The ratio k_1/k_0 formulation assumes the first kernel in the chosen basis is positive. State explicitly that among bases with positive first kernel, the ratio changes by a real fractional-linear transformation whose denominator stays nonzero, so strict monotonicity is preserved.

### R83-T3. Specify the regularity of the gauge functions

The gauge

a_b -> h a_b,
theta_{b,nu} -> theta_{b,nu}+rho_nu

is described fibrewise at each endpoint.

If h and rho_nu are allowed to vary with z, state their required C^m regularity explicitly. If they are only pointwise ambiguity parameters, explain why centering produces a C^m representative globally on the component covering.

### R83-T4. Separate exact model identifiability from the off-model target space more cleanly

The off-model local extension can have signed channel entries when the exact channel lies on the probability-simplex boundary.

This is mathematically acceptable for an ambient smooth extension, but then the target of the off-model reconstruction is not literally the original statistical parameter space. State the ambient affine target space explicitly.

### R83-T5. The rank threshold is a reference-margin theorem, not model-order discovery

Corollary cor:v83-error assumes a nonzero singular-value margin sigma_*.

Thresholding at sigma_*/2 recovers B only because sigma_* is already known as a reference margin.

Do not let the prose suggest that the theorem solves model-order selection from unknown noisy data without a signal-strength hypothesis.

### R83-T6. Make the dependency of stability constants explicit

The constant C in the global estimate depends on:

- the finite chart cover;
- partition-of-unity C^m norms;
- minor inverse bounds;
- spectral gaps;
- probability floors;
- action residual bounds;
- anchor separation;
- channel signature gap;
- centered parameter bounds.

A compact dependency statement would make the theorem easier to audit.

### R83-T7. Clarify connected versus disconnected total component coverings

The base Q is connected, but the B-sheeted component covering itself may be disconnected.

The statement that a covering isomorphism is determined by its action on one fibre is correct in the finite covering setting, but it would be helpful to say explicitly that the admissible fibre permutation must commute with the monodromy action; not every permutation of the fibre necessarily extends to a covering automorphism.

### R83-T8. Define the local-map word when Bezout exponents are negative

For local maps with restricted domains, the expression

(g^r)^u (g^s)^v

is not merely a formal group identity. The nested domains and order of composition matter.

The theorem says the required inverse-factor domains and collars are supplied; write the actual domain recursion once so the local meaning of the word is completely unambiguous.

### R83-T9. The return theorem assumes absolute primitives, not merely generating functions up to constants

This is central to the claim of recovering absolute return time.

State prominently that the observation model supplies the actual action/primitive normalization through the clock factor T-W, rather than only a type-I generating function modulo an additive branch constant.

### R83-T10. In cor:v83-contact, distinguish a local covered suspension from a full global suspension

If the reconstruction covers only a target subset of the section, the phrase “its section-preserving strict contact suspension” can be read globally.

Say explicitly whether the conclusion is a suspension germ/restriction on the covered target or a global contact manifold.

### R83-T11. State the phase-domain hypotheses in prop:v83-unobserved more explicitly

The Hamiltonian perturbation is compactly supported in O, and small time ensures it remains inside the canonical phase domain.

Add this domain-invariance sentence to avoid an implicit extension of the phase space.

### R83-T12. The nonpolynomial proposition should separate scalar and multi-component hypotheses

The scalar positive-kernel criterion identifies one unequal-action pair.

The multi-component theorem additionally requires spectral separation of every pair of component trajectories.

The proof supplies this for the exponential family, which is good. State this separation of roles in the proposition statement or immediately before it.

### R83-T13. The nonpolynomial family still has a known shape parameter lambda

The proposition assumes lambda>0 is known and only beta_b is unknown.

This is a legitimate example, but the discussion should not imply that the entire nonpolynomial detector shape is unknown. Recovering lambda jointly would be a substantially stronger problem.

### R83-T14. The principal bibliography is too small even as exposition

Even if no theorem is changed, the literature section should be expanded enough that a reader can independently audit novelty.

Seven references are not adequate for the breadth of claims.

### R83-T15. Keep verification language out of the mathematical significance argument

The revision does this better than earlier rounds.

Continue to keep native builds, regression counts, source hashes, and CI status in the repository verification files. They are useful for reproducibility but irrelevant to whether the theorem is deep enough for a leading general journal.

---

## 12. Independent assessment of the principal proofs

For clarity, here is my present mathematical assessment of the new proof blocks.

### 12.1 Sharp scalar inverse

I do not find a defect in the main q+3 argument.

The two consecutive order-(q+1) divided differences annihilate the polynomial nuisance. The resulting kernels are positive below the first clock, and their ratio is strictly monotone. This gives a globally injective two-moment map for the oriented action interval.

The full square Jacobian also appears correct.

### 12.2 q+2 lower bound

The local IFT argument is valid as a worst-case exact-identifiability obstruction.

It should be understood as local nonidentifiability, not a global classification of all ambiguities.

### 12.3 Component recovery

The reduced-operator calculation is standard and appears correct.

The argument that the joint ratio vectors are pairwise distinct uses q+2 equal values and the nonvanishing (q+1)-st derivative when actions differ, or polynomial rigidity when actions agree. I do not see a short counterexample.

### 12.4 Global quotient inverse

The v82 gap has been materially repaired.

The key improvement is that local reconstructions are not averaged before their labels are synchronized. Nearest-neighbor matching in the original readout space, under a uniform channel-column gap, gives an exact transition cocycle on a sufficiently small reference neighborhood. After gauge centering, partition-of-unity gluing is then legitimate.

I regard this as a correct local-around-reference architecture unless a subtler bundle-regularity issue emerges.

### 12.5 Nonpolynomial example

The kernel formulas and monotonicity claim for the exponential log-detector are consistent.

The separate spectral-separation argument is necessary and is supplied.

### 12.6 Unsampled-region ambiguity

The left composition by a compactly supported exact Hamiltonian perturbation outside the finite sampled orbit tube preserves the recorded lifted iterates by induction and changes a designated unsampled target.

This is a sound obstruction in the stated smooth exact-lift class.

Thus my negative recommendation is not based on an assertion that these principal arguments are obviously false.

---

## 13. Status of the main v82 referee objections

A useful way to summarize v83 is:

| v82 issue | v83 status |
|---|---|
| No coherent noisy permutation/gauge gluing | **Substantially closed** |
| Norm not quotient-invariant | **Closed in the fixed covering stratum** |
| Spectral-chart changes not synchronized | **Substantially closed** |
| Local and global stability conflated | **Closed** |
| Connectedness incorrectly used for global labels | **Closed** |
| Local sheet recovery confused with phase-cover recovery | **Now correctly scoped, not solved** |
| “No cross-gate labels” overstated as global unmarked rigidity | **Now correctly scoped, not solved** |
| Detector family lacks structural criterion | **Partially closed by positive-kernel theorem** |
| Polynomial extension too interpolation-like | **Improved, but the new theorem remains classical in mechanism** |
| Four-versus-five clock question open | **Closed: four is sharp for q=1** |
| Shear is engineered | **Still true; persistence added** |
| Natural billiard consequences remain conditional/marked | **Still true** |
| Literature comparison too thin | **Still a major issue** |
| Latent-variable priority unclear | **Improved** |
| Theorem hierarchy diffuse | **Improved but not top-four compelling** |
| Principal article incoherent | **Closed** |
| Revision-history overload | **Improved by separate principal/expanded entries** |

This is why the present report should not be read as “v82 again.” V83 really does close multiple old objections. It also exposes more clearly what remains.

---

## 14. What would justify another top-four review

I would not recommend another top-four-style round based on incremental polishing alone.

A materially stronger revision should contain at least one genuinely new theorem of broader scope. The most promising directions are:

1. **General detector-space theory.** Move from a fixed codimension-two sampled quotient to a function-space theorem, ideally with higher annihilator dimension and a sharp necessary-and-sufficient condition.

2. **Observation-driven geometry.** Recover some nontrivial part of the phase cover, iterate organization, or common-lift structure from the data rather than supplying it.

3. **Natural application.** Prove a new rigidity theorem for an independently important Hamiltonian, Reeb, billiard, or scattering class.

4. **Uniform robust inference.** Replace reference-local C^m stability with a theorem that gives observable margin certification, finite-sample rates, or minimax sharpness under noise and model-order uncertainty.

5. **A stronger impossibility boundary.** Characterize the maximal nuisance classes for which absolute action remains identifiable, rather than showing only that completely free deadline dependence is impossible.

6. **Serious novelty audit.** Expand the literature comparison until each principal theorem has a precise closest-predecessor statement and a clear explanation of what is not already contained in classical moment/T-system or latent-factor methods.

Without one of these, I would regard further rounds as refinement of a specialized result rather than movement toward the requested journal class.

---

## 15. Final verdict

Revision 83 is the strongest and cleanest version of this A2 line that I have reviewed.

It deserves explicit credit for three things:

- the sharp q+3 clock theorem is better than the previous five-clock result;
- the component-covering globalization repairs a genuine logical weakness;
- the paper now states the geometric acquisition assumptions honestly.

Those are substantial improvements.

They are not enough for the requested editorial level.

At present the paper's deepest exact theorem reduces to a classical two-function Chebyshev/interval-moment mechanism after a classical latent spectral decomposition, while the geometric theorem remains conditional on a supplied phase organization and the only new realization is an engineered model. The bibliography and novelty analysis are not yet broad enough to overturn that assessment.

**Recommendation: reject in the present form at the Annals / Inventiones / Acta / JAMS level.**

I would be open to reassessing a future manuscript only if it adds a theorem that changes the conceptual scale of the work, not merely another layer of sharp constants, examples, or verification infrastructure.
