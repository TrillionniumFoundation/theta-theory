# A2 v39 — single-law response rigidity

**Qian Qi, _Scalar collision laws and recognition of periodic dispersing billiards_.**

The complete article is [main.tex](main.tex). This revision responds to the
[v38 external report](https://github.com/TrillionniumFoundation/theta-theory/blob/5dd7a7e346a9d31d7541efe791335d4e965cadb0/reviews/a2-v38-external-harsh-top4-rereview-2026-10-04/REFEREE_REPORT.md)
at review commit `5dd7a7e346a9d31d7541efe791335d4e965cadb0`, which reviewed
author commit `a346669928e5147cf2c0ef86c3bc2a455b512d14`.
The new branch begins at that review commit, so the reviewed manuscript,
the controlling report and the historical derivations remain in its ancestry
and in their original repository directories.

- Author branch: `revision/a2-v39-response-rigidity-2026-10-04`.
- Referee-copy branch: `revision/a2-v39-referee-copy-2026-10-04`.
- Manuscript directory: `papers/A2-v39-response-rigidity`.

The delivery uses the same source commit on both revision branches. The
exact commit and hosted build result are recorded by the execution receipt;
this README does not predeclare a future workflow outcome.

## The principal theorem

The experiment still returns one first-collision bit per attempted
preparation. A single stationary launch density is unknown. Nominal
centers, directions and positive command lengths are controlled, and the
exact datum is the full directional short-flight germ

\[
q_\theta=\lim_{t\downarrow0}t^{-1}F_{t,\theta}
\quad\text{in }L^1_{\mathrm{loc}}.
\]

For a boundary point \(c_C(\phi)\) with outward normal angle \(\phi\)
and curvature radius \(r_C(\phi)\), angular differentiation gives

\[
(\partial_\theta^2+1)q_\theta(x)
=\sum_C\sum_{\sigma=\pm1}
r_C(\theta+\sigma\pi/2)
j(c_C(\theta+\sigma\pi/2)-x).
\]

Under the uniform antipodal-copy separation of Theorem 2.3, the spatial
support components are translated, reflected copies of the launch
footprint. Their masses, Steiner points and normalized densities
recover the footprint, the entire launch density almost everywhere, and
the obstacle boundaries in one common translation gauge. Theorem 2.3
first proves this directly when every antipodal pair is separated.
Theorem 2.6 extends exact recovery to the assumptions
\(\operatorname{diam}A\le\Delta<d\) and the existence of one obstacle
with diameter greater than \(\Delta\); the other obstacles need not
satisfy a uniform lower width bound. The configuration is nonempty,
locally finite, uniformly bounded in component diameter, positively
separated, and has strictly convex \(C^2\) components of positive curvature.

The common translation is the complete observational fiber. The germ
determines all finite-length forward responses and the full obstacle
translation-period group, without a periodicity prior. There is one
unknown launch setting; neither exact homothety between settings nor a
separately prescribed reciprocal preparation is an input to this theorem.
The controlled directional germ is an active whole-field datum.

## A finite experiment and the retained sharp benchmark

Theorem 3.3 gives finite forward-only recovery of the centered footprint
and periodic obstacle geometry under quantitative smoothness,
boundary-mass, uniform angular-copy separation and positive patch-margin
priors. Spatial and angular regularization, finite rational commands,
their deterministic bias, and a signed Bernstein estimator are all
included in the proof. No upper bound or continuity modulus for the
unknown density is used.

For \(s=6+\beta\), its sufficient attempted-bit bound is

\[
N_\nu\le C\nu^{-Q_\gamma}\log\frac{C}{\nu\delta},
\qquad Q_\gamma=\frac{(3\gamma+27/2)s}{s-2},
\qquad S_\nu\le J_\nu\le N_\nu.
\]

Here \(J_\nu\) counts command-labelled occurrences, including revisits,
and \(S_\nu\) counts distinct nominal sites. The theorem also specifies
the command length, coordinate mesh and total binary description. Its
nominal aperture is prior-bounded; a prior bound on the actual physical
aperture additionally requires a coarse bound on the launch offset.
Corollary 3.4 recovers a finite nonperiodic configuration from a complete
protected aperture without a patch-margin or periodicity assumption.
These finite statements estimate geometry; exact density identification
in Section 2 is not asserted to have a uniform strong-norm finite rate
over arbitrary \(L^1\) densities.

Section 4 retains the known-uniform-disk minimax exponent
\((3s/2+1)/(s-2)\), with one logarithmic factor between the upper and
lower bounds. Its fixed-law comparator and the new joint unknown-law
experiment have separate hypotheses and rates.

## Article organization and retained mathematics

Sections 1–5 contain the experiment, the single-law exact inverse, its
finite realization, the fixed-law minimax benchmark and the comparison
with earlier work. Appendices A–Q contain the complete earlier
occupation, stopping, stationary, calibration, registration, period,
localized-control and information arguments.

All 29 previously active v38 TeX files remain active. All 265 reviewed
labels and all 66 reviewed proof bodies are retained; the proof bodies
are byte-identical. The current primary has 34 active TeX files, 32 core
inputs, 322 labels, 76 proof environments and 79 formal theorem, lemma,
proposition or corollary blocks. There are ten new proved results.

- [Response to referees](RESPONSE_TO_REFEREES.md): all seven section 9
  requests and the substantive response to the conceptual assessment.
- [Proof ledger](PROOF_LEDGER.md): new proof chain, delicate steps,
  retained results and diagnostic scope.
- [Historical derivation audit](HISTORICAL_DERIVATION_AUDIT.md): source
  chronology and the observation models of the inherited arguments.
- [Literature audit](LITERATURE_AUDIT.md): primary sources and the
  distinction between classical transforms and the present inverse.
- [Submission map](SUBMISSION_MAP.md): the primary, supporting files,
  proof dependencies and reproducible delivery.
- [Source pins](SOURCE_PINS.json): the complete source manifest and
  immutable review and historical-tree identities.

## Reproduction

From this directory in the delivered clean checkout:

```sh
python3 tools/validate_v39.py --expected-head "$(git rev-parse HEAD)"
```

The validator checks the exact committed bytes, active input closure,
historical tree identities, labels, citations and preservation of every
reviewed proof. It runs the finite diagnostics and qualification-contract
tests in ordinary and optimized Python, requires identical outputs, and
builds the complete primary with native LaTeX. Evidence is written under
`verification/current/`, including the PDF, two source archives, final
TeX log, source pins and receipt. The workflow
`.github/workflows/a2-v39-verify.yml` binds this evidence to its triggering
SHA and retains evidence after a failed qualification as well.

The finite diagnostic program contains 622,976 checks: 606,502 retained
v37 checks, 1,796 retained v38 checks and 14,678 new checks. The separate
qualification-contract suite contains 66 tests. These finite models and
source checks accompany the written continuum proofs; they do not
constitute formal proof certification or physical sensor execution.
