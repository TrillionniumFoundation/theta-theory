# A2 v32 source preservation and active graph

Review parent: `9edd5f48d91b74d09718149de6e2c3550c375f20`. Reviewed source: `e1f6304f6069869ac323e7d1a634a619faa4bc32`. Mathematical commit: `35fd4ccef1b5785692de512635f7240a4df0d641`.

The mathematical commit changes the native main and adds two active sections plus an exact copy of the previous main. It deletes no path. All other inherited mathematical files, the companion, the 36-input auxiliary compendium, bibliography and review reports are retained. The later integration commit changes navigation and build tooling, not those mathematical dependencies.

## Exact preserved Git blobs

| Source | Preserved path | Git blob SHA-1 |
|---|---|---|
| v31 native main | `main_pre_v32.tex` | `408a9a0fb6c317ea9c080027283c69a50d5b19dd` |
| Previous root README | repository-root `README_PRE_V32.md` | `eda66be0234cc6c5677c60e8e9878887dc13f103` |
| Previous paper README | `README_PRE_V32.md` | `b5e5e81b8e7ad9e11f9c86427c7d9b363a96fbe6` |
| Previous native builder | `tools/build_submission_pre_v32.py` | `233b6f37ff4912b99793460634983ac9b8da379b` |
| Original count chapter, retained in place | `article/18d_count_endpoint_multirate_v23.tex` | `04637efc790ace6dba7c9128b89d7f13c4cbb985` |

## Active mathematical replacement

The main adds `article/18a1_compact_experiments_v32.tex` after the fixed-window endpoint chapter. It substitutes `article/18d_count_endpoint_multirate_v32.tex` for the old count chapter; the old file remains available for comparison and is not simultaneously compiled with the same labels. Every other direct scientific input is unchanged.

| New active file | Bytes | Git blob SHA-1 | SHA-256 |
|---|---:|---|---|
| `article/18a1_compact_experiments_v32.tex` | 7110 | `176e2588344ce0646ed47c09c64f371d6d16a045` | `807b162e3f1eec7c8ac3714dd133e11c8b50be5bdd2d20938ef5a7e59af7b36a` |
| `article/18d_count_endpoint_multirate_v32.tex` | 12802 | `8f84b43e8c8634036cb682453b007136d8f6d673` | `f396d5b41641600c6da784300c8105d780cb3952e89ca6cbd9dd3ab158b97ff1` |

The two Git blob identities above were read back from GitHub and matched to the locally syntax-checked sources. The native preamble used for that check has its unchanged repository blob `7e0de97c08dd2e12187193aff89f3ca4712f430f`.

This is a preservation record, not a successful native-build certificate. The full workflow emits a recursive active-source manifest and compiler recorder inputs only when it actually runs. Its exact source SHA and execution outcome belong in `VERIFICATION_V32.md` and the resulting build report.
