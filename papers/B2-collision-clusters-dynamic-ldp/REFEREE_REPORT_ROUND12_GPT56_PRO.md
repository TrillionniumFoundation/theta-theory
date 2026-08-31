# Independent Referee Report — Round 12

**Manuscript:** B2 — *Collision Clusters and Dynamic LDP*  
**Reviewed branch:** `revision/round12-referee-positive-closure-11paper-2026-08-31`  
**Reviewed commit:** `10b553a750b3ba3f82c751e699446ed40db80d62`  
**Controlling module:** `ROUND12_POSITIVE_CLOSURE.tex`  
**Registered module SHA-256:** `6501f052594ad9034340fdb2147ad38ee59c1dad944f2faf18904e8ea1685f09`  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *JAMS*  
**Recommendation:** **Reject**

## Executive assessment

Round 12 corrects the normal-trace convention, keeps the true reflected future, abandons the false genealogy-uniform Łojasiewicz exponent, and tries to sum fixed-genealogy recollision errors by dominated convergence. This is the most promising structural change in the hard-sphere chain.

The central estimate is still not proved. Pointwise convergence of each fixed genealogy plus an \(L^1\)-summable cluster majorant yields a total \(o(1)\) cyclic contribution on a fixed horizon. It does not yield the stronger blockwise bound \(h\,\omega_T(\varepsilon)\) uniformly for every interval of length \(h\). That linear factor is essential for sewing \(T/h\) blocks. The proof has no uniform time-density estimate, and collision/grazing integrals can have integrable singularities. The fixed-genealogy nonvanishing determinant and the global lower-recovery theorem also remain asserted rather than established. Microcanonical closure additionally inherits B1's false coefficient theorem.

## Decisive objections

### 1. Dominated convergence does not give the stated linear-in-block-length modulus

For each fixed genealogy, the manuscript argues that its total surplus-contact weight tends to zero and is dominated by the ordinary cluster weight. Summing by dominated convergence can give

\[
\operatorname{CyclicWeight}_{[0,T]}(\varepsilon)=o(1).
\]

Theorem 3.2 needs the much stronger statement

\[
\operatorname{CyclicWeight}_{I}(\varepsilon)
\le |I|\,\omega_T(\varepsilon)
\]

uniformly for every time interval \(I\).

An \(L^1\) majorant does not imply such a Lipschitz modulus in time. For example, an integrable density \(g(t)=t^{-1/2}\) satisfies

\[
\int_0^h g(t)\,dt=2\sqrt h,
\]

which is not \(O(h)\). Near grazing, near simultaneous contacts, and near a block endpoint, coarea densities can have precisely this type of integrable singular behavior.

The proof's sentence “the first surplus time is integrated over the block, yielding the factor \(h\)” assumes a uniform \(L^\infty\) density in that time variable. No such estimate follows from fixed-genealogy analytic sublevel bounds or from an \(L^1\) cluster majorant.

### 2. Without the factor \(h\), the sewing theorem does not close

There are \(O(T/h)\) blocks. If the cyclic error is merely \(\omega_T(\varepsilon)\) per block, its accumulated size is

\[
O\left(\frac{T}{h}\omega_T(\varepsilon)\right),
\]

which need not vanish for arbitrary partition sequences. The claimed partition-independent fixed-horizon pressure therefore depends on an unproved uniform absolute-continuity theorem for the first-surplus time.

The trace state makes this especially delicate: laws may approach incoming collision faces at a block boundary. A tiny time interval can then carry a non-negligible boundary flux unless one proves a uniform nonconcentration estimate for the actual evolved ensemble.

### 3. Nonvanishing of the physical Jacobi determinant is not proved for every genealogy

The proof says that one may choose two root positions so the two subtrees approach the youngest connecting collision with independent transverse translations. But those root variations must preserve every earlier creation constraint, collision order, homogeneity strip, and absence of extra contacts. The implicit-function rank needed to do this is exactly the theorem being asserted.

Symplecticity of individual free-flight/collision derivatives does not imply that the selected two-dimensional projection at the eventual surplus time has nonzero determinant. A symplectic map may send a chosen two-plane into a plane whose projection onto the required transverse coordinates has rank one or zero.

For each discrete genealogy, the paper must exhibit a regular point with a nonzero specified minor or prove a structural transversality theorem. The present paragraph does neither.

### 4. The genealogy sum requires a uniform majorant that is not constructed

The quantity \(a_m(T)\) is introduced as the total absolute weight of all connected \(m\)-label genealogies and declared summable. For real hard-sphere trajectories with all actual contacts, this is not the ordinary Lanford tree sum: cyclic trajectories may have arbitrarily many contacts and complicated multiplicities. A source-uniform absolute majorant independent of \(\varepsilon\), homogeneous charts, and source derivatives is the principal new theorem.

Writing \(\sum_m a_m(T)<\infty\) does not prove that theorem. Without it, dominated convergence cannot be applied across genealogy depth.

### 5. The trace graph does not automatically possess all iterated traces used later

Divergence-measure currents have normal traces on codimension-one Lipschitz faces. Iterated traces on intersections of collision faces require additional regularity and compatibility. The manuscript says that such intersections have zero flux and are “included through their oriented iterated traces,” but neither the state space nor a trace theorem for those higher-codimension measures is supplied.

For smooth absolutely continuous trajectories, simultaneous collisions are null. In the weak graph completion, measures can concentrate on those sets; zero flux cannot simply be assumed.

### 6. The kinetic Hodge repair is not a proved right inverse for the nonlinear balance complex

Solving

\[
(\partial_t+v\cdot\nabla_x-\mathcal L_M)u=d
\]

constructs a linear Maxwellian correction. The lower-bound argument needs a correction of an arbitrary smoothed nonlinear pair \((f,\Gamma)\) that:

- has the exact endpoint conditions;
- preserves positivity of both density and contact flow;
- respects pre/post symmetry;
- is small in the topology controlling the entropy perspective; and
- has a norm uniform under velocity truncation.

Representing \(\mathcal L_Mu\) as a signed collision flux does not prove all of these. The five endpoint moment corrections can also reintroduce balance defects unless constructed jointly.

### 7. Local analytic pressure does not by itself give the global rate

The paper takes an increasing family of bounded real-source balls and declares their conjugates to converge to the full Poisson entropy, with infinite cost for singular or unbalanced pairs. This requires uniform source exhaustion, exponential tightness in the chosen path/contact topology, and a lower recovery theorem whose constants are compatible with the growing source radius. None follows from normal convergence on each fixed bounded ball.

The source \(\log(d\Gamma/dA_f)-\Delta p\) is unbounded for general finite-entropy pairs, so this interface is essential rather than technical.

### 8. The microcanonical statement is invalid independently through B1

Round 12 B1's high-frequency coefficient theorem is contradicted by the compound-Poisson empty-sector atom. Therefore the final B1 change of measure cannot presently transfer B2's source tilts or lower-recovery laws to the primitive shell.

## Genuine improvements recognized

The following should be retained:

- one normal flux measure, without double weighting;
- an analytic-scale rather than fictitious fixed-radius semigroup;
- true post-collisional trajectories;
- fixed-genealogy rather than falsely uniform analytic exponents;
- dominated-convergence summation as a possible strategy; and
- explicit real-source exhaustion and conservative repair as necessary interfaces.

## Required reconstruction

The authors must prove a uniform block-time absolute-continuity estimate for the summed cyclic sector, not merely a fixed-horizon \(o(1)\) result. They must construct the physical Jacobi minor and its genealogy majorant quantitatively. Only after a complete grand-canonical marked LDP exists should the nonlinear conservative repair and B1 microcanonical transfer be attempted.

## Recommendation

**Reject.** Round 12 removes several false shortcuts, but the replacement recollision theorem does not deliver the blockwise modulus required for sewing, and its two main geometric/cluster inputs remain unproved. The full actual-contact LDP is therefore not established.