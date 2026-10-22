# Mathematical audit of native pressure module 326

Audit status: complete native proof and final exact-algebra runs. The root has reconstructed the proof and budget; the review-baseline agent has independently reconstructed the same final native source and found no defect in its stated scope. This document records the author's mathematical reconstruction and finite verification. It does not replace the proof body or claim independent-expert certification.

## Source identities

- New proof: `326_physical_boundary_stopping_pressure.tex`.
- SHA-256 at this audit: `9d385ad65261b1a2451c6777270547fcf8bba4b7ce0972bd45dd2c75faa7f5b5`.
- Auxiliary checker: `check_326_boundary_pressure.py`.
- Checker SHA-256: `d79328d2189db2bdf333f680cb79ccb8f98916fce4506f81979fc9071b740a87`.
- New canonical-source input 324 independently read for the part used here, including its final seam and optical-conjugacy clarifications: SHA-256 `e366f8323739bf995309192cb183fa791ebb91766b0f49961fec65e4873ab5c0`.
- Inherited native source retrieved at commit `4d83de89d16bae7f9e9439dcc80e099b8f8f5c4e`, article `papers/A2-DYN-critical-source-transport-author-revision`.
- Inherited 318 Git blob: `ad795026d7925cc55d6bfe4669942a2e916b2471`.
- Inherited 321 Git blob: `33a39842e29325b77f5049fe8e4fc1d06ea76ec6`.
- Inherited 313 Git blob: `eeea54a681134e9fae78d68bb2e56a4cdb9c5071`.
- Local source copies downloaded for this research remain under `new-round-pressure/native/`.

Root provenance and publication manifests determine the controlling final baseline. These identifiers specify exactly the inherited files read by this author. The independent author reconstruction is recorded separately in `new-round-ci/math-reconstruction/326_INDEPENDENT_AUTHOR_RECONSTRUCTION.md`, bound to the same final proof hash. This is collaborative proof reconstruction, not external expert certification.

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

The uncapped horizontal source input of 324 was reconstructed in its actual qualified enlarged class from 284. Its auxiliary growth partition need not equal the original homogeneity partition used for stopping in 326. Its physical first-hit count does not include optional coordinate seam cuts: those are paid by the displayed length-subdivision allowance, while one-flight and terminal images use continuous unwrapped angles. The exact conjugacy `B(c') D = K(c') P(tau) B(c)` and terminal identity `c_l (0,1) B(c_l)^(-1) K(c_l) = (kappa_l,c_l)` verify precisely `l` true flights and `l-1` intermediate kicks. No initial or terminal reflection is silently duplicated.

## Inherited consequences activated by the new input

The complete proof bodies of modules 266–269 were read, not inferred from their titles. With native 313's `C0=30000`, `C1=6400` and the newly proved `Q*=Qstop`, their constants are
\[
C_\star=\frac{30000Q_{\rm stop}}{2c_*\lambda_\circ},
\qquad K_\star=6400D Q_{\rm stop}.
\]

| Inherited module and source SHA-256 | Consequence enabled, with all other hypotheses retained |
|---|---|
| 266: `c235cb3284db7cc23a8734fe159b0d86ad9080bbdb2acf20b71584c84c74ef01` | Full target-roof multiple-incidence and product insertions, followed by factorial witness bounds. |
| 267: `d253307587292a19e78ba74e519ceb9fea6a578564a6858a0de7c08b8d800a2e` | Payment of the stated deep/numerous incidence events in the original ordered height; exact source preservation. |
| 268: `5f223489e32e79565614895181e8e55d92f90a97c9455ab6cdd4769660e6512a` | Joint incidence-load exponential moments and tails, and the quadratic witness-count tail. |
| 269: `7d3eb30b03741249c19fc92bbc7e5414f0ddb24e570984057db4fe81156a1a99` | The specified high-load payment, source decomposition and retained low-load equivalence. |

These are inherited consequences activated by a new proved input, not new proofs or new claims that the raw theorem is complete. In 267–269 the collision-dependent thresholds are substituted into bounds already valid at every finite count. The outer parameters remain fixed before the collision limsup. The remaining low-load shortage is still an assertion to prove. Neither an inverse-incidence insertion nor these incidence-tail payments supplies an `m^-2` same-roof estimate for a single unvisited-clearance witness.

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

The final checker accepts `--details PATH` and `--source PATH`. Its installed default resolves `../core/326_physical_boundary_stopping_pressure.tex` from a script directory; the scratch fallback is the same-directory native proof. Mathematical stdout and detail JSON omit runtime metadata. The receipt stores interpreter and timestamps separately. The final runs bind the source and checker hashes listed above.

Earlier successful receipts and their then-current audit remain byte-for-byte under `preliminary/326_before_final_scope/`. Their embedded source hash describes the earlier source they actually checked. They have not been relabeled as final-source runs.

The first scratch implementation attempted a SymPy import and failed because that dependency was absent. It was replaced by a small exact polynomial ring over rational numbers using only the standard library. The successful runs described above use that final implementation.

Continuous geometric completeness rests on the native proof bodies and independent reconstruction, not these finite scripts.

