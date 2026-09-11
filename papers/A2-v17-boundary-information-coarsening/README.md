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
