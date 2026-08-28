# Round306B1AF4K2I0 R292 identity/representation partial lane

## Verdict

`PASS_INDEPENDENT_COLD_REPLAY_PARTIAL_R292_IDENTITY_OWNER_INDEX__ZERO_THEOREM_CREDIT`

This package is a strict, executable **partial R292 lane**. It is not the
six-family completion promised by the filename prefix, and it is not a
normalized-support theorem or representation-cover theorem. Five coarse
families remain absent.

## Exact closed census

- R292 member identities joined through R292 → R294 → B0: **9,404**.
- Uncovered exact `(t^2,p,s)` representation cells: **10,252**.
- One unsigned-bytewise-ASCII minimum primary per component: **9,404**.
- Remaining component cells indexed as `REFINED_PRIMARY_EXTRA`: **848**.
- Occupied exact cells back-bound through R294 to preserved owners: **1,600**.
- Fixed-sign `t = sigma*sqrt(u)`, `u = t^2` obligations enumerated: **11,852**.

The component-size histogram is `1:9124, 2:80, 3:12, 4:88, 5:84,
10:16`. All component/cell, component/registry, registry/B0,
occupied-cell/alias, output missing, orphan, and duplicate anti-joins are zero.

## Reproducibility and hardening

- Producer SHA-256:
  `035629dda904aae42f877e5425dc17c8500ff3e33b837ecdf8142e0b264233b5`
  (`37,543` bytes).
- Independent verifier SHA-256:
  `ae1c11bca4203f4828ea0284aa1a1e0a535c5a3bdbdb846e8777bc7567d7ffbc`
  (`40,978` bytes). It does not import or execute the producer.
- Hash seeds `17` and `91` produced byte-identical copies of all four
  ledgers and the result marker (`5/5` files).
- Final fixed producer replay: rc `0`, wall `151.30 s`, peak RSS
  `95,452 KiB`.
- Final type-strict independent cold replay: rc `0`, wall `156.52 s`, peak
  RSS `65,236 KiB`.
- The verifier rejects bool/int aliases recursively. Its self-test rejected
  `7/7` explicit alias mutations, covering result credit, all four ledger
  credit shapes, and count `True == 1`.
- Inputs are held by FD, byte-pinned in two passes, and finally rebound to
  their regular single-link path. Decoded source slices and successful
  canonical rows are capped at 8 MiB. Scratch is explicitly rooted at a held
  `/tmp` dirfd outside `deliverables`; publication uses held dirfds and the
  result marker is published last.

## Byte commitments

- Member index: `feae99820c48576261aa8326ea51388d149637e30538afcdeb8b3c2c6dec4459`
  (`9,404` rows; `3,463,003` bytes gzip).
- New-component representation index:
  `5a560e16e793dd2e2a2b91a860ee6294463424307b406df6ba070b47d27c221b`
  (`10,252` rows; `2,534,453` bytes gzip).
- Preserved-owner alias index:
  `cd42c63b845042e442d921bd19fa02314a71c9be54a45eae1f3b0156f5fac416`
  (`1,600` rows; `388,633` bytes gzip).
- Fixed-sign obligation index:
  `97bf1b0cf31c80d559da37238e5d582d1d49f43ebcebda5a00ffea56fc1f2746`
  (`11,852` rows; `2,542,608` bytes gzip).
- Result marker:
  `ac88dd5157de65f82cba7478e62e7cd45df122b2548923bb799e4c059765f5af`.
- Independent verification:
  `325f8b38f91f572def4cf6c9f9c9aca78f4a03bb926c2e8454b0e4ed1a4d7901`.

## Explicit non-credit and remaining gaps

Every output row is only `IDENTITY_JOINED`, `OWNER_INDEXED`, or
`OBLIGATION_ENUMERATED_NOT_DISCHARGED`. The exact transformed open cell and
source-row SHA are carried for recovery, but authoritative sigma/branch data
and fixed-sign pullback proofs remain missing for all `11,852` cells. The 848
physical-face/Kruskal semantic obligations remain undischarged.

Still absent from K2I0:

- `PRESERVED`, `NON_GRAPH`, `R2`, `G2A`, and `G2B` identity lanes;
- `555,088` remaining member-index rows;
- `600,052` remaining global representation rows;
- the `80,092` A1/A2 obligation enumeration;
- any normalized-support, representation-cover, A1/A2 theorem, B1A, B2,
  maximality, fibre, global-disposition, D02/D03/D04, Gate5, or CM2 credit.

All those credits remain exactly zero.

## Cold-replay commands

```text
python3 cm2_round306b1af4k2i0_source_g_six_family_identity_representation_index_producer.py --produce --output-directory deliverables --hash-seed 17
python3 cm2_round306b1af4k2i0_source_g_six_family_identity_representation_index_producer.py --produce --output-directory /tmp/<held-seed91-output> --hash-seed 91
python3 cm2_round306b1af4k2i0_source_g_six_family_identity_representation_index_independent_verifier.py --verify
```

