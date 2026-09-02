# External Referee Report on the Round-Twenty-One Revision

## Recommendation: **Reject — not suitable for a major-revision decision**

**Repository:** `TrillionniumFoundation/theta-theory`  
**Reviewed branch:** `revision/round21-referee-positive-closure-11paper-2026-09-02`  
**Pre-review head:** `229cc83ca394268b4c9030067ba7f3b4389a4c73`  
**Review date:** 2 September 2026  
**Scope:** the active `main.tex` wrappers, the eleven active `ROUND17_POSITIVE_CLOSURE.tex` replacement modules, the Round-Twenty author response, the Round-Twenty-One dependency ledger, revision status, and internal rereview.

This report applies the correctness, self-containedness, significance, and presentation standard expected at *Annals of Mathematics*, *Inventiones Mathematicae*, *Journal of the American Mathematical Society*, or *Acta Mathematica*. It is deliberately severe because the manuscripts advertise theorem packages that, if correct, would settle or substantially strengthen difficult results in several unrelated fields.

The compilation status is not in dispute. The question is whether the displayed arguments prove the displayed theorems. They do not.

---

## 1. Confidential recommendation to the editor

I recommend **rejection of the entire eleven-paper dossier, without treating the present submission as a candidate for major revision**.

This conclusion is not based merely on omitted routine details. Several central statements are false as written, and several proofs contain one-line algebraic, measure-theoretic, or topological contradictions. In particular:

1. A4 attempts to remove a transmission zero by adjoining a residue of the full resolvent at a point where the full resolvent is explicitly assumed analytic. That residue is zero.
2. A4's claimed large-\(z\) cancellation for the memory transform is algebraically wrong: the generic leading term is \(z^{-1}(PL^2P-(PLP)^2)\), not \(O(z^{-2})\).
3. B1's canonical pressure \(N^{-1}\log Z_{\varepsilon,N}\), with the displayed \(1/N!\) and no compensating activity factor, tends to \(-\infty\) at rate \(-\log N\).
4. B3's proposed second variation of the collision entropy is incorrect. At \(q=1\), moving along the zero-cost manifold \(\Gamma=A_f\) gives zero collision action, while the manuscript's quadratic form is strictly positive in general.
5. C1 requires deterministic hidden transitions to possess densities bounded above and below with respect to one fixed probability measure. An uncountable family of Dirac kernels cannot have this property.
6. A3's empirical transition measure is unordered and therefore cannot determine the concatenated physical path that the state is claimed to encode.
7. A3's recovery replaces a continuous reference kernel by atoms, which normally have infinite relative entropy.
8. B4's claimed compact action sublevels already fail at time zero on the stated energy shells.

These defects alone force rejection. The remaining problems show that the failure is systematic rather than local.

The correct editorial classification is therefore not “interesting paper with gaps” but “the advertised theorem packages have not been established, and some are demonstrably false in their present formulation.”

---

## 2. What was actually reviewed

The latest revision does contain mathematical source changes rather than only reports or branch metadata. Each wrapper now inputs an active replacement file. The repository's internal checks establish that the files exist, contain theorem/proof environments, avoid a finite blacklist of old phrases, and compile.

Those checks do **not** establish any of the following:

- that a defined operator is well typed;
- that a claimed topology has the asserted compact sets or dual;
- that a periodic-data argument proves lattice aperiodicity;
- that an entropy recovery control is absolutely continuous with respect to the reference kernel;
- that a local central limit theorem has the stated covariance;
- that a high-frequency bound follows from the available integration variables;
- that a short-time cluster expansion concatenates to arbitrary finite time;
- that a Hessian calculation is correct;
- that weak convergence of processes yields convergence of predictable brackets;
- or that an analytic residue at a regular point is nonzero.

The active modules are generally only a few hundred lines long, yet each claims a package that would normally require a substantial paper. Their proof paragraphs repeatedly replace the hard step by a name (“growth lemma,” “coarea,” “Kawashima compensator,” “standard compactness,” “implicit-function theorem,” “Dolgopyat,” “Mitoma,” “Trotter--Kato”) without stating and verifying the hypotheses needed in the actual singular, countable-state, weighted, or nonautonomous setting.

A further serious presentation failure is that the active replacement modules contain essentially no literature citations. The wrappers load and print bibliographies, but the mathematical text does not locate the results relative to the existing literature or identify which exact external theorem is being invoked. At this level, “standard” is not a substitute for a precise citation and hypothesis check.

---

## 3. Dependency-level assessment

The repository records the order

\[
A2\to A3\to A4,\qquad
B2_{\rm GC}\to B1\to B2_{\rm MC}\to B3\to B4,
\]
followed by C1, C2, and D1.

That bookkeeping is useful, but it makes the present verdict worse:

- A2's arithmetic and Fourier claims fail, so A3's conditioning theorem and A4's renewal inputs are unavailable.
- A3's state and recovery fail, so A4's “exact history” platform does not exist in the asserted form.
- B2's recollision and finite-time concatenation arguments fail, so the pressure imported by B1 is unavailable.
- B1 has independent normalization and covariance errors, so the microcanonical B2 theorem and B3's Schur-corrected cumulants are unavailable.
- B3's quadratic form is wrong, so B4 and C2 cannot import the claimed tangent inverse.
- B4's compactness and transfer fail, so C1's reachable-chart and continuous-time control claims are unavailable.
- C1's common domination is impossible for the deterministic kernels it includes, so C2 and D1 lose their observation and phase-mixture interfaces.
- D1 therefore has no valid component theorem family to synthesize.

An acyclic graph of invalid implications remains invalid. A dependency ledger cannot replace proofs at the root nodes.

---

## 4. Decisive mathematical contradictions

### 4.1 A4: the proposed transmission closure adds the zero space

A4 defines \(Z\) to be the zeros of the compressed transfer matrix \(C(z)\) **away from poles of the full resolvent**
\[
R(z)=(z-L)^{-1}.
\]
It then enlarges the resolved space using
\[
\operatorname{Ran}\operatorname*{Res}_{z=z_0}R(z)P,
\qquad z_0\in Z.
\]

But “away from poles of the full resolvent” means that \(R(z)P\) is holomorphic at \(z_0\). Hence
\[
\operatorname*{Res}_{z=z_0}R(z)P=0.
\]
Every purported generator vector is zero. Consequently
\[
\mathcal R^\sharp=\mathcal R,
\]
and the construction cannot remove a single transmission zero. The proof's discussion of “complete finite Jordan chains” concerns poles/eigenvalues of \(R\), not zeros of the compression at regular points. The lemma is false by its own definitions.

### 4.2 A4: the memory-transform asymptotic is wrong

Assume enough domain regularity for the expansion used by the manuscript. Write
\[
C(z)=P(z-L)^{-1}P
   =z^{-1}I+z^{-2}A+z^{-3}B+O(z^{-4}),
\]
where
\[
A=PLP,\qquad B=PL^2P.
\]
Then
\[
C(z)^{-1}
 =zI-A+z^{-1}(A^2-B)+O(z^{-2}).
\]
Therefore A4's own definition
\[
\widehat K(z)=zP-PLP-C(z)^{-1}
\]
gives
\[
\widehat K(z)
 =z^{-1}(B-A^2)+O(z^{-2})
 =z^{-1}PLQLP+O(z^{-2})
\]
whenever the block products are defined. The coefficient is generically nonzero. The asserted \(O(|b|^{-2})\) vertical decay does not follow, and the claimed absolutely integrable shifted-contour argument collapses.

### 4.3 B1: the displayed canonical pressure diverges

B1 defines
\[
Z_{\varepsilon,N}(H,\lambda)
 =\frac1{N!}\int_{\mathcal D_{\varepsilon,N}\times\mathbb R^{3N}}
   \exp\!\left\{\sum_{i=1}^N\lambda\!\cdot C(x_i,v_i)
        +\mu_\varepsilon H(\mathbf X)\right\}\,d\mathbf x\,d\mathbf v
\]
and
\[
q_N(H,\lambda)=\frac1N\log Z_{\varepsilon,N}(H,\lambda).
\]

At \(H=0\), on every multiplier compact where the one-particle integral is finite,
\[
Z_{\varepsilon,N}(0,\lambda)
 \le \frac{M(\lambda)^N}{N!}.
\]
Stirling's formula gives
\[
q_N(0,\lambda)
 \le \log M(\lambda)-\frac1N\log N!
 =-\log N+O(1)\longrightarrow-\infty.
\]
Hard-core exclusion only lowers the integral. An \(O(N)\) source term cannot cancel the missing \(N\log N\). The theorem claiming convergence to a finite strictly convex \(q(H,\lambda)\) is false unless the model is redefined with a compensating activity/reference normalization that is absent from the manuscript.

### 4.4 B3: the collision-action Hessian is incorrect

Let
\[
A_{f_\eta}=e^{\eta a+O(\eta^2)}A_f,
\qquad
q_\eta=qe^{\eta k+O(\eta^2)},
\qquad
\ell(q)=q\log q-q+1.
\]
The collision integrand is
\[
e^{\eta a}\ell(qe^{\eta k}).
\]
Its second derivative at zero is
\[
\ell(q)a^2
 +2q\log(q)\,ak
 +q(1+\log q)k^2,
\]
before adding second-order chart corrections and the linear first-variation terms that those corrections may pair with.

This is not
\[
q\,|k+a|^2,
\]
the form stated in B3.

The contradiction is clearest at \(q=1\) and \(k=0\). Then
\[
\Gamma_\eta=A_{f_\eta},
\]
so the collision action is identically zero because \(\ell(1)=0\). Its second variation is zero. B3's formula instead gives \(a^2/2\), generally positive. Thus the Mosco theorem and the asserted inverse-covariance identification cannot be correct as stated.

### 4.5 C1: common domination of deterministic transitions is impossible

For a deterministic hidden evolution \(x\mapsto\Phi_\vartheta^a(x)\), the transition kernel is
\[
M_\vartheta^a(x,dx')=\delta_{\Phi_\vartheta^a(x)}(dx').
\]
C1 requires all such kernels on an uncountable reachable chart to have densities with respect to one fixed probability \(m_0\), bounded above and below.

Domination would require
\[
m_0(\{\Phi_\vartheta^a(x)\})>0
\]
for every reachable image point. A probability measure has at most countably many atoms of positive mass. Hence an uncountable family of distinct Dirac kernels cannot be dominated by such an \(m_0\), let alone have uniformly bounded positive densities. This directly contradicts the hard-sphere finite-volume deterministic flow and the deterministic kinetic state evolution included in the theorem.

Likewise, a probability density cannot have a uniform positive lower bound on an infinite-measure Euclidean/counting stratum. The regular chart on which the filtering, LAN, and Bernstein--von Mises results are built therefore does not exist as stated.

### 4.6 A3: an unordered empirical measure cannot encode an ordered path

A3 defines the stopped state as
\[
Z=(\Theta,\mathsf C,\zeta),
\]
where \(\Theta\) is an empirical transition measure, \(\mathsf C\) records clocks, and \(\zeta\) is the terminal prefix. It then asserts that concatenation of the excursions is a continuous deterministic image of this state.

An empirical transition measure forgets temporal order. Two legal sequences can have the same transition occupation counts, total clocks, and terminal prefix but traverse different Eulerian orderings and hence generate different concatenated paths. Even the elementary mark sequences \(AB\) and \(BA\) have the same empirical mark measure and clock totals but different ordered paths. Recording source and target histories in a balanced transition measure does not, in general, select one Eulerian ordering.

Therefore there is no well-defined “concatenated path” map from the stated \(Z\). The path-level LDP is not even formulated on a sufficient state.

### 4.7 A3: the proposed recovery has infinite entropy

A3's recovery proof partitions the continuous mark space into cells and then says to “choose an actual physical mark in every mark cell.” For a non-atomic reference kernel \(\mathcal K_R(x,\cdot)\), the resulting atomic transition
\[
q_x=\delta_m
\]
satisfies
\[
H(\delta_m\mid\mathcal K_R(x,\cdot))=+\infty
\]
whenever \(\mathcal K_R(x,\{m\})=0\). Positive reference mass of the surrounding cell does not make an atom absolutely continuous.

A valid finite-cell approximation would have to retain a conditional density on each cell, not replace it by a representative point, and would then need a separate argument preserving exact physical compatibility. The stated legal recovery theorem is false.

### 4.8 B4: the announced compact state/action sublevels are not compact

Take a smooth probability density \(\varphi\) concentrated near \(v=0\), and let \(\varphi_n(v)=\varphi(v-ne_1)\). Define
\[
f_n=(1-n^{-2})\varphi+n^{-2}\varphi_n.
\]
The masses are one and the second moments are uniformly bounded. The measures converge narrowly to \(\varphi\), but a quadratic-growth test detects a nonvanishing unit of energy escaping to infinity:
\[
\int |v|^2 f_n\,dv-\int |v|^2\varphi\,dv\longrightarrow 1.
\]
Thus there is no convergent subsequence in the topology generated by the manuscript's tests of up to quadratic growth. The energy shell \(\mathcal E_M\) is not compact in that topology.

Starting each \(f_n\) on the zero-cost control \(q=1\) gives an action-sublevel sequence whose failure occurs already at \(t=0\). The claimed path compactness cannot be rescued by a dynamic estimate not assumed in the state space.

---

## 5. Paper-by-paper report

## A1 — *Deterministic Path Ensembles, Driven Collision Maps, and Endogenous Conjugate Parameters*

**Decision: reject.**

### A1.1 The response theorem assumes a rate not implied by its hypothesis

The theorem allows an arbitrary current \(J_a\) in the weighted Hilbert current space and then uses a geometric finite-cylinder approximation rate. Membership in a Hilbert completion guarantees only
\[
\|J-J^{(n)}\|\to0.
\]
It gives no uniform exponential rate. In any infinite-dimensional Hilbert space, projection tails can converge arbitrarily slowly. Consequently the passage from finite-cylinder differentiation to an absolutely convergent all-order response tree is unsupported.

The statement also writes expressions such as \(\int J_a\,d\mu_a\) without defining whether \(J_a\) is a state observable, a random current, a dual test functional, or a fixed Hilbert vector. The current space and the probability space are not connected by a measurable map of the required type.

### A1.2 The FCLT is a template, not a proof

The increment \(Y_k\) is not constructed precisely enough to verify stationarity, measurability, centering, the projective condition, or the claimed depth decomposition. The crucial estimate
\[
\sum_n\|\mathbb E(Y_n\mid\mathcal F_0)\|<\infty
\]
is asserted from symbolic mixing without proving that the current-valued observable belongs to the Banach class on which that mixing estimate holds.

Trace-class covariance is likewise not obtained merely by summing coordinate variances after naming a weighted basis. One needs a genuine trace estimate for the covariance operator of the actual increment.

### A1.3 The current calculus is underdefined

The “incidence-completed labelled current calculus,” fixed-fibre connection, and derivative \(\partial_a\) are described in prose, but domains, coordinate identifications, and closure are not specified at the level needed to make the material derivative an operator. Saying that a transpose is bounded and “therefore closed after graph closure” does not establish that the original geometric derivative is represented by that transpose.

### A1.4 Significance

The mapping-torus suspension itself is standard. The potential novelty lies in the response/current package, precisely where the mathematical construction is missing. The manuscript therefore does not meet a top-journal correctness or significance threshold.

---

## A2 — *Homological Liouville Path Ensembles and Projective Empirical-Process Large Deviations*

**Decision: reject.**

### A2.1 Real linear independence is not lattice aperiodicity

The periodic-data lemma produces four real-linearly independent difference vectors \(d_j\) and claims that this forces the Fourier parameter \((u,v,b)\) to vanish.

The periodic equations only imply
\[
D^\top\omega\in 2\pi\mathbb Z^4,
\qquad D=(d_1,\dots,d_4).
\]
If \(D\) is invertible, this gives
\[
\omega=2\pi D^{-\top}k,\qquad k\in\mathbb Z^4,
\]
not \(\omega=0\). There are generally infinitely many nonzero solutions, including solutions with nonzero roof frequency \(b\). The required conclusion is a statement about the closed subgroup generated by *all* periodic data, together with the period/constant phase, not about the nonzero determinant of four real vectors.

The subsequent assertion that the base periodic equation forces \(c=0\) also requires an exact gcd/period argument absent from the text.

### A2.2 The two-block coarea argument uses dependent variables as independent coordinates

The proof selects “coordinates” \(x_1,x_2\) in two returns of one deterministic orbit and integrates by parts once in each. But the second return coordinate is a deterministic image of the first. The proof does not construct a legitimate change of variables from the original integration domain to two independent coordinates, nor does it give a lower bound for the corresponding full Jacobian.

A UNI derivative along one unstable coordinate does not automatically produce two independent integration directions or a \(b^{-2}\) matrix-coefficient bound. This is the decisive missing step in the very-high-frequency estimate.

### A2.3 Weighted branch complexity is not proved

An exponential tail for return times and an integral identity for inverse Jacobians do not by themselves imply a summable family of branchwise \(C_*^2\), \(C_*^4\), and four-parameter derivative norms. Passing from integral mass to supremum derivative norms over countably many shrinking branches requires explicit domain-size and distortion estimates. The proof replaces this with a sentence.

### A2.4 The LLT is unsupported

The raw unsmoothed LLT relies simultaneously on:

- a valid common anisotropic Banach bundle;
- exact lattice aperiodicity;
- uniform nondegenerate covariance;
- a medium-frequency Dolgopyat estimate;
- an integrable high-frequency majorant;
- and absolute continuity with sufficient uniformity.

None is proved at the stated level. The local theorem and all downstream conditioning claims therefore fail.

---

## A3 — *Full Liouville Empirical-Path Large Deviations and Information Projections for Finite-Horizon Sinai Billiards*

**Decision: reject.**

### A3.1 The state does not determine the claimed observable

As shown in Section 4.6, the unordered transition occupation \(\Theta\) does not determine the expanded physical path. The central state space is therefore insufficient for the theorem it is supposed to support.

### A3.2 The uniform exponential moment is not derived

A2 supplies, at best, a stationary weighted return estimate. A3 asserts
\[
\sup_x\int e^{\eta\chi(m)}\,\mathcal K_R(x,dm\,dx')<\infty.
\]
Uniformity over the complete-history state is much stronger than an invariant-average tail bound. Stable-holonomy distortion on regular charts does not control every history near every singularity. No proof closes this gap.

### A3.3 The claimed lower tightness of the number of returns is false

Let the reference return tail satisfy roughly
\[
\mathcal K(r\ge N)\asymp e^{-cN}.
\]
A controller may condition the first mark on \(r\ge N\). The relative entropy cost is \(O(N)\), which is allowed by the manuscript's normalized entropy sublevel, while the stopping index is \(\nu_N=1\). Hence
\[
\nu_N/N\to0.
\]
The claimed lower tightness does not follow from the entropy bound and exponential reference tail.

### A3.4 Recovery produces infinite KL cost

The atomic-cell error from Section 4.7 is fatal. The connectors do not fix it. A finite directed graph of representative physical marks is generally singular with respect to the continuous reference transition kernel.

### A3.5 The conditional LDP misuses A2 insertions

The numerator contains \(e^{-NF}\) for a path-level functional. This is not a fixed bounded cylinder insertion of the kind appearing in an LLT. Reducing a full path functional to finite-memory approximants is not exponentially harmless merely because the state is tight. The claimed cancellation of local prefactors is unproved.

---

## A4 — *Exact History Dynamics, Domain-Safe Memory, and Universal Excess Path Pressure*

**Decision: reject.**

### A4.1 The minorization proof fails on its own Lyapunov sublevels

With
\[
V(x)=\sum_{j\ge0}\rho^j\chi(e_{-j}),
\]
a bound \(V(x)\le C\) does not make the remote past tail uniformly small. Put one excursion cost of size \(C\rho^{-n}\) at depth \(n\). Then \(V=C\), but the contribution beyond any fixed truncation remains \(C\) when \(n\) is farther out.

Thus a \(W\)-sublevel cannot be uniformly approximated by finitely many history cylinders in the manner used to prove a common small set. The Harris spectral gap is not established.

### A4.2 The rough-path theorem lacks observable regularity

A moment bound
\[
|A|^{2+\epsilon}\le C(1+W)
\]
does not place \(A\) in the weighted Lipschitz Banach space on which the Poisson solution is claimed. A spectral gap on one Banach space does not solve the Poisson equation for every measurable \(L^{2+\epsilon}\) observable. The martingale-coboundary decomposition is therefore unavailable under the stated hypotheses.

### A4.3 The renewal factorization is only formal

The “exact history” boundary operator is not shown to be boundedly intertwined with A2's anisotropic billiard operator. Entry, exit, trace, and residual-flight maps are named but not defined with domains and norms. Meromorphic continuation of a scalar leading eigenvalue does not automatically produce the asserted full resolvent estimates.

### A4.4 Transmission closure and memory decay are false

The residue and high-frequency contradictions in Sections 4.1 and 4.2 independently invalidate the central memory theorem. In addition, finitely many poles in a strip do not imply finitely many zeros of a finite-dimensional analytic compression without a separate zero-counting/growth argument.

---

## B1 — *Microcanonical Preparation and Exponential-Scale Ensemble Transfer for Deterministic Hard Spheres*

**Decision: reject.**

### B1.1 The canonical normalization is wrong

Section 4.3 gives a direct contradiction. This error occurs in the first principal theorem and contaminates the saddle, coefficient extraction, and microcanonical pressure.

### B1.2 The block selection is not a valid product damping argument

The set of “fresh” blocks depends on the full configuration. To multiply one-block characteristic-function contractions, the selection must be measurable and predictable with respect to the successive conditioning sigma-fields, with uniform conditional regularity after previous selections. A posterior finite-atlas statement does not provide this. There are combinatorially many particle subsets, not finitely many possible selected block families.

The alleged exceptional event is first assigned probability \(e^{-cN}\), which would yield a frequency-independent remainder and destroy integrability over all frequencies. The later proof changes the assertion and says the exceptional set is covered by other charts. Those are different claims.

### B1.3 \(W^{s,1}\) push-forward regularity is not automatic

A smooth density restricted to a compact chart with boundary does not automatically push forward to a globally \(W^{s,1}\) density. Boundary terms appear under integration by parts unless the partition and density vanish to sufficient order. The proof supplies neither a boundary-compatible atlas nor uniform extension estimates.

### B1.4 The mixed lattice--continuous LLT has the wrong covariance

Partition the joint covariance as
\[
\Sigma=
\begin{pmatrix}
\Sigma_{\mathbb Z\mathbb Z}&\Sigma_{\mathbb Z\mathbb R}\\
\Sigma_{\mathbb R\mathbb Z}&\Sigma_{\mathbb R\mathbb R}
\end{pmatrix}.
\]
Conditioning on a lattice deviation \(z_{\mathbb Z}\) shifts the continuous Gaussian mean by
\[
\Sigma_{\mathbb R\mathbb Z}
\Sigma_{\mathbb Z\mathbb Z}^{-1}z_{\mathbb Z}
\]
and replaces the continuous covariance by the Schur complement
\[
\Sigma_{\mathbb R\mathbb R}
-\Sigma_{\mathbb R\mathbb Z}
 \Sigma_{\mathbb Z\mathbb Z}^{-1}
 \Sigma_{\mathbb Z\mathbb R}.
\]
B1 instead multiplies a lattice Gaussian term by an unshifted \(\gamma_{\Sigma_{\mathbb R}}(D)\). That is false unless the cross covariance vanishes, an assumption nowhere made.

---

## B2 — *Collision-Marked Trajectory Clusters and Joint Dynamic Large Deviations for Deterministic Hard Spheres*

**Decision: reject. This is a failed root paper.**

### B2.1 Entropy/moment bounds do not give the stated trace exclusion

Finite trace mass and velocity moments do not force
\[
\lambda^-\{|(v_i-v_j)\cdot\omega|<\delta\}\le C\delta^2
\]
for an arbitrary sequence of transport currents. A measure can concentrate its density near grazing while retaining finite mass and moments. An entropy bound could give a weaker uniform-integrability estimate relative to a specified reference measure, but no such quantitative density hypothesis is stated in the theorem.

### B2.2 The rank atlas does not prove the exhaustive singular classification

Analytic stratification says that rank strata are semianalytic. It does not prove that every rank-deficient point is grazing, simultaneous in chronology, collinear, or in multiple contact. That classification is the geometry to be proved, not a consequence of invoking Weierstrass preparation. The proof's one-sentence variation argument is not adequate.

### B2.3 The surplus-contact gain is not obtained

On a regular rank-three chart, coarea enforces the contact constraint and the hard-sphere flux supplies the standard \(\varepsilon^2\) cross-section. The manuscript itself says this exactly matches the Boltzmann--Grad normalization. Nothing in the regular-chart argument then produces an additional factor \(\varepsilon^{\alpha_G}\). A small-minor sublevel estimate only controls the singular charts; it cannot create a small factor on the complementary regular charts.

This is the central recollision estimate. Without it, surplus graphs do not vanish and the tree recursion does not close.

### B2.4 The finite-time concatenation is invalid

The manuscript proposes to extend a short-slice cluster expansion to arbitrary fixed \(T\) by retaining at each interface only the empirical density and incoming contact trace. Those data do not determine the multi-particle correlations, labels, or collision genealogies entering the next slice. Kernel composition on that reduced boundary state is therefore not the microscopic hard-sphere composition law.

This point is especially important in light of the current literature. The long-time hard-sphere derivation of Deng--Hani--Ma succeeds by propagating a detailed cumulant ansatz that retains full collision-history information and by a substantial cutting algorithm. It does not follow from concatenating one-particle density data. The present two-paragraph slicing argument does not reproduce that machinery.

### B2.5 Pressure and LDP identification do not follow

Even a locally uniform logarithmic moment limit does not by itself yield a full good LDP with all lower bounds. The proof needs exponential tightness in the precise topology, exposed-point density or an equivalent control representation, and concentration under microscopic tilts. Solving a controlled limiting Boltzmann equation does not prove that the exact deterministic finite-volume tilt concentrates on that solution.

The known hard-sphere fluctuation and large-deviation theory is technically substantial even for short times. The present module neither reproduces those estimates nor proves its stronger contact-current and arbitrary-finite-time extensions.

---

## B3 — *Hamilton--Boltzmann Cotangent Geometry from Deterministic Hard-Sphere Collisions*

**Decision: reject.**

### B3.1 The form comparison is not uniform under the stated assumptions

The manuscript assumes \(f/M\) and \(q\) are bounded above and below only on compact velocity sets, then concludes global equivalence with a Maxwellian collision Dirichlet form in a weighted space. Compact-by-compact positivity does not provide one global coercivity constant.

### B3.2 The closed-range conclusion is overclaimed

An adjoint estimate can give closed range modulo a specified kernel. It does not by itself make both kernel and cokernel finite dimensional. A Fredholm conclusion requires a compactness or finite-dimensional macroscopic reduction theorem that is not supplied.

### B3.3 Deterministic interval cumulants do not imply stopping-time cumulants

The localized cumulant bound is stated for tests supported on a deterministic interval. The proof of Aldous tightness then claims the same estimate conditionally after an arbitrary stopping time because genealogies can be “ordered after the stopping sigma-field.” Hard-sphere dynamics has memory through the entire current configuration and correlations. There is no independent-increment or strong Markov cluster decomposition of the kind used in that sentence.

### B3.4 The second epi-derivative is false

Section 4.4 supplies an explicit counterexample. This invalidates the manuscript's main variational theorem and the claim that its inverse is the Gaussian covariance.

---

## B4 — *Microcanonical Excess-Pressure Semigroups and Kinetic Theta-Generators*

**Decision: reject.**

### B4.1 Compactness fails

Section 4.8 gives a zero-cost counterexample. A bounded second moment gives narrow tightness, but not compactness for a topology testing unbounded quadratic functions. Uniform integrability of the second moment, or a strictly higher moment bound, is required.

### B4.2 The transfer lemma confuses weak and strong metrics

The hypothesis is smallness in \(d_*\), a weak metric generated by countably many tests. The proof uses a weighted \(L^1\) stability estimate and then claims that approximation of tests converts it into
\[
\sup_t d_*(f_t,g_t)\le C d_*(f_0,g_0)
\]
and a Lipschitz action bound.

Weak closeness does not control weighted \(L^1\) distance. Smooth oscillatory positive densities can converge in \(d_*\) while remaining a fixed distance apart in \(L^1\). The Gronwall estimate used in the proof therefore cannot be initialized from the theorem's hypothesis.

### B4.3 Product collision measures do not follow from the stated convergence

Weak convergence of \(f_n\), even with velocity averaging, does not generally imply convergence of
\[
A_{f_n}\propto f_n f_{n,*}B.
\]
One needs strong convergence in a space controlling the quadratic product. The compactness proof assumes this decisive nonlinear passage.

### B4.4 The semigroup limit is not established

The corrector estimate is integrated over genealogies and does not give locally uniform generator convergence on every kinetic action sublevel. Moreover, maximal accretivity of an abstract graph is not by itself the viscosity comparison theorem for the half-relaxed-limit equation on this non-locally-compact weighted state space. The required test-function core, containment function, and comparison proof are absent.

---

## C1 — *Typed Control, Information, and Saddle Envelopes for Kinetic Cotangent Phases*

**Decision: reject.**

### C1.1 The regular dominated chart is impossible

Section 4.5 is decisive. The theorem conflates deterministic state evolution with a nondegenerate transition density. Neither A2/B1 aggregate local limit estimates nor B2/B4 limiting equations manufacture a one-step density for a deterministic hidden kernel.

The claimed lower density bound on every infinite observation stratum is also incompatible with normalization.

### C1.2 Aggregate Fourier estimates do not give conditional observation kernels

A local theorem for sums under a stationary or canonical law is not a uniform Sobolev density theorem for
\[
G_\vartheta^a(x',dy)
\]
conditional on every hidden state and action. C1 repeatedly upgrades global coefficient estimates into pointwise conditional likelihood regularity without a disintegration theorem.

### C1.3 The Feller proof mishandles small evidence

The estimate “mass at most \(\delta\nu(Y)\)” is useless when the dominating stratum has infinite measure. Tail moments do not repair this without a uniform integrable envelope for the evidence densities. More fundamentally, the posterior may vary arbitrarily near zero evidence; continuity of the integrated belief kernel requires a precise uniform-integrability argument not supplied.

### C1.4 Finite moments do not provide a continuous approximate inverse into an arbitrary compact set

A finite family of coordinates can separate points approximately on a compact metric space, but a partition-of-unity barycenter need not lie in a nonconvex reachable set \(\mathcal K\). There is no general theorem producing a continuous map
\[
R_m:T_m(\mathcal K)\to\mathcal K
\]
uniformly approximating the identity from finitely many arbitrary separating functions. This would impose finite-dimensional approximation/retraction properties not assumed.

### C1.5 Uniform LAN and BvM over policies are unsupported

Compactness of a policy class does not imply a uniform information lower bound. A policy may choose uninformative actions or suppress parameter-sensitive observations. The asserted
\[
cI\le I_\vartheta^\alpha
\]
requires a uniform identifiability/observability condition that is absent.

The score under an adaptive policy is not automatically a stationary additive functional to which A4 or B3 applies. Uniform laws of large numbers for conditional information, martingale Lindeberg bounds, tests against fixed-distance alternatives, and posterior concentration all require independent proofs. The text supplies only labels for them.

---

## C2 — *Path-Space Cotangent Rigidity, Universal Contractions, and Tangent Representations*

**Decision: reject.**

### C2.1 The weighted strict-dual proof does not match the stated topology

The proof of weighted integrability proposes tail-supported functions with amplitude comparable to \(W\). Such functions have
\[
q_R(f_n)\approx1
\]
on arbitrarily remote annuli and therefore do not satisfy the manuscript's own “uniform normalized tail vanishing” convergence condition. They cannot be used to contradict continuity. The identification with the Mackey topology is asserted without proving the equicontinuity/compactness characterization for this modified topology.

This is not the standard strict-topology theorem merely by analogy; the precise weighted topology matters.

### C2.2 The hard-sphere annihilator contradicts the displayed formal adjoint

The manuscript first computes
\[
\mathcal B^*r
 =(-\partial_t r-v\cdot\nabla_xr-\mathcal Lr,\Delta r).
\]
It then states that every annihilating source has the form
\[
(-\partial_t r-v\cdot\nabla_xr,\Delta r)+\zeta.
\]
The sentence that the collision component “absorbs” \(\mathcal Lr\) is not an algebraic identity. Unless the source pairing is redefined and the resulting term explicitly transferred through the derivative of \(A_f\), the theorem omits a nonzero adjoint term.

### C2.3 Pressure equality does not yield periodic data by differentiation alone

Differentiating a local pressure identity gives equilibrium expectations against source directions. It does not directly give “every periodic-orbit derivative.” Recovering periodic orbit sums requires a separate rigidity theorem and hypotheses on the transfer operator/Gibbs measures. The proof assumes its desired Livšic input.

### C2.4 Optional projections and brackets are not stable under the stated weak convergence

Weak convergence of \((X^\varepsilon,Y^\varepsilon,L^\varepsilon)\), even with uniform integrability, does not generally imply convergence of conditional expectations under changing filtrations. One needs an extended weak-convergence or prediction-process hypothesis formulated and verified precisely.

Even process convergence of martingales does not imply convergence of predictable quadratic variations or stochastic logarithms. Those require uniform tightness of semimartingale characteristics or an equivalent structure condition.

### C2.5 The stochastic-exponential theorem is false without strict positivity

A nonnegative uniformly integrable martingale can hit zero. A Doléans exponential of a finite continuous Brownian stochastic integral is strictly positive. Therefore
\[
M_t/M_0=\mathcal E\!\left(\int_0^tH_s\,dI_s\right)
\]
does not follow from positivity and uniform integrability alone. Equivalence of likelihoods, strict positivity, and logarithmic integrability are missing.

The claimed automatic convergence of bounded Girsanov transforms and Lipschitz BSDEs is correspondingly unsupported.

### C2.6 The examples do not satisfy the contraction hypotheses

The A3 clock map is not a continuous map on the stated state because the ordered path is missing. The C1 Bayes map is not globally continuous at zero evidence, particularly with an isolated cemetery point. Thus the theorem's advertised nonvacuous examples do not meet its own data-level definition.

---

## D1 — *Rigidity and Universal Contractions of Hard-Sphere Kinetic Cotangents*

**Decision: reject.**

### D1.1 An LDP does not give the claimed complete phase-weight asymptotics

An LDP yields
\[
\lim a_\varepsilon^{-1}\log
P(\Xi_\varepsilon\in U)
 =-\inf_U I
\]
under suitable regularity. It does not yield
\[
e^{-a_\varepsilon\alpha_j}
a_\varepsilon^{-\gamma_j}(c_j+o(1))
\]
for arbitrary neighborhoods of isolated minimizing compact sets.

Such an expansion requires a model-specific nondegenerate saddle/Morse--Bott analysis, control of boundaries, and a local theorem valid over the entire minimizing set. A2 and B1, even if correct, state central local results in compact interior saddle charts; they do not automatically cover every phase cell or its boundary complement.

### D1.2 Conditional component LDPs require regular conditioning events

For a fixed Borel phase cell, the conditional lower bound can fail at its boundary. The rate
\[
I_j=I-\inf_{U_j}I
\]
on the closure is not automatic unless the cell is an \(I\)-continuity set and the numerator/denominator asymptotics are proved. Positivity of every nonempty finite-\(\varepsilon\) event is also not a consequence of the limiting LDP.

### D1.3 The boundary phase argument is incomplete

The complement of disjoint neighborhoods need not be a compact set separated by a positive rate from all minima in the noncompact path/order-parameter setting. If it contains additional minimizing sequences or degenerate saddles, it need not have either the same polynomial expansion or a strictly larger exponential cost.

### D1.4 Downstream synthesis rests on failed inputs

The common observation domination comes from false C1. The continuous-time shared-control compactness comes from false B4. The component CLTs and local constants come from the invalid A/B chains. The zero-free analytic chart assumes exactly the asymptotic expansion that has not been proved.

The finite-mixture contraction lemma and the correctly centered abstract Gaussian-mixture statement are standard and conditionally reasonable. They do not salvage the paper because the existence and asymptotics of the components are the substantive claims.

---

## 6. Literature and novelty assessment

The manuscripts do not engage adequately with the literature against which their claims must be judged.

For orientation:

1. D. Dolgopyat and P. Nándori, *On mixing and the local central limit theorem for hyperbolic flows*, arXiv:1710.08568, formulate substantial abstract hypotheses for local central limit theorems and verify them for classes including finite-horizon Sinai billiard suspensions. A2 must state exactly which hypotheses it strengthens and provide the full operator/arithmetic verification.
2. T. Bodineau, I. Gallagher, L. Saint-Raymond, and S. Simonella, *Statistical dynamics of a hard sphere gas: fluctuating Boltzmann equation and large deviations*, arXiv:2008.10403, obtain fluctuation and large-deviation results through detailed cumulant-generating-function estimates, under regularity assumptions and a time restriction.
3. The same authors' *Cluster expansion for a dilute hard sphere gas dynamics*, arXiv:2205.04110, develops a genuine trajectory-cluster expansion and carefully retains dynamical cluster information.
4. Y. Deng, Z. Hani, and X. Ma, *Long time derivation of the Boltzmann equation from hard sphere dynamics*, arXiv:2408.07818, forthcoming in the *Annals of Mathematics*, extends the derivation to the lifespan of a regular Boltzmann solution by propagating a detailed collision-history cumulant ansatz and proving difficult diagrammatic cutting estimates.
5. R. Kraaij, *A Banach--Dieudonné theorem for the space of bounded continuous functions on a separable metric space with the strict topology*, arXiv:1602.01587, illustrates that strict-topology duality is a precise locally convex result, not a conclusion obtained from an informal convergence description.

The present revision neither cites nor reproduces the machinery needed to improve these results. In particular, B2's proposed arbitrary-time concatenation discards exactly the collision-history correlations that the recent long-time theory works hard to propagate.

A top-four-journal paper may certainly introduce a radically shorter method. But then the short argument must be complete at the point where it replaces the established machinery. Here the decisive steps are slogans, and several are false.

---

## 7. Minimum requirements for a scientifically meaningful resubmission

The current eleven-paper architecture should be abandoned for review purposes. A credible future submission would need to proceed in a much narrower order.

1. **Select one root theorem.** Either produce a complete A2 paper with a precise billiard model and a fully proved operator/Fourier theorem, or produce a complete B2 paper with a precise hard-sphere ensemble and recollision analysis. Do not submit downstream synthesis papers before the root theorem exists.
2. **Remove every theorem contradicted above.** In particular, correct the B1 normalization, recompute the B3 Hessian, replace A4's transmission-zero construction, and reformulate C1 without impossible common domination.
3. **State all spaces and maps before use.** Every kernel, trace, current, graph domain, topology, source class, and conditioning window must have a complete definition. Every compactness or differentiability theorem must use those exact definitions.
4. **Prove absolute continuity in entropy recoveries.** Representative atoms cannot approximate continuous kernels at finite KL cost.
5. **Retain sufficient ordered/correlation state.** Path concatenation requires order; long-time hard-sphere evolution requires correlation or collision-history data.
6. **Separate theorem levels.** Finite-dimensional Laplace asymptotics, process LDPs, functional CLTs, LAN, BvM, nonlinear semigroup convergence, and memory decay are different theorems with different hypotheses. They cannot be obtained from one generic “analytic pressure” sentence.
7. **Add a real literature section and theorem-by-theorem comparison.** Every use of a standard theorem must cite an exact result and verify its hypotheses.
8. **Provide complete proofs, not proof summaries.** The present modules read like proposed proof strategies. They are not publishable proofs.
9. **Use the repository checks only for reproducibility.** Add mathematical regression checks for the explicit algebraic counterexamples above, but do not call passing scripts a closure certificate.
10. **Obtain independent specialist review of each root area.** The billiard, hard-sphere, large-deviation, operator-memory, filtering, and asymptotic-statistics claims require different expertise.

These are reconstruction requirements, not a finite list of revisions to the present text.

---

## 8. Final verdict

The Round-Twenty-One revision is more organized than its predecessor and does place new mathematical prose in the active source files. That is a repository-level improvement.

It is not a mathematical closure.

The suite contains multiple explicit false statements, invalid changes of variables, impossible domination assumptions, incorrect entropy recoveries, incorrect asymptotic algebra, and unproved promotions from finite-dimensional estimates to process-level theorems. Because the dependency graph exports the failed root claims into every later manuscript, none of the eleven papers is ready for publication.

**Recommendation to the editor: reject all eleven manuscripts. Do not invite a major revision of this dossier. Any future submission should be a substantially reconstructed, self-contained root paper with corrected statements and complete proofs.**
