# Second Independent External Harsh Referee Report

## General Theta Foundations I: Constructive Causal Deficiency and Physical Testing — Revision v16

**Author:** Qian Qi  
**Repository:** TrillionniumFoundation/theta-theory  
**Reviewed branch:** revision/general-theta-foundations-i-v16-constructive-causal-certification-referee-ready-2026-09-23  
**Reviewed HEAD:** 5941223e297f6c54583d729cc292831c183277e9  
**Immediate mathematical base:** v15 certified-physical-comparison, 09d5540897d592a5e434f7431bfff470b4ebad1a  
**Review date:** 23 September 2026  
**Requested standard:** Annals of Mathematics / Inventiones Mathematicae / Journal of the AMS / Acta Mathematica level  
**Review type:** second independent, external-referee-style, pipeline-aware harsh audit

**Provenance and independence note.** This is an owner-requested, AI-assisted external-referee-style report, not a report commissioned by a journal. I reviewed the frozen v16 manuscript, the three genuinely new theorem files, the v13–v15 theorem spine imported by v16, the response/proof/history ledgers, the executable certificates, the typed eleven-component dependency graph, the historical B4 and C2 closure documents, and the already deposited v16 harsh report. The prior report is treated as historical input rather than as evidence of correctness. I re-derived the principal v16 finite inequalities and independently recomputed the two main scalar examples before reaching the assessment below.

---

# Recommendation

## Reject in the present form at the requested top-four general-mathematics standard

The reason is not that the manuscript is empty or obviously false. To the contrary, I find a substantial part of the fixed-finite theorem spine technically credible:

- the private finite problem is correctly kept nonconvex at the original state/selector signature;
- the power-weighted approximation of a finite maximum is sound;
- the stated Bernstein coefficient identity and eventual strict positivity mechanism are sound at a positive margin;
- the private two-time value \(\sqrt2-1\) and hidden-two-selector value zero check out;
- the stateless presentation triangle used to transfer finite certificates to physical experiments is mathematically legitimate under the inherited v15 hypotheses;
- the explicit collective hard-sphere formulas are consistent with conservation of total momentum;
- the displayed series for the marked scalar deficiency numerically evaluates to approximately \(0.20580912288771521416\), inside the deposited rational interval;
- the total-variation-to-logarithmic-moment estimate is correct.

The top-four problem is deeper. The manuscript still does not establish a theorem of the conceptual magnitude suggested by the title **General Theta Foundations I**, by the language of intrinsic/constructive/physical causal certification, or by its proposed role in an eleven-paper program. The strongest new finite statement is a resource-aware use of a classical polynomial positivity mechanism after a representation-dependent cube parameterization. The strongest new physical example is dynamically solvable precisely because the collision interaction cancels from the relevant collective mode. The physical deficiency example is positive precisely in a regime where the private/hidden/visible resource architecture is inert. The main physical transfer theorem is largely inherited from v15. The exponential theorem is a sharp but elementary stability estimate. The historical B4 and C2 gates remain mathematically independent and open.

My conclusion is therefore sharper than “the proofs need polishing.” The paper needs either a **qualitatively stronger structural theorem** or a **qualitatively harder physical theorem** before it is plausible at the requested venue level.

---

# 1. Exact review object and mathematical delta from v15

The frozen v16 object is real and materially deposited. This is an important improvement over the earlier branch-scope confusion. The canonical article, complete development, source manifests, exact certificate arrays, build receipts, and pinned inherited inputs are present.

However, the v16 mathematical delta must be separated from the inherited bulk. The canonical source imports, essentially unchanged, the v13 intrinsic deficiency theory, v14 local/residual certificates, and the v15 witness, task-tolerance, finite-presentation, enriched-certificate, constructive-hard-sphere, physical-certification, and physical-data modules.

The genuinely new mathematical files are concentrated in:

1. nonlinear-testing.tex;
2. collective-hard-spheres.tex;
3. physical-testing.tex.

Thus v16 adds three main ingredients:

- a global strict polynomial certificate hierarchy for the finite private nonconvex problem;
- a solvable collective hard-sphere example with an exact marked deficiency and explicit approximation rate;
- a composition of the new finite lower certificate with the already established v15 physical bridge, plus an exponential-value stability estimate.

That is a meaningful revision. It is not the birth in v16 of the full end-to-end physical certification architecture.

This distinction must be visible in the article itself, not recoverable only from Git history.

---

# 2. Re-derivation of the finite theorem: credible mathematics, but the conceptual claim is too large

The finite theorem starts from a fixed finite resource signature and writes

\[
F(q)=\max_i f_i(q)
\]

over the original executable simulator rows. The stick-breaking map \(q(x)\) is polynomial and onto the product of row simplexes. With \(h_i=f_i\circ q\), \(g_i=(1+h_i)/2\), and the empty event included, the manuscript defines

\[
A_p(x)=\frac{\sum_i g_i(x)^p h_i(x)}
{\sum_i g_i(x)^p}.
\]

If \(b=\max_i g_i\) and \(r_i=g_i/b\), then

\[
A_p=2b\frac{\sum_i r_i^{p+1}}{\sum_i r_i^p}-1.
\]

The Hölder/log-convexity argument indeed yields a monotone approximation to \(\max_i h_i\) and therefore

\[
\delta=\sup_p\min_x A_p(x).
\]

I do not see a hidden convexification in this step. The feasible private image remains the original nonconvex image of executable rows.

Likewise, for

\[
P_{p,L}(x)=\sum_i g_i(x)^p(h_i(x)-L),
\]

strict positivity at a positive margin can be converted into eventual strict positivity of all tensor Bernstein coefficients. The coefficient formula

\[
b_{\alpha,n}=\sum_k c_k\prod_j
\frac{\binom{\alpha_j}{k_j}}{\binom{n}{k_j}}
\]

and the manuscript's \(O(1/n)\) coefficient-versus-grid bound are consistent with the elementary sampling-with/without-replacement argument.

This is the strongest technical success of v16.

It still does not justify the conceptual framing currently attached to it.

## 2.1 The object called a “dual” is not a dual in the standard variational sense

The parameter \(p\) is a smoothing/concentration parameter. The weights

\[
g_i(x)^p/\sum_j g_j(x)^p
\]

depend on the candidate primal simulator \(x\). There is no independently feasible dual object, no minimax exchange over an adversarial testing law, no complementary slackness, no dual attainment theorem, and no separation of the original nonconvex feasible image by an independent functional class.

The manuscript itself admits that the weights are not an exchanged constant test mixture. That admission is mathematically correct and terminologically revealing.

At the requested venue level, “endogenous polynomial testing dual” risks confusing an exact max-approximation/certificate transform with an actual duality theory.

The paper should either construct an independent variational dual object, or rename the result as what it presently proves: a **complete strict positive-polynomial lower-certificate hierarchy for a fixed finite causal resource signature**.

## 2.2 “Complete” is only a strict-margin completeness theorem

The finite algebraic result is complete for rational \(L<\delta\): some finite \(p\) and sufficiently high Bernstein degree provide a strict certificate.

It does **not** prove that equality \(L=\delta\) has a finite nonnegative Bernstein certificate, nor does it give a finite decision procedure for zero margin or exact equality. The manuscript is aware of this, and the dovetailed interval procedure correctly avoids claiming otherwise.

This boundary must remain explicit wherever the paper uses phrases such as “complete certificate,” “exact constructive testing,” or “finite certificate equivalence.” The exact statement is semidecision/completeness for **strict** lower levels plus independently enumerable upper witnesses.

For a foundational paper, the distinction between strict semidecision and exact boundary decision is not cosmetic.

## 2.3 The certificate existence theorem is coordinate-dependent in exactly the place where “intrinsic” language matters

The deficiency value is intrinsic to the declared resource signature. The Bernstein certificate hierarchy is not.

It depends on:

- the chosen stochastic-row realization;
- the order in which outcomes are stick-broken;
- the raw cube dimension \(D\);
- the polynomial degrees created by that parameterization;
- the coefficient norm \(C(P)\);
- the tensor Bernstein degree;
- the resulting \((n+1)^D\) coefficient count.

Different onto polynomial parameterizations of the same behavior image can produce radically different degrees, coefficient norms, and certificate sizes while representing the same intrinsic resource problem.

The paper has a v15 theorem controlling the **number of tests** by an intrinsic behavior dimension. V16 does not produce an analogous invariant theorem for polynomial certificate size.

This is a serious conceptual gap. A theory advertised as intrinsic should not have its principal constructive complexity controlled only by a coordinate artifact without saying so.

A genuinely strong next theorem would bound certificate support/degree/bit size in intrinsic behavior dimension, resource width, horizon, or another representation-invariant quantity.

## 2.4 “Constructive” presently means effective dovetailing, not a quantitative construction law

The shipped two-variable certificate already uses \(p=12\), tensor degree \(96\), and \(9{,}409\) coefficients merely to prove the rational lower level \(2/5\).

For general causal signatures, the coefficient count grows as \((n+1)^D\), while \(D\) itself contains all row coordinates of the chosen realization. The paper makes no polynomial-time claim, and it should not.

But once complexity is left uncontrolled, “constructive” has the precise meaning:

> there is an effective terminating search for each requested positive gap under fixed finite rational data.

That is useful. It is weaker than a structural complexity theorem. The exposition should not blur these meanings.

---

# 3. The closest polynomial-positivity literature is not optional background

The current bibliography says that Bernstein positivity and degree elevation are classical, but it does not make a theorem-level comparison with the literature most directly adjacent to the v16 algebraic engine.

At minimum the paper should engage:

- E. de Klerk and M. Laurent, “Error Bounds for Some Semidefinite Programming Approaches to Polynomial Minimization on the Hypercube,” SIAM J. Optim. 20 (2010), 3104–3120, DOI 10.1137/100790835. Their abstract explicitly identifies multivariate Bernstein approximation as a tool giving constructive proofs and degree bounds for positivity certificates on the hypercube.
- M. Laurent and L. Slot, “An effective version of Schmüdgen’s Positivstellensatz for the hypercube,” Optim. Lett. 17 (2023), 515–530, DOI 10.1007/s11590-022-01922-5.
- E. de Klerk and J. C. Vera, “The link between 1-norm approximation and effective Positivstellensätze for the hypercube,” Numer. Algebra Control Optim. 16 (2026), 84–104, DOI 10.3934/naco.2024060, which explicitly refines effective degree dependence in terms of coefficient 1-norm and polynomial parameters.

I am not asserting that these papers contain the present causal-resource theorem. They do not, from the material inspected. That is precisely why the subtraction is necessary: the manuscript must state what remains new **after** generic effective hypercube positivity technology is removed.

A top-four novelty claim cannot rest on “the algebraic ingredients are classical” without locating the nearest quantitative results and explaining why the causal structure forces a genuinely new theorem rather than a direct encoding followed by known positivity machinery.

This is a publication-level blocker, not a bibliography nicety.

---

# 4. The two-time private/hidden/visible example is correct and important, but still only a finite witness example

The delayed binary target is a good example. The private width-one objective

\[
\max\{0,\tfrac12-pq,\tfrac12-(1-p)(1-q),p+q-2pq\}
\]

has minimum \(\sqrt2-1\). A hidden fair selector between the two deterministic constant paths reproduces the target exactly. The exposed selector restores the fiberwise obstruction, so visible randomization does not erase the private gap. The target lies in the convex hull of deterministic private behaviors, so fixed constant test mixtures cannot separate it.

This successfully demonstrates that free convexification destroys the intended private resource notion.

However, it does not establish that the new Bernstein hierarchy is the canonical geometry of the resource image. It shows only that **some nonlinear certificate is necessary**.

The top-four-scale missing theorem is the geometry behind this example: an intrinsic characterization of the nonconvex causal behavior image, a sharp dimension/width law, a resource-sensitive nonlinear separation principle, or a certificate-support theorem. The current hierarchy is complete but generic and potentially enormous.

---

# 5. The new hard-sphere example is collision-compatible but essentially collision-insensitive

This is the most important physical criticism.

The new observable is

\[
\vartheta=\frac{2\pi}{\ell}\sum_iq_{i,1},
\qquad
X=N^{-1/2}\sum_i v_{i,1},
\qquad
f=\cos\vartheta.
\]

Because elastic hard-sphere collisions conserve total momentum,

\[
U(t)f=\cos(\vartheta+\omega Xt).
\]

This identity is valid. It also removes the difficult interaction from the observable dynamics.

The effective reduced dynamics are simply

\[
(\vartheta,X)\mapsto(\vartheta+\omega Xt,X).
\]

No collision itinerary, sphere diameter, recollision graph, collision frequency, scattering angle, or BBGKY hierarchy enters this orbit formula.

Indeed, in the explicit numerical corollary:

- the marked deficiency \(d(\tau)\) depends on \(\tau=\omega\Delta\);
- the residual \(R=\omega^2\);
- neither quantity depends on the sphere diameter except through the trivial requirement that the configuration space be nonempty.

This is decisive evidence that the “interacting hard-sphere” language is ambient rather than dynamically essential for the new example.

The manuscript does say it is a solvable collective mode. That caveat is welcome. But the physical rhetoric must go further: this example does not test whether the certification machinery can control genuinely collision-generated information.

## 5.1 The nonzero residual is not an interaction residual

The one-dimensional trial residual \(R=\omega^2\) is the projection residual of \(L f\) outside the span of \(f\).

The same residual occurs in the reduced free collective system. It is not a measure of collision complexity, collision-induced memory, or interaction strength.

A nonzero residual and a positive deficiency occurring in the same ambient hard-sphere phase space are not enough to demonstrate a nontrivial interaction-sensitive bridge.

## 5.2 The \(2^k\) to \(k+1\) word collapse is a symmetry reduction, not a solution of generic feedback combinatorics

The controlled word depends only on the signed clock

\[
s(w)=\Delta\sum_{j=1}^k\prod_{i=1}^j a_i.
\]

This is a useful exact simplification. It occurs because the only controlled latent variable relevant to the observable is the sign of a conserved one-dimensional total momentum.

The manuscript should not present this as evidence that the general collision/feedback word explosion has been controlled. It has been bypassed by a special symmetry.

---

# 6. The exact physical deficiency is positive precisely where the resource architecture is inert

The finite example and physical example do not yet meet in one nontrivial model.

For the exact physical theorem:

- the action is chosen before an informative report;
- the source report is independent of the actual mark \(W\);
- global reversal leaves the relevant marked target law unchanged by symmetry;
- every source-generated report is independent of \(W\);
- hidden persistent selection cannot help;
- visible selection cannot help;
- feedback has no informative earlier observation on which to act.

Consequently the same scalar deficiency holds for every nonempty private, hidden-selector, and visible-selector signature.

This is mathematically valid. It is conceptually the opposite of the causal resource phenomenon highlighted by the finite theorem.

The lower bound is essentially a static correlation obstruction: the target correlates \(W\) and \(Y\), while the source simulator has no access to \(W\). The stateless simulator attains the upper bound by drawing the target's unconditional marginal.

Thus:

- the finite example shows a genuine private/hidden/visible gap but has no physical dynamics;
- the physical example has an exact positive marked deficiency but **no resource gap** and no operative causal information structure.

The paper says the statistical and microscopic conclusions are “joined at the same register and selector budgets.” They are joined formally through the transfer theorem, but not in the strongest sense suggested by the narrative.

A decisive physical theorem would exhibit, in one microscopic system:

1. collision-sensitive evolution of the informative observable;
2. feedback that changes future information;
3. a strict difference between at least two of private/hidden/visible resources;
4. a same-budget impossibility certificate;
5. convergent physical approximation with explicit error;
6. preferably a parameter-uniform or scaling statement relevant to the downstream analytic program.

V16 does not yet do this.

---

# 7. Theorem v16-main is primarily a new finite lower module plugged into an inherited v15 transfer theorem

The v16 physical interval

\[
\max\{0,L-a-c\}\le\delta_b(E,F)
\le\min\{1,U+a+c\}
\]

is correct under the stated two-sided stateless presentation errors.

But this stability mechanism is already the main content of v15 theorem v15-main. V15 already proved:

- finite report quantization;
- marked joint-prefix rationalization;
- two-sided stateless marked comparison;
- preservation of the original state/selector budget;
- transfer of finite lower and upper bounds;
- an effective convergent interval procedure under graph/integration data.

V16 changes the **finite lower-certificate module** from the v14/v15 local-cell method to the new global polynomial positivity hierarchy and provides a new explicit collective class.

That is a meaningful strengthening. It is not a new physical transfer principle.

The paper should state this with theorem-level precision. A reader should not need repository archaeology to learn which half of the “main physical theorem” is inherited.

---

# 8. A quantifier issue in the word “terminating” should be cleaned up

The general v16 physical theorem says, in effect, that rational finite presentations with two-sided errors \(a_j,c_j\to0\) and computable upper bounds yield a terminating dovetailed search for an interval of any prescribed positive width.

For an algorithmic theorem, the input structure must be explicit.

The statement should specify that:

- the sequence of presentations is effectively enumerable;
- each rational instrument can actually be computed from its index;
- the certified error bounds can be effectively produced and compared with a requested rational tolerance;
- the finite certificate/upper-table enumeration is uniform in the presentation index.

The inherited v15 hard-sphere specialization appears designed to supply these effective operations. The abstract general theorem should state them rather than silently moving from existence of approximants to an executable enumeration.

This is not necessarily a fatal flaw in the mathematical idea, but at a paper centered on “constructive certification” the computability quantifiers must be written with the same care as probabilistic quantifiers.

---

# 9. The exponential theorem is a stability lemma, not a nonlinear kinetic bridge

The estimate

\[
\left|
\frac1\beta\log E_P e^{\beta h}
-
\frac1\beta\log E_Q e^{\beta h}
\right|
\le
\frac1\beta
\log\left(1+\varepsilon(e^{\beta\operatorname{osc}(h)}-1)\right)
\]

is correct and sharp for bounded \(h\).

Its mathematical role is to quantify the presentation accuracy needed when a bounded payoff is exponentiated.

It does not provide:

- exponential tightness;
- a large-deviation principle;
- a dynamic action;
- a Hamiltonian identification;
- a Nisio semigroup;
- nonlinear resolvent comparison;
- particle-number-uniform estimates;
- microscopic-to-kinetic nonlinear-semigroup convergence.

Calling this a “B4 edge” is acceptable only if “edge” means a scoped accuracy-transfer prerequisite. It is not evidence that the hard B4 theorem has been materially proved.

---

# 10. Pipeline audit: the repository itself shows that GTF-I is an interface theory, not yet the mathematical foundation of the eleven-paper chain

I inspected the v16 typed graph and the historical Round-17 closure documents.

The graph has eleven components: A1, A2, A3, A4, B1, B2, B3, B4, C1, C2, D1. Its own fields repeatedly record full_historical_target_closed_by_v16 = false.

The current state, as represented by the repository, is approximately:

| Component | What GTF-I presently supplies | What remains outside v16 |
|---|---|---|
| A1 | protocol/task adapters and finite decision-resolution consequences | full historical A1 target not closed by v16 |
| A2 | historical adapter only; primary geometry explicitly independent | primary A2 chain not consumed or derived |
| A3 | conditional interface | historical analytic/geometric target independent |
| A4 | model-scoped/operator-domain consumer | Sinai spectral/renewal-memory closure not supplied |
| B1 | conditional interface | hard analytic target independent |
| B2 | conditional interface | hierarchy/scaling results not generated by GTF |
| B3 | conditional interface | closed-range/balance structure independent |
| B4 | fixed-particle microscopic consumers, physical certificates, v16 collective acquisition edge | dynamic action, nonlinear resolvent, m-dissipativity, BBGKY corrector, nonlinear Trotter–Kato and kinetic scaling |
| C1 | finite/computable acquisition consumer | local asymptotic/risk-sensitive saddle structure not implied |
| C2 | fixed operator-domain/memory consumer | strict duality, covariant form response, rigidity and optional-projection limit independent |
| D1 | model-scoped consumer | no full historical D1 closure supplied |

The Round-17 B4 source is particularly clear. Its closure theorem requires, among other things:

- compact dynamic action sublevels;
- a kinetic Nisio semigroup;
- a nonlinear resolvent identity;
- full range and \(m\)-dissipativity;
- comparison;
- a single BBGKY graph-core hierarchy corrector sequence;
- nonlinear Trotter–Kato convergence.

The Round-17 C2 source separately requires:

- weighted strict duality;
- covariant type-(B) resolvent response on transported form bundles;
- dissipative compressed resolvent/memory response;
- rigidity;
- optional-projection convergence under changing filtrations.

These are not consequences of the v16 finite-resource comparison theorem.

The v16 pipeline checker itself correctly says that it verifies source identity, preserved fields, and label existence rather than analytic truth. That limitation is essential.

A typed dependency graph is useful project management. It is not a proof-producing functor.

Therefore the paper's strongest defensible program-level description is:

> GTF-I is a comparison/certification interface that can consume rigorously proved model-specific inputs and preserve declared causal resource budgets.

That is potentially valuable. It is not yet:

> the first-principles foundation from which the hard eleven-paper theorem chain follows.

A top-four paper with “Foundations” in the title should earn that word through a theorem that reorganizes or proves difficult mathematics downstream, not through metadata edges.

---

# 11. The filtered-experiment priority boundary remains materially incomplete

The bibliography contains Espen Norberg's 2002 paper, but the manuscript's literature audit explicitly states that it was not inspected at proof level.

This is a serious unresolved priority issue because Norberg is not a remote citation. The published abstract says that the paper extends Le Cam deficiency to stochastic-process experiments in which a statistician chooses successive actions while observing a parameter-dependent process and gives several equivalent risk-comparison expressions.

That is directly adjacent to the conceptual core of the present manuscript.

The required comparison is not a superficial “our notation is different” paragraph. It must answer:

1. What is Norberg's exact filtered deficiency?
2. What stochastic/randomization operators are admissible?
3. What persistent information can the operator retain?
4. What is charged and what is free?
5. How are sequential actions timed relative to observations?
6. Which risk criteria are equivalent?
7. Can the present finite-state/private/hidden/visible constraints be inserted into that framework?
8. Which theorem in v13–v16 is still genuinely new after the comparison?

The same principle applies to the automata/state-minimization lineage where the paper invokes Paull–Unger but still lacks proof-level retrieval.

A foundational paper cannot leave the nearest historical priority boundary explicitly unresolved and simultaneously ask for top-four novelty credit.

---

# 12. Verification artifacts are strong reproducibility practice but do not alter theorem depth

The evidence package is careful:

- exact coefficient arrays are deposited;
- negative controls are run;
- source hashes are pinned;
- predecessor tests are rerun;
- rational interval arithmetic is used for the physical scalar;
- the manuscript explicitly says the checker is not an analytic proof verifier.

This is excellent scientific hygiene.

It is not mathematical significance.

A 9,409-coefficient certificate shows that one finite lower bound is mechanically verifiable. It does not explain the intrinsic geometry of the resource set.

A narrow rational interval for \(d(\tau)\) shows that the scalar calculation is reproducible. It does not make collisions essential to the physical theorem.

A passing pipeline JSON shows that labels and provenance are coherent. It does not prove the historical B4 or C2 analytic statements.

The paper generally knows this. Its top-level rhetoric should be made equally disciplined.

---

# 13. Journal architecture remains too repository-dependent

The canonical article is 47 pages, but its source identity is spread across multiple revision directories and hundreds of pinned inherited files. The 243-page complete-development object is useful for preservation but is not a plausible journal submission object.

At a conventional top mathematics journal, the reader should not need:

- Git history to determine what is new;
- a 402-input source closure to determine theorem identity;
- multiple historical introductions to understand the current scope;
- branch names to distinguish “retained” from “new.”

A future submission should have one clean source tree and one mathematical narrative. If results from v13–v15 are unpublished and are logically required, they must be restated/proved in a coherent self-contained form. If they are prior work, the paper must cite them as prior work and isolate the new theorem sharply.

The present repository organization is excellent for iterative research. It should not dictate the journal exposition.

---

# 14. Major blocking requirements for another top-four-level review

I would regard all of the following as serious.

## E16-R2.1 — Close the polynomial-positivity novelty boundary

Give theorem-level comparison with de Klerk–Laurent, Laurent–Slot, de Klerk–Vera, and the relevant Bernstein/Handelman/Positivstellensatz hierarchy. Identify exactly what is new after generic hypercube positivity certification is subtracted.

## E16-R2.2 — Replace “dual” by an accurate term, or prove an actual duality theorem

If “dual” remains, provide an independent resource-sensitive dual object and a genuine variational theorem. Otherwise call the current construction a positive-polynomial certificate hierarchy.

## E16-R2.3 — Prove an intrinsic certificate-complexity theorem

Relate degree, support, coefficient count, or bit complexity to behavior dimension, horizon, resource width, or another representation-invariant parameter. The current stick-breaking/tensor-Bernstein size is coordinate dependent.

## E16-R2.4 — Preserve the strict-margin boundary explicitly

State everywhere that finite completeness is for \(L<\delta\). Do not imply a finite equality/zero-gap decision theorem unless one is actually proved.

## E16-R2.5 — Give one genuinely resource-sensitive physical example

Produce a single microscopic example with a strict private/hidden/visible separation in which the causal information pattern matters. The present physical example has the same deficiency for all those signatures.

## E16-R2.6 — Make the physical observable genuinely interaction-sensitive

At least one central quantitative result should depend essentially on collision geometry rather than only on total-momentum conservation. Sphere diameter/collision structure should enter the theorem nontrivially.

## E16-R2.7 — Isolate v16's exact strengthening over v15

State explicitly that the physical stability/triangle mechanism is inherited and that v16 strengthens the finite lower-certificate module plus explicit examples.

## E16-R2.8 — State algorithmic quantifiers precisely

Make effective enumeration, production of rational presentations, certified error comparison, and uniform finite subroutines explicit hypotheses of any terminating general algorithm theorem.

## E16-R2.9 — Either close one hard downstream theorem or narrow the foundational claim

A top-four-scale route would be a particle-uniform theorem or kinetic-scaling theorem that supplies a genuine B4 hypothesis, or a comparably hard C2/A4 consequence. Otherwise describe GTF-I as an interface/certification theory rather than as the foundation of the full chain.

## E16-R2.10 — Complete the Norberg proof-level crosswalk

The direct filtered-deficiency antecedent must be compared definition by definition and theorem by theorem.

---

# 15. Technical comments

1. **State the finite carrier explicitly every time “complete certificate” is used.** The v16 theorem is not a general standard-Borel finite certificate theorem.

2. **Separate value invariance from certificate invariance.** The deficiency value may be intrinsic while the stick-breaking/Bernstein degree is not.

3. **Report raw dimensions.** For every computational example give \(D,m,p,n,(n+1)^D\), maximum coefficient bit length, and total certificate byte size.

4. **Visible selectors.** Keep the joint target selector law explicit in theorem statements rather than relying on inherited conventions.

5. **Physical example terminology.** “Collision-compatible” is accurate. “Interaction-sensitive” would not be.

6. **Residual interpretation.** State that \(R=\omega^2\) is a projection residual, not a collision or mixing strength.

7. **Diameter independence.** The numerical example should explicitly note that the displayed scalar and residual do not depend on hard-sphere diameter once the equilibrium configuration space is nonempty.

8. **Causal language in the one-acquisition example.** Because the action precedes informative observation and all resource signatures coincide, call this a marked physical comparison example rather than evidence of a nontrivial causal-resource gap.

9. **Algorithmic theorem.** Distinguish a computable sequence from a sequence of individually computable objects if termination is claimed.

10. **Bernstein positivity.** Cite the nearest quantitative hypercube results in the main paper, not only in supplementary discussion.

11. **Exponential theorem.** Keep bounded payoff and common output interface in the theorem heading or immediately adjacent statement.

12. **B4 link.** Call it an accuracy-transfer prerequisite unless an actual large-deviation/Nisio/kinetic result is proved.

13. **Pipeline checker.** Retain the present disclaimer that label/source checks are not semantic proof verification.

14. **Complete development.** Treat it as archival material, not part of the mathematical object a journal referee is expected to read as the submission.

15. **Historical labels.** If a theorem is inherited verbatim, say so at its first canonical appearance or reorganize the source so chronology is unnecessary.

---

# 16. What would change the recommendation

There are two mathematically credible routes.

## Route A — Make the finite causal resource theory genuinely structural

A new theorem of the following scale would materially change the paper:

- an intrinsic nonlinear separation/duality theorem for finite-memory causal behavior sets;
- sharp dimension-versus-width laws for private, hidden, and visible resources;
- a certificate-support theorem independent of a row parameterization;
- a complexity dichotomy or lower/upper classification in intrinsic parameters;
- an equivalence between approximate causal congruence, positive-error state complexity, and universal continuation state.

Then the physical material can be an application.

## Route B — Make the physical bridge genuinely interaction-sensitive

Construct a microscopic acquisition in which:

- collisions change the informative observable in an essential way;
- feedback changes later information;
- private/hidden/visible deficiencies separate;
- same-budget lower and upper certificates are explicit;
- the approximation survives a physically meaningful scaling;
- at least one hard downstream B4/C2 hypothesis is supplied by the theorem.

Then the finite certificate machinery would acquire substantially greater significance.

The present v16 sits between these two routes without yet reaching either.

---

# 17. Positive aspects that should be preserved

A harsh report should still distinguish strengths worth keeping.

1. The manuscript has become unusually explicit about source provenance and review scope.
2. It no longer treats free convexification as innocent at a fixed private-memory budget.
3. The two-time example is an effective explanation of the hidden-versus-visible resource distinction.
4. The finite strict certificate is exact rational mathematics rather than a floating-point heuristic.
5. The v15 stateless marked presentation architecture is a serious attempt to preserve actual marks and resource budgets under physical approximation.
6. The new hard-sphere example gives exact generator-domain formulas rather than formal boundary differentiation.
7. The authors explicitly disclaim particle-uniform kinetic closure and formal proof verification.
8. The pipeline metadata now distinguishes independent primary chains from adapters more honestly than earlier versions.

These should survive any rewrite.

---

# 18. Final assessment

V16 is a real mathematical revision, not merely a repackaging. I do not find a simple fatal algebraic error in its main fixed-finite certificate theorem, and the explicit scalar calculations I checked are consistent with the manuscript.

Nevertheless, at the requested Annals/Inventiones/JAMS/Acta standard, correctness inside a carefully restricted scope is not enough.

The present manuscript asks a classical positivity mechanism, a symmetry-reduced collective hard-sphere mode, an inherited stateless transfer theorem, and an elementary exponential stability inequality to carry the burden of a paper titled **General Theta Foundations I**.

They cannot yet carry that burden.

The finite resource theory still lacks an intrinsic structural/certificate-complexity theorem. The explicit physical model still avoids interaction-sensitive dynamics and does not realize a private/hidden/visible causal gap. The end-to-end physical stability principle is substantially inherited. The B4 and C2 hard analytic gates remain separate. The closest filtered-deficiency and hypercube-positivity priority boundaries are not yet closed at proof level.

Accordingly, my recommendation remains:

## Reject at the requested top-four general-mathematics venue in the present form.

A future submission could become much stronger by pursuing either Route A or Route B above. What is needed is not another layer of validation metadata or another exact finite instance. It is one new theorem whose mathematical content changes the architecture of the subject rather than certifying the current architecture more thoroughly.
