# A2 v40 — joint recovery from two fixed collision fields

**Qian Qi, _Scalar collision laws and recognition of periodic dispersing billiards_.**

This revision responds to the latest [v39 referee report](https://github.com/TrillionniumFoundation/theta-theory/blob/790654161f2f069fb4d1d1ee18bfe86ea5290d74/reviews/a2-v39-external-harsh-top4-rereview-2026-10-04/REFEREE_REPORT.md). Its parent is the completed review commit `790654161f2f069fb4d1d1ee18bfe86ea5290d74`; the reviewed author commit is `f815a7acdb5c03e03b9996fc7052b405db66936d`.

## Read the revision

The submission has two independently compiled documents:

- [main.tex](main.tex): the focused primary article, proving the new two-field exact inverse, finite geometry, finite launch-law recovery and response prediction.
- [companion.tex](companion.tex): the complete retained mathematical programme, including all 32 v39 core files, all 322 baseline labels and all 76 baseline proof bodies. The prior statements retain their individual hypotheses.

The two PDFs are named `A2-v40-primary.pdf` and `A2-v40-companion.pdf`. They cross-reference one another with distinct label prefixes. [SUBMISSION_MAP.md](SUBMISSION_MAP.md) gives the reading order and proof dependencies. [RESPONSE_TO_REFEREES.md](RESPONSE_TO_REFEREES.md) answers the controlling report item by item. [PROOF_LEDGER.md](PROOF_LEDGER.md) lists every new proved block and the preserved baseline. The historical and literature audits document attribution and the exact source identities.

## Mathematical changes

The exact datum is now the ordered pair of spatial fields

\[
F_+(x)=\int B_{te}(x+z)\,d\mu(z),\qquad
F_-(x)=\int B_{-te}(x+z)\,d\mu(z),
\qquad x\in\mathbb R^2,
\]

with **one fixed positive length and two fixed opposite forward commands**, at the same unknown stationary law. The fields remain continuum spatial data. No angular command sweep or length limit is supplied. Solids, boundary contacts and attempted-bit denominators retain the original convention.

The exact theorem allows nonsmooth strictly convex obstacles and any compact probability law with a nonempty convex support, including singular, atomic and lower-dimensional cases. The size condition is `t + diam(A) < d`, where `d` is the obstacle separation. A finite prefix formula recovers occupation. Three support functions cancel the footprint, leaving the support difference of an obstacle and its transverse contact chord. Strict convexity makes the obstacle curvature measure nonatomic, while the chord has two atoms; their signed-measure separation recovers geometry. An isolated compact occupation convolution then recovers the entire probability law. The complete ambiguity is common translation, and the two fields determine all forward responses and the full obstacle period group.

For the separate quantitative smooth class, the same fixed commands yield geometry with sufficient power

\[
Q_{\rm pair}=\frac{(\gamma+9/2)s}{s-2},\qquad s=6+\beta,
\]

and attempted-bit bound

\[
N_\nu\le C\nu^{-Q_{\rm pair}}
\log(C/\nu)\log(C/(\nu\delta)).
\]

At `gamma = 0`, `s = 7`, the exponent is **6.3**, compared with the retained v39 sufficient exponent **18.9**. The fixed-law sharp benchmark in the companion concerns a different experiment. No optimality of the new joint rate is asserted.

The finite law theorem gives `W1` error `C epsilon` at sufficient cost

\[
\exp\!\bigl(C\varepsilon^{-1}\log(C/\varepsilon)\bigr)
\log^2(C/\delta).
\]

It also predicts all bounded-length responses in local spatial `L1`. A known BV bound on the zero-extended density gives density `L1` recovery and uniform raw response prediction on every fixed bounded window, with `epsilon^{-2}` replacing `epsilon^{-1}` in the exponential bound. These finite statements use their declared geometric and boundary-mass priors; the exact nonsmooth class is not treated as a uniform statistical class. Finite primitive-period decisions retain a positive patch margin. A complete finite configuration instead requires a complete protected aperture.

## Build and verify

The repository workflow is [a2-v40-verify.yml](../../.github/workflows/a2-v40-verify.yml). It captures fixed sources immediately after checkout, before installing TeX, and retains failed-execution evidence as well as successful evidence. Both PDFs are compiled together in a fresh auxiliary directory until their cross-references stabilize.

From this directory, after source edits:

```bash
python3 tools/validate_v40.py --freeze-manifest
python3 tools/validate_v40.py --allow-dirty
```

The development mode does not qualify a Git commit. After committing, qualify the exact intended SHA:

```bash
python3 tools/validate_v40.py --expected-head FULL_40_CHARACTER_SHA
```

`SOURCE_PINS.json` hashes the complete submitted source and workflow, declares both executed TeX input closures and pins nine preserved historical trees. The qualifier checks committed bytes and the worktree, preservation of every v39 proof body, ordinary/optimized Python parity, both final TeX logs and recorders, stable references, and PDF metadata. A declared `xr-hyper` reference can probe the other entry file for existence; the recorder contract identifies that specific metadata probe separately. It cannot replace a missing mathematical input or admit an unrelated source file. Generated build and verification files are excluded from source tracking.

The workflow artifact contains both PDFs, both final logs and recorders, a journal-source archive, a complete pinned-source archive, the manifest, receipt and run binding. The receipt, rather than this source README, records the exact qualified SHA, final counts and generated-file digests. Finite diagnostics are checks of finite identities and resource algebra; they do not certify the continuum proofs or a physical instrument.

## Revision branches

The author branch is `revision/a2-v40-joint-response-2026-10-04`; its referee-copy alias is `revision/a2-v40-referee-copy-2026-10-04`. Both are intended to resolve to the same source commit. Earlier author papers and review directories are preserved. The revision makes no change to the article's topic or author identity.
