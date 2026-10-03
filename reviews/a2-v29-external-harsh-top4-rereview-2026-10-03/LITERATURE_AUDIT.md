# Focused literature audit for A2 v29

## 1. Scope

This is a focused theorem/input comparison, not an exhaustive priority search. It does not establish that the v29 theorem is contained in prior work, nor does it infer journal significance from citation counts. Its purpose is to identify the closest observation traditions that a final novelty discussion should address.

The manuscript's current comparisons with covariograms and local-periodicity/Delone theory are useful. The principal omission is the much older theory of translated hit probes, capacity functionals and active geometric probing.

## 2. Observation in v29

For a deterministic obstacle set `O`, one attempted launch uses:

- a commanded starting density `f`;
- a fixed displacement `a=tv`;
- a single bit indicating a collision before time `t`;
- zero for both a solid attempted start and a free miss.

The reverse command translates the input density and reverses the velocity. The difference of the two means gives a spatially weighted signed finite difference of the occupation indicator.

This is not a translation-invariant autocorrelation. The input mask retains laboratory location. It is also not a passive trajectory observable: the spatial law, direction and horizon are controlled.

## 3. Random closed sets and mathematical morphology

### 3.1 Matheron

G. Matheron, *Random sets theory and its applications to stereology*, Journal of Microscopy 95 (1972), 15–23, DOI `10.1111/j.1365-2818.1972.tb03708.x`.

Matheron's summary explicitly describes mathematical morphology through structuring figures `B` and frequencies of events such as “`B` hits `A`” and “`B` is included in `A`”. It then formulates the random-closed-set capacity functional

`T(K)=P(A cap K is nonempty)`

for compact `K`.

The v29 sensor is not identical to this capacity functional:

- the obstacle is deterministic and the probe translation is randomized by a commanded density;
- the bit excludes a solid initial endpoint;
- two opposed commands are subtracted;
- the signed cancellation recovers an endpoint occupation difference;
- the bounded zero-witness minimum formula then fixes the additive ambiguity.

Nevertheless, the “translated segment hits a set” language and the use of hit frequencies are close enough that Matheron's framework should appear in the manuscript's nearest-observation comparison. The general concept that hit/no-hit frequencies of structuring elements encode sets is not new in 2026.

### 3.2 Modern random-set reference

I. Molchanov, *Theory of Random Sets*, second edition, Probability Theory and Stochastic Modelling 87, Springer, 2017, DOI `10.1007/978-1-4471-7349-6`.

Molchanov's monograph develops random closed sets, capacity functionals and related geometric operations in a modern framework. It is a natural general reference for the observation category, even though the deterministic signed reversal identity and periodic-lattice inverse in v29 are not standard random-set statements.

### 3.3 Consequence for novelty framing

The paper should not present “scalar hit probabilities determine geometry” as an unqualified new paradigm. Its more defensible increment is narrower:

1. the endpoint-exclusion reversal identity for attempted collision launches;
2. exact cancellation of interior-only segment intersections;
3. the bounded-diameter/separation zero witness;
4. the finite-chain minimum inverse with scale-independent mean-error propagation;
5. integration with repeated-motif period recognition.

## 4. Active geometric probing and binary projections

M. Lindenbaum and A. Bruckstein, *Reconstructing a convex polygon from binary perspective projections*, Pattern Recognition 23 (1990), 1343–1350, DOI `10.1016/0031-3203(90)90080-5`.

This paper studies unique reconstruction of convex polygons from binary perspective projections and identifies an equivalent tactile geometric-probe model. Its probes, finite-dimensional targets and reconstruction strategy differ substantially from v29. It does not obviously contain the reversal identity or the periodic repeated-motif theorem.

It nevertheless belongs to a long active-probing tradition in which binary responses are paired with controlled probe location/orientation. That is closer to the total information structure of v29 than passive marked-length, spectrum or uniformly prepared collision-count data. A final paper should acknowledge this tradition and explain the different probe, target class and exact identity.

Related geometric-probing, X-ray and discrete-tomography literature may contain additional relevant comparisons. This audit did not attempt to survey that field exhaustively.

## 5. Covariograms

B. Galerne, *Computation of the perimeter of measurable sets via their covariogram. Applications to random sets*, Image Analysis and Stereology 30 (2011), 39–51, DOI `10.5566/ias.v30.p39-51`.

The manuscript correctly distinguishes its signed, spatially weighted occupation difference from a translation-invariant covariogram. A covariogram integrates products of translated indicators; the v29 command family keeps the launch location through `f` and uses a difference of hit probabilities. No covariogram uniqueness theorem is imported.

The comparison is useful but should supplement, not replace, the capacity/hit-functional comparison.

## 6. Local periodicity and Delone theory

The manuscript cites and distinguishes:

- J. C. Lagarias and P. A. B. Pleasants, *Local complexity of Delone sets and crystallinity*, arXiv:math/0105088v1;
- N. Dolbilin, A. Garber, E. Schulte and M. Senechal, *Bounds for the regularity radius of Delone sets*, Discrete and Computational Geometry 74 (2025), 78–94;
- P. Herva and J. Kari, *Periodicity and local complexity of Delone sets*, arXiv:2504.20709v1 (2025).

Those works study local hypotheses that force or characterize periodic structure. Version 29 instead assumes a bounded periodic presentation and uses it to guarantee that one finite central patch contains all orbit representatives and protected generators. The paper recognizes the full intrinsic period group of an already periodic union; it does not prove crystallinity of an arbitrary locally finite set.

This distinction is accurately stated in the current manuscript.

## 7. Information comparison with the retained v28 experiment

The retained v28 theorem uses uniform launches and records first-impact positions. Exact support then directly reveals the boundary patch. Version 29 removes output location but introduces a grid of localized spatial commands and two calibrated collimated directions.

Neither experiment is uniformly more informative without specifying a comparison of input control, output, calibration, sample cost and apparatus range. The paper correctly declines to interpret the attempt exponents as competing minimax rates.

The same caution applies when comparing v29 with earlier uniformly prepared count laws. A spatially commanded family of Bernoulli means is not the previous count-only datum.

## 8. Audit conclusion

The existing period-recognition comparison is adequate. The novelty discussion of the scalar observation is not yet complete without random-set/morphological hit functionals and active geometric probing.

The focused comparison does **not** show that prior work subsumes v29. It does show that the broad premise “binary hit probabilities of translated probes encode a set” is classical. The manuscript's potentially new mathematical package should be stated as the particular signed reversal balance, zero-witness inversion, finite-confidence geometric recovery and periodic repeated-motif assembly under the declared active-input protocol.
