# Referee Report — General Theta Foundations I, Revision 36

**Manuscript:** *General Theta Foundations I: Finite Alphabets, Spectral Gaps, and Hidden Memory*  
**Repository:** `TrillionniumFoundation/theta-theory`  
**Reviewed branch:** `revision/general-theta-foundations-i-v36-referee-ready-2026-09-25`  
**Reviewed head:** `1a08578710d55a2379cea56c43feb5eca56340a2`  
**Native mathematical source recorded by the manuscript:** `d60efb58807c3feffa01065e698d1fa9fe140802`  
**Controlling previous report:** `6da551c5b804b683240d5f5631e1c4f5689e21bd`  
**Previous reviewed manuscript:** `aabc0731a0c913f7b9e75e6efc08f7af665bdf23`  
**Review branch:** `review/general-theta-foundations-i-v36-finite-alphabet-memory-pipeline-harsh-top4-r21-2026-09-25`  
**Date:** 25 September 2026

## Recommendation

**Reject at the Annals / Inventiones / JAMS / Acta level.**

Revision 36 is a substantial mathematical response to the twentieth report. It repairs the full-word/product quantifier gap in the packet lemma, replaces the uncountable orthogonal-command comparison by genuinely finite alphabets, proves a finite-generator spectral-gap theorem, supplies an explicit five-letter rational noncommuting example, gives an exact one-qubit realization of the same numerical behavior, extends the sharp cube-root law to a structured noncommuting monomial class, and adds a separately charged finite-coin implementation.

I did not find a short fatal counterexample to the principal new arguments. In the nonuniform, finite-horizon, wordwise, clocked, atomic stochastic-row model actually defined, the corrected full-word contraction lemma, the spectral-gap-to-Lipschitz-mixing step, the spherical quantization estimate, the packet occupation bound, the rational spherical synthesis, the explicit `SU(2)` gate application, the resonant monomial construction, and the sparse dyadic compiler appear internally coherent. The negative recommendation is therefore **not** based on an allegation that the displayed theorems are false.

The four-journal case nevertheless fails for decisive reasons.

1. The principal spectral-gap theorem does not determine the sharp state-cardinality order. It proves only

   ```text
   c (N/log(N+1))^((d-1)/2)
       <= W_(N,epsilon)
       <= C N^((d-1)/2).
   ```

   The logarithmic gap is not a cosmetic constant. It records the unresolved cost of converting finite-generator mixing into a compatible exact realization. In the explicit three-dimensional rational example the main conclusion remains `c N/log N <= W_N <= C N`, with no matching construction or converse.
2. The proof is a synthesis of three ingredients of very different status: the deep Bourgain--Gamburd spectral-gap theorem, classical spherical quantization/covering at rate `k^(-2/(d-1))`, and a short endpoint-compression inequality. The last ingredient is useful and apparently new in this formulation, but the article does not develop a general representation-theoretic or information-theoretic classification commensurate with the breadth suggested by its title.
3. The explicit quantum comparison uses a highly specialized objective: uniform, wordwise approximation of numerical terminal probabilities by a horizon-specific nonuniform classical transducer. It is correctly distinguished from strict-cutpoint language simulation, but that distinction also limits the significance of the claimed memory separation. In persistent bits, the rational sphere example gives one qubit versus `log_2 N + O(log log N)` classical bits, not one qubit versus linear classical space.
4. The matched noncommuting monomial theorem does not obtain its lower bound from genuinely noncommutative dynamics. Its converse restricts to the inherited cyclic subalphabet `{Id,A}`; noncommutativity enters only in proving that the sparse upper machine handles the enlarged alphabet. This is a valid closure result, not a noncommutative lower-bound theory.
5. The finite-coin compiler is an implementation lemma in a self-paced nonuniform interface. It is based on standard dyadic comparison and union-bound error accumulation, leaves the threshold tables and their construction free, and needs an explicit convention preventing update duration from becoming a side channel to an adaptive environment. It does not convert the paper into a uniform probabilistic-space theorem.
6. The primary resource model remains permissive: the epoch and horizon are free; all transition tables and arithmetic are uncharged; exact real stochastic kernels are atomic; rows may depend on the layer and horizon; the final decoder may depend on `N`; and only one terminal coordinate query is required. This is a legitimate positive-realization width, not ordinary streaming space, total branching-program size, or autonomous finite-state complexity.
7. The repository-wide Foundations pipeline remains unchanged at every difficult analytic gate. The manuscript's own status file leaves the A2 replacement, B4 and C2 aggregates, the eleven-paper aggregate, fully adaptive collision scheduling, noisy-tag composition, all-irrational classification, and the sharp spectral-gap order open.

Revision 36 is a serious specialist-paper candidate. It is not close to the standard of the four leading general mathematics journals. The “General Theta Foundations I” branding continues to overstate both the theorem's generality and its relation to the repository's principal analytic program.

---

## 1. Scope of this review

I reviewed the focused Revision 36 article and the repository records needed to evaluate both its local mathematics and its position in the larger pipeline. In particular, I examined:

- `papers/GTF-I-v36-finite-alphabet-memory/main.tex`;
- `introduction.tex`;
- `machine-model.tex`;
- `word-packets.tex`;
- `spectral-width.tex`;
- `rational-gates.tex`;
- `monomial-width.tex`;
- `finite-coins.tex`;
- `comparison.tex`;
- `references.tex`;
- `RESPONSE_TO_REFEREE.md`;
- `LITERATURE_AUDIT.md`;
- `HISTORY_AUDIT.md`;
- `RESOURCE_LEDGER.md`;
- `PROOF_STATUS.json`;
- `PIPELINE_STATUS.json`;
- `verify.py` and the executed build records;
- the complete twentieth referee report;
- the Revision 35 packet and resonant-polygon proofs reused or generalized here;
- the repository-level `ROUND17_PROOF_DEPENDENCY_LEDGER.md`.

I also made a targeted comparison with the directly relevant literature on:

- algebraic spectral gaps for finitely generated compact groups;
- vector quantization and covering on spheres and compact manifolds;
- probabilistic ordered branching programs;
- quantum finite automata and strict-cutpoint simulation;
- classical-versus-quantum memory in stochastic-process simulation.

This was a targeted audit, not an assertion of exhaustive priority clearance.

The publication genealogy is clean. Revision 36 descends from the controlling r20 report, preserves Revision 35 as supporting material, and adds a branch-specific package rather than overwriting prior manuscripts. That is good repository practice. It is not evidence for correctness, priority, or journal significance.

The 13-page article is sufficiently self-contained to audit its new claims. The 463-page mathematical archive and 1016-page development archive are therefore optional provenance records, not proof supplements that increase the mathematical weight of the submission. I did not treat regression counts, source hashes, negative controls, page comparisons, or successful compilation as substitutes for proof.

---

## 2. What Revision 36 genuinely repairs

### 2.1 The word/product gap is repaired correctly

The previous report identified a formal mismatch: the packet lemma assumed that an endpoint kernel depended only on the group product, while the proposed machine could process and remember the spelling of the whole word.

Revision 36 now introduces a fresh packet word `W`, a many-to-one ordered product map `g(W)`, and an arbitrary word-dependent endpoint kernel

```text
P(S'=r | sigma(Y,S,W)) = T_W(S,r).
```

The proof keeps `T_W` through the endpoint-centroid identity. It removes the word-dependent assignment only by taking a pointwise maximum over endpoint directions. Only after that maximum does it push the word law forward to the product distribution.

This is the correct repair. Equal-product words may induce different kernels, and no product-sufficiency assumption is used. The accompanying collision remark also correctly explains why independence of the product alone would not be enough: the spelling could be correlated with the past and leak it even when the product is fixed.

### 2.2 The finite-alphabet restriction is now real rather than rhetorical

Revision 35's compact-command theorem allowed an arbitrary real orthogonal matrix as one external symbol. Revision 36 instead charges every letter from a fixed finite alphabet. Its spectral lower bound uses packets of

```text
B_k = O(log(k+1))
```

ordinary command slots to approach the spherical distribution at the spatial resolution relevant to `k` endpoint labels.

This is an important conceptual improvement. A Haar-distributed rotation is not smuggled in as one command, and the logarithmic mixing time is explicitly paid.

### 2.3 The explicit five-gate example is genuinely finite and rational

The matrices `R_x` and `R_z` have rational entries, the alphabet has five symbols including inverses and the identity, the seed and query alphabets are fixed, and all target response probabilities remain in `[9/20,11/20]` for every horizon.

The `SU(2)` lifts are algebraic. Their powers are dense in the two axial one-parameter subgroups, and those connected subgroups generate `SU(2)`. Subject to the cited Bourgain--Gamburd theorem, the symmetric lazy walk has an `L^2` spectral gap; the sphere action inherits it as a homogeneous quotient.

Thus the paper obtains a concrete finite classical experiment with separate positive minimum four and compatible width growing almost linearly in `N`.

### 2.4 The qubit comparison is operationally explicit

The paper does not merely invoke the Bloch sphere metaphor. It gives the seed density matrices, the two fixed command unitaries and their inverses, and the Pauli queries. A single qubit exactly realizes every specified conditional probability.

The manuscript also correctly states why this does not contradict a constant-state strict-cutpoint PFA simulation. The cited conversion preserves signs relative to a cutpoint while attenuating the numerical margin by a length-dependent positive factor. That is enough for language recognition and useless for a fixed wordwise probability tolerance.

### 2.5 A structured noncommuting class has a matched order

The resonant monomial theorem handles finite commands that permute modes, conjugate them, and apply bounded integral powers of one badly approximable phase. It proves an all-hidden-state cube-root lower bound and gives a sparse exact cube-root upper construction for the entire alphabet.

The upper construction is not a dense redraw disguised as a sparse row. The charged mode index, polygon label, adjacent-vertex interpolation, and antipodal mixture are all explicit, and no free zero state is used.

### 2.6 The finite-coin implementation is more honest than the atomic model alone

The compiler charges the old label, current input, binary-tree node, bit position, and ready/query phases. It does not claim zero-error finite-bit sampling of irrational rows. For fixed tolerance it preserves the leading logarithmic coefficient of persistent label bits.

These improvements answer the principal formal and modeling objections in r20. They do not establish top-four depth.

---

## 3. Technical audit of the common model

### 3.1 The nonuniform clocked transducer is defined clearly

For a prescribed horizon, the paper gives cut-dependent state alphabets, initialization rows, one stochastic transition matrix per command and layer, and terminal decoder columns. The error is the maximum binary total variation over every seed, complete command word, and query.

The seed and query are atomic external symbols. Only the updated register persists. Private randomness that survives an update must be represented in the register. Padding counts as available labels.

The following resources remain free:

- the epoch and horizon;
- the complete transition tables;
- construction and lookup of those tables;
- exact arithmetic;
- exact sampling of an atomic stochastic row.

The paper now calls this a nonuniform probabilistic ordered read-once program rather than ordinary algorithmic memory. That is the right classification.

### 3.2 The separate positive minimum is correctly computed

The residual rows are affine in the predictive vector `rho U_w x`. Identity prefixes generated from `±e_j` span the full `d`-dimensional affine family, and idle suffixes with coordinate queries distinguish its coordinates. Normalization adds the constant direction, giving ordinary normalized rank `d+1`.

A regular simplex centered at zero with inradius `rho` and circumradius `d rho < 1` encloses every reachable predictive vector. Its vertices define legal future binary channels under every orthogonal suffix. The selected-cut factorization is embedded into a complete finite machine by storing raw prefixes or suffixes elsewhere.

This proves the separate minimum claimed. It does not provide a small simultaneous machine, and the article does not confuse the two.

### 3.3 Terminal calibration is valid

Combining the `d` decoder columns into a proof-side vector does not ask the machine to emit `d` joint answers. Each column is the mean associated with a separate atomic query.

Uniform binary TV error `epsilon` changes each coordinate mean by at most `2 epsilon`, so the combined vector error is at most `2 sqrt(d) epsilon`. The final correlation with the unit orbit vector yields

```text
q_N >= rho/sqrt(d) - 2 epsilon.
```

The normalization is conservative but correct.

---

## 4. Technical audit of the full-word packet theorem

### 4.1 The conditioning statement is now the right one

The packet word is independent of the old orbit variable, old register, and private randomness. Conditional on the old state and the entire word, the internal packet computation integrates into a stochastic endpoint kernel `T_W`.

The lemma neither assumes that the endpoint law depends only on the product nor that distinct spellings with equal product are operationally indistinguishable.

### 4.2 The centroid calculation is correct

Writing `z_s=E[Y|S=s]`, the unnormalized endpoint centroid is

```text
p'_r z'_r
  = sum_s p_s int T_w(s,r) U_(g(w)) z_s dnu(w).
```

Choosing the unit direction of each endpoint centroid and summing inner products recovers the retained amplitude. Replacing the stochastic assignment by a pointwise maximum over endpoint directions can only increase it.

For each nonzero old centroid direction, the resulting integral is at most `1-Gamma_k(mu)`. Summing over old states proves the contraction.

The argument covers arbitrary hidden directions and arbitrary internal widths inside the packet. Only the endpoint register is bounded.

### 4.3 The packet budget follows

Fresh disjoint words allow the contraction factors to multiply. Fixed commands between packets cannot increase conditional-mean norm by Jensen's inequality. The terminal correlation enforces positive surviving amplitude.

The resulting product and logarithmic budgets are correct. The public test-word distribution may be selected after the advertised profile is known because the simulator is required to work on every word. It may not depend on the private trajectory, and the theorem does not allow that.

---

## 5. The finite spectral-gap theorem

### 5.1 The analytic hypothesis is strong and correctly stated

The paper assumes a full mean-zero `L^2` operator-norm bound on the sphere, not merely contraction in the defining finite-dimensional representation. Density of the generated subgroup is not substituted for a spectral gap.

This distinction matters. A finite set can mix low harmonics while leaving high harmonics essentially invariant. The manuscript's negative controls and prose correctly reject finite matrix-spectrum checks as proof of the infinite-dimensional gap.

### 5.2 `L^2` mixing is converted to uniform Lipschitz mixing correctly

The action preserves Lipschitz constants. If `h=P^B f-sigma f`, then `||h||_2<=lambda^B`. Averaging the Lipschitz bound over a small spherical cap gives

```text
|h(v)| <= r + C r^(-m/2) lambda^B.
```

Choosing `r=lambda^(2B/(m+2))` gives the displayed uniform estimate. The special `S^2` cap computation and constant are consistent.

This is a standard smoothing argument, but it is applied correctly.

### 5.3 The spherical distortion bound is classical in substance

For `k` centers, caps of radius proportional to `k^(-1/m)` cover at most half the sphere. On the complement, the cosine loss is proportional to the squared radius. Hence the spherical average distortion is at least a constant times

```text
k^(-2/m).
```

Uniform mixing transfers this lower bound to a finite product law after `B_k=O(log k)` letters.

The mathematics is correct. The presentation should, however, connect this quantity explicitly to classical vector quantization and spherical covering. The exponent `2/m` is not a new geometric rate. Zador-type quantization theory, Graf--Luschgy's framework, and manifold quantization results are the natural context. The paper currently labels the geometric mechanism classical but does not provide a theorem-level map.

### 5.4 The lower and occupation bounds follow

Disjoint length-`B_k` iid packets each lose at least `c k^(-2/m)` amplitude when the endpoint has at most `k` labels. The packet budget gives

```text
floor(N/B_k) c k^(-2/m) <= log(1/kappa_d).
```

This yields the stated peak lower bound. The greedy interval selection used for the occupation estimate removes at most `B_k` eligible endpoints per selected packet and is valid even when the other cuts have arbitrarily large width.

### 5.5 The exact upper construction is correct but leaves the central logarithm unexplained

A rational stereographic grid gives a spherical net of cardinality `O(N^(m/2))`; its convex hull contains a ball of radius `1-1/(8N)`. Scaling the associated state vectors by `eta_N^(-t)/4` allows every orthogonal command to be implemented by a convex row while keeping the final decoder bounded.

For rational input data, each row is a rational linear feasibility problem and a basic solution has at most `d+1` successors.

This is a clean exact construction. It is also geometrically generic: it ignores the finite generating set and its mixing. The unresolved question is whether finite-generator structure can reduce the upper width by the same logarithmic factor paid in the converse, or whether the converse can avoid the mixing-time loss. The paper determines only the polynomial exponent.

---

## 6. The explicit rational gates

### 6.1 The density argument is credible

The two `SU(2)` lifts have algebraic entries and infinite-order eigenphases. Their closures contain the `x`- and `z`-axis one-parameter subgroups. The corresponding Lie algebras generate `su(2)`, so the closed subgroup they generate is `SU(2)`.

The symmetric support includes inverses. Bourgain--Gamburd's algebraic dense-generator theorem therefore supplies a spectral gap on `SU(2)`. Adding laziness converts it into an absolute norm gap, and restriction to the homogeneous sphere quotient preserves the bound.

I do not see a short defect in this application.

### 6.2 “Explicit” does not mean quantitatively effective here

The five matrices are explicit, and the asymptotic existence of a gap follows from a deep external theorem. The manuscript does not give a numerical value or computable lower bound for `1-lambda`.

Consequently, the constants in

```text
c_epsilon N/log(N+1) <= W_N <= C N
```

and the finite excluded-horizon formula are not numerically instantiated. The theorem is explicit at the level of the generating matrices and qualitative asymptotics, not at the level of an effective classical-memory threshold.

That is not a correctness problem, but it materially limits the force of the “explicit rational family” claim.

### 6.3 The hard external input carries much of the breadth

The move from the planar cyclic example to a finite dense noncommuting alphabet is enabled by the Bourgain--Gamburd gap. The paper's new contribution is the packet-compression consequence of such a gap, not a new expansion theorem.

For top-four depth one would expect a broader structural theorem—for example, a criterion in representation-theoretic terms that determines the exact width order, or a sharp converse/upper construction for a substantial class of finite actions. Revision 36 supplies neither.

---

## 7. The qubit comparison

### 7.1 The exact qubit implementation is correct

The seed density matrix has Bloch vector `rho x`. The command unitaries induce the stated rational rotations. Measuring the appropriate Pauli observable gives exactly the target binary law.

Seed-reset and query operations fit a general one-way quantum automaton with completely positive updates. The protocol's numerical behavior is therefore realized by a fixed one-qubit system.

### 7.2 The strict-cutpoint comparison is properly separated

For a fixed cutpoint, the current Chen--Wu conversion yields a constant-state PFA for the threshold language of a fixed two-dimensional quantum automaton. Its stochasticization attenuates the acceptance margin with length while preserving its sign.

Revision 36 correctly explains why this does not approximate the numerical probabilities with fixed error. There is no contradiction.

### 7.3 The significance must be stated in the correct memory unit

The classical lower bound is on state cardinality. In three dimensions it is of order at least `N/log N`. Encoding a label therefore requires

```text
log_2 N - log_2 log N + O(1)
```

bits. The comparison is consequently one qubit versus logarithmically growing classical persistent bits.

This is a genuine unbounded separation. It should not be advertised as one qubit versus linear classical memory without saying “linear number of labels.” The article's finite-coin corollary largely makes this distinction, but the headline discussion should be equally explicit.

### 7.4 The broader quantum-memory literature is still underdeveloped

The paper now gives a careful QFA comparison, which is a major improvement. It still does not adequately situate the result relative to quantum models of stochastic processes and known quantum memory advantages in process simulation.

Those works often optimize stationary entropy, support dimension, or generated-process fidelity rather than worst-case wordwise transducer width, so they do not subsume this theorem. Precisely for that reason, the article should include a short theorem-level comparison instead of leaving the impression that strict-cutpoint QFA simulation is the only adjacent quantum-memory framework.

---

## 8. The resonant monomial theorem

### 8.1 The lower bound is valid but one-dimensional

The converse restricts the alphabet to the identity and a single irrational rotation on one mode. On that sublanguage, the Revision 35 separated packet gives the cube-root lower bound.

This is legitimate: a machine for the full alphabet must realize every restricted word. It is also important for the novelty assessment. The lower-bound difficulty remains the cyclic planar problem already solved in Revision 35. No genuinely noncommutative packet obstruction is proved.

### 8.2 The upper construction handles the full alphabet

The register stores a mode and a resonant polygon index. Permutations move the mode; conjugations reverse the polygon index; bounded powers of the irrational phase are implemented by adjacent-vertex interpolation. An antipodal mixture equalizes the radial factor across commands.

The expected associated vector follows every full monomial command exactly, the rows have at most four successors, and the final decoder remains bounded when the convergent denominator is chosen at cube-root scale.

This is a neat sparse closure construction.

### 8.3 The “no character” proposition should not be oversold

The generated compact closure can be noncommutative and irreducible, and every continuous one-dimensional character is trivial on the connected rotation torus. That proves the theorem is not formally obtained by applying a character of the full group.

Nevertheless, the converse explicitly uses a cyclic subgroup and the upper bound explicitly uses monomial coordinates. The result does not reveal a new nonabelian obstruction invariant or classify finite noncommuting alphabets. It shows that an abelian hard sublanguage can survive inside a noncommuting family whose remaining commands admit a sparse implementation.

---

## 9. The finite-coin compiler

### 9.1 The state accounting is mostly sound

A sparse categorical row can be decomposed into at most `L-1` conditional Bernoulli decisions. Rounding each conditional probability to `b` dyadic bits gives row-TV error at most `(L-1)2^(-b)` by a natural coupling.

A comparison with a fixed `b`-bit threshold needs only the threshold position while prefixes agree; it need not retain the entire sampled prefix. Charging the old label, current input, decision-tree node, bit position, and ready states gives the stated multiplicative `K(b+1)` label overhead.

Error accumulation under TV contraction gives the advertised fixed terminal tolerance.

### 9.2 The self-paced timing convention needs one more sentence—or padding

The bitwise comparison may stop early. If an interactive environment is allowed to observe the number of microsteps before the ready signal and choose the next command accordingly, private random bits leak through timing. That interaction is outside the original wordwise model.

The theorem should state explicitly that the external command word is fixed independently of update duration and that only ready-boundary symbols are observable. An equally clean repair is to pad every update to exactly `(L-1)b` fair-bit microsteps. The bit-position control already present makes such padding straightforward.

This is a minor interface issue, not a defect in the main atomic-width theorem.

### 9.3 The implementation theorem is not itself deep

Dyadic rounding, threshold comparison, sparse decision trees, and TV coupling are standard. The value of the proposition is honest resource bookkeeping for the manuscript's constructions. It should remain an implementation appendix or corollary rather than part of the primary originality case.

---

## 10. The central unresolved mathematical question

The paper now contains two finite noncommuting classes:

1. spectral-gap actions on a sphere, with width between

   ```text
   (N/log N)^((d-1)/2) and N^((d-1)/2);
   ```

2. resonant monomial actions, with matched cube-root width.

This is useful evidence that orbit geometry and command structure affect memory growth. It is not a classification.

The manuscript does not answer:

- whether every finite spectral-gap action has the lower or upper state-cardinality order;
- whether the logarithmic factor is necessary;
- whether a finite alphabet can realize other exponents;
- which representation-theoretic properties determine width;
- whether the optimal construction can exploit the same mixing that powers the lower bound;
- how the answer changes for multiple queries, adaptive commands, or uniform machines;
- whether there is a general direct-sum, tensor, or product law for these widths.

The title “Finite Alphabets, Spectral Gaps, and Hidden Memory” accurately names the ingredients but not a completed theory. The broad “General Theta Foundations I” prefix is still unjustified.

---

## 11. Originality and literature boundary

### 11.1 Classical quantization must be mapped explicitly

The quantity `Gamma_k(mu)` is a one-shot `k`-center distortion under cosine loss. Under spherical measure its order `k^(-2/(d-1))` belongs to classical quantization and covering theory.

The paper needs a direct comparison with Zador asymptotics, Graf--Luschgy's quantization framework, and quantization on compact manifolds. The elementary cap proof is self-contained, but self-contained proof does not make the exponent or geometric mechanism new.

The potentially new statement is the causal packet-compression consequence, not the spherical rate.

### 11.2 The branching-program comparison is improved but not complete

Revision 36 correctly calls the model a nonuniform stochastic ordered read-once program and recalls matrix Fourier coefficients for Boolean input. It distinguishes arbitrary stochastic rows from regular or permutation programs.

A specialist submission should still state exactly whether existing lower-bound, fooling-distribution, or width-hierarchy results for randomized OBDDs imply any special cases. The current discussion focuses mainly on pseudorandomness and Fourier growth, not on numerical real-valued behavior simulation.

### 11.3 Quantum memory comparisons need more than QFA language simulation

The Chen--Wu comparison is direct and useful. The broader literature on quantum simulation of stochastic processes, including dimension and entropy advantages, is adjacent enough to merit explicit discussion.

The objectives differ sharply: stationary generated processes versus externally driven words; average memory versus worst-case labels; exact process statistics versus terminal behavior. A careful paragraph stating these differences would strengthen, not weaken, the paper's novelty claim.

### 11.4 No independent priority certification has been obtained

The manuscript's own status files correctly say so. The repository's internal review sequence is provenance, not external peer review. Twenty prior reports do not substitute for an independent expert assessment in positive systems, branching programs, compact-group random walks, or quantum automata.

---

## 12. Resource interpretation

The primary quantity is the maximum number of available labels at a declared macro cut. It is not:

- total program size;
- transition-table size;
- construction complexity;
- arithmetic workspace;
- random-bit complexity;
- autonomous state count across all phases;
- uniform streaming space;
- total branching-program size.

The exact upper machines may use common command rows, but their state alphabet and final decoder are selected for the horizon. The lower machines may be redesigned for every `N` and may use unrelated rows at every layer.

The fair-bit compiler introduces a different self-paced interface and only fixed-error approximation. It leaves nonuniform threshold tables free.

These conventions are legitimate. They substantially narrow the interpretation of “memory,” and the abstract and introduction should keep them visible whenever the quantum comparison is emphasized.

---

## 13. Pipeline assessment

The Round-Seventeen repository ledger still contains two principal chains:

```text
A2 -> A3 -> A4 -> C2 -> D1
```

and

```text
B2-GC -> B1 -> B2-MC -> B3 -> B4 -> C1/C2 -> D1.
```

Their unresolved obligations involve, among other things:

- branchwise Fourier analysis and raw local limit theory;
- stopped large deviations and compact rate sublevels;
- one global kernel and common-domain projection identities;
- nonlinear semigroup and resolvent range arguments;
- graph cores and Mosco limits;
- exact filtering and measurable selection;
- changing-filtration optional projection;
- labelled large deviations and typed contraction.

Revision 36 proves no theorem in those chains. Its local proof edges are:

```text
full-word packet contraction
  -> finite spectral-gap mixing
  -> orbit distortion
  -> width/occupation;

explicit algebraic gates
  -> external Bourgain--Gamburd gap
  -> rational finite-alphabet width
  -> qubit numerical behavior;

cyclic hard sublanguage
  -> monomial sparse upper
  -> matched structured class;

sparse atomic rows
  -> dyadic compiler
  -> finite-coin bit rate.
```

These are genuine local mathematical consequences. They do not replace A2, close B4 or C2, close the eleven-paper aggregate, solve fully adaptive collision validation, or provide the missing noisy-tag theorem.

The repository history is therefore context, not additional weight for this submission. The focused article must stand alone, and for its local claims it largely does.

---

## 14. Minimum changes for a credible specialist submission

These are not a route to acceptance at a top-four general journal. They are the minimum changes needed for a fair specialist evaluation.

### 14.1 Retitle and reposition

Remove “General Theta Foundations I.” A defensible title would identify finite-alphabet stochastic transducers, packet compression, or classical simulation of orthogonal command experiments.

### 14.2 Choose one central theorem spine

The paper currently combines:

- a general spectral-gap theorem;
- an explicit rational qubit/classical example;
- a monomial cube-root theorem;
- a finite-coin compiler.

A stronger article would make the spectral-gap theorem and explicit example central, move the monomial closure and compiler to appendices or a companion note, and explain the one mathematical question that unifies them.

### 14.3 Add a theorem-level quantization comparison

Identify `Gamma_k` with a cosine-loss quantization problem, cite the relevant sharp asymptotics, and state precisely which part of the causal packet theorem is new.

### 14.4 Clarify the quantum-memory claim

State the separation simultaneously in labels, classical bits, and quantum dimension. Explain that it concerns worst-case wordwise numerical behavior and a horizon-dependent nonuniform classical simulator. Compare briefly with quantum stochastic-process memory results.

### 14.5 Address the logarithmic state-cardinality gap

Either close the gap for spectral-gap alphabets or present it as the paper's principal open problem. A matching upper construction, a stronger lower bound, or an example proving the logarithm necessary would materially deepen the work.

### 14.6 Make the external gap input quantitatively honest

Keep “explicit rational generators” but distinguish it from “effective numerical lower constant.” State whether any effective bound can be extracted from the cited theorem for the displayed gates.

### 14.7 Fix the finite-coin timing convention

Declare update duration unobservable to the command source, or pad each update to a fixed microstep length. Keep the atomic and compiled resources separate.

### 14.8 Remove archival volume from the editorial case

Retain the cumulative PDFs in the repository if desired, but do not ask an editor or referee to treat a thousand-page development archive as support for a 13-page theorem paper.

### 14.9 Obtain an independent priority audit

A specialist in at least two of positive realization, branching programs, compact-group random walks, quantization, and quantum automata should assess the novelty boundary before further priority claims are sharpened.

---

## 15. Specific major and minor points

1. **Keep the full-word formulation.** The corrected `T_W` lemma is the right statement; do not revert to product-sufficient language in summaries.
2. **Define the order of group products once.** Right-versus-left action conventions should be fixed before the first packet theorem.
3. **State whether `Gamma_k` permits repeated centers.** It makes no difference, but a formal definition should say so.
4. **Cite quantization theory where the `k^(-2/m)` rate first appears.**
5. **Do not call the spectral theorem sharp.** Only the logarithmic exponent is sharp.
6. **Distinguish state cardinality from memory bits in the abstract.**
7. **State that the lower constant in the rational-gate theorem depends on an unevaluated spectral gap.**
8. **Do not use finite matrix computations as evidence for the `L^2` gap.** The manuscript currently avoids this; preserve that restraint.
9. **Clarify the quotient convention in the `SU(2)`-to-sphere passage.** One sentence fixing left/right actions would remove an avoidable ambiguity.
10. **State the exact quantum automaton model in the proposition title.** The seed operation is a reset channel, not a unitary measure-once transition.
11. **Do not summarize the qubit result as a language-state separation.** It is a numerical behavior separation.
12. **Give both label and bit lower bounds for the explicit family.**
13. **Qualify “noncommuting lower bound.”** The monomial converse uses a cyclic sublanguage.
14. **Separate irreducibility from hardness.** The full representation is irreducible, but the lower witness occupies one mode.
15. **Explain whether the monomial constants are uniform in the selected finite alphabet.** They are not uniform as `M` or `r` varies.
16. **Clarify the seed count in the monomial section.** The notation `(±1±i)e_j` should explicitly mean all four sign choices.
17. **State whether the dyadic compiler pads early comparisons.** This resolves the timing-channel issue.
18. **Do not call the compiler exact.** It is fixed-error except for already dyadic rows.
19. **Keep the self-paced interface distinct from the macro atomic model.**
20. **State table-storage assumptions beside the bit-rate corollary.**
21. **Do not infer an efficient algorithm from rational feasibility.** Basic solutions exist, but table generation may be expensive.
22. **Give the dependence of constants on `d`, the gap, signal, and tolerance in one place.**
23. **Avoid saying the sphere example is almost linear memory without specifying labels.**
24. **Keep all-irrational classification listed as open.** The spectral and badly approximable cases do not cover every irrational cyclic action.
25. **Do not conflate adaptive input design with a proof-side test distribution.**
26. **Move internal pipeline labels out of the mathematical conclusion.**
27. **Do not use archive size, regression count, or revision count as significance evidence.**
28. **Add a neutral contribution table.** Separate new packet consequences, external spectral input, classical geometry, inherited rotation results, and implementation lemmas.
29. **Remove the Foundations branding.** It remains editorially misleading.
30. **Seek a specialist venue.** Positive systems, stochastic realization, theoretical computer science, compact-group random walks, or quantum information are the natural homes.

---

## 16. Scorecard

| Criterion | Assessment |
|---|---|
| Correctness in the stated model | Main new arguments appear coherent; no short fatal counterexample found |
| Advance over Revision 35 | Substantial: formal repair, finite alphabets, explicit rational gates, quantum comparison, structured noncommuting class |
| Originality boundary | Plausible specialist novelty, but quantization and quantum-process literatures are incompletely mapped |
| Mathematical depth | Serious specialist level; below top-four general-journal level |
| Spectral-gap quantitative strength | Polynomial exponent determined; logarithmic state-cardinality gap remains |
| Explicitness | Gates and upper rows explicit; lower spectral constant not numerically effective |
| Generality | Fixed orthogonal command experiments, one terminal coordinate query, nonuniform horizon-specific machines |
| Quantum comparison | Genuine numerical-behavior separation; not a new strict-cutpoint theorem and only logarithmic in classical bits |
| Monomial theorem | Matched order for a structured class; lower bound inherited from a cyclic sublanguage |
| Finite-coin result | Honest bookkeeping, but standard and interface-dependent |
| Pipeline impact | None on the decisive A2/B4/C2/D1 analytic gates |
| Presentation | Focused and technically improved; branding and theorem bundle remain disproportionate |
| Reproducibility engineering | Strong, but irrelevant to proof, originality, and journal level |
| Editorial recommendation | Reject at top-four level; consider only after specialist repositioning |

---

## 17. Final assessment

Revision 36 is a strong response to the previous report. The word/product gap is repaired rather than papered over. The finite-alphabet spectral theorem is mathematically meaningful. The five rational commands and exact qubit comparator make the abstract framework concrete. The monomial upper construction is technically neat, and the resource accounting is substantially more honest than in the early revisions.

That is the positive assessment.

The negative assessment is equally clear. The principal spectral class still has an unresolved logarithmic state-cardinality gap. Much of its breadth comes from a deep external expansion theorem and a classical quantization rate. The quantum comparison uses a narrow numerical-behavior objective and gives logarithmic classical bit growth. The matched noncommuting class derives its converse from an inherited abelian sublanguage. The finite-coin result is implementation bookkeeping. The model remains nonuniform and permissive. The larger repository pipeline remains open.

Put bluntly: **Revision 36 has produced a credible finite-alphabet specialist theory, but it has not produced a general foundation of hidden memory, nor a result of Annals/Inventiones/JAMS/Acta scale.**

My recommendation is therefore firm:

**Reject for Annals of Mathematics, Inventiones Mathematicae, Journal of the AMS, or Acta Mathematica.**

A retitled, literature-complete paper centered on finite-alphabet packet compression and classical simulation of orthogonal command experiments could merit serious specialist review. That should be treated as a new editorial submission, not another internal revision under the claim that the manuscript is approaching the four-journal threshold.
