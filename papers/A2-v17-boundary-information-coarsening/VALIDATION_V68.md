# A2 v68 — validation design and scope

The mathematical revision is in `article/10d_smooth_contact_rigidity_v68.tex` and its integrated statements. Proofs, not finite tests, establish the asserted general conclusions. The following executable checks support source preservation and error detection. Completed run identities, native file hashes, page counts and observed diagnostics are recorded in the final versioned delivery/review-ready record outside the frozen manuscript tree.

## Source preservation

`tools/check_revision_v68.py` checks every one of the 855 inherited file records, using the exact archived original for each of the nine edited files and the active path for every other inherited file. It checks lengths, SHA-256, Git blob identity and retention of original labels in edited TeX files. Working-tree modes are checked directly; the build engine deliberately makes frozen copies read-only, and their original Git modes are verified through the frozen manifests and the materialization tree identity. It reconstructs old and new active input graphs and requires the only added active path to be the new smooth-contact proof section. It checks the presence of the v67 complete stopping formulas. It neither deletes inherited files nor rewrites previous reports.

## Mathematical diagnostics

The new standard-library diagnostic uses exact rational arithmetic for weighted-tail thresholds, signed cyclic operator inverses, finite nonlinear composition samples and their weighted tails, polynomial jet alignment, the two-offset normalization algebra, and elementary bounds entering the flat asymptotic. The derivative polynomial recurrence for `exp(-1/u^2)` is checked algebraically. A negative control explains why `C rho^j` with `C rho>1` cannot alone justify the large-weight argument.

The v67 pure mathematical control routine is explicitly reused to retain its quadratic, residual, inexact-evaluation, cubic and noncommutative finite-jet bounds. Its old source-preservation routine is not reused: revision 68 has its own correct baseline. This reuse is not described as an independent referee computation. Normal and optimized Python executions must produce identical JSON.

These finite checks are not global billiard realizations and do not certify the actual smooth half-line construction, infinite envelope, smooth functional uniqueness, trace-class limit, analytic Banach inverse, global continuation or statistical catalogue. Those require mathematical review of the indicated proofs. In particular, testing a finite composition model cannot replace the uniqueness argument that gives shift-covariance for the actual billiard half-line.

## Build and delivery

`tools/build_revision_v68.py` reuses the retained frozen-Git build engine. It compiles the companion, full manuscript and principal article from a complete committed source snapshot, with shell escape disabled and regenerated auxiliaries. The engine verifies active inputs, source manifests, recorder files and the required producer/consumer auxiliary identities. It runs the established finite-chain diagnostics and the new version-scoped checker.

`tools/retain_native_v68.py` retains all three complete PDFs, frozen source ZIP, source/input manifests, diagnostics and native logs in a commit-scoped repository directory. It checks indexed products, then checks fetched committed objects and writes the publication attestation. A completed workflow is not claimed by this design document; actual completion is recorded separately after execution.

Visual examination is reported only for pages actually rendered and inspected. All-page text or pixel parity, when recorded, is a mechanical comparison and not all-page proof review or all-page visual inspection. PDF bytes may differ between toolchains even when contents agree. No font files are included in the delivered source archive.
