# Independent Referee Report — Round Eleven

**Manuscript:** A3 — Full Empirical-Path LDP  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *JAMS*  
**Recommendation:** **Reject**  
**Reviewed branch:** `revision/round11-referee-positive-closure-11paper-2026-08-31@e81cbf57624d21be23ee9d982a1255c076363761`  
**Reviewed source:** `revision/round11-referee-final/A3_RENEWAL_COEFFICIENT_RECESSION_LDP.tex` (Git blob `a795acbd250c7a00de1313dfcdca25a03438cbb9`)

## Executive assessment

Round eleven correctly abandons a random LDP speed and no longer replaces the countable return process by a non-lumpable finite cemetery chain. It also recognizes that macroscopic terminal excursions must remain in the state. These are the right structural moves.

The new proof, however, consists almost entirely of theorem-sized assertions. The finite coefficient argument gives only local exposed-point information, the terminal partial excursion is not present in the renewal coefficient operator, unbounded tail coordinates lie outside the stated source theorem, and the physical-time law is not obtained from the collision-horizon law by a proved speed-change theorem. The claimed full good path LDP is therefore not established.

## Major mathematical objections

### 1. The finite coefficient theorem does not prove a full finite-dimensional LDP

Cauchy coefficient extraction near a simple real saddle can give a local logarithmic asymptotic and an exposed-point lower bound. The manuscript then states that the finite-dimensional empirical state “therefore satisfies an LDP.” That inference is invalid without:

- an upper bound for arbitrary closed sets;
- lower bounds at nonexposed finite-rate points;
- exponential tightness;
- control of multiple saddles and lattice periodicity; and
- an effective-domain theorem for the countable renewal pressure.

A matching lower bound at regular exposed points is not a full LDP.

### 2. The renewal coefficient does not include the stopped terminal excursion

The state at deterministic collision horizon \(n\) contains \(N(n)\) completed excursions and a pointed prefix of the next excursion. A standard coefficient of total renewal length \(n\), however, sums paths whose *completed* return lengths equal \(n\). It does not describe paths stopped strictly inside an excursion with \(A_n>0\).

The proof never introduces the entrance/residual operator that chooses an excursion of length exceeding the remaining clock and records its prefix. Hence the coefficient theorem and the empirical state in the headline theorem are different probability objects.

### 3. The tail-profile coordinates are unbounded and are not covered by the source theorem

The finite theorem allows bounded edge/profile cylinders and a bounded clock source. The recession coordinates contain

\[
r(a)1_{\{r(a)>L\}}\delta_{K_a},
\]

which are unbounded. Their log-Laplace transforms have a restricted domain determined by the return-tail exponent. Projective consistency as measurable maps does not supply an LDP for these coordinates, and ordinary exponential moments do not automatically provide exponential tightness in an infinite profile-measure space.

### 4. The recession rate is defined by the theorem it is meant to prove

The “lower-semicontinuous epigraph limit of actual long-excursion coefficients” is not constructed. Existence, projective consistency, the Gamma-liminf, and recovery are all asserted in one paragraph. Concatenation also requires legal transitions, control of Gibbs distortion, and a connector cost uniform relative to the long clock. None is quantified.

### 5. The singularity shield is not an exponentially good approximation theorem

Absolute continuity of homogeneous branch measures and a profile exposure coordinate do not imply that visits to iterated singularity neighborhoods can be removed with the required exponential accuracy. The complexity grows with excursion length; the shield must be uniform over the recession recovery family. The manuscript supplies no frequency estimate, no neighborhood schedule, and no source-uniform bound.

### 6. The physical-time LDP is not a continuous contraction of the collision-time LDP

A law indexed by collision horizon \(n\) and speed \(n\) does not directly produce a law indexed by physical time \(T\) and speed \(T\). One needs a joint collision/roof LDP, inversion of the random clock, residual-flight control, and conversion of rate normalization. Retaining the roof prefix makes the map measurable; it does not prove the change of speed.

### 7. The recurrence classification is disconnected from the rate proof

Vere–Jones recurrence of a scalar renewal matrix does not by itself classify the weighted Gibbs operator with all profile sources or prove the tightness statements later used. The proposition supplies terminology but no analytic consequences for the projective rate.

## Status of earlier objections

The manuscript has genuinely corrected the random-speed statement, the false SPR dichotomy, and the claim that a convex recession profile must be realized by one excursion. The load-bearing coefficient, tail, singularity, and clock-inversion theorems remain absent.

## Minimum reconstruction

A viable paper must construct one joint deterministic-clock renewal process including the terminal residual operator, prove full finite-dimensional LDPs on a source domain containing the tail coordinates, establish exponential tightness in a specified profile topology, and then prove a separate physical-clock inversion theorem.

## Recommendation

**Reject.** The state design is improved, but the full empirical-path LDP is still a program summarized as a sequence of theorem statements rather than a completed proof.