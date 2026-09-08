# Independent referee report on A1 v33

**Manuscript:** *Attainable information, exponent collisions, and finite-state realization*  
**Author:** Qian Qi  
**Review date:** 8 September 2026  
**Requested standard:** Annals of Mathematics / Inventiones Mathematicae / Journal of the American Mathematical Society / Acta Mathematica  
**Reviewed revision branch:** `revision/a1-english-v33-moment-controllers-2026-09-08`  
**Controlling manuscript commit:** `e7dfc3a0e1c8d7a9d3be6b7f52944c5c7c59bb0c`  
**Previous review commit:** `60c5b116a2c002dfd8056a351a87d7014d8c78e1`  
**Review branch:** `review/a1-english-v33-harsh-independent-2026-09-08`

This is an owner-requested, AI-assisted independent referee-style assessment. It is not a report commissioned by, or an editorial decision of, any of the journals named above. The assessment is pinned to the commit, rather than to a moving branch. The revision head was rechecked before this review branch was created. [S0]

## Recommendation and basis of judgment

**Recommendation: reject in its present form at the requested four-journal level.** I would not recommend another minor-revision cycle whose principal deliverable is additional verification machinery.

**This is not a finding that the main theorem is false.** I have not established a fatal counterexample to the examined main-article theorem chain. The principal collision argument survives the checks described below. The new finite-moment formula, purification argument, scalarized polyhedral realization and continuous-command example are substantive, mathematically intelligible improvements. Several concrete v32 objections should now be closed, not repeated under new wording.

The remaining adverse recommendation is principally an editorial judgment about the demonstrated originality, conceptual reach and hierarchy of contributions. The new controller section removes history-indexed optimization variables, but much of its mechanism is finite-experiment postprocessing, finite-dimensional forward propagation, classical purification and compact minimization. Its exact relation to those antecedents is not sufficiently exposed. The collision-uniform attained geometry remains the strongest candidate to bear the exceptional-journal case. The manuscript needs to make that case directly, rather than expect several correct realizability and certification consequences to settle it by accumulation.

This recommendation is a judgment, not a theorem about the work's eventual publication prospects. I have not proved prior publication of the exact collision classification, and I do not allege plagiarism. Nor do I regard a polynomial-time algorithm, sharp leading constant or new infinite-horizon theorem as a universal condition for publication at these journals.

## 1. Scope and evidence

I examined the current main-article proof chain in the native TeX sources: the experiment and risk definitions, attainable transversality, confluent pairing and covering inputs, collision flags, checkpoint and causal classification, collision consequences, the complete new moment-controller module, finite compatibility and approximation arguments, precision calculation, exact example and current comparison section. Exact source labels are used below because they are more stable than page numbers. [S1–S9]

I also consulted the controlling v32 report and the v33 response, and selected inherited comparison material on nonlinear-filter quantization, information states and finite pairings. These comparisons contain relevant qualifications that must not be ignored merely because they now occur in the companion. This is not a claim that every historical branch or every companion proof has been independently audited. [S10, S11, S13]

The author supplies a two-volume build receipt and a session record reporting 79 active TeX inputs, 35 main pages, 159 companion pages, resolved references, and local visual checks. Those are materially stronger provenance records than the preceding source-publication record. I read them but did not independently reexecute the native two-volume build or recheck all 79 source hashes. I did not render or visually inspect the manuscript PDFs in this review. The independent calculations accompanying this report are a different artifact from the author's build and certificate execution. [S12]

External verification used primary research sources. In particular, the real entropy inequality invoked in the main proof is explicitly recalled in Comte–Halupczok, equations (4)–(5), and the cited semialgebraic regularity statement is present in Zhang–Kileel, Lemma 2.18. The relevant text was retrieved; attempted web PDF screenshots failed and are not represented as successful visual inspection. [L1, L2]

The qualifications above limit the review's coverage; they are not evidence of defects in unexamined material.

## 2. Disposition of the controlling v32 objections

| Previous concern | Finding on v33 | Disposition |
|---|---|---|
| R32.1: a chosen relative-certificate power was carrying too much conceptual weight | `thm:v33-precision` allows arbitrary precision exponent s > 2, gives the literal search cardinality, and separates the full collision profile from the one-dimensional floor | **Closed as a precision-versus-statistical-exponent issue** |
| R32.2: exact compatibility still used a history-state tree | `thm:v33-moment-program` genuinely removes complete-history variables from the controller optimization for prescribed acquisition | **The concrete representation objection is closed; the significance assessment changes rather than disappears** |
| R32.3: finite approximation and channel-continuity comparisons were insufficiently specific | `v33/comparison.tex` names particular results, identifies their information resources, and does not dismiss team theory as lacking information constraints | **Substantially answered; a different, more immediate comparison for the new implementability body remains necessary** |
| R32.4: the delayed block example was not an application of the main per-report model | The delayed block calculation is segregated, and the new N = M = 2 example has continuous acquisition commands, positive likelihoods and a full attainable query basis in the per-report model | **Closed as an admissibility/model-mismatch objection** |
| R32.5: no executed original-model enclosure or current full native build record | The exact example has a global analytical lower-bound argument and an executed rational enclosure; current author build/session records are present | **Closed as an absence-of-delivery objection; this reviewer does not claim independent reproduction of the two-volume build** |

The previous report did not promise acceptance if these requests were met. Nevertheless, it would be unfair to preserve the old rejection reasons as though the author had not met them. In particular, the exact example must not be dismissed as a sample of candidate controllers, and the moment program must not be described as still assigning variables to every command-report history. [S7–S12]

## 3. Audit of the publication-bearing collision theorem

### 3.1 Exact information and acquired dimension

The distinction between the full future test space and the attained prediction image is correctly maintained. For a detector spanning the monomial space W_A, future likelihoods span W_(mA); the normalized attained dimension is

$$
d_A(n,m)=\min\{n(r-1),|mA|-1\}.
$$

The lower-dimensional claim is supported by an explicit tangent, not merely an ambient dimension count. At the attainable binomial tuple, writing z = t^D, the polynomials P_i(z) = P(z)/(1+c_i z) form a basis through degree n−1. The tangent exponents consist of the multiples jD and the distinct translates a+jD for interior a. This gives n(r−1)+1 independent unnormalized directions. Strict mixed-moment positivity yields the required pairing rank for every fixed full-support prior. Since the product itself belongs to the tangent and its constant moment is nonzero, normalization loses exactly one rank. [S2: `lem:binomial-tangent`, `thm:rank`]

The minimum continuous encoding dimension is also justified within its stated resource. The local section and invariance of domain establish the lower bound. The upper construction retains normalized chronological factors until the future-moment representation is smaller, and then makes a single changeover. It is not a global embedding claim about an arbitrary curved prediction variety into its dimension. A sufficient encoding may distinguish histories that have the same posterior. The subsequent raw-moment update uses only permitted moments and a positive report-probability denominator. [S2: `thm:causal`]

**Finding:** no identified rank or topological gap in this argument. The scope is sparse monomial spaces and a fixed full-support prior; arbitrary factor spaces do not inherit the dimension formula automatically.

### 3.2 Collision flags and unconditional lower mass

The Leja construction keeps formal labels at coincident nodes. Positive pivots precede zero pivots, the leading nonzero triangular block has bounded inverse, and

$$
\prod_{j=1}^{\ell}d_j\le\mathcal V_{m,\ell}
\le\ell!\prod_{j=1}^{\ell}d_j.
$$

The zero-pivot convention is not an illicit division by a vanishing gap. The proof operates with scaled coordinates and only inverts the leading nonzero triangular block. [S3: `lem:leja-scales`]

More importantly, the acquired lower bound is not inferred from a Vandermonde estimate alone. Initial Newton divided differences span complete confluent test systems, including repeated nodes in nonadjacent positions. Their uniform continuity at t = 0 follows because positive exponents remain bounded away from zero while the logarithmic powers are bounded after multiplication by the corresponding monomials. The positive mixed pairing against the binomial tangent therefore gives a surjective differential for every required initial flag. There are only finitely many formal orderings. Compactness then supplies uniform bounds. [S3: `lem:newton-attainment`]

The inverse-function argument includes kernel coordinates and the all-failure evidence. Its subprobability minorization is under the actual joint command-and-report law. It does not replace that law by a command law conditioned on a word without evidence. The latent prior may be singular: the absolutely continuous variables used in this local acquisition argument are commands, not latent parameters.

**Finding:** these are genuine experiment-level steps. It would be inaccurate to characterize the lower bound as a generic quantization theorem applied to an assumed box.

### 3.3 Global covering and one causal transducer

For a fixed calibration and report word, prediction coordinates are rational functions of commands with evidence bounded away from zero. Their moments and exponent values enter as real coefficients. Consequently the bounded-format semialgebraic argument does not require the calibration set K, or the dependence of the moments on calibration, to be semialgebraic. That distinction is correctly used. [S4: `thm:intrinsic-checkpoint`]

The thin-rectangle covering proof has an identifiable external input. The real Vitushkin–Ivanov bound controls entropy by averaged component counts of affine sections. Bounded semialgebraic format controls those component counts independently of coefficients. Sections of codimension above the attained dimension are empty almost everywhere; the remaining variations are bounded by products of the largest side lengths of the containing rectangle. The cited primary sources support these inputs. This is a classical real inequality, not an application of the nonarchimedean theorem in the paper whose introduction recalls it. [S5: `lem:tame-rectangle`; L1, L2]

The causal upper bound has the necessary extra step beyond checkpoint covering. It quantizes reachable raw moment representatives, updates a representative by the same Bayes ratio as an exact reachable state, and quantizes again. The denominator is bounded below on a segment of two reachable moment vectors because that segment corresponds to posterior mixtures. The resulting finite-horizon recurrence has no inverse exponent gaps. No discarded prefix is supplied to the transducer. The common-law lower bound follows because every streaming index is an admissible checkpoint encoder. [S4: `thm:intrinsic-streaming`]

**Finding:** the full argument is materially stronger than separately quantizing each checkpoint. No counterexample to the printed fixed-horizon, calibration-uniform comparison law was found.

### 3.4 What the collision result does and does not settle

The two-parameter phase calculation is internally consistent. At n = 3, m = 2, six separated groups have three within-group gaps |u|, |v−u|, |v−2u|. The two largest gaps are comparable to rho, and the third is tau. The seven-dimensional term is controlled by interpolation between the six- and eight-dimensional terms. This leads to the stated three-term profile and the 6/8/9 dimension pattern. The independent rational checks include the intersection, each of the three collision lines, generic points, and a near-tangent configuration. [S6: `cor:two-parameter`]

The theorem determines risk up to constants that may depend on the fixed experiment, horizon and prior. It does not identify a sharp finite-M causal price relative to separately optimized checkpoint encoders, nor a quantitative law for how optimal transition partitions change near a collision. Those are limitations of the conclusion, not contradictions of what is actually stated. The fixed-prior and fixed-horizon qualifications must remain visible wherever the result is interpreted.

## 4. Audit of the new finite-moment controller section

### 4.1 One-step implementability: correct coupling, but a classical surrounding framework

The body in `lem:v33-body` enforces a real restriction. After failure, the controller cannot read which raw cell failed. Thus all raw-cell rows must arise from the same function u(g). Treating the failure allocation separately for each raw cell would enlarge the admissible experiment. The compactness proof via weak-star compact simplex-valued functions and finitely many integrals is valid. The accepted part can be replaced by a command-independent probability vector because the retained coefficients only require its weighted average. The support maximizer is Borel by a finite tie-breaking rule. [S7]

There is, however, a direct classical interpretation that should be made explicit. Introduce an auxiliary finite experiment whose unknown index is the raw cell k and whose observation is the command/report pair:

$$
E_k(dg,dx)=\nu(dg)\{g_k\delta_k(dx)+(1-g_k)\delta_\dagger(dx)\}.
$$

For any Markov postprocessing U from this observation to M labels,

$$
(EU)_{kj}=\int\{g_kU(j\mid g,k)+(1-g_k)U(j\mid g,\dagger)\}\,\nu(dg).
$$

Therefore, exactly and without an approximation,

$$
\mathscr A_M(\nu)=\{EU:U\text{ is a Borel Markov kernel to }[M]\}.
$$

This is the finite-output postprocessing, or garbling, region of a fixed experiment. The displayed identity is a direct reduction written out here; it is not an unsupported claim that a cited paper contains the manuscript's entire dynamic theorem. Classical comparison-of-experiments theory is the pertinent surrounding framework. The reference point is Blackwell's comparison theory, not only finite-controller optimization or quantized-action approximation. [L5]

Likewise, evaluating a linear functional on this region separates over observations and yields precisely the manuscript's support formula. The row overlap follows because both conditional observation laws share the failure submeasure

$$
\min(1-g_k,1-g_l)\,\nu(dg)\,\delta_\dagger(dx),
$$

whose mass cannot disappear after common postprocessing. This derivation validates the result and clarifies the novelty boundary at the same time.

**Finding:** the lemma and corollary appear correct. Their specialized formula is useful. Their conceptual framework is not new merely because it is called an implementability body.

### 4.2 Exact mean-risk formula and zero occupancies

For prescribed independent commands, the conditional occupancy recursion

$$
q_{n,j}(t)=\sum_{i,k}q_{n-1,i}(t)k_k^a(t)A_{n,kj}(i)
$$

is both necessary and sufficient. In the forward direction, the current command law is independent of the previous state conditional on the latent parameter. In the converse, one implements a kernel for each of finitely many time-state matrices. This is a single controller, not a family of separately chosen checkpoint encoders. [S7: `thm:v33-moment-program`]

The formal nonnegative coefficient recursion and the multinomial sum identity are correct. The stated coefficient count is an upper bound in a formal polynomial representation; it need not be a minimal identifiable parametrization. The quantities q are an offline description of state laws, not retained state variables.

The cross-term identity in the squared loss is essential. Conditional on a complete acquired command/report history, the latent parameter and the controller state are independent: the likelihood product contains all latent dependence, while the state-path probability depends on the fixed history and fresh coins. Thus, for a fixed decoder,

$$
\mathbb E[p_{nq}(H_n)d_{nq}(S_n)]
=\mathbb E[H_{nq}(t)d_{nq}(S_n)]
=\sum_i b_{niq}d_{nq}(i).
$$

Completing the squares yields the stated centroid and objective. The extension at w = 0 is valid because 0 <= b <= w implies 0 <= b^2/w <= w. Separate decoder coordinates allow the checkpoint decoder minimizations to occur simultaneously; the transition matrices remain common. Compactness then gives attainment.

The baseline B_n does not introduce additional unknown moments above degree N. It does, however, still require integration of rational expressions over command histories. The manuscript explicitly acknowledges the distinction between a finite-dimensional optimization, coefficient evaluation and efficient global solution. I do not find a concealed polynomial-time claim in this passage. The old complaint about history-indexed optimization variables is therefore closed.

### 4.3 A generality observation that sharpens the novelty question

The core of the new moment argument does not require monomials. Let Theta be a standard Borel latent space and let k_1,...,k_J be any bounded measurable nonnegative cells summing to one, with the same positivity assumptions when positive evidence is needed. Keep the same acceptance/failure channel, prescribed independent command laws, and future likelihoods that are products of these cells' linear combinations. Then:

1. The implementability body is unchanged.
2. Every conditional state law lies in the span of degree-n cell monomials, by the displayed recursion.
3. The loss calculation uses only the moments of cell products through degree N.
4. The same finite-action purification applies when the command laws are atomless.

These statements follow by the same finite induction and conditional-independence calculation; no monomial tangent, exponent sum or total positivity is used. This observation is not a counterexample and is not presented as an established priority theorem. It identifies which part of the mechanism is a general finite-mixture construction and which part is the manuscript's special attained collision geometry.

The manuscript would be conceptually stronger if it stated this distinction. It would be weaker if it used the broad validity of the controller algebra as a substitute for proving the special geometric result. The latter remains the demanding part.

### 4.4 Purification and polyhedral scalarization

The finite-moment purification proof is sound under atomlessness of the command law. The feasible weak-star compact convex set has an extreme point. If two coordinates are positive on a set of positive measure, partitioning that set into d+1 pieces supplies a nonzero bounded perturbation annihilating d moment constraints. Extremality then forces a pure partition. Applying this separately to accepted reports with weight g_k and jointly to the failure weights 1−g_k preserves the entire one-step matrix. Induction preserves every q_{n,i}(t), not just one numerical objective. [S7: `lem:v33-purification`, `thm:v33-pure`]

Dvoretzky–Wald–Wolfowitz is explicitly credited, and that attribution is appropriate. It would be unfair to accuse the manuscript of presenting an unattributed purification principle. The same observation explains why the theorem is a useful application of a classical mechanism rather than a new general purification theorem. The atomlessness belongs to acquisition, so a singular latent prior causes no difficulty. The assertion does not purify individual-history risk or a persistent public seed. [L3]

For a nonnegative weighted sum of checkpoint mean risks, freezing decoder tables makes the objective affine in any one time-state matrix. A path uses that time only once. Replacing one matrix by an exposed minimizer preserves global optimality, and repeating finitely many times gives command-independent accepted updates and affine-comparison failure regions. This replacement proof is valid even for atomic command laws. [S7: `thm:v33-polyhedral`]

The theorem is scalarized. There is no justification for exchanging min and max over checkpoints merely from this result, and the manuscript does not do so. Deterministic attainment of the checkpoint maximum in the atomless case follows from purification, not from an unsupported claim that every Pareto-optimal point is exposed. Tie-broken polyhedral regions can have half-open boundary conventions; these should be described carefully for atomic laws, but this is a minor terminology point rather than a proof failure.

### 4.5 Compact collision transfer

The fixed implementability domain is calibration-independent. Uniform continuity of the cells and their finite products, positive evidence in B_n, and the continuous perspective extension imply joint continuity of the finite-M objective. Compact minimization then yields value continuity and convergence of subsequences of optimal matrices to an optimal limit. The finite polynomial recursion gives uniform-in-latent-parameter convergence of occupancies along that subsequence. [S7: `thm:v33-collision`]

These are correct compactness conclusions. They do not imply convergence of the realized Borel partitions themselves, an optimizer phase diagram, a modulus uniform as M grows, or a sharp causal penalty. The appended two-sided Xi comparison is obtained by substituting the exact representation into the already proved collision theorem. It is not an independent derivation of that geometric classification.

**Finding:** useful consistency of the two descriptions, but limited additional structural information about optimal policies at collisions.

## 5. Exact example: the global lower bound is real

The new example is in the original per-report model. Its two future likelihoods span the full affine test space, the command law is continuous on a genuine cube, and the latent prior is uniform with full support. Positivity and trial accounting are explicit. [S9: `thm:v33-exact-example`]

Let a = 1/240 and let Y be the centered full-history prediction for the nonconstant query. The acquired law has atoms of mass 1/4 at each of +a and −a and a symmetric central part of mass 1/2 supported in [−a/10,a/10]. On failure, the density includes the evidence factor (u+v)/2. Consequently

$$
\mathbb EY^2=a^2(1/2+J_*/2).
$$

For a stochastic binary encoder Q, put p = EQ and v = E(YQ). The best explained variance is v^2/[p(1−p)]. Conditional averaging of Q given Y loses nothing for these two quantities. Label complementation and symmetry reduce the upper-bound argument to 0 < p <= 1/2 and v >= 0. When p <= 1/4, v <= ap. When p = 1/4+s, the upper-tail selection gives v <= a(1/4+s/10), and

$$
(1/4+s)(3/4-s)-3(1/4+s/10)^2
=s\{7/20-(103/100)s\}\ge(37/400)s
$$

for 0 <= s <= 1/4. The explained variance is at most a^2/3 and is attained by selecting only the positive atom. This covers all Borel stochastic encoders, not a selected finite family. Subtracting and applying the query weight 1/2 gives the printed exact value.

I independently evaluated the rational enclosure using a different integral reduction from the author's binomial expansion. With X,Z uniform on [−1/20,1/20], diamond coordinates s = X+Z and d = X−Z give

$$
\mathbb E[d^2s^{2k}]
=\frac{4\,10^{-(2k+2)}}{(2k+1)(2k+2)(2k+3)(2k+4)}.
$$

Summing k = 0,...,5 and applying the stated nonnegative geometric tail bound reproduces

$$
L=\frac{18108150189130829}{12454041600000000000000},\qquad
U=\frac{150901251576091}{103783680000000000000},
$$

$$
U-L=\frac{1}{136857600000000000000}.
$$

The decoder values 121/240 and 359/720 were also independently reproduced. The analytical argument supplies global coverage; the script evaluates that argument's rational consequences. Neither should be represented as a formal proof-assistant verification of the other.

**Finding:** the example closes the preceding original-model certificate request. Its limitation is significance, not validity: N = 2 has only one acquisition checkpoint, so it cannot reveal a genuinely multi-checkpoint causal trade-off. It also contains no additive collision. Those facts must not be used to deny that it is a legitimate original-model example.

## 6. Remaining major concerns

### R33.1 — Locate the controller body in comparison-of-experiments theory

**Type:** major conceptual positioning; not an identified false theorem.

The explicit identity A_M = {EU} in Section 4.1 of this report should be incorporated into the mathematical discussion, together with the appropriate classical references and the exact novelty claim. Section 13 currently emphasizes finite-controller optimization, finite approximation, channel continuity and DWW purification. These are relevant, but the immediate static object is a garbling region. The support function is its Bayes decision functional, and the overlap is preservation of a shared submeasure.

A useful response would separate the known framework, the special acceptance/failure formula, the polynomial occupancy closure, and the genuinely new coupling to acquired collision geometry. It would not merely add the word Blackwell to a bibliography. I have not established that any one prior source already contains the manuscript's full common-controller theorem. [S7, S8; L4, L5]

### R33.2 — Distinguish an exact representation from a classification of optimal causal behavior

**Type:** major significance and claim hierarchy.

The new program is an exact, smaller representation. That is a real answer to v32. Its minimum remains a nonconvex optimization over all time-state matrices, with a potentially costly baseline. The polyhedral theorem concerns scalarizations, and the collision theorem gives fixed-M compactness of optimal coefficient arrays. Together they do not yet determine which information an optimal common controller retains, how it reallocates labels between competing checkpoints, or whether a nontrivial causal price appears at a collision.

There are two legitimate ways to improve the case. One is to extract a consequential same-model conclusion from this representation, for example an analytically certified multi-checkpoint comparison or an informative structural characterization of a class of optimizers. The other is to argue, with substantially greater precision, that the attained collision classification alone supplies the exceptional contribution and to present the controller algebra as its realization theory. These are alternatives, not cumulative demands for a continually expanding paper. No particular unsolved strengthening is made a compulsory correctness condition.

The N = 2 certificate cannot answer the multi-checkpoint question because there is only one checkpoint. More decimal places for the same example would not change that. Nor would another arbitrary precision exponent.

### R33.3 — Make the exceptional contribution unmistakable

**Type:** major editorial significance; priority remains unresolved, not disproved.

The attained all-budget collision law is the most persuasive mathematics in the paper. The nontrivial points are the attainable binomial tangent, full-support mixed pairing, simultaneous confluent flag attainment with actual acquired mass, and a whole-image cover compatible with reachable raw updates. The paper deserves credit for proving these points rather than assuming them.

The current new-results narrative nevertheless gives several classical consequences nearly the same rhetorical weight. The selected companion comparisons already concede that stable filtering recursions, finite approximation and ordinary quantization are not new principles. Those concessions should inform the main hierarchy, not be relegated to qualifications around an ever-growing list of named theorems. [S13]

A precise comparison should identify what a known interpolation or quantization result would establish before attainment is proved, and exactly what it would leave open. Conversely, it should not imply that the entire problem is routine merely because the tools are classical. The present review has not established duplication of the main geometric result; the issue is that the manuscript's exceptional-journal case is still not sufficiently concentrated and persuasive.

### R33.4 — Keep model and quantifier boundaries attached to conclusions

**Type:** important exposition and scope control; largely repaired already.

The manuscript generally states these boundaries correctly. They should remain adjacent to the conclusions, particularly in abstracts, summaries and future revision responses:

- The exact centroid moment program uses prescribed independent acquisition, not a controller-dependent benchmark B_n.
- Purification preserves the mean-risk vector; it does not establish equality of randomized and deterministic worst-history optima or eliminate a persistent public seed.
- Polyhedral realization for a weighted sum does not imply a minimax exchange.
- Compact collision transfer is at fixed M; the all-budget rate comes from the separate attained geometry theorem.
- Uniformity across a compact exponent chamber is not uniformity over all full-support priors, growing horizons, or changing detector complexity.

These are not newly discovered contradictions. Their purpose is to prevent corrected statements from being expanded again in interpretation. The new generality observation in Section 4.3 would help identify the boundary between the general finite-mixture algebra and monomial-specific information geometry.

### R33.5 — Reproducibility is now evidence, not the main publication argument

**Type:** provenance and editorial proportion.

The author has provided current local execution records and an executed original-model certificate. This should be acknowledged without requiring the general astronomical controller net to be run at every budget. A readable complete main article of the reported length is not disqualified by the existence of a long archival companion. Preservation of historical derivations is not itself a defect.

At the same time, successful arithmetic, compilation, source-hash matching and contact-sheet inspection establish different things. They cannot certify the mathematical proofs or their originality. In the next revision, the publication case should not turn on a larger count of diagnostic checks, pages, receipts or reference passes. This report's own diagnostics have the same limitation.

## 7. Independent execution and its limits

The accompanying `independent_checks.py` uses only the Python standard library, exact `fractions.Fraction` arithmetic, and explicit exceptions rather than assertions. It was executed under Python 3.13.5 both normally and with `-O`; the resulting JSON files were byte-identical. The committed output is `INDEPENDENT_CHECKS.json`, with execution and coverage qualifications in `AUDIT_RECORD.json`.

The checks consist of:

1. **Independent continuous-example arithmetic:** the diamond-coordinate formula above, the two enclosure endpoints, their width, the decoder values, the next positive series term and the 37/400 algebraic margin. The continuum upper-tail argument is reviewed analytically, not established by a finite test.
2. **Implementability support:** all 64 deterministic transition maps for a two-command, two-cell, two-label experiment, tested against 81 integer-valued linear functionals. Exact support values match the printed formula and every tested matrix satisfies the common-failure overlap. This finite-law test is within the extended prescribed-law model, not the principal uniform-cube instance.
3. **Multi-stage occupancy and risk:** a fixed nontrivial rational stochastic controller with one shared uniform latent parameter and three acquisition stages. Direct enumeration of 6, 36 and 216 command/report histories agrees with the occupancy polynomials, formal multinomial identities and mean-risk formula at every checkpoint. Future probes use the remaining trials of horizon N = 4. This is a consistency test of one controller, not optimization of the multi-checkpoint problem.
4. **Collision flags:** seven exact-rational two-parameter configurations, including the intersection, all three collision lines, generic configurations and a near-tangent configuration. All nine Leja-volume comparisons and the predicted distinct-node counts agree. These tests do not prove a continuum entropy estimate or uniform attainment.

The script SHA-256 is `50dd32ea1337ce30d3230065ea5c199431bb50fc81f8c017dcc6c6ab8f357c26`. The output SHA-256 is `5f9847b28f8c8222cba145e7badcc49b4806c282f70cf83d08327ae88b2828e4`.

No floating-point optimizer, general continuous-controller enumeration, formal proof assistant, independent manuscript PDF rendering, complete companion audit or independent native two-volume build is claimed. The author certificate script was read; the present execution used independently written calculations rather than a claimed rerun of that script.

## 8. Actionable disposition

A further response should explicitly close R32.1, the concrete history-variable part of R32.2, the model-admissibility part of R32.4, and the absence-of-delivery part of R32.5. The approximation-literature response to R32.3 should be retained. No proof needs to be deleted merely to simulate a more focused article.

The remaining priorities are narrower than another wholesale rewrite: identify the implementability body as the appropriate postprocessing region and give the exact comparison; make the separation between general finite-mixture closure and monomial-specific geometry explicit; and present a defensible hierarchy in which the publication-bearing collision theorem is evaluated on its actual novelty and consequences. A genuinely multi-checkpoint consequence would strengthen the new controller layer, but a new theorem is not the only admissible answer to the editorial issue.

My final recommendation remains rejection at the requested exceptional-journal level on the present showing. The mathematical assessment is substantially more favorable than an allegation of a broken principal theorem. The correct response to this report is not to manufacture stronger claims or conceal qualifiers. It is to make the surviving, nontrivial theorem and its relation to existing mathematics decisive enough to support the intended venue.

## Source map

All S-references below are pinned to the reviewed commit unless the historical review is explicitly identified. Labels in the report identify the relevant statements within each source. Primary literature is used for the specified comparison only, not as a claim of exhaustive priority certification.

**S0.** [Controlling commit](https://github.com/TrillionniumFoundation/theta-theory/commit/e7dfc3a0e1c8d7a9d3be6b7f52944c5c7c59bb0c).

**S1.** [Main entry point](https://github.com/TrillionniumFoundation/theta-theory/blob/e7dfc3a0e1c8d7a9d3be6b7f52944c5c7c59bb0c/papers/A1-english-v33-moment-controllers/main.tex), [experiment](https://github.com/TrillionniumFoundation/theta-theory/blob/e7dfc3a0e1c8d7a9d3be6b7f52944c5c7c59bb0c/papers/A1-english-v33-moment-controllers/core/02_experiments.tex), [persistent resource](https://github.com/TrillionniumFoundation/theta-theory/blob/e7dfc3a0e1c8d7a9d3be6b7f52944c5c7c59bb0c/papers/A1-english-v33-moment-controllers/text/operational_model.tex), and [risk quantifiers](https://github.com/TrillionniumFoundation/theta-theory/blob/e7dfc3a0e1c8d7a9d3be6b7f52944c5c7c59bb0c/papers/A1-english-v33-moment-controllers/risk_criteria.tex).

**S2.** [Exact transversality and causal continuous state](https://github.com/TrillionniumFoundation/theta-theory/blob/e7dfc3a0e1c8d7a9d3be6b7f52944c5c7c59bb0c/papers/A1-english-v33-moment-controllers/core/03_transversality.tex).

**S3.** [Collision flags and attained mass](https://github.com/TrillionniumFoundation/theta-theory/blob/e7dfc3a0e1c8d7a9d3be6b7f52944c5c7c59bb0c/papers/A1-english-v33-moment-controllers/text/collision_flags.tex).

**S4.** [Checkpoint and common-controller collision classification](https://github.com/TrillionniumFoundation/theta-theory/blob/e7dfc3a0e1c8d7a9d3be6b7f52944c5c7c59bb0c/papers/A1-english-v33-moment-controllers/text/collision_direct.tex).

**S5.** [Confluent positivity and real-geometric input](https://github.com/TrillionniumFoundation/theta-theory/blob/e7dfc3a0e1c8d7a9d3be6b7f52944c5c7c59bb0c/papers/A1-english-v33-moment-controllers/text/analytic_inputs.tex).

**S6.** [Collision phases and bit law](https://github.com/TrillionniumFoundation/theta-theory/blob/e7dfc3a0e1c8d7a9d3be6b7f52944c5c7c59bb0c/papers/A1-english-v33-moment-controllers/text/collision_consequences.tex).

**S7.** [Complete v33 moment-controller module](https://github.com/TrillionniumFoundation/theta-theory/blob/e7dfc3a0e1c8d7a9d3be6b7f52944c5c7c59bb0c/papers/A1-english-v33-moment-controllers/v33/moment_controllers.tex).

**S8.** [Finite compatibility and approximation](https://github.com/TrillionniumFoundation/theta-theory/blob/e7dfc3a0e1c8d7a9d3be6b7f52944c5c7c59bb0c/papers/A1-english-v33-moment-controllers/v33/finite_compatibility.tex), [arbitrary precision](https://github.com/TrillionniumFoundation/theta-theory/blob/e7dfc3a0e1c8d7a9d3be6b7f52944c5c7c59bb0c/papers/A1-english-v33-moment-controllers/v33/precision.tex), and [main comparison](https://github.com/TrillionniumFoundation/theta-theory/blob/e7dfc3a0e1c8d7a9d3be6b7f52944c5c7c59bb0c/papers/A1-english-v33-moment-controllers/v33/comparison.tex).

**S9.** [Continuous-command exact example](https://github.com/TrillionniumFoundation/theta-theory/blob/e7dfc3a0e1c8d7a9d3be6b7f52944c5c7c59bb0c/papers/A1-english-v33-moment-controllers/v33/exact_instance.tex) and [author's rational evaluator](https://github.com/TrillionniumFoundation/theta-theory/blob/e7dfc3a0e1c8d7a9d3be6b7f52944c5c7c59bb0c/papers/A1-english-v33-moment-controllers/v33/certify_instance.py).

**S10.** [Controlling v32 referee report](https://github.com/TrillionniumFoundation/theta-theory/blob/60c5b116a2c002dfd8056a351a87d7014d8c78e1/reviews/a1-english-v32-harsh-independent-2026-09-08/REFEREE_REPORT.md).

**S11.** [V33 response](https://github.com/TrillionniumFoundation/theta-theory/blob/e7dfc3a0e1c8d7a9d3be6b7f52944c5c7c59bb0c/papers/A1-english-v33-moment-controllers/RESPONSE_TO_REFEREE_V33.md).

**S12.** [Author build receipt](https://github.com/TrillionniumFoundation/theta-theory/blob/e7dfc3a0e1c8d7a9d3be6b7f52944c5c7c59bb0c/papers/A1-english-v33-moment-controllers/verification-v33/BUILD_RECEIPT.json) and [author session checks](https://github.com/TrillionniumFoundation/theta-theory/blob/e7dfc3a0e1c8d7a9d3be6b7f52944c5c7c59bb0c/papers/A1-english-v33-moment-controllers/verification-v33/SESSION_CHECKS.json).

**S13.** [Inherited filtering comparison](https://github.com/TrillionniumFoundation/theta-theory/blob/e7dfc3a0e1c8d7a9d3be6b7f52944c5c7c59bb0c/papers/A1-english-v33-moment-controllers/sections/filter_quantization_comparison.tex), [information-state comparison](https://github.com/TrillionniumFoundation/theta-theory/blob/e7dfc3a0e1c8d7a9d3be6b7f52944c5c7c59bb0c/papers/A1-english-v33-moment-controllers/sections/comparison.tex), and [finite-pairing comparison](https://github.com/TrillionniumFoundation/theta-theory/blob/e7dfc3a0e1c8d7a9d3be6b7f52944c5c7c59bb0c/papers/A1-english-v33-moment-controllers/sections/finite_pairing_comparison.tex).

**L1.** G. Comte and I. Halupczok, *Motivic Vitushkin invariants*, Compositio Mathematica 161 (2025), 959–992; [arXiv:2206.15412v2](https://arxiv.org/pdf/2206.15412v2), introduction, equations (4)–(5), printed pp. 3–4. Used only for the recalled classical real variations and entropy inequality. The introduction identifies Yomdin–Comte, Theorem 3.5, as a source; this review does not claim to have independently read that monograph in full.

**L2.** Y. Zhang and J. Kileel, *Covering Number of Real Algebraic Varieties and Beyond: Improved Bounds and Applications*, [arXiv:2311.05116v4](https://arxiv.org/pdf/2311.05116v4), Lemma 2.18, printed p. 11, with its proof in Appendix B. Used for coefficient-independent semialgebraic regularity, not as a source already proving the manuscript's acquired anisotropic law.

**L3.** A. Dvoretzky, A. Wald and J. Wolfowitz, *Elimination of randomization in certain statistical decision procedures and zero-sum two-person games*, Annals of Mathematical Statistics 22 (1951), 1–21, DOI [10.1214/aoms/1177729689](https://doi.org/10.1214/aoms/1177729689). The finite-action, finitely many atomless measures formulation is also explicitly described in M. A. Khan, K. P. Rath and Y. Sun, [*The Dvoretzky–Wald–Wolfowitz theorem and purification in atomless finite-action games*](https://link.springer.com/article/10.1007/s00182-005-0004-3), International Journal of Game Theory 34 (2006), 91–104. The manuscript's purification proof was checked directly.

**L4.** C. Amato, D. S. Bernstein and S. Zilberstein, [*Solving POMDPs Using Quadratically Constrained Linear Programs*](https://www.ijcai.org/Abstract/07/389), IJCAI 2007. The official abstract describes a desired-size finite-controller optimization formulation and distinguishes it from local numerical solution. The authors' [*Optimizing Memory-Bounded Controllers for Decentralized POMDPs*](https://arxiv.org/abs/1206.5258), Section 4.1, supplies another explicit finite-controller nonlinear-programming precedent. These precedents do not automatically supply the present objective, command body, no-seed resource or collision geometry.

**L5.** D. Blackwell, *Equivalent comparisons of experiments*, Annals of Mathematical Statistics 24 (1953), 265–272, DOI [10.1214/aoms/1177729032](https://doi.org/10.1214/aoms/1177729032). Bibliographic identification is available in the [collected publication record](https://celebratio.org/Blackwell_DH/article/26/). The original publisher full text was not successfully retrieved in this session; no unverified theorem number or verbatim quotation is attributed to it. The postprocessing identification needed for this report is proved explicitly in Section 4.1 above.

**L6.** N. Saldi, S. Yüksel and T. Linder, [*Near optimality of quantized policies in stochastic control under weak continuity conditions*](https://doi.org/10.1016/j.jmaa.2015.10.008), Journal of Mathematical Analysis and Applications 435 (2016), 321–337; and S. Yüksel and T. Linder, [*Optimization and Convergence of Observation Channels in Stochastic Control*](https://doi.org/10.1137/100808976), SIAM Journal on Control and Optimization 50 (2012), 864–887. Publisher descriptions confirm the finite-action and observation-channel-continuity antecedents. This review does not claim a complete theorem-by-theorem subsumption audit of all the approximation papers cited in v33.
