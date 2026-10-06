# Proof audit — General Theta Foundations I, Revision 95

The controlling report is v90/R60, external commit `cf13712c54e9ef0c9c54a240b1f26efc78cc3568` and pipeline audit `e4e72a512bf747e7bd190196cd8dc3db35689e3c`. Their frozen texts are unchanged. The immediate source baseline is v94 at remote head `db6739da3487be8787a67fc175b9086bd62f0e80`, native commit `24f48c90d6bcc1eae1d4c38ac5195405ac21da7d`, publication `0919ff61895716ea3de1d6a0f2a6a291935764d0`. No report on v91–v94 was found in the branch survey. These are observed predecessor identities, not identities of this local revision.

This is an author-side mathematical audit, not an independent referee approval. Printed Section 21 corresponds to `sections/88-equal-prior-initial-spectra.tex`.

## Statement and quantifiers

The input dimension d is at least two; the alternative basis is drawn once from a weighted exact second-moment family and reused twice; both hypotheses have prior one half. The first acquisition is a prescribed pure vector with Gram rho, not a classically flagged initial mixture. The full old receiver is bounded by two at the specified reset recording cut. The fresh reference may have any allowed dimension ell>=2. No old receiver subsystem enters the fresh preparation coherently. Public history, mixed channels, fresh mixtures, early stopping, null histories, countable outcomes and tester closure are all included through the inherited dimension-preserving normal form.

## The filter interval identity

For Hermitian X, the identity `||sqrt(M) X sqrt(M)||_1=max_(-M<=Z<=M) tr(XZ)` holds even at singular M: the order constraints annihilate the kernel and inverse square roots are used only on the support. Convex combinations of feasible maximizers prove concavity in M. For fixed A the substitution M=A tensor B gives concavity in B. Diagonal unitary invariance and averaging therefore give a diagonal B upper when A is diagonal.

**Rank trap checked:** pinching does not preserve a rank bound. The proof first relaxes fresh rank entirely, computes that unrestricted maximum, and constructs an optimizer on the old two-coordinate support. Only that final construction establishes equality for every ell>=2.

## Rank-two leaf certificate

Normalize A to eigenvalues x,1-x. Pinching B gives outside-support contribution 1-m and within-support contribution m F. Since the active maximum is at least d-1>=1, no outside mass is required. Rank one and A=0 are handled before division.

Set z=2x-1, v=1-z^2, e=d-1, C=d(d-2)+(2d-1)v, T=2psi_d(v)-e, and w*=z(eT-1)/C. The direct 2-by-2 block spectrum gives

```
2 F_z(w)=e(1+zw)+sqrt((z-w)^2+d^2 v(1-w^2)).
```

The exact upper certificate is

```
(T-ezw)^2-[(z-w)^2+d^2 v(1-w^2)] = C(w-w*)^2.
```

Its quadratic coefficient, linear coefficient and constant coefficient are all displayed in the proof. The proof checks T-ezw>0 on the full feasible interval and 0<=w*<=z<1. Thus taking a square root is legitimate, not an unchecked squaring of a stationary equation. For v=0 a pure aligned fresh factor yields d-1; for d=2 the apparent C=0 division is never used at that endpoint.

## Spectral envelope and full feedback

The function psi is strictly increasing and concave; its proof differentiates a rationalized square-root expression, showing the derivative decreases. Composition with 4x(1-x) yields a continuous symmetric strictly concave function on the rank-two simplex. The inherited rank-capped spectral-envelope lemma then identifies its exact roof at (q,1-q), q=max(lambda_max(rho),1/2).

For each first label, the refined physical normal form gives sum_h A_yh=rho with rank A_yh<=2. Gram traces are the weights used in the roof, not conditional history probabilities. Equal and unequal second labels have opposite centered-swap payoffs. Their positive parts add to alpha times the whole centered trace norm. Summing d first labels yields alpha*d=t^2/[2d(d+1)], not alpha and not 2alpha*d.

## Instrument converse

The inherited at-most-d commuting atom decomposition has one common spectrum (q,1-q). Set C_h^*C_h=w_h a_h and V_h=C_h C_0^+. On the actual Schmidt support, V_h C_0=C_h and sum_h V_h^*V_h=I. Extend the instrument on the unused orthogonal complement; it is never reached by the prescribed first acquisition. Fresh maximizing Grams are normalized, prepared independently conditional on h, and factor through a two-dimensional output. Final positive/negative spectral projections are complementary binary effects for every label pair. No artificial dilation dimension is retained. Every upper is simultaneously attained.

## Consequences and checks

At lambda_max<=1/2, psi(1)=d-1/2 recovers the v92 rank-two benchmark and the v93 optimal-initial cap. For rank-one initial rho, psi(0)=d-1 recovers the classical benchmark. At t=0 all scores equal 1/2. A pure-atom decomposition proves the rank-one-register assertion at every fixed initial rho.

For d=2, the rank-two roof is the original spectrum, so the single atom rho suffices. The fresh weights simplify to (1 +/- z/(1+2sqrt(1-z^2)))/2. The determinant formula is exact for all initial pure acquisitions. The spectral-loss inference deducts a calibrated score error before dividing by t^2; no assertion is made at t=0, and a score above the benchmark is identified as inconsistent with the supplied model/calibration.

## Executable versus proof

The new suite checks the symbolic certificate and its coefficient signs, rational enclosure endpoints, explicit instruments, complex pinching examples, Pauli Born probabilities, and controls rejecting independent redraw and incorrect fresh optimizers. Ordinary and optimized results must agree. The all-dimension argument is the written proof above, not a finite replay. All inherited suites remain in the build; neither proof originality nor physical reset calibration follows from them.

This revision was authored and verified locally. The active GitHub connector exposed reads but no write actions, and direct network access was unavailable. No v95 remote branch, push, Actions check, legacy status or human signature is claimed. Build receipts identify actual local Git objects; applying the source to a remote-backed checkout requires a new native commit and a fresh build. Independent human specialist priority clearance remains unobtained. The journal objective is unchanged, and no journal acceptance is claimed.
