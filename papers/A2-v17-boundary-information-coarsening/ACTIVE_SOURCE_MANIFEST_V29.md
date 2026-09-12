# A2 v29 — active source and preservation manifest

Mathematical source commit: `78852f2ccf828385fd45063c1b58c0d474ddf6c5`.  
Initial mathematical commit: `e468c075b0e57e015e774829f5886ce2322e6c02`.  
Review parent: `5f10927a6399ebec0492b7f87b622ec80a4df631`.  
Branch: `revision/a2-v29-equivariant-density-stability-top4-2026-09-12`.

The stable manuscript directory retains its historical v17 name. `main.tex` is the complete current native entry, not a shortened compilation fixture. It has 50 direct inputs, including the preamble. The companion is `two_collision.tex`. The complete 36-input auxiliary compendium and bibliography are retained.

## Active mathematical changes

| Path | Git blob |
|---|---|
| `main.tex` | `e8cea2c2b136624c61fa3d3c4629965e31321613` |
| `article/01b_observation_hierarchy_v29.tex` | `9ff3141c19ec00b669667c0a9226138a2698d234` |
| `article/23f1_equivariant_density_extension_v29.tex` | `f90531eae71f43486029a7dd042c249627aa22b8` |
| `article/23h_global_orientation_quotient_v29.tex` | `ac9938ee655b8b63f069a0c79c467d227eca5ab1` |

The two versioned substitutions replace the v28 hierarchy and orientation inputs; the added subsection follows the unchanged v26 single-offset inverse. Every other input keeps its order. The inherited abstract is byte-identical. The old versions remain in the repository.

## Selected unchanged dependencies

| Path | Git blob |
|---|---|
| `article/23f_single_offset_law_inverse_v26.tex` | `35f538eea4415951d1572cd9db76fdff429afa0a` |
| `article/23a_signed_endpoint_rigidity_v27.tex` | `0285c90309b8ab88d1ce1ecf8d492ea6d71f268e` |
| `article/18f_domination_and_position_comparison_v27.tex` | `97b115829b5b770c856596bb7c86f3d769483ced` |
| `article/23b_intrinsic_multichannel_rigidity_v28.tex` | `7930d5deac7c53c50aef2e90f90aeb426c10a77d` |
| `article/99_auxiliary_compendium_v19.tex` | `a596f344cd660eeaacc8e4e3eb21a0cb39610a9e` |
| `preamble.tex` | `7e0de97c08dd2e12187193aff89f3ca4712f430f` |
| `two_collision.tex` | `df44402b17031525c087d39dfedf8dac3ada611d` |

The exact orientation classification prefix, folded-record remark and all its labels are preserved in the active v29 copy. Its stability corollary is explicitly qualified by the exact image and the new transported-anchor extension.

## Exact archives

`main_pre_v29.tex` retains blob `7f150377c310e8243b0d99bce4a5eab147cea6ac`; the paper navigation archive retains `3edfc32ff84cd7b4ea59ceb45dfb88ad06e5da82`; the root navigation archive retains `66ac472cdf9c3aa71bec847482b70976acbee69b`. No inherited path was removed when the mathematical tree was created.

## Reproducible checks and their scope

`tools/check_revision_v29.py` has blob `bd27b08638c9ca2d92f77eb848ac69d24f18fd1f`. Its ordinary and optimized outputs are byte-identical. The executed changed-source audit, with SHA-256 and Git-blob identities and the full direct-input list, is [diagnostics/v29-changed-source-audit.json](diagnostics/v29-changed-source-audit.json).

`tools/check_preservation_v29.py` checks the whole Git tree against the pinned review base when run in a full checkout. The GitHub commit comparison independently showed no removals. The existing recursive native scanner and complete native builder are retained, and the new bounded workflow invokes them on a full checkout.

This manifest is not a claim that the complete native main closure was materialized and compiled locally. Complete native companion verification and the separately limited module fixture are described in [VERIFICATION_V29.md](VERIFICATION_V29.md). C2 remains open for the complete main submission package. Later navigation/evidence-only commits must leave the mathematical source blobs above unchanged.
