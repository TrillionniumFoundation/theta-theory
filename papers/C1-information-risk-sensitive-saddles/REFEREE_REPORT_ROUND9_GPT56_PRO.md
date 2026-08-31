# Round-Nine Independent Referee Report — GPT-5.6 Pro

**Manuscript:** C1 — *Typed Control, Information, and Saddle Envelopes for Kinetic Cotangent Phases*  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*  
**Recommendation:** **Reject**  
**Reviewed revision branch:** `revision/round9-referee-positive-closure-11paper-2026-08-31`  
**Payload-host branch head at review lock:** `a8c0c551f5f8614856a9d433e78b2eb92a5dcfa1`  
**Registered round-nine payload SHA-256:** `cf230322211332af59a7883af1b669eeb9b4f7e9f4220fc24712c634bda17716`  
**Reviewed registered source:** `revision/round9-referee-final/C1_EVIDENCE_CURRENT_BELIEF_DPP.tex`  
**Reviewed source SHA-256:** `60c72a6685d6b1f8a814d4b8a0b5828ddb8f52e661bebbb3cc9118251cb56180`  

## Evidence boundary

At the review lock, the branch stored the checksum-pinned round-nine payload while the paper-level `main.tex` files still loaded the round-eight modules; the repository publication workflow was queued. I independently verified the payload hash, unpacked it, and ran the repository materializer successfully, producing byte-identical paper-level `ROUND9_POSITIVE_CLOSURE.tex` files. This report therefore reviews the exact registered round-nine theorem text. It does not treat a queued workflow, a clean build, theorem/proof counts, or an internal hostile-regression script as evidence that the mathematical claims are true.

## Executive assessment

Round nine keeps exact observations, stores unnormalized coarea currents and log evidence, uses separate source and zero-source saddles, and restricts reduction to a reachable belief class. These are appropriate repairs.

The stratified filter and its asymptotic reduction are not constructed. In particular, an unnormalized current does not make the normalized posterior transition Feller at zero evidence; the B1 good-block coefficient does not apply to a general global observation map; and the claimed finite “correlation skeleton” is defined by the conclusion it is meant to prove.

## Major objections

### 1. The observation–collision current tower is asserted, not constructed

Repeated intersections of observation level sets with moving collision faces produce currents with corners, critical strata, and changes of rank. A finite Whitney stratification of the observation maps does not by itself give bounded coarea operators on the B2 divergence-measure trace spaces.

The proof needs precise pullback/intersection theorems for normal currents, orientation conventions, continuity under prediction, and uniform norms through changing strata. None is supplied.

### 2. Keeping the unnormalized current does not make the belief kernel Feller at \(Z=0\)

For \(Z>0\), the posterior is
\[
 \Pi^y=\frac{\mathcal O_yG^-}{Z(y)}.
\]
As \(Z(y_n)\downarrow0\), the normalized measures can oscillate between mutually singular limits even if the unnormalized currents converge to zero. Appending \(\log Z\to-\infty\) records the evidence but does not determine a continuous normalized posterior at the zero current.

The dynamic value and future transition depend on the normalized belief, so a Feller extension of the zero *unnormalized* current is not sufficient. The theorem needs a compactification of projective current directions at zero evidence or must restrict to finite evidence slices.

### 3. The exact belief state is not shown to be moment determinate

The paper says that a complete current hierarchy is equivalent to a probability law on a “moment-determinate reachable class,” but it never defines or proves invariance of that class. With unbounded particle number and singular strata, factorial moments need not uniquely determine a law without exponential bounds stable under every observation update.

### 4. The B1 regenerative Fourier mechanism does not apply to a general observation

The observation \(O_k^u\) is an arbitrary finite-dimensional \(C^{r+3}\) function of the complete block path/microstate. It is generally not a sum of independent one-particle marks. The B1 good-block construction cannot simply be enlarged to the “combined constraint–observation mark.”

A global collision count, occupation functional, or nonlinear observation couples all cells. Full rank of the coarea map is not the conditional product minorization needed for high-frequency decay. Thus Theorem `r9-c1-coefficient` has no proven Fourier input.

### 5. Separate saddles are acknowledged but not constructed

Using two saddles is correct. A saddle in the observation Fourier variable is generally complex, and the contour deformation must avoid singularities and track the coarea amplitude. The theorem supplies no analytic domain, nondegenerate Hessian, minor-arc bound, or source-uniform contour argument for either numerator or denominator.

The determinant ratio and the \(o(1)\) relative errors are therefore formal.

### 6. The evidence-tail corollary does not follow from local saddle charts

A local coefficient near regular observation values cannot give, for every \(M\), a compact set whose complement has probability \(e^{-M\mu}\). That is an exponential-tightness theorem for the entire observation/evidence state, including critical strata and values outside the regular charts. It requires global coercivity not present in the proof.

### 7. The reachable chaotic class is circular

The state includes a finite skeleton \(\kappa\) of all correlations that “survive at order one,” and the remaining correlations are assumed to satisfy
\[
 \|h_j\|\le C^j\mu^{1-j}.
\]
The lemma then concludes that this property is preserved. No criterion identifies the finite skeleton before solving the filtering problem, and an exact nonlinear observation can create correlations of arbitrarily high order.

Differentiating a coarea pressure does not prove a uniform cluster expansion for a singular conditional law, particularly on small-evidence events. The claim that every extra label retains the usual \(\mu^{1-j}\) factor is the missing quenched theorem.

### 8. Reduced-value sufficiency and BvM are not consequences of the stated estimates

Uniform \(o(1)\) reward errors do not by themselves control minimax strategy-dependent transition kernels. One needs a coupling or total-variation/Wasserstein estimate stable under dynamic programming.

The Bernstein–von Mises conclusion additionally requires posterior concentration, identifiability, local asymptotic normality uniformly on growing neighborhoods, and control of phase boundaries. These are merely invoked.

## Dependency assessment

C1 depends on B2, B1, B3, and B4, all of which remain open. It also has an independent filtering-state obstruction at zero evidence and an unproved observation coefficient theorem.

## Required reconstruction

A viable paper should choose a restricted observation model—preferably with a positive noise density or a rigorously controlled finite coarea family—and construct its belief kernel first. It should prove a global evidence LDP and a quenched cluster/chaos theorem on an explicitly defined reachable class before reducing the state or asserting a game limit.

## Recommendation

**Reject.** The state representation has improved, but the Feller belief transition, exact observation coefficient, and asymptotic sufficiency theorem remain unproved.
