# Round301 Source-G legal component DSU application — seal report

## Outcome

Round301 applies every currently sealed legal edge channel to the frozen
expanded occurrence registry and independently replays the same edges in
reverse channel/row order.

- Member universe: **564,492**
- Base roots before Round301: **367,964**
- Sealed legal edge rows applied: **434,606**
- Formal DSU rank reductions: **246,016**
- Post-Round301 components: **121,948**
- Forward/reverse partition equality: **PASS**
- Canonical partition SHA-256:
  `c1ab6beed75d5e7379103975d6a9ac1b1095a3eb24b34c87288782e7c97cfe09`
- Ineligible source-consumption rows audited: **119,844**
- Ineligible rows fed to DSU: **0**
- Final official-key universe: **124**
- Formal component quotient credit: **1**

The result status is:

`PASS_ROUND301_COMPLETE_LEGAL_COMPONENT_DSU__246016_RANK_REDUCTIONS__121948_COMPONENTS__FORWARD_REVERSE_SAME_PARTITION`

## Producer dual-seed replay

The producer was run independently with two distinct CLI seeds:

1. `--seed 301031`
2. `--seed 301977`

Both runs produced the same canonical bytes for all five candidate artifacts
listed below. The producer declares `seed_affects_output=false`.

- Producer:
  `cm2_round301_source_g_legal_component_dsu_application.py`
- Producer SHA-256:
  `4a0513885f21c5544be84964bb0d968ca1b04435aff4bbed36755a1684f3bcd5`

### Frozen five-artifact pins

| Artifact | SHA-256 |
|---|---|
| `cm2_round301_source_g_legal_component_dsu_application_edge_application_ledger.json.gz` | `2597d788dd4459a6e111b49e55300d49ef40258698874911adbefbe74f0142c5` |
| `cm2_round301_source_g_legal_component_dsu_application_member_component_ledger.json.gz` | `88adb1ac6c9ee447fddb2ccd8e657a238827e9b31712d974a2a9abd2a3591b93` |
| `cm2_round301_source_g_legal_component_dsu_application_component_key_incidence_ledger.json.gz` | `95b7ce99f7aabd90b411484ff0cdc15f341bebd28f32f30da4d0e22c4e8b133c` |
| `cm2_round301_source_g_legal_component_dsu_application_ineligible_source_consumption_ledger.json.gz` | `5fbc5a409eccd4e04954c7b63dab6739897efd8d9e327c47045cbfbbbaf7633e` |
| `cm2_round301_source_g_legal_component_dsu_application_result.json` | `aeb7c98be3d8fb6226bc39d5e45379484a3bb5e936a0475777b1d5fc59ab062c` |

The result object's internal self-digest is:
`7bcb973ca1355c46cd8e8afd77b49322b11646606a51442410de9a57bb5903e9`.

## Frozen member universe

| Member kind | Count |
|---|---:|
| `CANDIDATE_NEW_ROUND288_CANONICAL_ATOM` | 295,336 |
| `CANDIDATE_NEW_ROUND292_REFINED_R287_SUPPORT_COMPONENT` | 9,404 |
| `EXPANDED_OCCURRENCE` | 126,468 |
| `VALID_VIRTUAL_STRATUM` | 133,284 |
| **Total** | **564,492** |

All 564,492 members are keyed; no unkeyed member is admitted. The retained
Round266 registry contributes 259,752 members / 63,224 roots, and the
Round294 singleton extension contributes 304,740 members / roots.

## Sealed legal edge channels and DSU accounting

Forward and reverse replays process the same 434,606 legal edge rows. Rank
attribution to an individual channel is order-dependent; the total reduction,
component count, and canonical partition digest are order-independent.

| Channel | Edge rows | Forward rank | Reverse rank |
|---|---:|---:|---:|
| `R297_ORDINARY_FACE` | 330,724 | 221,916 | 221,352 |
| `R296_TRUE_SEAM` | 48,444 | 5,212 | 52 |
| `R299C_SIGNED_FACE` | 25,452 | 4,332 | 7,064 |
| `R300B_COMPLETE_FACE` | 10,416 | 16 | 2,584 |
| `R300C_POSITIVE_VOLUME` | 6,314 | 5,890 | 5,752 |
| `R300E_HALF_OPEN_OWNER` | 12,992 | 8,476 | 8,948 |
| `R300F_R245_HALF_OPEN_OWNER` | 264 | 174 | 264 |
| **Total** | **434,606** | **246,016** | **246,016** |

Both traversals end at **121,948** components and the same partition pin:
`c1ab6beed75d5e7379103975d6a9ac1b1095a3eb24b34c87288782e7c97cfe09`.

## Ineligible source-consumption closure

The dedicated ledger contains **119,844** rows:

| Ineligible source class | Rows |
|---|---:|
| R300D canonical incidence pairs | 111,524 |
| R300D single-target assignment exclusions | 1,600 |
| R300A canonical closure pairs | 3,232 |
| R300A source expansions | 3,488 |
| **Total** | **119,844** |

Every row is consumed for audit/disposition only; **zero** of these rows is an
input to DSU.

The 111,524 R300D pair dispositions are:

- 110,516: no stronger proof; incidence only.
- 472: stronger R300E proof exists, while the R300D row remains ineligible.
- 264: stronger R300F proof exists, while the R300D row remains ineligible.
- 128: R300G audited fail-closed, no edge.
- 144: R300H audited fail-closed, no edge.

All 1,600 R300D single-target exclusions are covered by the sealed R300H
audit. The 3,232 R300A canonical contacts split into 432 reclosed by R300B,
8 R300B-rejected fail-closed rows, 128 R300G fail-closed rows, and 2,664
no-endpoint-face rows reserved for a later Round302 reopen. The 3,488 R300A
source-expansion rows supply 6,292 canonical references and no DSU edge.

## 124-key component incidence

The component-key incidence ledger covers all **124** final official keys and
contains **121,984** component/key rows:

- 121,916 components have official-key multiplicity 1.
- 28 components have official-key multiplicity 2.
- 4 components have official-key multiplicity 3.
- Cross-official-key component count: 32.
- Maximum official-key multiplicity in one component: 3.
- Formal official-key identity merges: **0**.

These rows record incidence only. Sharing a DSU component does not identify,
collapse, or merge official keys.

## Independent verifier seal

The independent verifier treats the producer only as inert, fixed,
hash-pinned bytes. It does not import, execute, parse, or tokenize producer
source. It reconstructs the member universe, legal edge ledger, both DSU
orders, the component-key incidence ledger, the ineligible-source ledger, and
the result in a cacheless temporary directory before opening candidate
artifacts for exact byte comparison.

- Verifier:
  `cm2_round301_source_g_legal_component_dsu_application_verifier.py`
- Verifier SHA-256:
  `58f28198c1d1f43f76f8ec7f7f9d341b6bd5617c81fb4d52d2ecab42f870caa3`
- Sealed attack census: 41/41 rejected, including 28 independently
  re-signed semantic attacks.

### Verifier run Alpha

- Seed: `301101`
- Mode: cacheless write
- Verdict:
  `PASS_INDEPENDENT_CACHELESS_ROUND301__564492_MEMBERS__434606_LEGAL_EDGES__119844_INELIGIBLE_ROWS_CONSUMED_WITH_ZERO_DSU_INPUT__246016_RANK_REDUCTIONS__121948_COMPONENTS__ALL_41_ATTACKS_REJECTED`
- Elapsed wall time: `18:37.80`
- Maximum resident set size: `1089056 kB`

### Verifier run Beta

- Seed: `301909`
- Mode: cacheless `--no-write`
- Verdict:
  `PASS_INDEPENDENT_CACHELESS_ROUND301__564492_MEMBERS__434606_LEGAL_EDGES__119844_INELIGIBLE_ROWS_CONSUMED_WITH_ZERO_DSU_INPUT__246016_RANK_REDUCTIONS__121948_COMPONENTS__ALL_41_ATTACKS_REJECTED`
- Elapsed wall time: `18:49.11`
- Maximum resident set size: `1076324 kB`

### Final verifier artifact pins

- Attack-suite file SHA-256:
  `e74d0fc98da73b9ceb52e8880fa04c6c134687fcc422065d29f38637f39829a0`
- Attack-suite internal SHA-256:
  `d52ac40e4ddd7752317749e7dcab84cac2605cbb2589c932e9d69d805e1f8aea`
- Verification file SHA-256:
  `31db1fd416c12a384bcfc7dd08d0a6ecf1cba5a9390b47227847f5c7852f376a`
- Verification internal SHA-256:
  `0f25c6adc3884511577f5d0c14c5684a23530eabbdd5174a278a379e77887ab0`

No final seal may be asserted while any placeholder in this section remains.

## Formal credit and strict nonclaim

Round301 grants only the following formal credit:

- legal component edge-application credit: 434,606;
- DSU rank-reduction credit: 246,016;
- component-union credit: 246,016;
- component-quotient credit: 1;
- post-Round301 component count: 121,948.

It grants **zero** occurrence-identity-collapse credit, official-key-merge
credit, maximality credit, fibre credit, and global-disposition credit.

In particular:

- no R295A or R300D incidence row enters DSU;
- no R300A closure-contact row enters DSU;
- R300G and R300H contribute zero eligible edges;
- no rejected raw multi-endpoint cross-product is used;
- no obsolete Round298 or temporary spike is imported, executed, or parsed;
- the historical speculative rank value 29,984 is not used;
- component/key incidence is not an identity, maximality, fibre, or global
  disposition proof;
- D02 and CM2 are **not claimed** by Round301.

## Required final 11-item manifest

The final
`cm2_round301_source_g_legal_component_dsu_application_manifest.sha256`
must contain exactly these 11 entries, with no manifest self-entry:

1. `cm2_round301_source_g_legal_component_dsu_application.py`
2. `cm2_round301_source_g_legal_component_dsu_application_edge_application_ledger.json.gz`
3. `cm2_round301_source_g_legal_component_dsu_application_member_component_ledger.json.gz`
4. `cm2_round301_source_g_legal_component_dsu_application_component_key_incidence_ledger.json.gz`
5. `cm2_round301_source_g_legal_component_dsu_application_ineligible_source_consumption_ledger.json.gz`
6. `cm2_round301_source_g_legal_component_dsu_application_result.json`
7. `cm2_round301_source_g_legal_component_dsu_application_verifier.py`
8. `cm2_round301_source_g_legal_component_dsu_application_attack_suite.json`
9. `cm2_round301_source_g_legal_component_dsu_application_verification.json`
10. `cm2_round301_source_g_legal_component_dsu_application_report.md`
11. `cm2_round301_source_g_legal_component_dsu_application_cold_replay.md`

The producer, verifier, five candidate artifacts, attack suite, and
verification artifact are pinned above. The report and cold-replay file pins
are fixed by the final manifest after both cacheless verifier runs have
passed.
