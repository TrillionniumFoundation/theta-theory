# Referee Report — General Theta Foundations I, Revision 30

**Manuscript:** *General Theta Foundations I: Positive Realization and Exact Streaming Memory*  
**Repository:** `TrillionniumFoundation/theta-theory`  
**Reviewed branch:** `revision/general-theta-foundations-i-v30-referee-ready-2026-09-24`  
**Reviewed head:** `a4abeb1c5e0323e5850e7f2446bf96fb1f7d4d8a`  
**Native mathematical source recorded by the manuscript:** `24b98c1a87382104d10ebf518ca90bddb35416fc`  
**Controlling previous report:** `c039e5bc8bc8b30fca92246bc1458f66214522e1`  
**Previous reviewed manuscript:** `b0bd13753456c15815b174db1106e2ce6ee7433b`  
**Review branch:** `review/general-theta-foundations-i-v30-streaming-geometry-pipeline-harsh-top4-r15-2026-09-24`  
**Date:** 24 September 2026

## Recommendation

**Reject at the Annals / Inventiones / JAMS / Acta level.**

This is not a recommendation for another ordinary revision cycle at that level. Revision 30 is a serious and substantially better paper than revision 29: it is shorter, mathematically focused, and it directly attacks the previous report's two strongest local objections. The residual-hull simplex hypothesis has been replaced by an if-and-only-if compatibility formulation for support-rank saturation, and the binary-query example is now treated throughout the fixed interior signal range at the level of its first-order exponential memory rate. The article also gives an explicit online reservoir, a Hadamard-based endpoint construction, a row-error exponent, and a concrete residual-automaton versus unrestricted-positive-automaton separation.

I did not find a short fatal counterexample to the principal displayed theorems in the **very specific clocked, atomic-row, one-query model actually stated**. The face-separation lower bound, the reservoir process, the entropy-cap argument, the random-codebook enclosure, the charged block construction, and the total-variation attenuation argument are internally coherent. The negative recommendation is therefore not based on a claim that the new theorem statements are obviously false.

The decisive problems are mathematical level, originality, and scope.

1. The new “coherent rank enclosure” theorem is, after the all-stochastic face lower bound inherited from revision 29, very close to a coordinate restatement of the existence of a rank-saturating machine. Its witness consists precisely of rank-many state continuations together with the common positive transition coefficients that make those continuations into one machine. This is a correct equivalence, but not yet a structural classification of positive realizability of four-journal depth.
2. The entropy exponent is classical random-access coding, as the paper now correctly acknowledges. The exact-row convex-hull formulation and the pricing of an elementary blockwise streaming implementation are useful refinements, but the paper obtains only a first-order exponent and a coarse `O_eta(sqrt(n log n))` streaming excess, with no matching second-order lower bound, no constructive complexity theorem, and no separation between adaptive and fixed-order acquisition.
3. The priority analysis remains materially incomplete in the very geometry on which the finite threshold theorem rests. The checkpoint statement `K_n(eta)=n+1` is a cube-inside-simplex problem. Classical work on the absorption index of a cube by an inscribed simplex proves the universal factor `n`, gives the Hadamard equality case, and goes beyond Hadamard dimensions; in particular, exact factor `n` is known in dimensions 5 and 9. The manuscript's trace obstruction and the checkpoint half of its Hadamard theorem therefore require a theorem-level crosswalk with this literature, not merely a comparison with nonnegative rank.
4. A 2026 paper on classical random access codes gives a geometric worst-case characterization as an optimization over finitely many points in a cube. It predates the present September 2026 manuscript and is absent from the audit. I am not asserting that it contains the manuscript's exact-channel theorem, but it is plainly adjacent enough that omission prevents the claimed novelty boundary from being assessed.
5. The repository-wide pipeline is not advanced in the sense relevant to the advertised “Foundations” program. The manuscript itself correctly records that A2, B4, C2, the eleven-paper aggregate, arbitrary adaptive collision scheduling, and the historical analytic gates remain open. Preservation and build provenance are useful engineering records; they are not mathematical leverage on those gates.

A sharply repositioned paper could be of interest to a specialist venue in stochastic automata, information theory, convex geometry, or positive realization. That is a materially different editorial judgment from acceptance in one of the four general mathematics journals.

---

## 1. Scope of this review

I reviewed the focused article and the records needed to place it in the repository pipeline, including:

- `papers/GTF-I-v30-streaming-geometry/main.tex`;
- `introduction.tex`;
- `coherent-realization.tex`;
- `finite-streaming.tex`;
- `entropy-streaming.tex`;
- `approximation.tex`;
- `residual-comparison.tex`;
- `literature-and-scope.tex`;
- `references.tex`;
- `RESPONSE_TO_REFEREE.md`;
- `LITERATURE_AUDIT.md`;
- `HISTORY_AUDIT.md`;
- `RESOURCE_LEDGER.md`;
- `PROOF_STATUS.json`;
- `PIPELINE_STATUS.json`;
- the revision-30 build receipt and theorem-location metadata;
- the controlling revision-29 referee report;
- the retained revision-29 theorem chain to which the response refers;
- the repository-level `ROUND17_PROOF_DEPENDENCY_LEDGER.md`.

I also spot-checked external literature specifically around the two places where the revised article now places most of its novelty weight: cube/simplex containment and worst-case random-access-code geometry. This was a targeted check, not an assertion of exhaustive priority clearance.

The build records establish that a particular source tree produced the distributed files and that the predecessor volumes were retained. They do not independently certify any proof, priority claim, or editorial standard. I have therefore evaluated the mathematical text rather than treating the verification metadata as evidence of theorem correctness.

---

## 2. What revision 30 genuinely improves

### 2.1 The article now has a defensible mathematical spine

The journal-facing article is no longer a 69-page consolidation of heterogeneous developments. It has one identifiable sequence:

1. a lower support-component rank;
2. an equality criterion using enclosing simplices and compatible shifts;
3. a finite binary-query family;
4. exact fixed-signal asymptotics;
5. a uniform approximation theorem;
6. an explicit residual versus unrestricted-positive realization gap.

This is a major editorial improvement. The article can be read without reconstructing the entire repository history, and the old material is preserved in separate volumes rather than being silently deleted.

### 2.2 The residual-hull simplex condition is no longer presented as a characterization

Revision 29 had only a sufficient residual-vertex construction. Revision 30 correctly allows internal continuations outside the residual hull. At equality, each support component is enclosed by exactly its affine-rank number of positive generators, and those generators must obey common one-step shift equations. This resolves the previous report's objection that nonsimplicial residual hulls were excluded by the theorem rather than by the underlying model.

The reservoir family is a clean demonstration that a nonsimplicial residual hull can nevertheless attain the affine-rank lower profile with non-residual internal states.

### 2.3 The intermediate fixed-signal regime is no longer empty

For each fixed `0 < eta < 1`, the manuscript proves

```text
n I(eta) <= log_2 K_n(eta) <= n I(eta) + O_eta(log n),
n I(eta) <= log_2 W_n^ad(eta) <= log_2 W_n^fo(eta)
          <= n I(eta) + O_eta(sqrt(n log n)),
```

where `I(eta)=1-h_2((1+eta)/2)`.

This is a real advance over the two endpoint windows in revision 29. The upper proof is not merely a success-probability code: it constructs a finite set of decoder mean vectors whose convex hull contains the entire inner cube, so every prescribed conditional mean has an exact convex representation. The subsequent block conversion explicitly charges raw bits and retained block labels.

### 2.4 The finite constructions are explicit and correctly delimited

The `t+1`-state reservoir is elementary but elegant. Its state law and update rule can be checked directly, and the profile lower bound is correctly stated for the fixed acquisition order. The Hadamard update is also a genuine online stochastic process rather than a terminal factorization.

The manuscript is commendably careful about several boundaries:

- the Hadamard construction gives peak `n+1`, not the individual `t+1` profile at earlier cuts;
- one later query is not a joint product of all query answers;
- a persistent random seed is not free;
- program description length and running time are not counted;
- atomic exact stochastic rows are distinct from finite-bit implementations;
- the fixed-clock collision theorem is not promoted into an arbitrary adaptive scheduling theorem;
- the historical A2/B4/C2 obligations are not declared closed.

These qualifications should be preserved in any future version.

---

## 3. Technical audit of the main proofs

### 3.1 The support-component lower bound remains sound

If a residual continuation `R_h` is represented as

```text
R_h = sum_s E_h(s) B_s,
```

then every positively used continuation `B_s` belongs to the minimal face containing `R_h`. A state used for residuals in two different support components would lie in two intersecting minimal faces, contradicting the component separation. Within one component, a convex hull containing an affine set of dimension `r-1` needs at least `r` normalized generators. Summing gives the stated lower bound.

This argument applies to arbitrary stochastic continuations in the declared model, not merely to actual residual states. That remains the strongest conceptual observation in the realization part of the paper.

### 3.2 The coherent-enclosure equivalence is formally correct

At equality, the lower-bound proof leaves exactly `r_(t,j)` generators in component `j`. Their convex hull contains the residuals and their affine span must coincide with the component affine span. Actual machine transitions give the common nonnegative shift coefficients. Conversely, the listed vertices and coefficients define stochastic updates, and backward induction identifies their future laws with the declared continuations.

I do not see a hidden dependence on an unread report in the next-action row. The buffer convention is explicit, and zero-probability action rows can indeed be completed arbitrarily.

The algebraic decidability corollary is also plausible for a fully listed rational or real-algebraic array: the unknown vertices, convex coefficients, and shift weights satisfy a finite semialgebraic system, and generic real quantifier elimination decides nonemptiness. This says nothing useful about polynomial complexity in a succinct horizon, which the manuscript now acknowledges.

### 3.3 The reservoir and Hadamard online updates check out

For the reservoir, the vertices

```text
v_(t,0) = -eta 1,
v_(t,i) = -eta 1 + 2 t eta e_i
```

lie in the outer cube when `(2t-1)eta <= 1`. The state distribution that chooses each observed positive coordinate with probability `1/t` and aggregates all negative coordinates into label zero has mean exactly `eta x_(1:t)`. The replacement update produces that distribution inductively. At every fixed-order cut, the already read coordinates still induce a full `t`-dimensional cube of future query means, so `t+1` labels are necessary.

For the Hadamard construction, orthogonality makes

```text
q_(i,x_i)(s) = (1 + x_i v_(s,i))/m
```

a probability law with mean `x_i e_i`. The reservoir-style mixture over the acquired indices has mean `x/n`, and the final decoder is legal at `eta <= 1/n`. This proves an online upper bound with `m` labels.

The trace obstruction is also correct: nonnegative barycentric coordinates on the inner cube give `a_s >= eta ||b_s||_1`, while differentiating the barycentric identity and taking traces gives `n <= sum_s ||b_s||_1 <= 1/eta`.

### 3.4 The fixed-signal exponent proof is coherent

The cap lower bound follows from

```text
E exp(t X dot z) <= cosh(t)^n
```

and the Legendre transform of `log cosh`. Covering all input corners by generator caps then gives `K_n >= 2^(n I(eta))`.

For the upper bound, the conditioned Hamming layer has the stated mean, and the threshold probability is at least `delta`. Combining this with the binomial-layer mass, an `l^1` net, and the Lipschitz property of a support function gives a finite sign codebook whose hull contains the inner cube. Choosing `delta=1/n` gives the checkpoint logarithmic overhead.

The block construction then retains all completed block labels plus the active raw block. Under the paper's atomic-overwrite convention its count is bounded by

```text
2^ell M^floor(n/ell),
```

and the chosen block length yields the displayed `sqrt(n log n)` excess. This proof does what it claims.

### 3.5 The row-error theorem is correct but nearly immediate

Uniform binary total variation changes each conditional mean by at most `2 epsilon`. Thus the cap lower bound sees effective signal `(eta-2 epsilon)_+`. Exact synthesis of that attenuated channel gives the matching first-order upper rate. This is a useful corollary, but it is not an independent deep theorem once the exact fixed-signal result is available.

### 3.6 The probabilistic-residual separation is credible in the stated convention

After a supported length-`n` prefix, the residual languages form the `2^n` corners of an affine cube and are extreme. Nonnegativity forces any state language used at that phase to have the same remaining word-length support. Under the residual-automaton definition cited by the manuscript, such a state language must be an actual residual of the original stochastic language, hence one of those corners. This yields the exponential residual-state lower bound. The phase-tagged reservoir construction gives the stated polynomial unrestricted-positive upper bound.

A future version should nevertheless state the exact probabilistic-automaton and termination convention in a standalone definition rather than rely on prose and citations. Different papers normalize stochastic languages, final weights, and prefix termination differently. The result is strongest when the model translation is entirely internal to the article.

---

## 4. The central realization theorem is not yet a structural classification

The manuscript repeatedly calls Theorem `thm:coherence` a necessary-and-sufficient criterion. Formally that is true. Substantively, however, the witness is extremely close to the object whose existence is being tested.

A rank-saturating machine supplies:

- rank-many normalized state continuations in every component;
- convex coefficients expressing each residual in those continuations;
- a next-action distribution for every state;
- update probabilities after each report;
- compatibility of those updates with the next-cut continuations.

The “coherent rank enclosure” records exactly the same data as enclosing vertices and bilinear shift weights. The converse then reads those data back as a machine. Apart from the face lower bound and the observation that equality places the generators in the residual affine slice, little compression of the realization problem has occurred.

This is not merely a semantic objection. The paper does not provide the example that would demonstrate a genuinely new compatibility phenomenon: an array for which every cut separately admits a rank-sized positive enclosure but no simultaneous rank profile exists. The conclusion explicitly admits that no such example is supplied. Nor does it derive a graph-theoretic, topological, order-theoretic, or convex-geometric condition that can be checked without solving essentially the same global bilinear feasibility problem as the machine itself.

The CAD corollary does not change this assessment. Any finite existential real-algebraic feasibility formulation is decidable by Tarski-Seidenberg/CAD. That generic fact is not a classification theorem and gives no informative complexity bound.

For a top-four paper, one would expect at least one of the following:

1. a nontrivial invariant equivalent to compatibility but substantially smaller than the machine witness;
2. a genuine obstruction example separating static rank saturation from causal rank saturation;
3. a classification on a broad natural class not defined by possession of the desired compatible factors;
4. a sharp complexity theorem;
5. a connection that resolves a recognized open problem in positive realization.

Revision 30 supplies none of these. It gives a clean normal-form feasibility statement. That is useful, but the manuscript overestimates its structural depth.

---

## 5. The cube/simplex threshold has an omitted classical geometric lineage

This is the most serious priority defect in the revised paper.

By the manuscript's own cube-enclosure lemma, `K_n(eta)=n+1` means that there is an `n`-simplex

```text
S = conv{v_0,...,v_n} subset [-1,1]^n
```

that contains `[-eta,eta]^n`. At the critical value `eta=1/n`, this is exactly the centered inclusion

```text
S subset Q'_n subset n S,
Q'_n = [-1,1]^n.
```

This problem has a substantial classical literature under the absorption index of a cube by an inscribed simplex, axial diameters, interpolation projectors, and perfect simplices.

In particular, M. Nevskii and A. Ukhalov, *Five-dimensional Perfect Simplices*, arXiv:1709.06068 (2017), records the universal lower factor `n`, the Hadamard equality construction, and the fact that equality also occurs in dimensions `5` and `9`, where `n+1` is not a Hadamard order. Its Theorem 2 shows that equality in `S subset Q subset nS` forces the simplex and parallelotope centers to agree; its Theorem 3 gives the Hadamard case. The paper also points to older cube-simplex and maximal-determinant literature.

Consequences for the present manuscript are immediate.

- The trace lemma is an elementary rederivation of a classical cube/simplex lower factor in the centered setting, not an isolated new obstruction.
- The **checkpoint** part of the Hadamard theorem is classical geometry after translating decoder means into simplex vertices.
- The Hadamard construction is not the whole static equality story: dimensions `5` and `9` already show exact factor `n` beyond Hadamard orders.
- The genuinely potentially new part is the claim that a suitable critical simplex can be equipped with an online stochastic acquisition realization of the same peak. That online compatibility must be separated sharply from the classical static containment statement.

The current `LITERATURE_AUDIT.md` discusses nonnegative rank and nested polytopes but omits this direct cube/simplex literature. That omission is not cosmetic. It causes the article to present a known static geometric threshold as though its primary context were generated internally from the streaming model.

Before any specialist submission, the authors must add a theorem-level translation between `K_n(eta)=n+1` and the standard absorption-index notation, cite the classical lower bound and equality results, state what is already known for dimensions `5` and `9`, and identify exactly which online statements remain new.

---

## 6. The random-access-code priority boundary is still incomplete

The paper now credits Ambainis--Nayak--Ta-Shma--Vazirani for the first-order entropy exponent and logarithmic communication overhead. This is necessary and correctly done. It also means that the main asymptotic formula itself cannot carry the novelty burden.

There is a further omission. R. Kondo, Y. Sato, H. Yano, Y. Maeda, K. Ito and N. Yamamoto, *Random Access Codes: Explicit Constructions, Optimality, and Classical-Quantum Gaps*, arXiv:2604.21274v3 (submitted April 2026, revised July 2026), gives a geometric characterization of optimal classical random access codes under average and worst-case criteria. Its worst-case formulation is a minimax problem over finitely many points in `[0,1]^L` and it derives explicit optimal constructions for several parameter families.

I am **not** claiming, without a full theorem-by-theorem comparison, that this paper proves the exact conditional-channel enclosure theorem of revision 30. The objectives differ: a uniform lower bound on decoding success is not automatically equality of every conditional response probability. But the object, geometry, date, and optimization language are close enough that a September 2026 novelty audit cannot omit it.

The revised manuscript must answer at least the following questions.

1. Is its cube-enclosure number exactly one of the worst-case RAC geometric quantities after an affine change of coordinates, or a stricter equality-constrained variant?
2. Can an optimal worst-case RAC be symmetrized or attenuated to the exact-row channel without increasing message cardinality?
3. Which of the finite threshold statements follow from existing optimal RAC constructions?
4. Is the random sign-codebook enclosure new, or a reformulation of a known covering-code/RAC upper construction?
5. What part of the charged block streaming result is absent from existing streaming-space or online encoding literature?

Until this comparison is supplied, the priority boundary of the article's largest quantitative section is not established.

---

## 7. The streaming theorem is first-order and obtained by a coarse conversion

The theorem resolves the former empty fixed-signal interval only at exponential scale. This is worthwhile, but substantially weaker than the paper's rhetoric sometimes suggests.

### 7.1 No finite phase diagram is obtained

The result does not determine `K_n`, `W_n^ad`, or `W_n^fo` at any general finite pair `(n,eta)`. It does not determine the critical window when `eta` varies with `n`. It does not determine the exact simplex threshold in arbitrary dimensions. It does not even show that checkpoint and whole-streaming costs differ by more than a subexponential factor.

### 7.2 The streaming excess has no matching lower bound

The `O_eta(sqrt(n log n))` excess comes from choosing a block length that balances a raw block with repeated checkpoint overhead. This is a standard blocking device, not a sharp streaming theorem. There is no lower bound beyond the checkpoint exponent and no evidence that the displayed excess is intrinsic.

The adaptive quantity receives no independent upper construction: it is squeezed between the checkpoint lower bound and the fixed-order upper bound. Thus the equality of normalized exponents does not reveal whether adaptive acquisition helps at finite or second order.

### 7.3 The codebook is nonconstructive in the computational sense

The random argument proves existence of a finite sign set, after which the codebook is treated as part of an uncharged program. The article explicitly excludes program description length, construction time, transition-table access, and exact sampling workspace. Under that model the theorem is correct. It should not be confused with an implementable streaming algorithm using `n I(eta)+o(n)` bits and an efficiently describable update rule.

A stronger specialist-level paper could develop one of the missing quantitative directions. At four-journal level, the present first-order sandwich and elementary blocking conversion are not enough.

---

## 8. The resource model is legitimate but unusually permissive

The phrase “exact streaming memory” invites a stronger computational interpretation than the theorem supports. The actual resource is the logarithm of the number of labels in a finite stochastic transducer with:

- arbitrary exact atomic stochastic rows;
- a free externally declared clock;
- an uncharged, potentially enormous program and transition table;
- nonconstructively selected codebooks hard-wired into that program;
- one atomic external query;
- one response per installation;
- no charge for time or random-bit complexity of sampling a row.

The manuscript states these conventions, so this is not a correctness defect. It is a significance constraint. A finite-state realization theorem in this oracle-like model is not a conventional streaming-space algorithm. The top-level title and abstract should make the distinction impossible to miss.

In particular, the exactness claim is partly purchased by allowing exact real or algebraic transition probabilities as primitive operations. For rational rows, variable-length fair-bit sampling is possible in principle, but the resulting sampler has its own control states, counters, stopping time, and workspace. Those are deliberately outside the current count.

This modeling choice may be entirely appropriate for positive realization. It weakens the article's claim to broad streaming-complexity significance.

---

## 9. The probabilistic-residual gap is useful but not four-journal depth

The finite-language example performs a clear service: it prevents canonical minimality inside a residual-state class from being confused with minimization over arbitrary positive state languages. The exponential-versus-polynomial count is concrete, includes the clock and query buffer, and is more persuasive than a verbal warning.

Still, the mechanism is straightforward once the reservoir family is available. The supported length-`n` residuals are deliberately made into the extreme corners of a cube. A residual automaton must keep those actual residuals; an unrestricted positive automaton uses non-residual simplex states. The paper itself declines to claim that exponential succinctness gaps between probabilistic models are new.

For a specialist venue, this is a valuable example and a useful correction to the literature discussion. It does not transform the article into a four-journal contribution.

---

## 10. Pipeline assessment

Revision 30 is commendably honest about the repository-wide proof DAG. Its own status files say that the following remain unresolved:

- the historical A2 replacement;
- the B4 aggregate;
- the C2 aggregate;
- the eleven-paper aggregate;
- arbitrary adaptive collision optimization;
- all finite query counts;
- exhaustive original-source priority clearance.

The Round-Seventeen ledger still has independent Fourier/LLT, stopped-LDP, global-kernel, nonlinear-semigroup, graph-core, filtered-experiment, optional-projection, and typed-contraction gates. None is discharged by a finite one-query channel-synthesis theorem.

The local consumer corollary transports row total variation through one downstream decision and through fresh independent reinstallations. That is standard contraction and coupling. It is not an analytic bridge to A2, B4, C2, or D1.

Therefore the repository history contributes context but not additional mathematical weight to this submission. The title “General Theta Foundations I” remains disproportionate to what the focused paper actually proves. A more accurate title would identify positive realization and one-query random-access memory without implying that the larger foundations program has been closed or reorganized around these results.

---

## 11. Required changes before a credible specialist submission

The following are not a recipe for making the paper suitable for a top-four journal. They are the minimum changes needed for a fair specialist evaluation.

### 11.1 Repair the priority analysis

Add a dedicated cube/simplex subsection translating the checkpoint problem into absorption-index language. Cite the classical universal factor, Hadamard equality, perfect simplices, dimensions `5` and `9`, axial-diameter formulas, and the relevant maximal-determinant literature. Split every static checkpoint statement from the online compatibility statement.

Add a theorem-level comparison with the 2026 Kondo--Sato--Yano--Maeda--Ito--Yamamoto random-access-code paper and any other recent worst-case RAC geometry work. Do not merely add the citation; identify equivalent, stronger, weaker, and incomparable statements.

### 11.2 Reduce the novelty claims around the entropy exponent

The exponent and logarithmic communication overhead are classical. The paper's possible contribution is exact conditional equality plus full-schedule label counting. State that distinction theorem by theorem and test whether exactification follows from existing symmetric RAC constructions.

### 11.3 Produce a genuinely structural compatibility result

At minimum, give an explicit finite causal array for which every cut separately admits a rank-sized positive enclosure but no simultaneous rank-sized realization exists. Better would be a broad criterion that detects compatibility without parameterizing the entire desired machine. Without such a result, the coherence theorem remains a useful normal form rather than a classification.

### 11.4 Strengthen the streaming side

A substantial advance could take one of several forms:

- a matching second-order law;
- a nontrivial lower bound on `W_n-K_n`;
- a finite separation between adaptive and fixed-order acquisition;
- an efficiently constructible exact codebook;
- a sharp varying-signal phase diagram;
- online realizations for the non-Hadamard perfect simplices;
- an exact threshold in a broad new sequence of dimensions.

At present none is supplied.

### 11.5 Internalize all automaton conventions

Define the stochastic-language automaton, residual automaton, initial/final weights, termination, and state-language normalization in the article. Then state the separation theorem entirely in that language before comparing it with external papers.

### 11.6 Reposition the article

Remove or sharply qualify the “Foundations” branding. The focused 15-page structure is a good decision; the next step is to present the paper as a local contribution in positive realization, random-access coding, and finite stochastic automata rather than as closure of a repository-wide mathematical program.

---

## 12. Minor and editorial points

1. The phrase “necessary and sufficient condition” should always be followed by “for simultaneous attainment of the support-component affine-rank lower profile,” not allowed to sound like a solution of unrestricted positive realization.
2. The use of `rank` in the static proposition, support-component affine rank, nonnegative rank, restricted nonnegative rank, and queried block-normalized generator number is now much clearer, but a single comparison diagram would still help.
3. The checkpoint and streaming models should be separated typographically at every finite theorem. A reader can otherwise mistake a static simplex result for an online one.
4. The Hadamard theorem should state in its title that only the online upper construction is specifically Hadamard-based; the static critical inclusion belongs to a wider perfect-simplex problem.
5. The approximation result should be labeled as a corollary of the exact theorem unless the authors add a genuinely new approximation phenomenon.
6. The phrase “exact streaming” should be paired with “atomic stochastic-row model” in the abstract.
7. The proof of the PRFA separation should state whether unreachable states are removed and whether subprobability state languages are permitted before normalization.
8. The literature audit should record search dates and version numbers for all 2026 preprints, as it already does for several older sources.
9. The manuscript should not cite the repository's own revision 29 as though it were an external publication. It is useful provenance, but not peer-reviewed prior literature.
10. The preserved 375-page and 928-page volumes should not be part of the journal submission package unless an editor explicitly requests them. They obscure rather than strengthen the focused article.

---

## 13. Final assessment

Revision 30 answers the previous report more effectively than I expected. It contains real mathematics, its principal local proofs appear coherent in the stated model, and the focused article is potentially publishable after a serious priority rewrite. The author has also shown welcome restraint by explicitly preserving unresolved pipeline gates instead of declaring them solved.

Nevertheless, the four-journal question is not close.

- The realization equivalence largely repackages the desired machine as an enclosing-and-shifting witness.
- The principal asymptotic exponent is classical.
- The streaming upper bound is a coarse blocking consequence with no matching lower order.
- The finite simplex threshold omits a direct classical geometric literature that already contains the universal factor, the Hadamard case, and non-Hadamard equality dimensions.
- A recent geometric RAC paper is absent from the novelty audit.
- The one-query atomic-row model is substantially narrower than ordinary streaming computation.
- No major gate in the repository's advertised foundations pipeline is closed.

**Recommendation: reject at the Annals / Inventiones / JAMS / Acta level.**  
**Specialist-venue outlook: potentially positive after major priority correction, claim reduction, and preferably one genuinely new structural or sharp quantitative theorem.**

This recommendation is made with high confidence on venue and originality, and moderate-to-high confidence on the local proof audit. It is not an allegation that the principal revision-30 statements are false.