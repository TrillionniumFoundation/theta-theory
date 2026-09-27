# Referee Report — General Theta Foundations I, Revision 46

**Manuscript:** *General Theta Foundations I: Certified Positive Realization of Numerical Word Experiments*  
**Repository:** `TrillionniumFoundation/theta-theory`  
**Reviewed revision branches:**
- `revision/general-theta-foundations-i-v46-certified-hankel-2026-09-27`
- `revision/general-theta-foundations-i-v46-source-review-2026-09-27`

**Reviewed head:** `d7914880e7df679756c3b6ae86311485ac922f8a`  
**Readable mathematical source identified by the release:** `1fa2327b39c7fd6fb220d27250a20aac26d37e4e`  
**Mathematical predecessor:** v44 publication `d7042cf71485f661e27d87d12ffae35a2edfc15c`  
**Controlling prior report:** r29, `6e8a9504a1a0820e6195317df885d99aed06c878`  
**Review branch:** `review/general-theta-foundations-i-v46-certified-positive-realization-harsh-top4-r30-2026-09-27`  
**Date:** 27 September 2026

## Recommendation

**Reject at the Annals / Inventiones / JAMS / Acta level.**

**Mathematical disposition:** I did not find a fatal counterexample to the new finite-horizon statements after checking the all-word Gram identity, the failed-word extraction, the even-moment sandwich, the rational-grid approximation, the zero-command planar frontier, and the stochastic normalization used in the nonnegative-factorization comparison. Several of these statements are clean and useful. The rejection is not based on a claim that the new section is mathematically empty or obviously wrong.

The decisive problem is that Revision 46 does not contain a four-journal advance. Its new core consists primarily of:

1. a finite dynamic-programming/Gram expansion of the sum of squared word residuals;
2. the finite-dimensional normalized `L^p`–`L^∞` comparison, followed by compactness;
3. elementary rational-grid rounding of stochastic rows; and
4. a normalization that imports a known nonnegative-rank complexity and field-sensitivity result into a categorical-output stochastic factorization problem.

These are legitimate ingredients, but they do not produce a new structural theorem for positive realization, a classification of the manuscript's width invariant, a broad new arithmetic law, or a solution of a major open problem. The inherited arithmetic-width theory remains the mathematically stronger part of the paper, and its scope and unresolved limitations are substantially the same as in the v43–v44 line.

**Disposition outside the four leading general journals:** major revision, substantial compression, and likely division into separate papers before submission to a strong specialist journal. A focused article on arithmetic positive-realization width could be worthwhile. A separate short paper or note on finite-horizon certificates could also be worthwhile if its algorithmic claims, input model, and relation to existing weighted-automata/positive-realization methods are sharpened. The present accretive package should not be submitted in its current form.

---

## 1. Scope, genealogy, and what was actually reviewed

The two v46 revision branches listed above point to the same reviewed head. I therefore treat them as one mathematical revision, not as competing versions.

I read the complete readable v46 LaTeX input graph, in particular:

- `papers/GTF-I-v46-certified-hankel/main.tex`;
- `introduction.tex`;
- `machine-model.tex`;
- `hankel-compatibility.tex`;
- `finite-horizon-certificates.tex`;
- `word-profiles.tex`;
- `distortion-rate.tex`;
- `circle-optimization.tex`;
- `arithmetic-scales.tex`;
- `metric-width.tex`;
- `irrational-fluctuations.tex`;
- `finite-bit-memory.tex`;
- `comparison.tex`;
- `references.tex`;
- `RESPONSE_TO_REFEREE.md`;
- `README.md`;
- `PUBLICATION_STATUS.md`;
- `RESOURCE_LEDGER.md`;
- `PROOF_STATUS.json`;
- `PIPELINE_STATUS.json`;
- `HISTORY_AUDIT.md`;
- `LITERATURE_AUDIT.md`;
- `PREDECESSOR_MANIFEST.json`; and
- the locally recorded validation summary.

I also re-read the controlling r29 report and the repository-level Round-Seventeen dependency ledger. I inspected the current remote Actions status rather than relying only on the manuscript's last-observed status.

The genealogy is unusually important here. The release states that the ten inherited mathematical/program modules are preserved from v44, while the new mathematical material is concentrated in the finite-horizon certificate section and its surrounding introduction, comparison, bibliography, response, and evidence records. The separate v45 draft is explicitly not claimed to have received mathematical review. Accordingly, this report distinguishes:

- the inherited v43–v44 arithmetic and compatible-realization results;
- the new v46 finite-certificate layer; and
- repository publication/verification claims.

A build receipt, a preservation manifest, or a successful regression comparison would not be an independent proof of a universal theorem. Conversely, a packaging failure is not itself a mathematical counterexample. The report keeps those categories separate.

---

## 2. What Revision 46 genuinely improves

Revision 46 does answer part of the most serious conceptual criticism in r29.

### 2.1 The positive-realization object is now much better situated

The v44/v46 manuscript gives a normalized positive Hankel formulation with cut-dependent compatible future-response polytopes. It distinguishes:

- ordinary signed Hankel rank;
- nonnegative rank;
- normalized stochastic rank at an individual cut; and
- the simultaneous compatible profile required by one legal controlled stochastic machine.

That distinction is essential. The paper no longer treats low signed rank or separate nonnegative factorizations as if they automatically produced a legal dynamic realization. The planar example in which all separate ranks remain three while compatible width grows is a useful explanation of the resource being studied.

The comparison section also now acknowledges classical positive-cone realization, weighted automata, HMM realization, tensor/Hankel reductions, and nonnegative factorization. This is a substantial improvement over the literature positioning criticized in r29.

### 2.2 Candidate exactness is compressed without enumerating words

The augmented representation in `thm:gram46` is clean. With

```text
A_{t,a} = diag(T_{t,a}, U_a^T),
u_x     = (E_x, -rho x^T),
v_j     = (d_j, e_j)^T,
```

the execution-order transpose is correct even for noncommuting commands, and

```text
u_x A_w v_j = R_{x,w,j}.
```

The recursion

```text
G_0     = sum_x u_x^T u_x,
G_{t+1} = sum_a A_{t,a}^T G_t A_{t,a}
```

indeed yields

```text
S_2 = sum_j v_j^T G_N v_j
    = sum_{x,w,j} R_{x,w,j}^2.
```

Thus exact zero checks all supplied finite words, not merely average agreement. The dual backward recursion also supports deterministic extraction of a seed, word, and query with nonzero residual when `S_2>0`. This is a sound finite certificate for a *given* legal rational machine.

### 2.3 The paper now distinguishes candidate checking from global optimization

The response and resource ledger repeatedly say that:

- checking one candidate is not synthesizing a minimum-width machine;
- a local numerical minimum is not a global certificate;
- the symmetric-power recurrence represents a finite objective but does not by itself solve the global optimization;
- exhaustive small grids are not a generic optimizer; and
- exact rational realization at the optimum is not guaranteed.

These distinctions are mathematically necessary and are handled more responsibly than in many computationally presented manuscripts.

### 2.4 The new finite-error statements appear correct in their declared scope

For a fixed profile, compactness gives attainment. The normalized finite-vector inequalities give

```text
ell_p <= E <= Q^(1/p) ell_p,
```

and the monotonicity of normalized `L^p` norms gives convergence along even `p`. The rational-grid theorem follows by rowwise total-variation rounding and contraction. The zero-command planar frontier is a correct elementary convex-geometric calibration. None of these arguments appears to require an unstated observability or rank-minimality assumption.

These are real improvements in auditability. They are not enough for the claimed journal tier.

---

## 3. Detailed correctness audit of the new v46 results

### 3.1 The finite all-word Gram certificate

I regard the central identity as correct.

The rectangular block dimensions match the cut-dependent widths. The lower block in the word product is

```text
U_{a_1}^T ... U_{a_N}^T = (U_{a_N} ... U_{a_1})^T,
```

so the target residual has the stated sign and command order. The forward Gram recursion is simply a compressed sum over prefixes. The backward matrices are positive semidefinite, and if a current quadratic form is positive then one child contribution must be positive. This justifies the failed-word extraction.

The rational bit-complexity claim is plausible: the number of matrix operations is polynomial in the displayed unary horizon and matrix dimensions, while numerator and denominator bit lengths grow at most polynomially under the finite sequence of exact additions and multiplications. Nevertheless, this should be elevated from an informal sentence to a precise lemma. The paper currently mixes arithmetic-operation counting and Turing bit complexity too quickly.

For algebraic input, the existential formula is also plausible. Stochasticity, decoder bounds, Gram recursions, and `S_2=0` are semialgebraic. High-degree defining polynomials can be represented by arithmetic-circuit variables so that local equations have bounded degree. A nonempty semialgebraic set over real algebraic coefficients has an algebraic sample point.

The following qualifications are mandatory:

1. **This is membership in an existential-real formulation, not an efficient synthesis theorem.** The manuscript says this, but the theorem statement still gives the stronger rhetorical impression.
2. **The polynomial-time result is candidate verification only.** It does not find the least profile, decide growing-width feasibility in polynomial time, or optimize error.
3. **The finite Gram mechanism is classical in substance.** Its adaptation to the exact stochastic constraints is useful, but the sum-of-squares recursion is not itself a new realization-theoretic principle.
4. **The input model must be formalized in one place.** The roles of unary `N`, explicitly listed widths, binary rational encoding, algebraic defining polynomials, isolating intervals, and fixed versus variable `D` should not be distributed across prose.

### 3.2 The moment hierarchy

The inequalities in `thm:moments46` are correct, and the manuscript avoids the most obvious error: it does not interchange the minimization over machines with the maximum over words. Using an `L^p` minimizer as a candidate for the `L^∞` objective gives the upper bound in the correct direction.

However, the theorem currently packages three very different levels of content:

1. elementary norm equivalence on a finite residual vector;
2. a dynamic-programming representation of a candidate's degree-`p` moment; and
3. real-algebraic global optimization over all legal machine parameters.

Those levels should be separated. In particular, the sentence saying that the moment sum is computable by a polynomial recurrence can easily be misread as a computation of `ell_p`. The recurrence evaluates or symbolically represents the objective. It does not certify its global minimum without a separate, generally expensive semialgebraic optimization.

The “effective obtainability” of the optimum is a standard quantifier-elimination consequence. It is not an algorithmic advance unless the paper supplies a meaningful complexity bound or exploits special structure to do better than generic real algebraic geometry. At present it does neither.

The notation also needs repair. `Q` is used for the number of residuals while `\mathbb Q` is already a basic field symbol. The proof should use `|R|^p` even when `p` is declared even, because this makes the norm argument transparent and avoids accidental extension to odd `p`.

### 3.3 The rational-grid certificate

The grid sandwich is correct but elementary. Rounding the first `k-1` coordinates of a stochastic row downward and assigning the residue to the last coordinate gives total-variation error at most `(k-1)/L`. Telescoping or coupling gives the displayed cumulative bound.

One sentence is mathematically inaccurate as written:

> “dyadic machines with the same available boundary profile attain every strictly larger error than `E`.”

The proof shows the following:

> For every tolerance `tau>E`, there exists a dyadic machine on the same boundary profile whose error is **strictly less than** `tau`.

It does not show that every numerical value above `E` is attained exactly as an error. This is a small correction, but it is mandatory because the paper is explicitly about exact boundary phenomena.

The target-stability statement should likewise be phrased using threshold feasibility: a strict margin between a threshold and the optimum is stable under sufficiently small target perturbations. “Positive feasibility or infeasibility margin” is otherwise too informal.

### 3.4 The calibrated planar frontier

The one-state and two-state lower bounds are correct. A two-state mean set lies on an affine line, and `l_infinity/l_1` duality gives coordinate error at least `rho/2`, hence binary-TV error at least `rho/4`. The diagonal segment attains it. The three displayed decoder means form a legal triangle for `rho<=1/2` and contain the four target means.

This proposition is a good sanity check. It is not a substantial research result. It is a zero-command, two-dimensional convex-hull exercise, and its identity-only extension contains no new dynamics. It should not carry significant weight in the novelty claim.

### 3.5 The categorical-output complexity comparison

The stochastic normalization argument is valid. Row-normalizing a nonzero rational nonnegative matrix preserves nonnegative rank. Given `P=WH`, normalizing the rows of `H` and absorbing their row sums into `W` produces row-stochastic factors because `P1=1`.

But the result is almost entirely imported:

- existential-real hardness comes from the cited nonnegative-factorization universality theorem;
- rational/real field sensitivity comes from the cited external construction; and
- the manuscript contributes the straightforward stochastic normalization.

The proposition does **not** establish hardness for the fixed-dimensional orthogonal binary-query model that motivates the paper. It allows an explicitly listed categorical output whose alphabet may grow. The manuscript acknowledges this, and that boundary must remain in the theorem title and abstract-level discussion.

The word “optimizer” is also misleading in the exact factorization sentence. What is shown is that the minimum inner dimension over the reals need not admit a rational factorization of that same inner dimension. This should be stated directly.

---

## 4. The main unresolved conceptual gap remains

The inherited manuscript has two important but differently quantified profiles:

- a distortion profile that lower-bounds every hidden realization by testing endpoint contraction; and
- a compatible-enclosure profile that builds one particular common-polytope realization.

Revision 44 added a one-sided distortion–dilation inequality. Revision 46 adds a brute-force finite characterization of the true optimum at a fixed displayed profile. It still does **not** provide a structural characterization of the optimum that explains when either inherited profile is sharp.

This is the central missed opportunity.

A top-level advance would have been something like:

- a duality theorem between an intrinsic converse object and compatible positive realization;
- a minimax characterization of exact or approximate width;
- a broad criterion for equality in the distortion–dilation bound;
- a nontrivial complexity classification for the manuscript's fixed orthogonal binary-query subclass;
- a classification of finite alphabets by width growth; or
- a new asymptotic theorem for a broad noncommutative or higher-dimensional family.

The moment hierarchy does not fill this gap. It says that finite `L^p` objectives converge to a finite `L^∞` objective on the same compact parameter space. That is a generic norm fact, not a structural theory of positive realization.

The existential-real formula does not fill the gap either. A finite semialgebraic formulation is expected once the horizon and all widths are explicitly listed. It gives decidability and algebraic witnesses, not insight into the optimal profile.

---

## 5. Novelty and significance at the four-journal level

The strongest inherited results remain:

- the endpoint-contraction converse against arbitrary hidden states;
- the nonuniform interval budget;
- the compatible polytope synthesis;
- the one-sided distortion–dilation comparison;
- matched exponents for the special planar Diophantine classes;
- almost-everywhere logarithmic refinements;
- Liouville subsequence fluctuations; and
- the separate finite-bit compiler.

Those results form an interesting specialist program. They do not become a top-four paper merely by adjoining finite candidate certificates.

The sharp asymptotic applications remain narrow:

1. planar rotations, principally commuting;
2. minimal dual type or uniformly badly approximable classes;
3. finite rational extensions and one reflected extension;
4. no general finite-alphabet classification;
5. no sharp result for broad noncommuting alphabets;
6. no matched law at general finite Diophantine type;
7. no determination of the Liouville upper logarithmic limit; and
8. no nontrivial closed finite-width frontier beyond the elementary calibration example.

The paper is candid about several of these limitations. Candor is welcome, but it does not substitute for a theorem that overcomes them.

The current title and series branding remain disproportionate. “General Theta Foundations I” suggests a foundational theorem with broad downstream force. The mathematical content is a specialized theory of nonuniform positive stochastic realization width for controlled numerical word responses, with sharp results in particular planar arithmetic families. The subtitle is more accurate than earlier versions, but the series prefix still overstates the scope.

For a specialist submission, I recommend a title centered on one of the following:

- positive stochastic realization width for Diophantine rotation alphabets;
- finite-horizon certificates for controlled positive realization; or
- compatible positive realization of numerical word responses.

Trying to carry all three under a foundational series title weakens the paper.

---

## 6. The resource model is coherent but exceptionally permissive

The paper's primary width invariant allows:

- redesign of the whole machine for each horizon `N`;
- free knowledge of the horizon and external epoch;
- free horizon-dependent row tables;
- free table construction and lookup;
- exact real arithmetic;
- atomic exact sampling of arbitrary prescribed real stochastic rows; and
- correctness only for the terminal selected query, not an anytime interface.

All persistent history and private randomness must be represented in the current label, which makes the label lower bounds meaningful. Nevertheless, this is not ordinary computational memory, program size, random-bit space, or implementable finite-state complexity.

The separate finite-bit compiler is valuable precisely because it addresses a different model. But it is proved only for a special planar angle setting and does not retroactively price the exact-real rows in the general theorems.

The abstract and introduction should therefore use “nonuniform clocked positive-realization label width” consistently. The word “memory” should be reserved for statements that explicitly include the corresponding implementation resources.

A reader should not have to reconstruct the resource distinction from a ledger file. The article itself needs one boxed definition or table comparing:

1. exact nonuniform atomic-row width;
2. table size and coefficient description;
3. random-bit complexity;
4. uniform work space;
5. time complexity; and
6. anytime versus fixed-horizon correctness.

---

## 7. Literature positioning is improved but not yet decisive

The manuscript now correctly recognizes several classical antecedents:

- probabilistic-automata equivalence;
- weighted-automata/Hankel and tensor-square constructions;
- positive realization via invariant cones;
- HMM and stochastic realization;
- nonnegative-factorization universality and field dependence; and
- real algebraic elimination.

This repairs a serious defect in the earlier line. However, the repository's own literature audit says it is not an exhaustive priority clearance. That is accurate.

For publication, the author should produce a theorem-by-theorem novelty table with columns:

```text
claim in this paper | closest known result | exact added hypothesis/objective | exact new conclusion
```

In particular:

- the Gram recursion should be presented as a constrained finite-horizon specialization, not as a newly discovered equivalence principle;
- the moment statement should be separated from existing weighted `l_2` approximation and from generic finite norm equivalence;
- the positive Hankel normal form should be explicitly related to classical cone and stochastic-language formulations;
- the categorical factorization proposition should be identified as a transfer lemma for an external hardness theorem; and
- internal revision citations should not replace conventional archival references when the underlying mathematics has established antecedents.

The current comparison section is thoughtful, but the paper still lacks a compelling statement of why its new finite certificates change what experts can prove rather than merely what they can encode.

---

## 8. Relation to the repository-wide paper pipeline

The repository-level Round-Seventeen ledger contains two major dependency chains:

```text
A2 -> A3 -> A4 -> C2 -> D1
```

and

```text
B2-GC -> B1 -> B2-MC -> B3 -> B4 -> C1 -> C2 -> D1.
```

Their gates require Fourier/local-limit, stopped-LDP, global-kernel, nonlinear-semigroup, filtering, strict/form response, and labelled-contraction arguments. The v46 Gram, moment, grid, and finite factorization statements do not discharge any of those analytic gates.

The manuscript's own `PIPELINE_STATUS.json` correctly records that:

- the B4 aggregate is not closed;
- the C2 aggregate is not closed;
- the eleven-paper aggregate is not closed;
- historical A2 has not been replaced; and
- the v45 draft has not been mathematically reviewed.

This honesty is a strength. The consequence is that repository accumulation cannot be used as evidence of foundational closure or general-journal significance. Revision 46 is mathematically orthogonal to most of the controlling A/B/C/D proof DAG.

The paper should make one of two choices:

1. **Decouple from the pipeline.** Present a self-contained specialist paper whose contribution is judged on its own theorems.
2. **Prove an explicit dependency theorem.** State exactly which downstream result uses the new positive-realization machinery and why the new theorem closes a previously open mathematical gate.

At present it does neither. The “Foundations” branding therefore creates a pipeline expectation that the actual dependency graph does not support.

No theorem credit should be assigned merely because predecessor PDFs, cumulative volumes, or verification scripts are preserved. The current report assigns none.

---

## 9. Remote verification and publication status

The reviewed source is readable, but the remote publication record is not current.

`PUBLICATION_STATUS.md` says that workflow `36260243370` was queued at the last read. As of this review, that run has completed with **failure**.

The failure was not a failed mathematical test. The workflow:

1. checked out the old trigger head `d158ff0f5f45bcbad96a2fadd8b9d0848a892638`;
2. successfully restored twenty-eight native source files from the transport payload;
3. created a local source commit; and
4. failed when pushing because the remote branch had advanced, producing a non-fast-forward rejection.

The dependency installation, complete verification/build, isolated rebuild, publication, and artifact-upload success path were then skipped. Therefore there is no successful remote exact-head build or verifier receipt for v46.

Moreover, the reviewed head does not publish the new native `certify.py`, `verify.py`, and `build.py` files. The release explicitly says they exist only in a separately delivered local package. The local receipt is honestly labelled `local-uncommitted`, but it is not a reproducible Git binding for an external referee.

Required corrections:

1. update every status file that still describes the run as queued;
2. publish the native verifier/build sources at the exact reviewed head;
3. run the workflow on that exact head without a self-publishing race;
4. make verification read-only with respect to the branch under test, or publish through a separate controlled job;
5. obtain a successful remote build and isolated rebuild receipt tied to the exact source SHA; and
6. retain the distinction between build success and mathematical certification.

This reproducibility issue is not the reason for the top-four rejection. It is nevertheless a release blocker for any computationally supported submission.

---

## 10. Required mathematical and editorial revision

Before any serious resubmission, I would require the following.

### 10.1 Choose one central paper

The current article combines:

- compatible positive Hankel realization;
- distortion/enclosure profiles;
- arithmetic width exponents;
- Liouville fluctuations;
- a finite-bit compiler;
- finite Gram verification;
- moment convergence;
- rational grids; and
- an imported factorization complexity boundary.

This reads as a revision archive, not as a paper organized around one decisive theorem.

The author should split the work unless a genuinely unifying structural theorem is added. My preferred division is:

1. **Arithmetic positive-realization width:** the packet converse, compatible synthesis, distortion–dilation comparison, arithmetic laws, and finite-bit compiler.
2. **Finite controlled positive-realization certificates:** normalized Hankel compatibility, the all-word certificate, exact semialgebraic feasibility, finite-error approximation, and complexity boundaries.

Each paper would then need its own focused introduction and independent novelty claim.

### 10.2 Add a nontrivial structural theorem or reduce the claims

For the certificate paper to be more than a competent note, it should prove at least one result not supplied by generic finite-dimensional compactness or quantifier elimination. Examples include:

- a dual certificate for profile infeasibility of controlled stochastic realization;
- a complexity classification for a fixed-dimensional binary-query subclass;
- an efficiently computable hierarchy with certified convergence under meaningful structural assumptions;
- a theorem relating the moment hierarchy to the distortion/enclosure profiles;
- a broad exact-width characterization; or
- a nontrivial lower bound on certificate degree/size.

Without such a result, the new v46 contribution should be presented modestly as a finite certification framework.

### 10.3 Formalize the computational statements

Create a dedicated theorem/definition block specifying:

- the bit model;
- whether `N` is unary or binary;
- how dimensions and widths are encoded;
- rational numerator/denominator heights;
- algebraic-number encoding;
- whether `D` and `p` are fixed or variable;
- arithmetic-operation complexity versus Turing complexity;
- the output format of a failed word;
- the output format of an algebraic witness; and
- which claims are merely existential-real membership.

Give an explicit polynomial bit-length bound for the rational Gram recursion. Separate “objective circuit construction” from “global optimum computation” in `thm:moments46`.

### 10.4 Correct exactness language

Replace the grid theorem's “attain every strictly larger error” sentence by a tolerance statement. Replace “rational exact optimizer” in the factorization discussion by a statement about rational factorization at minimum real inner dimension. Define strict feasibility/infeasibility margins precisely.

### 10.5 Demonstrate nontrivial use of the new certificates

The current evidence verifies candidates and tiny one-cut grids. Add at least one genuinely dynamic example in which:

- the horizon is nonzero and commands do not all act identically;
- the exact optimum or a rigorous narrow interval is obtained;
- the compatible Hankel profile, Gram certificate, moment bound, and grid bound can be compared; and
- the example teaches something not visible from rank alone.

The zero-command frontier is not enough.

### 10.6 Reframe the pipeline and title

Either prove a concrete downstream dependency or remove the foundational/pipeline suggestion from the title and front matter. The open A/B/C/D gates should remain explicitly open.

### 10.7 Complete the reproducible release

Publish the exact code, repair the workflow race, run exact-head CI, and update stale status records. Do not treat a local package delivered in a chat as archival supplementary material.

---

## 11. Minor and local comments

1. In `thm:gram46`, state one matrix dimension line explicitly; this will help readers verify the rectangular block recursion.
2. Give a named lemma for polynomial rational bit growth rather than saying common-denominator bounds suffice.
3. Distinguish “legal candidate verification” from the legality constraints inside the existential formula.
4. Replace `R^p` by `|R|^p` in the moment definition, even for even `p`.
5. Define exactly what “running minima of the right sides” means.
6. Avoid using `Q` both for the rational field and for the number of residual coordinates.
7. In the semialgebraic optimization proof, say that sampling occurs in the fiber at the algebraic optimum, not merely “above” the endpoint.
8. The grid terminal rounding constant can be sharpened if nearest rounding is used; either sharpen it or say the stated `1/L` is deliberately crude.
9. In `prop:smallfront46`, make explicit that the decoder mean vectors lie in `[-1,1]^2` because `rho<=1/2`.
10. In the identity-only extension, spell out the conditioning argument at a narrowest cut in one sentence.
11. In `prop:hard46`, state the exact decision problem and encoding before declaring existential-real completeness.
12. Cite the exact theorem/corollary version used for nonnegative-rank hardness and field separation.
13. The abstract is overloaded. It lists inherited and new results in a way that obscures the principal contribution.
14. The introduction contains too much defensive boundary language. Some is necessary, but much belongs in a scope subsection or appendix.
15. Internal manuscript revisions should not dominate the bibliography of a journal submission.
16. Repository commit hashes belong in a reproducibility appendix, not in the mathematical narrative.
17. The manuscript should say explicitly whether the selected terminal query is announced only after the word and whether all decoder columns must coexist in one machine; the formal model implies this, but the operational wording should match.
18. “Polynomial-size exact feasibility formula” must always be qualified by the explicitly displayed profile and unary horizon.
19. The finite-word table has exponential cardinality even when the formula is compressed; explain what information about the target is supplied succinctly and what is generated from the orthogonal alphabet.
20. The response to r29 should not spend space disputing the rhetoric of the prior minimum-bound comment. The corrected displayed minimum is enough.

---

## 12. Assessment by criterion

| Criterion | Assessment |
|---|---|
| Correctness of new v46 core | Mostly sound; no fatal counterexample found; several statements need precision repairs |
| Novelty of new v46 core | Limited; mainly constrained repackaging of classical finite linear algebra, norm equivalence, rounding, and external NMF results |
| Significance | Interesting for a specialist audience; insufficient for a leading general journal |
| Breadth | Sharp results remain concentrated in planar arithmetic families; no broad classification |
| Conceptual unity | Weak; the paper is accretive and lacks one governing structural theorem |
| Literature positioning | Much improved, still not an exhaustive or decisive priority analysis |
| Resource semantics | Explicit but highly nonuniform/permissive; not ordinary computational memory |
| Reproducibility | Incomplete; remote workflow failed before build and exact verifier sources are absent at the reviewed head |
| Pipeline closure | Explicitly open; v46 does not close the major repository DAG gates |
| Exposition | Technically careful but overloaded and defensive; substantial restructuring needed |

---

## Final recommendation

Revision 46 is a competent and more intellectually honest manuscript than several earlier versions in this line. It now states the positive-realization object more clearly, acknowledges the right neighboring theories, and supplies a correct finite candidate certificate. Those are meaningful advances in presentation and auditability.

They do not amount to an Annals/Inventiones/JAMS/Acta contribution. The new finite section is too close to standard finite weighted-representation algebra, finite norm comparison, generic real-algebraic decidability, and elementary stochastic rounding. It does not solve the structural width problem posed by the inherited paper, broaden the sharp arithmetic classification, or close the repository's foundational proof pipeline.

**Recommendation: reject at the four leading general journals.**  
**Possible future disposition: major revision and division into focused specialist papers, after the mathematical, complexity-model, literature, and reproducibility requirements above are met.**
