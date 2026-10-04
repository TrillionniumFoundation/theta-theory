# Source audit for the external A2 v38 rereview

## 1. Reviewed object

Repository: `TrillionniumFoundation/theta-theory`  
Manuscript: Qian Qi, *Scalar collision laws and recognition of periodic dispersing billiards*  
Reviewed directory: `papers/A2-v38-finite-field-rigidity`

The reviewed source is identified by Git objects:

- author branch: `revision/a2-v38-finite-field-rigidity-2026-10-04`;
- equivalent referee-copy branch: `revision/a2-v38-referee-copy-2026-10-04`;
- final author commit: `a346669928e5147cf2c0ef86c3bc2a455b512d14`;
- repository tree: `3abc9b8fb500c87b125332e7d798a27f72a81a33`;
- active core tree: `64cf5f5af705113b494c6f16ad538c413dfbc5e4`;
- mathematical checkpoint: `3178349cc91a3f0f0607dd54ab13039e7c999874`.

The final commit adds only a two-point first-page layout adjustment. The checkpoint contains the v38 mathematical and verification package.

The review branch

`review/a2-v38-external-harsh-top4-rereview-2026-10-04`

was created directly from the final author commit. Review files are confined to

`reviews/a2-v38-external-harsh-top4-rereview-2026-10-04/`.

No author source, revision branch, prior report, workflow, retained paper, or unrelated path is edited.

## 2. Chronology and preserved source

The immediate author source is A2 v37:

- commit: `02e6a6c799cb00c7dc7304ddfbf7ac885c83ea4d`;
- repository tree: `f640fe628767f4312810f61c1eed2db85eefcc87`;
- retained active core tree: `12a9e42058be2b228f6855e8fbf296ac97555d52`.

The controlling external report is the v36 review:

- review commit: `3c6b195c183df2c52e58e25cf59f7e3fcba07fc3`;
- report blob: `eb9f5658c909622778bcf8a80f9de220e57ab6ef`;
- reviewed v36 author commit: `2559749a038fd2b5ec46d7cc74fdb4bd844b266a`.

No separate v37 review branch existed. Version 38 says so explicitly. The present review therefore audits both the major v37 additions and the new v38 additions.

`SOURCE_PINS.json` records twenty-four retained v37 core files. Repository inspection confirms that those files are active in the v38 primary; the new core inputs are:

- `core/00g_finite_field_overview.tex`;
- `core/17_finite_stencil.tex`;
- `core/18_isotropic_rigidity.tex`.

The v37 additions retained in v38 include:

- `core/14_global_response.tex`;
- `core/15_unregistered_footprints.tex`;
- `core/16_sharp_stationary.tex`;
- `core/16a_shrinking_upper.tex`.

## 3. Files inspected in detail

The audit read the current:

- `main.tex`;
- `core/00_setting.tex`;
- `core/00f_global_overview.tex`;
- `core/00g_finite_field_overview.tex`;
- `core/14_global_response.tex`;
- `core/15_unregistered_footprints.tex`;
- `core/16_sharp_stationary.tex`;
- `core/16a_shrinking_upper.tex`;
- `core/17_finite_stencil.tex`;
- `core/18_isotropic_rigidity.tex`;
- `core/05_comparison.tex`;
- `RESPONSE_TO_REFEREES.md`;
- `PROOF_LEDGER.md`;
- `HISTORY_AND_LITERATURE.md`;
- `README.md`;
- `SOURCE_PINS.json`;
- `references.tex`;
- `tools/validate_v38.py`;
- `tools/verify_v38.py`;
- `.github/workflows/a2-v38-verify.yml`.

It also read the v36 external report, the v37 commit/source chronology, and the retained v37 diagnostics through the exact-SHA artifact.

## 4. Mathematical deltas confirmed

### 4.1 Global response-period rigidity

The full reciprocal difference field determines the occupation by an optimal-stopping formula. Its translation periods agree exactly with those of the obstacle configuration. The theorem applies to arbitrary locally finite separated bounded convex configurations and does not assume periodicity.

### 4.2 Unregistered homothetic footprint inverse

At several labelled settings, footprint supports may have independent translations and unknown scale ratios. Integrated forward-response deficits recover scale. Centered support envelopes recover the common centered footprint without component matching. The complete geometric fiber is a common table translation and independent footprint shifts by obstacle periods.

### 4.3 Matching stationary polynomial power

The effective collision boundary gives a pairwise squared-Hellinger contraction of order `epsilon^(3/2)` for all short directions and lengths. Combined with the physical packing and stopped information chain, this gives the same polynomial power as the shrinking-layer pooled-compass upper construction, up to one logarithm.

### 4.4 Fixed finite-stencil inverse

Pointwise occupation is the value of a fixed killed-walk stopping linear program. The inverse is defined and Lipschitz for arbitrary data vectors, admits primal and dual certificates, and leads to a fixed-site `epsilon^-2` finite sampling law.

### 4.5 General and isotropic command laws

Exact period rigidity extends to any known bounded mean-zero displacement law with positive second moment. For uniform directions, an integrated forward response is `t/pi` times obstacle perimeter, giving an intrinsic scale deficit and the same origin-free registration theorem.

## 5. Exact-source workflow audit

The exact-head workflow is

`.github/workflows/a2-v38-verify.yml`.

The final run is:

- run ID: `37188797187`;
- head SHA: `a346669928e5147cf2c0ef86c3bc2a455b512d14`;
- status: `completed`;
- conclusion: `success`.

All job stages succeeded:

1. exact triggering-commit checkout;
2. build-environment installation;
3. source, finite-algebra, retained-diagnostic, and complete-primary qualification;
4. exact-source evidence upload.

Artifact metadata:

- artifact ID: `11297913971`;
- name: `A2-v38-a346669928e5147cf2c0ef86c3bc2a455b512d14-1`;
- digest: `sha256:2296e44f9640d20d8ecb7f5f9efc9e67de826e10af74604be212ae280ed9d085`.

## 6. Receipt audit

The downloaded artifact contains the source archive, PDF, build log, layout findings, current diagnostics, retained diagnostics, source hashes, receipt, and artifact binding.

The receipt records:

- schema: `a2-v38-qualification-1`;
- status: `passed`;
- exact commit qualified: true;
- source commit: `a346669928e5147cf2c0ef86c3bc2a455b512d14`;
- pages: 71;
- active TeX files: 29;
- labels: 265;
- proofs: 66;
- retained core files: 24;
- current diagnostics: 1,796 checks, including 512 enumerated stopping policies;
- retained v37 diagnostics: 606,502 finite checks;
- layout findings: none;
- formal proof certificate: false;
- physical sensor executed: false.

Important artifact hashes include:

- primary PDF: `711054010f4c7ce16f58abefa19c2ff380969df5d6c213744b0d635b1895f4c5`;
- source archive: `1bf88d3d0801a86bed5d9eb59e3a8b67b3fc424bb49414b9bcf14c6f5dd6b55e`;
- current finite diagnostics: `19e8860914757586ee6271bc1f40f175c13fd6be871faca60efa78ed226e7ee7`;
- retained finite diagnostics: `38ea9bd0f798a632bfc04423e95802f27b46ffc5bd99a2f13f058bb4572a839f`.

The exact source is therefore reproducibly qualified at the reviewed head. This is not proof certification.

## 7. Independent finite diagnostics

The review's `verify_review.py` imports no author module and uses only the Python standard library. Normal and optimized executions are byte-identical at SHA-256

`0a3174f1ce669cd03bf564e28b2466730231dedba16a58ecc8066c81d270473b`.

It records 931,220 checks. The largest groups are finite exact support-envelope, width, perimeter, and translation tests. It also includes:

- all 512 deterministic stopping policies on a `3 x 3` killed compass model;
- flow and Green-budget checks;
- Bellman/primal equality;
- arbitrary-data weighted and supremum stability;
- a model with nonzero occupation on the computational boundary;
- 308 centered one-dimensional exit systems, including singular covariance;
- 640 finite Hellinger-capacity comparisons;
- exact exponent and Hoeffding-budget identities.

These diagnostics are not continuum proof certificates and do not validate a physical apparatus.

## 8. Limits of the audit

This was a focused external top-four rereview, not formal verification of a seventy-one-page programme with sixty-six proof environments. The audit concentrated on:

1. source identity and preservation;
2. the global stopping inverse and period identity;
3. the unregistered support-envelope inverse and gauge;
4. the matching stationary-rate argument;
5. the finite stopping polytope and finite sampling law;
6. the general centered and isotropic command extensions;
7. the editorial significance of the combined package.

No exhaustive literature or priority search was performed. The most delicate continuum argument remains the uniform effective-boundary/Hellinger estimate. No physical collision apparatus was executed.

## 9. Audit conclusion

The reviewed object is unambiguous and source-qualified. The v37 and v38 additions are real mathematical changes, not branch aliases. No fatal counterexample was found in the audited core. The negative recommendation in `REFEREE_REPORT.md` is a top-four significance and information-model judgment, not a claim that the manuscript failed to respond or failed to build.
