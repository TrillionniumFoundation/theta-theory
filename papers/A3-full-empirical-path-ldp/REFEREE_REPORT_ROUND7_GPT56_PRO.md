# Round-Seven Independent Referee Report — GPT-5.6 Pro

**Manuscript:** A3 — Full Empirical-Path Large Deviations for Periodic Sinai Billiards  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*  
**Recommendation:** **Reject**  
**Reviewed revision:** `revision/round7-referee-positive-closure-11paper-2026-08-31@b1e3d17f59ca9bb1a04d4ac9157f10dc333f9607`  
**Controlling module:** `ROUND7_POSITIVE_CLOSURE.tex`, blob `d57949b23204a0abaa264213e4ce0417263659c7`

## Executive assessment

The explicit recession coordinate and the insistence on admissible graph edges are important conceptual improvements. The paper also correctly stops using periodic orbit measures as entropy-preserving approximants for positive-entropy phases.

The proposed compactification nevertheless loses the branch/transition information required to define the recurrent entropy, while its recession rate is created by declaring a Gamma limit that has not been shown to exist. The “actual excursion recovery” proof is circular, and the marked empirical measure uses branch-averaged profiles without proving exponential equivalence to the actual orbit empirical process. The headline full path LDP is therefore not established.

## Major mathematical objections

### 1. The mark \((r(a)^{-1},K_a)\) does not identify an inducing branch

The paper defines

\[
\Lambda_N=R_N^{-1}\sum_j r(a_j)
\delta_{(r(a_j)^{-1},K_{a_j})}.
\]

It then says that the restriction to \(x>0\) determines the recurrent occupation measure \(m\) on the inducing alphabet. This is false in general. Two distinct branches can have the same return length and the same finite-window averaged profile \(K_a\), while having different endpoints, transition possibilities, Gibbs weights, or symbolic information. The map

\[
a\longmapsto (r(a)^{-1},K_a)
\]

is not proved injective and has no reason to be injective.

Hence \(\Lambda\) does not determine the branch transition process, its entropy, or the induced potential average. The quantity \(\mathcal J_{m rec}(m)\) is therefore not a function of the announced state \(\Lambda\). The central rate functional is ill defined unless the mark retains the branch label or a complete transition kernel.

### 2. The branch profile is an averaged law, not the actual excursion profile

For an actual point \(y\in Y_a\), the empirical excursion profile is

\[
 r(a)^{-1}\sum_{j<r(a)}
 \delta_{\Theta^j\Gamma(y)}.
\]

The manuscript replaces this random profile by its branch conditional average \(K_a\). Bounded distortion only compares densities on a branch; it does not imply that two such density-weighted averages differ by \(O(r^{-1})\), nor does it show that an individual excursion profile is exponentially equivalent to \(K_a\).

A finite-window observable may vary throughout the branch, and the cumulative discrepancy can be order one. A full empirical-path LDP cannot be obtained by replacing every excursion by a conditional expectation without an exponential approximation theorem. None is proved.

### 3. A Gamma limit is assumed, not constructed

The functions \(c_L\) form a sequence on compact finite projections. Compactness gives subsequential Gamma limits; it does not imply that the full sequence Gamma-converges or that different subsequences have the same limit. The text simply writes

\[
c_\infty=\Gamma\hbox{-}\lim_{L\to\infty}c_L
\]

and then treats the defining recovery property as a theorem.

Equicoercivity supplies compactness of minimizing sequences, not existence or uniqueness of the Gamma limit. To prove the announced result, the authors must establish the Gamma-liminf and Gamma-limsup envelopes and show they coincide on a projectively compatible state space. The current “diagonal definition” is circular: it declares the recovery sequence whose existence the theorem is meant to prove.

### 4. Concatenating excursions does not generally produce one excursion

Convexity and the pressure dual are justified by concatenating two long inducing branches with a uniformly bounded connector. But inducing branches are first-return words. A connector that passes through the inducing base creates an intermediate return, so the concatenation is a sequence of excursions, not one branch admissible in the definition of \(c_L\). If the connector is required to avoid the base, its uniformly bounded existence is a new specification theorem and is not established.

Thus the claimed subadditivity of the single-excursion pressure, Fekete limit, convexity of \(c_\infty\), and recovery of barycentric combinations do not follow.

### 5. The recurrent–defect normalization is formal rather than topological

The proof of

\[
\int r\,dm+\zeta(1)=1
\]

says the escaped mass is “interpreted at the boundary.” Weak convergence of \(\Lambda_N\) does not by itself identify the limit of the unbounded function \(x^{-1}\). The whole purpose of the defect coordinate is to retain that missing moment, but the claimed identity requires a precise compactification theorem and lower-semicontinuity argument. The displayed manipulation does not supply one.

### 6. The survivor approximation and spectral dichotomy remain unproved

The finite-state approximation proof assumes a positive stationary flow in a finite admissible truncation and repairs it by mixing with a periodic orbit. A general irreducible countable component need not contain a finite strongly connected subgraph carrying both the retained transitions and a periodic orbit that puts the flow in the relative interior. Entropy convergence with unbounded information function also requires a quantitative tail theorem, not a sentence invoking uniform integrability.

Likewise, the SPR/non-SPR alternative is a research theorem for the specified billiard coding. The manuscript does not build the strong/weak spaces, renewal operators, or pressure comparison needed to identify every non-SPR contribution with the proposed recession rate.

### 7. The physical-time completion mixes collision and roof arithmetic

Coprime integer collision lengths allow one to fill large integer collision counts. They do not fill arbitrary real physical durations, because the corresponding roof sums are not integer multiples of those lengths. Stopping inside a final suspension segment can hit an exact physical time, but then the proof must quantify the effect on the marked profile and rate. The Frobenius argument does not do this work.

## Dependency assessment

A3 remains independently open even if A2 were repaired. A4 has no established parent path LDP or phase compactification, and C2/D1 cannot contract a rate that has not been defined on a state carrying the required entropy and transition information.

## Required reconstruction

The state must retain enough branch/transition information to define entropy and admissibility, while separately recording a recession profile. The authors must prove exponential equivalence between actual excursion profiles and any reduced mark, establish a genuine Gamma-convergence theorem for excursion costs, and construct recovery words without introducing intermediate returns or forbidden edges.

## Recommendation

**Reject.** The recession idea is promising, but the announced state loses the data needed for its own rate function, and the recovery/Gamma-limit argument assumes the central theorem rather than proving it.
