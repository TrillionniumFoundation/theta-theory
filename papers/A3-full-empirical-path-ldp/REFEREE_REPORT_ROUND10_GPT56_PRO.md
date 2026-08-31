# Independent Referee Report — Round Ten (GPT-5.6 Pro)

**Manuscript:** A3 — Full Empirical-Path LDP  
**Reviewed revision:** `revision/round10-referee-positive-closure-11paper-2026-08-31@b45406b03ab45e70461d36da5d3ee64892a92c8f`  
**Controlling mathematical commit:** `101dc123e4bafbb8e140e658ac1390f7735dc67e`  
**Registered module SHA-256:** `a09b122092f38c0b7c4ef84ad03462611621f2eb887cc06528dbbd8a11ab3d69`  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *JAMS*  
**Recommendation:** **Reject.**

## Executive assessment

Round ten fixes two important conceptual errors. The initial empirical flow is now indexed by the deterministic excursion count \(N\), and the state retains actual branch labels, edges, clocks, and excursion profiles. The manuscript also stops claiming that a convex recession profile must be realized by one first-return branch.

The replacement proof does not establish the advertised LDP. Collapsing all excursions outside a finite core to a cemetery mark does not produce a finite Markov chain unless a strong lumpability condition holds. The finite-core rate is therefore not obtained from the finite Perron matrix written in the proof. The recession functional is introduced without a precise normalization or probability family, and the final rate simply adds an excursion-count rate to a clock-speed recession rate without a joint mixed-speed LDP. These gaps remain at the exact points where the deterministic path theorem is supposed to be proved.

## Major mathematical objections

### 1. The cemetery projection is not a finite-state Markov factor

The manuscript keeps edges inside \(\mathcal A_L\) and sends every other edge to one “marked cemetery state.” A countable Markov/Gibbs process projected in this way is generally a hidden Markov process, not a Markov chain on the finite quotient. Transitions out of the cemetery depend on which omitted branch was actually visited, and the omitted branches carry different roof lengths, potentials, profiles, and return destinations.

A simple countable-state example already shows the issue: two hidden states identified as one cemetery state can have different probabilities of returning to two visible states. The projected next-step law then depends on the hidden state and is not determined by the cemetery label.

Consequently the statement

> “On the finite core, the transfer matrix with cylinder sources is a positive finite matrix”

is false for the projected full process unless the authors prove lumpability or retain enough hidden information to make the quotient Markov. If all omitted marks and transition information are retained, the state is no longer finite.

### 2. The finite-core rate formula is not derived from the actual projected laws

Because the quotient is not finite Markov, its empirical edge-flow rate is not simply

\[
D(q_\lambda\Vert q_\phi\mid\lambda_1).
\]

Even for a genuine finite Markov chain this formula requires a correctly normalized transition kernel, initial effects, and a precise convention for forbidden edges. For the current hidden-state projection, the rate contains the cost of the unresolved excursions and their return distribution. Calling the cemetery weight “retained” does not determine that cost.

The asserted exact consistency

\[
I_L=\inf_{\pi_{L,L'}\lambda'=\lambda}I_{L'}
\]

would follow if all \(I_L\) were already the contraction rates of one established full LDP. It cannot be used to prove that full LDP when the finite rates were obtained from unrelated truncated matrices.

### 3. Exponential tightness in the declared weighted profile topology is not proved

An exponential moment for the scalar return length does not automatically give exponential tightness of the realized excursion profile near iterated billiard singularities. The “singularity shield” is cited but no uniform exponentially good approximation is stated or proved in this paper. The negative part of the Gibbs potential, the path-window complexity, and the roof/profile marks must be controlled jointly.

This is the load-bearing billiard-specific compactness theorem, not a consequence of weighted Prokhorov compactness after the moment bound is assumed.

### 4. The recession functional has no mathematically specified speed

The text conditions \(M\) consecutive excursions to have total collision clock at least \(L\), speaks of “finite-window logarithmic costs,” and then takes \(L\to\infty\) and \(M\to\infty\). It never defines whether the cost is divided by \(L\), by the realized total clock, by \(M\), or by another deterministic sequence.

Without a normalization, Fekete's lemma has no object to act on and \(J_\infty\) is not a rate function. Quasi-Bernoulli/Gibbs concatenation would in any case give subadditivity only up to distortion and connector errors that must be quantified in the same normalization.

### 5. The final action adds rates living at different speeds

The excursion empirical flow \(I_{\rm e}\) is a speed-\(N\) rate. The proposed recession cost is intended to be a collision-clock rate. The main theorem then writes

\[
I_{\rm e}(\lambda)+J_\infty(\zeta)
\]

without the proportions converting excursion count, recurrent clock, recession clock, and physical time to one common deterministic speed. There is no joint LDP proving additivity, no independence, and no infimal-convolution formula derived from the same microscopic trajectory.

A recurrent block and a macroscopic excursion are not separate random samples. Their costs and connector probabilities are coupled by the underlying Gibbs path law.

### 6. The terminal-excursion lemma contradicts the finite-rate one-big-excursion mechanism

The lemma says that the terminal cut has negligible normalized path mass, while also acknowledging that a macroscopic terminal excursion has a finite recession cost. On the event that the very first or last excursion has length comparable with the deterministic horizon, the cut profile can carry order-one empirical mass. Its probability is typically \(e^{-c n}\), so it is part of the finite-rate lower bound, not an exponentially negligible perturbation.

Representing the cost somewhere in \(J_\infty\) does not make clock inversion an exponentially good continuous map; the pointed partial-excursion state and its joint rate must be present before contraction.

### 7. The lower-bound construction is only a proof sketch

Balancing a truncated countable flow with a fixed connector circulation can change entropy, potential, period, and clock moments. The paper gives no quantitative entropy-density theorem, no control of connectors for all retained vertices, and no construction of a microscopic Gibbs tilt concentrating on the proposed recovered flow. The difficult lower bound is summarized in a paragraph.

## Dependency and editorial assessment

A3 remains the principal upstream obstruction for A4, C2, and the Sinai component of D1. It also depends on A2's unproved local-limit packet. Neither documentary consistency nor a projective notation can replace the missing finite-projection and mixed-clock theorems.

A viable paper would first prove a genuine finite-coordinate LDP for the countable inducing process without an invalid cemetery Markovization, then formulate a deterministic-clock recession-inclusive state and prove one joint lower bound. The current manuscript is a research plan.

## Recommendation

**Reject.** The finite-core theorem is based on a non-Markov quotient, the recession rate is not defined with a speed, and the main contraction adds incompatible rate scales without a joint LDP.
