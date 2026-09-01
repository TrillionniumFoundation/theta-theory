# Independent Referee Report — Round 15

**Manuscript:** A3 — *Full Empirical-Path LDP*  
**Submitted revision branch:** `revision/round15-referee-positive-closure-11paper-2026-09-01`  
**Locked branch commit:** `e25e565cc15ae65693c87eda37fd3a1f29357ecd`  
**Locked tree:** `d3c54fc19f0881ce3d38253f62ca3215fbf5000c`  
**Actual controlling module at review lock:** `ROUND14_POSITIVE_CLOSURE.tex`  
**Recoverable registered Round-Fifteen candidate:** `A3_PREDICTABLE_STOPPED_RENEWAL_LDP.tex` from the truncated checksum-pinned payload  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*  
**Recommendation:** **Reject**

## Evidence boundary

The submitted manuscript still loads Round Fourteen. The complete A3 candidate was recoverable from the truncated Round-Fifteen payload and is reviewed below as supplemental evidence. It was not materialized or built in the submitted tree.

## Executive assessment

The candidate correctly enlarges the control class from stationary/current-state kernels to arbitrary predictable kernels and explicitly retains the terminal branch. This repairs an important prior objection. The proposed rate then undercharges that terminal branch: the exact path likelihood pays the full branch-selection entropy, whereas the declared terminal cost multiplies the full branch log weight by the observed fraction of the branch. The stopped control formula and the rate formula are therefore inconsistent.

The later full LDP, physical-clock contraction, and recession claims also rely on unproved stationary relaxation and recovery statements on a highly nonstandard compactification.

## Decisive objections

### 1. The terminal likelihood is paid in full, not proportionally to the prefix length

The candidate's exact entropy identity disintegrates the law of the branch sequence. Once the terminal branch \(a\) is selected, its conditional likelihood contribution is

\[
-\log w(a\mid\xi)
\]

in full. Cutting the realized trajectory after a fraction \(u\in(0,1)\) of that branch does not retroactively reduce the probability with which the branch was selected.

The manuscript instead defines

\[
J_c^{\rm term}(\rho)
=
\liminf
\frac{-\log w(a\mid\xi)}{r(a)}\,u_a.
\]

Here \(u_a\) is declared to be the terminal fraction. This charges only a fraction of the branch log likelihood. It contradicts the chain-rule entropy sum in the preceding theorem.

There are only two coherent alternatives:

- if the state reveals the full branch label—as it does through \(\iota_c(a)\)—charge the full branch entropy;
- if the state reveals only the prefix, integrate over all legal completions and charge the negative log probability of the prefix event.

The displayed fractional cost is neither.

### 2. The rate formula double-types the terminal coordinate

The stopped state stores the entire \(\iota_c(a)\) and the pointed prefix. Thus the terminal coordinate already reveals the branch length and full normalized branch profile. It is not merely a partially observed prefix. The rate must be the contraction of the exact full-branch entropy under this explicit state map.

Instead, the proof alternates between “the last branch is sampled and counted exactly once” and “the prefix pays only its clock fraction.” The claimed exact reconstruction set \(\mathfrak R_c(z)\) is not defined sufficiently to resolve this conflict.

### 3. Finite-memory entropy approximation does not automatically preserve legality and irreducibility

The proof replaces the full conditional law by its conditional expectation on the last \(k\) symbols and adds an \(arepsilon\)-fraction of a reference connector. For a countable constrained shift, that operation need not preserve the correct source vertex, legal adjacency, invariant marginal, or prescribed excursion/profile moments. A new finite-memory kernel can create transitions absent from the original conditioning class.

A complete approximation theorem must be stated on the edge shift, with balancing corrections and quantitative entropy/moment convergence.

### 4. The compact stopped-state space is not constructed

The text declares that a compactification by inverse length and local Skorokhod graph topology is compact “after the exponential moment weight is imposed.” Moment bounds give tightness of probability laws; they do not make the underlying state space compact. The recession points, singular germs, source/target vertices, profile normalization, and terminal prefix topology require an explicit metric and a proof of closedness.

The phrase “actual recession profiles of legal return branches” is a restriction on the boundary that itself needs a characterization and recovery theorem.

### 5. The lower bound is largely the theorem restated

The proof says: generate a typical controlled word, insert actual long branches at prescribed scales, use connectors of sublinear total cost, and diagonalize. This leaves open:

- simultaneous realization of edge-flow and all profile coordinates;
- interaction among multiple mesoscopic scales;
- stationarity and endpoint balance after insertions;
- uniform control of singular exposure;
- density of the chosen recovery class in the declared rate domain; and
- physical-time inversion for sequences with macroscopic terminal branches.

These are the hard parts of the full LDP.

### 6. A3 still depends on A2's missing coefficient/spectral theorem

The path law, exponential mark moments, graph completion, and physical-clock regularity are taken from A2. Since A2's unsmoothed joint Fourier theorem and common induced bundle are not proved, A3 cannot use them as closed interfaces.

## Required reconstruction

Define the stopped state as an explicit measurable image of the full branch sequence and define its rate by contraction of the exact predictable relative entropy. In particular, derive the terminal cost rather than postulating it. Then prove a separate stationary/defective relaxation theorem and a recovery construction for every component of the state.

## Recommendation

**Reject.** The candidate corrects the control class but assigns the terminal branch a cost inconsistent with its own exact entropy chain rule. The full stopped and physical-time LDPs therefore remain unproved.
