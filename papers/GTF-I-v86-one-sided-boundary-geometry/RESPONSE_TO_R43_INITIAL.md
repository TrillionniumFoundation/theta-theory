# Response to the controlling v66/r43 reports — Revision 68

**Quantitative manuscript:** *Joint Instrument Coding Laws and Boundary-Uniform Rational Realization*.
**Structural companion:** *Finite Physical Actions and a Strong Converse for Repeatable Observations*.
**External report:** `0a3d74582eeeda315237ee73fdd2ac0021862184`.
**Companion proof/pipeline audit:** `6c2aee0e242668ff960f3bf4835c87923b8e730f`.
**Immediate mathematical predecessor:** qualified v67 publication `98a4b12126502ea41c620b58bad4b9aa30f9c72c`.

The controlling reports review v66. The intervening v67 manuscript was already remotely published and qualified when this revision began; its intrinsic coordinate code, positive-body fixed-error entropy theorem and supporting proofs are inherited, not called new or externally endorsed here. The general-journal mathematical objective is unchanged. We respond by proving sharper statements and supplying exact constructions rather than changing the target or removing results.

## Principal mathematical response

The referee identified the lack of a matching precision law and of a boundary theory beyond safe positive-buffer upper bounds. The new Section 40 proves a small-separation binary testing estimate valid even at probability endpoints. It yields a local repeated-Choi lower bound, which combines with the inherited exact intrinsic codec to determine

    (s/2) log2 N + s log2(1/delta) + O_(d,n,m,a)(1),
    s=d^2(mn^2-1), N>=1, 0<delta<=1/32.

Unlike the v67 fixed-error asymptotic, the additive remainder is independent of both N and delta. The hypotheses are explicit: dimensions and a positive Choi margin are fixed; one decoded memoryless instrument is reused; a common adaptive quantum tester can hold arbitrary references/memory and stop publicly before N uses. No action spectral gap is needed.

Section 41 establishes a separate boundary-complete law for preparation instruments R_y(X)=tr(X)sigma_y, including zero outcomes and all ranks up to public bounds. With v=sum_y r_y(2n-r_y)-1, the optimal rational and unrestricted legal descriptions both have length

    (v/2) log2 N + v log2(1/delta) + O_(m,n,ranks)(1).

Here no positive eigenvalue margin is assumed. All adaptive tests reduce exactly to the product-state experiment. A singular triangular-factor chart has at most v+1 real coordinates on a unit sphere; fixing one ratio anchor removes its radial coordinate. The resulting rational code preserves every zero target outcome and never increases an output rank. Its encoder compares rational squared coordinates and computes only integer square roots, without representing irrational factors. A rank-stratum packing and the local binary test prove the matching converse. Full prepared states, pure states and classical outcome distributions give coefficients n^2-1, 2n-2 and m-1, respectively.

These results are description theorems, not general mutable-workspace lower bounds. The boundary family erases its input; arbitrary disturbing instruments need not obey the same product reduction. The inherited unitary phase example remains and explains this distinction. Dimension constants, general boundary classification and the separate v63 multiplicative width gap are not silently declared resolved. The classical ingredients and quantum-population-coding antecedent are credited explicitly.

## Fifteen required revisions

### R43 required 01 — Focused manuscripts

The quantitative and structural proof graphs remain independent. The complete research edition retains all 394 prior labels; every one of the 115 predecessor native files remains at its original path. The new Sections 40–41 augment rather than delete the previous work.

### R43 required 02 — Reference-sensitive simulation

The Naik–Zartab–Gisin–Banik comparison remains in the common bibliography and quantitative discussion. The new preparation processor is explicitly a quantum channel supplied with quantum programme states, not a finite-classical-message physical simulator of unknown entangled input.

### R43 required 03 — Independent priority

The primary-source audit now additionally compares quantum population compression (Yang–Bai–Chiribella–Hayashi), including its unknown-copy and hybrid-memory interface. This author-side comparison does not manufacture the independently commissioned expert report requested by the referee.

### R43 required 04 — Operational interface

The first page distinguishes reusable description coding, specified-matrix numerical simulation, physical action on unknown input and transcript-only tasks. Public family parameters and target-dependent payload are specified. The same memoryless instrument and common tester are used throughout.

### R43 required 05 — Upper/lower asymmetry

The general variable-description trajectory theorem remains an upper theorem. The matching new results are precise description laws: a uniform joint law on positive Choi bodies and a rank-stratified law throughout the preparation boundary. Neither is substituted for a general mutable-workspace converse.

### R43 required 06 — Dimension and accuracy

Section 40 determines both horizon and precision coefficients with a remainder independent of N and delta. Section 41 gives the coefficient v=sum r_y(2n-r_y)-1 and an explicit finite full-body lower constant. Dimension-dependent constants and validation exponents remain nonoptimal.

### R43 required 07 — Preprocessing

The inherited bordered-minor validation proof is retained. New factor digits are computed from exact rational squared coordinates, with integer square roots; the algorithm never stores irrational factors. Preprocessing and expanded matrices are not identified with the optimal payload.

### R43 required 08 — Expected time and storage

The new codec is deterministic. The inherited rejection sampler retains expected-time/fresh-bit and worst-case per-trial storage distinctions; no blanket efficient-simulation claim is made.

### R43 required 09 — Rare posterior

The existing true-law weighted, tail and pooled-event bounds, including fallback states at zero simulated mass, are retained. Product-state and joint tester bounds do not imply simultaneous control of every rare normalized branch.

### R43 required 10 — Positivity language

Positive semidefinite matrices with Gaussian-integer entries is used throughout the new construction. Integer triangular factors themselves need not be positive matrices; it is their products that are PSD.

### R43 required 11 — Spectral hypotheses

No action spectral gap is used in Sections 38–41. The old width and fixed-program streaming lower bounds retain full Koopman and all-direction cap hypotheses. Choi eigenvalue margin is not relabelled as an action gap; the preparation boundary theorem needs neither.

### R43 required 12 — Width crossover

The v63 exp(O(sqrt(N log N))) multiplicative uncertainty remains explicitly retained. Sharp coding coefficients for another resource do not close that width problem.

### R43 required 13 — Structural scope

The structural companion remains about fresh repeatable nondisturbing classical probes. The preparation theorem classifies description length in an input-erasing family, not bounded mutable memory for all disturbing processes or POMDPs.

### R43 required 14 — Evidence

Proofs, exact finite tests, rendered pages and source identity have separate records. Hosted reconstruction is not proof-assistant verification, independent priority, cryptographic authorship or journal acceptance.

### R43 required 15 — Wider pipeline

All A/B/C/D aggregate flags remain false. No local coding or bounded-testing statement is represented as raw local-limit, stopped LDP, global-kernel, filtering/LAN, Mosco/Nisio, response or posterior-contraction closure.

## Twenty-four detailed comments

### R43 detail 01 — Tensor convention

The new preparation theorem restates J_y=I_d tensor sigma_y under input-first unnormalized Choi convention. The inherited general integer-contraction formula is unchanged.

### R43 detail 02 — Trace unit ball

The retained Choi/diamond proof includes the rank-one partial-isometry convex-hull/SVD reduction. New lower testing explicitly normalizes by d.

### R43 detail 03 — Lower Choi estimate

The lower Choi direction remains used for intrinsic coding and now supplies the local repeated-use separation bound, with its factor 1/(2d) shown.

### R43 detail 04 — Independent coordinates

The intrinsic s coordinates remain unchanged. The new triangular chart separately counts real diagonals and real/imaginary lower coordinates, removes one radial coordinate, and records singular pivot sets.

### R43 detail 05 — Residual anchor

The old arbitrary outcome/output residual anchor and alternate-anchor checks remain. The new factor anchor is a distinct largest-magnitude coordinate selected by exact squared comparisons.

### R43 detail 06 — Zero outcomes

The generic repair still removes/restores known zeros when required. The new factor construction needs no positive buffer and preserves zero outcomes directly, including at rank-deficient boundaries.

### R43 detail 07 — Description versus learning

Both new cover bounds are deterministic description results. The executable encodes one rational target without enumerating the whole codebook. No unknown-channel learning guarantee is claimed.

### R43 detail 08 — Same tester

The product-state reduction and local tester compare a single common strategy in the two worlds. A metric supremum may choose a tester for the pair, not for knowledge of which hidden world was selected.

### R43 detail 09 — Classical commands

The general inherited tester excludes coherent command superpositions. The new repeated-use statements concern one fixed memoryless instrument; no new coherent command port is introduced.

### R43 detail 10 — Public stopping

A public stopping rule ignores unused programme copies. This is a fixed trace-preserving processor construction, not private simulator-dependent stopping.

### R43 detail 11 — Norm convention

Section 40 uses Bernoulli total variation and explicitly multiplies by two for unhalved trace distance. Section 41 and certificates use unhalved joint-state error throughout.

### R43 detail 12 — Zero simulated mass

The posterior theorem and schemas retain true event probability alpha and arbitrary fallback states at zero simulated mass. No altered conditioning claim is introduced.

### R43 detail 13 — Exact trajectory numerator

The retained algorithm explains omitted common path denominators. Factor-code normalization is different and displayed explicitly as T=sum ||Z_y||_F^2.

### R43 detail 14 — Stored description

The old numerical program charges its full description S. The new optimal index length is not the storage of expanded Choi matrices, an external-ROM model or the encoder workspace.

### R43 detail 15 — Command identifiers

The inherited token cap and longest-identifier accounting remain; the new codec has no live command stream.

### R43 detail 16 — Schur minors

Lemma schurminors67 remains the exact operand-length input. Section 41 uses it for rational residuals; signed factor squares are computed directly, avoiding irrational Cholesky-number storage.

### R43 detail 17 — Zero pivots

The factor codec and proof use the same zero-diagonal/zero-residual-row criterion, without a hidden pivot permutation. Independent Gaussian-rational elimination checks actual ranks.

### R43 detail 18 — Randomness source

OS randomness is not certified as ideal in the retained numerical sampler. The new factor encoder and decoder are deterministic.

### R43 detail 19 — Finite reference tests

All inherited entangled/stopped examples remain tests only. New exact pure-state and classical product checks support the normalization and tensor identities, not arbitrary-tester theorem certification.

### R43 detail 20 — Transpose control

The inherited positivity/TP-versus-CP transpose negative control remains enabled. A further negative control rejects a legal unitary identity channel as not an input-erasing preparation instrument.

### R43 detail 21 — Typesetting

All mathematical material is retained. The build rejects unresolved references/citations and overfull or underfull boxes; ragged-bottom page layout and actual display reflow, not suppressed diagnostics, are used.

### R43 detail 22 — Watrous citations

The inherited precise Choi/diamond citations remain. Section 41 additionally cites Chapter 3 Section 3.2 on fidelity and includes the short purification/product inequality proof with the stated normalization.

### R43 detail 23 — Bibliography

Naik et al. and the current channel-learning sources remain. Yang–Bai–Chiribella–Hayashi is added with a theorem-interface comparison, not a claim to have independently cleared the surrounding literature.

### R43 detail 24 — Signature

No author key or signature is invented. Exact commit genealogy, source/PDF/package digests and an external contents-read-only attestation supply provenance of a different kind.

## Delivery and independent questions

The proofs have named labels and explicit dependencies in PROOF_STATUS.json and PROOF_AUDIT.md. The preservation manifest pins the entire v67 native archive and all prior proof labels. The exact finite suite separately checks binary gaps, factor coordinates, singular pivots, ranks, zero outcomes, product distances, parameter parsing and altered certificates. All five inherited suites remain enabled. Native source and minimal journal packages are reconstructed separately before publication; final-head verification is read-only and stores its attestation outside the reviewed tree.

Independent expert priority review has not been obtained by this author-side source inspection. No cryptographic author signature, formal proof-assistant verification, editorial acceptance or independent analytic-programme closure is claimed. These are separate questions from the written proofs and reproducible implementation submitted for the next referee.
