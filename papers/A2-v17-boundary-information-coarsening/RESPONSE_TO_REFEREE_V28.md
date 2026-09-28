# Response to the referee on A2 v27

**Manuscript:** *Boundary laws, intrinsic periodic rigidity, and global physical reconstruction in dispersing billiards*  
**Author:** Qian Qi  
**Revision:** v28, September 12, 2026  
**Branch:** `revision/a2-v28-common-orientation-quotient-top4-2026-09-12`  
**Addressed review head:** `e5a153b1bbb663c4a5e3153c6a7bdedb7fcd5864`  
**Mathematical revision:** `6d8f158c60f3636c572daa64779f57c9c9ec757b`

We thank the referee for distinguishing the two repaired mathematical objections from the remaining bounded requests. The report closes the observed-contact objection and the arbitrary-smooth-remainder objection in the inspected v27 proofs. It requests a precise common-orientation quotient (C1) and an actually executed complete native submission (C2). This response follows that distinction. The signed inverse, physical information results, analytic reconstruction, companion manuscript and auxiliary derivations have not been replaced by a narrower problem.

The report is preserved at `reviews/a2-v27-external-harsh-top4-2026-09-12/REFEREE_REPORT.md`. The current full source entry is [main.tex](main.tex); the companion remains [two_collision.tex](two_collision.tex). Revision records are separate from the mathematical article.

## C1. The orientation quotient

**Referee request.** Define a single global orientation action on the complete signed datum and prove its Euclidean quotient classification. Do not identify it with pointwise absolute values or independent sign erasure in separate channels.

**Response.** The active classification theorem now explicitly refers to a common-orientation orbit and its proof. The ambiguous sentence has been replaced in `article/23b_intrinsic_multichannel_rigidity_v28.tex`, at `thm:v23-intrinsic-table-rigidity`. The entire inherited section, including its signed classification proof, cycle-holonomy argument, spanning-tree reconstruction and all sixteen labels, is otherwise preserved. The old source remains in the tree.

The new subsection `article/23h_global_orientation_quotient_v28.tex` supplies the following complete argument.

### Data and the marked lattice convention

Definition `def:v28-common-orientation-datum` applies the same endpoint reversal `r(u,v)=(-u,-v)` to every edge, contact type and retained offset. Obstacle labels, directed channels, deck elements and onset gaps do not change. Reversing a directed edge is a different operation. Residual-time coordinates, counts and failure atoms are not discarded by this convention change.

There is an additional bookkeeping issue in the inherited formulation: its lattice realization is orientation-preserving. Reflection moves it to the opposite orientation sector. We therefore write the complete convention as `(epsilon,D)`, with `epsilon` the orientation character relative to the marked basis, and define

`R(epsilon,D)=(-epsilon,R_0 D)`.

The unoriented datum is the orbit of this one involution. The orientation character is transported with all transverse signs; it is not independently erased, and it is not a supplied angle, root placement or inter-channel registration. The original signed theorem is exactly its positive sector. Its incidence-equation proof applies equally in the negative sector. This makes the improper Euclidean action an actual action on the stated realization space rather than an operation silently leaving the admissible orientation class.

### Equivariance and the classification proof

Lemma `lem:v28-reflection-equivariance` uses `J(x,y)=(x,-y)` and proves the representative transformation

`(iota,(A_e),(C_e)) -> (J iota,(J A_e J),(J C_e))`.

Reflection preserves the physical flight geometry and collision flux. The action and contact coefficients transform as `S_b^r(u)=S_b(-u)` and `q_{b,n}^r=(-1)^n q_{b,n}`; the proof does not equate a smooth function with an infinite Taylor series. The displayed incidence identity proves that all deck-corrected gluings remain consistent. Disjointness, facing contacts and admissibility are preserved, and conjugating a proper global change of representative proves well-definedness on signed gluing classes.

Theorem `thm:v28-unoriented-classification` identifies realizing marked tables modulo one common element of `E(2)` with the quotient of the two corresponding signed gluing spaces by this involution. Its proof gives both directions: a proper motion acts within one signed class; an improper motion is `B J` with `B` proper and interchanges the two coherent representatives. A signed singleton therefore gives an unoriented singleton. The same conclusion applies when the signed inverse uses one positive offset per contact type.

Corollary `cor:v28-quotient-holonomy-stability` records the consequences for the rest of the reconstruction. Odd curvature-signature derivatives change sign, incidence matches remain unique, and cycle holonomies are conjugated by `J`. With marked cycle columns `M` and holonomy columns `V`, one has `V^r=JV`, `L^r=JL` for `L=VM^{-1}`, and an unchanged Gram form. Fixed-order estimates descend under reflection-invariant orbit metrics for the representative pairs covered by the signed estimates; sectorwise estimates use same-sector comparisons. No order-independent continuation condition number is asserted.

### What this datum does not mean

Remark `rem:v28-folded-records` displays the four-term density of the observation `(|u|,|v|)` and distinguishes it from an orbit of the complete law. It also distinguishes samplewise simultaneous-reversal quotients, random symmetrization, and independent channel reversals. Two positive exchange-symmetric densities with the same folded law but different complete-law reversal orbits illustrate the distinction. They are explicitly a density-class example, not a claimed pair of physical billiard tables.

The abstract and `article/01b_observation_hierarchy_v28.tex` propagate this distinction. We neither invoke the signed inverse as an inverse of folded data nor infer a physical nonidentifiability result without a realizing construction. C1 is thus addressed in the active statement, definitions and proof, not only in this letter.

## C2. Complete native submission validation

**Referee request.** Supply an immutable-source complete build of both entry points, recursive reference/citation verification, native logs and engine versions, complete PDFs with hashes/page metadata, and layout inspection. A revised-module fixture or an unexecuted script is not sufficient.

**Response and present status.** We agree with this requirement and do not mark it closed. The new complete-native workflow was actually triggered at mathematical commit `6d8f158c60f3636c572daa64779f57c9c9ec757b`. Run `34677164341`, job `103508962672`, completed with `failure` and `steps=[]`, `runner_id=0`, and an empty runner name. The job executed neither checkout nor any audit or TeX command. These observations were read from the live run and jobs responses; no account or scheduling cause was established. This is not a failed TeX compilation, and it supplies no successful full-native certificate.

The workflow retains both native entry points and the full auxiliary input graph. It archives the source commit before compilation, runs v27/v28 diagnostics in ordinary and optimized Python, invokes the existing recursive native audit including companion references, builds the companion before the main article, and records versions, logs, PDFs, metadata and hashes. Those are executable requirements, not results claimed from the existence of the workflow.

We separately executed 883 exact finite orientation diagnostics and a changed-source preservation audit in ordinary and optimized Python, obtaining byte-identical outputs. A local eight-page revised-module typesetting fixture was compiled for three pdfLaTeX passes and its new proof pages visually inspected. It has no overfull boxes, missing-glyph or duplicate-label messages, but has ten unresolved-reference occurrences involving eight inherited labels not loaded in the fixture. These are explicitly not a complete native build or full reference audit. Details and reproducible commands are in [VERIFICATION_V28.md](VERIFICATION_V28.md).

A functioning full checkout/build execution, locally or on another runner, remains necessary to close C2. No shortened manuscript, artificial reference labels or deleted auxiliary mathematics has been substituted for that execution.

## Preservation of the repaired results and historical derivations

The v27 observed-type dichotomy and the functional interpolation/envelope proof for finite smooth remainders remain active and byte-unchanged. The same is true of the single-offset density inverse, rank-two lattice recovery, signature stability, boundary-information results and global charged physical reconstruction. The companion and the complete auxiliary compendium remain in the current native source graph. The main entry has 49 direct inputs rather than 48: precisely two versioned replacements and one added orientation subsection, with the remaining order preserved.

The previous main entry is archived by its exact Git blob as `main_pre_v28.tex`. Both preceding mathematical sections and all prior reports remain available. The [active source manifest](ACTIVE_SOURCE_MANIFEST_V28.md) and [historical derivation audit](HISTORICAL_DERIVATION_AUDIT_V28.md) identify the lineage and the material actually inspected. Preservation and finite diagnostics are not a claim to have independently recertified every inherited theorem.

This is an author revision for further independent assessment. C1 has a supplied mathematical resolution; C2 remains a specifically identified submission-validation requirement. Neither statement is a journal acceptance decision or a certificate of priority or exceptional significance.
