# Referee Report

**Manuscript:** *The Two-Time Moving-Defect Problem for Dispersing Billiards*  
**Subtitle:** *Pair-safe selection lifts, occurrencewise propagated currents, product-time face control, global incidence Cauchy, two-cutoff convergence, and a strongly conditional pathwise CM2 criterion*  
**Source reviewed:** `cm2-bridge-note.tex`  
**Repository state reviewed:** `main` at commit `08aac05e51577bcd2f2ec5a6aef2a960a8d3ef9d`  
**Standard applied:** Annals of Mathematics / Inventiones Mathematicae / Journal of the AMS / Acta Mathematica  
**Recommendation:** **Reject as a research article; retain only as an internal technical program**

## 1. Summary

This is a very long working note whose stated purpose is to isolate a two-time estimate (“CM2”) needed for differentiating an infinite correlation susceptibility under moving billiard scatterers.

The note develops an immense ledger of:

- fixed-gauge difference quotients;
- graph-face and product-current decompositions;
- positive standard-family lifts;
- stopping trees and cemetery labels;
- occurrence and carrier kernels;
- physical/source Radon–Nikodym matching;
- polynomial escape and slope-energy estimates;
- multiple clock systems;
- shallow/deep and word/time cutoffs;
- weighted recovery and Hölder exponents.

Its main theorem is explicitly titled “Conditional pathwise quantitative CM2 criterion.” The theorem assumes a collection of interfaces so extensive that they occupy several pages: `UCR_sh`, full product moments, `REC`, `NST_phys`, `SS`, `ACTUAL_SLOPE_BRIDGE`, `PAIR_SAFE_REFERENCE`, `PPE_N`, `CEM_DOM`, `TENERGY_W`, `DUAL_MASS_KERNEL`, `MPD`, `POST_CARRIER_DOM`, `PHYS_TEST_LIFT`, `PHYS_TREE_MATCH`, `PROP_Q_MATCH`, `MAIN_CLOCK_COVERAGE`, `SEL_JSL`, `CLOCK_PROB_W`, `CLOCK_SRC_W`, `KRH`, `USC_end`, `BR_sec`, `FZ_geom`, `SF_split`, `CP_env`, `SHCOL_env`, `TAIL_env`, `NREC_deep`, `MT_DQ`, `FACE_2CUT`, and either `FACE_TIME_CM2` or `FACE_TIME_REC`, among others.

Under those hypotheses it proves the desired product decay and dominated convergence of the CM2 series.

This is not a solution of the two-time moving-defect problem. It is an elaborate conditional assembly theorem.

## 2. Main reasons for rejection

### 2.1 The main theorem assumes the hard part

Several hypotheses are essentially the estimates the theorem is meant to deliver:

- `FACE_TIME_CM2` is, by name and use, a CM2 time-majorant input for face owners.
- `TENERGY_W`, the clock bounds, and the selection-safe source likelihood provide the weighted small-ball/source estimates needed for the central band.
- `MT_DQ` assumes the fixed-gauge operator quotient decomposition and convergence of the typed pieces.
- `FACE_2CUT` assumes the growing-depth face convergence and the no-\(|s|^{-1}\) intermediate-tail bound.
- `REC` / `NREC_deep` assume the recovery moments needed for long-time control.
- `ACTUAL_SLOPE_BRIDGE`, `PPE_N`, and the physical/source matching interfaces assume the exact law transfers that are the nontrivial billiard-specific content.

The proof then combines these estimates correctly through Hölder, Cauchy, coupling, and dominated convergence. But the hard billiard theorem has been placed in the assumptions.

At a top journal, a criterion is meaningful only if its hypotheses are substantially easier to verify than its conclusion and are verified in an important model. Neither is demonstrated.

### 2.2 No concrete billiard family satisfies the full hypothesis list

The abstract expressly says that the explicit two-disk fixed-section pilot does **not** prove:

- the global block atlas;
- rare-cell regularity;
- all-depth weighted polynomial escape;
- transfer from the fixed section to the standard full-boundary collision map.

It also says that the cited literature does not supply the remaining gates.

Therefore the main theorem currently has no nontrivial verified application. A “nonvacuity route” is not a nonvacuity theorem.

### 2.3 The relative-translation example is only a pilot and does not close the target

The note derives several useful local or finite-block statements for a fixed-section two-disk setup:

- an exact two-step block identity;
- a typed product rule;
- a weak–weak gluing counterexample;
- a clean-core moving-boundary current;
- a local positive standard-family entry.

These are preliminary ingredients. They do not yield CM2 for the full collision map or flow.

The manuscript should not present the pilot in the abstract as if it nearly verifies the theorem. The missing gates are global, all-depth, and parameter-uniform; they are precisely the difficult part.

### 2.4 The hypothesis forest prevents independent audit

The main theorem refers to dozens of named interfaces, each with multiple internal clauses and cross-references. Many interfaces have both global and parentwise versions, physical and source versions, weighted and unweighted versions, and shallow/deep variants.

A referee cannot verify the theorem by following a finite dependency chain. The architecture resembles a proof-assistant specification without the machine checking. The possibility of:

- circular dependence;
- inconsistent normalization;
- reuse of an exponent under a different law;
- a hidden dependence on the final query;
- a missing measurability or projective-consistency condition;

is too high to assess reliably from the prose.

A top-journal proof must compress this machinery into a small number of natural lemmas with transparent hypotheses.

### 2.5 Several hypotheses are not intrinsic dynamical properties

The theorem depends on a large constructed probability space containing proposal marks, cemetery continuations, owner partitions, source-incidence records, and chosen carrier kernels. These may be legitimate proof devices, but the theorem must show that they are canonically generated by the billiard and that their constants are invariant under admissible representations.

At present many are interfaces to be supplied. This creates a danger that the auxiliary law can be tuned to encode the desired estimate. The exact physical/source Radon–Nikodym identities are intended to prevent that, but they too are assumptions in the main theorem.

### 2.6 The constant component-mass restriction is severe

The fixed probability-space gauge requires the normalized boundary-length vector of the scatterers to be constant along the deformation. A relative translation satisfies this, but general shape deformations do not. The theorem's geometric scope is therefore much narrower than “moving scatterers” suggests.

More importantly, a measure-trivializing transport does not by itself trivialize the moving singularity structure or provide differentiability of the transfer operator. The note sometimes gives the gauge disproportionate conceptual weight.

### 2.7 Conditional polynomial escape is not supplied by the cited roughness results

The manuscript correctly notes that roughness on an Axiom-A Cantor conditional does not imply the required physical-SRB polynomial escape on billiard unstable curves. It also correctly notes that conditional normalization among survivors cannot create full physical mass.

This admission is decisive. The physical polynomial escape estimate is one of the central new theorems needed for the phase argument, and it remains an assumption.

### 2.8 The product-time estimate is not obtained from known coupling alone

Sequential-billiard coupling gives loss of memory for proper families. It does not directly control a differentiated two-time graph current with moving faces, selection weights, and source amplitudes. The note introduces `FACE_TIME_CM2` or a recovered-core alternative precisely because this step is unavailable.

Thus the main theorem cannot be described as completing the problem from existing coupling technology.

### 2.9 Many local propositions are diagnostics, not advances at the claimed scale

Examples include:

- weak–weak composition can fail;
- global moments do not imply parentwise reverse Hölder;
- optional stopping cannot be applied to an uncontrolled terminal mark;
- a non-Borel code choice destroys measurability;
- bounded roof does not imply aperiodicity;
- one must distinguish probability clocks from additive source mass.

These are sensible safeguards. Individually they are elementary. Their accumulation does not amount to a top-tier theorem.

## 3. Relation to the literature

Demers–Liverani's projective-cone work gives powerful sequential-billiard estimates. Stenlund–Young–Zhang give uniform memory loss for moving scatterers. Demers–Zhang give spectral stability under perturbations. Baladi–Demers–Liverani give fixed-table flow mixing. None proves the differentiated two-time current estimate required here.

The note is accurate when it says so. The problem is that it does not prove the missing estimate either.

A top-journal contribution would need to verify the new physical polynomial-escape, face-time, and all-depth source-matching mechanisms in an actual billiard family, not merely name them as interfaces.

## 4. Presentation

The current document is not in publishable form:

- the title and abstract are extraordinarily long;
- the abstract is effectively a complete internal change log;
- the source is around twelve thousand lines;
- notation is introduced faster than mathematical structure;
- there is no short theorem map separating primitive assumptions from derived estimates;
- version-specific risk controls dominate the exposition;
- many paragraphs explain invalid proof routes rather than proving the valid one.

The phrase “strongly conditional” in the title is honest. It also confirms that this is a working note.

## 5. A publishable direction

There are two realistic options.

### Option A: prove one missing geometric gate

For a specific relative translation or radial family, prove one major theorem such as:

- the actual-SRB physical polynomial escape estimate at the required moving depth;
- the full-boundary fixed-gauge difference-quotient decomposition and convergence;
- the product-time positive face-envelope estimate;
- the all-depth physical/source occurrence matching with quantitative moments.

A paper containing one such theorem, with a concise application to CM2, could be important.

### Option B: publish a short abstract criterion elsewhere

If the goal is an abstract assembly theorem, reduce the assumptions to perhaps four or five natural hypotheses, state them invariantly, and give a 30–40 page proof. Do not claim a billiard solution until a model verifies them.

## 6. Recommendation

The note is a sophisticated research blueprint and a valuable internal audit. It does not prove CM2 for a genuine moving billiard family, and its main theorem assumes the decisive estimates.

**Recommendation: reject as a research article.**
