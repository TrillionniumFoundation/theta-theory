# External Referee Report on the Round-Twenty-Three Revision

## Recommendation: **Reject all eleven manuscripts — do not invite a major revision of this dossier**

**Repository:** `TrillionniumFoundation/theta-theory`  
**Reviewed branch:** `revision/round23-referee-positive-closure-11paper-2026-09-02`  
**Pre-review head:** `50de9a642e9e2b1bfcfc1f7828336deead5b5b1d`  
**Review date:** 2 September 2026  
**Scope:** all eleven active `main.tex` wrappers and `ROUND23_POSITIVE_CLOSURE.tex` modules, the Round-Twenty-Two response, the proof-dependency ledger, the mathematical regressions, the second-pass self-audit, and the third-pass technical audit.

This report applies the correctness, self-containedness, novelty, and presentation threshold expected at *Annals of Mathematics*, *Inventiones Mathematicae*, *Journal of the American Mathematical Society*, or *Acta Mathematica*. It is intentionally severe. The dossier simultaneously claims new theorems in billiard dynamics, local limit theory, path-space large deviations, deterministic hard-sphere limits, nonlinear kinetic semigroups, filtering, asymptotic statistics, operator memory, and phase coexistence. Results of that breadth can be accepted only when every root theorem is stated on a precise space and proved at the level needed by every downstream import.

The Round-Twenty-Three revision does correct several elementary contradictions identified in the preceding report. In particular, the active prose no longer uses the old unnormalised canonical pressure, the old collision Hessian, the old regular-point residue, or the old atomic entropy recovery. Those corrections are real. They are not, however, a proof of the advertised replacement theorems.

My conclusion is that the active manuscripts remain mathematically invalid. Several statements are directly false as written; several displayed operator products are not even well typed; and the root analytic estimates on which the dependency graph rests are replaced by short proof sketches that omit precisely the difficult steps. A further threshold problem is that the latest audit documents describe substantial source repairs that are not present in the active mathematical files at the reviewed head.

---

## 1. Confidential recommendation to the editor

I recommend **rejection without a major-revision invitation**.

The decisive reasons are not matters of exposition or missing routine estimates. Among the failures that can be checked internally from the submitted text are the following.

1. **The latest-head audit does not match the active sources.** The head commit adds only `ROUND23_THIRD_PASS_TECHNICAL_AUDIT.md`. It does not make the A2, B1, B4, or other mathematical changes that the audit says are now active. The second-pass audit has the same problem for several claimed replacements.
2. **A4's synchronized minorization is impossible on the complete-past state.** After finitely many append/shift steps, the untouched remote initial tail remains an exact state coordinate. Transition laws from different initial tails are supported on disjoint tail cylinders and cannot all dominate one nonzero probability measure.
3. **A4's alleged weighted Lipschitz norm does not impose local continuity.** Its denominator is `(1+d)(V+V')`, not `d(V+V')`; every function bounded by a multiple of `V` automatically has finite “Lipschitz” seminorm.
4. **A4's renewal formula is not composable with its declared domains and codomains.** The product `E(z)(I-T(z))^{-1}X(z)` is ill typed, and the displayed definition of `E(z)` contains an unbound mark variable.
5. **B3's closed-range argument fails on an explicit infinite-dimensional kernel.** For every nonzero collision defect `h` with `C h=0`, the pair `(u,h)=(0,h)` has zero image under the displayed balance operator. The claimed null-space description and coercivity inference are therefore false.
6. **C1's hidden/observation model is internally incompatible.** If the hidden state is complete enough for the next state to be the deterministic Dirac `delta_{Phi(x)}`, then the noiseless billiard or hard-sphere aggregate conditioned on that same complete state is also deterministic, not an `L^1` observation density. If unresolved coordinates are retained to obtain a density, the hidden transition is the nontrivial A3 kernel, not a Dirac map.
7. **D1's leading-order control formula cannot retain the shared-policy constraint.** For finitely many scalar component values, `sup_alpha max_j G_j(alpha) = max_j sup_alpha G_j(alpha)`. The repository's own second-pass audit recognizes this, but the active D1 source still presents only the leading formula and claims that it preserves shared control.
8. **B4's action does not control the asserted superquadratic moment under the written hypotheses.** The entropy Young inequality used in the proof produces an exponential `p`-moment term, whereas the state assumes only a polynomial `p=2+delta` moment.
9. **B2's loop-opening theorem has no rank theorem behind its Łojasiewicz estimate.** An analytic determinant ideal may vanish identically on a component. The text never proves nonvanishing or independence of the purported loop constraints.
10. **A2's scalar integration-by-parts calculation does not prove the advertised anisotropic transfer-operator norm estimate.** The passage from a two-dimensional scalar integral to a uniform `B -> B_w` bound, including orbit segments with too few UNI blocks, is absent.

Any one of items 2–7 is enough to block the corresponding paper. Because A2–A4 and B1–B4 are upstream of C1, C2, and D1, the failures propagate through the entire dossier.

---

## 2. Source identity and the latest-head audit failure

The review index correctly designates the eleven `ROUND23_POSITIVE_CLOSURE.tex` files as the active proof sources. The wrappers inspected in this review import those files directly. I therefore judged the mathematical claims in those files, not claims in status documents, workflows, generated manifests, or unexecuted patch payloads.

This distinction matters here.

### 2.1 The third-pass head contains an audit, not the advertised source repairs

The reviewed head is `50de9a642e9e2b1bfcfc1f7828336deead5b5b1d`, with commit message

> `Record third-pass Fourier, conditioning, rate, and topology repairs`.

The comparison with its parent shows only one added file:

> `ROUND23_THIRD_PASS_TECHNICAL_AUDIT.md`.

No active manuscript source was changed by that commit.

The audit says, among other things, that:

- A2 now fixes a high differentiability order `r_*`, uses four frequency regimes, and proves an ultra-high-frequency `|b|^{-M}` estimate;
- B1 now has a fixed high-order full-frequency damping argument and an exact continuous coarea interface;
- B4 now obtains superquadratic containment for the original action from a B2 exponential collision-source estimate and a Povzner mechanism.

The active sources do not contain those replacements. At the reviewed head:

- A2 still assumes a `C^5` family, gives the three-line estimate (A2.7), and uses only `(1+|b|)^{-2}` in the unbounded Fourier direction;
- B1 still gives (B1.8) with an uncontrolled constant `C_N` and no active exact-fibre coarea theorem;
- B4 still attempts to propagate the `p`th moment by a one-line entropy inequality under a merely polynomial moment assumption.

Thus the latest audit is a plan or provenance note, not a description of the active theorem source.

### 2.2 The second-pass audit also claims replacements absent from the active files

The second-pass audit states that the active sources now contain, among other things:

- an exact quantitative Diophantine certificate in A2;
- a projective recession state and explicit time reparametrization in A3;
- a two-rate cost and a sectorial coupling domain in A4;
- a near-Maxwellian hypocoercive graph theorem in B3;
- a positive strong-core recovery compiler in B4;
- a finite probability observation envelope in C1;
- complete exposing rays in C2;
- and subleading shared-policy asymptotics in D1.

Those objects are not the objects in the active files reviewed below. For example, active C1 still uses the sigma-finite geometric reference (C1.2), active C2 still extrapolates from a local pressure ball, and active D1 ends at the scalar leading-order formula (D1.15).

This is not a cosmetic repository issue. A referee must be able to identify the theorem under review. An audit cannot repair a proof unless the repair is actually present in the source imported by `main.tex`.

### 2.3 Regression scripts are not theorem verification

The regression file usefully prevents a few old algebraic mistakes from being silently reintroduced. It does not check:

- whether an analytic determinant is nonzero on every graph component;
- whether a family of transfer operators has the stated high-frequency norm;
- whether a controlled action propagates a moment;
- whether a filter model is consistently typed;
- whether a random-stop local theorem follows from a fixed-iterate local theorem;
- whether a graph operator has closed range;
- or whether an infinite-dimensional LDP is exponentially tight.

Passing source-token checks, compiling TeX, and reproducing elementary finite-dimensional identities cannot be called proof closure.

---

## 3. Direct contradictions and counterexamples

This section records several blockers that do not depend on specialist literature. They follow directly from the submitted definitions.

### 3.1 A4: no common finite-step minorization on a complete-past shift

A3 defines a history as

`h=(...,m_{-2},m_{-1})`

and A4 uses the append-and-shift update. After `n` updates, the newly sampled marks occupy the most recent `n` coordinates, while the older initial history is merely shifted farther into the past. It is not erased.

For a fixed initial history `h`, let `A_h^n` be the set of histories whose coordinates beyond the newest `n` entries agree with the shifted tail of `h`. Then

`P^n(h,A_h^n)=1`.

Choose `h` and `h'` with different remote tails. Then `A_h^n` and `A_{h'}^n` are disjoint. If (A4.6) were true,

`P^{n_L}(h,.) >= epsilon_L nu_L(.)`

and the same inequality held for `h'`, the probability `nu_L` would have to be supported on both disjoint tail cylinders. Hence `nu_L=0`, contradicting that it is a probability.

A weak-Harris contraction in a metric that discounts the remote tail may be possible. A Doeblin minorization on the full exact-past state is not.

This invalidates Lemma `lem:r23-a4-small`, the claimed operator gap (A4.7), the subsequent pressure construction, and the assertion that the orthogonal dynamics inherits exponential stability.

### 3.2 A4: the displayed norm is not a Lipschitz norm

A4 defines

`sup_{h != h'} |f(h)-f(h')| / ((1+d_sigma(h,h'))(V(h)+V(h')))`.

If `|f(h)| <= C V(h)`, then

`|f(h)-f(h')| <= C(V(h)+V(h'))`,

so the displayed quotient is at most `C` independently of how discontinuous `f` is. The factor `1+d_sigma` never tends to zero. Consequently the norm does not encode local continuity, cannot support the stated local-contraction estimate, and does not justify a Feller or spectral-gap argument.

The source-analyticity claim is also unsupported. A small element of this space may grow like `epsilon V`; multiplication by `e^g` then grows like `e^{epsilon V}`, while the space and drift control only the linear weight `V`.

### 3.3 A4: the renewal formula is ill typed

The source declares

- `E(z): X -> Y`,
- `X(z): Y -> X`,
- `T(z): Y -> Y`.

With the ordinary right-to-left convention, the expression

`E(z)(I-T(z))^{-1}X(z)`

cannot be composed: the rightmost `X(z)` outputs an element of `X`, but `(I-T(z))^{-1}` accepts an element of `Y`. In addition, the definition

`E(z)f(h)=int_0^{tau(m)} ... ds`

contains a free mark `m` that is neither part of the stated input nor integrated out. The history `h_x` used in `X(z)` is also not a uniquely defined function of a section point `x`.

Thus (A4.9) is not an operator identity on the declared spaces.

### 3.4 B3: the displayed balance operator has a much larger kernel

B3 defines

`B(u,h)=(partial_t u+v.grad_x u-DQ_f[u]-C h, u(0))`.

The collision-to-density map `C` maps an infinite-dimensional collision-defect space to a one-particle residual space and has a large kernel. For example, collision-involution cycles give nonzero signed defects `h` with `C h=0`; smooth `L^2(A_f^{-1})` versions can be obtained by regularization on a region where `A_f` is positive.

For every such `h`,

`B(0,h)=(0,0)`.

Therefore the kernel is not “exactly the solutions of the homogeneous linearized Boltzmann equation with allowed initial tangent,” as the theorem claims. Moreover, estimate (B3.10) places `int h^2/A_f` on its right-hand side. It does not bound the graph-domain norm by the norm of the image and hence cannot prove closed range or a bounded right inverse.

The right inverse is then used to manufacture the exact nonlinear balance correction in (B3.16), so the Mosco upper bound also loses its construction.

### 3.5 B3: conditioning on the full microscopic state does not restart an ensemble cumulant expansion

The future hard-sphere trajectory conditional on the complete phase point at a stopping time is deterministic. Its conditional law is a Dirac mass. B3 nevertheless says that after conditioning on that full state one may reapply B2's prepared-ensemble connected expansion and obtain the uniform conditional estimate (B3.12).

A deterministic restart property is not a stochastic regeneration property. Rare stopped states need not satisfy the original ensemble cumulant bounds with a uniform constant. No conditional density or uniform absolute-continuity theorem is supplied. Thus (B3.12), the Aldous estimate, and the process CLT are not established.

### 3.6 C1: deterministic hidden transitions and smooth conditional observations cannot both describe the stated noiseless mechanics

C1 takes `X` to be the prepared A3 or B2 history state and declares

`M_theta^a(x,dx')=delta_{Phi_theta^a(x)}(dx')`.

For the A3 state this already contradicts A3, where the next legal excursion is sampled from the nontrivial kernel `K(h,dm)`.

There are only two ways to interpret the discrepancy:

1. `x` contains the complete microscopic state. Then both the next state and every noiseless mechanical observation are deterministic functions of `x`; the observation kernel is a Dirac mass, not the `L^1(nu)` density asserted in (C1.3).
2. `x` omits unresolved coordinates so that the next observation has a density. Then the unresolved coordinates also randomize the next hidden state, so the transition is a kernel, not a Dirac push-forward.

No independent measurement noise is introduced that could reconcile the two. Proposition `prop:r23-c1-observation` therefore cannot hold for the model as typed.

### 3.7 D1: the leading scalar asymptotic forgets the shared-policy constraint

For arbitrary scalar functions `G_j(alpha)` and finitely many phases,

`sup_alpha max_j G_j(alpha) = max_j sup_alpha G_j(alpha)`.

Hence the right-hand side of (D1.15) is algebraically identical to phasewise pre-optimization at leading exponential order. It cannot encode the information constraint that one policy is shared across unobserved phases.

The repository's second-pass audit explicitly notices this fact and says that the sharing constraint survives only in finite-scale log-sum-exp and subleading corrections. The active D1 source contains no such subleading theorem and still says that (D1.15) proves the desired distinction.

There is a second gap: taking the finite-`N` supremum over policies before the limit requires a uniform Laplace principle or an equicoercive control compactness theorem. Componentwise limits for each fixed policy do not justify

`lim_N sup_alpha = sup_alpha lim_N`.

Policies may depend on `N`.

### 3.8 B4: finite entropy action does not imply the claimed `p`-moment bound

The proof applies the entropy Young inequality with a test comparable to `|v|^p`, `p=2+delta`. Its dual term is of the form

`int A_f (exp(c|v|^p)-1)`,

which is not controlled by a polynomial `p`-moment.

The failure is not merely formal. On a Maxwellian high-velocity region with `v_*` bounded, the reference collision measure has radial order `e^{-c r^2} r^3 dr`. Choose a multiplier of order

`q(r)=e^{c r^2} r^{-a}`

with `6<a<=6+delta`, localized smoothly to large `r`. Then

- the entropy action behaves like `int r^{5-a}dr` and is finite;
- the `p`-weighted controlled collision flux behaves like `int r^{p+3-a}dr` and diverges.

Thus finite action under the written assumptions does not control the moment needed for the asserted `W_2` compactness. A genuine Povzner or exponential-source estimate would have to be stated and proved in the active source.

### 3.9 B2: the grazing constant is not uniform under the stated class

For a fixed relative velocity `g=v-v_*` with `|g|=r` and `eta<r`, angular integration gives

`int_{0<g.omega<eta} [g.omega]_+ d omega = pi eta^2/r`.

Therefore the coefficient in an `O(eta^2)` estimate depends on `1/|v-v_*|`. A bounded `(2+delta)` moment and an `L^p(A_f)` bound on `q` do not control concentration near `v=v_*`. Taking `f` concentrated in a velocity ball of radius `epsilon_v` makes the constant grow like `epsilon_v^{-1}`.

Accordingly (B2.8) is not uniform on the class stated in B2. A global two-sided Maxwellian or density regularity assumption would be needed before the claimed grazing-removal argument.

---

## 4. Paper-by-paper report

## A1 — exact benchmark, response, and Hilbert FCLT

The revision makes a useful conceptual correction by separating a geometric current fibre from a measurable Hilbert-valued observable and by putting an explicit cylinder-tail requirement into the response domain. This resolves the specific false inference that arbitrary Hilbert membership gives exponential approximation.

It does not yet prove the advertised theorem.

### Major objections

1. **Parameter differentiation occurs in mutually singular probability fibres.** Distinct two-sided Bernoulli product measures with different symbol weights are generally mutually singular. The definition says that material derivatives exist in `L^2(mu_a;J^m)` but does not define a common parameter fibre, a difference quotient, or a transport between these `L^2` spaces.
2. **The conditional expectation depends on the parameter.** `Pi_N^a J_a` integrates the infinite tail with the `a`-dependent product law. It is not merely a finite-coordinate function whose expectation can be differentiated by the central finite product density. The derivative of the tail conditional expectation must be included and estimated. The proof does not do so.
3. **The material derivative changes the current index.** The text maps `J^m` to `J^{m+2}` but requires repeated derivatives to remain in `J^m` in the response norm. The common graph domain and embeddings needed for this iteration are not defined.
4. **Closure of the infinite subdivision relation is asserted.** The closedness of `R^m` is a substantive compatibility statement for an infinite weighted incidence system and is not proved.
5. **The functional martingale remainder is not established.** Summability of `sum_j ||P_0Y_j||` is followed by a “standard telescoping construction” and then by a maximal `o(sqrt n)` claim. The exact Hilbert-valued invariance-principle theorem and all its hypotheses should be stated. The scalar `L^2` approximation at a terminal time is not automatically a uniform-in-time approximation.
6. **No principal geometric current is shown to lie in the new domain.** The response theorem is an abstract result for observables already assumed to have exponential conditional-expectation tails. The paper does not prove that the seam/flag current whose response motivates the construction satisfies that assumption.

### Disposition

**Reject in present form.** A substantially narrower abstract response theorem might be salvageable after the varying-measure derivative and maximal approximation are treated rigorously, but the present text does not establish the advertised current response package.

---

## A2 — Sinai periodic arithmetic and raw local limit theorem

The replacement of a real-determinant argument by a periodic-character formulation is directionally correct. The main theorem, however, still rests on unproved and in places implausible operator estimates.

### Major objections

1. **The certified billiard family is not constructed.** The sentence about four scatterers, unfolded loops, and a corridor-length ratio `sqrt(2)` does not prove that the exact roof differences have the required irrational ratio after solving the reflection equations. Irrationality is not an open condition in a nonconstant parameter family. The active source does not contain the quantitative Diophantine certificate claimed by the second-pass audit.
2. **Estimate (A2.1) is not a consequence of the cited growth lemma.** Uniform `C^j` summability of all inverse branches, parameter derivatives, and roof derivatives through the stated orders across homogeneity cuts requires a detailed anisotropic branch calculation. “Choose the homogeneity exponent above the largest derivative polynomial” is not a proof and does not address branch proliferation and singular derivatives simultaneously.
3. **The UNI calculation is scalar, not an operator estimate.** Formula (A2.6) estimates a two-dimensional Lebesgue integral. The anisotropic weak norm is defined through stable-curve pairings, and the transfer operator is a sum over inverse branches. The text supplies no pairing, branch matching, or partition argument that converts (A2.6) into the norm estimate (A2.7).
4. **The phases used in (A2.6) are branch differences.** The twisted operator contains the phase of each branch, not directly the scalar phase `Psi_1+Psi_2`. Exploiting a temporal-distance difference requires an explicit cancellation or Dolgopyat cone argument. None is given.
5. **Bad orbit segments cannot acquire future oscillatory factors.** A length-`n` word that has not encountered two good UNI blocks is part of `L^n`. One cannot “delay the integration until the next two good blocks” without replacing the operator by a longer iterate. A frequency-independent bad-family remainder over an infinite Fourier line is precisely the difficulty the proof needs to solve.
6. **The all-frequency estimate is far stronger than what is shown.** The uniform factor `(1+|b|)^{-2}e^{-cn/N_0}` for every large `b` and every `n` is not derived. The third-pass audit itself says that a higher fixed derivative budget and a four-region argument are necessary; those are absent from the active source.
7. **Aperiodicity to covariance and peripheral spectrum needs regular Livšic input.** The text moves from periodic data to absence of unit-circle spectrum and to positive covariance in one sentence. The needed eigenfunction regularity/coboundary theorem on the actual countable induced system is not stated.

### Disposition

**Reject.** The raw LLT (A2.8), and therefore every A3/C1/D1 conditioning result that imports it, is not proved.

---

## A3 — ordered path LDP and entropy recovery

The conditional-reference recovery (A3.6) is a genuine improvement: it avoids the infinite-KL atomic approximation from the previous revision. The state-space and large-deviation theorem remain undefined at the level needed for publication.

### Major objections

1. **The mark topology is inappropriate for moving collision times.** Uniform convergence of time-rescaled billiard trajectories is generally unstable when reflection times vary. A Skorokhod or graph topology with explicit endpoint matching is needed.
2. **The ordered point-measure limit does not determine a path.** Each atom in (A3.2) has mass `1/N`. Typical weak limits are diffuse Young measures, not finite atomic words. The instruction “order the atoms and concatenate” therefore does not define a map on the proposed limiting state space.
3. **The path coordinate is not tight.** Over a collision horizon of order `N`, the rescaled microscopic trajectory has order `N` velocity jumps of order one. No Aldous, modulus, or compact-containment estimate in the stated Skorokhod space is supplied.
4. **The recession compactification is undefined.** The equivalence class `[m]`, its compact topology, the role of the arbitrary threshold `K_N`, and compatibility between different thresholds are not defined. The projective replacement promised by the second-pass audit is absent.
5. **The rate map is not well defined.** A measure `Q(ds,dh,dm)` with a weak balance relation does not by itself determine one chronological sample-path law. The map `Z(Q)` and the clock normalization are asserted rather than constructed.
6. **The random-stop interface is missing.** A2 proves a local theorem for a deterministic iterate number `n`. A3 conditions the randomly stopped sum at `nu_N`. No renewal theorem or joint local theorem for `(nu_N,S_{nu_N}X,S_{nu_N}tau)` is proved.
7. **The path-source insertion is outside A2.** A2 permits fixed bounded strong-space insertions. It does not prove the local Fourier expansion after inserting `exp(-NF_M)` for a path functional. Repeating an entire tilted operator theorem is not a one-line corollary.
8. **Exact continuous conditioning is not defined.** An event fixing the roof coordinate exactly has probability zero. A regular conditional density/coarea formulation is required.
9. **Connector entropy is not controlled.** A3.1 is an upper moment estimate; it does not give a uniform positive lower probability for connector cells. The assertion that all recurrent/recession connectors have `o(N)` entropy is unsupported.

### Disposition

**Reject.** The paper now contains a plausible research programme for an ordered controlled excursion LDP, not a proof of such an LDP.

---

## A4 — history spectral theory, renewal, and memory

This paper contains the strongest direct contradictions in the dossier.

### Major objections

1. Lemma `lem:r23-a4-small` is false on the exact complete-past state, as shown in Section 3.1.
2. The norm (A4.5) does not impose Lipschitz continuity, as shown in Section 3.2.
3. The analytic Feynman–Kac map is not bounded on the stated linear-weight space.
4. The renewal identity is ill typed, as shown in Section 3.3.
5. The stability of `e^{tQLQ}` does not follow from mixing of the full Markov semigroup. Compression by a non-invariant finite-rank projection can create very different orthogonal dynamics; `e^{tQLQ}` is not `Qe^{tL}Q`.
6. The resolvent expansion in (A4.14) is formal for an unbounded generator. An operator-norm expansion through `L_Q` requires range/domain assumptions on `QLP`, `PLQ`, and powers of `L_Q`. The active source does not contain the sectorial coupling theorem claimed by the audit.
7. The explicit Lyapunov function `V` is not shown to be the `W` furnished by A3, and recent singularity proximity is not included in the active A3 cost.

### Disposition

**Reject.** The exact block algebra (A4.11)–(A4.15) would be standard under suitable invariant-domain and semigroup hypotheses, but those hypotheses are neither proved nor compatible with the preceding false minorization argument.

---

## B2 — hard-sphere collision histories, pressure, and dynamic LDP

This is the principal hard-sphere root paper. The active source is far below the proof threshold required for its claims.

### Major objections

1. **The retained hierarchy is not defined.** The spaces of rooted histories, label partitions, open half-edges, signed measures, and the product `star` are named but not constructed. Associativity, measurability, positivity, and norm continuity are not proved.
2. **The grazing estimate is not uniform.** Section 3.9 gives an explicit concentration counterexample to (B2.8) under the stated moment class.
3. **Łojasiewicz does not prove rank.** Before using (B2.11), the authors must prove that the determinant ideal is not identically zero on every relevant analytic component. No such theorem appears.
4. **Cyclomatic number is not geometric rank.** `s(G)` counts graph cycles; it does not show that the corresponding loop-closure equations have independent transverse directions after all earlier contact constraints. Degenerate and repeated loops are not excluded by graph counting.
5. **The per-loop gains do not automatically multiply.** Recomputing a determinant ideal after each reduction is an instruction, not a proof that all conditional ideals have a common nonzero minor and controlled density.
6. **The key finite-time estimate is simply postulated.** Inequality (B2.17) is essentially the hard correlation-propagation theorem. No Duhamel map, combinatorial cutting rule, or proof of its factorial norm bound is provided.
7. **The connected coefficient counting is schematic.** Collision vertices, particle roots, labels, time orderings, and automorphisms are conflated in (B2.15)–(B2.16). Cayley's tree count alone is not the trajectory-cluster expansion.
8. **Positive balance correction is unproved.** An arbitrary invariant-orthogonal balance defect is not automatically in the range of the nonlinear collision operator with a positive bounded multiplier.
9. **Pressure differentiability does not imply tilted concentration at every controlled path.** Exposed-point uniqueness, a law of large numbers under the tilted deterministic ensemble, and exponential tightness must be proved.
10. **The LDP topology is inconsistent.** The theorem names laws of `(f^epsilon,Gamma^epsilon)` but also requires compactness of an unlisted history coordinate. An atomic empirical density also cannot converge strongly in local `L^1` without a smoothing or correlation-density definition.

### Literature threshold

The existing hard-sphere fluctuation and large-deviation programme of Bodineau, Gallagher, Saint-Raymond, and Simonella obtains its results through detailed cumulant-generating-function estimates and explicit time restrictions. Their trajectory-cluster work retains nontrivial dynamical cluster structure. The recent long-time derivation by Deng, Hani, and Ma propagates a collision-history cumulant ansatz through an elaborate diagrammatic cutting argument. A radically shorter proof is possible in principle, but (B2.17) cannot replace that machinery by assertion.

### Disposition

**Reject.** Because B2-GC is not proved, B1, B2-MC, B3, B4, C1, C2, and D1 lose their hard-sphere root input.

---

## B1 — canonical normalization and mixed coefficient theorem

The explicit normalization error from the prior revision is corrected, and the Gaussian Schur formulas (B1.10)–(B1.12) are algebraically correct. The analytic coefficient theorem is not established.

### Major objections

1. **Removing affine identities does not make every block map a submersion.** Zero velocities, critical points of spatial cell functions, and other rank-deficient configurations remain after quotienting.
2. **A fixed finite atlas cannot uniformly resolve all hard-core boundaries created by the exterior configuration.** The current block sees exclusion surfaces centred at all previously exposed particles. Their number and geometry depend on `N` and on the conditioning.
3. **The boundary-flat argument does not supply a uniform lower minor.** A partition of unity can localize a regular set; it cannot make a vanishing Jacobian nonzero.
4. **A deterministic positive fraction of blocks need not be usable.** Legal configurations satisfying energy and packing constraints can place every labelled block outside the selected full-rank charts. What is needed is an exponentially small exceptional-set theorem under the conditional canonical law, not the deterministic sentence in the source.
5. **Global covariance does not imply conditional block covariance.** Successive conditioning can make a particular block nearly deterministic.
6. **The Fourier majorant contains an uncontrolled `C_N`.** Without a growth bound, `C_N(1+|v|)^{-s theta N}` gives no uniform integrable estimate and cannot justify the local inversion.
7. **The proof is circular at the canonical level.** The small-frequency canonical pressure and covariance are invoked before the exact-`N` coefficient extraction that is supposed to derive them from the grand-canonical pressure.
8. **Global contour deformation is not justified.** Local analyticity and a local saddle do not exclude other activity saddles, zeros, or comparable coefficient contributions.
9. **The numerator and denominator generally have different source-dependent saddles.** Calling the contour “common” does not prove the ratio formula.

### Disposition

**Reject.** The exact-number interface imported by B2-MC, B3, C1, and D1 is unavailable.

---

## B3 — fluctuation process and second epi-derivative

The local collision Hessian has been corrected: the normal defect `h=delta Gamma-D A_f[u]` is the right variable at a zero-cost path. That algebraic repair does not prove the graph theorem or process CLT.

### Major objections

1. The weighted spaces in (B3.7) are internally inconsistent (`M_+^{-1/2}` in the prose and `M_+` in the displayed norm), and collision invariants need not lie in the stated space.
2. Two different comparison Maxwellians do not automatically give uniform equivalence of all form and Hilbert norms at infinity.
3. A Fourier-in-`x` Kawashima argument does not directly handle a spatially varying non-equilibrium coefficient `f(t,x,v)`. Partitioning only time does not control spatial commutators.
4. The closed-range theorem fails on the collision-kernel directions described in Section 3.4.
5. The stopping-time cumulant estimate fails for the reason in Section 3.5.
6. The exact nonlinear-balance chart depends on the unavailable right inverse.
7. The Mosco lower bound assumes uniform integrability of the rescaled entropy defects without proving it, and the covariance/inverse-form identification imports the unproved process CLT.

### Disposition

**Reject.** The correct scalar second variation is a useful correction, but the functional theorem is not established.

---

## B4 — nonlinear kinetic semigroup and microscopic limit

The use of a superquadratic static shell is appropriate for excluding the previous escaping-energy example. The dynamic action and microscopic convergence arguments remain invalid.

### Major objections

1. Finite action does not propagate the `p`th moment under the active assumptions; Section 3.8 gives an explicit tail obstruction.
2. Negative-Sobolev equicontinuity plus pointwise `W_2` compactness does not by itself give compactness in `C([0,T];W_2)`. A temporal modulus for the second moment is needed.
3. The synchronous `W_2` estimate for an unbounded hard-sphere collision rate and a state-dependent multiplier is asserted without a coupling construction. Truncating `q` under finite entropy does not automatically preserve a uniform stability modulus.
4. “Entropy topology relative to `A_{f_n}`” is not defined for varying reference measures in Proposition `prop:r23-b4-product`.
5. The comparison proof is a paragraph, not a viscosity proof on Wasserstein space. The collision exponential, containment derivatives, and doubled transport terms are not calculated.
6. The microscopic objects are ill typed. `H_epsilon` and `V_t^epsilon` act on finite-particle configurations or laws, yet (B4.13)–(B4.14) evaluate them directly at arbitrary continuum densities `f` and take a supremum over the whole shell. No realization map or convergent sequence of microscopic laws is specified.
7. B2 provides, at most, a regular prepared class. It cannot yield uniform convergence over every density in the entropy/moment shell.
8. The finite BBGKY corrector is only named. Its exact specular-domain construction and uniform generator estimate are not proved.

### Disposition

**Reject.** Neither the Nisio state space nor the nonlinear Trotter–Kato limit is closed by the active argument.

---

## C1 — filtering, adaptive LAN, and Bernstein–von Mises

The revision correctly abandons common domination of deterministic hidden Dirac kernels. It replaces that error by an inconsistent hidden/observation model.

### Major objections

1. The deterministic-transition/dominated-observation contradiction is given in Section 3.6.
2. A2/B1 aggregate local theorems do not provide a pointwise conditional observation density for every exact entrance history. A point-history insertion need not be a bounded element of the anisotropic strong space.
3. The active source uses a sigma-finite geometric observation reference, while the second-pass audit says a finite probability envelope was required. That finite envelope is not in the active proof.
4. `L^1` continuity and the integrated ratio estimate prove an integrated Feller property under suitable compactness. They do not give three recursive derivatives of the log evidence when the evidence may approach or equal zero.
5. QMD of the one-step channel does not by itself give uniform QMD of the recursively parameter-dependent filter.
6. The reconstruction (C1.12) lands in the convex hull of net beliefs, not necessarily in the forward-reachable regular set on which the model estimates were verified. The finite-coordinate dynamic program may therefore leave its domain after one step.
7. The policy class is defined partly by the desired information conclusion (C1.15). A theorem uniform over such a class still needs a topology, compactness, and a common limiting information map.
8. Fixed-radius LAN and fixed-distance KL tests do not alone prove posterior contraction on every growing local annulus needed for total-variation BvM.

### Disposition

**Reject.** The Feller ratio identity is potentially useful, but the model-derived observation proposition and the statistical theorems are not proved.

---

## C2 — strict duality, rigidity, and optional projections

The pullback calculation for the weighted strict dual is the strongest isolated argument in the revision. It does not rescue the rest of the paper.

### Major objections

1. **The annihilator operator is missing the initial-output component.** B3 defines its graph operator with `u(0)` as a second output. C2 drops that component in (C2.5). The adjoint and annihilator must therefore contain the associated boundary source; (C2.6)–(C2.7) are incomplete.
2. **The argument imports B3's false closed-range theorem.** Even a corrected formal adjoint would not yield (C2.7) without a valid graph theorem.
3. **Local pressure analyticity cannot be continued along arbitrary unbounded potential rays.** Eigenvalue isolation may fail, and the A4 source only treats a small source ball. The exposing-ray repair promised by the second-pass audit is absent.
4. **The localizing potential is not Hölder.** `1_{Sigma\K_m}` is an indicator with a jump at the boundary of `K_m`. It is not in the stated Hölder class.
5. **Equilibrium tightness and uniqueness on a countable-history shift are not proved.** The finite-state approximation sentence does not control escape of mass or pressure.
6. **The prediction process is insufficient for arbitrary path functionals.** `Pi_t^n=Law(X_t^n|Y_{<=t})` determines conditional expectations of functions of `X_t^n`, not of an arbitrary complete-path functional `F(X^n)`. Formula (C2.11) is false without augmenting the hidden state by the relevant path.
7. **The optional-projection hypotheses largely assume the desired convergence.** Prediction-process convergence and predictable-bracket convergence are listed as assumptions and then said to be “verified” by upstream papers that contain no such process theorem.
8. **C1 and C2 are inconsistent about equivalence.** C1 explicitly permits zero evidence. C2 claims that the same regular experiment verifies strict positivity plus reciprocal moments. Localization away from zero changes the experiment and does not prove the global claim.
9. **Reciprocal polynomial moments do not automatically imply Novikov's exponential condition.** The step from (C2.12) to a global Girsanov theorem needs a separate argument.

### Disposition

**Reject.** The strict-topology lemma could be separated into a short functional-analytic note; the rigidity and stochastic-convergence package is not established.

---

## D1 — phase weights, shared control, and coexistence

The paper now correctly acknowledges that an LDP alone does not determine a polynomial phase prefactor. It nevertheless assumes a local theorem much stronger than anything proved upstream and mishandles the control limit.

### Major objections

1. **The input (D1.1) is not an upstream theorem.** A2 and B1 prove, at most, finite-dimensional central local limits for selected additive coordinates. They do not prove a joint density in an arbitrary path variable `Z_N` with a smooth rate `J_j(m,z)`, positive `C^2` amplitude, and two derivative error bounds.
2. **The Morse–Bott integration is incomplete.** The probability of the phase event integrates over `z`, but (D1.2) freezes `z=z_j` and (D1.7) contains only the normal Hessian in `m`. Unless `z` is conditioned, its saddle dimensions and determinant contribute additional powers and constants.
3. **The conditional rate notation is undefined.** The function `I(z,j)` in (D1.9) has not been constructed as a joint labelled rate.
4. **The limit/supremum exchange over policies is unproved.** A component Laplace principle for each fixed policy does not allow the finite-`N` optimizer to vary without a uniform control theorem.
5. **The leading max-plus formula cannot retain shared control.** Section 3.7 gives the exact algebraic identity. The subleading theorem promised by the audit is absent.
6. **The phase posterior is initialized inconsistently.** The Bellman state allows arbitrary weights `w_j`, while (D1.15) inserts the microscopic costs `-gamma_j` as though those weights always came from the asymptotic phase probabilities.
7. **The complex expansion (D1.16) is not proved upstream.** Local real LLTs do not automatically give a zero-free uniform analytic expansion of every phase-restricted partition function.
8. **All component inputs are unavailable.** The A2/A3/A4 and B1/B2/B3/B4 chains fail before D1 is reached.

### Disposition

**Reject.** The phase-weight calculation is a conditional formal Laplace exercise, not a synthesis theorem for the submitted mechanical models.

---

## 5. Dependency-level consequence

The repository's directed order is useful because it makes the propagation transparent.

### Billiard chain

- A2 does not establish its branchwise high-frequency transfer estimate or raw LLT.
- A3 therefore lacks its local denominator and, independently, lacks a well-defined compact ordered path state.
- A4 imports the failed history platform and also contains direct false minorization, norm, and typing statements.

Consequently the Sinai observation, pressure, memory, and phase interfaces exported to C1, C2, and D1 are unavailable.

### Hard-sphere chain

- B2 does not establish loop smallness, finite-time history propagation, pressure, or the GC LDP.
- B1 therefore has no valid GC input and independently fails to prove its block Fourier theorem.
- B2-MC has no denominator theorem.
- B3 has no valid closed-range or stopping-time CLT theorem.
- B4 has no valid compact action state or microscopic semigroup convergence.

Consequently the hard-sphere observation, tangent, control, and phase interfaces exported to C1, C2, and D1 are unavailable.

### Synthesis chain

- C1 is internally mistyped and lacks model-derived observation kernels.
- C2 imports failed B3/A4/C1 results and contains independent adjoint and optional-projection errors.
- D1 assumes local and control theorems not supplied by any upstream paper.

The dependency ledger is acyclic as a graph. It is not a proof ledger because the nodes do not prove their declared contracts.

---

## 6. Significance, novelty, and relation to the literature

If even a substantial subset of these results were proved, the work would be significant. That makes the current level of compression more problematic, not less.

A top-four-journal proof may be conceptually short, but it must replace established machinery at the exact point where the machinery is normally used. In this dossier:

- the Sinai local theorem replaces anisotropic/Dolgopyat analysis by one scalar integration-by-parts paragraph;
- the ordered path LDP replaces construction of a controlled Polish state and exponential tightness by a few assertions about ordering atoms;
- the hard-sphere root theorem replaces trajectory-cluster combinatorics and correlation propagation by undefined history objects and (B2.17);
- the kinetic process CLT replaces conditional cumulant and martingale-problem analysis by an invalid deterministic restart;
- the filtering paper replaces model-specific conditional kernels by an inconsistent deterministic/smooth-density pair;
- and the semigroup limit replaces microscopic realization and comparison arguments by formal half-relaxed-limit prose.

The relevant existing work demonstrates the scale of the missing steps. Examples include:

- Szász and Varjú on local limit theory for the Lorentz process;
- Baladi, Demers, and Liverani on spectral/mixing theory for finite-horizon Sinai billiard flows;
- Dolgopyat and Nándori on mixing and local central limit theorems for hyperbolic flows;
- Bodineau, Gallagher, Saint-Raymond, and Simonella on hard-sphere fluctuation/large-deviation generating functions and trajectory-cluster expansions;
- Deng, Hani, and Ma on long-time hard-sphere-to-Boltzmann derivation through collision-history cumulants and diagrammatic cutting;
- and Kraaij on the strict topology of bounded continuous functions.

The active manuscripts cite some of these subjects, but they do not state theorem-by-theorem what is imported, what hypotheses are verified, and exactly what new lemma closes the remaining gap.

---

## 7. Minimum requirements for a scientifically meaningful resubmission

The present eleven-paper dossier should not be revised by another layer of audit documents. A credible resubmission would require a different process.

1. **Freeze one source of truth.** Every claimed repair must be committed to the exact active file imported by `main.tex`. Status documents must be generated from source, not used as substitutes for it.
2. **Submit one root paper first.** Choose either A2 or B2. Do not submit downstream memory, filtering, BvM, contraction, or phase papers until the root theorem has survived specialist review.
3. **For A2, prove an actual operator theorem.** Define the anisotropic spaces, the parameter transport, the UNI cancellation mechanism, every frequency regime, and an integrable tail with all insertion derivatives. Supply a real periodic-orbit certificate for a concrete billiard family.
4. **For A3, construct the limiting state before stating the LDP.** The ordered/projective excursion object, path topology, random stopping, recession compatibility, and controlled rate map must be complete measurable objects. Prove tightness of the actual path coordinate.
5. **For A4, change the state or the mixing claim.** A complete-past state cannot satisfy finite-step Doeblin minorization. Use an appropriate Wasserstein weak-Harris theorem, correct the norm, and type every renewal map. Prove the orthogonal semigroup hypothesis separately.
6. **For B2, define and prove the collision-history hierarchy.** Establish graphwise rank/nonvanishing, cutting, factorial bounds, exact composition, and finite-time propagation. Do not treat (B2.17) as a lemma without proof.
7. **For B1, separate regular charts from exceptional configurations.** Prove an exponentially small exceptional-set theorem and uniform conditional Fourier damping. Remove the uncontrolled `C_N`.
8. **For B3, quotient the full kernel and prove a genuine graph estimate.** State the exact domain, codomain, boundary outputs, null space, and image norm. Develop a legitimate stopped conditional estimate rather than a deterministic restart slogan.
9. **For B4, prove action coercivity under the original rate.** A superquadratic containment estimate needs a real Povzner/exponential-source argument. Define the microscopic realization map before any uniform semigroup statement.
10. **For C1, choose a consistent partially observed model.** Either the hidden state transition is stochastic, or the observation includes independent noise. Derive the conditional kernel for that model and impose fixed support/positivity where log-likelihood derivatives are used.
11. **For C2, include all boundary adjoint terms and use path-valued prediction when needed.** Do not infer optional projections of whole-path functionals from a current-state filter.
12. **For D1, retain finite-scale shared control or prove subleading asymptotics.** A scalar max-plus limit cannot encode the shared-policy constraint. State a uniform control Laplace theorem before interchanging optimization and limits.
13. **Add theorem-level literature comparisons.** Every use of “standard,” “growth lemma,” “Kawashima,” “Dolgopyat,” “Mitoma,” “Trotter–Kato,” or “Bernstein–von Mises” must identify an exact theorem and verify its assumptions on the actual space.
14. **Obtain independent specialist reports.** No single referee can responsibly certify all areas claimed here. The root billiard and hard-sphere papers require separate experts before any synthesis paper is reviewed.

These are reconstruction requirements, not a finite major-revision checklist.

---

## 8. Final verdict

Round Twenty Three is more responsive than Round Twenty One. It removes several explicit formulas that were demonstrably wrong and introduces some potentially useful ideas, notably conditional-reference entropy quantisation, the collision-defect Hessian coordinate, and a weighted strict-topology pullback.

Nevertheless, the active dossier is not mathematically closed. It contains:

- a false finite-step minorization on an exact complete-past state;
- a non-Lipschitz “Lipschitz” norm;
- an ill-typed renewal product;
- an incorrect graph-kernel/closed-range inference;
- an invalid stopped-ensemble restart;
- an incompatible deterministic-transition/smooth-observation model;
- an action compactness proof that requires an unassumed exponential moment;
- unproved root Fourier and loop-opening estimates;
- an algebraically phase-blind leading control limit;
- and audit documents whose advertised repairs are not present in the active sources.

The dependency structure exports these failures to every later manuscript. Compilation, hashes, theorem labels, and regression tokens do not alter that conclusion.

**Recommendation to the editor: reject all eleven manuscripts. Do not invite a major revision of this dossier. Any future submission should be a substantially reconstructed, self-contained root paper whose active source, claimed audit status, and complete proof are identical.**
