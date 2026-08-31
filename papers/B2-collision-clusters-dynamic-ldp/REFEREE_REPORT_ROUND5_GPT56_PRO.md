# Round-Five Independent Referee Report — GPT-5.6 Pro

**Manuscript:** B2 — *Collision Clusters and a Dynamic Large-Deviation Principle for Deterministic Hard Spheres*  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*  
**Recommendation:** **Reject**  
**Reviewed revision branch:** `revision/round5-referee-positive-closure-11paper-2026-08-31`  
**Reviewed branch head:** `557c88ef447ab8c693b11e1c072efe97b4452556`  
**Active controlling module:** `ROUND3_POSITIVE_CLOSURE.tex`, blob `0efaf76e05ffe1f32c0a19fcd3aa7a9e07ae0715`  
**Unmaterialized round-five candidate:** `revision/round5-referee-final/B2_GENEALOGICAL_GRAMIAN_SOURCE_SEWING.tex`, blob `d33b148df5ac302145b774c2446b63a5f3513ebd`

## Source-control verdict

The active B2 paper is unchanged from round four. Its recollision surgery still deletes deterministic contacts and thereby changes all subsequent velocities, so the all-contact generating estimate and the resulting joint LDP remain unproved.

The round-five candidate attempts a better strategy: retain the actual post-collisional state after the first surplus contact, estimate that first contact by a genealogical Gramian, and control later contacts by a boundary-flux ledger. The packet was never materialized. More importantly, its new ledger has a direct counterexample and its Gramian proof does not establish the claimed uniform controllability.

## Decisive counterexample to the proposed contact ledger

The candidate claims that for every nonnegative `L1` Liouville density supported in an energy ball,

\[
M_z(t,\rho)=\int e^{zN_t(Z)}\rho(Z)dZ
\le \|\rho\|_1
\exp\{Ck(1+\mathbb V)^Ct(e^z-1)\}.
\]

This is false without a trace or distance-from-boundary condition on `rho`.

Choose `rho_t` concentrated in a layer of thickness `o(t)` immediately inside one incoming binary-collision boundary, with regular inward relative velocity bounded away from zero. Almost every initial configuration in that layer has one collision before time `t`. Hence, for fixed `z>0`,

\[
M_z(t,\rho_t)\approx e^z\|\rho_t\|_1.
\]

The proposed right-hand side tends to

\[
\|\rho_t\|_1
\]

as `t` tends to zero. For sufficiently small `t` this contradicts the inequality. An `L1` density may have arbitrarily large boundary trace while keeping the same mass and energy support. Liouville invariance does not provide a uniform collision rate from mass alone.

The conditional version after a stopping contact is even less justified: the transported boundary law is a trace measure, not an arbitrary interior `L1` density with the same norm. Therefore the future-preserving ledger, the whole-cyclic-sector estimate, and all downstream pressure bounds fail.

## Further major objections to the candidate

### 1. The genealogical Gramian proof does not prove full transverse rank

The Gramian is defined using Jacobi fields obtained by varying impact coordinates on creation edges. The proof propagates a covector backwards and concludes at the “terminal roots” that independent root translations force it to vanish. But root translations are not included among the summands of the displayed Gramian. Reaching two roots does not create an orthogonality condition to their translations.

For some genealogies the impact-normal variations along the path can span only one transverse direction, or become nearly aligned after repeated scattering. The qualitative backward argument does not yield the stated word-uniform lower bound

\[
\lambda_{\min}\mathcal G_{ab}
\ge c\delta^C(1+m)^{-C}.
\]

A genuine controllability theorem must include all relevant root and creation variables, identify the exact linearized scattering matrices, and prove a quantitative observability inequality uniform over arbitrary tree depth.

### 2. The bad-set estimate has no uniform analytic-sublevel theorem

The packet classifies small relative speed, grazing, short event gaps, and vanishing Jacobian minors as a set of measure `C^m delta^beta`. For arbitrary composed hard-sphere collision words, the order of vanishing of those minors can grow with the word. Finitely many local variable types do not provide one uniform Łojasiewicz exponent. The claimed constants independent of the collision word are not derived.

### 3. The boundary-flux renewal inequality treats deterministic contacts as a bounded-rate process

The proof expands at the first contact and writes a Gronwall inequality with coefficient `Ck(1+V)^C`. This is precisely the unjustified bounded collision-intensity assertion exposed by the boundary-layer counterexample. Elastic reflection preserves phase volume, but it does not bound the incoming boundary trace of an arbitrary density by its interior `L1` mass.

### 4. Source sewing is not accompanied by a uniform error theorem

The packet allows a hierarchy label radius `alpha_R` growing like `T e^{CR}` and composes many source-dependent local charts. It does not prove that the initial hard-core law and every intermediate tilted hierarchy lie in these stronger spaces with uniform constants, or that the accumulated Boltzmann–Grad approximation error tends to zero as the number of blocks grows with `R`.

Exact finite-volume Feynman–Kac composition does not imply convergence of the composed limiting charts without stability and consistency estimates.

### 5. The finite-cell balance repair has an uncontrolled inverse

The conservative repair solves a finite collision-incidence system and invokes the inverse spectral gap of a connected graph. As the velocity/time mesh is refined, that gap can tend to zero. The proof gives no uniform bound ensuring that the signed correction is smaller than the added positive background, nor that its relative entropy tends to zero. Thus action-dense regular feasible pairs are not established.

### 6. Bounded-source pressure plus compactness does not by itself prove the full LDP

The upper bound requires a separating source class and a complete exponential-tightness theorem. The lower bound requires an exact microscopic normalized tilt concentrating at every regular pair. Those statements are asserted from differentiability of the sewn pressure. No Radon–Nikodym formula or conditional concentration theorem is proved for deterministic actual contacts.

### 7. The dynamic entropy formula remains a candidate, not a deterministic theorem

The pointwise conjugacy of `e^z-1` and `ell(q)` is correct. It does not show that the deterministic contact process has Poisson relative-entropy cost. That conclusion depends entirely on the failed marked-pressure and lower-bound construction.

## Genuine improvement

The candidate no longer deletes future collisions after the first surplus event and correctly retains the logical order

```text
B2-GC -> B1 -> B2-MC.
```

Those are meaningful corrections. The replacement contact ledger is mathematically false on its stated class, so the principal microscopic gate remains open.

## Required reconstruction

A viable B2 paper must prove a recollision estimate for the actual finite-volume initial law and for the specific tilted densities generated by the cluster expansion—not for arbitrary `L1` densities. It needs trace regularity, a correct quantitative genealogical transversality theorem, and a source-uniform normalized lower-bound construction. The full LDP should not be claimed before those results exist.

## Recommendation

**Reject.** The active paper retains invalid collision deletion. The unmaterialized candidate replaces it with a boundary-flux exponential ledger that is directly contradicted by densities concentrated near a collision boundary. Since B2-GC is the root of the hard-sphere dependency chain, B1–D1 cannot use it as a proved input.