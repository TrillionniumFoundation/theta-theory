# Referee Report — General Theta Foundations I, Revision 35

**Manuscript:** *General Theta Foundations I: Sharp Width of Hidden Rotation Experiments*  
**Repository:** `TrillionniumFoundation/theta-theory`  
**Reviewed branch:** `revision/general-theta-foundations-i-v35-referee-ready-2026-09-25`  
**Reviewed head:** `aabc0731a0c913f7b9e75e6efc08f7af665bdf23`  
**Native mathematical source recorded by the manuscript:** `0ae43a2180d07bda18384697a33da48d3fc1562a`  
**Controlling previous report:** `6016075083626f7c94cfb07912c49fa256fcf9e0`  
**Previous reviewed manuscript:** `47bc47e5995e4b1b99a18aaa472a1309f1668f40`  
**Review branch:** `review/general-theta-foundations-i-v35-sharp-memory-pipeline-harsh-top4-r20-2026-09-25`  
**Date:** 25 September 2026

## Recommendation

**Reject at the Annals / Inventiones / JAMS / Acta level.**

Revision 35 is a substantial mathematical advance over Revision 34. The authors have answered the preceding report's central quantitative objection: for every fixed badly approximable rotation angle and every fixed row-total-variation tolerance below `1/20`, the unrestricted hidden-state width is now proved to have order `N^(1/3)`. The lower bound allows arbitrary hidden states, arbitrary time-dependent stochastic rows, unobservable directions, and a new machine for each horizon. It matches the inherited resonant-polygon construction without imposing a vector-state restriction.

I did not find a short fatal counterexample to the fixed-binary-command cube-root theorem. The separated-packet test law, endpoint compression lemma, terminal calibration, disjoint-packet occupation argument, badly-approximable separation estimate, and resonant exact upper construction appear internally coherent in the clocked atomic stochastic-row model actually defined. The negative recommendation is therefore **not** based on an allegation that the headline theorem is false.

The paper nevertheless does not meet the standard of the four leading general mathematics journals.

1. The sharp theorem is confined to one specially engineered planar rotation experiment, badly approximable angles, fixed signal, fixed error, one terminal coordinate query, and a highly nonuniform resource model. It is a strong specialist theorem, not a general theory of hidden causal memory.
2. The packet lower bound is elegant, but its main mechanism is a finite-orbit `k`-center quantization inequality combined with a width-dependent adversarial input distribution. Once formulated, the proof is short and elementary. The article does not derive a structural classification of stochastic programs, a general finite-alphabet representation theorem, or a broad complexity dichotomy.
3. The representation-valued packet theorem has a formal quantifier mismatch as written. Lemma `lem:packet` assumes that the endpoint kernel depends on a packet only through its group product `G`, while Theorem `thm:group-budget` allows the machine to process the full command word and hence distinguish two words with the same product. The desired inequality can apparently be repaired by formulating the lemma with an independent packet word `W` and action `U_{g(W)}`, but the present theorem is not literally a consequence of the stated lemma.
4. The priority audit still omits a directly adjacent 2026 literature on exact classical simulation of quantum finite automata. The manuscript's prepare--rotate--query architecture is close enough to constant-dimensional unitary/quantum automata that the sharp PFA-simulation results of Chen--Wu and the recent irrational-phase world-model separation of Lumbreras--Ma--Thompson--Gu require theorem-level comparison.
5. The `SO(d)` theorem changes the model radically: every exact real rotation matrix is an atomic external command and a complete Borel row table is free. Its exponent is driven by classical sphere quantization and covering. It is not a finite-alphabet generalization of the headline theorem and should not carry substantial weight in the four-journal case.
6. The resource measure remains permissive. The epoch, horizon-specific machine, row tables, arithmetic, and exact real sampling are free; only persistent labels are counted; and only one final query is answered. The resulting `(\log N)/3+O(1)` label-bit statement is not a conventional uniform-space theorem.
7. The repository-wide Foundations pipeline is still unchanged at every difficult analytic gate. The manuscript itself leaves A2, B4, C2, the eleven-paper aggregate, fully adaptive collision scheduling, noisy-tag composition, and classification of all irrational angles unresolved.

Revision 35 could form the core of a serious specialist paper after a formal repair and a materially broader priority analysis. It should not continue to be presented as approaching the Annals/Inventiones/JAMS/Acta threshold, and the “General Theta Foundations I” branding remains unsupported by its relation to the larger repository program.

---

## 1. Scope of this review

I reviewed the focused Revision 35 article and the repository records needed to evaluate both its local mathematics and its place in the larger pipeline. In particular, I examined:

- `papers/GTF-I-v35-sharp-memory/main.tex`;
- `introduction.tex`;
- `machine-model.tex`;
- `packet-compression.tex`;
- `sharp-rotation.tex`;
- `compact-groups.tex`;
- `simulation-error.tex`;
- `literature-and-scope.tex`;
- `angular-lemma.tex`;
- `references.tex`;
- `RESPONSE_TO_REFEREE.md`;
- `LITERATURE_AUDIT.md`;
- `HISTORY_AUDIT.md`;
- `RESOURCE_LEDGER.md`;
- `PROOF_STATUS.json`;
- `PIPELINE_STATUS.json`;
- `verify.py` and the executed build records;
- the complete nineteenth referee report;
- the Revision 34 conditional-phase and resonant-polygon arguments;
- the repository-level `ROUND17_PROOF_DEPENDENCY_LEDGER.md`.

I also made a targeted comparison with directly adjacent work on probabilistic and quantum finite automata, exact PFA simulation costs, finite-memory world models, probabilistic ordered branching programs, and orbit quantization. This was not an exhaustive priority certification.

The publication genealogy is clean. Revision 35 descends from the controlling r19 report, preserves Revision 34, and adds a branch-specific package rather than overwriting prior manuscripts. This is good provenance practice. It is not evidence for correctness, originality, or journal significance.

The 13-page focused article is self-contained enough to audit its new claims. The 449-page mathematical archive and 1002-page development archive are optional provenance records, not proof supplements that increase the weight of the journal submission. I did not treat regression volume, negative controls, hashes, source binding, page comparisons, or successful compilation as substitutes for proof.

---

## 2. What Revision 35 genuinely resolves

### 2.1 The principal hidden-width exponent gap is closed in the stated regime

Revision 34 proved

```text
Omega_alpha(N^(1/5)) <= W_N(alpha) <= O_alpha(N^(1/3))
```

for bounded-type angles. The lower proof saw actual hidden states, but its Fourier witness paid a quadratic harmonic cost and left the main exponent open.

Revision 35 changes the test law rather than changing a constant. A packet of length `B=2k-1` is selected as

```text
1^J 0^(B-J),    J uniform on {0,...,B}.
```

The endpoint register has at most `k` labels, while the packet produces `2k` separated phase increments. Any `k` endpoint centroid directions miss at least half of these increments by a controlled angular distance. This yields a relative amplitude loss of order `s_B(alpha)^2`, where

```text
s_B(alpha) = min_{1 <= l <= B} ||l alpha||.
```

For a badly approximable angle, `s_B(alpha) >= b_alpha/B`. Independent packets therefore give a cube-root lower bound, matching the exact resonant upper construction.

This is a genuine solution of the exact asymptotic-order question posed in the previous report, within its explicit scope.

### 2.2 The lower bound covers arbitrary hidden states

The proof uses

```text
E || E[Y | S] ||
```

at packet boundaries. It neither assigns a predictive vector to every hidden basis state nor projects a simplex section into an observable polygon. All internal rows and internal hidden states of one packet are integrated into its endpoint kernel.

Thus the lower bound covers precisely the hidden-lift freedom that caused the exponential loss in Revisions 32--33. This is the strongest aspect of the paper.

### 2.3 The theorem is robust under fixed output error

The terminal calibration is wordwise. Binary row-TV error `epsilon` changes each coordinate mean by at most `2 epsilon`, giving

```text
kappa = 1/10 - 2 epsilon.
```

For every fixed `epsilon < 1/20`, the packet product must retain a positive terminal phase amplitude. Hence the same cube-root order survives.

This is materially stronger than an exact-only lower bound that disappears under arbitrarily small perturbation.

### 2.4 The nonuniform occupation statement is retained and sharpened

The paper proves more than a scalar peak bound. For each `k`, it selects disjoint packets ending at cuts with `K_t <= k` and obtains a bound of order

```text
#{t : K_t <= k} = O_alpha,epsilon(k^3).
```

Widths at all other cuts may be arbitrarily large. The packet intervals are selected from the declared profile, not from the machine's private trajectory. This is a valid worst-case converse because the target specification is wordwise.

### 2.5 The actual terminal-error objective is separated from local deficiency

Revision 35 defines the true compact optimization

```text
E_N(K_0,...,K_N)
```

for minimum uniform terminal row error. A weighted interval-packing budget yields a direct lower bound on this intrinsic objective. Only afterwards is the result transferred to an accumulated local deficiency certificate.

This resolves an important semantic weakness of Revision 34: cancellation of intermediate local errors cannot evade the new terminal bound.

### 2.6 The branching-program and circle-walk comparisons are much better

The article now maps the transducer to a nonuniform stochastic ordered read-once branching program, writes the standard Boolean Fourier coefficient as a matrix product, distinguishes arbitrary row-stochastic programs from regular programs, and cites the Reingold--Steinke--Vadhan, Steinke--Vadhan--Wan, and Lee--Pyne--Vadhan results.

It also distinguishes the classical uncompressed circle walk from the new correlated packet law. These repairs directly answer two omissions identified in r19.

These are substantial improvements. They do not, by themselves, establish top-four depth.

---

## 3. Technical audit of the fixed-binary-command theorem

### 3.1 The machine model is now sufficiently explicit

The model fixes a horizon, cut-dependent finite state alphabets, initialization rows, two row-stochastic matrices per layer, and two terminal decoder columns. Uniform binary TV error equals half the maximum mean error. Available labels, including padding, are counted.

The external clock, horizon-specific design, exact stochastic rows, read-only tables, arithmetic, and table size remain free. This is a coherent positive-realization width model.

The lower bound may choose an input-word distribution after the available profile is known. This is legitimate because the simulator must be correct on every word. The chosen distribution is proof-side data and is not supplied as runtime memory.

### 3.2 The separate positive minimum remains three

Residual rows are affine in a two-dimensional predictive vector. Idle prefixes from four seeds span that affine plane, and the two terminal queries distinguish the coordinates. Normalization gives ordinary rank three.

The fixed triangle contains all reachable predictive vectors, and its vertices give legal future channels. Storing the raw history before a selected cut and a triangle label plus count after it embeds the selected-cut factorization into a complete finite machine. Thus the separate minimum is genuinely attained, not merely an amputated matrix factorization.

### 3.3 The one-packet contraction lemma is correct in its stated setting

For an independent group element `G`, old conditional centroids `z_s`, and at most `k` endpoint labels, choose the unit direction of each endpoint centroid. The retained amplitude is bounded by the expected best inner product with these `k` directions. The orbit-distortion definition gives the stated contraction.

Randomized endpoint assignments only weaken the upper bound because they are dominated by the pointwise maximum over endpoint directions. No statewise observable realization is assumed.

### 3.4 The separated circle packet gives the claimed loss

For `B=2k-1`, the phase increments indexed by `J=0,...,B` are pairwise separated by at least `s_B(alpha)`. An open arc of radius `s_B/2` contains at most one increment. Therefore `k` center directions leave at least `k` of the `2k` increments outside all such arcs.

Averaging the corresponding loss gives

```text
(1/2)(1-cos(pi s_B)) = sin^2(pi s_B/2) >= s_B^2.
```

The constants are crude but the argument is correct.

### 3.5 The packet uses actual binary-command time

The random choice `J` is not one enlarged free input. The word `1^J0^(B-J)` occupies exactly `B` ordinary command slots. The machine may react to every internal command and use arbitrarily large internal registers. Only the endpoint width is bounded in the packet inequality.

This point is essential, and the manuscript handles it correctly.

### 3.6 Terminal calibration works for the correlated packet law

The target is correct word by word, so the terminal correlation argument applies under any externally chosen command-word distribution. Combining the two coordinate decoders into one complex column does not demand joint sampling of two outputs.

The row-TV factor of two is correct. Conditioning on the final state yields

```text
q_N >= 1/10 - 2 epsilon.
```

No correctness at earlier query times is used.

### 3.7 The occupation and peak bounds are coherent

Independent packets on disjoint intervals multiply the surviving amplitude. The inequality `1-u <= exp(-u)` turns the product into an additive packet budget.

For the occupation theorem, the greedy interval selection removes at most `B` low-width endpoints per selected interval, after discarding at most `B-1` initial endpoints. This gives the stated count.

For a peak-`K` machine, consecutive packets give

```text
floor(N/(2K-1)) s_(2K-1)(alpha)^2 <= log(1/kappa).
```

Bad approximability then yields the cube-root lower bound. The golden-angle constant `168` is a proof constant, not an optimized asymptotic constant.

### 3.8 The exact resonant upper construction remains credible

A continued-fraction denominator `q` makes the residual rotation angle of order `q^(-2)`. The radial enlargement per step has logarithm of order `q^(-3)`. Taking `q` of order `N^(1/3)` keeps the terminal decoder bounded.

The idle row mixes the current label with the zero barycenter; the active row mixes two adjacent resonant vertices. The expected associated vector follows the exact rotation. The command matrices are common across epochs, while the decoder depends on the selected horizon.

This matches the unrestricted lower order for badly approximable angles.

### 3.9 The angular appendix is correct but no longer central

The coefficient `l^2-1` follows by retaining the exact remainder coefficient and is sharp under symmetric two-point mixtures. This repairs the proof detail raised previously.

The cube-root theorem does not depend on improving the Fourier summation. That separation is correctly stated.

---

## 4. A formal gap in the general packet theorem

The principal fixed-circle application appears sound, but the general representation-valued theorem is not proved exactly as stated.

Lemma `lem:packet` assumes that, conditional on `(Y,S,G)`, the endpoint law depends only on `(S,G)`. In other words, `G` is the packet input visible to the endpoint kernel.

Theorem `thm:group-budget`, however, allows a machine to process an entire command word. Its proof says that the internal computation can be integrated into a kernel conditional on the starting state and the **command word**, and then invokes Lemma `lem:packet` with the word's group product `G`.

These are not the same statement when two different command words have the same product. The machine may distinguish the two words through their ordered intermediate inputs even though the representation acts by the same final `U_G`.

This is not merely pedantry. The theorem expressly advertises noncommuting packets and general compact groups, where collisions of the product map are natural.

The intended inequality appears repairable. One can formulate the lemma with a fresh packet variable `W`, a measurable product map `g(W)`, and an endpoint kernel depending on `(S,W)`. In the proof,

```text
sum_r T_W(s,r) <U_{g(W)}v_s,u_r>
    <= max_r <U_{g(W)}v_s,u_r>,
```

and expectation over `W` depends only on the pushforward law of `g(W)`. This would recover the same orbit-distortion bound without requiring product sufficiency.

But that argument is not the stated lemma, and the theorem's present proof skips the distinction. The authors must do one of the following:

1. restate and prove the packet lemma with the full fresh word variable;
2. add an explicit product-sufficiency hypothesis;
3. restrict the theorem to injective packet supports.

The main circle packet has distinct irrational character values, and the `SO(d)` theorem uses one group command per packet, so this gap does not appear to invalidate the headline fixed-binary theorem. It does affect the claimed general compact-group theorem and must be repaired before publication.

---

## 5. The compact-group extension changes the problem

### 5.1 The character corollary is a genuine finite-alphabet extension

If a finite command alphabet contains the identity and one element with a badly approximable character angle, the circle packet argument transfers directly. This is a useful and natural representation-theoretic reformulation of the headline theorem.

It remains a one-dimensional observed character. It does not give a multiplicative theorem for several characters or a general finite noncommuting alphabet.

### 5.2 The `SO(d)` theorem uses an uncountable atomic input alphabet

The second compact result allows every matrix in `SO(d)` as one exact external command. A complete Borel lookup table `g -> T_{t,g}` is free, as are exact matrix input and exact real arithmetic.

This is a coherent mathematical experiment, but it is not a finite automaton or ordinary branching program. It has substantially stronger input access than the main binary-command model.

### 5.3 The exponent is classical sphere quantization in sequential form

Haar rotation makes the orbit uniform on the sphere. A `k`-center small-ball bound gives distortion of order `k^(-2/(d-1))`; a spherical net of size order `rho^(-(d-1))` gives the matching construction.

The sequential contraction theorem converts this classical quantization rate into a width law

```text
Theta(N^((d-1)/2)).
```

This is a neat application. Its geometric exponent is not a new sphere-covering theorem, and the model change makes it weak evidence for the breadth of the original fixed-alphabet result.

### 5.4 A stronger generalization would keep the alphabet finite

For broader significance, the authors would need a theorem for a natural finite noncommuting generating set, with orbit-growth or representation hypotheses stated intrinsically. The present all-`SO(d)` input theorem avoids the main difficulty by drawing a fresh Haar group element in one atomic command.

The paper correctly warns that the two models differ. The abstract nevertheless gives the compact theorem substantial prominence, and the editorial case should not treat it as if it generalized the fixed binary interface without cost.

---

## 6. Originality and the missing quantum-automata comparison

Revision 35 repairs the branching-program and circle-walk omissions from r19. It still omits another direct neighboring literature.

The target process is a prepare--rotate--test architecture with a constant-dimensional continuous phase and two terminal observables. This is naturally adjacent to one-way quantum finite automata, generalized quantum finite automata, and their exact simulation by probabilistic finite automata.

Two recent papers are especially relevant:

- Zeyu Chen and Junde Wu, *The Quadratic State Cost of Classical Simulation of One-Way Quantum Finite Automata*, arXiv:2604.07058 (2026);
- Zeyu Chen and Junde Wu, *On the Simulation Cost of Quantum Finite Automata*, arXiv:2605.10682 (2026).

Those works study exact strict-cutpoint language simulation and obtain sharp worst-case PFA state costs for quantum automata. Their objective, quantifiers, and asymptotic parameter differ from the present finite-horizon uniform-real-output approximation problem. They do not automatically imply the cube-root theorem.

That difference is precisely why a theorem-level comparison is required. The authors should answer:

1. Can the present rotation experiment be written as a constant-dimensional measure-once or general one-way quantum automaton with a query symbol or query-dependent terminal measurement?
2. Which part of the `Theta(N^(1/3))` law is invisible to strict-cutpoint equivalence?
3. Is horizon length playing the role of an input-length restriction absent from the state-complexity results?
4. Does uniform approximation of both real observables impose a stronger requirement than language equivalence at one cutpoint?
5. Can the prepare--test or sign-rank mechanisms in that literature give an alternative lower bound or a different family?

The manuscript also drops a recent source that Revision 34 had regarded as directly relevant:

- Josep Lumbreras, Hailan Ma, Jayne Thompson and Mile Gu, *An Irreducible Quantum Advantage in Aligning World Models with Reality*, arXiv:2608.19779 (2026).

That paper uses an irrational phase and finite classical memory in a stationary decision/world-model setting. Again, its result is not the present theorem: its task, stationarity, output, and conclusion differ. But the common phase-memory architecture and the manuscript's own historical comparison make omission from Revision 35 difficult to justify.

A September 2026 priority audit cannot stop at classical branching programs when two 2026 quantum/classical simulation lines are this close to the mathematical object.

---

## 7. Mathematical depth and generality

### 7.1 The main proof is elegant but specialized

The sharp lower bound combines three observations:

1. a wordwise simulator may be tested under an adversarial correlated packet law;
2. `2k` separated orbit points cannot be quantized into `k` endpoint directions without `Omega(k^(-2))` average loss;
3. independent packet losses multiply.

This is clean and useful. It is not a deep classification of stochastic branching programs or positive realizations. It is a tailored test distribution for one rotation-count statistic.

### 7.2 The theorem does not classify all irrational angles

For badly approximable angles, the lower and upper orders match. For the irrational angle with rational rotation entries, the manuscript retains only a logarithmic lower bound and a much larger upper bound. More generally it gives a lower formula under a Diophantine exponent without a matching construction.

Thus “Sharp Width of Hidden Rotation Experiments” is broader than the result. The sharpness is for fixed badly approximable angles, fixed signal, and fixed error.

### 7.3 No leading asymptotic constant or exact finite law is obtained

The paper explicitly declines to optimize constants. That is reasonable. But once the theorem is confined to a single model family, the absence of a leading constant, exact integer asymptotics, or a finite-width phase diagram limits its four-journal significance.

### 7.4 The terminal query is highly restricted

The machine is asked one coordinate query only after the prescribed length. It need not answer at intermediate lengths, retain an output history, support repeated queries, or produce the joint pair of coordinates.

The authors correctly distinguish the stronger anytime task. The paper does not explain why this one-query interface is foundational for the broader theta program.

### 7.5 Adaptive experimental design is absent

The command word is externally supplied. The lower bound may choose its distribution, but the machine does not optimize informative actions, and no controller chooses commands based on previous reports.

This is not a theorem about the fully adaptive collision-validation or experiment-design problems appearing elsewhere in the repository.

---

## 8. Resource-model assessment

The counted resource is the maximum number of available persistent labels. The following are free:

- the horizon `N`;
- the external epoch;
- a different state set at every layer;
- a different pair of stochastic matrices at every layer;
- a complete horizon-specific row table;
- table lookup and arithmetic;
- exact sampling from arbitrary real stochastic rows;
- exact computable-real constants in the resonant construction;
- one atomic terminal query.

There is nothing inconsistent about this model. It is a positive-realization width model.

It is not ordinary uniform computational space. The statement that the theorem uses `(\log_2 N)/3+O(1)` persistent label bits excludes the description required to identify the machine, its transitions, the exact real constants, and the horizon-dependent decoder.

The exact upper construction is particularly nonuniform. Although its two command matrices are common across epochs for a fixed `N`, the selected convergent denominator, alphabet size, radial scale, and final decoder depend on `N`.

The fair-bit compiler for rational rows has additional workspace and does not preserve the atomic optimum. The badly approximable upper construction generally uses irrational rows and has no finite exact fair-bit implementation theorem.

These boundaries are stated more honestly than in earlier revisions. They remain central to the editorial judgment.

---

## 9. Actual terminal error and deficiency

The weighted-interval dynamic program is correct. It maximizes the sum of packet separation costs over disjoint admissible intervals. The packet product gives an upper bound on terminal conditional amplitude for every machine with the declared profile.

Combining this with terminal calibration yields

```text
E_N(profile) >= (1/2)[1/10 - exp(-B_alpha(profile))]_+.
```

This is an intrinsic lower bound on actual terminal error and is immune to cancellation of local modeling errors.

The result is useful, but several limitations should remain prominent:

- it is a lower bound, not an exact finite formula;
- the limiting `1/20` constant is not claimed optimal;
- no matching approximate construction is given for general subcritical profiles;
- the angle-dependent interval weights may not be computationally accessible under a succinct representation;
- the diagram corollary is derivative, obtained by executing local garblings and invoking the terminal theorem.

The distinction between actual terminal error and accumulated local deficiency is now correct. The deficiency corollary does not constitute an independent dynamic-comparison classification.

---

## 10. Pipeline assessment

Revision 35 closes one local status objective:

```text
sharp_hidden_rotation_width_solved = true
```

but only in the explicitly recorded scope:

```text
badly approximable fixed angle;
fixed signal 1/10;
fixed epsilon < 1/20;
asymptotic order only.
```

The same status file records as unresolved:

- classification of all irrational angles;
- historical A2 replacement;
- B4 aggregate closure;
- C2 aggregate closure;
- the eleven-paper aggregate;
- fully adaptive collision scheduling;
- noisy-tag composition;
- independent priority certification.

The Round-Seventeen proof ledger contains two long analytic chains:

```text
A2 -> A3 -> A4 -> C2 -> D1
```

and

```text
B2-GC -> B1 -> B2-MC -> B3 -> B4 -> C1/C2 -> D1.
```

Their gates require branchwise Fourier/LLT estimates, stopped large deviations, common-domain kernels, nonlinear semigroups, graph cores, filtering regularity, optional projection, and typed contraction. None follows from a finite-register packet quantization theorem.

The word “Fourier” in the historical A2 gate and the harmonic language of Revision 34 do not create a dependency edge. Revision 35's proof is a self-contained finite-memory converse for a different experiment.

No downstream manuscript in the main pipeline is shown to consume the cube-root theorem. The repository history supplies context and provenance, not additional mathematical leverage for this submission.

The title “General Theta Foundations I” therefore remains misleading. The focused paper is about one positive-realization/branching-program width problem and a separate compact-input quantization problem. It is not a foundation theorem for the A/B/C/D program.

---

## 11. Required changes for a credible specialist submission

These are not a route to acceptance in a top-four journal. They are the minimum changes needed for a fair specialist evaluation.

### 11.1 Repair the packet theorem's quantifiers

Restate the one-packet lemma with a fresh packet word and a product map, or impose product sufficiency. Then verify that the noncommuting and compact-group claims use the corrected statement.

### 11.2 Add the quantum-automata simulation comparison

Compare the exact objective and resource parameter with the Chen--Wu 2026 QFA-to-PFA simulation results and with earlier state-complexity work on quantum versus probabilistic automata. Explain whether the rotation experiment is itself a constant-dimensional quantum automaton under a query-dependent measurement.

Restore the comparison with the Lumbreras--Ma--Thompson--Gu irrational-phase world-model result, or explain precisely why the models are too different to be informative.

### 11.3 Retitle the paper

Remove “General Theta Foundations I.” A subject-specific title such as

> Sharp hidden-state width for finite rotation transducers

would accurately classify the result.

### 11.4 Separate the compact-input theorem

The all-`SO(d)` result should be clearly labeled as a different model, possibly as an application or separate paper. Its uncountable exact command alphabet and free Borel row lookup should not be allowed to blur the finite-alphabet theorem.

### 11.5 State the true computational interpretation

Use “nonuniform clocked stochastic branching-program width” consistently. Avoid presenting `(\log N)/3` label bits as a uniform streaming-space bound.

### 11.6 Narrow the sharpness claim

State “sharp for fixed badly approximable angles at fixed signal and error.” Do not permit the title or abstract to suggest classification of all hidden rotation experiments.

### 11.7 Develop one broader finite-alphabet theorem

A major strengthening would give an intrinsic finite-generator criterion, perhaps in terms of orbit packing growth, representation dimension, or a Diophantine separation function, with matching upper and lower bounds beyond one cyclic character.

### 11.8 Keep the large archives outside the submission

The focused source, proofs, response, and a modest reproducibility supplement are sufficient. The 449-page and 1002-page cumulative PDFs should remain optional repository archives.

---

## 12. Specific technical and editorial points

1. In Theorem `thm:group-budget`, distinguish the packet word from its group product.
2. In Lemma `lem:packet`, state the exact conditional-independence sigma-fields rather than the prose phrase “depends only.”
3. State explicitly whether the group representation may have invariant directions and whether `Gamma_k=0` is permitted; the text currently does so, but the theorem statement should make the vacuity visible.
4. In the circle theorem, emphasize that the packet law depends on the candidate width `k`.
5. Explain that the lower bound is worst-case/wordwise and need not hold under the fair-command distribution alone.
6. The occupation theorem counts cuts `1,...,N`; state separately what happens at the initialization cut.
7. Preserve the distinction between available labels and positive-mass states under a selected test law.
8. Do not describe the common-row upper construction as one machine for all horizons; the decoder and state alphabet depend on `N`.
9. Clarify whether the strict inequality in the finite main bound is important or merely a floor-removal artifact.
10. The persistent-bit interpretation should explicitly say “label bits in a nonuniform machine.”
11. The quantum-automata comparison must distinguish strict-cutpoint language equivalence from uniform real-output approximation.
12. The world-model comparison must distinguish stationary repeated updates from cut-dependent finite-horizon rows.
13. In the `SO(d)` model, define the measurability requirement on `g -> T_{t,g}` in the formal machine definition, not only in the theorem section.
14. Explain whether Borel row lookup is oracle access or part of a nonuniform row table.
15. The finite triangulation argument for a Borel convex decomposition should be stated as a lemma or referenced.
16. Do not use the compact-input theorem as evidence of a finite noncommuting command result.
17. State that the sphere constants `c_d,C_d` may deteriorate rapidly with fixed `d`; no uniform-in-d theorem is claimed.
18. The actual-error theorem should specify that the maximizing interval family may depend on the proposed profile.
19. Clarify the representation required to compute `s_B(alpha)` and the interval weights.
20. Do not imply that the dynamic program is an efficient algorithm for arbitrary exact real angles.
21. Keep the deficiency sum separate from intrinsic final error in every summary table.
22. The branching-program comparison should include probabilistic, not only deterministic/regular, terminology.
23. Explain whether private stochastic rows can be represented as distributions over deterministic tables without introducing a persistent shared seed.
24. State that the matrix-product Boolean Fourier identity is not used in the proof of the cube-root theorem.
25. The angular lemma is now an appendix and should not be marketed as part of the sharp proof.
26. The rational-entry irrational angle remains far from classified; avoid treating “explicit logarithmic converse” as near-sharp.
27. The separate-minimum proof stores a remaining command count after the chosen cut; state its finite label cost even though other cuts are unrestricted.
28. Remove internal A2/B4/C2 labels from the focused mathematical conclusion; retain them in repository status records only.
29. Do not use revision count, test count, archive size, or source hashes as evidence of significance.
30. Obtain an independent priority review from researchers in probabilistic/quantum automata or positive systems before sharpening novelty claims.

---

## 13. Scorecard

| Criterion | Assessment |
|---|---|
| Correctness of the fixed-binary theorem | Appears coherent; no short fatal counterexample found |
| Correctness of the general packet theorem | Repairable formal word/product mismatch in the current proof |
| Advance over Revision 34 | Substantial: closes the unrestricted bounded-type exponent gap |
| Originality boundary | Incomplete: direct 2026 quantum-automata simulation and world-model literature omitted |
| Mathematical depth | Strong specialist level; below top-four general-mathematics level |
| Quantitative strength | Sharp exponent for badly approximable angles; no leading constant or all-angle classification |
| Generality | One cyclic planar family; compact extension changes to an uncountable exact input alphabet |
| Computational model | Nonuniform clocked atomic rows; tables, arithmetic, and exact real sampling free |
| Terminal error | Genuine intrinsic lower bound, not an exact finite characterization |
| Pipeline impact | Closes one local status objective; none on decisive A2/B4/C2/D1 gates |
| Presentation | Focused and substantially improved; Foundations branding remains misleading |
| Reproducibility engineering | Strong, but irrelevant to proof, priority, and journal level |
| Editorial recommendation | Reject at top-four level; consider after specialist repositioning and formal repair |

---

## 14. Final assessment

Revision 35 is the strongest manuscript in this sequence. It does what the previous report asked at the mathematical level: the unrestricted hidden-state lower bound now matches the exact cube-root construction for badly approximable angles. The packet test law is a clever way to avoid the quadratic Fourier-harmonic loss, and the argument genuinely covers arbitrary hidden states and cut-dependent stochastic rows.

That achievement should be credited without reservation.

It should also be classified accurately. The proof is a specialized orbit-quantization/data-processing argument for one rotation-count experiment under a width-dependent adversarial input law. The compact-group theorem changes the input model and rests on classical sphere quantization. The general packet theorem needs a quantifier repair. The quantum-automata simulation boundary has not been audited. The computational model is nonuniform and permissive. The theorem has no demonstrated role in the repository's main analytic DAG.

Put bluntly: **Revision 35 has solved the sharp width of the authors' chosen bounded-type rotation toy model; it has not established a foundational theory of hidden causal memory.**

My recommendation is therefore firm:

**Reject for Annals of Mathematics, Inventiones Mathematicae, Journal of the AMS, or Acta Mathematica.**

After repairing the packet theorem, completing the quantum/probabilistic-automata comparison, removing the Foundations framing, and separating the compact-input application, a focused paper on sharp width for stochastic rotation branching programs could merit serious specialist review. That would be a new editorial submission, not another internal revision under the claim that the manuscript is approaching the four-journal threshold.
