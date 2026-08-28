# CM2 Round280: true-seam and reverse-rechart incidence probe

## Decision

This is a strict zero-credit probe.  It closes the finite overlap census but
does **not** close the seam-normal corridor gate.

All `13,788` Round275 reverse-rechart regions have a nonempty exact algebraic
image under

```text
(t')² = 1 - t²,  p' = p,  s' = s.
```

Their exact relation to the Round279 collar-atom graph is:

- no incident Round279 atom class: `8,776`;
- one incident atom class: `2,820`;
- two or more incident atom classes: `2,192`.

The geometric witness census is:

- exact positive physical-volume overlaps: `8,048`;
- exact positive-area common `p` faces: `3,288`;
- exact positive-area common `s` faces: `2,256`.

Full 10-field signature object equality, owner-target equality, adjacent-chart
identity, and exact algebraic `t`-image intersection are required.  A signature
hash is used only as a spatial-index key and never as a binding rule.

## The 152 true-seam patches

Every Round268 patch has a positive `p×s` projection into Round275 guard
channels on both directed sides.  The side census is:

- candidate guards per side: `1` for 64 sides, `2` for 240 sides;
- candidate connected Round275 regions per side: between `1` and `555`;
- positive conditional region-node pairs exist for all `152/152` patches.

However, direct exact seam incidence is `0/152`.  Every source guard is
strictly outside its source chart and every Round275 rational region is
strictly inside its adjacent chart.  Both have a strictly positive exact
normal gap from the irrational seam `t²=1/2`.  Therefore positive `p×s`
projection alone is not a same-point component edge.

Against the current Round279/Round280 atom graph:

- `240/304` directed patch endpoints have no candidate Round275 region that
  binds a Round279 atom;
- `64/304` directed endpoints have a mixed/multiple conditional channel;
- `128/152` patches have at least one atom-orphan endpoint;
- `24/152` patches have conditional ambiguity on the available region set;
- no patch is directly resolved, because the seam-normal corridor is absent
  in every case.

The probe preserves every candidate region ID and exact patch-side gap in the
152-row attachment.  It does not infer incidence from origin equality,
signature equality, or Jx/Jy.

## Conditional rank sizing only

Starting with the Round280 zero-credit `136,740` provisional component nodes
and adding `13,788` Round275 region nodes:

- exact region-to-Round280 component relations requested: `7,120`;
- their preview rank reduction: `5,116`;
- conditional true-seam region edges requested: `134,920`;
- their additional preview rank reduction: `4,812`;
- conditional component count after only those included relations: `140,600`.

These numbers are not DSU credit.  The preview excludes both the complete
Round275 region-to-region frontier and the missing seam-normal corridors.

## Exact blocker and next gate

The next certificate must construct, for each patch-side cell, an exact
connected half-open normal corridor from the Round182 root `t²=1/2` to a
uniquely identified Round275 region or collar atom.  It must:

1. keep the complete return signature and official exact key fixed on the
   corridor;
2. prove positive normal width and positive `p×s` footprint;
3. use the owner/shadow boundary convention at the seam;
4. prove the analytic rechart identity on the exterior side;
5. separately exhaust Round275 region-to-region overlap/common-face
   adjacency.

Until then the frozen baseline remains quotient `63,224`, expanded
occurrences `126,468`, maximality `0/63,224`, fibres `0/116`, dispositions
`0/224,580`, Gate5 `10/18`, D02 blocked, and CM2
`NO-GO_FOR_CLAIM`.  Jx/Jy glue credit remains zero.

## Artifacts

- producer:
  `cm2_round280_source_g_true_seam_and_rechart_region_incidence_probe.py`
- result:
  `cm2_round280_source_g_true_seam_and_rechart_region_incidence_probe_result.json`
- complete Round275 region ledger:
  `cm2_round280_source_g_true_seam_and_rechart_region_incidence_probe_region_bindings.json.gz`
- complete Round268 patch-channel ledger:
  `cm2_round280_source_g_true_seam_and_rechart_region_incidence_probe_patch_channels.json.gz`

