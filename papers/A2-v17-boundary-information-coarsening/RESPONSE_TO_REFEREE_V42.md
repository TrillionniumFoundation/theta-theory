# Response to the A2 v41 referee report

**Manuscript:** *Boundary laws, intrinsic periodic rigidity, and global physical reconstruction in dispersing billiards*  
**Author:** Qian Qi  
**Revision:** A2 v42, September 14, 2026  
**Branch:** `revision/a2-v42-native-source-referee-response-2026-09-14`

The addressed [report](../../reviews/a2-v41-independent-harsh-top4-2026-09-13/REFEREE_REPORT.md) is committed at `e162532115071265cf73b97a5069f33628347cfe` and concerns submission `c730a60bbc8af2a4c6e432813c31dccc897828e7`. This response addresses that report, rather than relabelling an earlier response. The current source entry is [main.tex](main.tex); execution claims are confined to [VERIFICATION_V42.md](VERIFICATION_V42.md).

We thank the referee for distinguishing the nonlinear analytic and geometric arguments from their algebraic conclusions, and for identifying the remaining delivery and navigation requirements. The revision retains the complete mathematical scope and auxiliary derivations. In particular, it does not replace intrinsic transverse-law determination by the easier position-sampling experiment, impose contact symmetry, truncate the asserted finite-order inverse, or remove the statistical and global reconstruction results.

## 1. C2: complete source-matched native delivery

We agree that a configured workflow, an isolated companion, a miniature integration fixture, and finite diagnostics do not establish delivery of the complete manuscript. The relevant entries are the original complete `main.tex` and `two_collision.tex`, with every active recursive input and the companion-generated auxiliary references.

The new v42 workflow checks out the exact triggering commit, attempts to export the complete manuscript source independently of compiler installation, and invokes the retained fail-closed native builder for both entries. The first actual v42 workflow run was `34798984887`, at source-infrastructure commit `4d78f5d3850cfae79df6b13c30176e9c64222efe`. The job metadata show failure with no executed steps and runner ID zero. This attempt did not execute TeX and supplies no native PDF certificate. No billing, infrastructure, or compiler cause is inferred from those metadata.

At this initial source-revision checkpoint, **C2 remains open**. The verification ledger records that fact explicitly. Closure requires actual complete-main and companion products, exact source identities and recursive-input coverage, the commands and their exit status, raw logs and recorders, companion auxiliary producer/consumer provenance, PDF identities, and rendered-page inspection. The revision neither waives these requirements nor changes the manuscript to a shorter surrogate. Subsequent execution evidence, when present in this branch, must be read with its own pinned source and product identities rather than inferred from this paragraph.

## 2. R39-I1: current navigation and one response/evidence entry

Both the root README and this manuscript's README now identify v42 and point directly to the immediately preceding v41 report, this response, and the current verification ledger. The stable historical `A2-v17` directory name is explained. The new revision branch is stated explicitly. The previous root and manuscript README bytes are preserved in `history/v41-review-baseline`, so correcting navigation does not erase the historical record.

This closes the concrete stale-v38 navigation defect in the revised source. Historical verification results retain their original dates and scope; none is presented as a fresh v42 execution. A current source version and a completed delivery certificate remain distinct assertions.

## 3. Relative nonlinear boundary law and the finite smooth-jet inverse

The referee's substantive analytic distinction is retained. The forward result is relative to the exponentially small physical twist, and its proof uses a weighted Dirichlet inverse, summable Hessian perturbations in trace norm, separated endpoint layers and differentiated fixed-domain integration. An absolute error divided by an exponentially small quantity is not substituted for this argument.

The all-order contact inverse continues to depend on finite-truncation envelope differentiation and finite smooth-remainder estimates before homogeneous degree isolation. Its determinant-one two-by-two blocks are the final explicit inversion, not a replacement for the analytic filtration proof. The results concern every prescribed finite order, with order-dependent constants, and do not assert a bounded inverse on an unrestricted infinite-jet space. Smooth boundaries differing by flat terms remain covered by finite-jet factorization; identification of complete boundary images continues to use analyticity.

The v41 introduction and proof-architecture section, including these distinctions, are retained. Neither the common collar nor the mixed geometric derivative convention is weakened. Geometric differentiation remains channel-centered with physical time `t = j g(xi) + d`.

## 4. Single-offset inversion and common-frame global reconstruction

The complete single-offset chapter is retained as `article/23f_single_offset_law_inverse_v42.tex`, with its predecessor left at its original path. The four-density identity, positive fixed-anchor construction, amplitude recovery, interior fixed-order stability, finite-flight error bound and leading curvature inversion are unchanged. A programmatic comparison of theorem, proposition and corollary environments confirms that all their statement bytes agree with the predecessor.

The mathematical change is in the detailed proof of `thm:v26-single-offset-global`. The v41 introduction already invoked the historical rerooting lemma; the present revision integrates the same argument directly into the detailed composition:

1. Fix the common starting frame of the rank-two anchoring pair and choose an incident obstacle orbit. A signature-rigid anchoring incidence supplies a unique complete framed curvature signature.
2. Apply `lem:v40-signature-rigid-rerooting` to the supplied tree. This changes only its root and edge orientations, not its channels, labels, deck displacements or observation data.
3. Recover both cycle holonomies in that frame and set `L = V M^{-1}`. The lattice and its Gram form are thereby fixed in the same gauge as the root obstacle.
4. Propagate along the rerooted tree using unique framed-signature matching. Compare two admissible realizations after aligning their starting frames: their holonomies, lattice and successive child placements agree. The common lattice then identifies all translates.

The proof explicitly separates uniqueness from existence and admissibility, which follow from the realizability hypothesis. It does not assume that matrix inversion places obstacles outside the anchoring cycles. No additional registration assumption is inserted. This is an integration and expansion of the existing v40/v41 proof chain, not a claim that the referee overlooked a new fatal counterexample or that a new observation model has been solved.

## 5. Physical acquisition and the richer position benchmark

The charged calibration pilot, its selection at the final even flight number, the fresh post-pilot tests, and the deterministic preparation caps are retained. Unknown contact coordinates occur only in analytical comparisons, not as unobserved inputs to an acquisition kernel. Every failed preparation remains charged.

The same-experiment direct-position benchmark remains in the manuscript. The intrinsic inverse from two signed transverse laws is not replaced by it or declared statistically equivalent to noiseless graph sampling. The observed-contact-type deficiency distinction remains intact. The global conclusion continues to concern its specified compact marked analytic class with persistent channels and unique signature matching, while the local forward construction retains its more general smooth geometric setting.

## 6. Compact local experiments, contiguity and unbounded loss

The native inputs for finite likelihood-vector convergence, likelihood normalization and uniform integrability, the moving-boundary modulus and the finite-net upgrade remain in place. Thus compact-parameter Le Cam convergence is not inferred from a pointwise LAN display. The noncircular contiguity argument and original-alternative fourth-moment estimates are retained separately; total variation alone is not used to transfer quadratic losses.

The common-collar reference-dominated representative remains distinct from common domination of the original scalar and finite-strip Poisson families. The two actual Poisson comparison kernels and their layer, bulk and corner estimates are retained. Waiting-count information and the endpoint-only coarsening continue to refer to their declared record spaces, not the complete growing collision array.

## 7. Literature comparison, significance and article form

The corrected v41 comparison with Florio–Leguil retains the revised smooth-conjugacy statement and does not restore the withdrawn spectral-rigidity assertion. The distinctions among marked length spectra, enriched marked length data and intrinsic channel-law data remain explicit. No reduction between those observation maps is asserted without a proof.

The article continues to organize its principal contribution around the nonlinear relative law and its composition with the all-order signed contact inverse. The elementary amplitude cancellation and lattice matrix formula are not promoted as substitutes for that work. The report's significance reservation is an editorial judgment, not answered by inflating a diagnostic count or inventing an unsupported stronger theorem. The complete theorem–proof exposition, comparisons, physical consequences and auxiliary derivations remain included. Repository provenance and response records remain outside the mathematical article except for the existing attribution acknowledgment.

## 8. Preservation and verification boundary

[Preservation and dependencies](PRESERVATION_AND_DEPENDENCIES_V42.md) records the exact predecessor identities and the narrow mathematical delta. The main still has 54 literal direct inputs, including preamble and bibliography; its auxiliary compendium still has all 36 inputs. No historical derivation, previous referee report, A1 material, or other programme workstream is deleted.

The latest report's bounded positive findings are not converted into a new universal certification of every retained dependency. New source comparisons, actual executions and any PDF inspection must be distinguished from inherited findings in the current ledger. This revision is submitted for another independent examination of the complete source and its stated evidence.
