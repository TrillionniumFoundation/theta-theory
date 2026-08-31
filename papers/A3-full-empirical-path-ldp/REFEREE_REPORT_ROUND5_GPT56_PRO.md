# Round-Five Independent Referee Report — GPT-5.6 Pro

**Manuscript:** A3 — *Full Empirical-Path Large Deviations for Periodic Sinai Billiards*  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*  
**Recommendation:** **Reject**  
**Reviewed revision branch:** `revision/round5-referee-positive-closure-11paper-2026-08-31`  
**Reviewed branch head:** `557c88ef447ab8c693b11e1c072efe97b4452556`  
**Active controlling module:** `ROUND3_POSITIVE_CLOSURE.tex`, blob `9b0d466b25fcf1cfdee29a35062d337a4c16e3d2`  
**Unmaterialized round-five candidate:** `revision/round5-referee-final/A3_RECESSION_COMPLETE_PATH_LDP.tex`, blob `583a97d0743629152336b8a7bc67dc472bcc9df7`

## Source-control verdict

The active A3 manuscript is unchanged from round four. Its lower-bound proof still attempts to approximate general positive-entropy survivor phases by periodic orbit measures while preserving the rate. Since periodic measures have zero entropy, that argument is invalid and the claimed full LDP is not proved.

The round-five packet is not included by `main.tex` or by the controlling module. The repository materializer failed before installing any final packet. I therefore treat the packet only as a proposed repair. It abandons periodic approximation and introduces finite-state Markov approximants, which is directionally sensible, but it does not solve the recession/escape or countable-state lower-bound problem.

## Audit of the proposed round-five replacement

### 1. The state space still cannot retain a macroscopic recession fraction

The packet says that a nonzero recession fraction of long excursions is retained by states with increasing return level in a weighted topology. This is not correct for the declared space of ordinary invariant probability measures with finite

\[
\nu(W),\qquad W=1+r+|k|.
\]

If a fixed positive mass moves to symbols with return level tending to infinity, its `W`-moment diverges. If the moment is kept finite, that mass must tend to zero. In either case an ordinary weak limit on the countable graph does not retain a macroscopic excursion carrying order-one collision-time mass.

A recession-complete theorem needs an explicit defect/cemetery coordinate, a compactification at infinity, or a homogeneous measure recording escaped clock mass. Merely strengthening the topology by a moment does the opposite: it rules out the intended escaping mass. Thus the headline claim that the rate includes laws with a nonzero recession fraction is incompatible with the declared phase space.

### 2. The finite-state Markov approximation generally creates forbidden transitions

The construction takes finite block conditional probabilities and replaces zero transitions by

\[
\delta_m e^{-W(B')}
\]

before renormalizing. On a symbolic graph, a zero transition can mean that the edge is dynamically forbidden, not merely absent under the particular measure. Adding a positive probability then produces words outside the billiard code. The statement that the same construction stays inside the survivor subgraph is especially unsupported.

One must add mass only along admissible connector paths and track the extra symbols, clock, potential, and entropy. That was precisely the difficult issue in earlier connector approximations. The present formula does not define an invariant law on the original graph in general.

### 3. Entropy convergence is asserted without the required countable-alphabet hypotheses

For a countable graph, convergence of finite conditional entropies does not by itself give

\[
h(\nu_m)\to h(\nu).
\]

Uniform integrability of information functions and control of tail conditional probabilities are required. Finite `W`-moment need not control `-\log p(a|\text{past})`. The tail atom may carry very small transition probabilities and non-negligible entropy. The claimed `O(delta_m |log delta_m|)` error ignores the number and weights of newly introduced states and transitions.

Consequently the central rate-density lemma—the sole bridge from exposed Markov phases to every finite-rate law—is not proved.

### 4. Quasi-compactness of the full survivor operator does not follow from the stated norm

The packet uses a single weighted variation norm and says that the weighted supremum tail is compact. A bounded set in a weighted supremum space is not compact merely because the alphabet weights grow. One needs a strong/weak pair with a genuine vanishing-tail property or an explicit compact embedding, together with a Lasota–Yorke inequality for the survivor operator.

No proof is given that the survivor graph has the required recurrence, finite pressure, simple leading eigenvalues, or spectral gaps on all relevant components. Therefore the analytic survivor phases and the pressure maximum formula remain unproved.

### 5. The recurrent–survivor decomposition is not shown to cover all collision paths at the claimed exponential precision

The operator factorization separates paths that return to one chosen magnet from paths that never hit it. It does not automatically describe paths with a single return after a macroscopic initial segment, arbitrarily sparse returns, or sequences whose return frequency tends to zero. Entrance and exit series must be controlled up to the same critical abscissa as both competing branches. The proof simply states this analyticity from an exponential return estimate, which is exactly what fails in the recession regime.

### 6. The explicit entropy/free-energy formula is not established

The candidate declares

\[
I_R^c(\nu)=Q_R^c(0)-h_\nu(\Theta)-\nu(\Phi_{R,0})
\]

for every invariant finite-weight law. On a countable, singular graph this formula requires a complete variational principle, upper semicontinuity or controlled approximation of entropy, and identification of the Gibbs reference potential. None follows from the formal pressure decomposition alone.

### 7. The singularity shield depends on the unproved direct pressure

The diagonal Chernoff argument is a useful correction to the earlier illegal large-source limit at fixed bad set. But its input estimate

\[
Q_R^c(sB_{q,\delta})-Q_R^c(0)
\le C e^{c_0s}(e^{-c_1q}+q^C\delta^\alpha)
\]

is itself a substantial source-uniform theorem for the direct recurrent/survivor pressure. It is stated without derivation from the proposed operator spaces.

### 8. The physical-time theorem is downstream of the missing collision LDP

The bounded one-flight roof makes collision-to-physical contraction much more plausible than the old unbounded renewal argument. Nevertheless it cannot repair the missing collision-time lower bound or recession state space.

## Genuine improvement

The candidate correctly rejects periodic orbit measures as entropy-preserving approximants and recognizes that a one-big-excursion sector cannot be discarded at superexponential cost. Those are important conceptual corrections. The proposed replacement still lacks a state space capable of carrying the recession mass and a valid rate-dense approximation theorem.

## Required reconstruction

The authors must first define a recession-completed collision phase space, prove the recurrent/open survivor spectral theory on explicit strong/weak spaces, and construct admissible Markov approximants without adding forbidden edges. Entropy and free-energy convergence must be established quantitatively before a global lower bound can be claimed.

## Recommendation

**Reject.** The active manuscript retains a false lower-bound approximation. The unmaterialized candidate addresses the previous counterexample but does not represent escaped clock mass and does not prove the countable-state entropy-density or survivor spectral theorems needed for a full path LDP.