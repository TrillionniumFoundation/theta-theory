# Independent referee report: A1, English research edition 2.0

**Manuscript:** *A1: Realizable Mechanical Experiments, Path Selection, and Response — Instruments, resource-aware predictive states, and whole-preparation finite-time collision calculus*  
**Author named in the manuscript:** Qian Qi  
**Review date:** 5 September 2026  
**Requested benchmark:** Annals of Mathematics / Inventiones Mathematicae / Journal of the American Mathematical Society / Acta Mathematica  
**Recommendation:** **REJECT in its present form at the requested general-mathematics-journal level.**

This is an independent, AI-assisted referee-style assessment requested by the repository owner. It is not a report commissioned by, or an editorial decision of, any of the journals named above. “Reject” is my assessment of this submission, not a claim that the research direction is impossible or that a stronger theorem cannot be proved.

## 1. Exact object reviewed and a publication discrepancy

The revision branch inspected was `revision/a1-english-v2-referee-2026-09-05`. Its observed head was

```
c9455e8236ccc58137833402be8cd77bd25e62af
```

with repository tree `d74611f576397531678e1c18196a8d572653aa3a`. That commit contains the publication workflow `.github/workflows/a1-english-review-publication.yml`. The workflow identifies the mathematical submission by the frozen Git tree

```
900059b847980a27be4866d495b00eeb96562dc5
```

**The expected published path `papers/A1-english-v2/main.tex` was not present at the observed revision head.** The corresponding Actions run, [33967239325](https://github.com/TrillionniumFoundation/theta-theory/actions/runs/33967239325), reported `completed / failure`. Its jobs response returned one failed job with no step details. I therefore do not attribute the failure to LaTeX, a mathematical test, permissions, or a particular package: the retrieved evidence does not establish the cause.

The frozen tree itself was accessible. I read the complete mathematical text from its Git blobs: `main.tex`, `references.tex`, all twenty numbered sections, and all four appendices. I also inspected the proof ledger, review priorities, README, finite-test source, and build/verifier source. This review concerns **that frozen English-v2 source**, not an unseen PDF and not an earlier Chinese manuscript. The source tree contains 35 blobs. The accompanying `source/` directory on this review branch references that very tree, unchanged; it is not a referee rewrite of the paper.

The author's ledger identifies 63 proof-bearing statements and reports a 53-page compilation. Statement labels and source-line starts are used here; PDF pagination is author-reported and was not independently verified in this review. I did not rerun the author's test suite or compile/render the manuscript. I did execute a separate twelve-check referee suite, whose exact script and execution receipt accompany this report.

This publication discrepancy is a reproducibility/delivery issue, not evidence that the underlying mathematics is false. A source-object upload, a successful source build, and a successful branch publication are three different facts. The current repository entrance should not describe the third as completed merely because the first occurred.

## 2. Editorial assessment

The paper is more careful than a generic “mechanics implies nonlinear statistics” manifesto. Several distinctions are now stated correctly: preparation versus dynamics; observation versus selection; mathematical tilting versus an attainable protocol; information price versus mechanical work; finite-horizon bridges versus consistent infinite histories; nominal prediction versus parameter-family prediction; and weak distributional response versus likelihood differentiation.

Nevertheless, the manuscript does not establish a sufficiently substantial central mathematical advance for the requested journals. Most of its results are direct applications, recombinations, or elementary refinements of established machinery. Its most concrete geometric result is an exact first-collision change of variables in a time window deliberately shorter than the minimum intercollision flight. That result is useful and, under the printed density and smooth-test conditions, appears sound. But the paper does not demonstrate why this result, together with a long sequence of standard identities, constitutes a major advance in mathematics.

My negative recommendation is **not** based on inventing an error in the collision-tube Jacobian. Nor is it based on demanding that a paper explicitly restricted to one collision must already prove an arbitrary-time billiard theorem. It is based on the contribution actually proved: the difficult long-time, multi-collision, realizability, and reduction inputs are mostly left as future interfaces, while the submission's breadth and theorem count substantially exceed the depth of its verified new core.

There are also three local statement-scope defects, discussed below with counterexamples and precise repairs. Two involve hypotheses that may have been intended implicitly. They should not be advertised as three independent refutations of the flagship theorem. Even after all three are repaired, the editorial significance problem remains.

### Decision summary

| Question | Assessment |
|---|---|
| Is there a readable, substantial mathematical manuscript? | Yes: the full frozen English source was inspected. |
| Is the single-collision whole-preparation assembly obviously wrong? | No. I find its change-of-variables mechanism convincing in the stated regime. |
| Are all printed scopes unambiguous and justified? | No. See M1–M3. |
| Does strong negative-Sobolev response make the complete record a regular statistical experiment? | No; the explicit separation result S1 below shows otherwise. |
| Is a genuinely new compatibility theorem demonstrated for one nontrivial controlled mechanical model? | Not at the depth suggested by the proposed contribution. |
| Is rejection merely a matter of presentation or failed CI? | No. The principal objection is research significance, independent of CI. |
| Is a proof-assistant or exhaustive originality certification being claimed by this review? | No. |

## 3. The core collision calculation: what survives scrutiny

**Source anchors:** [Section 15](source/sections/15_lorentz_local.tex), [Section 16](source/sections/16_lorentz_global.tex); `prop:lorentz-geometry`, `lem:tube-jacobian`, `thm:global-tube`, `thm:global-response`, `cor:global-hit`.

### 3.1 Coverage, injectivity, and normalization

Let the triangular fundamental cell have area

\[
A_\Lambda=\sqrt3/2,\qquad A_R=A_\Lambda-\pi R^2.
\]

For `0.45 <= R <= 0.47`, distinct lifted disks are separated by at least `0.06`. An outgoing straight ray from a convex disk cannot re-enter that same lifted disk before meeting another one. Consequently, for `0<T<0.06`, there is at most one regular collision in the observation window.

At an impact with boundary normal `n_alpha`, tangential vector `t_alpha`, incidence angle `phi`, and time `s`, the proposed coordinates are

\[
v^-=-\cos\phi\,n_\alpha+\sin\phi\,t_\alpha,
\quad v^+=\cos\phi\,n_\alpha+\sin\phi\,t_\alpha,
\quad q_0=Rn_\alpha-sv^-.
\]

Holding the laboratory velocity angle fixed, the two position derivatives are `R t_alpha` and `-v^-`. Their determinant has magnitude `R cos(phi)`. The transformation from incidence angle to laboratory velocity angle has absolute determinant one. Thus the full Jacobian is exactly

\[
R\cos\phi.
\]

The backward segment of length `s<T` and forward reflected segment of length `T-s<T` cannot reach another disk. Every regular colliding initial state determines one impact and hence one such triple, modulo the periodic/angular identifications. This supplies the essential coverage and nonoverlap argument; a collection of sampled trajectories alone would not supply it.

The subtract-and-replace identity is then legitimate: begin with every free comparison record from the allowed initial domain, remove the free record on colliding initial states, and insert its reflected record. Positivity belongs to the assembled physical measure, not to each signed term. For the constant test, the correction cancels. For the collision indicator, only the inserted collision contribution remains.

At equilibrium the collision mass is `4*pi*R*T`, the preparation normalizer is `2*pi*A_R`, and therefore

\[
p_R=\frac{2RT}{A_R}.
\]

I independently checked the stated first two derivatives and the general recursion obtained from `A_R p_R=2TR`:

\[
p_R'=\frac{2T(A_\Lambda+\pi R^2)}{A_R^2},\qquad
p_R''=\frac{4\pi RT(3A_\Lambda+\pi R^2)}{A_R^3},
\]

\[
p_R^{(j)}=\frac{2j\pi R p_R^{(j-1)}+j(j-1)\pi p_R^{(j-2)}}{A_R},\quad j\ge2.
\]

The collision-section law and the equilibrium law are different preparations. The manuscript correctly avoids identifying the equilibrium residual time with an ordinary fresh collision flight.

### 3.2 The strong response argument

For the tagged report, the largest ambient component has dimension four. The condition `Sobolev exponent > 2+r` is sufficient for moving Dirac masses to have strong derivatives through order `r`. In the tube coordinates, the initial position is affine in the radius; incidence direction and impact time do not vary with the radius. The factor `cos(phi)` stays in the measure rather than becoming an inverse-grazing divisor.

The bulk integral over `Q_R` still has a moving-domain contribution. The manuscript retains it by subtracting the disk integral and differentiating its moving upper radial endpoint. That term must not be discarded when comparing equilibrium preparations at different radii.

For a finite set of physical sampling times, splitting the event-time integration interval at those times produces a finite partition independent of `R`. The reflected velocities can jump across these cuts, but no moving cut is introduced by radius differentiation in these coordinates. The paper explicitly includes the parameter-dependent decoding from the tagged record into physical states. This resolves an important potential mistake; I do not find that mistake in the submitted proof.

Accordingly, I have no specific counterexample to Theorem 16.3 under its ambient-density, compactness, and branchwise smooth cylindrical-test hypotheses. This is a positive mathematical assessment of a defined theorem, not certification of every possible report, preparation, or horizon.

### 3.3 Why the contribution still needs a sharper novelty case

Boundary flux coordinates and the relation between section measure and phase volume are classical. Golse's Section 3, including Lemma 3.1, states the relevant free-flight integral relation and explains the distinct invariant measures; Chernov's paper treats mean-free-path formulae in billiards [R1–R2]. These are closer comparisons to the present short-time mechanism than a general reference to spectral perturbation theory.

One can see the limitation directly. For a suspension representation with collision-section probability `nu` and roof `tau`, uniform phase measure gives

\[
\mathbb P_{\rm eq}(\hbox{next collision by }T)
=\frac{\int \min\{T,\tau(x)\}\,\nu(dx)}{\int\tau(x)\,\nu(dx)}.
\]

Indeed, on a flight of length `tau(x)`, the set of elapsed times whose remaining flight is at most `T` has length `min(T,tau(x))`. When `T` is below the minimum roof, this reduces immediately to `T/mean(tau)`. This is the referee's derivation from the classical flux/suspension mechanism, not an assertion that a cited paper states the submission's entire tagged all-order theorem verbatim.

The all-order tagged-record presentation may be a useful formulation. An exhaustive priority determination was not made here. The author must compare that precise formulation, including its topology, preparations, and horizon, with the closest previous results. The absence of such a comparison cannot be replaced by calling the result “whole-preparation.”

Moreover, the finite-horizon property of the triangular table, its chaotic behavior, and its marked nonconjugacy are not used to overcome a multi-collision difficulty in Section 16. The short-time tube mechanism needs positive separation and smooth local geometry. The same mechanism can operate in separated periodic disk arrangements with infinite corridors. This is not a flaw in the theorem; it limits the extent to which the theorem exploits the deeper dynamical features emphasized earlier in the paper.

## 4. Local mathematical scope defects and explicit repairs

The following findings are classified carefully. A counterexample to a broad reading of a printed hypothesis is not automatically a counterexample to a narrower intended theorem. Each repair should appear in the statement itself and be propagated to every downstream use.

### M1. Proposition 4.4 silently changes the source from `xi.C+B` to `xi.C`

**Anchor:** [Section 4, line 52](source/sections/04_selection.tex#L52), `prop:constraints`; compare `prop:cumulants` immediately above it.

The preceding notation permits a bounded bias `B` in

\[
Q^{\xi,B}=\frac{e^{\xi\cdot C+B}}{Pe^{\xi\cdot C+B}}P.
\]

Proposition 4.4 says that if `Q^xi C=c`, then this law uniquely minimizes bare relative entropy among laws with that mean. Its proof invokes `B=0`, but the statement has not explicitly reset the notation. With the inherited bias this is false.

**Two-atom counterexample.** Let

\[
P=(1/2,1/2),\quad C\equiv0,\quad c=0,\quad \xi=0,
\quad B=(0,\log3).
\]

Then `Q^{0,B}=(1/4,3/4)` satisfies the mean constraint. Nevertheless,

\[
D(Q^{0,B}\Vert P)=\tfrac14\log(1/2)+\tfrac34\log(3/2)>0,
\]

whereas the feasible law `P` has entropy zero. Substitution of `Q=P` also makes the printed bias-free decomposition assert `0=D(P||Q^{0,B})`, which is false.

**Required repair.** State explicitly that the proposition uses `B=0` and redefine the tilted law there. Alternatively retain `B` and write the actual identity

\[
D(Q\Vert P)=D(Q\Vert Q^{\xi,B})+\xi\cdot c+QB-\log Pe^{\xi\cdot C+B}.
\]

The optimizer then minimizes `D(Q||P)-QB`, not bare entropy, unless the bias expectation is constant on the constraint class. This is a local, readily repairable statement/notation defect. It does not damage the correctly stated bounded-source Gibbs identity or the later binary calculations that explicitly use no extra bias.

### M2. Theorem 12.2 needs two density traces or an explicit common-trace hypothesis

**Anchor:** [Section 12, line 37](source/sections/12_response.tex#L37), `thm:shape`, equation `eq:shape`.

The hypothesis says that all fields have `C^1` branch extensions. The interface formula, however, factors out one density trace:

\[
v_\Sigma\rho\,[e^{V_-}F_- - e^{V_+}F_+].
\]

If the density is permitted to be merely branchwise smooth, it can jump. Then the correct interface term is

\[
v_\Sigma[\rho_-e^{V_-}F_- -\rho_+e^{V_+}F_+].
\]

**Counterexample to the branchwise-density reading.** In `(0,1)`, let the moving interface be `x=a`, with minus side `x<a` and velocity one. Choose a nonnegative smooth compactly supported function `psi` with `psi(1/2)=1`. Set the two density extensions to `psi` and `2psi`, take `V=0`, and use the same test `F=psi` on both sides. These fields are supported away from the outer boundary. The integral is

\[
J(a)=\int_0^a\psi(x)^2\,dx+2\int_a^1\psi(x)^2\,dx,
\qquad J'(a)=-\psi(a)^2.
\]

At `a=1/2`, its derivative is `-1`. The printed bulk derivatives vanish, and the printed common-density interface term is zero because the two test traces coincide. The formula therefore fails under the allowed branchwise-density interpretation.

The executable diagnostic uses a compactly supported `C^1` polynomial bump, sufficient for this theorem, to verify the value exactly. The argument above also works with a smooth bump.

**Required repair.** Either require a single globally continuous density with matching traces and the stated differentiability, or allow a branch-indexed density and keep both of its traces throughout the formula and proof. If a global common density was intended all along, this finding is a hypothesis-clarity defect rather than a refutation of that narrower theorem. Section 16 assumes an ambient smooth density explicitly and is not invalidated by this example.

### M3. Theorem 13.3 must distinguish smooth trajectories from smooth preparations

**Anchor:** [Section 13](source/sections/13_hybrid.tex), `ass:chamber` and `thm:chamber` (the theorem starts at line 48).

The chamber assumptions fix compact preparation support, regular dynamics, a fixed finite itinerary, and separation/transversality margins. They do not explicitly say whether the preparation measure is fixed or differentiable in the physical parameter. The theorem then passes from smooth trajectories to preparation-integrated and distributional response. In a paper whose initial preparation is generally `mu_a`, fixed support is not a substitute for regularity of the measure.

**Counterexample to allowing arbitrary parameter-dependent preparation.** Use identity dynamics with no events and the fixed compact support `{0,1}`. On `|a|<1/4`, take

\[
\mu_a=(1/2+|a|)\delta_0+(1/2-|a|)\delta_1.
\]

All dynamical regularity requirements hold; event conditions are vacuous. For a smooth test agreeing with `x` on the support,

\[
\mu_a F=1/2-|a|
\]

is not differentiable at zero. This also rules out strong distributional differentiability in a topology in which pairing with that smooth test is continuous.

**Required repair.** State that the preparation measure is fixed for the integral assertion. For varying preparations, give a sufficient hypothesis such as

\[
\mu_a=(X_a)_\#(w_a\lambda),
\]

with a fixed finite measure `lambda`, `C^r` transports and weights, and common integrable bounds for all required derivatives; then retain their derivatives. A suitable signed-measure differentiability assumption is another possible route. The trajectory-only conclusion is unaffected. Theorem 16.3 already supplies its own stronger density and normalization assumptions and is not refuted by this cusp example.

## 5. S1: an explicit separation between mechanical response and statistical regularity

**Anchors:** `thm:global-response`, `thm:binary-info`, `thm:continuous-state`, `thm:synthesis`.

This is a consequence of the submitted model, not an allegation that its negative-Sobolev theorem is false. It should be stated prominently because it obstructs an unjustified merger of the paper's major components.

Let `M_R` be the complete tagged-record law of Section 16. A colliding record contains `(q_0,v_0,s)`. Define the parameter-independent reconstruction statistic on the collision tag by

\[
\widehat R(q_0,v_0,s)=d_{\mathbb T_\Lambda^2}(q_0+s v_0,0).
\]

Since the disk radius is below the injectivity radius `1/2`, every regular collision under parameter `R` satisfies `R_hat=R`. For each fixed `R`, consider the measurable set

\[
A_R=\{\hbox{collision tag},\ \widehat R=R\}.
\]

For any distinct radius `R'` in the stated interval,

\[
M_R(A_R)=p_R>0,\qquad M_{R'}(A_R)=0.
\]

Interchanging the radii gives the reverse statement. Therefore

\[
D(M_R\Vert M_{R'})=D(M_{R'}\Vert M_R)=+\infty,
\]

and

\[
d_{\rm TV}(M_R,M_{R'})\ge\max\{p_R,p_{R'}\}.
\]

In particular, the full tagged experiment is not continuous in total variation at any interior radius for fixed positive `T`; it cannot be differentiable in quadratic mean there. This does **not** say that the whole laws are mutually singular: their no-collision parts can overlap. The correct statement is that each law has a positive-mass collision component absent under the other.

By contrast, observing only the collision bit produces the smooth Bernoulli family with information `p_R'^2/[p_R(1-p_R)]`. There is no paradox. Discarding exact geometric information changes the statistical experiment. Likewise, the full record can be `C^r` as a distribution in a weak negative-Sobolev topology while remaining separated in total variation.

This distinction is stronger than merely repeating the generic example of a moving Dirac mass: it occurs in the paper's own principal complete mechanical record. It also shows that arbitrary finite deterministic readouts do not preserve the asserted response. For example, fixing an interior `R_0`, the binary readout

\[
Y=\mathbf1\{\hbox{collision tag and }\widehat R\ge R_0\}
\]

has probability `p_R 1_{R>=R_0}`, which jumps at `R_0`. A finite alphabet supplies an exact predictive representation, not automatic parameter differentiability.

**Required clarification.** Specify, for each claimed application, whether the retained object is the ideal complete record, a smooth cylinder, the collision bit, or a particular noisy channel. To use the continuous positive-density theorem or a regular likelihood theorem in the same model, verify the hypotheses for that actual observation channel and its multi-step instrument. A generic smoothing statement, or the existence of a different reflection-free pointer example, does not by itself establish the desired compatibility for the full billiard experiment.

The manuscript often warns about these distinctions abstractly. Those warnings are welcome. The missing ingredient is a sufficiently strong positive theorem joining the components in one nontrivial model, not another warning that the components need not join.

## 6. Contribution audit beyond the collision theorem

### 6.1 Realizability: a useful accounting identity is not a characterization theorem

Theorem 5.1 takes the infimum of the Gibbs gap over a declared attainable set. Its proof is correct. But the identity does not characterize which laws are mechanically attainable, establish compactness of the physical protocol set, prove attainment for a nontrivial apparatus class, or identify a work cost. The coarse-preparation theorem reduces to conditional expectation followed by the Gibbs formula. The density cap is a strictly concave optimization with a clipped exponential solution. The cap-response estimate correctly uses the two variational inequalities and Pinsker's inequality; the paper sensibly avoids claiming universal classical second derivatives across active-set changes.

These results can be useful in a focused paper. Their physical force is only as strong as the verified implementation class. The direction-only Lorentz restriction is explicit but particularly simple: its conditional hit probability is constant, so its entropy-priced optimizer is unchanged equilibrium. Completed-bit rejection is a legitimate implementation with an independent auxiliary preparation and a failure symbol under a hard trial cap. It is not a new force realization or a derivation of a reset/work budget, and the manuscript correctly says so.

The author should identify the single nontrivial feasible-set or implementation theorem that constitutes a research contribution, rather than counting each consequence of the Gibbs identity as a separate major advance.

### 6.2 Instruments and predictive states

The chronological kernel construction and the canonical pointer shear are correct at the level stated. Retaining apparatus memory and back-action is necessary. It does not make every abstract kernel a physically realizable operation with a declared cost; the manuscript does not prove such a realization theorem.

Predictive state representations based on action-conditional future observations predate this submission [R3]. Here the state retains **all** finite tests, and the parameter extension retains their complete parameter curves or jets. The measurable-minimality proposition is a coordinate factorization statement. It is not a finite-rank realization, finite-memory reduction, learning guarantee, or complexity bound. The paper admits these limits, which is appropriate, but they reduce the significance of the advertised state construction.

The continuous-alphabet theorem does address a real logical issue. Positive jointly continuous finite-record densities on compact domains provide common versions, extend equality from dense parameter/action sets, and let a continuous map descend through a compact quotient. I find that proof convincing under the printed conditions. The comparison with partially observed control should remain hypothesis-specific: posterior continuity is not automatic even when the underlying state transition is weakly continuous [R4].

The generality here is mainly representational. Retaining an entire experiment as an infinite array avoids information loss because almost nothing needed for future prediction has been discarded. A theorem showing when that array admits a genuinely useful reduction would be a substantially stronger contribution.

### 6.3 Resource-aware dynamic programming

The finite backward recursion correctly retains residual resources. Randomization cannot improve the risk-sensitive exponential value when it merely mixes the same feasible first actions. The continuous-action proposition appropriately requires both upper and lower hemicontinuity rather than only a closed graph. The separate information-priced theorem explicitly fixes the recorded update and assumes legal pasting.

These are reasonable sufficient theorems, but much of the substantive control problem is in the assumptions: the resource descriptor must already be sufficient, feasible continuations must already be identified, and the law selections must already have physical implementations. The paper should not treat a valid Bellman calculation under those conditions as the missing implementation theorem. The synthesis does not provide a multi-step collision apparatus for which all these conditions are established together with the geometric response estimates.

### 6.4 Approximation and higher response

The normalization, observable-test, and quotient-jet estimates in Section 11 are largely sound. They explicitly charge small evidence and source amplification. The distinction between total variation and weak experimental tests is important. The finite-horizon value estimate also correctly requires the actual continuation tests and common feasible actions.

The chamber sensitivity formula agrees with the standard saltation mechanism, including the essential fixed-comparison-time correction [R5]. The higher-order recursions are finite differentiation identities. The complete-preparation Cauchy theorem is a Banach-space fundamental-theorem-of-calculus argument once every derivative is uniformly Cauchy. It does not prove those estimates in an additional many-collision model, and the paper does not claim it does.

This allocation of responsibility is mathematically honest. It is not, by itself, evidence of a deep new response theorem. Demers–Zhang is relevant prior perturbation work, but its abstract spectral results should neither be used to certify the present all-order moving-boundary assertion nor dismissed because they answer a different question [R6]. A serious novelty section must compare the exact results rather than the breadth of their titles.

### 6.5 The synthesis is predominantly a conjunction

Theorem 20.1 collects the short-time flux law, a Bernoulli experiment, an elementary tilt, a simple preparation restriction, rejection sampling, and conditional applicability of the predictor/resource theorems. The common parameter and common collision bit create a coherent example. They do not yet supply a theorem in which a hard geometric estimate is essential to a new realizability, reduction, or controlled-inference conclusion.

The reflection-free smooth-pointer class verifies that the continuous-density hypotheses are nonempty. It does not automatically verify them for the full multi-step billiard instrument. Conversely, the billiard collision bit is a regular finite experiment, but its two-point probability formula does not need the full machinery of continuous experiment-family quotients. This disconnect is the central limitation of the proposed “compatibility” contribution.

## 7. Criticisms that should NOT be carried forward

Several tempting negative comments would misrepresent this revision. The paper does not infer a score from every mechanical path derivative; does not equate entropy with energy; does not apply a continuous point-event probability ratio at a zero-probability observation; does not omit the initial-history reweighting in its history Doob transform; does not assume that independent re-preparation follows from deterministic mechanics; and does not silently discard the failure mass of a capped rejection protocol.

It retains the parameter likelihood of the past when a prior posterior is needed. It distinguishes the radius-independent prepared beam from radius-dependent equilibrium. It retains terminal velocity interface terms and the moving equilibrium normalization. It distinguishes a finite horizon and a prescribed finite derivative order from arbitrary time and analyticity. It explicitly lists the model estimates needed downstream in the eleven-paper program.

A harsh review should acknowledge these corrections. Repeating objections to claims no longer made would not make the review more rigorous. Nor should this A1 report certify or reject the other ten papers without reading their exact current sources.

## 8. What a substantively stronger submission would have to accomplish

The three local scope repairs are mandatory but insufficient. The publication entrance also needs a verified branch-level source delivery. Neither task addresses the principal editorial objection.

The author should choose one central mathematical bottleneck and prove a theorem that genuinely crosses it. Examples of meaningful directions are: a specified finite multi-collision regime beyond the first-flight gap with an actual common preparation and uniform derivative assembly; a nontrivial mechanically implemented instrument/control class with proved feasible-law and resource structure; or a reduction theorem with verifiable error and response guarantees that does not merely retain all future tests. These are alternative research directions, not a demand that every one be solved in this paper.

For the geometric route, the next useful milestone is not an arbitrary-time slogan. It is a concrete horizon where more than one collision has positive probability, an identified itinerary structure, a precise reporting topology, and estimates that control the actual singular interfaces after integration. The difficult estimates must be proved for that model rather than renamed an “assembly assumption.”

For the operational route, specify the apparatus and its preparation, parameter-independent policies, physical or trial budget, outcome/failure record, and the class of resulting instruments. Prove both realizability and the applicable continuation property. When observation smoothing is needed, use the same channel in the mechanical response, likelihood, and control theorems, and prove the required derivative/evidence bounds for that channel.

For the state route, exhibit a nontrivial finite-dimensional, finite-rank, or quantitatively approximate reduction for a class of actual experiments. Include parameter-family information and resource feasibility in the error statement. A declaration that all such information can be retained is not a reduction theorem.

Whichever route is chosen, the introduction should distinguish established inputs, elementary consequences, genuinely new lemmas, and model-specific estimates. The present preliminary identities can be compressed or moved to an appendix. The paper's importance must rest on the theorem that remains after that compression, not on the number of named statements or downstream references.

## 9. Independent finite diagnostics and their limits

The accompanying [referee_checks.py](referee_checks.py) was executed locally with Python 3.13.5, NumPy 2.3.5, and SymPy 1.14.0. **Twelve tests ran; zero failed, errored, or were skipped.** The [execution receipt](CHECK_RESULTS.json) records the exact script hash and numerical values. This is the referee's separate suite, not the author's suite.

The checks cover the biased-tilt counterexample and corrected identity; the two-density-trace counterexample; a nonsmooth preparation under smooth dynamics; the incoming Jacobian; flux normalization; the radius-derivative recursion through order eight; a nonconstant collision-angle observable; radius reconstruction from an exact tagged record; the geometric margins; and the failure mass of finite-trial acceptance.

An additional direct geometric sampling check used 400,000 cell proposals and retained 93,251 equilibrium initial states at `R=0.46`, `T=0.04`. It solved line–circle intersections in the periodic geometry rather than generating trajectories from the submitted collision-tube coordinates. The following comparisons were obtained:

| Quantity | Direct sample | Analytic value | Discrepancy / estimated standard error |
|---|---:|---:|---:|
| `P(hit)` | 0.1828505861 | 0.1828440614 | 0.0052 |
| `E[hit * (v_in . v_out)]` | -0.0600777699 | -0.0609480205 | 0.9295 |
| `E[hit * collision_time]` | 0.0036640680 | 0.0036568812 | 0.2389 |

The last two analytic values are `-p_R/3` and `p_R T/2`. The first follows by integrating `1-2 cos(phi)^2` against the conditional density `cos(phi)/2`; the second follows by integrating the uniform impact time. These tests exercise nonconstant records as well as total collision mass.

Passing these diagnostics supports coefficient/sign consistency and provides a reproducible check of the reported counterexamples. It does not prove coverage for all initial states, uniformity in the radius, an infinite family of derivative bounds, or any long-time theorem. The full-record singularity result S1 is established by the measurable-set argument above, not by finitely many radius samples.

## 10. Final recommendation to the editor and author

I would not recommend acceptance, nor a routine major-revision invitation at the requested journal level, on the basis of this manuscript. The appropriate editorial decision is **rejection in the present form**, with a future submission justified by a substantially stronger central theorem and a precise comparison with the closest literature.

There is useful mathematics here. In particular, the one-collision whole-preparation construction should not be discarded because it is short-time, and its proof should not be caricatured as a pointwise derivative argument away from grazing. The constructive task is to identify what new obstruction its method can actually overcome, prove that result, and reorganize the paper around it.

The three scope defects should be corrected explicitly. The complete-record statistical singularity should be stated and respected in every inference interface. Most importantly, the next revision must supply research substance beyond a more elaborate account of which future papers will supply it.

## References checked for this review

These are targeted primary/author sources, not an exhaustive priority search. Sources were accessed on 5 September 2026. Exact source overlap, not an allegation of unattributed copying, is the purpose of the comparisons.

**[R1]** F. Golse, *Recent Results on the Periodic Lorentz Gas*, arXiv:0906.0191v2 (2009), Section 3 and Lemma 3.1. The displayed flux/free-flight relation was inspected in the full HTML text. https://arxiv.org/html/0906.0191v2

**[R2]** N. Chernov, *Entropy, Lyapunov exponents, and mean free path for billiards*, Journal of Statistical Physics **88** (1997), 1–29. DOI: 10.1007/BF02508462. The publisher record and abstract were inspected; no identical all-order theorem is attributed to this source. https://link.springer.com/article/10.1007/BF02508462

**[R3]** *Predictive Representations of State*, NIPS 2001, official proceedings entry. The entry and abstract describe action-conditional future-observation representations and a linear representation-size result. This is cited for the established predictive-state idea, not as an identical parameter-family/resource theorem. https://papers.nips.cc/paper_files/paper/2001/hash/1e4d36177d71bbb3558e43af9577d70e-Abstract.html

**[R4]** E. A. Feinberg, P. O. Kasyanov, M. Z. Zgurovsky, *Partially Observable Total-Cost Markov Decision Processes with Weakly Continuous Transition Probabilities*, arXiv:1401.2168v2 (2014). The author abstract states the relevant continuity issue and sufficient conditions. https://arxiv.org/abs/1401.2168

**[R5]** N. J. Kong, J. J. Payne, J. Zhu, A. M. Johnson, *Saltation Matrices: The Essential Tool for Linearizing Hybrid Dynamical Systems*, Proceedings of the IEEE **112** (2024), 585–608. DOI: 10.1109/JPROC.2024.3440211. The full HTML discussion, including the fixed-time sensitivity update, was inspected. https://arxiv.org/html/2306.06862v3

**[R6]** M. F. Demers, H.-K. Zhang, *A functional analytic approach to perturbations of the Lorentz gas*, Communications in Mathematical Physics **324** (2013), 767–830. DOI: 10.1007/s00220-013-1820-0; arXiv:1210.1261. The author abstract and publication record were inspected. https://arxiv.org/abs/1210.1261

---

**Companion files:** [claim-by-claim audit](CLAIM_AUDIT.md), [review manifest](REVIEW_MANIFEST.json), [independent checks](referee_checks.py), [actual check receipt](CHECK_RESULTS.json), [unchanged reviewed source](source/).
