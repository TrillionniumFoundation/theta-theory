# A2 v38 — preservation and native-source comparison

Baseline: v37 review commit `377efa79597776e75e3cc1d399c1986edd097aaf`. Mathematical revision: `c206a27ba01f20f1a21b780e6d71c77a837ef11d`. Source and build tools: `7d34d96a7c2dd974ab3725e009bbb584d3228114`.

Only three native mathematical files change. Every other inherited mathematical source blob, the companion, the preamble, the bibliography and the complete auxiliary compendium are retained. The [JSON comparison](verification/v38/manuscript-preservation.json) records the exact changed-file identities and structural checks.

| Native file | Baseline Git blob | Revised Git blob | Scope of change |
|---|---|---|---|
| `main.tex` | `c67badf42e0e6d1c30c73a54c19918ffe7508621` | `d0f57adda8474428024d587dd102971efd1fae24` | v38 identifiers and anchoring/tree wording in the abstract; all 52 direct inputs unchanged. |
| `article/01_introduction_v27.tex` | `4bf96b3ad9f77c0671a7142e8f4baad3db3f560b` | `aa13f32d24145d40d3f611dfe4083e3fe305e9c6` | Realizability/common-frame anchoring in the introductory theorem and the explicit rooted-propagation proof reference. All 10 labels and both proof blocks retained. |
| `article/18a_vector_boundary_information_v26.tex` | `8ff3ce7334954d6544555e9867a12fa805ca5ea0` | `6db9136e31c0e94bc09eddc5f261eab1b25be3ba` | Only the short bounded-sequence contiguity proof body changes. All 41 labels and eight proof blocks retained. |

The exact baseline files are preserved at [history/v37](history/v37) using their original Git blob identities. The old build driver is also preserved at `history/v37/tools/build_submission.py`, blob `029e9e96537df18a032d36de55e449e262be87c4`. Earlier response and verification files remain historical records; they are not overwritten with new executions.

## Native input chain

The sequence of all 52 direct `main.tex` input commands is unchanged. The auxiliary wrapper `article/99_auxiliary_compendium_v19.tex` remains blob `a596f344cd660eeaacc8e4e3eb21a0cb39610a9e` and retains all 36 input commands. These counts establish preservation of the entry and wrapper text, not availability or successful compilation of every recursive dependency in a local checkout.

In particular the source retains the fixed-collar relative law and differentiated operators; weighted nonlinear half-line inversion, finite-truncation envelope differentiation and finite smooth remainders; signed and odd-order contact jets; amplitude-free single-offset inversion; analytic continuation, intrinsic gluing, common-orientation quotient, lattice metric recovery and signature stability; moving-ceiling layer/bulk/corner comparisons; common domination and reference-domination distinctions; original-alternative moments and unbounded quadratic risk; finite likelihood-vector comparison and the separate compact-uniform passage; count–endpoint information; charged near-onset calibration, single-offset physical reconstruction and the same-experiment direct-position benchmark. The complete auxiliary proofs and earlier mechanical companion remain present.

## Unchanged dependencies singled out by the referee

| Source | Retained Git blob |
|---|---|
| Detailed single-offset composition, `article/23f_single_offset_law_inverse_v26.tex` | `63ed36efd417cd23e6f869952627719de00e6ef7` |
| Rank-two and full-table rigidity, `article/23d_rank_two_lattice_recovery_v24.tex` | `5e34a7c034ee8a5de0ae915a2b4c622f0f042b2c` |
| Detailed normalized likelihood and original-alternative risk, `article/18a2_likelihood_tilting_moments_v34.tex` | `b6f74b4d5cbf6e1065af521dc7364dab98445b38` |
| Native companion, `two_collision.tex` | `df44402b17031525c087d39dfedf8dac3ada611d` |
| Preamble with companion external references, `preamble.tex` | `7e0de97c08dd2e12187193aff89f3ca4712f430f` |

The root and paper navigation are updated with exact predecessor copies at `README_PRE_V38.md`. Statistical A1, dynamical A1, other manuscripts, review branches and the default branch are not changed. No merge, deletion of a workstream, branch-protection change or permission change is part of this revision.
