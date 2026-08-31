# Round-Nine Independent Referee Report — GPT-5.6 Pro

**Manuscript:** A3 — *Full Liouville Empirical-Path Large Deviations and Information Projections for Finite-Horizon Sinai Billiards*  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*  
**Recommendation:** **Reject**  
**Reviewed revision branch:** `revision/round9-referee-positive-closure-11paper-2026-08-31`  
**Payload-host branch head at review lock:** `a8c0c551f5f8614856a9d433e78b2eb92a5dcfa1`  
**Registered round-nine payload SHA-256:** `cf230322211332af59a7883af1b669eeb9b4f7e9f4220fc24712c634bda17716`  
**Reviewed registered source:** `revision/round9-referee-final/A3_POINTED_EDGE_FLOW_LDP.tex`  
**Reviewed source SHA-256:** `894e7cda305e4821ffdb1f2e939905c33fa06f43cfc6564c5343296b8726f6fa`  

## Evidence boundary

At the review lock, the branch stored the checksum-pinned round-nine payload while the paper-level `main.tex` files still loaded the round-eight modules; the repository publication workflow was queued. I independently verified the payload hash, unpacked it, and ran the repository materializer successfully, producing byte-identical paper-level `ROUND9_POSITIVE_CLOSURE.tex` files. This report therefore reviews the exact registered round-nine theorem text. It does not treat a queued workflow, a clean build, theorem/proof counts, or an internal hostile-regression script as evidence that the mathematical claims are true.

## Executive assessment

Round nine improves the state description by retaining inducing edges, actual excursion profiles, a return-step intensity, and a pointed terminal coordinate. It also correctly distinguishes recovery by one excursion from recovery by a mixture.

The proposed LDP is nevertheless not established. The theorem is indexed by a random “speed” \(R_N\), the finite-projection proof again discards one-big-excursion events as exponentially negligible at collision speed, and the recession and deterministic-time arguments rely on recoveries not supplied by the projective theorem. One of the stated renewal alternatives is false for positive-recurrent but non-strongly-positive-recurrent countable shifts.

## Major mathematical objections

### 1. “Speed \(R_N\)” is not a well-defined LDP speed

The law is indexed by the number \(N\) of completed excursions, while
\[
 R_N=\sum_{j<N}r(a_j)
\]
is random. An LDP speed is a deterministic sequence. A statement such as
\[
 \frac1{R_N}\log\mathbb P(\cdots)
\]
has no standard meaning without conditioning on \(R_N\), reindexing by a deterministic collision clock, or proving a random-speed equivalence theorem.

This is not notation: all upper and lower bounds, exponential tightness, and projective compatibility depend on which deterministic family of laws is being considered.

### 2. Return-length truncation is not exponentially good at collision speed

The proof of the finite marked-flow LDP truncates return length and says that exponential return tails make the truncation exponentially good. At collision speed this is false. The event
\[
 r(a_0)\ge \varepsilon R_N
\]
has probability of order \(e^{-c\varepsilon R_N}\), hence finite rate. It can carry an order-one fraction of the length-weighted profile.

This is precisely the one-big-excursion mechanism the boundary state is meant to retain. It cannot be removed before the finite projected LDP is proved. A correct finite theorem must include the escaped-clock/profile coordinates already at the truncation stage and calculate their finite cost.

### 3. A2 does not provide the source class invoked here

A2 concerns vector displacement and roof twists, plus fixed insertions. A finite family of edge/profile sources in A3 includes unbounded excursion-length weights and arbitrary bounded sums along an excursion. The paper gives no multiplier theorem placing all such decorated return operators on the A2 bundle with uniform spectral control.

Thus Theorem `r9-a3-finite` does not follow from A2 even if A2 were correct.

### 4. The projective lower-bound construction is not quantified

The proof selects finite-state recovery words for increasing projections and connects them by specification. To preserve the rate, one needs uniform control of:

- connector collision length and physical roof;
- connector Gibbs weight;
- period and communicating-class constraints;
- return-step intensity;
- singularity shielding; and
- the schedule \(m(N)\) relative to all tail errors.

None is supplied. On a countable graph, legal connectors can have unbounded length and cost, so “connector length is \(o(R_N)\)” is not automatic.

### 5. Extreme boundary recovery does not follow from Choquet separation

The projective theorem constructs empirical paths made of many excursions. It does not prove that an extreme point of the closed boundary rate domain is approximated at the same cost by a *single* first-return excursion. Extremality of a barycentric state can force concentration of representing measures under additional compactness, but it does not supply cost recovery for the original nonclosed set of actual excursions.

A separate \(\Gamma\)-convergence theorem for one-excursion laws is required. The definition of \(I_\infty\) does not prove the existence of its epigraph limit or the equality with the restriction of the full rate.

### 6. The stated SPR/recession dichotomy is false

There are irreducible positive-recurrent countable Markov shifts with an equilibrium probability and polynomial return tails that are not strongly positive recurrent. In such a component the tail-pressure gap vanishes, yet the normalized leading eigenvector/equilibrium law is tight.

Taking that actual eigenvector as an “approximate leading vector” contradicts alternative (ii), which says that every such family loses a positive fraction of clock mass outside every finite edge set. Positive recurrence, null recurrence, transience, and strong positive recurrence cannot be collapsed into the two alternatives stated.

### 7. The singularity shield again treats finite-rate long excursions as negligible

A macroscopic excursion can spend a positive collision fraction near deep singularity preimages at finite exponential cost. The displayed one-time neighborhood estimate does not yield a superexponential empirical-frequency shield uniformly over recession profiles. The proof must analyze singularity exposure inside the boundary excursion law rather than refer to a return tail that is finite-rate at the chosen speed.

### 8. The pointed state does not type the exact physical-time cut

The definition
\[
 K^{\rm pt}(a,y,u)
\]
uses a fraction of the *collision count*. Exact physical time depends on the accumulated continuous roof and on the age inside the final free flight. A normalized full-excursion profile and a collision fraction do not determine the prefix at a prescribed physical age.

The theorem later “cuts the following actual flight,” but the state does not contain the pointed roof path, the completed collision prefix, or a rate for this partial excursion. The deterministic-time contraction is therefore not defined.

## Dependency assessment

A3 remains an independent blocker after A2. A4 has no proved physical path law, recession rate, or conditional phase on which to build its history process. C2 and D1 likewise cannot use A3 as a completed global LDP interface.

## Required reconstruction

A valid approach should:

1. index the laws by deterministic collision or physical time;
2. include the boundary/recession coordinates in every finite truncation theorem;
3. prove a one-excursion epigraph recovery theorem separately from multi-block recovery;
4. use the full recurrence classification for countable components;
5. construct a pointed physical-roof prefix state; and
6. prove singularity shielding uniformly on recurrent and recession sectors.

## Recommendation

**Reject.** The headline full LDP is not proved, its speed is not correctly typed, and a central renewal dichotomy is false as stated.
