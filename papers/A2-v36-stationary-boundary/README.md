# A2 v36: stationary boundary queries and unknown scale recovery

**Qian Qi · 4 October 2026**

Primary article: *Scalar collision laws and recognition of periodic dispersing billiards*.

This revision responds to the latest v35 report at **985d798e172d38c0a9df2a068fe414b2fd13bcbc**, which reviewed the canonical stationary author source **70c055e1ff090d58ecd61a5644e0fa62a7766f13**. The new branch starts from that review and preserves all existing manuscript directories.

- Author branch: revision/a2-v36-stationary-boundary-2026-10-04.
- Referee-copy branch: revision/a2-v36-referee-copy-2026-10-04.

## Mathematical changes

**A faster stationary boundary query.** Proposition 4.2 (prop:rare-query) takes the conjunction of at most two translated pooled-forward collision tests. A true outward compass maximizer gives an exactly zero collision probability at an exterior target. Every selected candidate has probability at least a constant times \(e^{\gamma+3/2}\) at inner depth \(e\). A finite batch therefore costs \(e^{-(\gamma+3/2)}\), rather than the squared inverse signal needed for the signed reciprocal estimator. Direction outcomes remain unobserved. The fixed dyadic compass step satisfies \(2t+D_*<d_0\); earlier results under weaker separation remain active.

**An unknown homothety ratio.** At two stationary settings, neither the footprint nor the ratio \(r\) is supplied. For an isolated original component \(C\), the observed pooled-forward mean satisfies
\[
\Phi_C=\int_E F_1=\frac t2\mathcal W(C),\qquad
\mathcal W(C)=p_C(e_1)+p_C(-e_1)+p_C(e_2)+p_C(-e_2).
\]
Writing \(P_1=C+Q,\ P_2=C+rQ,\ D=(r-1)Q\), Theorem 5.2 gives
\[
a=\frac{\mathcal W(P_1)-2\Phi_C/t}{\mathcal W(D)},\quad
r=1+a^{-1},\quad p_Q=a p_D,\quad p_C=p_{P_1}-a p_D.
\]
The denominator has a fixed positive lower bound. Theorem 5.5 independently identifies the ratio from the two reciprocal differences alone, through occupation area and a mixed-area quadratic under weaker separation. Proposition 5.7 gives a finite killed-walk adjoint for that area.

**A joint resource theorem.** Theorem 5.4 reconstructs the table, the physical first-setting footprint and the unknown ratio, with the original uniform finite primitive-period conclusion. For \(s=6+\beta,\ 0<\beta\le1\), its attempted-bit bound is
\[
N_\nu\le C\nu^{-((\gamma+3/2)s+1)/(s-2)}
\log(C/\nu)\log(C/(\nu\delta))
+C\nu^{-2}\log(C/\delta).
\]
The scalar-measurement term is lower order because the leading power exceeds two. Its additional nominal centers are explicitly charged, and the theorem separately bounds the description of centers, setting indices and repetition counts. The finest nominal mesh is \(O(\nu^{s/(s-2)})\).

For a density bounded below on its footprint, the upper power improves from \((3s+1)/(s-2)\) to \((3s/2+1)/(s-2)\). The retained common-uniform-disk expected-attempt lower power is \((s+1)/(s-2)\). The remaining exponent difference is \(s/(2(s-2))\), one quarter of the previous difference. A matching minimax exponent is not asserted.

Exact homothety about the fixed common laboratory origin, quantitative footprint and boundary-mass priors, and nominal positioning remain specified resources. The recovered physical first-setting footprint is distinguished from an arbitrary latent scale normalization. Uniform finite period decisions retain the known positive nonperiod-patch margin.

## Reading and preservation

The primary is one self-contained amsart article with nineteen core inputs and its bibliography. Principal stationary results occupy Sections 2–6. Complete localized, control, period-recognition, packing and calibration results remain in Appendices A–H. No supplementary manuscript is required.

The controlling v35 source has 36 formal statements, 33 proofs and 117 labels. All 117 labels remain active, and all 33 old proof bodies are retained byte for byte. The revision has 46 formal statements and 43 proofs. Its title and collision-law topic are unchanged. Earlier v35/v34 directories and the controlling review are pinned by Git tree identity.

The native draft build produced 48 pages with no final TeX warnings, unresolved references or overfull/underfull boxes. Current diagnostic counts and exact-commit qualification are recorded by the generated receipt; no historical diagnostic or hosted-build result is reused as current evidence.

## Reproduction

Requirements: Python 3 with its standard library, latexmk, pdflatex and the packages in main.tex, and Poppler pdfinfo.

From this directory at a clean checked-out revision commit:

    python3 tools/validate_v36.py --expected-head "$(git rev-parse HEAD)"

For an explicitly uncommitted editing run:

    python3 tools/validate_v36.py --allow-dirty

SOURCE_PINS.json is the frozen source manifest. The validator rejects missing, altered and unexpected active files, verifies inherited tree/content preservation, runs finite diagnostics and contract checks in ordinary and optimized Python, builds the actual primary, and retains a receipt and available logs even on failure. A maintainer changes the manifest only after reviewing intended source changes:

    python3 tools/validate_v36.py --freeze-manifest

Generated outputs are under verification/current/: the primary PDF, journal and repository source ZIPs, logs, finite-check output and receipt.json. The workflow .github/workflows/a2-v36-verify.yml checks out its triggering SHA and uploads available evidence on success or failure. A development receipt never qualifies a Git commit. Finite diagnostics test their stated algebraic and finite-model scope; they do not certify continuum proofs or validate an apparatus.
