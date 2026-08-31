# Round-Eight Independent Referee Report — GPT-5.6 Pro

**Manuscript:** A3 — *Full Empirical-Path Large Deviations for Periodic Sinai Billiards*  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*  
**Recommendation:** **Reject**  
**Reviewed revision branch:** `revision/round8-referee-positive-closure-11paper-2026-08-31`  
**Reviewed branch head:** `ad2b5106678b29b7d9ffb3824f61ddbd141ac4b8`  
**Reviewed tree:** `00d7ef9edcddda26fc88962e206677f9b399bebe`  
**Active controlling module:** `ROUND8_POSITIVE_CLOSURE.tex`, blob `f0ea93f900feb5e94b5182a93cafb95f5fd9f309`

## Executive assessment

The round-eight state is better typed than its predecessors: it retains the actual inducing edge and the actual excursion profile, and it records escaped collision clock by bounded projective coordinates rather than an unbounded reciprocal moment. These are the correct kinds of variables.

The full LDP is nevertheless not proved. The manuscript begins by declaring finite-dimensional good rates `I_m` “obtained by exponential change of measure,” although neither A2 nor any argument in A3 establishes the required edge/profile pressure theorem. The projective diagonal construction produces long *blocks of many excursions*, but the recession theorem promotes that result to recovery by a *single long first-return excursion*. That implication is false. Several later statements—entropy approximation, the SPR dichotomy, and exact deterministic-time contraction—also require separate theorems not supplied here.

## Genuine repairs recognized

The revision correctly:

- retains edge labels and transition data rather than only branch-averaged profiles;
- uses actual excursion profiles instead of conditional branch averages;
- records escaped clock through bounded ledger coordinates;
- avoids inserting forbidden graph edges;
- distinguishes recurrent and recession sectors conceptually.

## Major mathematical objections

### 1. The finite-projection LDP is assumed at the first line where it is needed

The manuscript writes:

> Let `I_m` be the good finite-dimensional rate obtained by the exponential change of measure on `pi_m Xi_N`.

This is not a definition that carries a theorem. The sources include arbitrary edge indicators and profile tests on a countable inducing system, with random collision-time normalization and possible long-excursion escape. A2 proves, at most, a vector homology/roof spectral packet; it does not prove a coefficient theorem for this growing family of edge/profile sources.

The consistency identity

\[
I_m(z)=\inf\{I_{m+1}(z'): \pi_mz'=z\}
\]

is also asserted rather than derived from compatible finite-dimensional LDPs. Consequently Theorem `r8-a3-projective` assumes the primary content of the paper.

### 2. Projective block recovery does not yield one-excursion recession recovery

The proof of the projective theorem constructs a diagonal infinite path by concatenating finite admissible *blocks*. A block can contain many first-return excursions and can realize a convex mixture of several profiles.

The recession theorem then claims that every finite-rate boundary profile is approached by “actual long first-return excursions.” That does not follow. A boundary state such as

\[
z=\tfrac12 z_1+\tfrac12 z_2
\]

may be realized by alternating long excursions of two incompatible types. The projective block is valid, but no individual first-return branch need have profile near the mixture `z`.

The text itself later says that convex combinations are realized by consecutive long excursions and explicitly declines to call their concatenation one first-return word. This contradicts the theorem's preceding single-excursion recovery claim.

### 3. The recession duality interchanges projective limits and conjugacy without proof

The functional

\[
I_{\rm rec}=\sup_m I_m^{\rm boundary}
\]

is declared to equal the conjugate of a cylinder pressure. In general, a supremum of finite-dimensional conjugates is the projective rate only after compatibility, exponential tightness, and a full lower bound are established. It need not equal the conjugate of a naively defined limiting pressure, and exposed finite projections need not admit a common recovering sequence.

The sentence “the cylinder dual determines the projective supremum by separation” does not prove the minimax/interchange or the attainment needed for the advertised actual-excursion theorem.

### 4. The state still does not automatically determine the recurrent entropy at the boundary

On finite edges, a length-weighted edge flow can be converted to the unweighted return-step flow by dividing by the known return length and renormalizing. At the boundary, however, the return length diverges and that conversion loses the block frequency entirely. Different sequences can have the same escaped clock/profile coordinates but different numbers of blocks, connector entropy, and induced Gibbs weights.

The rate may assign the infimum over those hidden realizations, but then the claim that “the edge marginals determine the length-weighted entropy flow” needs a precise formula and lower-semicontinuous extension. None is given.

### 5. The stationary finite-core approximation theorem is too strong

The theorem claims approximation of every finite-rate countable stationary flow by flows on finite strongly connected subgraphs while retaining periods. If the original flow is a convex mixture of distinct closed communicating classes, one finite strongly connected graph cannot represent the mixture without adding connector circulation. Adding such circulation can change the period, and its entropy cost must be quantified.

Cycle truncation alone gives a finite union of cycles, not a strongly connected graph with the stated period and entropy properties.

### 6. The SPR/recession dichotomy is not established by uniform integrability

Strong positive recurrence is a precise renewal/spectral property. Uniform integrability of return lengths does not by itself give a quasicompact Ruelle operator or an isolated pole on the selected Banach space. Conversely, loss of an isolated pole need not force every approximate eigenvector to escape all finite edge sets; null-recurrent and essential-spectrum mechanisms require analysis.

The proof replaces this analysis with two sentences. It cannot support the global division between recurrent spectral phases and recession phases.

### 7. The deterministic terminal cut requires a new marked rate

The terminal coordinate

\[
(a_*,u_*,K_*^{\rm cut})
\]

is introduced only in the last subsection. It is not part of `Xi_N`, its finite-dimensional pressures are not constructed, and no rate is assigned to the cut profile. The profile of an initial fraction of a long excursion is not determined by the full-excursion profile; two excursions with the same full occupation can have very different prefixes.

Hence an order-`T` terminal excursion is not automatically “already represented by the recession sector.” A separate pointed/partial-excursion compactification and recovery theorem are required.

### 8. Singularity shielding and physical coding are missing from the Round-8 module

The previous versions at least stated a singularity-shield estimate before applying path-space contraction. The present controlling module invokes actual collision profiles and a final path contraction but gives no exponentially good continuous approximation through grazing and iterated singularity sets. This remains a necessary billiard-specific interface.

## Dependency assessment

A3 is still not a proved parent path LDP. A4 cannot use it for compact past kernels or recurrence phases, and C2/D1 cannot use it as a completed universal path-rate interface. The projective labels in this paper do not repair A2's unresolved source theorem.

## Required reconstruction

A viable theorem must:

1. prove the finite edge/profile LDPs rather than name them;
2. define a boundary state rich enough to retain the cost and frequency data lost at infinite return length;
3. distinguish recovery by one long excursion from recovery by a mixture of excursions;
4. prove the appropriate projective epigraph theorem with a common recovery sequence;
5. establish the SPR/non-SPR spectral alternatives on specified spaces; and
6. include pointed terminal excursions and singularity shielding before contracting to deterministic physical time.

## Recommendation

**Reject.** The state design has improved, but the paper's main lower bound is still inserted as a finite-dimensional premise, and the central recession theorem makes an invalid jump from multi-excursion block recovery to single-excursion recovery.