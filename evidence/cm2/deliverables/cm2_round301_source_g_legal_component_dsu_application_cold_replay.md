# Round301 Source-G legal component DSU application — cold replay

Run from the repository root. The observed resource measurements and all
sealed artifact pins below come from the completed dual-seed replays.

## Frozen expectations

- Producer seeds: `301031`, `301977`
- Verifier seeds: `301101`, `301909`
- Member count: `564492`
- Legal edge rows: `434606`
- Ineligible source-consumption rows: `119844`
- DSU rank reduction: `246016`
- Component count: `121948`
- Final official-key count: `124`
- Partition SHA-256:
  `c1ab6beed75d5e7379103975d6a9ac1b1095a3eb24b34c87288782e7c97cfe09`

The five candidate file pins must be:

```text
2597d788dd4459a6e111b49e55300d49ef40258698874911adbefbe74f0142c5  cm2_round301_source_g_legal_component_dsu_application_edge_application_ledger.json.gz
88adb1ac6c9ee447fddb2ccd8e657a238827e9b31712d974a2a9abd2a3591b93  cm2_round301_source_g_legal_component_dsu_application_member_component_ledger.json.gz
95b7ce99f7aabd90b411484ff0cdc15f341bebd28f32f30da4d0e22c4e8b133c  cm2_round301_source_g_legal_component_dsu_application_component_key_incidence_ledger.json.gz
5fbc5a409eccd4e04954c7b63dab6739897efd8d9e327c47045cbfbbbaf7633e  cm2_round301_source_g_legal_component_dsu_application_ineligible_source_consumption_ledger.json.gz
aeb7c98be3d8fb6226bc39d5e45379484a3bb5e936a0475777b1d5fc59ab062c  cm2_round301_source_g_legal_component_dsu_application_result.json
```

## 1. Environment and fixed source pins

```bash
set -euo pipefail

R301_PREFIX=cm2_round301_source_g_legal_component_dsu_application
R301_DIR=deliverables
R301_SCRATCH=.tmp/openclaw-spikes/r301-cold-replay
mkdir -p "$R301_SCRATCH"

test "$(sha256sum "$R301_DIR/$R301_PREFIX.py" | cut -d' ' -f1)" = \
  4a0513885f21c5544be84964bb0d968ca1b04435aff4bbed36755a1684f3bcd5
test "$(sha256sum "$R301_DIR/${R301_PREFIX}_verifier.py" | cut -d' ' -f1)" = \
  58f28198c1d1f43f76f8ec7f7f9d341b6bd5617c81fb4d52d2ecab42f870caa3
```

## 2. Producer dual-seed byte replay

The producer writes the five canonical candidate artifacts in `deliverables/`.
Hash each completed run before starting the next seed.

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=301031 \
  /usr/bin/time -v \
  python3 -B "$R301_DIR/$R301_PREFIX.py" --seed 301031 \
  >"$R301_SCRATCH/producer-alpha.stdout" \
  2>"$R301_SCRATCH/producer-alpha.time"

sha256sum \
  "$R301_DIR/${R301_PREFIX}_edge_application_ledger.json.gz" \
  "$R301_DIR/${R301_PREFIX}_member_component_ledger.json.gz" \
  "$R301_DIR/${R301_PREFIX}_component_key_incidence_ledger.json.gz" \
  "$R301_DIR/${R301_PREFIX}_ineligible_source_consumption_ledger.json.gz" \
  "$R301_DIR/${R301_PREFIX}_result.json" \
  >"$R301_SCRATCH/producer-alpha.sha256"

PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=301977 \
  /usr/bin/time -v \
  python3 -B "$R301_DIR/$R301_PREFIX.py" --seed 301977 \
  >"$R301_SCRATCH/producer-beta.stdout" \
  2>"$R301_SCRATCH/producer-beta.time"

sha256sum \
  "$R301_DIR/${R301_PREFIX}_edge_application_ledger.json.gz" \
  "$R301_DIR/${R301_PREFIX}_member_component_ledger.json.gz" \
  "$R301_DIR/${R301_PREFIX}_component_key_incidence_ledger.json.gz" \
  "$R301_DIR/${R301_PREFIX}_ineligible_source_consumption_ledger.json.gz" \
  "$R301_DIR/${R301_PREFIX}_result.json" \
  >"$R301_SCRATCH/producer-beta.sha256"

cmp "$R301_SCRATCH/producer-alpha.sha256" \
    "$R301_SCRATCH/producer-beta.sha256"
```

Check the frozen pins:

```bash
(
  cd "$R301_DIR"
  cat <<'EOF' | sha256sum -c -
2597d788dd4459a6e111b49e55300d49ef40258698874911adbefbe74f0142c5  cm2_round301_source_g_legal_component_dsu_application_edge_application_ledger.json.gz
88adb1ac6c9ee447fddb2ccd8e657a238827e9b31712d974a2a9abd2a3591b93  cm2_round301_source_g_legal_component_dsu_application_member_component_ledger.json.gz
95b7ce99f7aabd90b411484ff0cdc15f341bebd28f32f30da4d0e22c4e8b133c  cm2_round301_source_g_legal_component_dsu_application_component_key_incidence_ledger.json.gz
5fbc5a409eccd4e04954c7b63dab6739897efd8d9e327c47045cbfbbbaf7633e  cm2_round301_source_g_legal_component_dsu_application_ineligible_source_consumption_ledger.json.gz
aeb7c98be3d8fb6226bc39d5e45379484a3bb5e936a0475777b1d5fc59ab062c  cm2_round301_source_g_legal_component_dsu_application_result.json
EOF
)
```

## 3. Independent verifier Alpha

Alpha independently rebuilds all four ledgers and the result before opening
the candidates, performs forward/reverse DSU replay, runs 41 attacks, and
writes the canonical attack and verification artifacts.

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=301101 \
  /usr/bin/time -v \
  python3 -B "$R301_DIR/${R301_PREFIX}_verifier.py" --seed 301101 \
  >"$R301_SCRATCH/verifier-alpha.stdout" \
  2>"$R301_SCRATCH/verifier-alpha.time"
```

Observed seal record:

```text
verifier_alpha_verdict=PASS_INDEPENDENT_CACHELESS_ROUND301__564492_MEMBERS__434606_LEGAL_EDGES__119844_INELIGIBLE_ROWS_CONSUMED_WITH_ZERO_DSU_INPUT__246016_RANK_REDUCTIONS__121948_COMPONENTS__ALL_41_ATTACKS_REJECTED
verifier_alpha_elapsed=18:37.80
verifier_alpha_max_rss_kb=1089056
```

The final JSON line on stdout together with the sealed attack and
verification artifacts must establish:

- `seed_affects_output: false`
- `no_write: false`
- the five frozen candidate pins;
- partition pin
  `c1ab6beed75d5e7379103975d6a9ac1b1095a3eb24b34c87288782e7c97cfe09`;
- stdout status reports 41/41 attacks rejected;
- the attack and verification artifacts report 28 semantic attacks
  independently reclosed.

## 4. Independent verifier Beta (`--no-write`)

Record the attack and verification pins before Beta. `--no-write` must compare
the pre-existing canonical bytes and must not modify either file.

```bash
sha256sum \
  "$R301_DIR/${R301_PREFIX}_attack_suite.json" \
  "$R301_DIR/${R301_PREFIX}_verification.json" \
  >"$R301_SCRATCH/verifier-artifacts-before-beta.sha256"

PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=301909 \
  /usr/bin/time -v \
  python3 -B "$R301_DIR/${R301_PREFIX}_verifier.py" \
    --seed 301909 --no-write \
  >"$R301_SCRATCH/verifier-beta.stdout" \
  2>"$R301_SCRATCH/verifier-beta.time"

sha256sum \
  "$R301_DIR/${R301_PREFIX}_attack_suite.json" \
  "$R301_DIR/${R301_PREFIX}_verification.json" \
  >"$R301_SCRATCH/verifier-artifacts-after-beta.sha256"

cmp "$R301_SCRATCH/verifier-artifacts-before-beta.sha256" \
    "$R301_SCRATCH/verifier-artifacts-after-beta.sha256"
```

Observed seal record:

```text
verifier_beta_verdict=PASS_INDEPENDENT_CACHELESS_ROUND301__564492_MEMBERS__434606_LEGAL_EDGES__119844_INELIGIBLE_ROWS_CONSUMED_WITH_ZERO_DSU_INPUT__246016_RANK_REDUCTIONS__121948_COMPONENTS__ALL_41_ATTACKS_REJECTED
verifier_beta_elapsed=18:49.11
verifier_beta_max_rss_kb=1076324
attack_suite_file_sha256=e74d0fc98da73b9ceb52e8880fa04c6c134687fcc422065d29f38637f39829a0
attack_suite_internal_sha256=d52ac40e4ddd7752317749e7dcab84cac2605cbb2589c932e9d69d805e1f8aea
verification_file_sha256=31db1fd416c12a384bcfc7dd08d0a6ecf1cba5a9390b47227847f5c7852f376a
verification_internal_sha256=0f25c6adc3884511577f5d0c14c5684a23530eabbdd5174a278a379e77887ab0
```

## 5. Result invariants

```bash
jq -e '
  .member_universe.member_count == 564492 and
  .member_universe.base_root_count == 367964 and
  .member_universe.final_official_key_count == 124 and
  .legal_edge_census.total_sealed_legal_edge_row_count == 434606 and
  .forward_application.rank_reduction == 246016 and
  .reverse_application.rank_reduction == 246016 and
  .forward_application.component_count == 121948 and
  .reverse_application.component_count == 121948 and
  .forward_reverse_same_partition == true and
  .forward_application.partition_sha256 ==
    "c1ab6beed75d5e7379103975d6a9ac1b1095a3eb24b34c87288782e7c97cfe09" and
  .component_key_incidence_census.component_key_incidence_row_count ==
    121984 and
  .component_key_incidence_census.official_key_identity_merge_count == 0 and
  .ineligible_source_consumption.R300D_canonical_incidence_pair_count ==
    111524 and
  .ineligible_source_consumption.R300D_single_target_assignment_exclusion_count ==
    1600 and
  .ineligible_source_consumption.R300A_canonical_closure_pair_count ==
    3232 and
  .ineligible_source_consumption.R300A_source_pair_expansion_count ==
    3488 and
  .ineligible_source_consumption.ineligible_source_rows_fed_to_DSU == 0 and
  .formal_credit_transition.formal_maximality_credit == 0 and
  .formal_credit_transition.formal_fibre_credit == 0 and
  .formal_credit_transition.formal_global_disposition_credit == 0
' "$R301_DIR/${R301_PREFIX}_result.json"
```

The incidence ledger's multiplicity census must be
`{"1":121916,"2":28,"3":4}`, with 32 cross-key components and maximum
multiplicity 3. This is incidence only and grants zero official-key merge
credit.

## 6. Strict nonclaim audit

Before sealing, confirm all of the following:

- R295A/R300D incidence rows fed to DSU: 0.
- R300A closure-contact rows fed to DSU: 0.
- R300G eligible edges: 0.
- R300H eligible edges: 0.
- Historical speculative rank 29,984 is unused.
- Rejected raw face cross-products are unused.
- Obsolete Round298 and temporary spike artifacts are not parsed or executed.
- Occurrence identity collapse, official-key merge, maximality, fibre, and
  global-disposition credits remain 0.
- The component/key ledger is incidence, not identity.
- Round301 does not claim D02 or CM2.

## 7. Final 11-item manifest

After both verifier replays pass and the report and cold replay are frozen,
create a manifest containing exactly:

```text
cm2_round301_source_g_legal_component_dsu_application.py
cm2_round301_source_g_legal_component_dsu_application_edge_application_ledger.json.gz
cm2_round301_source_g_legal_component_dsu_application_member_component_ledger.json.gz
cm2_round301_source_g_legal_component_dsu_application_component_key_incidence_ledger.json.gz
cm2_round301_source_g_legal_component_dsu_application_ineligible_source_consumption_ledger.json.gz
cm2_round301_source_g_legal_component_dsu_application_result.json
cm2_round301_source_g_legal_component_dsu_application_verifier.py
cm2_round301_source_g_legal_component_dsu_application_attack_suite.json
cm2_round301_source_g_legal_component_dsu_application_verification.json
cm2_round301_source_g_legal_component_dsu_application_report.md
cm2_round301_source_g_legal_component_dsu_application_cold_replay.md
```

The manifest has 11 entries and does not include itself. Validate it from
inside `deliverables/` with:

```bash
sha256sum -c \
  cm2_round301_source_g_legal_component_dsu_application_manifest.sha256
test "$(wc -l < \
  cm2_round301_source_g_legal_component_dsu_application_manifest.sha256)" \
  -eq 11
```

Final dynamic pins:

```text
attack_suite_file_sha256=e74d0fc98da73b9ceb52e8880fa04c6c134687fcc422065d29f38637f39829a0
verification_file_sha256=31db1fd416c12a384bcfc7dd08d0a6ecf1cba5a9390b47227847f5c7852f376a
report_file_sha256=63210f326559daeac8a6cf5f27aa29e8fe663918d11c9c667302eb658e69266c
```

The cold replay does not embed its own SHA-256, and it does not embed the
manifest SHA-256, because either would create a self-reference or dependency
cycle. Compute both externally after materialization:

```bash
sha256sum \
  deliverables/cm2_round301_source_g_legal_component_dsu_application_cold_replay.md \
  deliverables/cm2_round301_source_g_legal_component_dsu_application_manifest.sha256
```

Do not declare the Round301 seal complete unless both cacheless verifier runs
pass, the manifest has exactly 11 non-self entries, and every manifest entry
validates.
