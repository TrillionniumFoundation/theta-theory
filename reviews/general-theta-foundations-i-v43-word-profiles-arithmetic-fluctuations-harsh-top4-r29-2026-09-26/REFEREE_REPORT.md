# Referee Report — General Theta Foundations I, Revision 43

**Manuscript:** *General Theta Foundations I: Word Profiles and Arithmetic Fluctuations of Numerical Memory*  
**Repository:** `TrillionniumFoundation/theta-theory`  
**Reviewed branch:** `revision/general-theta-foundations-i-v43-referee-ready-2026-09-26`  
**Reviewed publication head:** `153830f5dc8d13358f9103c307c619076c5ec80c`  
**Native mathematical source recorded by the manuscript:** `92722c0c14d1897740344a53e3e017258bec040e`  
**Controlling r28 report:** `d5fdba334f7a031413bba08c29af30a555936905`  
**Previous reviewed v42 publication:** `b5f9874903a429f9c1a9cb080547d50c891d050a`  
**Review branch:** `review/general-theta-foundations-i-v43-word-profiles-arithmetic-fluctuations-harsh-top4-r29-2026-09-26`  
**Date:** 26 September 2026

## Recommendation

**Reject at the Annals / Inventiones / JAMS / Acta level.**

**Mathematical disposition:** the new article is substantially stronger than Revision 42, and I did not find a fatal counterexample to its principal packet, arithmetic, metric, or irrational-fluctuation theorems. However, one displayed inference in the proof of the minimal-type theorem is false as written and must be corrected. The correction is local and does not appear to invalidate the theorem.

**Disposition outside the four leading general journals:** major revision before submission to a strong specialist journal. In a corrected and properly situated form, the paper could become a serious contribution on nonuniform positive stochastic realization width for Diophantine rotation alphabets.

Revision 43 genuinely answers the three most important mathematical requests in the controlling r28 report:

1. it replaces the one-family packet argument by an optimized finite-word distortion profile and a nonuniform interval budget applying to arbitrary hidden realizations;
2. it moves beyond the uniformly badly approximable class to minimal ordinary type, almost-everywhere logarithmic estimates, all irrational one-angle alphabets, and Liouville fluctuations;
3. it gives a direct theorem-level comparison with the Dick–Goda–Larcher–Pillichshammer–Suzuki Kronecker quasi-uniformity paper and stops presenting the shared algebraic vector or classical Diophantine input as new.

Those are real improvements. The present negative recommendation is therefore not a repetition of r28 and is not based on the claim that the main theorem is obviously false. It rests on the following independent obstacles.

1. **A correctness repair is mandatory.** In the proof of the minimal ordinary type theorem, the manuscript drops the `min{1/2, ...}` appearing in its own finite-type upper bound. The displayed upper estimate is false for sufficiently large auxiliary `h`. Restricting to sufficiently small `h`, or retaining the minimum, repairs the limit argument.
2. **The closest realization-theoretic literature is still not confronted.** The object being minimized is the state cardinality of a positive stochastic realization of a word-indexed rational response, with horizon-dependent time-inhomogeneous rows. The manuscript discusses quantization, branching programs and HMMs at a broad level, but it does not map its model to the extensive literature on positive realization, minimal positive order, stochastic/HMM realization, probabilistic and weighted automata, Hankel representations, and nonnegative factorization. Without that map, the priority and conceptual novelty of the central resource are not yet auditable.
3. **The two new profiles are useful but not a structural characterization of optimal width.** The lower distortion profile and upper polytope-enclosure profile have different quantifiers. No duality, comparison theorem, minimax principle, or broad criterion shows when either profile is sharp for the true hidden-state optimum. The packing–dilation corollary packages matching hypotheses; it does not establish those hypotheses for a broad new class.
4. **The sharp applications remain narrow.** The matched exponent is obtained for planar commuting rotations at minimal dual type and finite rational/dihedral extensions. For finite type above the minimum the bounds do not match; for Liouville angles the upper logarithmic limit remains in `[1/3,1/2]`; higher-dimensional intermediate and singular vectors are not classified; and no genuinely broad noncommutative family is solved.
5. **The resource model is mathematically coherent but exceptionally permissive.** The horizon, epoch, row tables, table construction, lookup, exact real arithmetic and exact sampling are free, and the machine may be redesigned for every `N`. The result is a theorem about nonuniform atomic positive-realization label width, not ordinary algorithmic memory, program size, random-bit space, or anytime simulation. The paper now says this, but the semantic distinction substantially limits general-journal impact.
6. **The repository-wide Foundations pipeline remains open.** Revision 43 closes none of the difficult A2/A3/A4, B1–B4, C1/C2 or D1 gates in the frozen dependency DAG. Its own `PIPELINE_STATUS.json` correctly marks the eleven-paper aggregate, B4, C2, historical A2 replacement, general nongapped classification and exact finite widths as open. The new local theorems must not be counted as closure of those unrelated analytic obligations.
7. **The series branding still overstates the result.** The subtitle is much more accurate than in earlier revisions, but “General Theta Foundations I” continues to suggest a foundational or repository-closing role that the paper itself explicitly disclaims. A specialist submission should be retitled around word profiles and positive stochastic realization width.

The paper is technically competent and, in several places, elegant. It is not yet a four-journal paper.

---

## 1. Scope of this review

I reviewed the focused fifteen-page Revision 43 article and the repository records needed to evaluate its mathematical claims, provenance, relation to Revision 42, and place in the larger paper pipeline. In particular, I examined:

- `papers/GTF-I-v43-arithmetic-profile/main.tex`;
- `introduction.tex`;
- `machine-model.tex`;
- `word-profiles.tex`;
- `circle-optimization.tex`;
- `arithmetic-scales.tex`;
- `metric-width.tex`;
- `irrational-fluctuations.tex`;
- `comparison.tex`;
- `references.tex`;
- `RESPONSE_TO_REFEREE.md`;
- `README.md`;
- `PROOF_STATUS.json`;
- `PIPELINE_STATUS.json`;
- `HISTORY_AUDIT.md`;
- `PREDECESSOR_MANIFEST.json`;
- `RESOURCE_LEDGER.md`;
- `LITERATURE_AUDIT.md`;
- `PRIMARY_SOURCE_AUDIT.json`;
- `PROFILE_CERTIFICATE.json`;
- `evidence/THEOREM_LOCATIONS.json`;
- `evidence/BUILD_RECEIPT.json`;
- `evidence/V43_EXACT_CHECKS.json`;
- `evidence/NEGATIVE_CONTROLS.json`;
- `verify.py`;
- the complete controlling r28 referee report;
- the retained v42 source and predecessor records relevant to the inherited packet mechanism;
- and the repository-level `ROUND17_PROOF_DEPENDENCY_LEDGER.md`.

I also made targeted external checks of the version-pinned Dick–Goda–Larcher–Pillichshammer–Suzuki source and of adjacent positive/stochastic realization and weighted-automata literature. This was not an exhaustive independent priority search.

The publication genealogy is clean. The final referee-ready head is three commits beyond the controlling r28 report; the native mathematical source is separated from the final packaging commit; old manuscript and review paths are retained rather than overwritten. This is good repository practice. It is not mathematical certification.

At the time of this review, no v44 branch was present. Revision 43 was the latest referee-ready General Theta Foundations I revision returned by the repository branch inventory.

---

## 2. What Revision 43 genuinely accomplishes

### 2.1 A finite-word converse profile against arbitrary hidden states

For a finite orthogonal alphabet and word length `B`, the paper defines

```text
D_k(p)
  = 1 - max_(u,v_1,...,v_k)
      sum_w p_w max_j <v_j,U_w u>,
Gamma_A(k,B) = max_p D_k(p).
```

The optimization over the word law is intrinsic to the listed finite alphabet and word length. It is not an analyst-selected packet presented as canonical. The profile allows every initial unit direction and every set of `k` outgoing centroid directions.

The endpoint contraction lemma is formulated with the correct hidden-state quantifier. A complete random word is independent of the information before its start; all internal stochastic rows are integrated into an endpoint kernel; outgoing conditional centroids are used only as test directions. Intermediate register sizes are unrestricted. The resulting estimate

```text
q' <= (1-D_k(p)) q
```

therefore applies to arbitrary hidden states, including states with no assigned observable vector beyond their actual conditional centroid.

This mechanism is inherited from the v35/v42 packet development, and Revision 43 credits it as inherited. The new contribution is the optimized finite datum and its systematic use.

### 2.2 A nonuniform interval budget and an actual-error lower bound

The dynamic program over disjoint intervals is a useful strengthening of a fixed packet tiling. An interval ending at time `t` and having length `B` is charged by

```text
chi_A(K_t,B) = -log(1-Gamma_A(K_t,B)).
```

The maximal sum over disjoint intervals is bounded by `log(1/kappa)` for every successful simulator. Because the test word laws are chosen independently on the selected complete intervals and the machine must be correct on every deterministic word, the proof does not inspect private runtime labels or assume independent letters inside a packet.

The same argument gives a lower bound on the best actual terminal error for a prescribed available-width profile. The occupation estimate for low-width cuts is also logically sound: the explicit greedy spacing count `M-(B-1) <= BJ` is the correct combinatorial statement.

This is the strongest genuinely general theorem in the paper. It applies to every finite orthogonal alphabet and does not assume commutativity or a spectral gap.

### 2.3 A separate exact positive synthesis profile

The enclosure profile minimizes a common dilation of a polytope with at most `k` generators and prescribed inradius. If

```text
rho * lambda_A(k,a)^N <= a,
```

the paper constructs one legal stochastic row for each command and label, initializes by a convex representation of `a x`, and uses a horizon-dependent decoder to restore the exact target amplitude.

The induction

```text
E[v_(S_t) | w] = a lambda^(-t) U_w x
```

is correct, and the decoder is bounded precisely by the displayed dilation condition. Carathéodory gives the stated successor sparsity. This is an exact wordwise realization in the declared atomic real-row model.

The manuscript is right not to identify this construction with the optimum over all hidden machines. That restraint is mathematically important.

### 2.4 Exact planar packet optimization

For planar rotations, the continuous search over the starting direction disappears by rotational invariance. For a fixed phase law, unit decoder centers induce cyclic Voronoi arcs, and the best contribution of one consecutive block is the norm of its weighted phase sum. Thus

```text
F_k(p) = max_(cyclic partitions P)
         sum_(A in P) |sum_(i in A) p_i z_i|,
Gamma_A(k,B) = 1 - min_p F_k(p).
```

The epigraph formulation with one family of second-order-cone variables per cyclic partition is valid. It can be exponentially large, as the manuscript states. The dynamic program for evaluating a fixed law is also plausible at the stated `O(k M^3)` arithmetic cost after cycling over the cut.

The four-phase certificate is correct: symmetry makes the uniform law optimal, and the values for one, two, three and four centers follow from the possible consecutive block sums.

This theorem makes one lower profile exactly finite. It does not compute the whole-run hidden width or the upper enclosure profile.

### 2.5 Finite arithmetic bounds at every scale

For the planar alphabet generated by the identity and `r` rotations, the lower profile is specialized through

```text
psi_alpha(H) = min_(0<||m||_1<=H) ||m.alpha||_(R/Z).
```

The packet uses `r` ordinary command segments and `L^r >= 2K` count vectors. Distinctness and separation are paid through actual commands; no count vector is supplied for free. The conclusion

```text
floor(N/B) psi_alpha(B)^2 <= log(1/kappa)
```

follows from the separated-phase certificate and the interval budget.

The upper profile is specialized through simultaneous approximation

```text
eta_alpha(q) = max_i ||q alpha_i||_(R/Z).
```

The regular `q`-gon dilation estimate has the correct order, and

```text
N eta_alpha(q) <= q^2/100
```

indeed suffices for an exact `q`-label common-row construction. The universal `O(sqrt(N))` exact upper bound follows by using only `eta_alpha(q) <= 1/2`.

The direct residue-collision lemma is also algebraically correct. Under

```text
||m.alpha|| >= b ||m||_1^(-tau),
```

it produces a simultaneous denominator satisfying

```text
c Q^(r/(tau+1-r)) <= q <= Q^r,
eta_alpha(q) <= Q^(-1).
```

Balancing the finite lower and upper profiles gives the stated power bracket and recovers the v42 exponent when `tau=r`.

### 2.6 Minimal ordinary type and almost-everywhere logarithmic bounds

The conceptual extension from uniform bad approximation to ordinary exponent

```text
omega*(alpha)
  = limsup_(||m||_1 -> infinity)
      -log ||m.alpha|| / log ||m||_1
```

is genuine. If `omega*=r`, then for every sufficiently small positive `h` there is a global constant at exponent `r+h`. The lower and upper powers converge to `r/(2r+1)` as `h` tends to zero.

The Borel–Cantelli proof of the logarithmic separation estimate is standard and adequate. Counting integer vectors on an `l_1` shell gives a summable series for every `s>1`; finite exceptions are absorbed into the constant after removing rational hyperplanes. The resulting lower and upper logarithmic corrections are obtained by a consistent finite-scale balance.

Subject to the correction in Section 4 below, the theorem appears valid.

### 2.7 Universal cubic scales and Liouville fluctuations

The continued-fraction separation lemma uses standard best-approximation facts and supplies the precise finite inequalities needed by the proof.

At horizon of order `q_n^3`, the lower bound uses the `q_n` phases with counts `0,...,q_n-1`, while the upper bound uses the polygon denominator `m_kappa q_n`. The constants are crude but the inequalities close. Thus every irrational one-angle alphabet has a subsequence on which width is comparable to the cubic root of the horizon.

For a Liouville angle, highly resonant denominators yield exact machines with subpower label counts along another subsequence. Combining that with the cubic subsequence and the universal square-root upper bound gives

```text
liminf log W_N / log N = 0,
1/3 <= limsup log W_N / log N <= 1/2.
```

The separate argument showing `W_N -> infinity` is necessary and correct: for each fixed `K`, the first `2K` irrational phases have a positive finite separation, and repeated independent packets eventually violate calibration.

The explicit number `sum_j 10^(-j!)` has the claimed tail bound. This is an effective illustration, not a new Diophantine construction.

### 2.8 Rational extensions and reflection

The finite rational extension argument properly pays for the rational phase by an `h`-fold state tag. Passing from `beta` to `gamma=beta/h` preserves a Diophantine lower bound up to a fixed factor because

```text
||m.beta|| = ||h(m.gamma)|| <= h ||m.gamma||.
```

Fixed integer coefficients only change constants in the polygon construction. Reflection acts by conjugation and phase inversion and preserves the regular polygon.

This covers finite rational reparametrizations and one dihedral-type noncommuting extension. It is not a general noncommutative classification.

---

## 3. Technical audit of the declared machine model

### 3.1 The model is explicit

The machine is a horizon-specific layered stochastic transducer. Initial rows may depend on the seed, command rows may depend on the epoch and command, and terminal columns may depend on the query. The peak is the maximum number of available labels at any layer, with the held binary answer charged as two labels.

All history and persistent randomness must be represented by the current label. Conversely, the horizon, external epoch, transition tables, their construction and lookup, exact arithmetic and exact sampling from known real rows are free.

This is a coherent mathematical model. The paper now distinguishes it from uniform computational space, total table size and finite-bit randomness. That distinction must remain visible in every abstract-level claim.

### 3.2 Calibration is sound

For a fixed word, total-variation error `epsilon` in a binary law gives coordinate mean error at most `2 epsilon`. Combining the coordinate decoders as a proof device and pairing with the unit target vector yields

```text
E <Y_N,d(S_N)> >= rho - 2 epsilon sqrt(D).
```

The decoder vector has norm at most `sqrt(D)`, so the expected conditional-centroid norm is at least

```text
kappa = rho/sqrt(D) - 2 epsilon.
```

No joint output distribution is assumed. This is a sufficient calibration certificate for the stated numerical experiment.

### 3.3 Why the model still limits significance

The model can encode arbitrarily complicated and infinite-precision information in the uncharged tables. It can be redesigned at every horizon and need not answer at intermediate stopping times. Therefore an exact `q`-label realization can have `(r+1)q` or more real rows whose description length, construction cost and sampling implementation are unbounded.

This does not invalidate the lower or upper theorems: the lower bound is stronger for allowing such machines, and the upper construction is legal. It does mean that “memory” must not be read as conventional algorithmic memory. The mathematically accurate term is nonuniform positive-realization label width.

A top general-journal paper could still be written about that resource, but it would need either a broad structural realization theorem or a much more decisive classification than the present examples.

---

## 4. Mandatory correctness correction

### 4.1 The proof of the minimal-type logarithmic law drops a minimum

Corollary 5.3 states that under a power lower bound of exponent `tau`,

```text
W_(N,epsilon)
  <= C N^min{1/2, r(tau+1-r)/(tau+1+r)}.
```

In the proof of the minimal-type theorem, the manuscript substitutes `tau=r+h` but writes, for every `h>0`,

```text
limsup_N log W_(N,epsilon)/log N
  <= r(1+h)/(2r+1+h).
```

That does not follow for every `h>0`. The corollary gives

```text
limsup_N log W_(N,epsilon)/log N
  <= min{1/2, r(1+h)/(2r+1+h)}.
```

The second term is at most `1/2` exactly when

```text
h(2r-1) <= 1.
```

For example, at `r=1` and `h=2`, the manuscript's displayed term is `3/5`, whereas the cited corollary only gives the square-root exponent `1/2`.

### 4.2 Repair

The theorem is repairable in either of two elementary ways.

1. Retain the minimum in the displayed estimate and then let `h` decrease to zero; or
2. state from the outset that one chooses `0<h<1/(2r-1)`, for which the second candidate is the minimum, and then let `h` decrease to zero.

The lower exponent is already correct. After this repair, both sides converge to `r/(2r+1)`. I therefore regard this as a mandatory local correctness correction, not a counterexample to the theorem.

### 4.3 Why this still matters

The error occurs in the proof of the first headline theorem, not in an optional remark. A referee-ready revision should not require the reader to reconstruct which branch of a minimum was intended. The exact restriction on `h` should be written, and a regression test of symbolic exponents does not substitute for correcting the proof.

---

## 5. The unresolved realization-theory and automata-theory comparison

This is the most important new scholarly objection in r29.

### 5.1 The manuscript's target is a rational word series with a positivity constraint

For fixed seed `x` and query `j`, the target mean

```text
w -> rho <e_j,U_w x>
```

has an ordinary signed linear representation of dimension at most `D`. The paper asks how many states are needed when the internal evolution must be stochastic and the state coordinates positive, while allowing horizon-dependent time-inhomogeneous transitions and bounded terminal functionals.

That is recognizably a positive/stochastic realization problem for a controlled word series. The severe gap between small signed linear dimension and larger positive realization dimension is a classical phenomenon in positive systems, HMM realization and nonnegative factorization.

### 5.2 The current bibliography is not sufficient

The manuscript cites Vidyasagar for HMM background and discusses branching programs, but it does not engage with the central realization literature. At a minimum, a revision should compare its model and results with representative work such as:

- L. Benvenuti and L. Farina, *A Tutorial on the Positive Realization Problem*, IEEE Transactions on Automatic Control 49 (2004), 651–664;
- L. Benvenuti, *Minimal Positive Realizations: A Survey*, Automatica 143 (2022), 110422;
- Y. Ohta, *On the Realization of Hidden Markov Models and Tensor Decomposition*, arXiv:2008.11487;
- L. Finesso, A. Grassi and P. Spreij, *Two-step Nonnegative Matrix Factorization Algorithm for the Approximate Realization of Hidden Markov Models*, arXiv:1007.3435;
- B. Balle, P. Panangaden and D. Precup, *A Canonical Form for Weighted Automata and Applications to Approximate Minimization*, arXiv:1501.06841;
- and the classical Hankel/rational-series literature underlying minimal weighted automata and probabilistic automata.

This list is indicative, not exhaustive, and I am not claiming that any one of these papers contains the present Diophantine width theorem. The point is that the paper has not yet explained its exact novelty relative to the standard language of the problem it studies.

### 5.3 The required comparison is mathematical, not bibliographic decoration

The authors should define the relevant finite-horizon Hankel or prefix/suffix matrices for their response family and answer the following questions.

1. What lower bounds on the present width follow from ordinary rank, nonnegative rank, positive realization order, or related cone-factorization invariants?
2. Which of those invariants fail to capture the sequential compatibility of one row per command and epoch?
3. How does allowing time-inhomogeneous rows and redesign at each horizon change the classical minimal realization problem?
4. How do separate seed initializations and query decoders enter the realization formalism?
5. How does wordwise `l_infinity` or binary-TV approximation compare with the norms used in weighted-automata approximation and HMM order reduction?
6. Is the enclosure polytope a special positive realization cone in the classical sense, and is the packet distortion related to a known factorization or communication invariant?

A strong answer could enhance the paper substantially. A weak answer could reveal that some of the terminology and claims should be narrowed. Until this analysis is present, the central novelty cannot be judged at a four-journal standard.

---

## 6. Why the paired-profile framework is not yet a foundations theorem

### 6.1 The lower and upper profiles solve different problems

The word distortion profile is a converse against arbitrary hidden states. The enclosure profile constructs one particular vector-state positive realization. Their quantifiers are deliberately different, and the paper correctly refuses to identify them.

That honesty also exposes the main structural gap: there is no theorem relating the two profiles to each other or to exact hidden width in a broad class.

### 6.2 The packing–dilation balance is conditional

Corollary 3.7 assumes both of the estimates needed for the final exponent:

```text
packet length <= C k^u,
cap radius ~ k^(-v),
enclosure dilation <= exp(C' k^(-u-2v)).
```

Once those hypotheses are given, balancing them to obtain

```text
W_N = Theta(N^(1/(u+2v)))
```

is useful and clean. But the corollary does not prove that a natural dynamical or geometric class satisfies these paired hypotheses, nor that the exponents on the two sides must match.

### 6.3 What would materially change the generality assessment

A four-journal revision would need a theorem of a different order, for example:

- a duality or comparison inequality between optimized distortion and positive enclosure complexity;
- a characterization of width in terms of a canonical cone, entropy number, nonnegative Hankel factorization, or semigroup invariant;
- a broad class of compact group actions for which both profiles are computed sharply;
- a sharp classification of all finite planar rotation alphabets, including nonminimal finite type and singular/intermediate cases;
- or a genuinely noncommutative family whose exact exponent is obtained for structural rather than finite-extension reasons.

More finite checks, more archived pages, or more examples with fixed constants would not supply this missing theorem.

---

## 7. Arithmetic scope and remaining open regimes

### 7.1 Revision 43 goes materially beyond v42

The move from uniform bad approximation to minimal ordinary type is not cosmetic. The Diophantine constants may degenerate along subsequences, so the constant-factor `Theta` law is replaced by a logarithmic exponent. The almost-everywhere logarithmic bounds and Liouville oscillations reveal behavior that v42 could not express.

The r28 objection that the paper only handled one uniformly separated commuting family is therefore substantially answered.

### 7.2 The classification is still incomplete

For `tau>r`, the finite-type bracket is

```text
N^(r/(2 tau+1))
  <= W_N
  <= N^min{1/2, r(tau+1-r)/(tau+1+r)}.
```

The powers generally do not match. The paper gives no lower/upper mechanism showing which exponent is correct for vectors of exact nonminimal type.

For Liouville angles, the result establishes genuine oscillation but leaves the upper logarithmic limit undetermined. It does not describe behavior between chosen convergent and resonant subsequences.

For `r>1`, singular vectors, vectors with prescribed uniform exponent, dependent vectors without a displayed independent basis among the letters, and anisotropic approximation spectra are not classified.

These are acceptable open problems in a specialist paper. They prevent the present paper from being a broad arithmetic classification.

### 7.3 The noncommutative extension is limited

The general profile theorems apply formally to noncommuting alphabets. The sharp arithmetic applications do not. Adding one reflection gives a dihedral semidirect extension whose regular polygon is invariant. This is a useful robustness check, not a solution of general noncommutative nongapped dynamics.

The final paragraph should avoid allowing the formal noncommutative scope of Section 3 to be confused with a sharp noncommutative width theorem.

---

## 8. Prior-art assessment

### 8.1 The DGLPS issue from r28 is repaired

The manuscript now version-pins Dick–Goda–Larcher–Pillichshammer–Suzuki, identifies their Theorem 3.9 and Lemma 3.11, and acknowledges that their Section 3.3 uses the same algebraic vector appearing in the predecessor. It correctly distinguishes their simultaneous Kronecker sequence from the dual packet phases `m.alpha` used in the lower bound.

The direct residue argument explains how a critical dual badly approximable condition implies the simultaneous lower bound needed for quasi-uniformity. The manuscript does not claim that the QMC theorem supplies the causal stochastic realization or the all-hidden-state converse.

This is an adequate response to the specific r28 priority objection.

### 8.2 The new literature audit remains targeted rather than comprehensive

The repository's audit files explicitly disclaim exhaustive independent priority certification. That is appropriate. The mathematical article should make the same limitation clear and should expand the realization-theory comparison described above.

### 8.3 Classical components are mostly labeled correctly

Nearest-center quantization, convex coding, Dirichlet approximation, continued fractions, the summable metric estimate and the explicit Liouville number are not presented as new. The endpoint conditional-centroid mechanism is marked inherited. The genuinely new claims are the optimized word profile, interval budget, exact planar law program, and the metric/Liouville consequences for the stated width resource.

This separation is substantially better than in earlier revisions.

---

## 9. Repository-wide pipeline assessment

### 9.1 The global dependency DAG is separate

The frozen Round-Seventeen ledger records, among other chains,

```text
A2 -> A3 -> A4 -> C2 -> D1
```

and

```text
B2-GC -> B1/B2-MC/B3/B4 -> C1/C2 -> D1.
```

The gates concern branchwise Fourier/local-limit analysis, stopped entropy/LDP, a global renewal kernel, nonlinear Nisio semigroups and graph cores, regular filtering, strict/form response, optional projection, and typed latent-phase contraction.

Revision 43's finite-word stochastic realization theorems do not prove those obligations and are not substitutes for them.

### 9.2 The manuscript's own pipeline status is appropriately fail-closed

`PIPELINE_STATUS.json` marks as false:

- `B4_aggregate_closed`;
- `C2_aggregate_closed`;
- `eleven_paper_aggregate_closed`;
- `historical_A2_replaced`;
- `general_nongapped_classification`;
- `general_infinite_gap_decidability`;
- `exact_finite_widths`;
- `fully_adaptive_collision_solved`;
- and independent expert review.

This is the correct status. The report gives no pipeline credit beyond the local v43 theorems.

### 9.3 Pipeline nonclosure is not a proof objection to v43

A focused paper need not solve every other manuscript in the repository. The problem is presentational: the Foundations title and cumulative archives can create an impression of program-level closure or weight. The journal-facing article should stand on its own and should not use repository volume, pipeline ancestry or unchanged older PDFs as evidence of significance.

---

## 10. Evidence, reproducibility and provenance

### 10.1 Strengths

The package records:

- a native mathematical source commit separate from the final publication package;
- predecessor hashes and unchanged v42 artifacts;
- theorem labels and page locations;
- source-bound builds;
- exact finite checks for the four-phase packet, interval recurrence, rational common rows, paid phase tags, arithmetic exponents and convergent identities;
- deliberately broken negative controls;
- and a successful recorded workflow.

The verification script uses explicit failures rather than Python `assert`, so optimized execution does not silently remove its checks. The package also states clearly that the checks are not universal proofs.

### 10.2 Limitations

The finite computations do not prove:

- the asymptotic minimal-type theorem;
- the Borel–Cantelli statement for all relevant vectors;
- the universal hidden-state quantifier in the packet theorem;
- the Liouville limit statements;
- priority;
- or journal significance.

The checks are useful for regression and delivery integrity only. The analytic proof must remain independently readable.

### 10.3 Genealogy

The reviewed final head adds the referee-ready package without rewriting prior review or manuscript paths. The source-to-publication comparison indicates that the last commit is packaging and evidence rather than a silent mathematical rewrite. This satisfies the repository hygiene expected for the review process.

---

## 11. Required revisions before a specialist submission

The following are mandatory, not optional polish.

### 11.1 Correct the minimal-type proof

Restore the `min{1/2,...}` or restrict the auxiliary `h` to `0<h<1/(2r-1)`. State explicitly why the chosen branch is active before taking `h` to zero.

### 11.2 Add a realization-theory comparison section

Provide a theorem-level mapping to positive realization, minimal positive order, HMM/stochastic realization, probabilistic and weighted automata, rational series, Hankel rank and nonnegative factorization. Define the finite-horizon object corresponding to the present word response and explain precisely which standard invariants do or do not control the sequential width.

### 11.3 Rename or sharply qualify the resource in the title and abstract

“Numerical memory” should be accompanied immediately by “nonuniform clocked atomic-row positive-realization label width.” A specialist submission should strongly consider dropping the `General Theta Foundations I` prefix.

### 11.4 Make constant dependence explicit

In the almost-everywhere theorem, state in the theorem itself that `c` and `C` may depend on the fixed vector `alpha`, `delta`, `r`, `rho` and `epsilon`, and are not uniform near rational relations or in growing dimension.

### 11.5 Add a standard reference for the Diophantine exponent

The notation `omega*` and the distinction among ordinary, uniform, simultaneous and dual exponents should be tied to a standard transference/Diophantine reference. The paper currently proves what it needs, but standard terminology is important in a result whose scope depends on the exact exponent notion.

### 11.6 Separate theorem-level novelty from conditional packaging

State explicitly in the introduction that the packing–dilation balance is a conditional meta-corollary. Do not present it as a classification theorem for finite orthogonal alphabets.

### 11.7 Preserve the fail-closed pipeline statement

The revised article and response must continue to say that no A/B/C/D analytic gate, aggregate publication gate or exact finite-width problem is closed by v43.

---

## 12. What would be required for reconsideration at a four-journal level

The corrections above would improve correctness and scholarship but would not by themselves change the top-four recommendation.

Reconsideration at that level would require a major new mathematical theorem, not another packaging round. Plausible directions include:

1. a structural duality between arbitrary positive hidden realizations and a canonical cone/polytope or nonnegative Hankel invariant;
2. a sharp width classification for a broad Diophantine spectrum, including exact nonminimal type and multidimensional singular regimes;
3. a general theorem for compact abelian actions beyond one common planar representation;
4. a genuinely noncommutative nongapped family with a computed exponent;
5. or a uniform/finite-bit version showing that the phenomenon survives after row descriptions, arithmetic and sampling costs are charged.

Any one of these would be a qualitatively larger advance than optimizing constants or adding more finite examples.

---

## 13. Minor and editorial comments

1. In the proof of the circle partition theorem, remind the reader that the decoder centers are constrained to the unit circle; this is what makes nearest chordal distance equivalent to maximizing the inner product without an additional center-norm term.
2. When `Gamma=1` and `chi=+infinity`, state the corresponding impossibility interpretation directly before the occupation formula.
3. Use unambiguous typography such as `||m||_1` consistently; several source passages are visually close to `||m_1||`.
4. In the almost-everywhere proof, spell out the monotonic step from rational `s>1` to every real `s>1`: choose a rational `s_0` with `1<s_0<s`.
5. State whether logarithms are natural. The limiting exponents are base-independent, but constants in the interval budget use the natural logarithm.
6. In the rational extension, give the final peak as `max(2,hq)` or the exact seed/phase count used, rather than only saying that a finite multiplier is harmless.
7. The phrase “finite second-order cone program” is correct but could be misread as polynomial size. Keep the exponential partition count adjacent to every complexity summary, not only in the theorem paragraph.
8. The finite algebraic quantifier-elimination statements are decidability results. They should not be called algorithms without an explicit warning about representation size and complexity.
9. In the universal cubic theorem, say explicitly that the constants implicit in `Theta(M_n^(1/3))` depend on the fixed calibration parameters but not on `n`.
10. The Liouville theorem uses two different special subsequences. A one-sentence diagram relating convergent cubic horizons and highly resonant subpower horizons would improve readability.
11. The exact upper rows may contain irrational or transcendental coefficients even when the command description is elementary. This should remain visible in the statement of exactness.
12. The comparison section should distinguish ordinary signed weighted-automaton rank from positive stochastic state cardinality before discussing branching-program Fourier growth.
13. The retained v42 article and cumulative archives should remain supplementary provenance, not part of the journal-facing logical dependency unless a theorem is actually imported.
14. The theorem-location manifest is useful, but page numbers should not replace stable equation and theorem labels in the response.
15. The article should state once, near the first definition of `W_(N,epsilon)`, that width is at least two because the held answer cut is charged.

---

## 14. Scorecard

| Criterion | Assessment |
|---|---|
| Internal correctness | Substantially plausible after one mandatory local repair; no fatal counterexample found |
| Novelty of the finite-word interval theorem | Meaningful and likely new in the stated formulation, subject to realization-literature comparison |
| Novelty of arithmetic input | Mostly classical and correctly labeled as such |
| Strength of sharp applications | Good for planar minimal-type rotations; incomplete beyond that class |
| Generality | Limited; formal general profiles, but sharp results remain essentially planar/Diophantine |
| Model significance | Mathematically coherent, but nonuniform and exact-real with uncharged tables |
| Exposition | Focused and much improved over v42; one headline proof error remains |
| Reproducibility/provenance | Strong for delivery integrity; not proof or priority certification |
| Repository-pipeline closure | None beyond the stated local objectives |
| Annals / Inventiones / JAMS / Acta suitability | No |
| Specialist-journal potential after revision | Yes |

---

## 15. Final verdict

Revision 43 is a serious and constructive response to r28. It introduces a useful optimized word profile, a legal interval converse against arbitrary hidden machines, a separate exact polytope synthesis theorem, a finite planar cone program, and genuinely new width consequences for minimal-type and Liouville rotation alphabets. The article is more focused, more honest about inherited and classical ingredients, and much better about external arithmetic prior art than Revision 42.

Nevertheless, the paper is not ready for acceptance anywhere until the dropped-minimum error in the headline proof is repaired. After that repair, the central obstacle is not an evident false theorem but insufficient structural and scholarly closure: the positive-realization resource is not compared to its closest established literature, the lower and upper profiles are not linked by a general theory, the sharp classifications remain narrow, the computational interpretation is highly nonuniform, and the broader repository pipeline remains open.

**Recommendation: reject at the four leading general mathematics journals; invite a major, independently reviewed specialist revision only after the correctness and realization-literature issues are addressed.**
