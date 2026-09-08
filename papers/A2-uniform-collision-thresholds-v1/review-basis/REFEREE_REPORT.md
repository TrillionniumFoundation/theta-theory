# Independent referee report: Two-collision counting response in a periodic Lorentz gas

## Recommendation: reject as a top-four-journal research article; retain the scoped mechanical result

**Review date:** September 8, 2026.  
**Reviewer:** GPT-6 Astra Pro. This is an independent AI-assisted assessment at the repository owner's request, not a report commissioned by or a decision of any journal.

**Author:** Qian Qi.  
**Source branch:** `work/2026-09-08-publication-dynamics-a2-b2`.  
**Frozen source commit:** `e8d3b658ead4996dabfc9f31a07b812e070f5446`.  
**Source:** `workstreams/2026-09-08-next-step/research/A2_Two_Collision_Response.tex`.  
**Source Git blob:** `df44402b17031525c087d39dfedf8dac3ada611d` (20,663 bytes).  
**New review branch:** `review/a2-two-collision-harsh-independent-2026-09-08`.

## 1. Editorial assessment

This is the newest A2-labelled mathematical work located in the accessible branch inventory. It is not on an A2-named revision branch. The repository index describes it as a finite-time technical note and explicitly separates it from the original long-time A2 programme. I therefore assess both its printed theorem and, separately, whether it supplies an article of the significance requested by the user.

The note makes a genuine improvement over a one-event calculation: two collisions have positive probability under the full equilibrium preparation, the expected count is not confused with the probability of at least one event, and the second derivative includes the moving-level term. The short-flight geometry is actually proved rather than replaced by a symbolic clock. I do not identify a fatal counterexample to the principal theorem within its stated radius interval, time window, and observable class.

Nevertheless, the result is not a sufficiently substantial top-four-journal research contribution as presented. In the chosen window, the exact count law reduces to a single positive-part integral of one free-flight roof. Its parameter regularity follows from uniform transversality and an ordinary regular-level argument on a finite collection of smooth branches. No estimate of multi-collision correlations, iterated singularity growth, long-time response, or a raw local-limit remainder is obtained. The elementary finite-experiment statistical corollary does not change this assessment.

The recommendation is **rejection at the requested level**, not an assertion that the scoped theorem is false. The note should be preserved as a useful mechanical lemma or technical component. A future submission requires a new structural advance of substantially greater scope or significance, not merely further differentiation of this fixed-window integral.

## 2. The scope actually proved

The family has unit particle speed, triangular lattice covolume $A_\Lambda=\sqrt3/2$, disk radius $R\in[0.45,0.47]$, and physical window $T=0.11$. The preparation is normalized full phase volume, not a hand-selected transverse initial ensemble. The minimum inter-obstacle gap is $d_*=0.06$, so $T<2d_*$ excludes three collisions while still allowing two.

On the outgoing section,

$$d\nu=\frac{\cos\phi}{4\pi}\,d\alpha\,d\phi,
\qquad \overline\tau_R=\frac{A_R}{2R},
\qquad \lambda_R=\frac{2R}{A_R},\quad A_R=\frac{\sqrt3}{2}-\pi R^2.$$

The active result is

$$p_2=\lambda_RJ,\qquad p_1=\lambda_RT-2\lambda_RJ,
\qquad p_0=1-\lambda_RT+\lambda_RJ,
\qquad J=\int(T-\tau_R)_+\,d\nu.$$

The three probabilities are positive; $p_2'>0$; and every fixed finite radius derivative exists and is bounded on the compact interval. The note does not assert bounds uniform in derivative order, arbitrary time windows, the number of collisions, a full marked two-impact path, or arbitrary smooth scatterer deformations. These exclusions should survive any later incorporation into a larger manuscript.

## 3. Theorem-level correctness audit

### 3.1 Stationary counting and normalization

The flux normalization is consistent. Total boundary flux is $4\pi R$ and total unit-speed phase volume is $2\pi A_R$, giving the displayed mean roof. Reflection preserves the section flux. The normalized suspension is therefore $d\nu\,ds/\overline\tau_R$.

For an invertible invariant section map and any positive roof, the interval of suspension positions producing at least $k$ future hits has the length used in `prop:tails`. Invariance gives

$$\Pr(N_t\ge k)=\frac{1}{\overline\tau}
\int\left[(t-S_{k-1}\tau)_+-(t-S_k\tau)_+\right]d\nu.$$

There is no renewal or independent-roof assumption here. The lower roof bound makes the tail sum finite for fixed $t$, so telescoping gives $\mathbb E N_t=t/\overline\tau$. The distinction $\Pr(N_T\ge1)=\lambda_RT-p_2\ne\lambda_RT$ is essential and correctly retained.

The independent diagnostic compares this formula against direct interval lengths in 333 finite rational cases, including correlated periodic roofs. These tests support the calculation but do not replace its exact proof.

### 3.2 Short flights and the terminal level

`lem:transverse` uses two effective geometric facts. A flight of length at most $T$ can reach only a nearest lattice centre because $2R+T\le1.05<\sqrt3$. At both endpoints,

$$c_0,c_1\ge\frac{1-2R-T^2}{2RT}\ge\frac{479}{1034}>0.46.$$

The constant is arithmetically correct. An earlier distinct obstacle before the candidate hit would require at least two inter-obstacle gaps, exceeding the window. A return to the initial convex disk along the same outgoing ray is impossible. Thus the active root is an actual first hit, not merely an unobstructed-looking algebraic root.

`lem:regularlevel` also has a sound critical-point argument. In angular coordinates $(\alpha,\vartheta)$, simultaneous vanishing of both section derivatives forces a head-on nearest-neighbour flight, whose length is $1-2R\le0.10<T$. Consequently the terminal level is regular and compactly separated from grazing. This is the mechanism giving smoothness; it should not be confused with a theorem controlling all billiard singularities.

For completeness, the terminal level is nonempty: at $\alpha=0$, take

$$\cos\vartheta=\frac{1-2R+T^2}{2T(1-R)}.$$

In the stated interval this gives a regular incoming root with time $T$. Together with the strict negativity of the radius derivative, it also shows that the level contribution to $J''$ is genuinely positive. Making this witness explicit would improve the exposition; its omission is not a fatal gap.

### 3.3 Radius derivatives and coarea

The implicit derivative

$$\partial_R\tau=\frac{1-n_1\cdot n_0}{n_1\cdot v}<0$$

is correct at fixed angular section coordinates. The numerator cannot vanish because the outgoing and incoming normal signs are opposite. A regular-level chart makes the positive-part integral smooth in $R$, and the preparation normalizer remains present through $\lambda_R$.

The manuscript's first and second derivative formulas are consistent with distributional differentiation. In particular,

$$J''=-\int_{\tau<T}\partial_R^2\tau\,d\nu
+\int\delta(T-\tau)(\partial_R\tau)^2\,d\nu.$$

The Bell-polynomial expression has the correct alternating signs: at order three its boundary terms are $3\tau'\tau''\delta(T-\tau)-(\tau')^3\delta'(T-\tau)$. The claim is finite-order smoothness on regular charts, not an unproved product of singular distributions at grazing.

The root recursion and the recursion obtained by differentiating $A_R\lambda_R=2R$ are likewise consistent. The positivity square, the lower bound for $p_1$, and the coarse area bound for $p_0$ have the required signs. The numerical lower bound $10^{-9}$ is very weak but valid; weakness of a lower bound is not a correctness objection.

### 3.4 Statistical corollary

`cor:source` is a finite-support exponential-family consequence. Positivity of all three probabilities gives positive source variance and a mean range $(0,2)$. The binary information formula follows from a smooth Bernoulli probability with $p_2'>0$. This is correct as a statement about this one-window experiment. It is not a long-time inference theorem, an efficiency comparison, or a new general statistical principle.

## 4. Independent geometric reduction and numerical evidence

I used a different coordinate system from the author's sector-grid diagnostic. Fix one nearest centre $e=(1,0)$, let $\vartheta$ be the direction angle, and let $c$ be the transverse line offset centred between the two disks. Write

$$s=\sin\vartheta,\quad C=\cos\vartheta,\quad a=s/2,
\quad h_\pm=\sqrt{R^2-(c\pm a)^2}.$$

The flight length and section measure are

$$\tau=C-h_--h_+,\qquad d\nu=\frac{d\vartheta\,dc}{4\pi R}.$$

The active domain has $|\vartheta|<\vartheta_*$ and $|c|<c_*(\vartheta)$, where

$$\cos\vartheta_* =\frac{1+T^2-4R^2}{2T},\qquad
U=1-2T\cos\vartheta+T^2,$$

$$c_*(\vartheta)=\frac{\cos\vartheta-T}{2}
\sqrt{\frac{4R^2-U}{U}}.$$

These expressions follow by solving $h_-+h_+=C-T$, not by assuming a statistical model for the roof. Define

$$F_R(x)=\frac12\left(x\sqrt{R^2-x^2}+R^2\arcsin(x/R)\right).$$

Integrating in $c$ analytically and using the sixfold symmetry gives

$$J(R)=\frac{3}{\pi R}\int_0^{\vartheta_*}
\left[-2c_*(C-T)+2F_R(c_*+a)-2F_R(-c_*+a)\right]d\vartheta.$$

The review script uses this one-dimensional integral. It also computes the section-coordinate bulk second derivative and the coarea contribution independently. At fixed angular section coordinates, putting $B=e\cdot v^\perp$ and $h=\sqrt{R^2-b^2}$ gives the useful exact identity

$$\partial_R^2\tau=\frac{B^2}{h^3}\ge0.$$

Consequently the bulk term in $J''$ is nonpositive. Any positive second response must account for the level term; it cannot be obtained by differentiating only on a frozen active domain.

The following numbers are floating quadrature, not interval-certified bounds:

| Radius | $p_0$ | $p_1$ | $p_2$ | $p_2'$ |
|---|---:|---:|---:|---:|
| 0.450 | 0.5710567933 | 0.4271761475 | 0.0017670593 | 0.7317574879 |
| 0.460 | 0.5156753538 | 0.4658281236 | 0.0184965227 | 2.7657806361 |
| 0.470 | 0.4602310874 | 0.4785413101 | 0.0612276026 | 6.0635377474 |

At $R=0.46$,

$$J''_{\rm bulk}\simeq-0.4777401032,\qquad
J''_{\rm level}\simeq36.1124921803,$$

$$J''\simeq35.6347520771.$$

Finite differences of the independently computed $J'$ agree with the bulk-plus-level value within the recorded numerical tolerance. The note already includes this term. It would therefore be wrong to repeat an objection that it omitted the moving boundary.

The coordinate reduction is supplied as a reproducible check and a potentially useful simplification, not as a requirement that every exact probability admit an elementary closed form.

## 5. A precise limit of what two-event counting can determine

The assertion “two collisions occur” does not imply that the statistic probes correlations between successive complete roofs. Under $T<2d_*$, the entire three-point count law is determined by the one-roof marginal and its mean. No composition of the collision map occurs in $J$.

Here is an exact scope test. Let the section map be a cyclic permutation of four equiprobable states. Compare roofs

$$\tau^{(a)}=(1,1,2,2),\qquad
\tau^{(b)}=(1,2,1,2).$$

They have the same section marginal and mean $3/2$. Under their stationary suspension preparations, at $t=3/2$ both count laws are

$$\Pr(N_t=0,1,2)=(1/6,\,2/3,\,1/6).$$

At $t=5/2$, however,

$$\Pr_a(N_t\ge3)=1/12,\qquad \Pr_b(N_t\ge3)=0.$$

Indeed, the two-roof sums in the first system are $(2,3,4,3)$, whereas in the second they are identically three. The stationary tail identity computes both answers exactly.

These are abstract suspensions, **not two asserted realizations as the manuscript's Lorentz gas**. They do not refute the printed theorem. They demonstrate the logical insufficiency of the two-event count law for recovering the multi-roof dependence needed in longer-window or long-time claims. A later A2 paper cannot close that gap by calling the current calculation a “two-collision response” without specifying which record is observed.

## 6. Collision thresholds are a real additional problem

The chosen interval is safely away from the first two-event onset. Let $R$ be fixed, put $g=1-2R$, and vary the physical window through $T=g$. In the line coordinates above, the head-on flight has the local expansion

$$\tau=g+\frac{c^2}{R}+\frac{g\,\vartheta^2}{4R}
+O((c^2+\vartheta^2)^2).$$

There are six equivalent minima. For $\varepsilon=T-g>0$ sufficiently small, integration of this nondegenerate quadratic minimum gives

$$J_R(g+\varepsilon)
=\frac{3}{2\sqrt g}\,\varepsilon^2+O(\varepsilon^3),$$

whereas $J_R(T)=0$ for $T\le g$. To see the coefficient, set $Q=c^2/R+g\vartheta^2/(4R)$. The plane integral of $(\varepsilon-Q)_+$ is $\pi R\varepsilon^2/\sqrt g$; multiply by $6/(4\pi R)$. The smooth Taylor remainder contributes at the next order after the $\sqrt\varepsilon$ rescaling.

Thus $J_R(T)$ is not $C^2$ across this onset. Equivalently, with $T=0.11$ fixed, the first radius threshold is $R_c=0.445$, outside the claimed interval, and the leading radius dependence is proportional to $(R-R_c)_+^2$.

This calculation is **not an in-scope counterexample**. It explains why the regular-level condition is mathematically doing work and why a future global parameter/time theorem needs a stratified threshold analysis or an explicitly restricted topology. Increasing the number of formal derivatives in the present safe window does not solve that problem.

The script checks the coefficient numerically at $R=0.46$: $J/\varepsilon^2$ approaches $3/(2\sqrt{0.08})\simeq5.3033008589$. At $\varepsilon=3\cdot10^{-5}$ the computed ratio is approximately $5.3022964397$. This convergence is corroboration of the local derivation, not a rigorous error enclosure.

## 7. Principal publication objections

**TC-R1 — The principal result is an incremental regular-domain calculation.** The stationary identity is general and elementary; the active geometric set is compactly transverse; and the parameter argument is a regular-level differentiation argument. The submitted combination is useful, but the note has not demonstrated a new mechanism or conclusion commensurate with the requested journal level.

**TC-R2 — No multi-history or long-time control is obtained.** A full marked two-impact law must retain event locations, directions, correlations, sampling-time cuts, and preparation terms. Longer windows introduce $S_j\tau_R$ and parameter derivatives of the collision-map iterates. The manuscript proves no bounds that are uniform or summable in that complexity. This is an absent result, not a hidden assumption in the correctly scoped count theorem.

**TC-R3 — The connection to the original A2 root theorem is not established.** The current note supplies neither a periodic-data realization nor a source-differentiated high-frequency transfer estimate or central integrable Edgeworth remainder. The Round 33 arithmetic/Fourier chapter remains conditional. A1 v36 concerns a different statistical programme and cannot supply missing specular-billiard estimates by name alone.

**TC-R4 — The originality argument is insufficient.** The manuscript acknowledges that the Palm/suspension identity is elementary and that its statistical corollary is not a new principle. It must therefore explain, by a precise comparison, why the residual geometric response result is a substantial advance over regular finite-itinerary calculus. No such case is established in the submitted note. I am not claiming an exhaustive literature proof that the exact numerical interval and every displayed identity have previously appeared.

These are not repaired by weakening the theorem, deleting the geometric proof, or presenting more numerical checks. They require additional mathematics or a different publication claim.

## 8. Literature and presentation

Marklof, *Entry and return times for semi-flows*, arXiv:1605.02715, is an appropriate primary reference for the stationary point-process/Palm setting, including non-ergodic systems. The exact counting identity in this note is independently proved and should not be advertised as a new general stationary-process theorem. [Primary source](https://arxiv.org/abs/1605.02715).

Demers and Zhang, *A functional analytic approach to perturbations of the Lorentz gas*, arXiv:1210.1261, treats perturbations including scatterer movements and deformations and continuity of spectral data. The manuscript should compare the regularity order, observables, and singularity treatment carefully rather than cite that work as an automatic all-order long-time extension. [Primary source](https://arxiv.org/abs/1210.1261).

Demers, Melbourne and Nicol, arXiv:1901.00131, proves martingale approximation and limit laws for Hölder observables of a Lorentz-gas time-one map. It is relevant background for the separate long-time programme, not an established raw mixed Edgeworth theorem for the sources proposed in A2. [Primary source](https://arxiv.org/abs/1901.00131).

The current paper's relatively restrained title and explicit exclusions are appropriate. Preserve them. Complete the bibliographic details, state the nonempty terminal-level witness, and keep “every fixed finite order” separate from order-uniform or analytic claims. These are useful improvements but are not the basis for a top-four acceptance decision.

## 9. What would merit a new review

A future submission should present a substantial theorem that reaches beyond this safely transverse one-roof functional. A viable route would be a genuine source-dependent, multi-impact response result with explicit singularity and summability control, followed by a clearly stated mechanical consequence. Another route could be a general structural classification of response and threshold singularities for a nontrivial family of mechanical experiments. These are examples of the kind of mathematical advance needed, not claims that those programmes are already complete or requirements to solve all eleven planned papers at once.

For the existing A2 long-time target, the key deliverable remains the actual model-level operator and remainder estimates, not another finite Bernoulli or Gaussian benchmark. The next source index should distinguish the present technical note, the conditional Round 33 chapter, and any newly proved root theorem.

## 10. Reproducibility and boundaries of this assessment

The full note was read in pinned TeX form, including the all-order formula, positivity proof, finite statistical corollary, and scope paragraph. The relevant A2 portion of the author diagnostic script and the workstream index were also inspected. The independent `diagnostics.py` imports no repository code and uses no network access.

All 31 named diagnostics passed in normal and optimized Python; the resulting JSON files were byte-identical. Exact algebra and rational suspension examples are labelled separately from non-interval floating quadrature. Five radii were checked for first and second responses; the second-derivative test includes, rather than suppresses, the coarea level term.

I did not replay the complete author suite, rebuild or inspect manuscript PDFs, run remote CI, simulate the full billiard flow, prove formal correctness, or conduct an exhaustive priority search. Passing these finite diagnostics does not certify all radii or all derivative orders; the source proofs, not the test count, are the basis for the scoped mathematical assessment.

Only new review files are added on a new branch. No manuscript, old report, source branch, repository permission, or protection setting is changed.

**Final disposition:** no fatal error was established in the printed fixed-window count theorem by this review. The manuscript nevertheless does not establish a research contribution of the requested top-four significance or complete the original A2 programme. **Reject at that level; retain the mechanical calculation with its scope intact.**
