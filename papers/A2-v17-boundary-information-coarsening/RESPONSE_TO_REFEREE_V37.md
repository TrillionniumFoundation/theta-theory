# Response to the v36 referee report — A2 v37

**Manuscript:** *Boundary laws, intrinsic periodic rigidity, and global physical reconstruction in dispersing billiards*  
**Author:** Qian Qi  
**Date:** September 13, 2026.

The report answered here is `reviews/a2-v36-external-harsh-top4-2026-09-13/REFEREE_REPORT.md`, at review commit `01e772030042ffde9df125c0d40401aee2aabd17`. Its reviewed submission is v36, `0802bfa20533feff55bf5620d39d6399d5e778f5`. The present mathematical-source revision is `b0c21cd799bbe4d96bab4a7e1e369d5d7152b294`, on `revision/a2-v37-referee-closure-native-submission-2026-09-13`. Locations below are native source paths and theorem labels, not page references to an uninspected main PDF.

We thank the referee for separating the accepted mathematical repairs from the remaining delivery and hypothesis-navigation requirements. We retain the full scope of the article and correct the precise full-table implication identified in E2. We also repair the current navigation. The execution record contains newly performed finite checks and an actual native companion build. It does **not** establish the complete-main delivery required by C2; that item remains open.

| Item | Response in this revision |
|---|---|
| E2: full-table hypothesis reference | Corrected in the theorem statement and its proof; lattice recovery and all-orbit propagation now have separate hypotheses and references. |
| I1: current-version navigation | Both current README entries identify v37, the exact v36 report, this response and the current verification ledger. Previous README contents are preserved. |
| R1 and v36 dependency clarification | Retained without modification. No renewed claim of proof from total variation alone is introduced. |
| C2: complete native delivery | Partially advanced, **not closed**. Actual companion products and focused diagnostics are available; the complete native main was not built or inspected. |

## 1. E2: hypotheses for complete periodic determination

**Location:** `article/23f_single_offset_law_inverse_v26.tex`, `thm:v26-single-offset-global`, part (3), and its proof.

We agree that `thm:v24-lattice-gram-recovery` does not state the spanning-tree hypothesis needed to place every obstacle orbit. Its conclusion concerns the lattice. The former reference was therefore insufficient as a source of the full-table hypotheses, even though the intended stronger theorem was present elsewhere in the article.

Part (3) now explicitly assumes that the data are realized by a labelled periodic dispersing billiard with connected real-analytic strictly convex obstacle boundaries; that the marked lifted-channel graph is connected; that it contains a rank-two anchoring pair of signature-rigid cycles based at one channel frame; and that a rooted signature-rigid spanning tree reaches every obstacle orbit. It cites `thm:v24-uncalibrated-periodic-rigidity`. These are the hypotheses of the existing full-table theorem, not newly imposed substitutes for the local inverse or a weakened conclusion.

The proof now distinguishes the two operations. In the common starting frame, let the recovered translation holonomies be the columns of V, and let the independent marked deck displacements be the columns of M. The lattice theorem gives

\[
L=VM^{-1},\qquad G=M^{-T}V^TVM^{-1}.
\]

The independence required here is over the real deck space; no unimodularity is inserted. These formulas determine the lattice realization and its marked Gram form. They do not place obstacle orbits that have not yet been reached.

For those placements, start at the root. At each tree incidence the already placed analytic boundary and its uniquely matched framed signature determine the adjacent channel placement. Induction reaches every obstacle orbit by the explicit spanning hypothesis. Realizability supplies existence and admissibility; the lattice calculation and tree induction establish uniqueness. Changing the initial frame applies one simultaneous element of SE(2) to the entire realization. It does not permit independent motions of the recovered obstacles.

The local input remains exactly the signed one-offset law of each contact type, together with the onset gap and the marked incidence information. The four-density cancellation supplies the two unsymmetrized action germs; the weighted half-line and finite-remainder argument supplies the contact jets; analytic continuation supplies the incident boundary images. No ambient longitudinal positions, supplied lattice metric, residual-time observation or uncharged registration is introduced into this intrinsic theorem.

The edited chapter retains all thirteen of its existing labels. Its density identity, fixed-order stability proposition, finite-flight corollary and preceding proofs are unchanged. A finite SE(2) tree diagnostic checks the composition convention, the common global gauge and rejection of an unreached declared orbit. That finite calculation is not a replacement for analytic signature rigidity or for realizability.

## 2. I1: current entry points and provenance

The root `README.md` and the paper `README.md` now identify v37, the precise latest report, the revised native entry, this response and `VERIFICATION_V37.md`. The stable paper directory is retained. The old root and paper README contents are copied without alteration to their respective `README_PRE_V37.md` files. The older A1 and programme navigation links remain available.

The mathematical-source commit is distinguished from the subsequent documentation/evidence commit. The source guards compare the actual native files with the pinned original blobs. In particular, the main entry changes only its two revision identifiers; its abstract and ordered inputs remain unchanged. The manuscript does not acquire a review log, a test-status table or repository-operational prose as a substitute for mathematical exposition.

## 3. R1, likelihood normalization and compact experiments

**Locations retained:** `article/18a_vector_boundary_information_v26.tex`, `article/18a2_likelihood_tilting_moments_v34.tex`, `article/18a1_compact_experiments_v32.tex`, and the count–endpoint chapters.

We retain the accepted separation of three arguments. The one-mark expansion gives the alternative mean before the independent-sum fourth-moment estimate is applied. With \(\ell_n=\log(1/\delta_n)\), \(q_n=\delta_n\ell_n^{1/4}\), and \(B_n=np_n\delta_n^2\ell_n\to1\), the retained budgets are

\[
np_n\delta_nq_n=B_n\ell_n^{-3/4},\qquad
np_n\delta_n^2\log(1/q_n)
=B_n\left(1-\frac{\log\ell_n}{4\ell_n}\right),\qquad
np_n\delta_n^4q_n^{-2}=B_n\ell_n^{-3/2}.
\]

The fourth-moment expansion is for summands centered under the same alternative. The bounded alternative mean is then restored. Every excluded observation contributes zero; one excluded observation does not erase the rest of the sample. These are moment estimates under the original product law.

Separately, the normalized likelihoods and the LAN expansion give the weak shifted limit by truncation and likelihood tilting. Unit means give uniform integrability through the retained identity \(\mathbb E(L_n-A)_+=1-\mathbb E(L_n\wedge A)\). Combining the shifted limit with the original-law fourth moments justifies the unbounded quadratic-risk limit. Total-variation comparison alone is not used to justify that limit. The fixed Moore–Penrose inverse acts on the identifiable range of the information matrix.

The finite likelihood-vector comparison and the compact-net passage also remain separate. The compact theorem retains its uniform continuity modulus, parameter-independent kernels and the order of limits with a fixed net before refinement. It is not replaced by a theorem only for finitely many local parameters. No claim of uniform equivalence on an unbounded local parameter space is added.

The new numerical run re-executes the report's original-alternative mean example, together with its other five finite families. Its role is a consistency check. The accepted general moment proof is retained, not reclassified as a theorem established by that radial example.

## 4. Other substantive distinctions in the report

The revision preserves the distinction between a density law and point values available in a finite sample; between an interior density norm and total variation; between signed endpoint data and pointwise folding; between the classification of admissible gluings and a uniqueness theorem; and between analytic continuation and an effective, well-conditioned reconstruction algorithm.

Likewise the two-sided moving-ceiling argument retains its separate bulk hypothesis and its reverse reconstruction kernel, including corner and exceptional-event rules. The physical pilot, fixed-window ordering, charged preparation failures and same-experiment direct-position benchmark remain in place. None of those chapters is removed or rewritten to evade the referee's distinctions.

The primary mathematical claim remains the nonlinear relative long-bridge law combined with the unsymmetrized contact inverse and its geometric consequences. We do not count the matrix formula for L, a standard compact-net argument, or the presence of a Poisson boundary model as a newly created rigidity theorem. This revision makes no new priority claim and does not present the absence of a counterexample as a correctness or acceptance certificate.

## 5. C2: actual products and remaining requirement

The unchanged native `two_collision.tex` was materialized byte-for-byte from Git blob `df44402b17031525c087d39dfedf8dac3ada611d` and compiled with `latexmk` and `pdflatex -no-shell-escape`. The exit code was zero. The PDF has seven pages and SHA-256 `9f2a4dc2b68b70a4f931a4c65371675ab8e895bc439dec55c843a84e66fc3670`. The command, tool identification, complete final log and driver output are retained. The PDF and an evidence archive are supplied with the revision conversation; the repository ledger identifies them without pretending that a hash is the product itself.

All seven companion pages were inspected in a rendered overview, and page 5 was inspected at a larger scale. No clipping or missing glyph was observed in that scope. The final log has no unresolved references or citations, duplicate-label warning, missing character or overfull box. It does contain the expected `epstopdf` warning that shell escape is disabled. This is companion evidence only.

Eight focused diagnostic families were executed in ordinary Python and with `python -O`; both exited successfully and produced identical JSON. The script retains the latest referee's six diagnostic families byte-for-byte and adds source guards and a finite rooted-tree example. It does not recursively validate every manuscript input or compile TeX.

The v37 hosted run `34735598451`, job `103666347616`, ended in failure with no executed steps, no log URL and no artifacts. The cause was not established. This does not establish a TeX error. More importantly, it supplies no complete-build evidence. The complete native main was not built or PDF-inspected locally in this session either. **C2 remains open.**

To close it, the unabridged native main and companion must be built from an identified full checkout, with actual products, commands, versions, exit statuses, complete final logs and recorder/input hashes retained, followed by an explicit inspection of the assembled PDFs. The inherited complete build driver and the source-first workflow remain available, but their configuration is not reported as execution. This remaining delivery item is not a mathematical no-go statement, a reduction of the article's scope, or a claim that another theorem could compensate for missing products.

## 6. Disposition of this revision

E2 is corrected in the native mathematical text; I1 is corrected in both current entry points; the accepted R1 and compact-experiment repairs are retained. The response and historical audit identify what was directly checked and what is inherited. The present branch is suitable for examining those revisions and their limited execution evidence, but we do not request that C2 be treated as closed or that the complete assembled article be accepted on that basis.
