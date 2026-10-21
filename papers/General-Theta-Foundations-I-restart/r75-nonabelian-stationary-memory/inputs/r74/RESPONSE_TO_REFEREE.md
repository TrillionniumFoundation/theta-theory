# Response to the controlling referee report — General Theta Foundations I, R74

## Author revision, controlling objects, and contribution

This is an author revision of **General Theta Foundations I: Acquired Geometry and Causal Resource Transfer**, by Qian Qi. Its scientific identity and its research objective at the level of Annals of Mathematics, Acta Mathematica, Inventiones Mathematicae, and the Journal of the American Mathematical Society are unchanged. The response to a concern about mathematical contribution must be stronger proved mathematics, with accurate attribution and scope. A longer proof, a new title, a different journal target, a larger archive, or an author-issued assessment of importance cannot discharge that concern.

The continuation begins from the complete R73 mathematical source, not from a version number or a recovery label. The controlling identities are:

| Object | Immutable identity and role |
|---|---|
| R73 mathematical source | Commit `e9d5f2765a2369ed7e136ca02e47fda8f3e9a49b`; paper path `papers/General-Theta-Foundations-I-restart/r73-reversible-normal-form`; paper tree `0507d04ad0bebd20cb0ce609ab94f7cc67d11f56`. |
| R73 completed publication | Commit `39980d65d6665e52c30aa340cfb0e2eb199c0f9a`, preserving the same complete mathematical-source tree and adding its publication evidence. |
| Controlling deposited R65 report | Commit `358481b21ceeeedb1205ebd30f86982e32a2cb04`; blob `d1ff9c5662390156ee212c82b173e86a21180e84`; SHA-256 `8c7d45d762736009fda667621fdf5019fa934f5f45f39364c747f837e6d7343c`. Its exact body is `provenance/R65_REFEREE_REPORT.md`. |
| Object actually reviewed in that report | R65 source commit `0469eb4f852eeea953cb3725d4b34dfdd2bf9d36`, delivered at `ee79ca9114f8009d62c056d07381b766645e3fc4`. |

The current all-head and historical-object audit found no later substantive independent report on R66–R73. Empty review heads, unchanged imports, source-recovery records, internal diagnostics, and pipeline audits are not treated as later reviews. The R65 report remains relevant because some of its contribution and generality concerns remain open; it is **not** a newly received or wholly unanswered report on R73. R66–R73 already answered several requests, and those scoped closures are inherited. The report's deposit does not establish a commissioned journal review or a human specialist's later approval. The current source and delivery identities are supplied by the final source-bound publication records linked from `START_HERE.md`; no provisional working-file identity is substituted for them.

### What is mathematically added in R74

The first new chain concerns the positive factorization in the inherited reversible normal form. For a finite observable group, the least positive core is `kappa_G(b)`, and the pure-start minimum is `m(b)=min{N,1+kappa_G(b)}`. R74 proves the following further statements.

* For **every finite observable group and every finite output alphabet**, decreasing terminal contrast toward the group average makes the positive-core minimum equal to the least size `nu_G(V_b)` of a containing permutation module. The result preserves the group, module, and residual count at every positive contrast. Its proof supplies a positive preparation, a bounded probability decoder, and an explicit positive interval; it is not an inference from linear rank alone. See `thm:r74-low-contrast`.
* At each core budget the feasible contrast set is an attained initial interval. For algebraic tables its endpoint is an effectively computable real algebraic number. When **every subgroup is normal**, within-orbit preparation can be absorbed into a quotient decoder, giving necessary and sufficient finite linear programs, explicit payoff separation, rational optimal controllers and rational endpoints for rational data. The hypotheses apply, in particular, to every finite abelian group. See `thm:r74-contrast-thresholds`, `lem:r74-normal-orbits`, `thm:r74-quotient-lp`, and `thm:r74-quotient-dual`.
* The retained prepared-qubit `S_3` model has an exact pure-start transition from four to six labels at contrast `2/3`. A binary response on `(F_2)^4` has dimension six, sixteen residuals, and the same permutation-module minimum ten at all positive contrasts, yet its positive core jumps from ten to twelve at `3/5`, and its pure-start minimum jumps from eleven to thirteen. Explicit family-dependent payoff witnesses make the larger-memory obstruction stable under a finite-table perturbation smaller than `(5t-3)/18`. These are sharp model laws and a sufficient robust lower certificate, not universal closed forms for all groups. See `prop:r74-s3-contrast`, `prop:r74-circuit-transition`, and `cor:r74-circuit-robust`.

A second new chain treats conditional dynamics. A supplied common contraction norm and a whole-ball probability-decoder margin give one finite stochastic machine for every command word, with an explicit dimension/contraction count and a counted pure start (`thm:r74-contraction`). More sharply, a stationary qubit instrument with three uniformly positive outcomes, an exactly depolarizing unconditioned channel, one-dependent observations, and word-Hankel rank three has exact classical hidden memory `q` with a free mixed start and `q+1` with a pure counted start when its conditional phase has order `q>=3`; a phase of infinite order has no finite classical realization, even with arbitrary real stochastic entries (`thm:r74-depolarizing-obstruction`). The upper constructions and the lower cycle rigidity are both proved.

Two inheritance corrections are essential. The full posterior-interiority construction for quantum instruments, including adaptive histories, complete stopped laws, costs, sparse rows, algebraic synthesis and a matching state-positive noise exponent, was **already proved in R68**. Its complete source `sections/27-interior-instruments.tex` remains authoritative; the current main article points to it. A provisional R74 restatement and a weaker dictionary lower bound were removed from the active theorem list and retained as superseded author research, rather than claimed as new results. Likewise the exact four-period damping transition at `1/sqrt(3)` already follows from the retained R69 first-sector theorem. `cor:r74-period-four-closed` records that inherited consequence and corrects the earlier open-status wording; it is not a new spectral-boundary discovery.

The source distinguishes classical invariant-cone and polytope realization, symmetric positive factorizations, residual automata, real-algebraic elimination, and finite-word equivalence from the particular new resource statements. In particular, the new one-dependent example is not the first one-dependent non-HMM process, the physical interpolation mechanism is not new, and the dependence of finite classical memory on a commensurate phase, together with a Perron obstruction at an irrational phase, has explicit antecedents. The Fanizza–Lumbreras–Winter comparison records that earlier mechanism. The claim here concerns the simultaneous qubit/rank-three/one-dependence/depolarizing-average/uniform-outcome properties and the exact additional pure-initialization charge. The inspected primary sources and exact comparison limits are recorded in `LITERATURE_AND_PRIORITY.md`.

## Major revision requests — report section 17

### R65-17.1 — Identify the mathematical center and distinguish theorem layers

**Layer: organization, theory breadth, and contribution.** The requested center was the strongest theorem available in R65. Subsequent proofs have advanced the center to exact positive realization of causal response laws, so it would be mathematically misleading to freeze the article permanently at the old heralded example. The current general finite-group contrast theorem and normal-quotient duality are the central new structural results; the conditional qubit family gives a sharp physical memory law. Their full proofs appear in the main article. The actual-history transfer theorem remains a separate general causal comparison; boundary minimax and robust tied realization remain separate decision theorems; local geometry, reset, discrimination, and timing keep their own assumptions.

The introduction and dependency map distinguish these scopes explicitly. The retained R68 instrument theorem supplies the positive physical mechanism against which the new conditional-memory family is compared. **Disposition:** the requested separation is maintained, and the central contribution is strengthened by new general theorems. This is not an author determination that a journal's significance threshold has been met.

### R65-17.2 — Make the Moore/Myhill–Nerode comparison explicit

**Layer: priority and quantifiers.** Minimal deterministic output machines are characterized by classical residual equivalence. The R65 theorem derives a task- and dictionary-specific optimal output function through physical boundary rigidity, an attained least-favorable witness, and wordwise zero slack. Uniqueness then permits positive-successor determinization. These are the physical and decision-theoretic steps; residual minimization itself is not claimed as new.

The probability-law problem studied in R73–R74 is different. Stochastic transitions and randomized readout can lower the count below the deterministic residual cardinality. The inherited size-preserving normal form, the initialization charge, and R74's constrained positive factorization retain that difference. R74 proves when the permutation-module lower bound becomes attainable and when positivity requires additional labels, with exact examples and dual certificates. **Disposition:** the classical comparison remains explicit; the new claims concern the stated stochastic resource problem, not rediscovery of residual automata or an unrestricted determinization theorem.

### R65-17.3 — Give a necessary and sufficient criterion with robust ties

**Layer: structural generality and proof scope.** This request was already substantively answered on the declared rigid class. `thm:r67-optimal-face` describes the entire robust optimal face, retaining the all-model risk inequalities in addition to wordwise tied Bayes simplexes. `thm:r67-polytope` gives the exact finite stochastic-memory criterion and pure-initial-label count by an anchored invariant polytope. The weighted R66 criteria, square-loss embeddings, and explicit failure of unqualified determinization remain intact. Those conclusions are not reopened merely because the current center has changed.

R74's quotient linear programs solve positive realization of a **specified** probability response within their group class. They do not choose an optimal point of every robust decision face or solve nonrigid boundary control. **Disposition:** inherited rigid-class classification remains closed; arbitrary nonrigid robust tied boundary optimization remains open.

### R65-17.4 — Extend beyond model-independent herald words

**Layer: generality, physical hypotheses, and applicability.** The R67 criterion `thm:r67-rigidity` already treats model- and state-dependent report masses through the ratio between unused modelwise budget and word probability. It proves necessity and sufficiency for first-herald rigidity in its uniformly transient one-command class; `ex:r67-nonrigid` gives a paid finite implementation when rejection remains feasible. The R68 theorem already permits multiple noncommuting commands and state-dependent outcomes under its uniform branch-interiority condition, preserving adaptive visible histories and stopped laws.

The R74 general contrast theorem permits arbitrary finite observable groups and output alphabets. One action realizes all mixed command words. Its normal-quotient specialization gives an exact optimization rather than testing each command separately. The new qubit instrument theorem supplies an unrestricted classical-memory obstruction even when the unconditioned dynamics mix in one step; this strengthens the earlier state-positive caution. The invariant information is the complete response law under continuation, not simply the physical state or raw failure word.

**Disposition:** several requested extensions are inherited proved results, and new exact structural and conditional-memory results strengthen them. A classification of optimal stopping and command choice for every nonrigid multi-command experiment is still not asserted. A simulator's private label is not supplied to the original feedback policy.

### R65-17.5 — Determine the general-`M` noisy-qubit risk frontier

**Layer: sharp quantitative optimality.** The specific requested quantity `V_{p,alpha,M}-V_{p,alpha}` is an approximation-risk optimum at a prescribed memory budget. Its general-`M` exact value and a matching asymptotic lower rate remain open. The retained exact one- and two-label values, strict attained finite-memory gaps, and exponential prefix upper are not weakened or relabeled as a sharp general frontier.

The new all-contrast finite-group thresholds, sharp `S_3` and four-bit transitions, and exact `q`/`q+1` instrument law solve different, explicitly defined exact-response memory problems. They provide matching constructions and obstructions in those problems. The four-period response count is now recorded correctly as already closed by R69. **Disposition:** the requested risk frontier is not closed; the revision adds precise exact-memory results without substituting them for it. No finite diagnostic or separating score is advertised as its missing asymptotic proof.

### R65-17.6 — Supply a natural quantum or causal consequence

**Layer: scientific consequence and application.** The strengthened instrument result concerns an ordinary repeated instrument with a fixed qubit, three outputs, a stationary preparation, and a completely depolarizing unconditioned channel. It computes the exact classical hidden-state resource for all observed words as the conditional phase varies. The lower holds for arbitrary real hidden transition probabilities; the matching polygon realization and unavoidable pure-start label establish optimality. It separates conditional predictive memory from physical dimension, linear prediction rank, mixing time, and dependence range within one explicitly specified experiment.

The all-group terminal-contrast result also gives a general resource consequence for prepared unitary experiments: sufficiently weak terminal readout attains the permutation-module lower bound without altering the command action. The `S_3` law is a complete prepared-qubit specialization. The diagonal four-bit example is classical and is not presented as a quantum advantage.

**Disposition:** substantive repeated-instrument and all-command consequences are supplied. We do not declare an independently recognized open problem solved without establishing its prior status. Whether these consequences meet the requested external-impact standard remains a question for actual independent mathematical assessment.

### R65-17.7 — Strengthen effective synthesis and certificates

**Layer: computability, complexity, and priority.** The inherited R67 algebraic fixed-memory optimum and R73 algebraic reversible finiteness/minimum-synthesis theorem remain active, with their exact input promises. R74 makes the finite-group positivity problem more explicit: for groups all of whose subgroups are normal, exact minimum cores and contrast thresholds reduce to a finite collection of bounded linear programs. Rational input gives rational thresholds and rational optimal tables; data in a specified real algebraic field admit controllers in that field. The payoff dual gives strict rational exclusion witnesses, with a quantified finite-table perturbation margin. The four-bit example supplies these witnesses explicitly for every admissible low-budget partition.

For general finite groups, compact polynomial feasibility and the inherited algebraic method give computable attained thresholds. These are proved procedures; a general quantifier-elimination computation is not reported as executed. The number of subgroup families or actions can be large. Common contraction is assumed through a certificate and is not turned into a decision algorithm for joint spectral radius.

**Disposition:** new exact LP reductions, arithmetic conclusions, and dual certificates complement inherited decidability. General polynomial complexity, hardness of every optimum, and matching program/precision/workspace or sampling lower bounds remain open. Classical elimination, finite automata equivalence, and positive realization receive explicit credit.

### R65-17.8 — Read back the exact hosted run

**Layer: evidence provenance.** The R65 report correctly recorded run `38861581555` as queued at its cutoff. The subsequently deposited terminal receipt `provenance/R65_HOSTED_TERMINAL_RECEIPT.json` records `completed`, `success`, head SHA `ee79ca9114f8009d62c056d07381b766645e3fc4`, and terminal update `2026-10-16T08:41:33Z`. It records the later GitHub readback on 18 October. This closes that historical terminal-state request; it does not rewrite the report's earlier observation.

R74 compilation, local finite diagnostics, remote publication, and any hosted Actions execution require their own matching source and delivery identities. Only their actual receipts, linked from the current entry point, establish what ran. **Disposition:** the historical request is closed by its retained exact-SHA record; no R65 success is reported as R74 CI, and no queued or unobserved run is called successful.

### R65-17.9 — Reduce the mathematical dependency surface

**Layer: organization and proof accessibility.** The minimal new reversible chain is the response conventions, the retained reversible criterion and normal form, the new contrast theorem, and the normal-quotient reduction and dual. The explicit transitions depend on that chain and elementary representation or Fourier calculations. The new conditional-instrument proof needs its displayed primitive maps, elementary Hankel and nonnegative-matrix arguments, and the expressly retained relative-spectrum normalization. It does not depend on all historical geometry, optimization, or pipeline claims.

The main article contains the complete new proofs and the central retained normal form. The paired supplement contains the necessary recurrent-projection proof and complete independent retained results. The R68 instrument mechanism is inherited once, rather than presented under duplicate new theorem labels. Original wrappers, responses, derivations, companions, and historical proofs remain at pinned locations outside the minimal reading path. `THEOREM_DEPENDENCIES.json`, `THEOREM_INDEX.json`, and `PRESERVATION_MAP.md` distinguish proof dependency from preservation. **Disposition:** the current entry identifies a concrete minimal chain without silently discarding valid mathematics or treating the whole archive as a prerequisite.

### R65-17.10 — Separate the resource conventions

**Layer: definitions and implementation.** All new pure-start counts include the initial live label. A mixed initial law is free only in an explicitly labeled comparison, such as `kappa_G` or the mixed-start `q`-state instrument model. The initializer processes the first command or first outcome during its counted transition. It is not an uncounted clock or a free state-preparation action.

Live labels, distinct decoder values, deterministic residuals, event-stopped total labels, state-stopped total labels, table descriptions, working storage, algebraic precision, sampling, protected physical dimension, and full-history mathematical information remain separate. On the inherited first-herald embeddings, the stated role-packing upper counts are `max(M,m)` for event stopping and `M+m` for state stopping, with `m` distinct decoder values. A simulator's hidden labels and a policy's own observer memory are also distinct. **Disposition:** definitions, lower bounds, constructions, and abbreviated new statements retain these conventions; none is inferred from a rank or a dual-support count.

## Technical comments — report section 18

Each item below answers the original numbered comment separately. A reference to a retained result identifies current proof authority, not a claim that the R65 report evaluated later source.

### R65-18.1 — Fixed decoder dictionary

**Assumption retained.** `thm:boundary-regularity` still fixes the finite dictionary `C`, and the squared-task examples retain their stated dictionaries. The new response theorems fix a finite output alphabet and a supplied probability table. Neither a change of dictionary nor an optimization over hard output width is free. The distinction is explicit in `sections/02-experiments.tex` and the current scope statement.

### R65-18.2 — Model-independent word probabilities

**Scope retained and extensions typed.** The common positive word law remains a hypothesis of the original herald theorem. R67 replaces it with its own model-dependent branch masses and rigidity criterion; it does not erase it retrospectively. R74's finite-group table is a prescribed all-word response, while the instrument theorem and retained R68 law concern joint state-dependent outcome probabilities. These are different mathematical inputs.

### R65-18.3 — The compulsory first call

**Cost convention retained.** `lem:boundary-herald` includes the first call in `p E[tau]=1+E[J]` and `N_min=1/p`. A pure initial label is a separate memory resource. The new initializer executes the first input or generates the first outcome on its transition, so no physical call or input-reading step is omitted.

### R65-18.4 — Audit cost

**Resource hypothesis retained.** A separately executed physical audit remains additive to the model's cost budget. A probability decoder is a mathematical simulation of its law, not a claim that the original measurement is free. The retained audit-compilation, reset, and physical realization results keep their explicit paid interfaces.

### R65-18.5 — Least-favorable measure

**Quantifier retained.** A least-favorable measure is an offline dual witness proving minimax restrictions. It is not a Bayesian model value provided to a runtime controller. The new payoff dual is likewise an external certificate of finite-table infeasibility; it is not an extra controller input.

### R65-18.6 — Wordwise uniqueness under one attaining witness

**Hypothesis retained.** Original determinization requires unique minimizing actions at every relevant word under one attaining least-favorable measure. The tied optimal-face theorem instead retains randomized decoders and all-model risk inequalities. R74's permutation-core normal form is a probability-law realization result, not a relaxation of that uniqueness premise.

### R65-18.7 — Positive word masses

**Proof step retained.** In the original zero-slack argument, positive masses are what force a wordwise conclusion. R67 treats model-dependent and null words explicitly; globally null words may be completed without changing any model's law. The new exact all-word response is a declared requirement on the supplied object, not an inference about an unobservable null history.

### R65-18.8 — Residual congruence

**Definition retained.** The original congruence is the right residual equivalence of the optimal task decision. For probability responses it is equivalence under every future response test. Neither is automatically the full channel state or a predictive quotient uniform over unknown models. The observable group is formed after removing future-test-invisible directions, as in `thm:r72-reversible`.

### R65-18.9 — Live and terminal labels

**Convention retained.** The new exact minima count live labels and include pure initialization. Terminal-role packing is stated separately for each physical interface: the inherited first-herald construction uses at most `max(M,m)` event-stopped labels or `M+m` state-stopped labels. The binary specializations do not become universal equalities for arbitrary stopping interfaces.

### R65-18.10 — Unreachable rows

**Minimality convention retained.** Unreachable or zero-initial-mass components can be pruned before a minimum is claimed. Completion of unused stochastic rows is only a feasibility device. In `lem:r74-normal-orbits` zero-mass orbits are discarded; in the conditional-memory lower proof, only reachable and co-reachable states of the selected cylinder are retained. Adding arbitrary unused rows cannot strengthen a lower bound.

### R65-18.11 — Positive-successor determinization

**Proof requirement retained.** The old unique-action argument follows positive successors only. The new conditional-phase lower also uses positive directed edges, and explicitly propagates maximal-modulus equality throughout the irreducible block before imposing cycle-length restrictions. Zero entries create no paths and cannot justify a cycle or deterministic selection.

### R65-18.12 — Robust ties near determinization claims

**Counterexample and closure retained.** `prop:boundary-ties` retains the two-model example in which randomization attains risk one half while every pure decision has risk one. The current tied discussion points to the complete R66/R67 optimal-face criterion. The R73 factorial separation and the R74 core/initializer distinction additionally make clear that stochastic realization need not have the deterministic residual count.

### R65-18.13 — Effective distinguishing depth

**Existence separated from computation.** The original continuum-data `H_M` is still only existential without further effective input. Under a supplied finite linear representation, the retained finite-word theorem gives the explicit horizon `d+M-1`; algebraic input makes its strict gap computable. The new finite-group LP certificate uses a known finite table. None of these added input assumptions is suppressed.

### R65-18.14 — A positive gap is not a sharp risk law

**Sharpness claims corrected.** The distinguishing-depth gap and robust finite-table witness are strict exclusions, not the missing general-`M` risk asymptotic. The new `S_3` and four-bit contrast thresholds have matching upper constructions and are exact for those models. The old `89/90<=alpha<=1` period-four interval remains a sufficient finite-probe certificate; the exact threshold `1/sqrt(3)` is recorded from R69, not inferred from that interval.

### R65-18.15 — Irrational rotation

**Proof retained.** For `z=(3+4i)/5`, a root of unity would make `z+z^{-1}=6/5` a rational algebraic integer, hence an integer. The contradiction remains the exact proof. The same phase supplies the algebraic infinite-memory specialization in `thm:r74-depolarizing-obstruction`. It supplies no particular Diophantine irrationality exponent.

### R65-18.16 — No zero cosine

**Hypothesis use retained.** In the original sign-decision example, a vanishing cosine at a positive integer time would imply a root of unity and contradict the preceding argument. That step establishes uniqueness there. The new finite-order instrument family permits zero cosine values at some times; its Hankel lower uses three distinct nonzero exponential coefficients and `sin(theta)!=0`, not the old sign-uniqueness argument.

### R65-18.17 — Polarization and degeneracy

**Endpoint retained.** The uncertain-polarization theorem keeps strictly positive polarization; at zero its uniqueness conclusion fails. The new terminal-contrast theorem treats `t=0` separately as a constant one-label response and makes its group/module claim only for positive contrast. The instrument's uniform posterior margin and the old polarization parameter are different quantities, each with its own endpoint statement.

### R65-18.18 — Unitary periodicity

**Uniqueness retained.** `cor:unitary-period` keeps a unique optimal action at each orbit time when upgrading ultimate periodicity to periodicity from the start. The compact-group probability-law theorem and the exact cyclic instrument theorem have distinct hypotheses and do not assume that a tied action has become unique. Their exact counts are established directly for the whole response.

### R65-18.19 — Contraction and a limiting gap

**Different sufficient conditions distinguished.** The retained decision theorem still requires a common limiting state and a strict limiting action gap. New `thm:r74-contraction` concerns a supplied linear probability response with one common norm and a whole-ball decoder bound `r||ell_c||_*<=p_c`. This is not a theorem about discontinuous optimal sign selection. In particular a vanishing limiting output with a nonzero functional fails its decoder condition.

### R65-18.20 — Average contraction is insufficient

**Counterexamples preserved and strengthened.** The old depolarizing sign-task and leakage examples remain valid. The R68 branch-interiority theorem already warns that unconditioned mixing does not verify its branch hypothesis. The new stationary qubit family sharpens that warning to exact unrestricted HMM memory: the average channel resets in one step, yet the recorded zero branch retains a finite or infinite order phase. The positive construction and the obstruction use explicitly different hypotheses.

### R65-18.21 — Row and chronological conventions

**Notation retained.** Stochastic matrices act on probability rows from the prescribed initial basis row. The two-state matrix remains `[[1-a,a],[b,1-b]]` at its first occurrence. The group action uses the stated chronological word convention; operator composition on physical states is written in its corresponding reversed product order. No transpose convention is used to change an initialization count.

### R65-18.22 — Randomized terminal decisions

**Optimization class retained.** The two-label signed decoder ranges over `[-1,1]`, so randomized terminal choices are included. A binary probability decoder ranges over `[0,1]`; a multi-output decoder has stochastic rows. The new bounded-decoder lower bounds optimize over that whole probability class, not only deterministic terminal functions.

### R65-18.23 — Degenerate endpoints

**Endpoints retained and typed.** The old two-state calculation keeps `x=0`, `c=1`, and `c=-1`. New contrast minima take the lower branch at `2/3` and `3/5`; `t=0` is constant and needs one label. The four-period damping response at `alpha=0` instead has initial probability one and later probability one half, so it needs two labels. These distinct zero-parameter cases are not conflated.

### R65-18.24 — The `q alpha>1/3` threshold

**Model restriction retained.** That threshold belongs only to the displayed `c=3/5` noisy sign-task specialization. Here `q` denotes its failure probability. The conditional-phase theorem uses `q` locally for an integer root order, and the `S_3`/four-bit contrast thresholds solve different response laws. None extends the old risk threshold to other phases, losses, priors, or experiments.

### R65-18.25 — The timing frontier

**Open problem retained.** The two-label quantum prediction calculation, reversible positive-core formula, and new instrument minima do not solve the intermediate phase-type release/timing frontier. Its earlier lower and upper bounds remain preserved with their original interpretation. The unresolved exact timing curve remains listed in `RESEARCH_STATUS.md`.

### R65-18.26 — Exact input for algorithms

**Input promise retained.** The prefix algorithm assumes exact rational primitives and fixed rational losses. The R73 synthesis theorem assumes a supplied real-algebraic representation and its declared probability/reversibility promises. R74's rational LP and same-field controller conclusions apply to a known finite group table. A real existence theorem, an algebraically encoded instance, and a model inferred from finite data are different inputs.

### R65-18.27 — Herald-rate dependence

**Complexity limitation retained.** The old polynomial precision statement requires a positive lower bound on the herald rate. R74 claims finitely many LPs or effective algebraic procedures where stated, without a polynomial bound on subgroup-family enumeration, action enumeration, quantifier elimination, or net construction. A known uniform contraction certificate is assumed, rather than silently computed.

### R65-18.28 — Primitive and dictionary encodings

**Additional resources retained.** Primitive entries, the decision dictionary, group/action descriptions, field encodings, and output probabilities contribute to the program. A small live-label optimum does not imply a small exact description. The LP reduction makes finite exact table synthesis available in its class, not a bound independent of those input lengths.

### R65-18.29 — Dense superoperator arithmetic

**Representation convention retained.** The old arithmetic bound uses the full `d^2` real Hermitian-coordinate representation and its dense operations. No unproved sparse implementation is inserted into that count. Observable reduction may improve a particular instance, while the retained R68 sparse branch rows bound a different quantity, namely successors after a dictionary has been constructed.

### R65-18.30 — Program table and working storage

**Resource separation retained.** A retained label, a stored transition/readout table, and temporary exact arithmetic storage are distinct. The explicit controller constructions specify mathematical tables. They do not by themselves solve minimum table-bit complexity, workspace, precision, or exact-sampling complexity. These remain separate research objectives.

### R65-18.31 — Meaning of local verification

**Evidence type retained.** The strict verifier binds the actual Git HEAD, complete source tree, preserved predecessor, source manifest, compiled theorem/number/page map, native PDFs, and actual ordinary/optimized finite diagnostic executions. It is not a proof assistant or a certificate of continuum theorem truth, novelty, expert agreement, or journal suitability. The separately recorded author-team AI proof challenge is described by that role.

### R65-18.32 — The queued R65 run

**Historical observation retained.** The run was queued at the original report cutoff. Its later terminal receipt closes the requested readback at that same R65 delivery SHA. This event is not a fresh R74 run and cannot be used as evidence that an R74 workflow completed. Current execution status comes only from current matching receipts.

### R65-18.33 — Paired cross-document references

**Delivery requirement retained.** The main article and current supplement are compiled as a pair with actual cross-document auxiliary labels. Their current PDF filenames should be kept together. `THEOREM_INDEX.json` supplies the current theorem numbers and pages; a historical PDF or old numbering is not substituted for either current document. The independent R58 companion remains separately compiled.

### R65-18.34 — Preservation is not re-review

**Provenance scope retained.** R74 preserves the complete R73 source tree, which carries the R72 and earlier preservation chain, as well as the pinned independent sources. Original current mathematical bodies and the inline supplement suffix are byte-identified. That records continuity and permits comparison. It does not claim that every R64 or earlier theorem was freshly re-proved or reviewed by a new expert.

### R65-18.35 — Actual historical-audit coverage

**Audit claims made precise.** The new audit separately records all remote heads, immutable commit/tree identities, actual historical text retrieval, Git-blob/SHA-256 checks, candidate-report classification, and mathematical proof scrutiny. The scan re-read the scoped historical text corpus rather than merely ordering branch names. Its receipt states the number of objects and errors; it still does not equate textual retrieval with a fresh line-by-line proof of every historical result.

### R65-18.36 — Bounded scores and unbounded duration

**Proof mechanisms separated.** The general performed-law comparison retains its bounded-score hypotheses. A bounded-coordinate compactness argument is not used to infer an unbounded waiting-time estimate. The retained R68 exact path-law simulation has a stronger premise and a separate induction; there nonnegative path-cost expectations follow from equality of laws and monotone convergence, as explicitly proved. These statements are compatible and must not be merged.

### R65-18.37 — Convexity and hard width

**Convexity scope retained.** Fixed-dictionary convexity does not imply convexity after optimizing a hard width constraint; the inherited dual-gap example remains controlling. Similarly, R74's feasible set for one fixed quotient family is a convex polytope, whereas selecting a family under a size budget is a separate finite combinatorial optimization. Its union is not silently treated as one convex feasible set.

### R65-18.38 — Sparse dual atoms

**Object distinction retained.** The `k_T+1` atoms in `thm:sparse-witness` are dual model/preparation witnesses. They are not primal observer or simulator states. The new quotient factors, physical dictionary elements, sparse successors per branch, and diagnostic checks are also distinct objects with separate counts. No live-memory bound is read off from a dual-support bound.

### R65-18.39 — The protected qubit

**Physical interface retained.** The qubit is part of the experiment, not a private quantum register granted to the observer. A classical hidden realization reproduces the declared output laws without reading or copying the physical state. The retained adaptive comparison does not expose the simulator's internal label to a policy; such exposure would change the experiment and its decision problem.

### R65-18.40 — Open scope

**Scoped closures and open problems distinguished.** The rigid-class robust-tie criterion is already proved and remains closed. General nonrigid tied boundary optimization, general multi-command optimal feedback, boundary finite-memory density beyond the declared classes, the general-`M` squared-sign risk curve, and the timing frontier remain open. The current exact group and conditional-instrument results do not complete A1, A2, or independent Theta construction objectives. The four-period first damping transition is no longer listed as open because R69 already settles it.

## Contribution objections and earlier unresolved issues

The report's section 16 separates a breadth objection, a classical-priority objection, a robust-tie gap, an external-consequence objection, an intermediate-memory gap, a computational objection, and a mismatch between the broad programme and the theorem article. The answers above preserve that separation. In particular:

| Concern | Current mathematical disposition |
|---|---|
| Special herald assumptions | Weighted rigidity and state-dependent multi-command instrument simulation are inherited extensions; arbitrary finite-group contrast structure and the new conditional-phase law add further exact results. No universal boundary-control classification is asserted. |
| Classical residual mechanism | Classical residual equivalence and positive realization are credited. R74 optimizes a bounded probability factorization and proves module saturation, a normal-quotient LP reduction, and exact positivity transitions. |
| Robust ties | The necessary and sufficient anchored optimal-face criterion is retained on the rigid class. The nonrigid problem remains open. |
| External consequence | The exact stationary instrument memory law and the all-group terminal-contrast theorem are supplied with constructions and lower proofs. No independent endorsement or pre-existing open-problem status is invented. |
| General-`M` risk | Still open for the original squared-sign task; exact response-memory laws are not substituted for it. |
| Computational strength | Inherited reversible exact synthesis is supplemented by explicit LP duality, arithmetic thresholds, and robust finite certificates. General efficiency and all-resource lower bounds remain open. |
| Programme breadth | Causal transfer, predictive compression, finite-order measurement, reset, communication, rank-constrained discrimination, spectral geometry, variational principles and strategy realization remain preserved with separate authorities. The larger Theta pipeline remains independent. |

The original independent finite-order measurement and reset developments remain pinned, including the general fixed-acquisition labelwise continuation-concavity criterion, the binary nonconcavity witness, rank-cut restrictions, support-inverse optimizer, and local spectral calculations. An equal-prior or low-dimensional formula does not replace the scope of the general criterion. The complete R58 calibration/directional-sensing companion remains separately available. `PRESERVATION_MAP.md` identifies these actual sources and their immutable identities.

The revision also retains, rather than repeatedly reopens, the R66/R67 stopping and robust-tie closures; the full R68 instrument construction and its state-positive scope; the R69 first-sector law; the R70 leakage/relative-spectrum results; the R71 arithmetic envelope; and the R72/R73 reversible classification, normal form, algebraic synthesis, and finite certificates. The history review corrected an open-status error about the four-period transition and prevented a duplicate R68 theorem from being counted as a new contribution. It did not uncover a reason to discard those valid mathematical bodies.

## Evidence, remaining research, and the next referee entry

The remaining problems are stated as research obligations rather than concealed assumptions: nonrigid boundary optimality and finite-memory density; general-`M` squared-sign risk; other damping transition laws; intermediate phase-type timing; sharp arithmetic constants and the particular algebraic rotation's exponent; efficient synthesis and matching program/precision/workspace/sampling bounds; learning unknown predictive representations; and independent A1/A2/Theta hypotheses. The new proofs do not rely on assuming these problems solved.

`START_HERE.md` identifies the current complete English manuscript, current supplement, preserved companion, source archive, exact source/publication identities, theorem/dependency map, preservation map, proof audit, and actual verification receipts. Those receipts determine what compiled and which checks ran at the stated SHA. Finite diagnostics supplement the written proofs and do not replace them. No formal proof-assistant verification, new human referee report, editorial decision, or journal acceptance is asserted. The packet provides a concrete source-bound basis for the next independent assessment of the strengthened mathematics while retaining the original research objective.
