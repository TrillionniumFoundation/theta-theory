# Written-proof audit — Revision 75

This document is an author-side adversarial audit of the written theorem chain. It is distinct from an independent referee report, an exhaustive priority search, a proof-assistant certificate, and a source-reconstruction record. The controlling r48 report and audit are identified in `CONTROLLING_REPORTS.json` and reproduced in the frozen review files.

## 1. Object, quotient and normalization

The new object is the full closed body of ordered binary qubit effects

\[
 E=\tfrac12(aI+x\cdot\sigma)=qI+(p-q)P_u,
 \qquad 0\le q\le p\le1,
\]

with the negative effect `I-E`. Here `a=p+q`, `r=p-q=|x|`, and `x=ru` when `r>0`. The bias is `a-1`; it is a target coordinate. A scalar effect has `p=q` and no identifiable direction. The deterministic effects `0` and `I` and every one-sided singular face belong to the body. Outcomes are ordered. The output contains the classical outcome and no residual quantum system.

The distance is the supremum of the unhalved output trace norm over all common reference-assisted adaptive testers using at most `N` calls. Input entanglement, retained quantum memory, outcome feedback and public stopping are allowed. Lower witnesses may be chosen for a known pair; they do not depend on which member of that pair is actually supplied.

For one call, the two difference blocks are `B` and `-B`, where `B=tr_input[((E-F) tensor I)rho]`. Duality against Hermitian contractions gives `||B||_1<=||E-F||op`; an eigenstate attaining the extreme absolute eigenvalue gives equality. Consequently

\[
 d_1(E,F)=2\lVert E-F\rVert_{\mathrm{op}}
 =|a-a'|+|x-x'|.
\]

This proves `eq:biasedoneuse75`, fixes the factor of two, and establishes identifiability on the effect body itself. Outcome relabelling is not a quotient. The hybrid bound `d_N<=N d_1` supplies continuity and the projective limiting upper estimate.

## 2. Finite Bernoulli separation and the support cutoff

The spectral argument requires a two-sided finite-use comparison for arbitrary Bernoulli parameters, including probabilities at zero and one. Lemma `lem:bernoulliproduct75` supplies that comparison with a `1/N` support cutoff. The cutoff is part of the finite-distance statement; no positive lower bound on either probability is assumed.

The lower argument extends the already proved rare-event block estimate to both support endpoints. Complementing both bits, where necessary, puts the mean at most one half. If the larger probability then exceeds three quarters, the parameters are separated by more than one half and the one-use bound suffices. Otherwise the larger probability is comparable, up to fixed constants, to the larger endpoint variance. The no-success event over blocks of length comparable to the smaller of `N` and the reciprocal larger probability then has a gap proportional to block length times parameter separation. The block length is at least one, including when the reciprocal-floor expression vanishes. A common legal affine stochastic map recentres the pair to symmetric Bernoulli biases. The inherited finite majority lemma amplifies these biases over independent blocks.

All maps used in this lower proof are common to both hypotheses and have coefficients in the interval of legal stochastic probabilities. Complementation and block processing cannot increase distinguishability, so a lower bound for the processed pair is a lower bound for the original product pair. The no-success statistic is a proof device, not an assertion that it is the exact optimal radial decision rule.

The upper bound combines a direct bit coupling with product fidelity. The former provides the linear `N` scale near a support endpoint; the latter provides the variance-dependent square-root scale. Their minimum is equivalent, up to absolute constants, to the smooth cutoff expression. No Gaussian approximation is used at a zero probability. Identical parameters are removed before division by a variance. In the inherited radial notation, `q=(1-s)/2=0` implies `s=r=1` and hence an identical projective pair.

The exact product distance is preserved in the proof as the operational object against which the cutoff estimate is compared. Finite rational product calculations may check instances of this inequality; they do not replace its uniform proof.

## 3. Exact angular upper bound by a scalar-overlap dilation

Fix the spectrum `0<=q<=p<=1` and two directions separated by `h in [0,pi]`. A common coordinate change puts the eigenprojectors in one real plane. Let

\[
 A_0=\operatorname{diag}(\sqrt p,\sqrt q),\qquad
 A_1=\operatorname{diag}(\sqrt{1-p},\sqrt{1-q}),
\]

and use the measurement dilation which records the classical label both in the output and in the environment, leaving the square-root effect on an environmental copy of the input. A rotation of this copy is a legal environment gauge; it changes the dilation but not the channel observed by the tester.

For the real rotation generator `J` and `R_phi=exp(phi J)`, direct multiplication gives

\[
 A_0R_\phi A_0+A_1R_\phi A_1
 =\cos\phi\,I+f\sin\phi\,J,
 \qquad
 f=\sqrt{pq}+\sqrt{(1-p)(1-q)}.
\]

The off-diagonal skew coefficient is the classical root fidelity of the two outcome laws attached to the eigenvectors. The diagonal terms sum to the identity because `A_0^2+A_1^2=I`.

Write `t=h/2`. After inserting the input rotation, choose the gauge angle so that the skew coefficient cancels. Equivalently, take

\[
 \cos\phi=\frac{f\cos t}{\sqrt{f^2\cos^2t+\sin^2t}},\qquad
 \sin\phi=\frac{\sin t}{\sqrt{f^2\cos^2t+\sin^2t}}
\]

with the corresponding orientation convention for the environmental rotation. The resulting cross overlap of the two dilations is `c I`, where

\[
 c^2=\frac{f^2}{f^2+(1-f^2)\sin^2t}.
\]

Let

\[
 A=\sqrt{p(1-p)}+\sqrt{q(1-q)},\qquad r=p-q.
\]

The elementary identities

\[
 A^2=r^2\frac{f^2}{1-f^2}
\]

away from their removable degenerate cases convert this to

\[
 c^2=\frac{A^2}{A^2+r^2\sin^2(h/2)}.
\]

The channel overlap is scalar on the entire input space, not just on one chosen probe state. Purify every common tester operation, including its classical control, and retain the dilation environments for the overlap calculation. Each call multiplies the total overlap by `c`; interposed common isometries preserve it. Thus the purifications after `N` calls have overlap `c^N`. Tracing out systems can only decrease trace distance, yielding

\[
 d_N\le 2\sqrt{1-c^{2N}}.
\]

An at-most-`N` tester is padded after stopping with dummy calls on fixed inputs whose outputs are ignored. This leaves its operational output unchanged and makes the multiplication argument literal. The proof therefore covers the full adaptive quantifier, not only parallel product probes.

The bound `1-(1+z)^(-N)<=Nz`, together with the hybrid estimate `2Nr sin(h/2)`, gives the desired cutoff scale. Since

\[
 V=p(1-p)+q(1-q)\le A^2\le2V,
\]

the comparison may be written using

\[
 K_N(p,q)=r\sqrt{\frac{N}{V+N^{-1}}}.
\]

The angle `h=pi` is covered by the displayed sine/cosine gauge and needs no tangent division. If `p=q`, direction is unobservable and the angular distance is zero. At the projective spectrum `(p,q)=(1,0)`, where `A=0`, the hybrid bound is used directly. The deterministic scalar endpoints also have `r=0`. None of these cases is obtained by an invalid zero-over-zero substitution.

## 4. Matching angular lower witnesses

The lower proof uses two admissible experiments and takes the stronger conclusion. The first is a common randomized preprocessing which cancels the bias. Choose the rotation by pi about the normal to the plane of the two directions. With probability one half use the original input; with probability one half apply that rotation and swap the reported outcome. After discarding the random branch label, the resulting channel has effects `(I plus/minus r u.sigma)/2` under either hypothesis. The operation is the same for the two directions. Contractivity therefore transfers the inherited unbiased angular lower bound to the biased pair.

The second experiment uses the input direction tangent to the midpoint of the known pair. Its two outcome probabilities have common mean `a/2=(p+q)/2` and difference `r sin(h/2)`. The finite Bernoulli lemma supplies the corresponding rare-output-sensitive lower bound. It remains uniform when the mean approaches zero or one.

Put `b=a-1`. The legal body condition is `|b|+r<=1`, and

\[
 2V=1-b^2-r^2.
\]

The two lower witnesses involve denominators comparable to `1-r^2+1/N` and `1-b^2+1/N`. The elementary inequality

\[
 \min\{1-r^2,1-b^2\}\le2(1-b^2-r^2)
\]

on this double cone shows that the larger witness has the required `K_N` scale, up to absolute constants. The chordal term `sin(h/2)` is converted to angle with its explicit fixed constants. The inherited entangled-block argument enters only through the unbiased theorem, with its existing proof and attribution.

This also audits an important new boundary distinction. On `q=0` with fixed `0<p<1`,

\[
 K_N=p\sqrt{\frac{N}{p(1-p)+N^{-1}}}
 \asymp_p\sqrt N.
\]

One rank-one effect alone does not produce the projective `N` scale. At `p=q`, `K_N=0` and the direction disappears. At the projective spectrum, `K_N=N`. These cases rule out the incorrect extension obtained by simply substituting the radius of a fixed-bias section into the unbiased theorem.

## 5. Spectral projection and cancellation-free coupling

For an actual pair `E,F` with maximal eigenvalues `p,p'`, suppose first that `p>=p'`. Input a maximal eigenvector of `E`. The first positive-outcome probability is `p`, while the second is at most `p'`. Monotone likelihood ratio of Bernoulli product laws shows that this experiment has distance at least the product distance between `p` and `p'`. When `p<=p'`, use the maximal eigenvector of `F`. The same argument with minimal eigenvectors proves the corresponding statement for `q,q'`. Thus each of the two eigenvalue product distances is bounded above by the distance of the actual, possibly noncommuting pair.

The monotonicity claim is used only along an ordered side of the Bernoulli parameter. Its self-contained justification is that the likelihood ratio is monotone in the success count and its optimizing count interval has probability monotone in the other parameter. Endpoint cases follow directly or by continuity. No subtraction of two lower estimates occurs.

To align the directions, compare `E` to the effect with the spectrum of `F` and the direction of `E`. Measuring the common eigenbasis first produces one of two classical rows. Supply in advance `N` independent Bernoulli bits for each row, and consume the appropriate fresh row bit at each call. This is a common programme for every adaptive tester; unused bits are discarded. The trace distance of the two programmes is at most the sum of the two row-product distances. The aligned spectral channel distance is therefore bounded above by twice the actual pair distance.

Triangle inequality now bounds the fixed-spectrum angular comparison by three times the actual pair distance. Performing the alignment using either spectrum permits the smaller angular scale to be used. Combining these controls with the upper spectral path and the angular upper estimate proves `thm:biasedmetric75`. Scalar pairs are handled using the effect rather than a fictitious angle; a zero spectral gap contributes zero angular term.

The aligned two-row construction is an upper programme bound. It is not asserted to be an exact tensor-product equality for a general biased commuting pair. The exact v74 equality involved a special common flip programme, while the new pair permits row choices. This distinction is retained in the statement and proof.

## 6. Full-body lower cover and the logarithm

Theorem `thm:biasedcover75` concerns the whole four-dimensional effect body. Its lower proof builds targets near the projective corner using

\[
 \alpha=1-p,\qquad\beta=q.
\]

On a box where both `alpha` and `beta` are comparable to a dyadic scale `t`, with `t` between a fixed multiple of `1/N` and a sufficiently small constant, the spectral gap stays bounded below and all the relevant noise variances have order `t`. The two spectral spacings and the angular spacing required for separation are therefore comparable to `delta sqrt(t/N)`.

There are order `Nt delta^-2` spectral pairs in such a box. A sphere packing of angular spacing comparable to `delta sqrt(t/N)` has order `N t^-1 delta^-2` directions. Their product is order `N^2 delta^-4`, independently of the dyadic scale. The global metric lower estimate separates targets within a box. Choosing the boxes with fixed multiplicative gaps separates targets belonging to different scales by a spectral test.

Order `log(N+2)` boxes can be used. Bounded horizons are included by a fixed interior four-dimensional patch, with constants independent of the error. This proves the lower order uniformly in `N` on the stated sufficiently small-error range.

A radius-`delta` ball cannot contain two targets separated strictly more than `2delta`, regardless of its centre. Consequently the lower result permits arbitrary legal memoryless centres of the binary interface. Such a centre may lie outside every selected spectral box or fixed-spectrum slice. There is no projection onto a chosen subfamily, no retraction theorem, and no common-estimator premise.

For geometric interpretation only, the same critical divergence is visible in the projective-corner kernel

\[
 N^2\frac{d\alpha\,d\beta}
 {\sqrt{\alpha+N^{-1}}\sqrt{\beta+N^{-1}}
  (\alpha+\beta+N^{-1})}.
\]

Integrating over `alpha+beta` produces a logarithm. The actual theorem is supported by the explicit separated boxes and the matching code count; this interpretation does not assume a general Fisher-volume theorem or a new Ahlfors statement at a scalar singularity.

## 7. Exact full-body upper cover

The upper construction discretizes the Bernoulli square-root angle by two rational charts. With public integer

\[
 B=\left\lceil\sqrt{64N/\delta^2}\right\rceil,
\]

the `2B+1` ordered spectral levels cover `[0,1]` and include both endpoints. In the first chart the level is `j^2/(B^2+j^2)` for `0<=j<=B`; the second chart is its reflected complement. Every level is rational. The derivative bound in the square-root angle and product fidelity control the two spectral approximation errors uniformly even at zero and one.

For each ordered pair of levels, the direction mesh is a signed-axis rational stereographic grid sized by the proved angular upper scale at the decoded spectrum. A scalar spectral pair has one word. A nonscalar pair has all chart and digit words counted, including overlap. The one-index union capacity in `eq:biasedcapacity75` charges both spectral levels and the entire angular address.

The global count reduces to a two-dimensional spectral lattice sum with a cutoff corresponding to `1/N`. Near the projective corner its summand has the form of a reciprocal squared radius plus a positive cutoff. The annuli below the cutoff contribute a bounded amount of the final order; the annuli above it contribute the `log(N+2)` factor. The radial mesh scale is retained in this cutoff, preventing a spurious `log(1/delta)` loss. Nonsingular regions and scalar words fit inside the same upper bound.

This is an all-body construction: no chart is assigned to a nonexistent scalar direction, no positive spectral margin is imposed, and no independent angular factor is multiplied by an uncharged visibility parameter. It gives order `N^2 log(N+2) delta^-4` legal rational centres and the matching fixed-length payload law. Comparison constants are not optimized.

## 8. Algebraic comparisons, legality and resource interface

The input consists of rational Cartesian effect data. Its Euclidean norm and hence its eigenvalues may be irrational. Encoding compares these algebraic quantities with rational chart thresholds; it does not store a rounded irrational eigenbasis. Every reduction involving a square first checks the sign of the unsquared side. The deterministic maximal-coordinate chart and tie convention remain part of canonical encoding.

Decoding returns rational spectral levels and a rational unit direction from an exact stereographic identity. With `0<=q<=p<=1`, the decoded effect `qI+(p-q)P_u` is positive and bounded by the identity. Its negative complement is positive and their sum is exactly the identity. The Choi implementation uses the declared input-first transpose convention. Legality therefore holds for every syntactically valid in-range codeword, including redundant chart words.

Canonical replay is stronger: the encoder recomputes the unique codeword for a supplied target under the fixed tie rules. A valid but different legal word need not be that target's canonical encoding. The validation interface separates these statements. The stored error certificate is a proved construction budget, assembled from spectral and angular errors, not an exact optimization of the adaptive distance. In the new reference code the stated budget is `delta/2`; the inherited v74 `delta/4` budget is retained for its own construction.

The payload is the ceiling of the logarithm of the full index capacity. Public dimension, horizon and tolerance, input precision, schema syntax, row-start tables, transient arithmetic, expanded matrices and hardware are separate resources. The reference encoder is exact and finite; it is not claimed polynomial in the binary lengths of all numerical parameters or optimal in mutable workspace. The operation encodes supplied mathematical data and does not itself estimate an unknown device or implement the measurement through a physical classical processor.

## 9. Preserved unbiased geometry and earlier dependencies

The v74 metric, radial equality, cancellation-free proof, weighted Ahlfors criterion, boundary-contact law and exact joint codec remain active with their hypotheses. The weighted measure in that criterion is an auxiliary geometric measure on the identifiable image, not a prior or register entropy. The family-dependent error cap depends on the regularity data. The contact example retains its two-sided volume and support-deficit assumptions.

The unbiased disk has `(k,alpha)=(2,1)`, so its weighted integral is `N` times an integral of `(t+1/N)^-1`, giving `N log(N+2) delta^-2`. The unbiased ball has `(k,alpha)=(3,1)`, giving the boundary-dominated `N^2 delta^-3` order. Boundary mass refers to the chosen target measure. Equivalent Ahlfors measures change constants rather than these exponents. None of these retained statements is overwritten by the four-dimensional biased-body theorem.

The v73 entangled angular and majority lemmas, v72 observable readout and seizing theorems, earlier Choi/rank-preparation/coherent codes and numerical-streaming results retain their original proof graphs. The structural companion is inherited and still concerns fresh nondisturbing classical probes. The earlier width gaps remain separate. All predecessor paths are preserved, and the v74 author documents are copied to `predecessor-v74-audit/` before replacement in the new revision directory.

## 10. Literature, analytic pipeline and evidence

The direct comparison now includes Fiurášek–Mičuda's 2009 two-use projective measurement discrimination, alongside the 2014 noisy single-shot, 2018 projective single-shot and 2021 projective multiple-shot references. `LITERATURE_AUDIT.md` identifies which mechanisms are established and which theorem-level conclusions are submitted for independent priority assessment. Author-side analysis is not independent human clearance.

The independent repository graph remains `A2 -> A3 -> A4 -> C2 -> D1`, `B2-GC -> B1 -> B2-MC -> B3 -> B4 -> C1/C2 -> D1`, with A1 independent. No completion of those raw local-limit, stopped-path, global-kernel, conditioning, process-limit, nonlinear-resolvent, filtering, response or posterior obligations follows solely from the present finite-dimensional operational geometry. Aggregate status fields are maintained accordingly.

`check_biased_geometry.py` and the inherited exact suites provide finite algebraic, codec, parsing and regression checks. Normal and optimized runs must agree. The emitted regression record states the number and scope of assertions actually performed; no count is supplied here in advance. Those tests do not establish the adaptive supremum, universal continuum metric, full cover, priority or editorial significance. The first three require the written arguments audited above.

Source hashes, theorem locations, page checks and the build receipt under `evidence/` record reproducibility for their stated source. Final-head read-only reconstruction must identify the actual submitted commit, not merely an earlier native parent. A successful source build cannot be transferred automatically to an unchecked successor. Human authorship signing and independent priority remain separate from these records. This audit makes no claim of a human signature or of journal acceptance.
