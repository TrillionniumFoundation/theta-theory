# Response to R60 — General Theta Foundations I, Revision 92

We thank the referee for the detailed mathematical and editorial analysis of Revision 90. We retain the manuscript's topic and journal objective. The intervening v91 completion already supplied the requested normal-form presentation, arbitrary-experiment variational/dual principles, pure-atom classical criterion, equal-prior example and quantitative Gram rigidity. This revision takes that published source as its immediate base and extends the general principle to two independently bounded receiver registers. It proves every value of their exact hierarchy on the same finite family, with explicit adjacent gains. No v91 result is being presented as a new v92 result.

The controlling report/audit commits are `cf13712c54e9ef0c9c54a240b1f26efc78cc3568` / `e4e72a512bf747e7bd190196cd8dc3db35689e3c`. Immediate base: v91 publication `ce2616a9f5d870d5cf4c8ee254a728544a0bea6a`. There is no new v91 referee report being assumed. The R60 venue judgment is preserved for reconsideration against the strengthened manuscript, not rewritten as approval.

## Principal mathematical response

The arbitrary-experiment optimum now has rank-k old atoms and rank-ell fresh Grams, with a common first barycenter, attained primal and dual, and a finite maximizing realization. The crucial proof refines discarded Kraus and fresh-mixture indices into classical records instead of retaining an extra quantum environment. The old register is counted after its recorded instrument; the initial first-call reference is not bounded by k. This distinction prevents a false all-times memory statement.

For the fixed shared-basis ensemble, r=min(k,ell) determines the exact biased and equal-prior optima, respectively `(d+1)/L+t^2(r-1)/(2rL)` and `1/2+t^2(dr-1)/(2dr(d+1))`. The lower uses a cyclic family of rank-r projections with sum rI; complete-class upper bounds use rank-sensitive negative-mass and centered-swap inequalities. Every adjacent level is strictly separated for t>0. Universal dual and calibrated score certificates apply at each specified resource threshold.

## Required revisions

### R01

**Location:** Primary 15.2; new 18.1.

The full unit-reset normal-form lemma is retained. Dimension-preserving Kraus and fresh-mixture refinements now cover mixed protocols without adding an uncounted coherent environment.

### R02

**Location:** Primary 15.1; Definition rankclass92 in 18.1.

The three original closed classes remain formal; the new dimensions specify both recording cuts, all remaining quantum registers, public records, early termination and closure.

### R03

**Location:** Primary 17.1; Lemma rankswap92 in 18.3.

Spectrum, fidelity and eigenvalue equality steps remain explicit. The rank-r extension treats singular factors and the distinct d=2,r=1 equality exception.

### R04

**Location:** Theorems operationalhierarchy90, equalprior91, rankspectrum92.

Each finite-game theorem states the once-drawn device rule. Independent redraws yield the scalar two-slot channel, not the same experiment.

### R05

**Location:** Primary 17.3; equation cyclicrankprotocol92 in 18.4.

The seven Pauli devices, both priors, normalized reference/input vectors and complementary effects remain explicit. The new construction specifies all rectangular factors and their normalizations.

### R06

**Location:** LITERATURE_AUDIT.md; INDEPENDENT_REVIEW_BRIEF.md.

Primary-source comparison is completed for the stated models. Independent human priority clearance has not been obtained and is not marked complete.

### R07

**Location:** Introduction and Primary 18.

Local orders, arbitrary-experiment exact values and solved shared-basis spectra have different quantifiers. Their common feature is the operational interface and reset cut, not an implication between theorems.

### R08

**Location:** Current audit files and predecessor-v91-audit/.

All active top-level proof/history/internal audits carry Revision 92. Their exact predecessor bytes are preserved.

### R09

**Location:** Printed Primary Sections 15–18.

Printed primary numbering is used first. Source modules 83,82,84,85 are archival identifiers. Build-generated theorem/page locations are authoritative.

### R10

**Location:** Primary 16 finite-design lemma.

The weighted exact second-moment family has real weights and an existence support bound; no rational construction or polynomial-time design algorithm is inferred. The same family is used at every rank threshold.

### R11

**Location:** Primary 17.4 and Corollary rankwitness92 in 18.4.

Channel, prior and law perturbations retain their explicit quantifiers and unhalved-to-probability factors. The same hybrid bound applies to each fixed dimension class; preparation defects compare specified implementations to ideal strategies.

### R12

**Location:** RELEASE_PROVENANCE.md and generated receipts.

Inherited transport records are kept historical. New native-source, artifact-only publication and exact-head checks must be observed separately; Actions checks, legacy statuses and unsigned objects are not conflated.

### R13

**Location:** JOURNAL_README.md and standalone package.

The initial submission route remains one primary plus one current linked supplement and reproducibility note. All inherited archival material remains in the research package.

### R14

**Location:** Definition rankclass92; PROOF_STATUS.json.

The response adds a complete hierarchy only for two specified recording-cut dimensions. It does not identify all-time workspace dimension, unrestricted coherent-memory transfer or arbitrary-pair strict advantages. The original theorem statements remain unchanged.

### R15

**Location:** HISTORY_AND_PIPELINE_AUDIT.md.

The independent A2/B4/C2 and later statistical/analytic obligations remain separate; all five aggregate closure fields remain false.

## Detailed comments

| Comment | Current location | Response |
|---|---|---|
| D01 | Primary 16 | The priors sum to one; their difference and t=0 baseline are explicit. |
| D02 | Primary 16–17 | The averaged one-call equality is a channel identity, including entangled inputs. |
| D03 | Primary 16 | Weighted exact second-moment family is used, without assuming an unweighted design. |
| D04 | Primary 16 | The at-most d^6+1 support bound is not a complexity or optimal-support claim. |
| D05 | Primary 15.1 and 18.1 | Finite-dimensional trace-norm tester closure is specified. |
| D06 | Primary 15.1 | Complete call slots and Choi factor order are explicit. |
| D07 | Primary 17.2 | Swap and symmetric/antisymmetric projectors are real under full transpose. |
| D08 | Primary 15.2 and 18.1 | Rectangular domains and codomains are explicit; the new restricted forms land in C^k and C^ell. |
| D09 | Primary 15.2 and 18.1 | Kraus completeness gives the common Gram sum, with positive trace tails. |
| D10 | Primary 15.1 and 18.1 | Formal null histories are included, also at projective endpoints. |
| D11 | Primary 17.2 and 18.4 | Positive-part optimization is used for each final decision block. |
| D12 | Primary 17.5 and 18.3 | Rigidity is about normalized Gram factors, not unique dilations. Rank-one equality exceptions are distinguished. |
| D13 | Lemma countable91 | The trace-class remainder lemma is retained and used by the dimension refinement. |
| D14 | Primary 16–17 | Independent device inputs and final joint reference readout are distinguished. |
| D15 | Primary 17.2 and 18.4 | Uppers cover arbitrary feedback; attainments need only the stated finite instrument. |
| D16 | Proposition causalnormal91 | The named physical causal-normalization proposition remains active. |
| D17 | Primary 16–17 | Antisymmetric input states are normalized and supported in a nonzero subspace for d>=2. |
| D18 | Primary 17.3 | Both orders of each Pauli eigenbasis are included. |
| D19 | Primary 17.4 and 18.4 | Unhalved trace-norm to decision-probability conversion retains the factor 1/2. |
| D20 | Corollary gamestability91 | The complete measurement channel is perturbed per latent index; the decision law is specified. |
| D21 | Primary 16–18 | At t=0 the equal-prior values all equal 1/2 and strictness is not claimed. |
| D22 | Primary 15.2 and 18.4 | Unnormalized branch formulas handle t=1 zero-probability outcomes. |
| D23 | Introduction | Explicit dimension formulas do not make local fixed-tube constants uniform. |
| D24 | Primary 13–14 and 18.1 | V/N and Q remain call-allocation resources; k and ell are different specified Hilbert-space dimensions. |
| D25 | Primary 14 | A large individual Q_pi still is not an information lower certificate. |
| D26 | Source preservation and journal package | All predecessor active labels and the current linked supplement are retained. |
| D27 | Generated LaTeX logs | Warnings are recorded as emitted. No blanket warning-free claim is made. |
| D28 | Release records | An Actions check run is not a legacy commit status. |
| D29 | Release records | Object hashes and reconstruction are not independent human signatures. |
| D30 | Frozen report and reply | R60 is an author-requested assessment, not an editorial decision commissioned by a named journal. |

## What has and has not been supplied

All manuscript-actionable R60 requests have explicit locations above. R06 / pipeline P05 requires an independent specialist judgment that this author-side revision cannot itself constitute; it remains outstanding. This is a priority-review status, not a reason to weaken a mathematical theorem. The two-cut dimension hierarchy is a new stated theorem with its own proof and quantifiers. It neither removes reset nor closes the separate analytic programme. All predecessor mathematical sections remain byte-identical and active. New exact checks supplement rather than replace proofs; publication qualification refers only to the newly observed source-bound and exact-head receipts.
