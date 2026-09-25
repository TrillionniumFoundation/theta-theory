# Response to the twenty-first pipeline-aware referee report

**General Theta Foundations I — Revision 37**  
**Entropy Dissipation and Sharp Finite-Alphabet Memory**  
25 September 2026

Controlling report: `reviews/general-theta-foundations-i-v36-finite-alphabet-memory-pipeline-harsh-top4-r21-2026-09-25/REFEREE_REPORT.md`, frozen at `d6b89112389b97a16a287fa32f3f75e4c2d72e0a`. Reviewed v36 publication: `1a08578710d55a2379cea56c43feb5eca56340a2`; native mathematical source: `d60efb58807c3feffa01065e698d1fa9fe140802`.

The report identifies the logarithmic gap for finite spectral-gap alphabets as the principal unresolved question. This revision closes that gap under exactly the preceding spherical L2-gap hypothesis. It does not add an atomic Haar command, restrict hidden states to observable vectors, or strengthen an L2 gap to a logarithmic Sobolev inequality. A new entropy argument works at each command epoch and amortizes conditional-mean compression through one quadratic loss budget.

The stable labels below are resolved to the compiled theorem numbers and pages in `evidence/THEOREM_LOCATIONS.json`. All new analytic proofs are in the focused article. Successful finite checks and repository publication do not independently certify those proofs or their originality.

## 14.5 / Sections 5.5 and 10 — the logarithmic state-cardinality gap

**Resolved for every finite orthogonal alphabet satisfying the stated full spherical L2 gap, at fixed positive calibrated signal and fixed sufficiently small output error.**

`thm:main` proves

```
c N^((d-1)/2) <= W_(N,epsilon) <= W_(N,0) <= C_d N^((d-1)/2).
```

The converse allows arbitrary hidden directions, time-dependent state sets and rows, and a different machine at every horizon. The exact upper construction is the rational spherical synthesis of v36, reproduced with its full proof. The separate positive minimum remains d+1 whenever the identity is present and d*rho<1.

The former proof spent O(log k) letters on every new packet to mix a point orbit at the scale of k centers. We do not claim that mixing has become faster. Instead, we smooth the law of the proof-side conditional centroid Z_t by a fixed Gaussian scale tau, retaining its entropy across all epochs. The Gaussian is not an extra observation, private random variable available to the machine, or approximation of the specified experiment.

There are three steps.

1. **Quadratic entropy cost.** In `lem:centroid-entropy`, if M=E[X|J], then `h(X+tau G)-h(M+tau G) <= E|X-M|^2/(2 tau^2)`. The log density of a Gaussian mixture has Hessian bounded below by `-I/tau^2`. Conditional centering cancels the first-order Taylor term in cross entropy. No unjustified entropy monotonicity under convex order is used.
2. **One-step entropy production.** In `lem:entropy-gap`, a spherical L2 norm gap gives `h(Pf)-h(f) >= (1-lambda^2)||sqrt(f)-Pi sqrt(f)||_2^2`, where Pi averages at each radius. This follows from the relative-entropy/Hellinger comparison and the angular L2 contraction. It is not one-step mixing in total variation and requires no density for the unsmoothed orbit law.
3. **A sparse-mixture obstruction.** In `lem:sparse-root`, at most k centroids with nonvanishing expected norm leave a definite angular Hellinger defect after smoothing at tau of order `k^(-1/(d-1))`. A union of caps around the long centroids has little surface measure but captures definite smoothed mass. This argument allows arbitrary atom weights, coinciding directions and centroids near zero.

The conditional-mean identity gives

```
Delta_t = E|Z_t|^2-E|Z_(t+1)|^2
        = E|U_(a_(t+1)) Z_t-Z_(t+1)|^2,
sum Delta_t <= 1.
```

Thus the entropy cost of every compression is paid from the same bounded sum. The endpoint entropy range contributes at most logarithmically in 1/tau and is absorbed by tau^(-2). This is the reason the previous repeated packet logarithm disappears.

## A stronger time-dependent occupation statement

`thm:occupation` permits independent command laws changing with time. With `g_t=1-lambda_t^2`, `m=d-1`, a spherical cap constant A_d, and `a_d=3+2/m`, it proves

```
sum_{0<=t<N, K_t<=k} g_t <= B_d kappa^(-a_d) k^(2/m),
B_d = 2048 d (16 A_d)^(2/m).
```

There is no bound on the widths at other cuts, nor a requirement that every g_t be positive. The result also holds for positive-probability labels under this particular independent-command law. Counting endpoints 1,...,N rather than source cuts 0,...,N-1 changes the unweighted count by at most one.

For a fixed gap, calibration gives `kappa=rho/sqrt(d)-2 epsilon`. The explicit peak lower bound is

```
K >= [(1-lambda^2) kappa^(3+2/m) N/B_d]^(m/2).
```

No numerical constant is optimized. We determine the cardinality order, not the exact integer optimum or leading asymptotic coefficient.

`cor:actual-error` also bounds the compact finite-dimensional optimum of actual terminal error for a prescribed profile. It allows intermediate errors to cancel. Accumulated local deficiency is treated only afterwards, by composing its common-row kernels into a real machine; it is not identified with the optimal terminal error.

## 14.3 / Sections 5.3 and 11.1 — quantization and entropy comparisons

**The geometric rate is explicitly classical, and the mathematical roles are separated.**

The main article identifies cosine-loss orbit distortion with half the squared chordal k-center distortion. Graf–Luschgy's framework and Iacobelli's manifold quantization theorem are cited at that definition. On the compact sphere, the exponent 2/(d-1) follows already from elementary cap and covering bounds. We do not claim a new quantization exponent, Zador constant, or covering theorem.

The new sparse lemma measures angular variance of the square root of a smoothed centroid density; it is not the distortion of a newly sampled packet product. The causal conclusion comes from combining that defect with entropy production and a telescoping conditional-mean loss.

Polyanskiy–Wu's Gaussian-smoothed entropy continuity is compared directly. Its regular-density/Wasserstein mechanism is classical. Our one-sided quadratic inequality uses a martingale coupling, so its linear term cancels. We prove the precise estimate used here and do not claim that the underlying Gaussian Hessian identity has no antecedent. The new principal assertion is the gap-weighted occupation and its sharp width consequence, not a renamed score identity.

`LITERATURE_AUDIT.md` records what was inspected, the minimized quantities, the relevant assumptions, and the differences. A publisher record is not described as a full-text proof audit.

## 14.4 / Section 7 — quantum memory and correct units

**The explicit rational comparison is strengthened, with labels, bits and quantum dimension stated together.**

`thm:rational` applies the sharp theorem to the same five rational three-dimensional commands used in v36. Its exact and fixed-error classical label complexity is Theta(N), so the persistent atomic label bits are `log2 N+O(1)`. `prop:qubit` repeats the exact one-qubit realization with seed reset channels, fixed command unitaries and one final Pauli query. The quantum memory dimension is two. No linear lower bound in classical bits is claimed.

The comparison is not a language-recognition separation. A strict-cutpoint conversion can attenuate a numerical margin with length while retaining its sign. Such a conversion does not meet the fixed wordwise numerical tolerance here.

The expanded comparison also covers Gu et al.'s entropy advantage, Thompson et al.'s input–output transducers, and Ghafari et al.'s memory-dimension advantage for stochastic processes. In particular, input commands are not claimed as a distinction absent from the earlier quantum transducer literature. Our quantified classical competitor is an arbitrary horizon-specific nonuniform simulator, and our objective is maximum row error and maximum available labels, not stationary memory entropy or a generated-process prior. These comparisons do not assert that quantum memory advantage itself is new.

## 14.6 — the external gap is still an external input

**Explicit matrices are kept distinct from a numerically certified gap.**

The proof again identifies the algebraic SU(2) lifts, their dense generated subgroup, the symmetric lazy walk, and its homogeneous sphere quotient. The left action and inverse density-pullback convention are fixed. Bourgain–Gamburd's theorem supplies existence of a spherical norm gap.

No numerical value of lambda_* is claimed. With A_3=1, the exact conditional formula is

```
K >= [(1-lambda_*^2) (1/(10*sqrt(3))-2 epsilon)^4 / 98304] N.
```

It makes dependence on any independently supplied gap certificate explicit. The finite tests of rational gates establish identities only; they are not tests of the infinitely many spherical harmonics. The lower constant for the named example remains unevaluated, while its asymptotic order is now matched.

## 14.7 / Section 9.2 — the finite-coin timing convention

**Repaired by deterministic-duration padding, not by assuming the source cannot see duration.**

Appendix `thm:compiler` consumes exactly `(L-1)b` fair-bit microsteps for every macro update. Each threshold comparison consumes all b bits, even after its result is decided. If a categorical leaf is reached early, its selected new label is held while dummy bits are consumed. The old label is released at that point, so no hidden K-by-K product is introduced. Deterministic thresholds and shorter trees are padded too.

The bit position, current input, relation, decision-tree node and ready/query phases are counted. The resulting label bound is `C K(b+1)` for fixed alphabets and row sparsity. Private coin outcomes cannot change the visible ready time. This does not claim privacy of the output label itself or enlarge the wordwise theorem into adaptive experimental-design optimization.

Rounding and stochastic contraction give the same finite tolerance. Threshold tables and their construction remain free nonuniform data. Exact real atomic sampling and fixed-error fair-bit implementation remain distinct resources. The resulting padded bit bounds have leading coefficient (d-1)/2, with an O(log log N) upper excess; an exact order for padded label cardinality is not inferred.

## 14.1–14.2 / 14.8 — presentation and preservation

The program prefix General Theta Foundations I is retained with the precise subtitle **Entropy Dissipation and Sharp Finite-Alphabet Memory**. The abstract leads with the resolved cardinality law, states the nonuniform clocked atomic-row model, and spells out the quantum memory units. No editorial level or acceptance is asserted.

The focused article has one central proof chain: conditional-centroid entropy cost, angular entropy production, sparse-smoothed obstruction, occupation, and sharp finite-alphabet width. The explicit five-gate application follows it. The compiler is an appendix. The monomial cube-root law, full-word packet theorem, earlier rotation results and other v36 mathematics remain unchanged in `supporting-results.pdf` and the cumulative archives; no substantive predecessor result is deleted or silently weakened.

The compact referee ZIP excludes the large archives. It contains the current paper, response, literature audit, theorem locations and independently buildable core sources. Every older repository path remains unchanged. Archival page counts and verification counts are not part of the mathematical significance claim.

## Pipeline and remaining distinctions

The frozen Round-Seventeen ledger and the relevant v34–v36 sources were consulted. The local `sharp_spectral_gap_width` objective is now marked proved under its exact L2-gap and signal/error assumptions. Independent A2 Fourier/LLT, stopped-LDP, nonlinear-semigroup, common-domain and optional-projection gates are not replaced by an entropy argument on finite registers. Fully adaptive collision validation, noisy-tag composition, and general all-irrational cyclic classification remain distinct tasks.

We have not proved optimized constants, all finite integer widths, a uniform signal-to-zero law, an explicit numerical Bourgain–Gamburd gap for the five gates, a uniform program-space theorem, or sharp compiled fair-bit label cardinality. Those distinctions do not change the resolved sharp atomic-width order for every finite alphabet in the stated spectral class.

The report's requested independent priority audit has not been obtained by this revision. A careful primary-source comparison is included, but internal reports, tests and compilation are not external peer review. The new entropy argument and its claimed scope should be independently checked in the next referee round.
