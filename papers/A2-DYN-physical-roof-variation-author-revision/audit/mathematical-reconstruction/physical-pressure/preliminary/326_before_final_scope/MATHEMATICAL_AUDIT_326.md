# Mathematical audit of native pressure module 326

Audit status: complete native proof drafted; independent reconstruction by the root and review-baseline agent requested. This document records the author's mathematical reconstruction and finite verification. It does not replace the proof body or claim independent-expert certification.

## Source identities

- New proof: `326_physical_boundary_stopping_pressure.tex`.
- SHA-256 at this audit: `fec7330ba0339bae69de5a4471645e5df5364568b2aa090f73eca9ac5260fb8f`.
- Auxiliary checker: `check_326_boundary_pressure.py`.
- Checker SHA-256: `85a3dcc7544baeb392a09eb102eaa6f50e97e07ebc9d2d9ad6a32bf88e3aa33d`.
- New canonical-source input 324 independently read for the part used here: SHA-256 `314529c81f4f55080733acf473aa64d9af0b8bb41255eae2234df8d961e75255`.
- Inherited native source retrieved at commit `4d83de89d16bae7f9e9439dcc80e099b8f8f5c4e`, article `papers/A2-DYN-critical-source-transport-author-revision`.
- Inherited 318 Git blob: `ad795026d7925cc55d6bfe4669942a2e916b2471`.
- Inherited 321 Git blob: `33a39842e29325b77f5049fe8e4fc1d06ea76ec6`.
- Inherited 313 Git blob: `eeea54a681134e9fae78d68bb2e56a4cdb9c5071`.
- Local source copies downloaded for this research remain under `new-round-pressure/native/`.

Root provenance and publication manifests determine the controlling final baseline. These identifiers specify exactly the inherited files read by this author.

## Actual new conclusion and input chain

The new conclusion is the original all-word pressure bound
\[
 \sup_{R\in[9/20,47/100],\,N\ge0}
 \sum_{w\in\mathcal W_N(R)}
 \sup_{x\in[w]_R\cap M'_R}J^sT_R^N(x)<\infty.
\]

This closes the formerly separate pressure clause of Input v112, provided native 324 is integrated and independently verified as stated. It does not assert the full raw pointwise local limit theorem, uniform twisted spectral estimates, exact arithmetic reconstruction, or the remaining original roofwise positive-source shortage.

The proof uses:

1. Native 318's radius-uniform comparison across arbitrary actual records of the same complete word and matching past strips at precisely \(-1,\ldots,-N\), including arbitrary cone directions.
2. Native 319's complete *positive-clearance* marked-source branch-supremum budget.
3. New 324's horizontal source branch-supremum budget and its exact internal collision factor \(c_i\).
4. The physical finite horizon, strictly separated circular obstacles, exact reflection differential, and the original collision-area form.

It does not use the unproved cell-abundance hypothesis, a replacement Markov model, the full raw theorem, or a radius-uniform version of Baladi–Demers. It does not deduce pressure from a bulk or roof integral.

## Critical inequality and normalization reconstruction

Let the positive physical derivative product be
\[
 D_N=\begin{pmatrix}A&B\\ C&D\end{pmatrix},
 \qquad \det D_N=c_0/c_N.
\]
The actual derivative in \((s,\varphi)\) is \((-1)^N D_N\). With
\(e_R=(1,-\kappa_R)/\sqrt{1+\kappa_R^2}\), define the finite-record continuous weight
\[
 w_N(T^Nx)=|DT^{-N}(T^Nx)e_R|^{-1}.
\]
The proof retains both coordinate conversions:
\[
 u_x=|\partial_{\alpha_0}p_N|^{-1}
       ={1\over Rc_NC},
\qquad
 w_N={c_0\sqrt{1+\kappa_R^2}\over
 c_N\sqrt{(D+\kappa_RB)^2+(C+\kappa_RA)^2}} .
\]
Consequently
\[
 w_N\le R_+\sqrt{1+(20/9)^2}\,c_0u_x.
\]
The terminal incidence cancels between two exact identities. In particular terminal grazing is **not** declared to have zero stable weight.

The stable line only enters through native 318 at the same current point:
\(j_N\le C_\times w_N\).
No stable-line continuity at a singular point is asserted. The second use of \(C_\times\) compares the almost-maximizer to any representative in the chosen real word/open past-strip class. Hence the final constant correctly contains \(C_\times^2\), not one copy and not a collision-count power.

The canonical two-half determinant from 324 is taken in the actual central coordinates \((\alpha_i,\varphi_i)\). Its absolute determinant is the **positive sum**
\[
 A_-^{\rm hor}Y_+ +Y_-A_+^{\rm hor}.
\]
The collision-area form is \(c_i\,d\alpha_i\,d\varphi_i\), with no additional \(R^{-1}\). Thus
\[
 u_x\le {53\over12}\,c_i
                 (A_-^{\rm hor}A_+^{\rm hor})^{-1}.
\]
The retained \(c_i\) is indispensable for summing all original horizontal homogeneity levels.

## Full physical stopping reconstruction

The affine fiber is the intrinsic circle-seam-safe curve
\[
 s_N=R(\vartheta-\varphi_N)\pmod{2\pi R},
 \qquad -\pi/2<\varphi_N<\pi/2.
\]
Choose the connected component of its intersection with a complete actual past word and **open** strips at \(-1,\ldots,-N\). A first endpoint exists in the closed angle interval.

Each fixed past strip has closure a positive distance from grazing. This distance is allowed to depend on the selected label; no uniform lower incidence is introduced. Hence all past visited incidences stay positive along the stopped interval. Finite consecutive-disk separation keeps every listed flight positive. The simple circle-intersection root continues the *prescribed* word uniquely at the endpoint.

If current grazing and a past homogeneity boundary are absent, then a failure of actual first-hit continuation must be a genuine unvisited tangency. A limit of exterior physical segments cannot enter the interior of a disk. Uniform flight bounds reduce the clearance test to finitely many relevant disks. Strict clearance to all of them would extend the interval, a contradiction. Disjoint obstacles prevent an unvisited tangent foot from coinciding with a listed endpoint.

This argument handles arbitrarily short and disconnected physical word domains. It uses neither planar convexity nor a special boundary arc or nonzero linearized sector. The selected affine interval itself gives the accessible path to the stopping event.

## Common-level transfer and no hidden multiplicity

For each assigned event, its interior distance is continuous, strictly positive on a tail, and tends to zero. The intermediate-value theorem therefore gives representatives at **every sufficiently small positive level**. A finite selected word family allows a common level by taking a finite minimum.

This remains entirely inside the selected actual word/open-strip class. No derivative is evaluated at the stopping boundary. No limiting trace word is assumed unique.

For internal and endpoint horizontal sources, the regular physical map takes an open record neighborhood to an open phase neighborhood, so an exact horizontal level leaves an open angular interval.

For a marked flight,
\[
 \det{\partial(\vartheta,b)\over\partial(s_j,\varphi_j)}=c_j>0.
\]
Thus the fixed positive clearance level likewise leaves an open angular interval in the same class. Two countable/null source-cut sets cannot exhaust it. The representative can be chosen on actual forward and backward source intervals.

One selected word is assigned exactly once. At a common source level an overlay interval fixes the complete actual physical word. Translating the uniquely reconstructed initial disk to the original fundamental copy removes periodic lift multiplicity. Therefore distinct selected words cannot charge one overlay interval. No count of unvisited disk labels is added: the marked source already uses the one-copy reconstruction.

## All grouping constants checked

Write
\[
 S_{\mathcal H}=2\sum_{k\ge k_0}\sin(k^{-2})
                    \le {2\over k_0-1}.
\]

| Stopping type | Group labels | Source budget after all groups |
|---|---|---|
| Current/terminal grazing | terminal sign, two possibilities | \(2H_{\rm hor}\) |
| Initial horizontal homogeneity | level and interior side | \(2S_{\mathcal H}H_{\rm hor}\) |
| Internal horizontal homogeneity | collision \(1\le i<N\), level, interior side | \(4S_{\mathcal H}(53/12)H_{\rm hor}E_{\rm cs}/(1-\sigma)\) |
| Genuine unvisited tangency | flight \(0\le j<N\); both signs already in 319 | \(2Q_{\rm mb}/(1-\sigma)\) |

Here \(E_{\rm cs}=47/6\), \(\sigma=47/59\). The internal sum is
\[
 \sum_{i=1}^{N-1}(\sigma^{i-1}+\sigma^{N-i-1})
     ={2(1-\sigma^{N-1})\over1-\sigma},
\]
including its zero value at \(N=1\). The marked sum is
\(2(1-\sigma^N)/(1-\sigma)\).
The two signed sides of each horizontal homogeneity level have been paid separately. Both mark signs are paid only once, inside 319.

## Suprema and limit order

At fixed \(R,N\), first choose a finite family of physical words and an \(\epsilon\)-maximizer of the continuous affine weight in each. Pullbacks of the finitely relevant horizontal levels are regular coordinate hypersurfaces, so these maximizers can be chosen off the artificial boundaries.

Common-level representatives are chosen only for that finite family. The selected word weights on the left are independent of the common positive level. Letting an internal source level approach a homogeneity boundary changes only the explicit factor \(\cos(h+\varepsilon\delta)\) on the upper bound. No derivative, trajectory, invariant stable line, density, or essential supremum is passed through that limit.

The bound is uniform in the finite family. Nonnegative exhaustion and then \(\epsilon\downarrow0\) recover the full word suprema. Finite horizon actually gives finitely many physical \(N\)-words, but the finite-family argument avoids any measurable selection requirement.

These auxiliary limits occur at fixed physical collision count. They do not exchange the original outer \(B\)-limit, \(m\)-limsup, roof essential supremum, radius supremum, or microscopic-window limits.

## Verification executed

The standard-library checker executes 1,251 exact checks, including positive-polynomial identities, rational matrix checks on the allowed coefficient rectangle, exact geometric sums, and telescoping strip-tail majorants. The rational coefficient cases are explicitly **not** represented as independently realizable physical trajectories.

Both ordinary and `python -O` runs exited zero and produced byte-identical deterministic stdout. Runtime, timestamps, commands and output digests are in `EXECUTION_326.json`; normal and optimized detail/output files are preserved. The checker uses no `assert` gates.

The first scratch implementation attempted a SymPy import and failed because that dependency was absent. It was replaced by a small exact polynomial ring over rational numbers using only the standard library. The successful runs described above use that final implementation.

Continuous geometric completeness rests on the native proof bodies and independent reconstruction, not these finite scripts.

