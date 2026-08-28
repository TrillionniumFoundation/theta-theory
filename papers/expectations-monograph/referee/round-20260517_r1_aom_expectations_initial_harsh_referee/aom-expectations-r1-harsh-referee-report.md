# Harsh Referee Report — R1 AoM/AoMath Expectations Manuscript

## 1. Verdict

**Reject in current form / major reconstruction before any serious submission. Readiness score: 3.6 / 10. Confidence: 4 / 5.**

The paper has an ambitious and interesting conceptual aim: derive a nonlinear expectation theory from deterministic finite-horizon dispersing billiards rather than from stochastic primitives. The current manuscript, however, is not yet a submit-ready mathematics article. It is 243 pages, proves or claims an enormous chain of singular billiard, transfer-operator, response, homogenization, HJB, and nonlinear expectation results, and often substitutes acyclic dependency declarations for proof details at exactly the points where a skeptical referee will demand the most precision.

## 2. Short Summary

The manuscript starts from a finite-horizon dispersing billiard table with singular collision map and a compact deterministic finite-response mechanical port. It claims to derive the singular atlas, cone invariance, distortion, growth lemma, anisotropic Lasota--Yorke inequalities, spectral gap, suspension resolvent, moving-singularity response formula, deterministic cell correctors, and an effective fully nonlinear HJB equation. It then defines a downstream $\theta$-expectation semigroup and representation calculus, including linearized diffusion, BSDE, and Girsanov-style formulae.

The most important advertised theorem is the deterministic homogenization theorem in `main.tex` lines 5865--5913, with proof sketched in lines 5916--6034. The most important conceptual claim is that every object in the HJB is derived before the macroscopic solution appears, summarized again in lines 6039--6099 and 7140--7281.

## 3. Positive Points

- The manuscript correctly avoids saying that a singular billiard map is a globally smooth Anosov diffeomorphism. The convention at `main.tex` lines 530--532 and the primitive assumptions at lines 573--598 keep grazing and singular strata in the model.
- The paper explicitly separates deterministic derivation from downstream probabilistic representation; see `main.tex` lines 7287--7347.
- The effective HJB form is clean once accepted: $-u_t-\operatorname{Tr}(D(x,\nabla u)D^2u)-H(x,\nabla u)=0$.
- The compile gate passes and the PDF has no unresolved references or citations.
- The paper has a useful internal map of dependencies. This is valuable for repair, even though it is not sufficient as a proof.

## 4. Blocking Concerns

### 4.1 The proof burden is far beyond what the manuscript actually discharges

The manuscript claims a full chain from ordinary geometric billiard inputs to spectral gaps, Dolgopyat suspension resolvents, moving-singularity response, cell equations, and viscosity homogenization. This is summarized in `main.tex` lines 637--662, 699--716, 5865--5913, and 7207--7237.

For a top mathematics venue, these cannot be accepted as a sequence of self-contained ledger statements. Each of the following is a major technical program on its own:

- spectral gap for singular billiard transfer operators on anisotropic spaces;
- suspension-flow Dolgopyat estimates with singular roof and homogeneity strips;
- parameter differentiability/moving-singularity linear response for billiard tables;
- inversion of observable generators on zero-mean anisotropic spaces;
- corrector-based homogenization where the fast dynamics, table, and cotangent feedback all depend on the slow gradient.

The local proofs are often written as ordered summaries: "rank 5 gives Lasota--Yorke," "rank 6 gives Dolgopyat," "rank 7 gives response." That is not enough. A referee will ask which exact Banach spaces, norms, regularity losses, distortion constants, trace bounds, and compatibility conditions make every operator identity legitimate.

### 4.2 The "primitive geometry only" claim is too strong

The primitive assumption block at `main.tex` lines 573--598 is relatively modest. The later conclusions are enormous. The bridge is the compact finite-response mechanical port, introduced around lines 1312--1495 and used throughout the HJB construction. But the port appears powerful enough to realize tailored feedbacks, finite jets, potentials, and cotangent read-outs.

This weakens the advertised "first-principles" character. If the port can be shaped to realize the desired Hamiltonian behavior, then the resulting nonconvexity is not primarily an emergent consequence of billiard chaos. It is partly engineered by the admissible coupling class.

The issue is especially clear in the nonconvexity construction at `main.tex` lines 6987--7005 and 7020--7065. The proof chooses a feedback curve $\Theta(x,p)=\theta_{\eta_3Q_3(r)-\eta_4Q_4(r)}$ and a potential $V=W(z)$ to obtain a cubic--quartic profile. This is a valid algebraic construction if all response theorems hold, but it does not yet justify the paper's stronger language that non-subadditive $\theta$-expectations are derived from first principles rather than designed through the port.

### 4.3 The singular billiard response theory is under-specified

The manuscript repeatedly invokes moving-singularity response and differentiated resolvents, for example around `main.tex` lines 3568--3679 and 3866--3920. In singular billiards, differentiating invariant measures and spectral projectors under table deformation is delicate: singularity curves move, homogeneity partitions change, grazing strata produce unbounded derivatives, and one must track strong-to-weak losses exactly.

The manuscript says these terms are controlled by strip summability and trace ledgers. That may be plausible, but the current presentation does not give a referee enough to verify:

- the exact anisotropic spaces and their parameter-dependent domains;
- the number of derivatives lost at each response step;
- why the contour/resolvent representation remains uniform under the moving singular set;
- how grazing trace terms are paired with the cell correctors used later in viscosity tests;
- whether the response formula is new or a corollary of a known theorem.

This is not a cosmetic issue; the response theory is a load-bearing part of $H(x,p)$ and of the full-gradient cancellation.

### 4.4 The prelimit HJ equation is not yet convincingly derived

The "exact deterministic prelimit Hamilton--Jacobi equation" at `main.tex` lines 1961--1987 is central. The proof at lines 1989--2018 asserts that a branchwise action identity and graph transform yield the prelimit PDE with $p=D_xU^\varepsilon$.

A referee will not accept this without a much more explicit variational or dynamic-programming construction. The difficulty is not differentiating a smooth action on a branch; the difficulty is that the branch structure, billiard table, generator, and slow drift all depend on the cotangent signal. The proof must show:

- existence and uniqueness of the branchwise graph transform on the required time interval;
- compatibility across collisions and singular exclusions;
- stability of the viscosity-duality completion;
- why the $p=D_xU^\varepsilon$ closure is not a hidden fixed-point assumption;
- how terminal data and boundary/singularity traces enter the exact equation.

The current proof mostly says the construction was already completed. That is too circular from a referee's point of view.

### 4.5 The homogenization theorem is too compressed relative to the machinery it needs

The main theorem at `main.tex` lines 5865--5913 states locally uniform paired convergence and a Liouville-a.e. microscopic statement. The proof at lines 5916--6034 is a standard perturbed-test outline, but the nonstandard parts are precisely where detail is needed:

- relaxed envelopes are taken over admissible density windows depending on contact gradients;
- the first corrector cancels an $\varepsilon^{-1}$ term while the coefficients depend on the full gradient;
- the second corrector absorbs moving-boundary and $p$-response terms;
- a paired anisotropic convergence statement is upgraded to Liouville-a.e. pointwise convergence without subsequences.

These steps may be defensible, but not in the current form. The manuscript needs a smaller theorem whose assumptions and topology can be checked line by line, or it needs to cite a known deterministic homogenization theorem and clearly state only the new verification work.

### 4.6 The representation layer overclaims relative to the derived PDE

Part II is presented as downstream, which is good. But the FBSDE section at `main.tex` lines 7452--7496 assumes uniform positive definiteness of $D$ on the visited region, while the main construction only gives a symmetric positive semidefinite Green--Kubo tensor. The Girsanov statement at lines 7501--7539 is essentially an algebraic Hamiltonian-shift identity at the semigroup level, not a probabilistic Cameron--Martin theorem unless additional integrability, nondegeneracy, and exponential-martingale assumptions are supplied.

This section should be reframed as optional formal representation under extra hypotheses. It should not be used to make the paper look like it has built a full nonlinear stochastic calculus from the deterministic model.

### 4.7 The manuscript is not in article shape

At 243 pages, the manuscript is not a normal submission paper. It contains many repeated appendix templates beginning around `main.tex` line 7681 and continuing into the 12,000-line range. The appendix excerpt at lines 11882--12060 illustrates the problem: it mixes a purported proof of roof bounds with later transfer-operator, resolvent, and viscosity consequences, and it repeatedly restates "deterministic" and "acyclic" rather than isolating the exact estimate.

The root `README.md` is still generic IMS/AOP template material, not a build/readiness guide for this paper. That is a package-readiness failure.

## 5. Compile and Package Notes

- Local compile passed with `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex`.
- Recompiled `main.pdf`: 243 pages, SHA256 `f9c25c7e3455dd4cd85746352438125514936df8035d2d01d30dcc05c4c1004d`.
- Undefined references/citations: 0.
- Overfull hboxes: 9, including displayed equations near `main.tex` lines 1359, 5597, 5809, 5911, and 7229.
- Underfull hboxes/vboxes: 19 total.
- LaTeX warnings: 1; package warnings: 1.
- The title in source line 182 matches the recompiled PDF title.

These are not the main blockers, but a final package should be log-clean or at least intentionally justify remaining layout noise.

## 6. Recommended Repair Plan

1. **Choose the actual paper.** Either write a 35--50 page article proving one new theorem, or make this a monograph/preprint. The current object tries to be all of singular billiard theory, response theory, homogenization, HJB theory, and nonlinear expectations at once.
2. **Demote broad derived claims to assumptions or cited propositions.** If the novelty is the $\theta$-expectation/HJB construction, state the billiard spectral gap and response package as explicit assumptions with citations. If the novelty is singular billiard response, remove the nonlinear expectation layer and prove that theorem carefully.
3. **Make the finite-response port concrete.** Replace the broad realization language with a physically inspectable coupling class. State what cannot be realized. Otherwise the "first-principles" claim will keep failing.
4. **Provide one worked example.** Give a specific billiard family and port where $D$ and $H$ can be computed, bounded, or at least numerically inspected. The paper currently proves existence-style flexibility but no tangible model.
5. **Rewrite the main theorem with exact assumptions.** Include regularity thresholds, Banach spaces, topology of convergence, degeneracy conditions, comparison hypotheses, and all regularity losses.
6. **Cut repetitive proof ledgers.** Replace repeated acyclicity declarations with a dependency table plus real proofs for only the new steps.
7. **Reframe Part II.** Present FBSDE/Girsanov as optional representation under additional nondegeneracy/smoothness assumptions, not as part of the core theorem.
8. **Clean package hygiene.** Fix overfull displays, replace the generic README, and add a reproducibility/build note.

## 7. Final Recommendation

The project has a potentially interesting core, but the current manuscript is not submission ready. The right next step is not another broad patch. It is a hard narrowing decision: select the one theorem that is genuinely new and defensible, move the rest to assumptions or future work, and make that theorem fully auditable.

