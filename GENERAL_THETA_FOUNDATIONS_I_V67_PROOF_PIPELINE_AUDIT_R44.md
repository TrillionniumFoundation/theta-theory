# Independent Proof and Pipeline Audit — General Theta Foundations I, Revision 67 (r44)

**Repository:** `TrillionniumFoundation/theta-theory`  
**Reviewed publication head:** `98a4b12126502ea41c620b58bad4b9aa30f9c72c`  
**Qualified native source:** `429a7cbe79c032386da934eb824d4ba31416ec44`  
**Revision 66 base:** `58490231d19fd5c5e557e353593251f1202105fa`  
**Prior external report:** v66/r43, `0a3d74582eeeda315237ee73fdd2ac0021862184`  
**Prior proof/pipeline audit:** `6c2aee0e242668ff960f3bf4835c87923b8e730f`  
**Source qualification run:** `37107995113`, success  
**Audit branch:** `review/general-theta-foundations-i-v67-proof-pipeline-audit-r44-2026-10-03`  
**Date:** 3 October 2026

## Executive classification

| Dimension | Independent audit result |
|---|---|
| Latest revision identity | **Pass.** Revision 67 at `98a4b121...` was the highest GTF-I branch located; no v68 branch was found. |
| Referee alias | **Incomplete.** A v67 work branch and review-ready marker exist, but no distinct v67 referee-ready branch was located. |
| Source genealogy | **Pass.** The publication commit is a direct successor of native source `429a7cbe...` and descends from v66 publication `58490231...`. |
| Intrinsic affine dimension | **Pass.** The real dimension is `s=d^2(m n^2-1)`. |
| High-resolution diamond entropy | **Pass with fixed-dimensional scope.** The coefficient `s` follows from affine interior, norm equivalence, volume packing, and an explicit rational upper net. |
| Rational intrinsic codec | **Pass.** No fatal defect found in coordinate elimination, affine reconstruction, positive buffering, canonical payload parsing, or exact CP/TP validation. |
| Adaptive programme upper bound | **Pass on a strict positive Choi body.** The classical-programme reduction remains valid for arbitrary common causal testers with bounded public stopping. |
| Repeated-Choi lower bound | **Pass.** Nonadaptive repeated Choi preparation and pair-dependent Helstrom testing yield the needed local quadratic separation. |
| Adaptive reusable entropy | **Pass with qualifications.** For fixed dimensions, fixed margin, and fixed error, the coefficient is `(s/2) log N`. |
| Boundary theory | **Open.** The manuscript proves failure of a global `sqrt(N)` modulus but not a rank/tangent-cone stratified law. |
| Exact PSD validation | **Pass as an exact arithmetic component.** It does not certify the analytical theorem by itself. |
| New finite regression | **Pass as implementation evidence.** It does not prove universal metric entropy, all adaptive testers, or novelty. |
| Source qualification | **Pass.** Run `37107995113` successfully qualified the native source and publication outputs. |
| Exact publication-head reconstruction | **Not completed at audit time.** No workflow run was attached to `98a4b121...` as triggering head. |
| Cryptographic identity | **Open.** The publication commit is unsigned; no contrary claim is made. |
| Independent priority clearance | **Not established.** The literature audit is author-side and targeted. |
| Whole Theta A/B/C/D closure | **Open.** Every aggregate completion flag remains false. |
| Four-leading-journal threshold | **Not met.** This is an editorial significance conclusion, not a correctness failure. |

The local v67 theorem package is coherent. Its principal weakness is not a detected contradiction but the restricted regime: fixed finite dimensions, strict Choi interior, fixed adaptive error, and a supplied memoryless instrument. The broader pipeline remains separate.

---

## 1. Frozen object and branch genealogy

The latest manuscript branch found was

```text
revision/general-theta-foundations-i-v67-intrinsic-instrument-entropy-2026-10-03
```

at

```text
98a4b12126502ea41c620b58bad4b9aa30f9c72c.
```

The publication commit message identifies it as the qualified v67 intrinsic/adaptive instrument-entropy publication. Its parent is the native theorem source

```text
429a7cbe79c032386da934eb824d4ba31416ec44.
```

The declared mathematical base is the v66 publication

```text
58490231d19fd5c5e557e353593251f1202105fa.
```

The controlling external report and audit are frozen into the package and identified as r43. No v68 branch was found. No separate v67 referee-ready alias branch was found, although the repository contains a v67 review-ready marker file and an exact-head workflow definition.

Both r44 review branches were created directly from `98a4b121...`. Each contains exactly one new report file. No manuscript source, PDF, evidence, workflow, predecessor file, or other review branch is changed by this audit.

---

## 2. Active proof dependency graph

### 2.1 Instrument geometry and intrinsic description

```text
Hermitian Choi blocks for m outcomes
  + joint partial-trace constraint
  -> affine translation space of dimension
       s = m(dn)^2 - d^2

positive central instrument
  -> relative interior in that affine space
  -> fixed-radius affine Hilbert--Schmidt ball

finite-dimensional norm comparison
  between Hilbert--Schmidt, Choi trace, and diamond norms
  -> diamond packing lower bound by volume

independent affine coordinates
  + rational grid
  + reconstruction of d^2 dependent coordinates
  + positive central buffer
  -> explicit legal rational diamond net

lower + upper
  -> log covering number
       = s log(1/eta) + O(1)
```

### 2.2 Adaptive reusable description

```text
strict blockwise Choi margin a
  + two nearby instruments J,L
  -> common endpoint instruments K_+,K_-
  -> two nearby Bernoulli programme distributions

same causal tester under both hypotheses
  + data processing
  + product-programme KL
  + Pinsker
  -> d_N(J,L) <= C(a) sqrt(N) ||J-L||_2

fresh maximally entangled input at each use
  -> repeated normalized Choi states
  + pair-dependent Helstrom test
  -> d_N(J,L) >= constant when
       N ||J-L||_2^2 >= constant

s-dimensional interior packing/covering at scale N^(-1/2)
  -> reusable covering number Theta(N^(s/2))
  -> description length (s/2) log_2 N + O(1)
```

### 2.3 Boundary obstruction

```text
rank-deficient/unitary phase family
  + parameter difference theta ~ 1/N
  -> one-use Choi/Frobenius distance O(1/N)
  + coherent N-use amplification
  -> constant/perfect adaptive distance

therefore:
  no global C sqrt(N) Euclidean modulus on the full body
```

### 2.4 Exact codec and validation

```text
supplied rational target
  -> exact retained coordinates
  -> signed rational truncation
  -> mixed-radix payload
  -> affine reconstruction
  -> central positive buffer
  -> exact rational instrument

ordered bordered minors / Schur elimination
  -> exact rational PSD validation

canonical payload/parser checks
  -> finite certificate format
```

### 2.5 Inherited v66 and earlier graph

Revision 67 retains, but does not replace:

```text
compact-group stationarization and purification
spectral-entropy occupation and width laws
return-free/no-idle quantitative bounds
exponential accuracy crossover
uniform classical numerical streaming
uniform Choi/instrument streaming
causal strong converse for repeatable probes
```

These inherited theorems provide context and some implementation primitives, but the v67 entropy coefficient is a separate affine-geometric statement.

---

## 3. Claim-by-claim status table

| Claim | Main source | Audit result | Principal qualification |
|---|---|---|---|
| Instrument affine dimension `s=d^2(mn^2-1)` | Section 38 | Correct | Fixed finite input/output/outcome dimensions. |
| Diamond/Hilbert--Schmidt norm comparison | Section 38 | Correct for stated use | Constants dimension-dependent and not claimed sharp. |
| Positive affine interior radius | Section 38 | Correct | Uses blockwise central instrument and fixed Choi normalization. |
| Diamond covering lower bound | Section 38 | Correct | Lebesgue volume is on the `s`-dimensional affine translation space. |
| Rational covering upper bound | Section 38 and codec | Correctly constructed | Legal net is encoder/validator image, not all grid strings. |
| High-resolution code length `s log(1/eta)+O(1)` | Section 38 | Correct | Fixed dimensions; public header excluded from payload. |
| Exact intrinsic coordinate codec | `instrument_codec.py` | Pass | Encodes a supplied target; not unknown-instrument learning. |
| Programme continuity `O(sqrt(N)r/a)` | Section 39 | Correct | Strict blockwise Choi margin and common tester. |
| Adaptive tester with stopping | Section 39 | Correctly handled | Stopping is public and bounded; pad programme draws to length N. |
| Repeated-Choi discrimination lower bound | Section 39 | Correct | Pair-dependent tester; fresh maximally entangled probes. |
| Fixed-error reusable entropy `(s/2)log N+O(1)` | Section 39 | Correct | Fixed margin and fixed nonzero error. |
| Boundary failure of global modulus | Section 39 | Correct example | Does not classify all boundary strata. |
| Exact PSD validation | Section 37 / code | Correct arithmetic lemma | Not a general optimal-code algorithm. |
| Whole-program completion | Status/ledger | Correctly false | No independent A/B/C/D gate is discharged. |

---

## 4. Detailed proof audit: affine geometry

### 4.1 Choi convention

The paper uses input-first, unnormalized Choi matrices. Each outcome map has a Hermitian block in `Herm(dn)`, of real dimension `(dn)^2`. The instrument body is

```text
J_y >= 0,
    sum_y Tr_out J_y = I_d.
```

All dimension and norm factors must be read in this convention. The source and codec use one convention consistently.

### 4.2 Rank of the affine constraint

The joint marginal map

```text
Phi((X_y)_y) = sum_y Tr_out X_y
```

maps onto `Herm(d)`. For an arbitrary `A in Herm(d)`, choose one outcome block `A tensor tau`, where `tau` is an output density matrix, and all other blocks zero. Then `Phi=A`. Thus the real rank is exactly `d^2`.

The affine dimension is therefore

```text
m(dn)^2 - d^2 = d^2(m n^2-1).
```

No positivity constraint is active at the central full-rank point, so this is also the local dimension of the feasible body.

### 4.3 Relative interior

The central instrument has identical blocks proportional to the identity:

```text
J_y^0 = I_(dn)/(mn).
```

Its joint partial trace is `I_d`, and every block has least eigenvalue `1/(mn)`. A translation-space perturbation whose block operator norms sum to less than this margin remains feasible. Since operator norm is bounded by Hilbert--Schmidt norm, a dimension-dependent Hilbert--Schmidt ball lies in the body.

This supplies positive `s`-dimensional volume in the affine plane.

### 4.4 Norm comparison

Let `X=(X_y)` be a Hermiticity-preserving instrument difference with zero joint marginal. The flagged direct-sum output convention makes the relevant instrument norm comparable to the sum of outcome diamond norms.

Applying the maps to a normalized maximally entangled input gives a Choi-state lower control, up to the input-dimension normalization. Standard Choi estimates give the upper control. Together with `||X||_2 <= ||X||_1 <= sqrt(rank)||X||_2`, the proof obtains constants `c,C` depending only on `d,n,m` such that

```text
c |X|_2 <= ||X||_diamond <= C |X|_2.
```

The exact constants in the source are sufficient for the subsequent covering estimates. No dimension-uniform statement is made.

### 4.5 Covering lower bound

Translate the body by the central instrument. Let `r B_2^s` be the legal interior ball. Suppose `M` diamond balls of radius `eta` cover the body. By norm comparison, each is contained in an affine Euclidean ball of radius `C eta`. Therefore

```text
vol(r B_2^s) <= M vol(C eta B_2^s),
```

and

```text
M >= (r/(C eta))^s.
```

This uses the correct affine dimension and needs no smoothness of the boundary.

### 4.6 Rational upper bound

A Hermitian matrix has one real coordinate on each diagonal entry and two real coordinates above the diagonal. The codec chooses all such coordinates across outcomes except one output-diagonal coordinate for each input matrix entry in one anchor outcome. The omitted coordinates are uniquely determined by the joint partial-trace equation. Exactly `d^2` real degrees are removed.

Rounding retained coordinates can amplify the omitted-coordinate error by at most a fixed factor equal to the number of contributing terms. A positive central buffer dominates the resulting operator perturbation. The denominator is adjusted so the reconstructed blocks remain positive and the joint marginal remains exactly `I_d`.

The number of retained digit vectors is `(2B+1)^s`, and `B` of order `1/eta` gives an `eta`-net. Hence

```text
N_diamond^Q(eta) <= (C/eta)^s.
```

The upper and lower exponents agree.

---

## 5. Detailed proof audit: adaptive programme upper bound

### 5.1 Strict positive body

The target family requires every outcome block to satisfy

```text
J_y >= a I_(dn)
```

for one fixed `a>0`. This is stronger than positivity of the total channel Choi matrix or of the sum over outcomes. It is the hypothesis needed to perturb each outcome block in both signs.

### 5.2 Common endpoint instruments

Let `Delta=J-L` and let `r=|Delta|_2`. After scaling by a dimension-dependent constant, define common endpoint instruments of the form

```text
K_+ = M + Delta/(2q),
K_- = M - Delta/(2q),
```

where `M` is an appropriate midpoint and `q` is chosen relative to the margin. Since `Delta` lies in the translation space, both endpoints preserve the affine marginal. The strict margin ensures block positivity.

The two targets can then be expressed as

```text
J = p K_+ + (1-p) K_-,
L = q K_+ + (1-q) K_-,
```

with `|p-q|=O(r/a)` and both parameters bounded away from zero and one in the local regime.

### 5.3 Programme representation under adaptive testers

At every invocation, first sample the classical programme sign and then apply the corresponding endpoint instrument. Conditional on the full programme sequence, the physical instrument sequence is identical under both hypotheses. The tester—including its quantum memory, entangled references, feedback decisions, and public stopping rule—is therefore one common quantum channel from the classical programme register to the final transcript/state.

By data processing,

```text
D(output_J || output_L)
    <= D(Bern(p)^{tensor N} || Bern(q)^{tensor N}).
```

A public stopping time bounded by `N` can be padded by unused programme symbols; discarding them is another channel and cannot increase divergence.

The Bernoulli divergence is `O(N(p-q)^2)` in the local parameter interval. Pinsker gives

```text
||output_J-output_L||_1
    <= C sqrt(N) r/a.
```

Taking the supremum over common testers yields the claimed upper modulus.

### 5.4 Large local distances

The local derivation assumes `r` below the margin scale. For larger distances the universal trace-distance bound `2` gives the displayed minimum with `2`. No gap occurs at the case split.

---

## 6. Detailed proof audit: testing lower bound

### 6.1 One-use flagged Choi state

For each use, prepare the normalized maximally entangled state between the instrument input and a reference. Record the classical outcome in orthogonal flags. The resulting state is the direct sum of the normalized Choi blocks.

The trace norm of the difference of these states is exactly, or up to the declared input normalization, the sum of the Choi trace norms. It therefore controls the affine Hilbert--Schmidt separation from below.

### 6.2 Tensor-power discrimination

Use fresh entangled pairs at each invocation. Under a memoryless instrument the output states are tensor powers. Fidelity or affinity tensorizes. Standard relations between fidelity and trace distance imply an error bound of the form

```text
error <= C exp(-c N r^2).
```

Equivalently,

```text
d_N(J,L) >= 2 - C exp(-c N r^2).
```

The tester is nonadaptive, so it belongs to the much larger class used in the definition of `d_N`.

### 6.3 Pair dependence

The optimal Helstrom measurement may depend on `J,L`. This is legitimate: metric separation asks whether for each pair there exists one admissible tester attaining the distance. The result is not a universal multi-hypothesis decoder for the whole packing.

---

## 7. Reusable metric entropy

### 7.1 Upper covering

Cover `C_a` in Hilbert--Schmidt norm at radius

```text
r_N = c(a,delta)/sqrt(N).
```

The programme lemma maps every such ball into a `d_N` ball of radius `delta`. Since `C_a` lies in an `s`-dimensional bounded affine body, a volume/grid upper bound gives

```text
N_(C_a,d_N)(delta) <= C N^(s/2).
```

### 7.2 Lower packing

Choose a smaller affine Euclidean ball around the central instrument that stays inside `C_a`. Pack it at Hilbert--Schmidt separation

```text
R_N = C(delta)/sqrt(N).
```

The repeated-Choi test makes every pair `d_N`-separated by at least `delta`. Volume gives

```text
packing >= c N^(s/2).
```

Covering number is at least packing number at a comparable radius.

### 7.3 Leading coefficient

Taking logarithms gives

```text
log_2 N_(C_a,d_N)(delta)
   = (s/2) log_2 N + O(1).
```

The `O(1)` depends on fixed dimensions, margin, and error. It is not uniform as `a` or `delta` varies.

### 7.4 Adaptive codec

The exact rational codec with grid `B~sqrt(N)` supplies a constructive description of length

```text
s log_2 B + O(1)
   = (s/2) log_2 N + O(1).
```

The adaptive certificate stores the same decoded memoryless instrument for every use. It does not store the tester's memory and does not simulate the tester classically.

---

## 8. Boundary and unresolved regimes

### 8.1 Failure of uniform interior continuity

For a unitary phase family, the Choi/Frobenius separation of parameters differing by `theta` is `O(theta)`. Choosing `theta~1/N`, coherent sequential use accumulates a constant phase and permits constant or perfect discrimination. Thus

```text
sqrt(N) ||J-L||_2 -> 0
```

can coexist with nonvanishing `d_N` near the boundary.

### 8.2 What is not proved

The package does not determine:

- metric entropy on fixed Choi-rank strata;
- local entropy near unitary or isometric channels;
- tangent-cone-dependent reuse exponents;
- simultaneous limits in `N`, error, margin, and dimension;
- optimal constants in the programme comparison;
- whether entangled/adaptive testers improve boundary covering exponents;
- a full comb/strategy-norm entropy theorem;
- an optimal variable-input workspace bound for codec construction and validation; or
- physical processor dimension needed to implement the decoded instrument.

These are the natural next mathematical problems.

---

## 9. Source-code audit

### 9.1 Coordinate enumeration

`coordinates(d,n,m,ay,ao)` enumerates all real Hermitian coordinates except one anchor output-diagonal coordinate for every input matrix entry in the anchor outcome. The count equals

```text
s = d^2(m n^2-1).
```

The regression suite checks this count over finite parameter ranges.

### 9.2 Affine reconstruction

`fill_affine` places the retained digits into Hermitian blocks and reconstructs the omitted anchor entries by subtracting every other outcome/output diagonal contribution from `B I_d`. This enforces an exact integer-scaled marginal before buffering.

`decode_digits` adds the central buffer to every block and adjusts the total denominator so the final partial trace equals `I_d`. It calls exact validation.

### 9.3 Payload coding

`pack_digits` and `unpack_digits` implement a base-`2B+1` fixed-length code. The bit count

```text
((2B+1)^s - 1).bit_length()
```

is the exact number of bits sufficient for every code integer. The hexadecimal serialization rejects overlong and noncanonical leading-zero fields, preventing an adversarial payload from forcing unbounded parse storage beyond the declared alphabet.

### 9.4 Active outcomes

With `preserve_zeros`, the encoder may omit identically zero outcomes and store an active-outcome mask. The effective dimension is then recomputed using the active outcome count. The public header and mask are separate from the payload length.

### 9.5 Validation and proximity

Bare decoding validates syntax, complete positivity, and joint trace preservation. It cannot certify proximity to an unspecified target. `verify` re-encodes the supplied target and compares the entire certificate. The source states this distinction correctly.

### 9.6 Adaptive grid

`adaptive_grid` selects `B` proportional to `sqrt(N)/(a delta)` times a fixed dimension-dependent constant. `encode_adaptive` first verifies the claimed Choi margin, then returns the ordinary intrinsic code plus the reuse metadata. It accurately describes itself as a reusable description, not a physical simulator.

### 9.7 PSD validation

The exact rational PSD routine is exercised by bordered-minor cases and negative controls. The analytical proof of polynomial bit complexity relies on fraction-free or controlled rational Schur elimination; the finite tests are regressions, not proof of all bit bounds.

---

## 10. Regression and evidence audit

The new receipt reports:

- `172262` new exact assertions;
- `480` codec cases;
- `40` adaptive-grid cases;
- `80` programme-product checks;
- `585` bordered-minor cases;
- `26` named negative controls;
- no floating-point decision oracle;
- inherited v66/v65/v64/v63 regression success;
- normal/optimized agreement;
- exact source inventory and isolated rebuild; and
- quantitative, structural, and complete PDFs with recorded hashes and page counts.

The negative controls cover malformed payloads, inconsistent dimensions, invalid masks, tampered error formulas, non-PSD reconstructions, false margin claims, and related parser/legality failures.

These checks materially increase confidence in the implementation. They do not establish:

- the continuum covering lower bound;
- the programme lemma for every adaptive tester;
- the tensor-power discrimination theorem in arbitrary dimensions;
- optimality beyond fixed parameters;
- independent novelty; or
- journal acceptance.

The receipt itself states the correct evidentiary boundary.

---

## 11. Workflow and provenance audit

### 11.1 Source qualification

The branch-specific source qualification run

```text
37107995113
```

completed successfully. The receipt binds the outputs to native source

```text
429a7cbe79c032386da934eb824d4ba31416ec44.
```

The workflow generated the rendered publication outputs and evidence.

### 11.2 Exact-head status

The publication head is

```text
98a4b12126502ea41c620b58bad4b9aa30f9c72c.
```

An exact-head workflow file exists in the tree, but an Actions query for this exact triggering SHA returned no runs at the time of audit. Therefore the final head has not yet received the separate read-only reconstruction used in several earlier revisions.

### 11.3 Referee alias

The work branch exists. A distinct v67 referee-ready branch was not found. The marker file should either be revised to say that the alias is pending or the alias should be created after exact-head verification.

### 11.4 Signatures

The publication commit is unsigned. The package makes no cryptographic authorship or release-signature claim. This is accurate, but a signed release would improve long-term provenance.

---

## 12. Literature and priority audit

The repository's literature file is explicit that it is author-side and not an independent expert opinion. It compares the new theorem with:

- finite classical resources for generic qubit-channel simulation;
- optimal and near-optimal learning of unknown channels in diamond distance;
- programme methods in channel metrology; and
- recent lower bounds for channel learning.

The distinctions drawn are largely correct. The v67 problem is neither unknown-channel tomography nor a physical classical simulation protocol. It encodes a supplied instrument and measures approximation under all common causal testers.

A fuller specialist comparison should include adaptive binary channel discrimination, especially Salek--Hayashi--Winter, arXiv:2011.06569. Their focus is error exponents and adaptive versus nonadaptive discrimination, whereas v67 studies a covering metric over a family. The distinction is genuine, but the concepts are close enough that the relationship should be stated.

Mele--Bittel, arXiv:2512.10214, and Oufkir--Girardi, arXiv:2601.04180, concern query/sample complexity for learning unknown channels in diamond distance. They do not imply the v67 description entropy, but they are relevant to any claim about intrinsic channel complexity. Naik--Gisin--Banik, arXiv:2501.15807, concerns physical classical simulation and is a different resource model.

The leading coefficient `s` has a classical convex-geometric character, and `s/2` has a local asymptotic-testing character. The likely novelty lies in the precise instrument/diamond/adaptive-tester synthesis and exact rational codec. Independent experts in quantum Shannon theory, programmable processors, and metric entropy should assess whether an equivalent formulation already exists.

---

## 13. Repository-wide pipeline assessment

The frozen analytic programme remains

```text
A2 -> A3 -> A4 -> C2 -> D1
B2-GC -> B1 -> B2-MC -> B3 -> B4 -> C1/C2 -> D1
A1 independent
```

Open gates include raw unsmoothed local limits, stopped-path entropy/LDP recovery, a global past kernel, exact canonical shell conditioning, process CLT/Mosco recovery, nonlinear Nisio cores, filtering/QMD/LAN, changing-filtration response, and labelled posterior contraction.

The v67 affine instrument body, codec, programme comparison, and repeated-Choi testing do not establish any of these gates. They may supply finite-dimensional tools useful elsewhere, but no bridge theorem is proved.

The following flags therefore remain false:

```text
historical_A2_replacement
B4_aggregate
C2_aggregate
eleven_paper_aggregate
whole_Theta_program
```

This separation is correct and should be preserved in all public summaries.

---

## 14. Risk register

### R1 — Independent priority risk: high

The literature audit is targeted and author-written. The subject is rapidly developing across adaptive discrimination, channel learning, programmable processors, and simulation.

### R2 — Boundary-regime risk: high

The strict-interior theorem does not describe rank-deficient or coherent boundary families. The manuscript supplies an obstruction but not a replacement classification.

### R3 — Joint-asymptotic risk: high

Fixed dimension, fixed margin, and fixed error hide potentially important dependence. A uniform theorem may have different exponents.

### R4 — Model-interpretation risk: moderate

A reusable classical matrix description is not a physical classical simulation and not an unknown-channel learner.

### R5 — Codec-alphabet risk: low to moderate

Not every digit word is legal. The codebook must be described as validated encoder outputs.

### R6 — Header/accounting risk: moderate in variable input

The leading payload law freezes dimensions and public metadata. Variable-input claims must charge the header and validation workspace.

### R7 — Exact-head provenance risk: low to moderate

Source qualification succeeded, but the exact publication-head read-only run and referee alias are pending.

### R8 — Regression overinterpretation risk: controlled

The package repeatedly distinguishes finite checks from universal proof; future summaries must retain that distinction.

### R9 — Whole-program overclaim risk: controlled

Aggregate pipeline flags remain false, but the size of the archive may tempt readers to infer broader closure.

### R10 — Four-leading-journal significance risk: high

The new results are elegant but local/fixed-dimensional and do not presently resolve a recognized broad external problem.

---

## 15. Specialist-release acceptance gates

### Mathematical gates

- keep a complete proof of the affine-rank calculation and norm comparison;
- state fixed dimension, fixed margin, and fixed error in headline theorems;
- distinguish the full body high-resolution law from the strict-interior reuse law;
- retain the boundary obstruction and formulate the rank-stratified open problem;
- state the exact adaptive tester class and stopping convention;
- keep Choi normalization factors explicit;
- identify the legal codec image rather than all payload words; and
- separate pair-dependent discrimination from universal decoding.

### Implementation gates

- complete exact-head read-only verification on `98a4b121...`;
- create the referee-ready alias only after verification;
- preserve canonical parser limits and exact CP/TP checks;
- include the active-outcome mask and dimensions in charged metadata for variable-input claims;
- distinguish decoder legality from target-proximity verification; and
- publish a minimal standalone codec example and manifest.

### Priority gates

- obtain an independent theorem-level literature review;
- add adaptive channel-discrimination comparisons;
- compare explicitly with programmable-processor approximation and channel metric entropy;
- retain distinctions from unknown-channel learning and physical classical simulation; and
- avoid claiming novelty for finite-dimensional volume packing or Pinsker/programme arguments in isolation.

### Editorial gates

- submit a focused instrument-entropy paper rather than the full combined archive;
- move detailed historical preservation records to a repository supplement;
- keep the 112-page complete edition archival;
- reduce repeated disclaimers by consolidating the resource model in one formal section; and
- state the principal theorem pair in one concise introduction.

---

## 16. Final audit verdict

### Local mathematics

**Pass with qualifications.** No fatal gap was found in the v67 intrinsic dimension, high-resolution diamond entropy, rational codec, adaptive programme upper bound, repeated-Choi lower bound, or fixed-error reusable entropy law.

### Boundary and generality

**Open.** The rank-deficient boundary, joint dimension/error/reuse regime, and variable-input mutable-workspace converse are not solved.

### Implementation

**Pass for the stated fixed-dimensional codec.** The exact source correctly reconstructs the affine constraint, validates legality, bounds payload parsing, and supplies adaptive grid scaling. It encodes supplied rational data, not an unknown instrument or a physical implementation.

### Reproducibility

**Strong source-bound evidence; incomplete exact-head closure.** Source qualification and isolated rebuild succeeded. The final publication head had not yet received its separate read-only exact-head workflow run, and no referee-ready alias was found.

### Priority

**Open.** The author-side audit is useful but not independent. A broader adaptive-discrimination and programmable-channel comparison is still needed.

### Whole Theta programme

**Open.** No A/B/C/D aggregate gate is discharged.

### Overall

```text
intrinsic affine dimension:       PASS
high-resolution entropy:          PASS, FIXED DIMENSION
rational codec:                   PASS, VALIDATED IMAGE
adaptive programme upper bound:   PASS, STRICT INTERIOR
adaptive packing lower bound:     PASS
reuse coefficient s/2:            PASS, FIXED ERROR/MARGIN
boundary classification:          OPEN
variable-input workspace law:     OPEN
source qualification:             PASS
exact final-head attestation:      PENDING
independent priority:              OPEN
whole-program closure:             OPEN
four-leading-journal bar:          NOT MET
```

Revision 67 should be treated as a serious specialist-level theorem package. Its correct editorial disposition is rejection at the four leading general journals and encouragement of a sharply focused specialist submission after the stated mathematical, priority, and release-hardening steps.
