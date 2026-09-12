# A2 v28 active source and preservation manifest

Date: September 12, 2026. Repository: `TrillionniumFoundation/theta-theory`.

Revision branch: `revision/a2-v28-common-orientation-quotient-top4-2026-09-12`.

Review base: `e5a153b1bbb663c4a5e3153c6a7bdedb7fcd5864`, tree `0d04e3ed2e4c9786d096f1aba5c3a22580daec95`.

Mathematical revision: `6d8f158c60f3636c572daa64779f57c9c9ec757b`, tree `768f467572a3a884073e69065d1239825be8f25e`.

The stable paper directory is `papers/A2-v17-boundary-information-coarsening`; its historical directory name is not the current revision number. The complete native entry points remain `main.tex` and `two_collision.tex`. The new revision inherits the entire review-base repository tree, rather than copying only the changed modules.

## Active changes

| Historical source retained | Active source | Exact change |
|---|---|---|
| `article/01b_observation_hierarchy_v23.tex` | `article/01b_observation_hierarchy_v28.tex` | Retain the entire old hierarchy; add the common-orientation distinction |
| `article/23b_intrinsic_multichannel_rigidity_v23.tex` | `article/23b_intrinsic_multichannel_rigidity_v28.tex` | Replace only the ambiguous final orientation sentence; preserve all sixteen labels and all other mathematics |
| No replacement | `article/23h_global_orientation_quotient_v28.tex` | Define the marked law-valued quotient and prove reflection equivariance, classification and holonomy consequences |
| `main_pre_v28.tex`, copied by the old blob | `main.tex` | Propagate the quotient to the abstract and wire the three modules into the complete manuscript |

The entry has 49 direct inputs instead of 48. There are exactly two versioned replacements and one addition. All other direct input order is unchanged. Inactive old versions are not also compiled into the current manuscript.

## Exact new Git blobs

| Path relative to the paper directory | Git blob |
|---|---|
| `main.tex` | `7f150377c310e8243b0d99bce4a5eab147cea6ac` |
| `article/01b_observation_hierarchy_v28.tex` | `b6b5a739939beab02dfbc9b4e9cb077866366116` |
| `article/23b_intrinsic_multichannel_rigidity_v28.tex` | `7930d5deac7c53c50aef2e90f90aeb426c10a77d` |
| `article/23h_global_orientation_quotient_v28.tex` | `d7181d0ce3e7092227b2ff984dab5a4c3a672650` |
| `tools/check_revision_v28.py` | `8467debd339b36a7c51db0486fb542b28497485b` |
| `diagnostics/v28-finite-checks.json` | `8edbf8a22284816c1dc555c026dd962068fbb3bd` |

The uploaded mathematical blobs match the local bytes used for checking and revised-module typesetting. The active multichannel file has no terminal newline; the resulting one-byte distinction is included in its exact hash and has no mathematical effect.

## Preserved central sources

| Source | Unchanged Git blob |
|---|---|
| Previous `main.tex`, now `main_pre_v28.tex` | `2133039c3a220a923b232db9f1c5a5661938773c` |
| Old intrinsic multichannel section | `0146f25a95d9cdb92cb09f4b6916d4d153cedeaf` |
| Old observation hierarchy | `4b747a51deb4e4bd2def93da7d73d8fd841041f5` |
| `article/23a_signed_endpoint_rigidity_v27.tex` | `0285c90309b8ab88d1ce1ecf8d492ea6d71f268e` |
| `article/18f_domination_and_position_comparison_v27.tex` | `97b115829b5b770c856596bb7c86f3d769483ced` |
| `article/23f_single_offset_law_inverse_v26.tex` | `35f538eea4415951d1572cd9db76fdff429afa0a` |
| `article/23d_rank_two_lattice_recovery_v24.tex` | `5e34a7c034ee8a5de0ae915a2b4c622f0f042b2c` |
| `article/99_auxiliary_compendium_v19.tex` | `a596f344cd660eeaacc8e4e3eb21a0cb39610a9e` |
| `two_collision.tex` | `df44402b17031525c087d39dfedf8dac3ada611d` |
| `preamble.tex` | `7e0de97c08dd2e12187193aff89f3ca4712f430f` |
| `tools/build_submission.py` | `233b6f37ff4912b99793460634983ac9b8da379b` |
| `tools/audit_native_sources_v27.py` | `304a8eb8aed7a2e0ea1ac2944afec1f34ed5e359` |

The complete auxiliary compendium and its 36 direct inputs remain active. The relative laws, weighted half-line construction, finite-jet inverse, analytic continuation, intrinsic gluing, metric-free rank-two lattice recovery, finite-signature stability, finite-flight benchmarks, domination and information comparisons, Abel/deautoconvolution results, charged observable calibration, global reconstruction and variation-bundle results remain in the same native graph. The bibliography `v5/references_v25.tex` is unchanged. No theorem-bearing historical source, companion source, review or bibliography is deleted.

## Navigation archives

The preceding root README is copied to root `README_PRE_V28.md` by exact blob `b288ebb79b8a8151716098165fcf72e5720005a3`. The preceding paper README is copied to paper-local `README_PRE_V28.md` by exact blob `14631c129934331b22f30257e42f2c33c1990002`. Earlier navigation archives, including the statistical A1 and distinct dynamical/mechanical workstreams, remain unchanged.

## Evidence boundary

`diagnostics/audit_changed_sources_v28.py` and its executed JSON verify the copied source identities, the exact sentence replacement, inherited labels and direct-input ordering. This is a changed-source audit, not an executed recursive audit of every inherited native dependency. The retained full native scanner and builder are distinct tools.

The actual complete-native workflow attempt at the mathematical revision failed before any step ran. [VERIFICATION_V28.md](VERIFICATION_V28.md) records that fact and the separate local executions. The existence of this manifest is not a full compilation or reference certificate. Subsequent response/navigation/evidence commits do not change the mathematical source bytes listed above.
