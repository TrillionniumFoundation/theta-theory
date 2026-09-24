# Response to the eighth independent external report

**General Theta Foundations I, revision 25**  
**Controlled Experiment Duality and Exact Marked Minimax Laws**  
Qian Qi · 24 September 2026

Controlling report: `reviews/general-theta-foundations-i-v24-external-harsh-top4-r8-2026-09-24/REFEREE_REPORT.md`, frozen at `c5c1a0d64f830bc3f036292357d8bbe2dbd04ca6`. Reviewed v24 manuscript: `ad1336e48e414b2c01e928b844c796ab4765178b`. The revision branch descends from the controlling review, not from an earlier manuscript. The final source-build commit and executed evidence are recorded in `evidence/BUILD_RECEIPT.json` after a successful build.

## 1. The mathematical response

The report correctly distinguishes the genuine v24 preparation theorem from the still-unsolved optimal score and low-width problems. We have not answered it by relabeling the same rational certificate, increasing diagnostic counts, deleting the physical application, or treating the common-dominating-row hypothesis as innocuous. The new revision takes two of the report's suggested theorem-level routes: an exact minimax solution and a controlled-action extension.

First, the one-preparation optimization is now solved. For the original marked target,

\[
U_1(b,Q_*)=\frac{85-7\sqrt{73}}{64}=0.393624590355895\ldots.
\]

This is an equality with an explicit optimal response and a two-point least-favorable prior, not a new nonmatching upper bound. The calculation extends to a continuous family of target mark biases `0 <= gamma <= 1-1/sqrt(2)`. Writing

\[
u_\gamma=\gamma-2+\sqrt{\gamma^2-2\gamma+5},\qquad
\tau_\gamma=\frac{2u_\gamma}{u_\gamma+2-\gamma},
\]

the exact value is `(3+u_gamma^2)/8`. The uniform optimality proof is the identity

\[
G_\gamma(p,q)-\frac{3+u_\gamma^2}{8}
=\frac{2-\tau_\gamma}{16}
\left(((p+q-1)^2-(p-q)^2-u_\gamma)^2+4(p-q)^2\right).
\]

The matching prior puts equal mass at `(t_gamma,t_gamma)` and `(1-t_gamma,1-t_gamma)`, where `t_gamma=(1-sqrt(u_gamma))/2`. The proof checks every coordinate of the full marked-word dual; it does not assume that arbitrary competitors are symmetric or count-based. The interval endpoint comes from the sign of the posterior coefficient for a mixed training pair. The zero-preparation endpoint is also computed exactly.

Second, the outer dual now retains genuine informative action choice. A finite controlled action family, a compact parameter space, a finite legal protocol and stopping are permitted without any common dominating action. The value is the minimum over one initial prior of an unnormalized posterior Bellman value. The parameter remains fixed along the execution; the prior is not reselected after an observation. Finite policy-tree minimax, attainment, null-history handling, supersolution certificates, finite-support reduction and causal perturbation bounds are proved. An explicit four-parameter experiment has adaptive value `3/4` and nonadaptive value `5/8`; its advantage survives full-support report noise.

Third, the physical bridge is now local. The current article gives the private simulator kernels, feedback pushforward, positive-volume preparation boxes, collision-time and outgoing-signal estimates, Gaussian sensor windows and the actual-mark coupling proving `TV(Q_d,sigma,Q*)<1/300`. The physical headline no longer asks the reader to recover these lemmas from an unpublished 649-page companion.

Finally, a separate revelation family has an exact joint preparation/decision-memory law for all horizons and a parametric range of widths:

\[
V_N^{\rm er}(K)=(1-(1-\alpha)^N)(1-1/K).
\]

This yields exact strict thresholds and matching sample and memory scales. Its memory coordinate is explicitly a decision-cut width. It is not substituted for the unresolved bit-level collision peak frontier.

## 2. Response to the specific mathematical requests

### 17.1. A genuine joint preparation–memory obstruction

The new joint-law section proves a matched preparation/decision-memory theorem for the revelation family, including a converse for arbitrary stochastic encoders and stopping and a `K`-state matching training machine. Its converse uses the parameter-independent all-erasure component and the convex geometry of the residual decision channel. The machine overwrites a random initial group label on a revelation and needs no hidden revelation flag. The full atomic-outcome validation peak is charged separately.

For the original collision task at threshold `2/5`, the least bit-level peak at two training preparations and the values at widths `3..11` are **not determined by this revision**. The new theorem is not labeled a solution of that problem. Instead, the revision also supplies the exact marked-family minimax solution and controlled-action theorem explicitly proposed as alternative decisive routes in §20 of the report. The physical target and its unresolved width question are preserved, not replaced or removed.

### 17.2. Solve one minimax value exactly

**Resolved for `U1`, and generalized to a continuous marked-target family.** See `marked-minimax.tex`, Theorem `thm:marked-exact`, Corollary `cor:exact-one`, and identity `eq:marked-sos`. The least-favorable prior and optimal response match. The upper argument optimizes all marked training histories, while the lower argument is a polynomial identity on the full `(p,q)` square. The exact result strengthens the physical lower endpoint from the old rational `u1` to `u_ex` in Corollary `cor:improved-physical`.

`U2` remains unevaluated. The two-preparation selector's score is still proved exactly for that selector and is not relabeled as the global two-preparation optimum.

### 17.3. Extend the outer dual beyond a single dominating experiment

**Resolved for the explicitly stated finite-action, finite-horizon controlled class with compact parameter space.** See `controlled-dual.tex`, Theorem `thm:controlled`. Available actions need not be comparable. The theorem keeps action optimization inside the recursion and one adversarial prior outside it. It handles legal protocol states, branch-dependent continuation, stopping and zero-mass histories. It gives upper certificates for every memory-constrained architecture implementing the same protocol, not just one fixed graph.

The equality is for unrestricted memory. The finite-state constrained game is not convexified for free, and the theorem is not presented as an exact generic width-`K` recursion. The proof explicitly distinguishes Bayes-optimal trees from the saddle mixture which realizes a minimax value. The strict adaptive example and its full-support perturbation make the absence of dominance operative rather than merely formal.

### 17.4. Prove a scaling law

**Resolved in the revelation family.** The exact identity gives the deficit

\[
1-V_N^{\rm er}(K)=q+(1-q)/K,\qquad q=(1-\alpha)^N.
\]

Thus an error at most `epsilon` requires both `K>=1/epsilon` and `N>=log(1/epsilon)/[-log(1-alpha)]`; choosing the corresponding bounds with `2/epsilon` suffices when the declared alphabet admits that width. Exact strict-threshold rounding is included, so a real equality boundary is not silently converted into a strict integer guarantee. This is not a claimed autonomous time–precision law or a collision asymptotic theorem.

### 17.5. Make the physical bridge self-contained

**Resolved for every physical fact used in the preparation theorem.** See `physical-bridge.tex`, Definition `def:physical-class`, Lemma `lem:local-scattering`, and Theorem `thm:local-physical`. The same boxes, actual conserved mark, positive noise and feedback acquisition model are retained. Both facts previously delegated to the companion are now proved locally: all-on product characterization for every private width-one candidate, and a legal common-garbling subfamily for the converse. The sensor-window coupling proves the required total variation estimate uniformly on the stated physical parameter interval.

The broader Gaussian/entropic and historical conditional-process developments remain in the preserved companion; they are not invoked to justify the present physical headline.

### 17.6. Finish or sharply delimit the filtered-experiment comparison

**The originality boundary is explicitly delimited; full Norberg proof-level comparison is not claimed.** We verified the accessible bibliographic boundary but did not obtain the original full proof. The current paper therefore makes no non-overlap claim for general filtered comparison. The claims submitted for assessment are its explicit marked minimax saddle points, their certificate and physical use, and its precisely formulated controlled validation theorem and resource realizations.

The finite-horizon belief recursion is now expressly related to Smallwood–Sondik. Minimax, positive-part testing, finite policy trees and the general piecewise-linear belief-value mechanism are not claimed as new inventions. Hellman–Cover remains the attribution for the stationary autonomous optimum. The May 2026 Managoli–Prabhakaran paper is retained with its distinct adversarial and stationary scope.

## 3. Secondary requests

### 18.1. Formal physical architecture class

Definition `def:physical-class` locally specifies legal training and validation, conditional reset independence, the order of observed report bits and actual mark, legal within-preparation gates, frozen row/event timing, stopping, independent randomization, target calibration, clock conventions and every charged register component. The simulator's width-one constraint is distinguished from the auditor's width. The lower-bound subfamily is stated as a subfamily; it is not used to narrow the construction's candidate class.

### 18.2. Abstract versus collision specialization

The controlled theorem is stated before the collision model. The marked minimax theorem is finite-alphabet continuous-parameter mathematics. The collision bridge is a separate local section. The preparation corollary combines their hypotheses. The revelation theorem uses its own atomic observation and decision-width conventions. The introduction, theorem captions and resource ledger maintain these distinctions.

### 18.3. Origin of the four-point rational prior

The old rational prior is retained as an explicit analytically verified certificate. We do not invent a structural discovery history for its four rational support points. Its nonoptimality is now resolved by a different, proved least-favorable two-point prior. The response-coefficient tie and the uniform stationarity condition derive the new prior and randomization together. The old rational table remains useful when an entirely rational certificate is desired.

### 18.4. Conceptual explanation of the five events

The exact one-preparation saddle point randomizes between precisely the same five event masks used by the deterministic two-preparation rule. The tied posterior coefficient explains which coordinate may be randomized, and the square identity fixes its optimal probability. This supplies a structural interpretation of the event alphabet without asserting optimality of the two-preparation count selector.

### 18.5. Finite checks subordinate to proof

The proof is the displayed identity, coefficient-sign analysis, policy-tree minimax argument, channel converse and physical coupling. `verify.py` independently reconstructs the exact symbolic identity, the old rational certificate, the finite adaptive example and small channel instances. Both ordinary and optimized Python executions must agree; deliberately false identities and inherited controls must fail. Counts in the build receipt are reproducibility evidence, not proof certification or a novelty metric.

### 18.6. Preserve the focused journal architecture

The current canonical article retains the substantive v24 sections and inserts the new proofs; it does not revert to a cumulative 96-page canonical manuscript. Its page count is recorded only after compilation. The unaltered v24 complete mathematical manuscript and development are appended in separate full volumes, with every appended page checked for identical extracted text and raster samples. No predecessor repository path is edited or deleted.

## 4. Updated exactness and dependency ledger

The exact statements are now: the one-preparation marked minimax value and optimizing pair on the stated continuous target interval; the unrestricted controlled finite-horizon dual; the joint preparation/decision-memory value in the revelation family; and the physical minimum preparation count for the declared high-width threshold segment. The original physical bit-level width optimum, global `U2`, generic constrained-width controlled recursion and matching autonomous finite-time/precision law remain different obligations.

The new physical theorem genuinely uses the statistical root: actual preparation gives a likelihood, a fixed prior gives predictive continuations, the exact dual gives a preparation obstruction, and a compatible residual machine gives the matching construction. The controlled theorem expands that root beyond post-processing control. Neither argument makes the independent A2 geometric proof depend on it. The historical B4 and broad C2 aggregate obligations and the eleven-paper program are preserved without a false closure claim.

The report's editorial judgment is not treated as a theorem that can be overturned by metadata. This revision supplies new mathematical arguments for a fresh independent assessment; it does not certify its own journal acceptance.
