# Response to the latest referee reports — Revision 68

**Quantitative:** *Joint Instrument Coding Laws and Boundary-Uniform Rational Realization*.

**Controlling report:** v67/r44, `68c69a4a2e8b4e3b11c43a181806ab578584b719`. **Companion audit:** `7a9586cd8cf7995152fbbf501f3e47da4aa89900`.

**Reviewed mathematical base:** v67 publication `98a4b12126502ea41c620b58bad4b9aa30f9c72c`; qualified source `429a7cbe79c032386da934eb824d4ba31416ec44`.

The initial remote survey found r43 and the newly qualified v67 publication. We anchored v68 remotely at `38887b7e358f354cfe3699c210c965cb33a9918a`. The r44 report and audit appeared during this revision and are now controlling. The original anchor and initial r43 response are retained as dated provenance, not retroactively rewritten into an earlier r44 review. Both new r44 documents review exactly the v67 publication from which v68 descends.

We retain the general-journal mathematical objective. The response is a new proof package and a more focused exposition, not a change of submission target or deletion of prior conclusions. The v67 affine and programme results are inherited, not presented as new v68 work.

## Principal mathematical changes

The fixed-error coefficient is strengthened to the joint law

    log2 M_N(delta;a) = (s/2) log2 N + s log2(1/delta) + O_(d,n,m,a)(1),
    s = d^2(m n^2-1), N >= 1, 0 < delta <= 1/32.

The remainder is uniform in both N and delta. The new ingredient is an elementary local Bernoulli product lower bound, valid even at arbitrarily small separation and at Bernoulli endpoints. A pair-dependent Choi test transfers it to instrument geometry. This retains the precision term that was hidden by the previous fixed-error argument. The upper bound remains the inherited rational codec plus the classical-programme estimate, with their source and hypotheses credited.

A separate boundary theorem concerns outcome-retaining preparation instruments, including rank-deficient states and zero outcomes. For fixed output-rank bounds r_y, the coefficient is

    v = sum_y r_y(2n-r_y)-1,
    log2 P_N(delta;r) = (v/2) log2 N + v log2(1/delta) + O_(n,m,r)(1).

The same joint range is covered, with no lower eigenvalue margin. The exact adaptive metric reduces to product-state trace distance because the channel erases its input. A normalized triangular-factor code has rational Gram-matrix outputs, preserves zero outcomes, and never increases block ranks. Its encoder compares rational squared factor coordinates and uses integer square roots; irrational Cholesky factors are not stored. A rank-stratum patch and the local testing lemma give the matching converse.

This is not a boundary theorem for every disturbing quantum instrument, a dimension-growing optimal law, or a general mutable-workspace lower bound. The coherent unitary obstruction is retained. The new comparison formulates the remaining general Choi-support/tangent-cone problem rather than declaring the entire boundary solved.

## Response to the fourteen required revisions

### R44 required 01 — Focused quantitative paper

The journal-facing quantitative article now contains only coding preliminaries, intrinsic description entropy, adaptive reuse, the joint-precision converse, rank-boundary preparation codes, and direct literature comparison. Every needed lemma is proved inside it. The complete research edition retains every previously active mathematical label and its full proof. No predecessor PDF is a dependency.

### R44 required 02 — Fixed-dimensional convention

All entropy formulas display fixed input/output/outcome dimensions. The new joint theorems have remainders independent of N and delta, but dependent on the stated fixed dimensions and, for the general instrument body, its fixed positive margin. No dimension-uniform constants are asserted.

### R44 required 03 — Full body versus strict interior

Section 38 is the one-use diamond law on the full instrument body. Sections 39–40 concern adaptive reuse on a blockwise positive Choi body. Section 41 is a distinct boundary theorem for input-erasing preparation instruments, not an extension to the entire instrument body.

### R44 required 04 — Boundary stratification

Section 41 proves an actual rank-stratified law for preparation instruments, with v=sum_y r_y(2n-r_y)-1, including smaller ranks and zero blocks. The comparison section separately formulates general Choi-support/tangent-cone and coherent-direction questions; it does not claim a complete classification for arbitrary disturbing instruments.

### R44 required 05 — Legal codebook

The intrinsic-coordinate codebook is the encoder image or the validated reconstructions, not the full mixed-radix cube. The new factor code also checks its mask, anchor, payload range and metadata; its normalized Gram matrices are automatically positive semidefinite.

### R44 required 06 — Header accounting

Dimensions, labeled outcomes, requested horizon/error, and declared rank bounds are fixed public data in the leading laws. The finite factor pivot mask is explicitly charged. Both schemas explain that variable headers, indexing, target input, validation workspace and decoded matrix storage cost extra.

### R44 required 07 — Description versus physical simulation

The decoder produces a mathematical rational instrument. The quantum operation still requires a quantum implementation. No finite-classical-message physical simulator accepting unknown entangled input or processor hardware-dimension bound is inferred.

### R44 required 08 — Description versus learning

The encoder receives the target matrix data. The current learning papers remain cited, with query/sample complexity expressly separated from deterministic description length.

### R44 required 09 — Adaptive discrimination

The new focused comparison cites Salek–Hayashi–Winter, arXiv:2011.06569v3, Sections II–V, Phys. Rev. A 105, 022419 (2022). Binary error exponents are distinguished from finite-use family covering numbers. In particular, input erasure, not entanglement breaking alone, proves our exact product-state reduction.

### R44 required 10 — Exact-head verification

The release workflow now includes a separate immutable checkout of the reviewed v67 publication 98a4b12126502ea41c620b58bad4b9aa30f9c72c, executing its existing read-only verifier and journal rebuild. Its attestation records that exact checkout, separately from the triggering v68 SHA. The v68 final request is independently reconstructed. Referee aliases are created only after successful corresponding attestations; workflow definitions alone are not reported as executed evidence.

### R44 required 11 — Finite-test scope

Exact finite regression validates the binary constants on test cases, rank and zero preservation, rational arithmetic, payload bounds, target-bound verification, and malformed-input controls. It does not prove the universal continuum covering theorem, all adaptive testers, or priority.

### R44 required 12 — Independent analytic pipeline

The old A/B/C/D graph and all false aggregate flags remain unchanged. Neither the product-state identity nor the new local testing lemma supplies an analytic closure theorem.

### R44 required 13 — Independent priority

The author-side primary-source audit is extended, including adaptive discrimination and physical population compression. No independent human priority report has been obtained or fabricated. This request remains an external scholarly assessment, not something a regression or a source archive can certify.

### R44 required 14 — Historical volume

The focused article and its native journal archive stand alone. The complete research edition and retained audit/derivation records remain separate research materials in the repository. Moving a result from the focused article to the current complete edition is recorded label by label, not achieved by deleting mathematics.

## Response to the twenty-four detailed comments

### R44 local 01 — Flagged diamond convention

Sections 36/38 explicitly define the norm as the diamond norm of the flagged direct-sum channel, not the sum of outcome-map diamond norms.

### R44 local 02 — Choi normalization

The input-first unnormalized convention, total Choi trace d, and normalized test state d^(-1) direct-sum J remain visible.

### R44 local 03 — Outcome slots and dimensions

The intrinsic s uses all m labeled slots. Removing known zero slots changes the active m; its mask must be supplied. The rank-bound theorem instead keeps fixed slots with r_y=0 allowed, and uses v.

### R44 local 04 — Affine volume

The volume argument is on the real translation space V of the marginal constraint, of dimension s. The rank lower bound uses an explicitly identified locally bi-Lipschitz patch of dimension v.

### R44 local 05 — Validated net

The codebooks are explicitly legal encoder images or validated reconstructions; illegal raw words do not count as legal centres.

### R44 local 06 — Target-bound guarantee

Bare decoding certifies syntax and legality only. Verification re-encodes the supplied target and compares the complete certificate.

### R44 local 07 — Blockwise margin

The margin is the minimum eigenvalue lower bound on every individual outcome Choi block, not on their sum.

### R44 local 08 — Stopping

Draw N programme symbols in advance; a publicly stopping tester ignores the unused suffix. The preparation reduction similarly provides N copies and discards unused ones.

### R44 local 09 — Ancilla dimensions

The metric now explicitly allows fresh ancillas of arbitrary finite dimension. Each tester is finite-dimensional at every slot; there is no common cap over the supremum.

### R44 local 10 — Nonadaptive lower tester

The normalized Choi outputs and repeated binary tests used in the lower bounds are nonadaptive, although the defining supremum allows adaptive testers.

### R44 local 11 — Pair-specific Helstrom tests

The measurement may depend on the two packing points. No simultaneous codebook identification or universal tomography measurement is asserted.

### R44 local 12 — Vanishing error

The new Theorem thm:jointcode68 proves the missing joint term s log2(1/delta), with a remainder uniform in N>=1 and 0<delta<=1/32. This is a new proof from the local binary lemma, not a reinterpretation of the old fixed-error O(1).

### R44 local 13 — Vanishing margin

The general instrument margin a remains fixed. No limit-uniform constant is asserted as a tends to zero. The preparation theorem avoids any positive-margin premise by a different factor argument.

### R44 local 14 — Boundary exponents

The old unitary phase obstruction remains active. The new rank theorem describes the preparation family only; general Choi-rank/tangent-cone directions are separately formulated as unresolved extensions.

### R44 local 15 — Validation complexity

The exact Schur/minor lemma is included in the focused proof. Polynomial validation is not called polynomial construction of a minimum net in variable dimensions.

### R44 local 16 — Fixed-length padding

Conceptual leading-zero padding is included in a fixed-length payload. Canonical hexadecimal interchange omits redundant leading zeros without changing that capacity bound.

### R44 local 17 — Zero masks

The inherited preserve_zeros option needs its active-outcome mask and effective dimension. The new triangular pivot mask is separately counted; labeled zero outcomes remain present.

### R44 local 18 — Memoryless reuse

The decoded instrument is fixed and reused. The tester’s quantum memory is not part of the classical description and is not being simulated by that code.

### R44 local 19 — Processor hardware

No universal programmable-processor hardware dimension follows without an additional physical implementation theorem.

### R44 local 20 — Build evidence placement

Detailed source hashes, tests, logs and preservation records are in the research/evidence package, not the main mathematical exposition.

### R44 local 21 — Unsigned provenance

No cryptographic author signature is claimed. The exact hashes and read-only CI are source identity evidence only.

### R44 local 22 — Alias order

The release procedure freezes the final request, verifies that exact head, then creates the referee alias at the same commit.

### R44 local 23 — v63 gap

All earlier width-crossover statements and their multiplicative gap remain in the complete edition. The new description laws concern a different invariant.

### R44 local 24 — Pipeline flags

No successful syntax, arithmetic, raster, hash or code-length check changes any A/B/C/D aggregate flag.

## Evidence and retained development

The source package retains `RESPONSE_TO_R43_INITIAL.md` and the inherited v67 audit material. `PRESERVATION_MANIFEST.json` binds all 115 predecessor native files, all 394 previously active complete-edition labels, and every focused-to-complete proof relocation. Actual executed results are supplied by the source-build and read-only final-head receipts. Written mathematics, exact finite regression, source identity, independent priority, authorship and editorial acceptance remain separate assertions.
