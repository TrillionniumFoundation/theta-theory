# Response to R60 — General Theta Foundations I, Revision 94

We thank the referee for the detailed report on Revision 90. We retain the manuscript's topic and four-leading-general-mathematics-journal objective. The intervening v91 already supplied the formal normal form, arbitrary-experiment variational and dual principles, pure-atom classical criterion and equal-prior experiment; v92 supplied the dimension-preserving two-cut hierarchy. We preserve these published results and distinguish them from this revision's additions.

The controlling external report is v90/R60 at `cf13712c54e9ef0c9c54a240b1f26efc78cc3568`, with companion proof/pipeline audit `e4e72a512bf747e7bd190196cd8dc3db35689e3c`. The immediate published base is v93 at `3b660839818d6ef676da72fb6e9969501be4e59a`, native source `2595ee56f70138c58b1924591d32e09cbad31381`. Both controlling reports remain byte-identical. No newer report is assumed.

## Inherited v93 response to the structural objection

Primary Section 19 identifies all initial Gram matrices attaining the rank-r optimum: the necessary and sufficient condition is `rho<=I/r`. Every such matrix has an attaining projection decomposition with at most d terms; the proof constructs its weights and a complete instrument on the actual Schmidt support. Counting the first reference as an independent third resource gives the exact minimum-dimension formula and an attainment using no feedback. Thus the result is not just a list of endpoint strategies.

The rank-sensitive deficit estimate gives quantitative closeness of both branch Grams to a common normalized rank-r projection. Summing its nonnegative losses yields approximate initial projection decompositions and a spectral loss certificate. The exceptional qubit rank-one face is not swept into a false common-support statement: its equality set is precisely commutation with the pure factor, and an exact pinching identity controls the error, including mixed factors.

These additions answer the significance objection with proved structure and equality information. They do not turn the solved shared-latent experiment into a universal strict-gap theorem. The general variational and dual statements retain their broader arbitrary-experiment quantifiers. The original R60 venue judgment remains unchanged for the referee to reconsider against the new manuscript.

## Required revisions

### R01

**Location:** Primary 15.2; 18.1 and new Section 19.

The full unit-reset normal-form lemma is retained. Dimension-preserving Kraus and fresh-mixture refinements now cover mixed protocols without adding an uncounted coherent environment.

### R02

**Location:** Primary 15.1; Definition rankclass92 in 18.1.

The three original closed classes remain formal; the retained dimensions specify both recording cuts, all remaining quantum registers, public records, early termination and closure.

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

**Location:** Current audit files and predecessor-v93-audit/.

All active top-level proof/history/internal audits carry Revision 94. Their exact predecessor bytes are preserved.

### R09

**Location:** Printed Primary Sections 15–19.

Printed primary numbering is used first. Source modules 83,82,84,85,86 are archival identifiers. Build-generated theorem numbers are cross-checked against the visible PDF headings; auxiliary page anchors alone need not locate a heading after a page break.

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
| D08 | Primary 15.2 and 18.1 | Rectangular domains and codomains are explicit; the rank-restricted forms land in C^k and C^ell. |
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

## Additional current locations and checks

Theorem 19.1, Corollary 19.2, Lemma 19.3, Corollary 19.4 and Propositions 19.5–19.6 correspond respectively to the optimal initial cap, three specified cuts, stable common support, approximate frames, initial spectral loss and exceptional qubit pinching. The generated theorem-location record supplies source labels and auxiliary anchors. Actual heading pages are checked against the submitted PDF and reported in the root review entry; auxiliary anchors alone may precede a page break.

R03/D12 receive the full rank-dependent equality stability and mixed qubit exception. R05/D14/D15 receive fixed-subspace normalized attainments at all three cuts with no feedback. R10 is kept distinct: rational initial eigenvalues yield rational decomposition weights, but no rational eigenbasis or efficient second-moment design is assumed. R11/D19 require adding calibrated score error before any spectral inference; Gram weights are never substituted for physical branch probabilities. R08/R09/R13 receive current active audits, primary numbering and the two-manuscript submission route, with predecessor copies retained.

The new suite labels its exact fixtures, deterministic numerical sanity cases and negative controls separately, and runs in both Python modes. No numeric success is described as a continuum proof. The inherited v93 build had 35 suites. All are retained, and the v94 spectral-value suite brings the current fresh production build to 36 suites.

## What remains external

R06 / pipeline P05 requires independent human specialist priority assessment. None has been obtained; the author-side literature comparison and this response cannot constitute it. This is an outstanding external assessment, not a reason to weaken any proved theorem. Main and unrelated papers are untouched, the five analytic aggregate closure flags remain false, and no journal acceptance is claimed. Current publication and exact-final-head qualification refer only to freshly observed v94 receipts; v93 receipts remain predecessor evidence.


## Current R60 continuation: exact initial values and feedback

The controlling external report is v90/R60 at `cf13712c54e9ef0c9c54a240b1f26efc78cc3568`, with companion proof/pipeline audit `e4e72a512bf747e7bd190196cd8dc3db35689e3c`. The immediate published base is v93 at `3b660839818d6ef676da72fb6e9969501be4e59a`, native source `2595ee56f70138c58b1924591d32e09cbad31381`. Both controlling reports remain byte-identical. No newer report is assumed.

New printed Primary Section 20 contains the prescribed-spectrum value theorem, secular concavity lemma, rank-constrained fresh-Gram lemma, a general rank-capped spectral-envelope evaluation, an exact receiver-message criterion and exact loss/saturation consequences. These are additions to the retained v91–v93 proofs, not a renaming of their contributions.

For every fixed pure initial Gram rho and r=min(k,ell), the biased value is p_E+t^2*chi(q^(r)(lambda(rho)))/(2L). The initial pure acquisition is held fixed. The upper covers all protocols at the stated cuts; the converse builds an actual recorded instrument on its Schmidt support. All branches have the same atom spectrum and at most d commuting atoms suffice. The optimum fresh spectrum is given by the secular eigenvector, not assumed uniform. Singular factors and zero signal are treated before dividing.

Holding the whole old receiver and restricting only the fresh reference, withholding a receiver message gives the leading-eigenvalue value instead. A message is strictly useful exactly when t>0 and 2<=r<rank(rho). The d=3 spectrum (3/4,1/8,1/8) has an explicitly normalized two-outcome instrument and strictly positive gain. The formula explains when the no-feedback globally attaining constructions do and do not remain optimal after fixing the initial acquisition. Its exact rank saturation and exact deficit strengthen, rather than replace, the earlier equality-set and quantitative-loss results.

R01/R02/D08–D16: the complete refined normal form is invoked at fixed rho and the converse is written explicitly, including its rectangular maps, Gram sums, null histories and probability-weight distinction. R03: a separate rank-constrained leaf optimization treats singular factors and identifies the true fresh optimizer. R07/R14: the new exact initial value uses the specified biased prior; the equal-prior hierarchy and local fixed-tube theory retain their original statements. R08/R09/R13: current audits and reading routes are updated; all prior bytes are archived, printed numbering is primary and the initial journal package stays primary plus one supplement. R06/P05: Nielsen, Jonathan–Plenio and assistance antecedents are added to the primary-source comparison; no human priority clearance is invented. All R01–R15 and D01–D30 responses above remain applicable except that the immediately preceding base/current-version identities are superseded by this continuation.
