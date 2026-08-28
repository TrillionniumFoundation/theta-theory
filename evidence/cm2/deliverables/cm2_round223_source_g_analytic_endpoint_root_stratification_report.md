# Round223 source-G analytic endpoint-root stratification

## Verdict

`FORMAL_ALL_7932_EXACT_P_S_CONTACTS_COMPLETE_BY_RATIONAL_AND_SYMBOLIC_ANALYTIC_ROOT_STRATA__236_PARTIAL_CONTACTS_AND_PHYSICAL_COMPONENT_QUOTIENT_REMAIN`

Round223 formally replaces every one of Round219's `7,236` unresolved exact
terminal subfaces.  The replacement uses exact symbolic analytic roots, not
floating-point or interval midpoints as coordinates.

The completed local exact-contact scope is:

- Round219 cumulative exact contacts: `916`;
- newly completed exact contacts: `7,016`;
- cumulative exact `p/s` contacts: `7,932 / 7,932`;
- remaining incomplete exact `p/s` contacts: `0`.

The remaining local face frontier is the `236` partial contacts.  Physical
component quotient closure and global occurrence/fibre exhaustion are still
missing, so component, whole-origin, global-fibre, and key-disposition credits
remain zero.

## Formal artifacts

- Producer:
  `cm2_round223_source_g_analytic_endpoint_root_stratification.py`
  - SHA256:
    `fb5d46a31857cb09c2606747d4fbec996eecffdf65702431a17624a2260ad970`
- Certificate:
  `cm2_round223_source_g_analytic_endpoint_root_stratification_certificate.json`
  - SHA256:
    `3d28f097419e11bde6733462736fcb70cd0164b18ac06a793a34b5dc26113168`
  - result SHA256:
    `db012bb2e68176c8a5c144455bac9ff780521bbfa3c03110694390c70a3343d9`
- Fresh verifier:
  `cm2_round223_source_g_analytic_endpoint_root_stratification_verifier.py`
  - SHA256:
    `c67d5898a24e04e367f46fa3ffc67e6773de69616287877e88c89e5e417819e6`
- Verification:
  `cm2_round223_source_g_analytic_endpoint_root_stratification_verification.json`
  - SHA256:
    `e5e48f7553580f36710e0f7de9c3a59f866fcad434bc1f2ae9e151900372b820`
  - result SHA256:
    `5191d6e993678bb2f9fdd437b4bbea580d0d2fec9887b55eacfe75d1a548977e`
  - status: `PASS_PARTIAL_FORMAL_ROUND223`

## Exact analytic-root contract

For an unresolved Round219 terminal subface, exactly one graph endpoint is
non-strict, while the other graph endpoint and the full graph-axis derivative
are strict.  Round223 restricts the active factor to that endpoint edge as an
analytic function of the transverse coordinate.

An exact root identity binds:

1. the source chart, target lift, and active factor;
2. the exact fixed face coordinate and graph endpoint;
3. the Round219 edge carrier;
4. an exact rational isolating interval;
5. opposite strict active-factor signs at the interval endpoints; and
6. a strict transverse derivative enclosure on the complete isolating
   interval.

These data prove by the intermediate value theorem and strict monotonicity
that the pinned analytic edge function has exactly one simple root in the
rational interval.  The coordinate is represented as
`EXACT_ANALYTIC_UNIQUE_ROOT_NOT_NUMERIC_APPROXIMATION`.

No decimal approximation, interval midpoint, or arbitrary chosen member of
an Arb enclosure is treated as an exact coordinate.

## Endpoint-edge partitions

The `7,236` old unresolved edge carriers split as:

| method/result | rows |
|---|---:|
| direct full-edge unique root | 6,980 |
| direct full-edge zero-free | 4 |
| adaptive rational partition with one unique root | 252 |

The 252 derivative-unavailable full edges are split only where unresolved.
Their completion-depth histogram is:

| adaptive depth | newly completed original edges |
|---:|---:|
| 2 | 88 |
| 3 | 84 |
| 4 | 64 |
| 5 | 16 |

All edge partitions close by depth five.  The terminal edge census is:

- terminal rational segments: `8,000`;
- unique-root segments: `7,232`;
- zero-absence segments: `768`;
- unresolved segments: `0`.

Every ordered partition starts and ends at the original rational endpoints,
has exact consecutive rational joins, and follows
`LEFT_CLOSED_RIGHT_OPEN_EXCEPT_FINAL_RIGHT_CLOSED`; it has no gap and no
owned overlap.

## Exact symbolic strata

Every analytic root is shared by four exact strata:

1. the 2D open side strictly below the root;
2. the 2D open side strictly above the root;
3. the 1D root slice with the graph-endpoint root point removed; and
4. the 0D endpoint root point.

Strict edge monotonicity fixes the ambiguous graph-endpoint sign on each open
side.  Combined with the other strict graph-endpoint sign and strict full
graph derivative, this proves one side `TRACE` and the other `ABSENT`.

On the 1D root slice, strict graph monotonicity proves zero absence away from
the root graph endpoint.  The 0D root point is exactly zero by the analytic
root definition and is joined to the unique TRACE-side restricted zero curve.
The root point is never hidden inside a 2D strip.

The four direct zero-free endpoint edges sharpen to four whole rational 2D
`TRACE` strips.  The total stratum census is:

| stratum | rows |
|---|---:|
| 2D open root sides | 14,464 |
| 2D whole rational strips | 4 |
| 1D root slices | 7,232 |
| 0D endpoint root points | 7,232 |
| **all symbolic strata** | **28,932** |

The 2D classification totals are `7,236 TRACE` and `7,232 ABSENT`.
There are `7,232` exact endpoint-to-curve join rows.

## Contact completion

For each of the `7,016` incomplete Round219 contacts, the completed-contact
row binds:

- the exact Round219 contact row and all inherited resolved subfaces;
- every old unresolved terminal subface;
- one complete endpoint-edge partition for every old unresolved subface; and
- every replacement 2D, 1D, and 0D stratum.

Complete credit is granted only after proving that all old unresolved rows
are exactly replaced and the replacement has no gap or owned overlap.  The
new contacts cover 20 official key ordinals; their per-ordinal count-map
SHA256 is
`528cbe40dbff99f168027c65bbea26b19775d933fe6c5e88218bf06a6555efdc`.
This is a local exact-contact census, not global key-fibre exhaustion.

## Formal ledgers

| ledger | rows | rows SHA256 | row-ID SHA256 |
|---|---:|---|---|
| endpoint-edge partitions | 7,236 | `f7f78461eb58fa396dea816badf1cf9fcef2bae4a9df18744a94450ba2250a37` | `a52a99a17a3f2f780e0f30f3150c82816990949713fda3338204f81a6db30701` |
| edge terminal segments | 8,000 | `0f626660f9054716a73803df09ecc8f9c063833d6abfcd455c489a77eda50a94` | `4207c08402d2656036a17be1af8b33d11c395d8c676ab99964223d1972c2a11f` |
| analytic roots | 7,232 | `fa875cad6a56378d71f5a7b56b504769a0143203e012f5842d84a3c632e22d70` | `8f62b229f3e45443224a0f2cef57670dcc9d22d284f7642051cff48a48b75dc4` |
| symbolic strata | 28,932 | `d6960c53790af488752c834d4bb4a62a3fbe6bc51e45312750130992cb9a7c38` | `4607dede8ada71f44ed5c860bbd060afe8870bddd2d8e9b59e720f72862d5ced` |
| endpoint-to-curve joins | 7,232 | `ef12cbbfb3e3b189409f07b102599313a3db29f7562053c35d2e5f56a7195e33` | `b5233b4230e09170867bd807b3d16b23152f602fe9fc82f43ad6f1c748ca1ad1` |
| completed exact contacts | 7,016 | `43d01f0c7cac298dccecc48ad7b2048785907bbad4943f5e5a5ce15775b258c4` | `28ee7d16235fc6ad4a1e23a75e0719764d9ba246a5cbc745ef100046f7985690` |

Every row has its own SHA256; every ledger independently closes ordered rows,
row IDs, and row hashes.

## Fresh verification and attacks

The verifier reconstructs the complete expected object from the pinned
Round219/Round186 boundary before loading the Round223 candidate.  It imports
or executes neither the Round223 producer nor either Round221 probe.

It demands full expected Python-object and canonical equality, then rejects:

- `18/18` genuinely re-signed semantic attacks;
- `15/15` strict JSON attacks; and
- `21/21` filesystem/path/output attacks.

Semantic attacks delete or alter roots, isolating intervals, derivative signs,
root slices, root points, joins, terminal classifications, complete contacts,
partition gap/overlap flags, and exact-coordinate representation; they also
attempt component, whole-origin, and global-disposition credit theft.

The hardened path suite rejects file-object substitutions, nested and
unallowlisted outputs, symlink-parent aliases, and explicit parent-`..`
aliases before normalization.  AST scans find zero duplicate literal
dictionary keys in both frozen sources.

## Strict boundary

Round223 grants local analytic-root, stratum, endpoint-join, and exact-contact
completion credits.  It grants no:

- component-deduplication credit;
- whole-leaf, whole-origin, or whole-tube credit;
- global component or global-fibre credit;
- global exact-key-disposition credit; or
- source-G disposition (`0 / 224,580`).

Therefore D02 remains `BLOCKED`, Gate5 remains `10/18`, and CM2 remains
`NO-GO`.

