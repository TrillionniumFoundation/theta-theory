# Round-Six Independent Referee Report — GPT-5.6 Pro

**Manuscript:** B2 — *Collision Clusters and a Dynamic Large-Deviation Principle for Deterministic Hard Spheres*  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*  
**Recommendation:** **Reject**  
**Reviewed revision branch:** `revision/round6-referee-positive-closure-11paper-2026-08-31`  
**Reviewed branch head:** `fb2ccfafab262f31f5b6f960df23e31258a59223`  
**Reviewed tree:** `2d3992ea12cfd513359a5f204bb1c2ae027bc7c4`  
**Active controlling module:** `ROUND6_POSITIVE_CLOSURE.tex`, blob `5f7db4c201e834dc75d7b3b65cbef050b706fa4f`

## Editorial summary

The revision correctly concedes that no contact-count bound can hold for arbitrary interior `L1` densities and replaces that false statement by a trace-regular hierarchy class. It also retains the true post-collisional future instead of deleting later contacts. These are necessary repairs.

The new first-surplus estimate, however, is not uniform in genealogical depth. Its own Gramian bound deteriorates like `delta^{C(1+m)}`. After the prescribed choice `delta=epsilon^kappa`, the coarea exponent becomes negative for large `m`, and no fixed hierarchy label weight can absorb powers of `epsilon^{-m}`. Thus the claimed uniform `epsilon^alpha` cyclic gain does not follow. The trace semigroup, conservative regularization, and LDP lower bound contain additional unproved or false assertions. Since B2-GC is upstream of the entire hard-sphere series, this remains the principal blocker.

## Major mathematical objections

### 1. The quantitative Gramian estimate cannot yield an `m`-uniform power of `epsilon`

The manuscript proves only

\[
\lambda_{\min}\mathcal G_{ab}
\ge c\,\delta^{C(1+m)}(1+m)^{-C},
\]

where `m` is the ancestral depth. The ensuing coarea estimate is therefore of the form

\[
C^m\varepsilon^2\delta^{-C(1+m)}.
\]

The proof chooses `delta=epsilon^kappa` with fixed positive `kappa`. This gives

\[
C^m\varepsilon^{\,2-\kappa C(1+m)}.
\]

For every fixed `kappa>0`, the exponent tends to minus infinity as `m` grows. There is no positive `alpha`, independent of `m`, for which this is bounded by `C_1^m epsilon^alpha` for all genealogies.

The text says that chronological tree weights and the hierarchy label radius absorb the powers `delta^{-Cm}`. They cannot do so uniformly in `epsilon`. A typical depth sum contains a ratio comparable to

\[
CT\,\varepsilon^{-\kappa C},
\]

which exceeds one for all sufficiently small `epsilon`, regardless of any fixed `T` or fixed label radius. Factorials in the label norm remove combinatorial counts but do not cancel an `epsilon^{-c m}` singularity.

One would need a Gramian lower bound with an exponent independent of `m`, a depth cutoff growing slowly with `|log epsilon|` plus a separate large-depth estimate, or a non-power choice of `delta` accompanied by a summable two-parameter optimization. None appears. `lem:r6-b2-tube`, `thm:r6-b2-cyclic`, and the claimed disappearance of all cyclic clusters therefore do not follow.

### 2. The backward observability proof does not handle common-root translations

The proposed control family includes translations of each independent root component. If labels `a` and `b` belong to the same creation tree, a translation of their common root moves both descendants equally and has zero derivative on the relative position `x_a-x_b`. It cannot eliminate a terminal transverse covector as the proof claims.

The two “exclusive ancestral paths up to the first common ancestor” terminate at that common ancestor, not at two independent roots. The statement that orthogonality to “the explicitly included independent root translations” removes the remaining components is therefore false in this case. Root velocity variations may help after unequal flight times, but no rank calculation is given, and energy/momentum constraints can remove precisely those directions.

A word-uniform controllability theorem must distinguish separate-root and common-root genealogies and compute the actual control matrix on each chronological cell. The present abstract backward propagation is not sufficient even for qualitative full rank.

### 3. Conditioning at a stopping contact does not produce an element of the declared trace Banach space

The trace norm is an integrated `L1` norm of incoming flux traces and tangential derivatives. A pointwise post-collisional state conditioned on a specific stopping contact is a boundary Dirac state, not an `L1` boundary density with finite tangential trace norm.

The corollary says that after any stopping contact, reflection produces an outgoing trace that is an admissible initial boundary coordinate for the remaining semigroup. That requires a boundary-to-interior semigroup acting on measure-valued traces and a disintegration estimate uniform in the stopping data. It is not a consequence of the integrated Green identity. Reflection is isometric between incoming and outgoing flux measures, but it does not regularize a singular conditional boundary state.

One may integrate the future expectation against the pre-contact flux density without conditioning pointwise. That would require an operator-valued boundary renewal estimate. The manuscript instead uses a conditional ledger in the proof of every cyclic sector, so this gap is material.

### 4. Lemma `lem:r6-b2-trace-class` is essentially the main theorem in disguise

The lemma asserts an exact Feynman–Kac BBGKY evolution on a norm containing interior densities, all incoming traces, and tangential derivatives, with constants uniform in `epsilon`, stable under actual-contact exponential weights and stopping contacts. The proof consists of one Green identity and a Gronwall sentence.

It does not treat:

- the `epsilon`-dependent curvature and area of hard-sphere collision boundaries;
- grazing singularities, multiple-contact corners, and their trace compatibility;
- creation operators changing label number and boundary codimension;
- tangential derivatives through specular reflection;
- boundary source multiplication and repeated returns; or
- closure and strong continuity of the full hierarchy generator.

Placing grazing pieces in a “bad-set ledger” does not estimate that ledger. Since the contact exponential moment is later obtained by merely inserting a constant source into this lemma, the alleged repair of the boundary-layer counterexample has been moved into an unproved trace-semigroup assertion.

### 5. The fixed-horizon pressure proof has no uniform block-error theorem

The pressure theorem divides a fixed horizon into source-dependent blocks, invokes a local Boltzmann–Grad consistency error “uniform on the reached trace ball,” and sums the errors. No such local convergence theorem is stated or proved for the trace hierarchy, and the reached radius/trace norm deteriorates at every block.

Normal convergence of formal creation trees on one small block does not imply convergence of the exact Feynman–Kac hierarchy after repeated composition. In particular, cyclic sectors must already be uniformly controlled—the failed result of objections 1–3. The claimed source sewing is therefore circular.

### 6. The conservative regularization lemma contains a false smoothing-rate assertion

Starting from an arbitrary finite-action feasible pair, the proof mollifies it and states that the balance defect is

\[
O(h^M)
\]

in a negative Sobolev norm for arbitrarily large `M` because the mollifier has matching moments. For a rough finite measure or merely finite-entropy density, convolution commutators generally converge at a rate determined by the regularity of the original object; there is no arbitrary-order `h^M` gain. Moment cancellation gives high-order approximation only for sufficiently smooth inputs.

This invented rate is then used to dominate the polynomially ill-conditioned right inverse `h^{-kappa}` and maintain positivity. Without it, the signed correction may be comparable to or larger than the positive background, and entropy convergence is unproved.

The statement that a finite collision incidence matrix on each energy–momentum shell has a right inverse of norm `Ch^{-kappa}` is itself unsupported. Connectivity of a discretized collision graph does not give a polynomial spectral gap uniformly over shell degeneracies, grazing cells, and conservation constraints.

### 7. Exponential compactness uses a source outside the proved pressure domain

The pressure theorem is stated for bounded particle and contact sources. The compactness proof then inserts a Maxwellian Lyapunov source such as `e^{beta'|v|^2}`, which is unbounded. No exhausted weighted-source theorem has been proved in B2 at this stage.

Initial Maxwellian energy estimates and conservation may provide velocity tightness, but they must be derived directly and combined with contact flux tails. They cannot be obtained by citing a pressure chart that excludes the source used. This is important because the LDP topology explicitly includes a Maxwellian Lyapunov moment.

### 8. The lower-bound tilt is circular and lacks concentration

For a regular pair the paper declares an exact Feynman–Kac density, says pressure differentiability makes its mean converge to `(f,Gamma)`, and says the second derivative plus exponential compactness gives concentration. Convergence of the mean and bounded covariance does not imply exponential concentration at large-deviation speed. A unique exposed minimizer and a pressure gap for every neighborhood are required.

Those properties are essentially the strict convexity/covariance theorem later claimed in B3 and the LDP lower bound being proved here. Solving a backward balance equation for bounded `p` with an arbitrary smooth target pair is also not justified. Thus the lower bound is not independently established.

### 9. Microcanonical B2 is unavailable because B1 remains invalid

The microcanonical theorem assumes a source-uniform shell coefficient for every bounded density/contact source. The B1 report identifies an impossible singleton-density hypothesis, an omitted compound-Poisson atom, and a shell scaling error. Therefore B2-MC cannot be credited even independently of the grand-canonical defects above.

## Dependency consequences

The declared order is `B2-GC -> B1 -> B2-MC -> B3 -> B4 -> C1/C2 -> D1`. Objection 1 blocks the first arrow. Every hard-sphere pressure, action, covariance, semigroup, posterior game, and commutation theorem downstream is consequently unsupported.

## Required reconstruction

A viable proof must:

1. obtain a surplus-contact estimate whose loss is summable jointly in `epsilon` and genealogical depth;
2. prove controllability separately for common-root and separate-root genealogies;
3. construct an actual boundary-trace semigroup, including singular stopping states or an integrated renewal formulation;
4. prove local and sewn Feynman–Kac convergence on that trace space;
5. replace the arbitrary-order mollification claim by a quantitative regularization theorem valid at finite action;
6. derive exponential compactness from sources genuinely inside the proved domain; and
7. prove exposed-tilt concentration without invoking downstream covariance results.

## Recommendation

**Reject.** Restricting to a trace-regular class is the correct response to the previous boundary-layer counterexample, but the new cyclic estimate fails its own depth-uniformity test. The trace semigroup and regularization lemmas are not proved, and the LDP lower bound is circular. B2-GC remains the decisive unresolved blocker of the hard-sphere series.