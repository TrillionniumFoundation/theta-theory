# Literature audit for the external A2 v31 rereview

## Scope

This is a focused theorem-and-information-model audit conducted on 4 October 2026. It is not an exhaustive priority search. The purpose is to identify the closest mechanisms relevant to the new reciprocal mean-exit theorem and to separate classical ingredients from the manuscript's application-specific synthesis.

## 1. Capacity functionals and mathematical morphology

G. Matheron, “Random sets theory and its applications to stereology,” *Journal of Microscopy* 95 (1972), 15–23, DOI `10.1111/j.1365-2818.1972.tb03708.x`, formulates hit and containment probabilities of structuring figures and the capacity functional

\[
T(K)=\mathbb P\{X\cap K\ne\varnothing\}.
\]

I. Molchanov, *Theory of Random Sets*, 2nd ed., Springer, 2017, DOI `10.1007/978-1-4471-7349-6`, gives the modern random-closed-set framework, including capacity functionals and Minkowski operations.

These sources support the manuscript's current framing: segment-hit probabilities and swept-set morphology are not new notions. The paper's specific identity subtracts the solid-start event and then uses a reciprocal translation to expose a signed occupation difference.

## 2. Active geometric probing

H. Edelsbrunner and S. S. Skiena, “Probing convex polygons with X-rays,” *SIAM Journal on Computing* 17 (1988), 870–882, uses exact real-valued X-ray information for finite-dimensional polygonal targets.

P. Bose, J.-L. De Carufel, A. Shaikhet and M. Smid, “Probing convex polygons with a wedge,” arXiv:1506.02572, studies wedge probes returning apex, ray and contact-point geometry and gives finite probe bounds for convex polygons.

These models are genuinely different from the manuscript's Bernoulli collision response. They nevertheless confirm that reconstruction from actively chosen geometric probes belongs to a substantial established literature. The v31 contribution should be described as a particular binary-probability protocol with localized spatial input, not as the first general recovery from hit/no-hit information.

## 3. Killed random walks, Green operators and potential theory

G. F. Lawler and V. Limic, *Random Walk: A Modern Introduction*, Cambridge University Press, 2010, DOI `10.1017/CBO9780511750854`, treats Green functions and potential theory for random walks. The row-sum interpretation of a killed Green operator as an expected occupation or exit-time quantity is standard in this setting.

The v31 equality

\[
\|(I-Q)^{-1}\|_{\infty\to\infty}
=\max_x\mathbb E_x\tau
\]

for a finite substochastic transition matrix is therefore a classical Dirichlet-resolvent fact. The manuscript correctly uses it as interpretation and sharp finite-state norm information rather than claiming a new general Green-function theorem.

The quadratic stopped martingale behind

\[
\mathbb E_x\tau\le\frac{(D+b)^2}{v_*}
\]

is likewise classical. What is specific here is that the measured reciprocal collision imbalance supplies the forcing while the physical component diameter and separation provide an unknown-zero-set exit bound.

## 4. Stochastic shortest paths and value iteration

D. P. Bertsekas, “Proper Policies in Infinite-State Stochastic Shortest Path Problems,” arXiv:1711.10129; *IEEE Transactions on Automatic Control* 63 (2018), 3787–3792, DOI `10.1109/TAC.2018.2811781`, studies proper policies, finite expected termination, Bellman equations and value-iteration behavior in infinite-state stochastic shortest-path models.

This supports the manuscript's disclaimer that finite-expected termination and value iteration are not new abstract principles. The unknown occupation and unknown zero set make the present inverse formulation different from a standard specified-cost control problem, but the Bellman machinery itself is classical.

## 5. Periodicity and local structure

The retained v30/v29 comparison cites work of Lagarias–Pleasants, Dolbilin–Garber–Schulte–Senechal, and Herva–Kari on local complexity, crystallinity and regularity of Delone-type sets. Those works ask when local patterns force periodic or regular global structure.

The present theorem assumes a bounded periodic presentation from the outset and reconstructs the primitive period group after recovering a sufficiently protected finite patch. It is not a crystallinity theorem for an arbitrary Delone or aperiodic configuration. The manuscript now states this distinction correctly.

I did not re-read every retained periodicity source in full during this v31 rereview. Their exact citations and prior audit remain in the retained v30 source.

## 6. Statistical active set and level-set estimation

The finite v31 theorem is also naturally adjacent to binary active level-set or set-boundary estimation: an observer chooses spatial query locations and estimates whether a smoothed occupation lies above a threshold.

The models are not identical. Here each query is a reciprocal collision probability, the target is a separated union of convex bodies, and the construction uses morphology, hulls, support smoothing and period locking. Nevertheless, a journal version should compare the sufficient rate

\[
O\!\left(\nu^{-3}\log\frac{C}{\nu\delta}\right)
\]

with the active set-estimation literature rather than leaving the exponent in isolation. No lower bound or minimax claim is proved in v31, so the displayed order should not be presented as statistically sharp.

## 7. Focused novelty conclusion

The audit found no basis for attributing novelty to:

- capacity functionals or swept-set morphology;
- stopped-martingale exit bounds;
- killed Green resolvents;
- value iteration under finite expected termination;
- generic active geometric probing;
- compensated smoothing or Hoeffding bounds.

The application-specific synthesis that appears genuinely distinctive is:

1. the endpoint-excluded reciprocal collision protocol;
2. identification of its pooled mean as \((T_\rho-I)u\);
3. recovery on a bounded separated physical class without a supplied zero set;
4. a fixed-aperture four-direction finite implementation;
5. coupling to the retained periodic patch and rational-relation reconstruction.

That synthesis is mathematically meaningful. This audit did not find a primary source that directly contains the complete combination. This is not a priority certificate, and no conclusion about top-four significance follows merely from that absence.
