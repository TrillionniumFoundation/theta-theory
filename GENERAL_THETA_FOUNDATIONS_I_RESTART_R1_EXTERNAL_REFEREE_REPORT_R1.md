# Referee Report — *General Theta Foundations I: Acquired Geometry and Causal Resource Transfer*

**Submission:** *General Theta Foundations I: Acquired Geometry and Causal Resource Transfer*  
**Author:** Qian Qi  
**Repository:** `TrillionniumFoundation/theta-theory`  
**Reviewed review-ready branch:** `review-ready/general-theta-restart-r1-acquired-geometry-2026-10-06`  
**Reviewed exact final head:** `589372183966bef1b40ae223b0ab468cb6419182`  
**Native mathematical source:** `6d1c37e511e5307913b81b091e8eceefa4e90448`  
**Canonical restart base:** `18000b21e4bfd89180ccb069e46ac0f21621f34d`  
**Rendered-paper SHA-256 recorded by the repository:** `c529dbf4d04d8cc6e5dd45a7a859e9a447465b765f2e3b06549abfd9b2afeb04`  
**Review branch:** `review/general-theta-restart-r1-acquired-geometry-external-referee-r1-2026-10-07`  
**Date:** 7 October 2026

This is an author-requested external mathematical assessment deposited in the repository. It is not a commissioned editorial decision of any named journal, and it does not constitute independent certification of priority or journal acceptance.

## Recommendation

**Reject at the level of the Annals of Mathematics, Inventiones Mathematicae, the Journal of the American Mathematical Society, or Acta Mathematica in the manuscript's present form.**

This is **not primarily a correctness rejection**.

The manuscript contains a coherent quantitative transfer lemma, a useful distinction between acquired probability mass and a merely reachable envelope, a careful innovation-localized error recurrence, and two genuinely different kernel-level examples. I did not find a single elementary algebraic error that collapses the central inequalities. The checkpoint projection identity, the anisotropic covering and small-ball argument, the positive transport recurrence, the intersecting-strata comparison, the hidden-state filter calculations, and the absorbing-sensor calculations are, in the load-bearing portions I checked, internally consistent.

The negative four-leading-general-journal recommendation is instead based on four connected points.

1. The central online theorem is conditional on an innovation recurrence and an acquisition-weighted second-moment certificate that already contain most of the difficult model-dependent stability needed for the conclusion. The manuscript derives this certificate only in a uniformly contractive setting, an exact-hold/contractive-active setting, and a one-acquisition absorbing setting. It does not yet derive the certificate from a broad, natural class of causal kernels.
2. The claimed resource-transfer layer is not yet a complete theorem in the full resource vector advertised by the paper. It supplies a constructive upper accounting and a standard total-variation common-loss transfer, while the matching lower in simulator, controller, clock, workspace, program, calibration, and acquisition resources is explicitly left open.
3. The robust lower-floor proposition is conditional on a not-yet-formalized common class and uniform upper theorem. It is not presently a fully quantified minimax result.
4. The priority comparison is too narrow for a paper presented as a new general foundation. The current comparison does not adequately place the work relative to causal-state/minimal predictive representations, probabilistic bisimulation and state aggregation, finite model approximation of belief-state control problems, the full Le Cam–Torgersen comparison-of-experiments framework, and broader quantization theory for singular measures.

For a strong specialist journal in stochastic control, mathematical statistics, information theory, nonlinear filtering, or quantization, I would recommend **major revision and resubmission**, provided the paper is repositioned accurately and the technical points below are addressed. A merely stylistic revision would not change my four-leading-general-journal recommendation. A materially stronger theorem deriving the weighted transport bound from a broad nonuniform kernel class, together with a genuine full-resource minimax theorem, could change the mathematical scale.

---

## 1. Review object, provenance, and pipeline inspected

The review-ready branch and the named revision branch were identical at the time of review. The exact review object is therefore the final head

```text
589372183966bef1b40ae223b0ab468cb6419182.
```

The mathematical source is the immediate predecessor

```text
6d1c37e511e5307913b81b091e8eceefa4e90448,
```

and the final child adds only the rendered `paper.pdf` and the two evidence receipts. The source itself descends from the canonical restart commit

```text
18000b21e4bfd89180ccb069e46ac0f21621f34d
```

by adding the dedicated r1 paper tree and its workflow. I found no indication that an old v1–v96 paper directory was silently rewritten in order to create this submission.

I reviewed the following current-paper materials as one pipeline rather than treating the rendered article in isolation:

- the complete native manuscript, including all six sections and the bibliography;
- `RESTART_CHARTER.md`, `THEOREM_TARGETS.md`, and `REALIZATION_REGISTRY.md`;
- the theorem map, assumption matrix, proof ledger, counterexample ledger, resource-accounting table, scope audit, notation audit, history-coverage statement, and literature comparison;
- the source manifest, publication policy, build script, regression script, build receipt, and regression receipt;
- the canonical restart provenance and the separation between source and artifact commits.

The committed build receipt records a 16-page paper, eleven formal statements, eleven proof environments, forty-seven labels, an independent rebuild, 10,008 finite checks, and twenty-four rejected negative controls. The regression script correctly states that these checks are not proofs of the continuum theorems. I have treated them as source-integrity and regression evidence only. No numerical test or successful typesetting job substitutes for the mathematical review below.

The pipeline materials are unusually candid about limitations. In particular, the scope audit expressly leaves open broad recurrent nonuniform transport, unknown-kernel learning, full-resource lower bounds, unrestricted exploration, and a single broad class realizing all robust error terms. This candor is a strength. It also confirms that several claims suggested by the title are not yet theorems of the paper.

---

## 2. Summary of the mathematical contribution

The manuscript begins with a prepared finite-horizon causal experiment. A visible history determines evaluations of executable future tests and hence a predictive equivalence class. For a fixed exploration policy and a terminal squared-prediction task, the full-history Bayes risk is denoted by \(B_N\), while the law of the conditional prediction vector is denoted by \(
u_N\).

A checkpoint encoder may compress the full history into at most \(m\) labels at time \(N\). An online encoder must maintain at most \(m\) persistent labels recursively, with no readable observation tape. Conditional-mean projection identifies the checkpoint excess risk with the optimal \(m\)-point quadratic quantization error of \(
u_N\).

The geometric hypothesis decomposes the actual acquired law into finitely many weighted component charts. Each component is the image of an anisotropic box with widths

```text
a_{j,1} >= ... >= a_{j,d_j} > 0,
```

and carries an actual conditional density bounded above by a constant multiple of the reciprocal box volume. The paper defines

```text
psi_j(k)
  = max_{1 <= l <= d_j}
      ((a_{j,1} ... a_{j,l})/k)^(2/l)
```

for \(k\geq 1\), gives a fixed discard penalty at \(k=0\), and minimizes the weighted sum over label allocations. The resulting quantity is \(\Psi_N(m)\).

The online part is encoded by a pathwise recurrence

```text
e_{t+1} <= A_{t+1} e_t
            + C_0 sum_j B_{t+1,j} r_j
            + u_{t+1},
```

where \(r_j=\sqrt{\psi_j(k_j)}\). Error is inserted only when the implementation actually rounds. Exact holds have zero innovation coefficient. Unrolling produces positive transport weights \(Z_{N,j}\). The decisive hypothesis is

```text
E (sum_j Z_{N,j} z_j)^2
    <= Gamma_N sum_j w_{N,j} z_j^2
```

for every nonnegative vector \(z\), with the same acquired weights \(w_{N,j}\) that occur in the geometric lower bound.

Under these hypotheses the central theorem proves

```text
B_N + c Psi_N(m)
  <= R_cp(N,m)
  <= R_on(N,m)
  <= B_N
     + (C sqrt(Gamma_N Psi_N(m))
        + L ||U_N||_2
        + v_N^num)^2.
```

The paper then adds a bounded-horizon report-law comparison, a causal-simulator composition statement, two explicit robust lower witnesses, and two realizations:

1. a controlled binary hidden-state filter with continuous reports, for which the posterior is a one-dimensional predictive state and the excess risk is of order \(m^{-2}\);
2. an absorbing geometric sensor, for which acquisition may fail for an arbitrarily long time, the acquired support may contain intersecting strata of changing dimension, and the error transport is an exact indicator identity.

This is a sensible and potentially useful synthesis. The central conceptual message—that memory resolution should be governed by the law actually acquired under the experiment, and that exact waiting steps should not be charged repeated quantization errors—is correct and worth stating clearly.

---

## 3. Assessment against the restart targets F1–F4

The repository gives four explicit theorem targets. My assessment is as follows.

### F1: causal acquired-geometry transfer

**Substantially achieved for the stated certificate class.**

The manuscript proves matching checkpoint and online predictive-label curves after assuming actual chart mass, a global valid cover, an innovation-localized implementation, and the weighted transport inequality. The optimal risk is not inserted as an assumption. The lower and upper use the same acquired component weights. This is a genuine class theorem, not merely a computation in one finite experiment.

The qualification is important: the hardest online property is concentrated in the transport certificate, and only narrow sufficient mechanisms are derived. Thus F1 is achieved as a conditional transfer theorem, not as a broad classification of causal experiments.

### F2: resource–resolution–risk composition

**Only partially achieved.**

The paper gives a constructive resource upper map, multiplies persistent state counts correctly, accounts for raw calls and pilot calls, and transfers a common bounded loss through total variation. Calibration and numerical state errors are propagated before squaring. These are valuable accounting improvements.

However, the theorem does not give a matching law in the complete resource vector. Workspace, program description, calibration precision, clock, and physical time are introduced but not retained as explicit arguments in the main joint-risk inequality. The lower-floor proposition is conditional on a common-class embedding and does not close the advertised full resource theorem. The paper itself acknowledges that growing controller, simulator, and clock costs have no matching lower bound. F2 is therefore not closed in the strong form stated by the restart target.

### F3: singular or nonuniform extension

**Achieved in a nontrivial but still special form.**

The absorbing sensor has exact holds, vanishing acquisition probability, intersecting finite strata, atoms, and changing rank. The constants do not divide by a collapsing width or an inter-stratum separation. This is more than a formal rank-deletion convention and more than a fixed finite ensemble.

The extension remains restricted to finitely many uniformly bi-Lipschitz boxes and a single absorbing acquisition. It does not yet cover recurrent nonuniform systems with expanding active updates, infinitely accumulating strata, cusp densities, or singular measures outside the finite-chart class.

### F4: two distinct realizations

**Achieved.**

The filter and the absorbing sensor use genuinely different mechanisms: repeated Bayesian contraction versus one-time overwrite with exact holds. Neither realization is used as a premise of the general theorem. This is the correct logical direction.

---

## 4. Audit of the main proof chain

### 4.1 Predictive quotient and minimality

The paper is right to define predictive equivalence through executable future tests rather than through an arbitrary parameter coordinate. It also correctly includes action legality, remaining budget, and clock information in the continuation interface. The compact-image argument is a natural way to obtain a metrizable realization when the belief domain and evaluation maps satisfy the stated continuity assumptions.

There are nevertheless two technical deficiencies in Proposition 1 that must be corrected.

First, the measurable factorization statement is too broad. The manuscript says that any measurable history statistic \(r_t\) through which all determining evaluations are measurable admits a measurable factor. A Doob–Dynkin type factorization is automatic when the statistic takes values in a standard Borel, or at least suitably countably generated, measurable space. It is not a theorem for an arbitrary unspecified measurable codomain. The codomain and the completion convention should be stated explicitly, and the proof should cite or prove the exact factorization lemma being used.

Second, the continuous-report update descent is compressed past a real version issue. Equality of a countable family of future-test expectations determines continuation laws, but a pointwise normalized update at a report value of zero probability is not obtained merely by writing a Bayes numerator and denominator. The manuscript assumes a common dominating measure and a jointly continuous normalized update; that is enough for the two realizations, but the proposition should state the precise instrument-level closure required so that density-weighted one-step pullbacks belong to the determining class. It should then prove that equivalent beliefs give equivalent updated beliefs for every declared report in the continuous version, not only almost everywhere under each belief. At present the proof moves too quickly from event-level future laws to pointwise conditional versions.

These are repairable issues. They are not merely cosmetic because the quotient is the first arrow in the advertised foundation.

### 4.2 Checkpoint projection

Lemma 3.1 is standard but correctly formulated for this task. Conditioning on the full history removes the cross term; decoder randomization is eliminated by convexity; encoder randomization is eliminated by nearest-center selection; and projection of centers to the prediction box is harmless. The distinction between separately executable probes and a nonexistent joint counterfactual probe vector is also handled correctly.

I found no substantive gap in this lemma.

### 4.3 Anisotropic actual-mass lemma

The upper grid argument is elementary and sound. With \(h=\sqrt{\psi_j(k)}\) and cell width \(2h\), the number of active coordinate cells is at most \(k\), and the Euclidean covering radius is controlled without dividing by a vanishing coordinate width.

The lower argument uses exactly the right kind of hypothesis: an upper small-ball mass estimate for the actual acquired law. A score ball has a preimage whose coordinate projections are short; the density upper bound then yields the anisotropic small-ball estimate. This is sufficient for a union-bound quantization lower bound and does not require an artificial lower density.

For separated components, assigning decoder centers to nearby score images and charging unassigned components by the separation scale is valid. The zero-allocation penalty correctly keeps the cost of discarding an entire component. The proof permits arbitrary decoder centers and does not assume that an optimal center lies on a chart.

The manuscript should nevertheless make the quantifiers more visible. If charts, maps, or valid domains vary with \(N\), this should be indexed explicitly, and the exact uniformity class for all constants should be stated before the theorem rather than partly after it. The present prose allows \(N\)-dependent certificates while the notation suppresses that dependence.

### 4.4 Innovation transport

The unrolling of the positive recurrence is correct. Minkowski's inequality and the weighted second-moment hypothesis give the stated root-mean-square upper bound without an independence assumption. The exact-hold convention is important and mathematically legitimate: if a representative is preserved exactly, a new covering error need not be inserted at that physical tick.

The principal mathematical limitation of the paper lies here. Condition (T) is not a modest regularity assumption. It is the assertion that the complete forced transport process is controlled in precisely the acquisition-weighted quadratic form needed to match the lower bound. Together with (I), it packages most of the hard online stability problem.

The manuscript proves three mechanisms:

- uniform contraction;
- exact holds interspersed with contractive active updates;
- one absorbing acquisition followed by exact holds.

All three are correct, but none is close to the general recurrent nonuniform problem emphasized by the title. In particular, no theorem derives (T) from a natural drift/minorization, Lyapunov, cocycle, regeneration, spectral, or martingale condition permitting occasional expansion on active steps. The scope audit recognizes this omission.

For a specialist paper it is acceptable to present (T) as a transparent verification target. For a four-leading-general-journal foundation, the paper needs a theorem that makes (T) emerge from a substantially broader structural condition, or it must narrow its claims and title. Merely adding further examples that directly compute \(Z_{N,j}\) would not fully answer this objection.

### 4.5 Main theorem

Conditional on the certificates, the main lower and upper inequalities follow. The online output is a legal checkpoint output, so the middle comparison is immediate. The score Lipschitz bound converts state error to prediction error, and the conditional projection identity supplies the same Bayes baseline.

Several statements should be sharpened.

1. The theorem says that the minimizing allocation is implemented effectively, while condition (C) also allows only a certified constant-factor allocation. These should be stated as two separate conclusions: an exact-minimizer conclusion under exact comparable data, and a constant-factor conclusion under the weaker effective certificate.
2. The asymptotic-comparability notation should specify its convention when \(\Psi_N(m)=0\), as occurs for point components once enough labels are available.
3. The phrase “parameter-independent update” is ambiguous in a theorem that initially fixes one experiment. If a parameterized family is intended, the common implementation and all uniform constants should be part of the theorem's quantified data.
4. The path-law allowance is stated under the fixed exploration, while the proof correctly notes that another controller requires its own certificate. This controller dependence belongs in the theorem statement, not only in the proof.

These are statement-level repairs rather than counterexamples to the displayed risk inequality.

### 4.6 Intersecting strata

The crossing corollary contains a useful point. The latent component mark may be used in the proof of the conditional acquired laws without being available to the encoder. The upper machine takes a nearest representative in the union codebook. The lower applies all \(m\) centers to each conditional component and compares equal allocation with the optimum. The resulting threshold \(m\geq 2J\) removes any inverse dependence on separation.

I find this argument correct for finitely many chart components. It is not a local manifold theorem and does not address infinitely many accumulating strata, but the paper does not formally claim that it does.

---

## 5. Audit of causal morphisms and resource accounting

The paper's insistence on a common task and a common oracle baseline is correct. A forward simulator transfers an upper risk bound; it does not automatically transfer a source lower bound. Simulator, controller, retained-label, and internal-clock state counts multiply as a constructive upper bound. Raw acquisition counts and calibration pilots must be charged. These distinctions are often mishandled, and the manuscript handles them responsibly.

The mathematical content of Theorem 4.1, however, is presently the triangle inequality for total variation, data processing under a nonanticipating kernel, and a Cartesian-product state implementation. This is a useful typed bookkeeping result, but it is not yet a fully developed resource theory.

The following definitions are needed before the theorem can bear the advertised weight.

1. Define the category or at least the complete data of a causal morphism formally: source and target filtrations, report transformers, lifted strategies, simulator state transitions, task readout, stopping, clock, and resource measurability.
2. Define the admissible strategy classes and prove that the two lifts in a serial composition map the outer class into the class on which the inner defect is uniform.
3. Define the resource preorder and the map \(ho_\Gamma\) coordinate by coordinate. The notation \(ho_1\circho_2\) is currently more suggestive than formal.
4. Keep the full resource vector in the risk notation. The vector is declared to contain acquisition count, label count, simulator state, controller state, clock, workspace, program description, calibration precision, and physical time, but the joint inequality later displays only acquisition and persistent state arguments.
5. Separate pathwise, expected, and tail resource constraints in the formal statement.
6. State precisely when an external public clock is free and what prevents that channel from carrying observation-dependent information.

Most importantly, the paper has no matching lower theorem for the complete resource vector. It explicitly says that a total persistent-budget law requires bounded overhead or a separate mandatory-state lower bound. This is mathematically honest, but it means that the full “resource–resolution–risk” title is ahead of the proved result. The proved matching law is for the intrinsic predictive-label cut, not for total memory or total implementation complexity.

---

## 6. Robust error floors

The two elementary witnesses in Proposition 4.2 are useful.

- If two calibration alternatives produce identical pre-terminal information and terminal Bernoulli means \(1/2\pm h\), the excess square loss relative to an oracle knowing the sign is \(h^2\).
- If an exact bit is replaced by an independent erasure with probability \(	heta\), the Bayes risk is \(	heta/4\), and fair imputation gives total-variation defect \(	heta/2\).

The conclusion drawn from these examples is not yet a formal minimax theorem. The paper refers to a declared class containing the alternatives, a geometry member, and a uniform upper bound, but it does not define one common class, one common resource index, and one minimax functional before asserting a four-term matched order. The fact that different terms may be witnessed by different class members is perfectly legitimate for a supremum minimax lower bound; it simply has to be written as such.

A revised proposition should define, for example,

```text
inf over algorithms with resource b
sup over experiments E in a specified class C
[common normalized risk or excess risk],
```

and then state all embeddings and normalizations explicitly. It should also prove that the erasure experiment has deficiency at least \(	heta/2\) within the declared simulator class, rather than only exhibiting a simulator with defect \(	heta/2\), if the defect is to serve as an unavoidable lower-order parameter.

Until this is done, the proposition demonstrates attainable examples, not closure of F2.

---

## 7. Audit of the binary-filter realization

The binary hidden-state filter is a clean test of the theorem.

The posterior update

```text
F_{a,y}(p)
  = r(1+ay) / [1+ay(2r-1)],
  r = q_0 + (1-2q_0)p,
```

has a denominator bounded below by \(1-a_+\). The terminal hidden-bit probe identifies the posterior \(p\), so the predictive quotient is not inferred from a covariance surrogate. The invariant posterior interval is plausible and the log-odds derivative is bounded by \(1-2q_0\). The observation update adds a report-dependent log-likelihood term and therefore preserves the same-input contraction.

The actual posterior-density bound is also correctly tied to the raw report law. The derivative of the posterior with respect to the continuous report has a positive lower bound depending on \(q_0,a_-,a_+\); change of variables gives a conditional posterior density upper bound; mixtures over actual histories preserve it. No uniform posterior distribution is inserted by hand.

The report total-variation calculation includes the necessary factor \(1/2\). The constants are correctly not claimed uniform as \(q_0\downarrow0\).

The implementation discussion should be more precise. An exact mathematical finite-label encoder may compare a real-valued report against Borel thresholds. A physical finite-precision program instead approximates the report and incurs a nonzero \(u_t\). The manuscript moves quickly between an “equally spaced rational grid,” a “rational update,” and a continuous real report. The exact-real and finite-bit models should be stated as separate algorithms with separate conclusions. The resource table partly does this, but the theorem itself should not describe exact arithmetic as an effective finite-precision implementation.

The example validates the theorem, but it is a uniformly contracting one-dimensional filter. Its principal ingredients are close to classical nonlinear-filter quantization. The new contribution is the matching task lower and the accounting, not the existence of a finite-state approximation by itself.

---

## 8. Audit of the singular absorbing-sensor realization

The second realization is mathematically distinct and addresses several important boundary cases.

The failure coin is independent of the hidden target, so after \(N\) attempts the unresolved mass is exactly

```text
h_N = (1-s)^N.
```

Conditioned on acquisition, the target law remains the prepared mixture. The predictive quotient glues equal absorbed futures and does not retain the latent component mark. The flag probe separates the unresolved mode from absorbed states.

The acquired law

```text
h_N delta_o
  + (1-h_N) sum_j pi_j (z_j)_# Unif(Q_j)
```

is therefore correct. Total variance gives

```text
B_N = b_* + h_N V_*.
```

At the successful report, the representative is overwritten once; failures and later calls are exact holds. Consequently the transport coefficients are disjoint indicators and the weighted energy identity has \(\Gamma_N=1\). This is the clearest illustration in the paper of why elapsed time and innovation count must not be conflated.

The intersecting-strata argument does not require the encoder to identify the latent mark. Widths may vanish without entering denominators. The theorem's budget threshold provides enough representatives for the unresolved point and the finite collection of charts.

I did not find a defect in these calculations. The limitation is conceptual breadth: the model is deliberately arranged so that one successful report reveals the complete target and all subsequent dynamics are identities. It proves a useful singular example, but it does not establish stability for recurrent acquisition with repeated partial information, alternating contraction and expansion, or evolving singular geometry. Those would be much stronger tests of the proposed framework.

---

## 9. Novelty and literature positioning

The manuscript is admirably careful not to claim priority for conditional-mean projection, predictive state representations, probability quantization, nonlinear-filter quantization, random-iteration contraction, or Blackwell comparison. Its current eight-item bibliography and short comparison table are nevertheless insufficient for a paper seeking a four-leading-general-journal placement as a foundational synthesis.

At minimum, the revised discussion must compare theorem statements and hypotheses with the following neighboring bodies of work.

1. **Causal states and minimal predictive representations.** Work of Shalizi and Crutchfield proves minimality and uniqueness properties for causal-state representations of stochastic processes. The present controlled, resource-typed quotient may differ, but that difference must be stated at theorem level rather than through the predictive-state-representation citation alone.
2. **Probabilistic bisimulation, behavioral pseudometrics, and state aggregation.** Work of Ferns, Panangaden, Precup, and others develops quantitative state similarity and approximation for controlled Markov processes. The relation between the manuscript's task metric, report-kernel continuity, and these behavioral metrics should be explained.
3. **Finite model approximation of MDPs and POMDPs.** Work of Saldi, Yüksel, Linder, and related authors quantizes belief-state control problems and proves near-optimality under continuity assumptions. The present fixed-exploration, same-task lower bound may be new relative to that literature, but the overlap in constructive belief-space quantization is substantial enough to require direct comparison.
4. **Le Cam deficiency and comparison of statistical experiments.** Blackwell is not the end of this literature. The paper should engage with Le Cam's randomization/deficiency framework and Torgersen's systematic treatment, including deficiencies restricted to classes of decision problems. The manuscript's causal strategy lifts and explicit resource maps may be a genuine refinement, but their relation to the classical theory must be formalized.
5. **Quantization of singular and mixed-dimensional measures.** Graf–Luschgy and one Ahlfors–David reference do not exhaust the relevant literature on quantization dimension, mixtures, lower-dimensional components, and singular measures. The finite-box lemma may still be useful, but its novelty and exact range should be positioned carefully.
6. **Nonlinear filtering and finite-state approximation.** The comparison should extend beyond the three numerical filtering papers currently cited and address constructive finite-state filters, stability-based approximation, and controlled observations.

I am not asserting that an existing theorem already contains the manuscript's exact acquisition-weighted innovation synthesis. I am asserting that the current submission has not performed the independent priority clearance needed to establish the claimed conceptual displacement at the four-leading-general-journal level.

---

## 10. Presentation and theorem architecture

The paper is only sixteen pages despite introducing a raw causal experiment, a predictive quotient, an acquired geometric decomposition, two encoder models, a transport cocycle, effective implementation, causal deficiency, a nine-coordinate resource vector, robust minimax witnesses, and two applications. The resulting compression hides assumptions in prose and makes some theorems appear broader than their formal data.

A stronger presentation would do the following.

1. Give a formal definition block for experiment, admissible strategy, predictive state, checkpoint encoder, online encoder, causal morphism, and resource-bounded risk.
2. Separate the pure mathematical finite-label model from the finite-bit effective implementation model.
3. State the main theorem first as a transfer theorem conditional on (G), (I), and (T), with all uniformity quantifiers explicit.
4. State a second structural theorem deriving (I) and (T) from natural kernel conditions. This is the missing theorem that would raise the paper's scale.
5. State the full resource upper theorem with every resource coordinate visible.
6. State a separate, fully quantified minimax lower theorem for whichever robust class is actually proved.
7. Move source-integrity and workflow material out of the mathematical narrative; retain it in the repository, where it is useful.
8. Add an appendix containing the continuous-report quotient lemma, all effective-algorithm pseudocode, and constants for the two realizations.

The title *General Theta Foundations I* is substantially broader than the proved setting: finite horizon, Bayesian preparation, fixed exploration, a finite squared-prediction menu, finitely many chart components, and a supplied weighted transport certificate. Either the mathematics should be broadened, or the title and abstract should describe the actual theorem class more narrowly.

---

## 11. Specific required revisions

The following are not optional editorial preferences; they are the minimum mathematical revisions I would require before recommending publication in a strong specialist venue.

### Major revision 1: repair the predictive-realization proposition

- Require the factor statistic to take values in a standard Borel or explicitly countably generated space.
- State and prove the measurable factorization lemma used.
- For continuous reports, formulate the instrument/density closure that permits pointwise normalized updates.
- Separate almost-sure conditional versions from continuous extensions on the declared valid domain.
- Verify that the continuation interface is included in every time-dependent quotient used by the theorem.

### Major revision 2: derive transport from a natural broader class

At least one theorem should permit recurrent active updates with nonuniform Lipschitz factors, including occasional expansion, and derive the weighted second-moment estimate from checkable conditions. Possible routes include regeneration, a Lyapunov drift for a positive matrix cocycle, a block-contraction condition with acquisition marks, or a spectral bound on a forced transfer operator. The exact method is open; the present contractive and absorbing examples are not sufficient for a foundational claim.

### Major revision 3: formalize the resource theory

- Define causal morphisms and serial composition completely.
- Define resource maps, their order, and their pathwise/expected/tail semantics.
- Keep all resource coordinates in the risk notation.
- Distinguish constructive state-product upper bounds from mandatory lower bounds.
- Prove a nontrivial matching lower for at least one growing simulator/controller/clock regime, or explicitly restrict the title to predictive-label resources.

### Major revision 4: turn the floor examples into a minimax theorem

- Define one robust class and one minimax risk.
- State common task, loss normalization, and oracle baseline.
- Quantify the embeddings of the geometry, calibration, and erasure subexperiments.
- Prove the relevant lower bound on simulator deficiency, not only an upper certificate.
- State clearly whether the four terms are simultaneously present in each member or are obtained through a supremum over different members.

### Major revision 5: complete theorem-level literature comparison

The revised paper should include explicit propositions or tables comparing assumptions and conclusions with causal states, predictive state representations, bisimulation metrics, belief-MDP quantization, nonlinear-filter approximation, Le Cam/Torgersen deficiency, and singular-measure quantization. Generic statements that the literatures are “classical” are not enough for a priority-sensitive general-journal submission.

### Major revision 6: separate exact and finite-precision algorithms

For both realizations, give the state-transition algorithm in pseudocode and state separately:

- the exact Borel finite-label encoder;
- the finite-precision executable approximation;
- the persistent bits, transient workspace, readonly data, calibration input, and clock state;
- the resulting \(u_t\), \(v_N^{\rm num}\), and report-law errors.

### Major revision 7: expose all quantifiers and constants

Index \(N\)-dependent charts and maps explicitly. State which constants may depend on \(J,d_*,D_0,\Delta,b,B,C_g,L\), and which are uniform in \(N,m,w_{N,j}\), and the positive widths. Avoid relying on prose scattered across the theorem, remarks, and audit files.

---

## 12. Minor and notational comments

1. The symbol \(A_t\) is used both for action spaces and for multiplicative transport coefficients. These should not share notation.
2. The symbol \(p_t\) denotes the general score vector and later the scalar filter posterior. The local reuse is understandable but unnecessary in a short paper with many interfaces.
3. The meaning of “positive kernel” should remain “nonnegative normalized kernel”; the paper usually says this correctly, but the terminology can suggest a strictly positive density.
4. The score metric and the predictive-state metric should always be distinguished typographically. In the sensor realization the predictive metric is chosen from the score vector; this is a special feature, not the general definition.
5. The exact dependence of constants on the separation \(\Delta\) in the separated theorem should be collected in one place.
6. The allocation set permits \(k_j=0\) and requires total allocation at least one. State explicitly how point components and duplicate representatives are counted.
7. The statement “the minimum is an algebraic comparison problem” applies only under the declared algebraic input model. The theorem should not imply this for arbitrary computable or oracle-presented real parameters.
8. The finite program description may grow with \(m\). A grid-generation program and a readonly table lead to different resource profiles; they should not be treated interchangeably.
9. The report-continuity norm convention is stated, but it would help to repeat whether total variation is \(\sup_A|P(A)-Q(A)|\) or one half of the \(L^1\) distance when densities are used.
10. The abstract's phrase “for every positive label budget” is accurate for the separated theorem, whereas the intersecting sensor theorem has a budget threshold. This distinction should be visible in the abstract.
11. The bibliography should be substantially enlarged and the literature comparison moved into the paper rather than left primarily in an auxiliary audit file.
12. The paper should state whether the terminal numerical error \(v_N^{\rm num}\) is deterministic, random but uniformly bounded, or measured in \(L^2\); the displayed use suggests a deterministic score-norm allowance.
13. When the clock is externally supplied, the model should specify that it is a fixed protocol value and cannot encode past observations through adaptive timing unless such timing is charged.
14. If a component has zero acquired weight, condition (T) forces its transport term to vanish almost surely. This useful consequence should be highlighted in the theorem statement because it is one of the framework's substantive consistency checks.
15. The source-integrity receipt is well designed, but the article should not cite the number of regression checks as evidence for mathematical correctness.

---

## 13. Positive assessment

The rejection recommendation should not obscure the manuscript's real strengths.

- It starts from a prepared causal experiment and an actual path law rather than a formal parameter manifold.
- It does not replace failed acquisitions by a success-conditioned clock.
- It separates the full-history Bayes baseline from the finite-label excess risk.
- It proves the quantization lower bound for arbitrary centers and actual component weights.
- It charges an omitted component rather than silently allocating every component a label.
- It correctly removes zero physical widths instead of introducing inverse singular constants.
- It identifies the exact accounting error caused by rounding on every inactive tick.
- It allows latent analytical marks without granting them to the implementation.
- It keeps common-loss total-variation transfer separate from regret relative to different oracles.
- It distinguishes persistent state, temporary workspace, program data, calibration, clock, acquisition count, and physical time.
- It supplies two kernel-level realizations with different causal mechanisms.
- Its source/provenance pipeline is non-destructive and unusually explicit about what the automated checks do not prove.

These are worthwhile contributions. With a more modest title and a rigorous expansion of the quotient, resource, and minimax layers, the paper could become a strong specialist contribution. With a new structural theorem deriving acquisition-weighted transport in a broad nonuniform class, it could become substantially more significant.

---

## 14. Final recommendation

I recommend **rejection at the four-leading-general-mathematics-journal level in the present form**.

The core risk inequality appears mathematically coherent under its stated certificates, and I found no fatal defect in the two realizations. The obstacle is that the manuscript's most difficult causal property is still assumed through a tailored weighted transport certificate, the complete resource lower theorem is not proved, the robust four-term match is conditional rather than formalized, and the novelty comparison is not yet adequate for a paper claiming foundational generality.

For a strong specialist journal, I recommend **major revision and resubmission**. The revision should preserve the acquired-law and innovation-localization insights, not dilute them. It should, however, distinguish sharply between:

1. the proved conditional transfer theorem;
2. structural conditions that imply its transport certificate;
3. the two current realizations;
4. the constructive resource upper accounting;
5. the still-open full-resource minimax problem.

A revision that merely adds exposition, more audit files, or more finite regression checks would not resolve the main objections. A revision that proves a broad nonuniform transport theorem and a genuinely typed full-resource minimax result would warrant a new general-journal assessment.
