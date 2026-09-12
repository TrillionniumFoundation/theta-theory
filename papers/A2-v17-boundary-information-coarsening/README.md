# A2 v25 — observable calibration, intrinsic rigidity and global reconstruction

**Boundary laws, intrinsic periodic rigidity, and global physical reconstruction in dispersing billiards**  
Qian Qi · Complete English author revision · September 12, 2026

Revision branch: `revision/a2-v25-observable-calibration-signature-top4-2026-09-12`.  
Reviewed v24 manuscript: `c35b31b1924a1621374eab72ee60e4cb5ab37df5`.  
Latest located v24 report and addendum: `8129defd970bbc1e011bb480b70603d39a31324d`.

[Complete native article](main.tex) · [Point-by-point response](RESPONSE_TO_REFEREE_V25.md) · [Active source and preservation manifest](ACTIVE_SOURCE_MANIFEST_V25.md) · [Executed verification and limitations](VERIFICATION_V25.md) · [Finite diagnostic output](diagnostics/v25-finite-checks.json) · [Referee report](../../reviews/a2-v24-external-harsh-top4-2026-09-12/REFEREE_REPORT.md)

## Current mathematical revision

The common global observation now records both components of endpoint positions in an independently placed sensor frame for each channel, with the same sensor frame shared by that channel's two endpoint types. No contact point, tangent, gap, inter-channel registration or lattice metric is supplied. A capped near-onset scan using long even same-type bridges estimates the within-channel contact frame and onset. The global estimator then uses a finite library of **mixed gap and conditional-law** coordinates. Every preparation is charged, and the final flight number is fixed before pilot precision is chosen.

Finite analytic signatures are selected with a proved local embedding bound as well as a global exclusion margin. A separate strict-convexity argument proves unique noisy least-squares matching under the stated signature-curve perturbation bounds. The compact inverse modulus is proved independently from exact full-data injectivity. The local finite-positive-design statement is now based on a constructed compatible analytic Hermite-variation bundle, not a claim that the entire compact analytic class is finite dimensional.

The retained Poisson equivalence has explicit parameter-independent kernels in both directions, an explicit bulk relative-density bound and corner conventions, with the density notation corrected. The one-flight signed-support inverse is included as a direct benchmark. The global theorem is formulated so that every used flight number is even and its minimum can tend to infinity; it does not rely on that short-flight benchmark.

The signed all-order contact inverse, metric-free rank-two lattice recovery, analytic gluing classification, count quotient, local Gaussian/Poisson hierarchy and complete auxiliary derivations remain active. The anchored scalar local information experiment is distinguished from the global two-dimensional position-sensor acquisition; its information limit is not claimed to exhaust that richer sensor record.

## Build and review status

337 finite diagnostics were executed in ordinary and optimized Python with byte-identical output. The executed script's blob hash agrees with the committed script. This is **not** a certified complete native article build or a proof-assistant verification.

The first hosted native-build job failed before running any steps. The exact-head workflow has been routed to the repository's existing self-hosted Linux x64 runner labels. A queued or unexecuted workflow is not counted as a successful build. `VERIFICATION_V25.md` records the evidence and the remaining native-execution requirement.

From a complete repository checkout:

```sh
python3 papers/A2-v17-boundary-information-coarsening/tools/check_revision_v25.py
python3 -O papers/A2-v17-boundary-information-coarsening/tools/check_revision_v25.py
python3 papers/A2-v17-boundary-information-coarsening/tools/build_submission.py \
  --output-dir /absolute/path/outside/the/manuscript/tree
```

The native build covers both `main.tex` and `two_collision.tex`, all active appendices and the bibliography. The v17 directory name is retained for source stability; it does not identify the current version. This revision is for independent re-review, not a journal acceptance decision, and is not merged into `main`.

---

# Historical v20 index — not the current revision

The following earlier index is retained for provenance. Its scope and verification claims concern v20, not v25.

# A2 v20 — signed rigidity and a fixed-window physical local experiment

**Boundary laws, signed contact rigidity, and physical information in dispersing billiards**  
Qian Qi · English manuscript · September 11, 2026

Revision branch: `revision/a2-v20-raw-physical-multirate-lan-2026-09-11`  
Review base: `review/a2-v19-independent-harsh-top4-2026-09-11`  
Review commit at branch creation: `f394a2822e748c3a40c1b1718c6afeb91bde0677`

[Article entry point](main.tex) · [Active source manifest](ACTIVE_SOURCE_MANIFEST_V20.md) · [Response to v19 referee](RESPONSE_TO_REFEREE_V20.md) · [Proof ledger](PROOF_LEDGER_V20.md) · [Historical derivation audit](HISTORICAL_DERIVATION_AUDIT_V20.md) · [Literature audit](LITERATURE_VERIFICATION_V20.md)

## What v20 changes

The v19 referee accepted the signed-endpoint inverse as a genuine strengthening and found the abstract vector boundary-LAN theorem internally consistent. The decisive objections concerned the physical realization: v19 used parameter-dependent centered time/contact coordinates for an unknown-geometry claim, did not include the separate gap/onset direction in the information-kernel proof, and stated the finite-bridge transfer below experiment level.

V20 closes those points without weakening the geometric theorem.

### Fixed physical windows and a multirate gap coordinate

For a specified reference registered channel, the experiment is programmed at physical times

` t_{j,l} = j g_0 + d_l `.

The local unknown geometry is

` g = g_0 + delta_n a / j_n`,  `vartheta = delta_n h`.

Hence the raw fixed-window excess is `d_l-delta_n a`. The gap therefore contributes a constant normal support velocity to the same endpoint moving-support likelihood as the contact-shape directions. The finite-design information kernel is trivial on the full coordinate `(gap, finite labelled contact jets)`, so finitely many positive same-type windows have a positive-definite summed information matrix.

### Self-contained vector boundary LAN

`article/18a_vector_boundary_information_v20.tex` now states and proves the vector collar moments, truncated-score centering, uniform compact-set likelihood expansion, central-sequence CLT, quadratic-term concentration, Gaussian testing profile and local asymptotic minimax theorem explicitly.

The central-sequence estimator is described precisely as a local estimator around a specified reference parameter, not as a global unknown-table procedure.

### Uniform finite-bridge experiment transfer

The actual physical policy uses deterministic preparation caps and stops each batch at its target success count or its cap. The complete stopped transcript retains failures, successes, designs and stopping times. For compact local parameter sets,

`sup ||P_fin - Q_boundary||_TV <= C k_n tau^{j_n}`.

Thus `k_n tau^{j_n} -> 0` gives experiment-level transfer. The endpoint-output coarsening inherits the LAN theorem, while every failed preparation remains charged. Waiting counts are not declared ancillary; a richer transcript can contain additional faster information.

### Charged pilot route to centered windows

The historical self-calibration theorem is now propagated through the boundary Hellinger scale. If the pilot gap error satisfies the printed `k_n r_n^{2m+2} log(1/r_n) -> 0` condition, post-pilot windows `j_n g_hat+d_l` are asymptotically equivalent to oracle centered windows. The pilot preparation cost remains explicit.

## Signed rigidity retained

V20 keeps the v19 signed endpoint theorem unchanged: support thresholds recover the unsymmetrized half-line actions; onset and the quadratic action terms recover both contact curvatures; arbitrary odd/even labelled graph jets enter through the determinant-one `coth/csch` block and are recursively recovered. Analytic endpoint-law germs determine the participating analytic contact germs.

## Scope

The principal statistical theorem is local around a specified **registered labelled channel**. The gap and participating contact geometry are unknown. Absolute Euclidean pose, label exchange and an unknown construction of the endpoint frames are calibration/nuisance quantities, not silently included statistical coordinates. If registration itself is unknown, the manuscript states the Hellinger scale required of a pilot rather than treating it as free.

One selected channel does not recover unrelated obstacles. The introduction compares the endpoint information set directly with modern marked-length/enriched-length rigidity rather than claiming global dominance.

## Reproduction and verification

From a complete checkout, the native route remains

```sh
python3 tools/build_submission.py --output-dir /absolute/path/outside/this/directory
python3 tools/check_boundary_information.py
python3 -O tools/check_boundary_information.py
```

`VERIFICATION_V20.json` is authoritative only for checks actually executed at the final v20 source head. A workflow that fails before runner steps is not counted as a successful build.

## Preservation

No reviewed v19 mathematical source is deleted. The historical v19 vector source remains in the tree, the auxiliary compendium remains available, and Git history preserves every predecessor. V20 changes the active theorem hierarchy and physical statistical formulation rather than shrinking the paper.
