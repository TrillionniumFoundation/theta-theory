# Referee Report — General Theta Foundations I, Revision 49

**Manuscript:** *General Theta Foundations I: Sign and Magnitude Duality for Numerical Word Realizations*  
**Repository:** `TrillionniumFoundation/theta-theory`  
**Reviewed branches:**
- `revision/general-theta-foundations-i-v49-robust-duality-2026-09-27`
- `revision/general-theta-foundations-i-v49-referee-ready-2026-09-27`

**Reviewed publication head:** `0a33f027a9088c4a55542efcd2784de95f43f557`  
**Validated native-source commit:** `23ef77d5adc9d6e6a257a6072dc95cc9264dedef`  
**Completed source ancestor:** v47 publication `98b59f3f45f63dacd8dba8cf132d23e54e7596e8`  
**Controlling prior report:** r30, `6ecf57a2d7ce804352f85daead8ec38e56377631`  
**Review branch:** `review/general-theta-foundations-i-v49-sign-magnitude-duality-harsh-top4-r31-2026-09-27`  
**Date:** 27 September 2026

## Recommendation

**Reject at the Annals / Inventiones / JAMS / Acta level.**

This is nevertheless the strongest and most mathematically coherent revision in the recent sequence. Unlike Revision 46, Revision 49 contains a genuine class-wide structural theorem rather than only candidate-verification identities or generic compactness statements. I did not find a fatal counterexample to the new support reduction, sign-chamber formulation, logarithmic feasibility system, Farkas-type multiplicative alternative, algebraic-threshold argument, cubic optimum, rational/nonrational attainment separation, or rational orthogonal example.

The negative top-four recommendation is therefore **not** based on a claim that the principal theorem is false or empty. It is based on scope, conceptual reach, and novelty relative to the methods used.

The new core classifies one sharply delimited model:

- finite, explicitly listed response tensors;
- antisymmetry under paired positive/negative seeds;
- a binary selected query;
- exactly two available stochastic labels at every command cut; and
- a nonuniform atomic-row model with free horizon-dependent real tables and exact sampling.

Within that class, the scalar normal form turns the realization problem into bounded rank-one tensor approximation. The subsequent support deletion, sign enumeration, logarithmic monomial substitution, linear feasibility, Farkas alternative, extreme-ray sparsity, and univariate root isolation are classical tools assembled correctly. The stochastic reconstruction and exact positive-error examples are useful. The resulting theorem is a serious specialist contribution if its priority survives a full literature audit. It is not, in its present form, a sufficiently broad or conceptually transformative theorem for the four leading general mathematics journals.

**Disposition outside the four leading general journals:** major revision, substantial compression, and submission as a focused specialist paper. The two-state duality, exact examples, and dynamic bottleneck results could form a publishable article. The inherited arithmetic-width program should be separated rather than appended in full.

---

## 1. Scope, branch genealogy, and materials reviewed

At the final branch survey used for this report, Revision 49 was the latest referee-ready `General Theta Foundations I` revision. The work and referee-ready branches pointed to the same publication head `0a33f027...`. No Revision 50 branch and no pre-existing Revision 49 review branch were present.

I reviewed the complete readable Revision 49 source package, with particular attention to:

- `papers/GTF-I-v49-robust-duality/main.tex`;
- `introduction.tex`;
- `machine-model.tex`;
- `two-state-compatibility.tex`;
- `magnitude-duality.tex`;
- `exact-error-examples.tex`;
- `encoding-and-comparison.tex`;
- `inherited-statements.tex`;
- `hankel-compatibility.tex`;
- `finite-horizon-certificates.tex`;
- `word-profiles.tex`;
- `distortion-rate.tex`;
- `arithmetic-scales.tex`;
- `metric-width.tex`;
- `irrational-fluctuations.tex`;
- `finite-bit-memory.tex`;
- `comparison.tex`;
- `references.tex`;
- `RESPONSE_TO_REFEREE.md`;
- `README.md`;
- `RESOURCE_LEDGER.md`;
- `PROOF_STATUS.json`;
- `PIPELINE_STATUS.json`;
- `HISTORY_AUDIT.md`;
- `LITERATURE_AUDIT.md`;
- `dual_certificate.py`;
- `check_duality.py`;
- the v49 workflow, build receipt, isolated-core receipt, exact-check records, and cubic certificate;
- the complete r30 referee report;
- the completed v47 manuscript and its new two-state section;
- and the repository-level Round-Seventeen proof-dependency ledger.

I also made targeted primary-source comparisons with Gillis–Shitov on rank-one infinity-norm approximation, Morozov–Smirnov–Zamarashkin on rank-one Chebyshev approximation, Boyd et al. on geometric programming, and Kahle–Kubjas–Kummer–Rosen on rank-one tensor completion and Segre/toric circuit structure. This was not an exhaustive independent priority search.

The genealogy is cleanly recorded. Revision 49 starts from the completed v47 publication, identifies r30 separately as the controlling report, and does not pretend that r30 is an ancestor of v47. The earlier v48 transport-only branch is neither overwritten nor treated as verified mathematics. The publication head is one commit beyond the validated source commit and adds generated artifacts and the root review-ready entry rather than silently changing theorem source.

---

## 2. Executive assessment of what Revision 49 accomplishes

Revision 49 materially answers the main mathematical demand of r30.

The earlier report asked for a structural certificate excluding an entire realization class, rather than another test of a supplied candidate. Revision 49 now provides such a certificate for the complete all-two-state antisymmetric class.

The new contribution has four substantive parts.

### 2.1 Complete feasibility at a fixed error threshold

The inherited v47 normal form says that the odd response of any two-label realization is a bounded decomposable tensor

```text
seed factor × epoch-1 command factor × ... × epoch-N command factor × query factor.
```

Revision 49 handles arbitrary zeros, inactive entries, inconsistent signs, and magnitude incompatibility. At a proposed mean tolerance `delta`, the active entries determine the factor coordinates that must remain nonzero. Fixed factor signs then reduce every surviving absolute-error interval to linear inequalities in the negative logarithms of factor magnitudes.

This is a complete decision alternative for the stated class, not merely a sufficient relaxation.

### 2.2 Global multiplicative infeasibility certificates

For one sign chamber the logarithmic system has the form

```text
C y <= log b.
```

Infeasibility is equivalent to a nonnegative integer vector `z` satisfying

```text
z^T C = 0,
product_i b_i^(z_i) < 1.
```

An extreme-ray argument gives support on at most one more inequality than the number of essential factor coordinates. To reject the complete two-state class, one supplies either a sign contradiction, an impossible surviving endpoint, or such a magnitude certificate for every compatible chamber.

This is the right global quantifier. It rules out all legal two-state machines in the class, not merely a proposed transition table.

### 2.3 Exact algebraic optimization

Between target absolute-value breakpoints, the active support, chamber equations, incidence matrix, and certificate cone are fixed. Certificate products are monotone algebraic functions of the scalar threshold. Enumerating rational extreme rays and isolating roots therefore gives a finite exact optimization algorithm for an explicitly listed algebraic tensor.

The proof also reconstructs algebraic factor magnitudes from vertices of the logarithmic polytope and compiles them into legal stochastic rows.

### 2.4 Nontrivial exact examples

The 2-by-2-by-2 rational table has a genuine positive optimum determined by a cubic. A five-entry monomial circuit proves the lower bound, while explicit algebraic rows attain it. Because the optimum is irrational, no rational machine of that fixed profile attains it.

The second example uses actual rational orthogonal commands at every positive horizon and has exact error `rho/20` in the all-two-label profile and between two separated two-label bottlenecks.

These examples are more informative than the zero-command calibration in v46 and answer the request for a dynamic exact frontier.

---

## 3. Detailed correctness audit

### 3.1 The inherited two-state scalar normal form

I continue to regard the v47 scalar normal form as correct.

A two-state distribution has a signed coordinate `r=2p-1`. A stochastic two-by-two row maps it affinely,

```text
r -> alpha + beta r,
```

with `|alpha|+|beta|<=1`. A bounded decoder is likewise affine. Taking the odd part under the paired-seed involution eliminates every offset and leaves a product of the initial odd coordinate, transition slopes, and terminal odd decoder coefficient.

The recentered construction using slope-only rows realizes that odd tensor without a free persistent symmetrization bit. Thus the optimum over legal two-label stochastic machines really is the bounded decomposable-tensor Chebyshev optimum stated in v47.

This normal form is specific to two states. It should not be rhetorically generalized to higher positive realizations.

### 3.2 Threshold support reduction

Lemma `support49` is correct and necessary.

If `|f_e|>delta`, every feasible approximating product at entry `e` is nonzero and has magnitude at least `|f_e|-delta`. Since every factor magnitude is at most one, each incident factor has at least that magnitude. Taking the maximum over active incident entries gives the declared lower bound `a_v`.

Setting every nonessential factor to zero cannot damage an active entry, because every coordinate of an active entry is essential by definition. Every changed entry is inactive and is then approximated by zero within the nonstrict threshold. This also correctly handles equality `|f_e|=delta`.

This is the point at which an informal “assume positive factors” argument would have failed. The manuscript handles it correctly.

### 3.3 Sign chambers and the logarithmic system

For a fixed chamber, the formulation is exact.

Write the product sign at entry `e` as `sigma_e`. The residual constraint

```text
|f_e - sigma_e p_e| <= delta,  p_e>0
```

is equivalent to

```text
max(0, sigma_e f_e-delta) <= p_e <= sigma_e f_e+delta.
```

A nonpositive upper endpoint is impossible. Otherwise, with `p_e=exp(-b_e.y)`, the upper and positive lower bounds become precisely the displayed linear inequalities in `y`.

The factor caps and the support-induced lower factor bounds are also represented correctly. Upper endpoints above one are harmless because `y>=0` already forces every product magnitude to be at most one.

Inactive entries containing a deleted factor are satisfied by zero. Inactive entries whose coordinates all survive remain in the system and are not silently discarded. This is an important correctness point and is handled properly.

### 3.4 Farkas alternative and sparse multiplicative certificates

For a finite system `Cy<=log b`, the stated alternative is standard and correctly applied:

```text
infeasible
iff exists z>=0 with z^T C=0 and z.log b<0.
```

Normalizing a nonzero dual vector by its coordinate sum produces a compact rational polytope. An extreme point has support at most `rank(C)+1`, hence at most `|V_delta|+1`. Since the equality matrix is integral, the extreme point is rational; clearing denominators yields an integer multiplier vector. Exponentiation converts the strict logarithmic inequality into a rational/algebraic product inequality.

No strict-feasibility assumption is used. The argument remains valid at boundary optima.

The certificate is sparse **within one chamber**. A global rejection may require certificates for exponentially many distinct chambers. The paper generally states this correctly, but every summary of the result should retain that qualification.

### 3.5 Completeness across sign chambers

The global theorem has the correct quantifier structure.

Active target signs impose a linear system over `F_2`. If it is inconsistent, a balanced parity certificate rejects all products. If it is consistent, every compatible factor-sign assignment is considered, with gauge-equivalent assignments deduplicated by their induced surviving entry-sign pattern. A feasible chamber reconstructs a bounded product and hence a legal stochastic machine. If every chamber is rejected, no all-two-state machine exists at that tolerance.

Crucially, the paper does not convexify the union of chambers or mix whole machines without charging a retained selector. That would change the state resource. The manuscript explicitly avoids this error.

### 3.6 Exact algebraic optimization

Theorem `algebraic49` is plausible and, in the stated explicit-table model, correct.

On an open interval between consecutive values in `{0} union {|f_e|}`:

- the active and surviving supports are constant;
- the sign equations are constant;
- the integer matrix `C` is constant;
- every right-hand-side base is one, a positive affine algebraic function of `delta`, or the reciprocal of one; and
- the dual cone has finitely many rational extreme rays.

Feasibility is equivalent to the nonnegativity of finitely many products. Clearing fixed positive denominators gives finitely many univariate polynomial inequalities with algebraic coefficients. Root isolation and endpoint testing therefore determine the smallest feasible threshold.

At an optimal threshold, a nonempty bounded logarithmic polytope has a vertex. Its coordinates are rational linear combinations of logarithms of positive algebraic numbers. Exponentiating gives products of positive rational powers of algebraic numbers, hence algebraic numbers. The positive real branches are the intended ones. These factors compile to an algebraic stochastic machine.

The result is finite and exact. It is not polynomial in a succinct horizon, and the software does not implement the complete symbolic optimizer. The article states both limitations.

### 3.7 Sparse tightness at a positive optimum

Proposition `tight49` is sound under its hypotheses.

Inside the one full-support sign chamber, every extreme-ray product is nondecreasing with the error threshold: upper endpoints increase, reciprocals of decreasing lower endpoints increase, and cap reciprocals increase. If every nonconstant certificate product were strictly above one at the optimum, continuity would allow a smaller threshold. Thus some nonconstant sparse certificate is tight.

Complementary slackness follows directly because the nonnegative dual-weighted sum of primal slacks is zero. Every positively weighted inequality is tight.

The final phrase about the feasible threshold interval should be read as the intersection over all relevant extreme-ray tests in that fixed stratum, together with the chamber endpoint conditions. It would be helpful to say this explicitly.

### 3.8 The cubic exact optimum

The cubic example is correct.

For a nonnegative target, taking absolute values of all factors cannot increase entrywise error. Every decomposable 2-by-2-by-2 tensor obeys

```text
g_011 g_101 g_110 = g_000 g_111^2.
```

At mean error `delta`, the three weight-two entries on the left are at least `4/5-delta`, while the weight-zero and weight-three entries on the right are at most `1/10+delta` and `2/5+delta`. This gives

```text
(4/5-delta)^3 <= (1/10+delta)(2/5+delta)^2.
```

The difference is the displayed cubic divided by 250. Its derivative has negative discriminant and positive leading coefficient, so the cubic is strictly increasing and has one real root. The rational brackets are consistent with the root.

For the upper bound, the symmetric factors `(A^(1/3),B^(1/3))` produce entries by Hamming weight. The cubic identity gives the exact weight-two value, while the weight-one value lies strictly within the permitted error. Every factor lies in `(0,1)`, so the stochastic compiler is legal.

Scaling one mode by `rho` gives the general signal case. The lower circuit scales homogeneously, so the optimum is `rho t/2` in binary total variation.

### 3.9 Irrational optimum and rational nonattainment

The field-separation statement is correct in its declared sense.

The cubic is irreducible modulo seven and hence irreducible over the rationals. For positive rational `rho`, the optimal error is irrational. A machine whose initialization, transition, and decoder entries are all rational has rational responses at this finite horizon. Its finite maximum absolute error against a rational target is rational. Such a machine therefore cannot attain the irrational optimum.

This does not say that rational machines have a positive gap above the optimum. The dyadic-grid argument correctly gives rational machines below every strictly larger tolerance. The manuscript makes that distinction.

### 3.10 The rational orthogonal example

The orthogonal example is also correct.

Restricting the experiment between two two-label cuts to an identity block and a block containing one coordinate swap gives the positive-seed matrix

```text
rho * [[4/5,3/5],[3/5,4/5]].
```

A decomposable approximant obeys the determinant identity. At mean tolerance below `3rho/5`, it forces `delta>=rho/10`, hence binary-TV error at least `rho/20`.

Retaining only the sign of the seed and answering both coordinates with mean `±7rho/10` attains that value for every word, because every target coordinate is `±3rho/5` or `±4rho/5`. A one-label bottleneck erases the seed sign and forces the larger error `2rho/5`.

This is a valid arbitrary-horizon magnitude obstruction. It is still fundamentally a two-by-two matrix-minor obstruction embedded in the controlled experiment; it is not a broad higher-order orthogonal classification.

### 3.11 NP-completeness boundary

The one-epoch, one-query, variable-seed/command-alphabet NP-completeness statement is a valid transfer of the Gillis–Shitov rank-one infinity-norm decision problem.

The normalization by `B=max(1,||M||_infty+k)` ensures the approximating rank-one matrix can be rescaled into two factors bounded by one. The binary-TV tolerance includes the necessary factor of two relative to mean error. Conversely, bounded stochastic factors yield the original rank-one approximation after rescaling.

Membership in NP follows from threshold support deletion, a guessed sign pattern, and a rational linear system with a polynomial-bit basic feasible solution. The single query factor can be absorbed into one matrix factor.

This corollary is not a new hardness theorem for a fixed-dimensional orthogonal alphabet, for multiple epochs, or for succinct word input. The manuscript states that boundary clearly.

### 3.12 Software and evidence

The executable checker is reasonably fail-closed in the inspected paths.

It uses exact rational products rather than floating logarithms, binds conclusions to the complete input table, verifies coverage of all induced sign chambers, reconstructs coefficient rows before accepting a dual certificate, and reports resource exhaustion as `undetermined` rather than `infeasible`. The negative controls test zero multipliers, altered bases, missing chambers, invalid factor magnitudes, duplicated sign cycles, malformed targets, incomplete tables, and resource limits.

The checker implements rational threshold decisions, rational bisection, and the worked cubic bracket. It does **not** implement the full symbolic algebraic optimizer of Theorem `algebraic49`. The paper and status files say so.

I was unable to perform a second network clone in the isolated local execution environment used for this review; the independent mathematical assessment above is based on source inspection and direct symbolic checking of the key identities, not on relabelling the repository's own CI as an external run. This limitation does not affect the logical audit of the displayed proofs.

---

## 4. Novelty and the missing tensor/toric comparison

The literature positioning is much better than in v46.

The manuscript now explicitly credits:

- Gillis–Shitov for threshold-inactive deletion, fixed-sign matrix feasibility, and matrix NP-completeness;
- Boyd et al. for monomial logarithms and geometric-programming transformations;
- Farkas' lemma and sparse extreme-point geometry;
- Morozov–Smirnov–Zamarashkin for global rank-one Chebyshev approximation; and
- standard real-algebraic root isolation.

That is necessary and welcome.

However, the comparison remains incomplete in a direction central to the new theorem: **rank-one tensor completion and toric circuit geometry**.

Kahle, Kubjas, Kummer, and Rosen, *The Geometry of Rank-One Tensor Completion* (arXiv:1605.01678), formulate rank-one tensors as the Segre variety, identify the associated `0/1` incidence matrix and toric ideal, analyze zeros and real sign obstructions, and use circuit/binomial relations. Their opening 2-by-2-by-2 example already states that real rank-one completability of four specified entries depends only on the signs and holds exactly when an even number are negative.

That paper does not solve Revision 49's bounded full-tensor absolute-error problem, and it does not provide the stochastic reconstruction. Nevertheless, it is an unavoidable structural antecedent for:

- the incidence vectors `b_e`;
- balanced parity obstructions;
- monomial cancellation identities;
- sparse multiplicative circuits such as the five-entry cubic identity;
- zero-support combinatorics; and
- the language of complete rank-one tensor feasibility.

The current paper should add a direct comparison with Segre toric ideals, circuit ideals, real sign completion, and zero consistency. Without that comparison, the novelty claim for the “complete sign and magnitude alternative” is not yet adequately situated.

The likely genuinely new part is not the existence of monomial circuits or logarithmic linearization. It is the exact combination of:

1. the stochastic two-state odd-part normal form;
2. threshold-dependent support deletion for the bounded complete tensor;
3. a chamber-complete absolute-error alternative;
4. sparse data-bound rejection certificates;
5. stochastic reconstruction; and
6. exact positive-error examples in the controlled interface.

That contribution can be significant in a specialist setting. It must be stated at precisely this level.

---

## 5. Why the result is still below the four-journal threshold

### 5.1 The complete classification is for the smallest nontrivial width only

The duality depends on a one-dimensional odd coordinate. At width three or higher, stochastic maps act on higher-dimensional simplices, products are replaced by compatible positive factorizations, and the logarithmic rank-one reduction disappears.

Revision 49 does not classify:

- three-state profiles;
- profiles with varying widths above two;
- general compatible positive Hankel order;
- all finite orthogonal frontiers;
- general noncommuting alphabets; or
- minimal width as a function of the response table.

The theorem is complete inside its class, but the class is narrow.

### 5.2 The input is the fully expanded finite tensor

The global alternative receives every response entry. Its size is exponential in the horizon if the word experiment is given succinctly by command matrices. Sign-chamber and extreme-ray enumeration can also be exponential, and the boundary polynomials can have high degree.

Thus the theorem gives exact finite decidability and certificates for a listed tensor. It does not give an efficient structural algorithm for the succinct controlled process that motivates much of the manuscript.

### 5.3 The principal mechanisms are classical

Once the scalar normal form is available, the rest of the general theorem is built from:

- support deletion;
- finite sign enumeration;
- taking logarithms of monomials;
- linear feasibility;
- Farkas duality;
- extreme rays; and
- univariate root isolation.

The assembly is correct and useful, but it is not a new duality principle of comparable generality to the major theories cited in the paper.

### 5.4 The exact examples are elegant but small

The cubic example is a well-designed 2-by-2-by-2 table. It is not an orthogonal orbit and its lower certificate is a single Segre/toric monomial circuit. The orthogonal example is dynamic and arbitrary-horizon, but its lower bound reduces to the determinant identity for a two-by-two matrix.

Neither example demonstrates a broad new phenomenon in higher positive realization or asymptotic word dynamics.

### 5.5 The new duality remains disconnected from the inherited profile theory

The inherited manuscript develops distortion profiles, enclosure profiles, an interval budget, a one-sided distortion–dilation comparison, Diophantine exponents, Liouville fluctuations, and a finite-bit compiler.

Revision 49 does not prove a theorem linking its complete two-state dual certificates to:

- equality or sharpness in the distortion–dilation comparison;
- the optimized word-distortion profile;
- a broad arithmetic-width classification;
- a higher-width positive-Hankel duality; or
- a new noncommutative asymptotic result.

The new theorem and the inherited asymptotic program share an interface, but they do not yet form one conceptual result.

### 5.6 The resource model remains highly permissive

The primary invariant still allows:

- redesign for every horizon;
- free knowledge of the horizon and epoch;
- free real-valued row tables;
- free construction and lookup of those tables;
- exact real arithmetic;
- atomic exact sampling of algebraic or arbitrary prescribed real rows; and
- only one selected terminal query.

All enduring information must fit in the charged label, so the lower bounds are meaningful. But this is not ordinary program size, uniform workspace, finite-random-bit implementation, or anytime memory.

The separate finite-bit theorem addresses a different and much more specific model. It does not price the general algebraic optimizer or exact algebraic rows in Revision 49.

### 5.7 The paper remains accretive rather than focused

The 38-page current article includes:

- the new sign/magnitude theorem;
- the v47 two-state compatibility frontier;
- positive Hankel normal forms;
- Gram and moment certificates;
- rational grids;
- distortion/enclosure profiles;
- arithmetic exponents;
- Liouville fluctuations;
- a finite-bit compiler; and
- several complexity boundaries.

This is a repository-history compendium, not a paper organized around one decisive theorem. The strongest new result is obscured by inherited material with different methods, inputs, and audiences.

A four-journal paper needs either a broad unifying theorem or a much more consequential application. Revision 49 has neither.

---

## 6. Relation to r30

Revision 49 responds seriously to r30.

It addresses the following requests:

- **A structural infeasibility certificate:** supplied by `thm:duality49`.
- **A genuinely dynamic nonzero-horizon optimum:** supplied by the cubic and orthogonal examples, together with inherited v47 frontiers.
- **Precise encoding:** substantially improved in `encoding-and-comparison.tex` and the rational-height lemma.
- **Corrected exactness language:** the dyadic statement now concerns existence below every larger tolerance, not exact attainment of every larger error.
- **A reproducible exact-head workflow:** the earlier self-publishing race is replaced by separated source, validation, and publication jobs.
- **Direct approximation literature:** Gillis–Shitov, geometric programming, and Chebyshev approximation are now discussed.

These are real advances. The current rejection should not be read as a repetition of r30.

What remains from r30 is the broader issue: the manuscript still lacks a structural theorem for general positive realization, and it still combines multiple specialist papers under the “General Theta Foundations I” series title.

---

## 7. Relation to the repository-wide paper pipeline

The Round-Seventeen dependency ledger contains the independent chains

```text
A2 -> A3 -> A4 -> C2 -> D1
```

and

```text
B2-GC -> B1 -> B2-MC -> B3 -> B4 -> C1 -> C2 -> D1.
```

Those gates require, among other things:

- a returned-UNI Fourier theorem and raw density local limit theorem;
- stopped entropy/LDP arguments;
- a single global past kernel and unsmoothed renewal analysis;
- canonical coefficient and shell conditioning estimates;
- process CLT/Mosco limits;
- Nisio resolvents, graph cores, and nonlinear Trotter–Kato;
- model-derived filtering and QMD/LAN;
- strict/form response and changing-filtration optional projection; and
- labelled posterior contraction.

The Revision 49 finite two-state tensor duality does not discharge any of those gates.

The manuscript's own pipeline status correctly records:

```text
historical_A2_replaced = false
B4_aggregate_closed = false
C2_aggregate_closed = false
eleven_paper_aggregate_closed = false
all_higher_width_duality = false
all_finite_orthogonal_frontiers = false
independent_priority_certification = false
```

The new local dependency edge is legitimate:

```text
v47 scalar odd reduction
  -> sign/magnitude alternative
  -> algebraic optimum and exact examples.
```

It is not a closure of the larger analytic program.

Accordingly, repository accumulation, preserved volumes, and successful builds must not be used as evidence that the “Foundations” pipeline is complete or that the paper has four-journal significance. This report assigns no such credit.

---

## 8. Reproducibility and publication status

The release engineering is substantially improved and, as far as I could verify remotely, successful.

Workflow `36286323886` completed successfully at exact source SHA `23ef77d5...`. It separated three jobs:

1. **native-source:** restored and published the readable source once;
2. **validate:** checked out the exact native commit, installed fixed dependencies, ran the inherited and new exact checks, compiled the article and archives, and rebuilt the standalone core in isolation; and
3. **publish:** downloaded the validated artifacts, checked source binding and branch freshness, and made a non-force atomic publication push.

The final publication commit `0a33f027...` is one commit beyond the validated source and adds the generated article, receipts, source archives, images, cumulative volumes, and review-ready root entry. The core rebuild reports page-by-page text and raster equality for the 38-page article.

The build receipt records ordinary/optimized agreement, no undefined references, no overfull boxes, sixteen new negative-control executions, inherited v44/v47 checks, rational tensor threshold checks, the cubic bracket, noncommuting Gram checks, and orthogonal-word checks.

This is good repository practice and fixes the v46 publication race identified in r30.

It remains true that:

- successful tests do not prove the universal analytic theorem;
- page equality does not establish mathematical correctness;
- finite random tests do not establish completeness of the general algorithm; and
- source-bound CI does not establish priority or journal significance.

The manuscript and receipts now state these limitations accurately.

---

## 9. Required revision before specialist submission

### 9.1 Split the paper

The most urgent editorial action is to stop carrying the entire historical manuscript forward.

A focused paper should contain:

1. the two-state stochastic odd normal form;
2. sign and support structure;
3. the complete logarithmic/Farkas alternative;
4. exact algebraic optimization;
5. the v47 dynamic frontier;
6. the cubic and rational orthogonal examples;
7. the NP-completeness boundary; and
8. a concise comparison with rank-one approximation, tensor completion, and positive realization.

The arithmetic-width, Liouville, distortion/enclosure, and finite-bit compiler results should be a separate paper.

### 9.2 Add the tensor-completion and toric-circuit literature

At minimum, compare directly with Kahle–Kubjas–Kummer–Rosen, *The Geometry of Rank-One Tensor Completion*, arXiv:1605.01678, and the surrounding Segre/toric literature.

The paper should identify:

- its incidence matrix as the Segre exponent matrix;
- balanced identities as lattice/circuit relations;
- sign inconsistency as a real rank-one completion obstruction;
- zeros as support/slice consistency phenomena; and
- the exact addition made by bounded absolute-error intervals and stochastic compilation.

This comparison may materially change the novelty assessment and is required before publication.

### 9.3 State one precise novelty theorem

The introduction should include a theorem-by-theorem table:

```text
current claim
closest prior theorem
what is identical
what is added
why the addition is nontrivial
```

Do not use “complete duality” without immediately appending “for explicitly listed antisymmetric all-two-state tables.”

### 9.4 Either extend beyond two states or reduce the ambition

A major conceptual advance would require at least one of:

- a complete width-three case;
- a nontrivial higher-width dual object;
- a tractable class of compatible positive Hankel polytopes;
- a theorem connecting the finite dual certificates to distortion/enclosure sharpness;
- a broad orthogonal or noncommutative frontier; or
- meaningful complexity results for a succinct controlled input.

Absent such an extension, the paper should be presented as a complete solution of a sharply delimited two-state problem, not as a general foundation.

### 9.5 Strengthen the orthogonal application

The rational orthogonal example is valid but reduces to a two-by-two determinant. Add an orthogonal controlled example whose optimality genuinely uses a higher-order multi-epoch certificate rather than a matrix flattening or one-command minor.

This would demonstrate that the new tensor alternative contributes more than the existing matrix Chebyshev theory.

### 9.6 Clarify output and certificate complexity

For the explicit-table algorithm, state bounds or honest worst-case descriptions for:

- the number of sign chambers;
- the number and bit size of extreme rays;
- the degree and coefficient height of threshold polynomials;
- the size of a global infeasibility certificate covering every chamber;
- the representation size of an algebraic minimizing machine; and
- the cost of verifying such an algebraic witness.

The present theorem is finite but its output can be enormous. That should be part of the formal result, not only a resource-ledger warning.

### 9.7 Separate theorem proof from software scope

Keep the explicit distinction:

- analytic full algebraic optimizer: proved, not implemented;
- rational threshold checker: implemented;
- rational bisection: implemented;
- cubic algebraic certificate: implemented specifically;
- generic higher-width optimizer: neither proved nor implemented.

The current status files are mostly accurate; the article itself should make this distinction equally prominent.

### 9.8 Reframe the title and pipeline status

A suitable specialist title would be something like:

> *Exact Chebyshev Duality for Two-State Controlled Stochastic Realizations*

or

> *Bounded Rank-One Tensor Certificates for Two-State Numerical Word Experiments*.

The “General Theta Foundations I” prefix continues to imply a repository-closing foundational role that the dependency ledger does not support.

---

## 10. Minor and local comments

1. In `thm:main49`, define `v` immediately as the number of essential factor coordinates at the tested threshold; it varies with `delta`.
2. Say explicitly that the `v+1` sparsity bound is per rejected chamber, not for the union of chambers.
3. In the support lemma, call attention to the fact that `a_v<=1`; this makes the logarithmic cap well-defined.
4. In the chamber construction, state that surviving inactive entries are retained because their factor coordinates remain nonzero.
5. Define “positive upper endpoint” as `U_e>0` at first use.
6. The notation `b_e` is used both for incidence data and `b` for logarithmic right-hand-side bases; consider separating these symbols.
7. In the Farkas proof, explicitly state that the normalized dual polytope is nonempty only after an infeasibility witness is known.
8. Explain that the nonnegative cone in the dual is pointed, so testing its extreme rays is sufficient.
9. In `thm:algebraic49`, specify the effective representation of algebraic coefficients after clearing denominators, for example via a common primitive element and isolating intervals.
10. When rational powers of algebraic bases are used, specify the positive real branch.
11. In `prop:tight49`, replace “the feasible tolerance” by “the feasible set in this fixed chamber and stratum” and include endpoint rejection conditions.
12. In the cubic example, display the five entries used by the circuit directly next to the identity.
13. Give the short algebra showing `D^2=AC` and the rational bounds proving `2/5<D<1/2` in a separate line.
14. For general `rho`, write the scaled lower inequality explicitly once rather than saying only that the same circuit scales.
15. State that “rational machine” means every initialization, transition, and decoder coefficient is rational.
16. The irreducibility argument should say the integer cubic is primitive before applying reduction modulo seven.
17. In the orthogonal proposition, name the fixed query and two macro-words used in the lower-bound matrix.
18. The phrase “distinct rational orthogonal commands” is accurate, but the identity and coordinate swap commute; do not suggest a noncommutative result.
19. In the NP-completeness statement, repeat that `epsilon` is binary-TV tolerance and `2epsilon` is mean tolerance.
20. The NP-membership proof should cite a standard polynomial bit-size bound for a basic feasible solution of a rational linear system.
21. Add the tensor-completion references to `LITERATURE_AUDIT.md` as well as the article bibliography.
22. Keep the current correction that dyadic machines lie below any prescribed larger tolerance; do not revert to “attain every larger error.”
23. The exact checker limits should remain fail-closed. Document all command-line limits, including the factor-sign limit, in `--help` output.
24. The full 677-page and 1230-page cumulative archives are provenance records, not reasonable referee reading assignments. Keep them outside the journal-facing package.
25. The compact referee package should exclude redundant historical introductions unless specifically needed for comparison.
26. Distinguish the arbitrary-table cubic example from an orthogonal-word realization in every abstract-level summary.
27. Do not count the imported Gillis–Shitov NP-completeness theorem as a new complexity result.
28. Do not count the generic finite-vector moment convergence as part of the new duality contribution.
29. The branch and build receipts are unsigned Git commits. This is not a mathematical problem, but signed release tags would improve archival provenance.
30. Preserve the explicit statement that the A2/B4/C2 and eleven-paper aggregate gates remain open.

---

## 11. Final disposition

Revision 49 crosses an important threshold relative to v46: it now contains a correct and auditable structural theorem for a complete realization class, together with exact lower certificates and nontrivial optimal-error examples. This is real progress.

I would not recommend acceptance by a top-four general mathematics journal because:

- the complete theorem is confined to the all-two-state antisymmetric class;
- the finite input is fully expanded;
- the main mechanisms are classical after the scalar reduction;
- the exact examples remain very small;
- the closest tensor/toric literature has not yet been confronted;
- no higher-width or broad orthogonal classification follows;
- the inherited asymptotic program is not unified with the new duality; and
- none of the repository-wide analytic pipeline gates is closed.

After splitting, direct tensor-literature comparison, and tighter framing, the two-state duality paper could be a strong specialist submission. A meaningful extension to width three or to a broad succinct controlled class would substantially change the significance assessment.

**Recommendation: reject at the Annals / Inventiones / JAMS / Acta level; major revision and refocusing for a specialist journal.**
