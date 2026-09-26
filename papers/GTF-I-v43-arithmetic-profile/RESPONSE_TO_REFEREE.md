# Response to the twenty-eighth pipeline-aware referee report

**General Theta Foundations I — Revision 43**  
**Word Profiles and Arithmetic Fluctuations of Numerical Memory**  
26 September 2026

Controlling report: `reviews/general-theta-foundations-i-v42-canonical-gap-calibration-pipeline-harsh-top4-r28-2026-09-26/REFEREE_REPORT.md`, at `d5fdba334f7a031413bba08c29af30a555936905`. Reviewed publication: `b5f9874903a429f9c1a9cb080547d50c891d050a`; native source: `bc4e304693eb13b979154f5ad30c937390925352`.

The report finds the v42 proofs coherent but asks for a finite-word invariant, an extension beyond uniform bad approximation, and a direct comparison with the Kronecker quasi-uniformity paper. The current revision addresses those mathematical requests. It does not use a change of venue or deletion of the series title as a substitute for a stronger theorem. The new remote branch starts at the controlling report and adds only this revision package and its publication entry.

Stable labels below are resolved to actual theorem numbers and pages in `evidence/THEOREM_LOCATIONS.json`. Full analytic proofs are in the article.

## 13.2 / Sections 4.4 and 9.1 — the omitted direct arithmetic source

**The source is added and the theorem-level dependency is made explicit.**

Dick–Goda–Larcher–Pillichshammer–Suzuki, arXiv:2502.06202v2, is version-pinned to 13 February 2026. Its Theorem 3.9 characterizes quasi-uniformity of the vector-valued Kronecker sequence `n alpha mod Z^r` by a simultaneous badly approximable inequality. Lemma 3.11 controls consecutive best simultaneous denominators. Their Section 3.3 also contains exactly the vector `(2^(1/(r+1)),...,2^(r/(r+1)))` used earlier. That vector and the underlying arithmetic geometry are not presented as new.

The v42 packet phases were instead the scalar quantities `m.alpha mod 1`. The current comparison explicitly distinguishes the dual and simultaneous inequalities. `lem:weak-denominator` supplies a direct residue-pigeonhole transference calculation with the constants used in the memory proof. At the critical dual exponent it implies the simultaneous badly approximable condition in the cited paper. Thus its quasi-uniformity theorem genuinely applies to the old uniform class; the comparison does not evade the overlap by changing terminology.

The QMC theorem does not construct a causal stochastic encoder or bound arbitrary hidden updates. Conversely the current almost-everywhere logarithmic separation is not claimed to imply quasi-uniformity. It is weaker than uniform bad approximation and is proved by a summable tail estimate. `LITERATURE_AUDIT.md` records exactly what was read: versioned metadata, the relevant full HTML section, and PDF pages including the displayed theorem, denominator lemma and algebraic vector. It does not assert exhaustive independent priority clearance.

## 13.3–13.4 / Sections 3.5, 5.2 and 9.3 — a finite-word framework

**Addressed by two distinct optimized finite profiles, an exact planar program, and a causal interval theorem.**

`Gamma_A(k,B)` maximizes, over probability laws on actual length-B words, the minimum loss under k centroid directions uniformly over all starting unit directions. It is an alphabet quantity, not an analyst-selected certificate. Compactness gives attainment, fixed algebraic data admit quantifier elimination, and a matrix-perturbation bound prices word length. Duplicate letters are immaterial. The word table is finite but can be exponential; this is not a general efficient algorithm.

`lem:packet` retains and fully proves the inherited endpoint mechanism. Given the old state and a complete independent word, all internal computation collapses to one stochastic endpoint kernel. Pairing with the outgoing centroid directions and enlarging the set of assignments gives `q' <= (1-Gamma)q`. Intermediate widths are unrestricted, and hidden unobservable directions are allowed. This mechanism is explicitly credited to v35/v42, not counted as a new invention.

`thm:profile` converts the optimized value into a nonuniform invariant. A dynamic recurrence maximizes `sum -log(1-Gamma_A(K_t,B))` over disjoint intervals. That value is at most `log(1/kappa)` for a successful simulator. The same recurrence lower-bounds the actual optimal terminal error over all machines with the given available profile. The proof chooses independent complete packets and fixed words in every gap and remainder. It does not assume independence of letters inside a packet, and it never chooses the law by inspecting private runtime labels. The greedy occupation count is displayed as `M-(B-1)<=B J`.

The upper profile `lambda_A(k,a)` minimizes common polytope dilation at k vertices and fixed inradius a. `thm:enclosure` gives exact common rows whenever `rho*lambda^N<=a`. It includes initialization, every command and the bounded terminal decoder. Lower and upper profiles have different quantifiers: no arbitrary hidden realization is assumed to be an observable polytope. `cor:balance` states precise packing and dilation hypotheses yielding a matched memory exponent for finite orthogonal alphabets, without assuming commutation. `prop:recoding` explains invariance of existing logarithmic exponents under bounded positive-word recodings, with the identity-padding qualification explicit.

For circle word sets, `thm:circle-socp` evaluates the continuous quantizer exactly through cyclic partitions. Optimizing the word law is a finite second-order cone program. A fixed law can be evaluated in O(k M^3) arithmetic operations; the complete cone program can have exponentially many partition constraints. `prop:square-packet` supplies exact optimal values for all state counts in a four-phase packet. The nearest-center geometry itself is classical; the operational use is a finite converse certificate for an entire hidden-state computation.

## Sections 3.5, 5 and 10 — outside uniform bad approximation

**Addressed by minimal-type, full-measure and Liouville theorems, not by restating the old hypothesis.**

`thm:arithmetic` first gives bounds in the unmodified finite functions

```
psi_alpha(H) = min_(0<||m||_1<=H) ||m.alpha||_(R/Z),
eta_alpha(q) = max_i ||q alpha_i||_(R/Z).
```

For `B=r(ceil((2K)^(1/r))-1)`, every width-K machine obeys `floor(N/B)*psi_alpha(B)^2<=log(1/kappa)`. For every q>=4, `N*eta_alpha(q)<=q^2/100` supplies an exact q-label common-row realization. These statements do not require a uniform arithmetic power. Every finite planar rotation alphabet has the additional exact O(sqrt(N)) upper bound. Each ordinary command remains charged.

`thm:metric-main` proves that every rationally independent vector of minimal ordinary dual type `omega*=r` has logarithmic width exponent `r/(2r+1)`. It does not claim a constant-factor Theta law on this larger set. The ordinary-type hypothesis allows the critical-scale lower constants to vanish along subsequences. For almost every vector and every fixed delta>0, the theorem gives the explicit lower and upper logarithmic corrections displayed in the abstracted main statement and README. The measure argument is classical and reproved; its numerical-memory consequence is the theorem here.

`cor:power-type` provides upper and lower power bounds for a noncritical finite dual type, without pretending those bounds match. `cor:rational-extension` handles redundant rational combinations when an independent basis is present among the actual letters. Its rational residue class is carried in a paid finite phase tag. If every angle is rational, an explicit finite orbit tracker gives bounded width. The reflected extension keeps the same matched logarithmic conclusions.

`thm:cubic-scales` applies to **every irrational single angle**, not just badly approximable angles. For each convergent denominator q_n it identifies a horizon of order q_n^3 with width between q_n/2 and a fixed multiple of q_n. The lower bound uses the q_n separated phases; the upper bound multiplies q_n by a fixed calibrated integer and checks the finite polygon inequality. All constructions remain exact.

`thm:liouville-main` proves, for **every Liouville angle**, that the lower logarithmic width exponent is zero, while the upper logarithmic exponent lies between 1/3 and 1/2. Width still tends to infinity. The explicit number `sum 10^(-j!)` supplies an exact subpower-horizon family. Thus even one fixed two-letter alphabet need not have a single power law. The exact Liouville upper limit is not determined. No universal classification of every irrational or every noncommuting alphabet is inferred from these results.

## 13.5 — gap scope and external inputs

The old optimized action/block gap theory is preserved in its entirety. The new finite-word profile is not that infinite-dimensional norm optimization; both may be useful even when all finite-block action gaps vanish. Fixed algebraic packet computation does not certify a general infinite gap. The new main proofs use no external positive spectral gap at all. The rational SO(3) example and its qualitative Benoist–de Saxce dependency remain in the unchanged v42 article, with no numerical gap invented. The optional older LPS source-audit limitation is likewise not declared resolved.

## 13.6 — calibration is a sufficient finite certificate

The old exact projection formula, certified isotypic input, 2^D sign inequalities, SDP rank condition and frame stability remain unchanged. The current core uses the elementary coordinate calibration `kappa=rho/sqrt(D)-2 epsilon`, so the main arithmetic scope is unambiguous. No calibration value is renamed as the exact whole-experiment critical error, and no quantifier-elimination statement is called practical. All fixed-signal and fixed-error assumptions are stated before the horizon limit.

## 13.7 / detailed model comments

Definition `def:machine` counts available persistent labels and a held two-label final answer. Positive-probability labels under a selected test law can strengthen a particular converse but are not substituted for available width. The machine is horizon-specific; command words are external; only one terminal coordinate is requested. Rows, decoder, epoch, real arithmetic, construction and table lookup are free in the stated atomic positive-realization model.

The general enclosure construction has |A|k common command rows and at most D+1 successors per row. A planar r-angle construction has (r+1)q rows and at most three successors; a reflection adds q rows, and finite rational phase labels multiply the actual state and row counts. These are not succinct-table or finite-fair-bit implementation theorems. Irrational-angle constructions have exact real atomic coefficients. The old algebraic angles do not imply algebraic matrix entries.

Constants depend on the fixed alphabet, r, signal and tolerance. No uniform growing-r claim, optimized crossover, best packet distribution for the entire horizon, exact finite hidden width, or optimal polygon shape is asserted. The four-phase optimal packet is expressly a finite example, not a generic optimality claim. Arithmetic separation used by the cosine bound is at most 1/2 by its definition as circular distance.

## 13.1 and 13.8 — focus and preserved mathematics

The General Theta Foundations I series prefix is retained with a precise mathematical subtitle. The current article follows one proof spine: finite word profiles, exact planar optimization, finite arithmetic bounds, minimal-type/metric laws, and irrational fluctuations. The journal-facing core is independent of the cumulative archives. Classical and inherited ingredients are identified within the mathematical exposition. Its conclusion does not use internal A/B/C/D project labels or archive length as evidence of significance.

The entire v42 article is retained byte-for-byte as `supporting-results.pdf`. Its complete mathematical and development volumes are appended without alteration after the full current article and a divider. All original paths and branches remain unchanged. No earlier theorem, calibration, expansion result or representation calculation is withdrawn merely because the new core does not repeat its full proof.

## Historical pipeline and next review

The full controlling r28 report, the frozen Round-Seventeen dependency ledger, the v42 sources and history record, and the original v35 packet proof were consulted. All v42 native files used by this work were checked against their published source hashes. The new proofs use the inherited packet mechanism in its actual complete-word independence convention. The deeper Fourier/local-limit, stopped-LDP, global-kernel, semigroup, domain, filtering and optional-projection obligations of the separate analytic manuscripts are preserved; they are not certified by the new finite-word results. No claim is made to have re-proved every archived page.

The next referee can test the finite alphabet optimization, the cyclic-partition equivalence, the metric logarithmic balance and the convergent/Liouville subsequences. Executed finite checks, intentionally broken controls and source-bound builds are delivery evidence only. Independent mathematical scrutiny and priority evaluation remain distinct from these checks.
