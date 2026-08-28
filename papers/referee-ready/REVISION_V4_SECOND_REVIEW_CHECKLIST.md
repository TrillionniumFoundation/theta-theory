# Second formal review checklist — θ-Theory revision v4

Use this checklist before sending any manuscript to a second-round referee.
The purpose is to ensure that the referee reviews the controlling v4 theorem,
not the obsolete monograph or an earlier `main-v2`/`main-v3` snapshot.

## 1. Branch and source identity

Confirm that the circulated package comes from:

```text
theta-referee-revision-v4-full-positive-2026-08-29
```

For every paper, confirm:

```text
main.tex == main-round4.tex
references.bib == references-round4.bib
```

The main source invokes `references-round4.bib`; `references.bib` is the
delivery mirror.

## 2. Required series documents

Include:

- `REVISION_V4_RESPONSE_TO_REFEREES.md`;
- `COMMON_ACTUAL_PLATFORM_V4.md`;
- `REVISION_V4_THEOREM_MANIFEST.yaml`;
- `REVISION_V4_APPENDIX_THEOREM_MANIFEST.yaml`;
- `TECHNICAL_APPENDICES_V4.md`;
- `REVISION_V4_HOSTILE_PROOF_AUDIT.md`;
- `REVISION_V4_LOCAL_VERIFICATION_RECEIPT.json`;
- `FORMAL_REFEREE_REPORT_TEMPLATE.md`.

Do not circulate the old monograph report branch as if it were the revised
manuscript.

## 3. Paper-specific packages

### Paper I

Send:

```text
paper-I-bilateral-response/main.pdf
paper-I-bilateral-response/main.tex
paper-I-bilateral-response/references-round4.bib
paper-I-bilateral-response/technical-appendix-v4.pdf
paper-I-bilateral-response/technical-appendix-v4.tex
paper-I-bilateral-response/REFEREE_GUIDE.md
```

Ask the referee to state separately whether the review covers:

- the crossed product-tail theorem;
- the explicit symplectic collision response;
- arbitrary-source susceptibility and exact innovations;
- analytic symbolic desingularization/open-billiard response.

### Paper II

Send the analogous main files plus:

```text
paper-II-pressure-diffusion/technical-appendix-v4.pdf
paper-II-pressure-diffusion/technical-appendix-v4.tex
```

Ask for separate conclusions on:

- pressure/Green--Kubo/physical-root formulas;
- scalar--quotient Diophantine full-frequency response;
- moving open-billiard temporal-shear/Dolgopyat theorem;
- triangular Lorentz geometry.

### Paper III

Send the main files plus both:

```text
paper-III-rough-theta/technical-appendix-v4.pdf
paper-III-rough-theta/physical-clock-appendix-v4.pdf
```

Ask for separate conclusions on:

- exact innovations and geometric rough lift;
- state-dependent homogenization;
- random physical clock and inverse-clock theorem;
- physical-time semi-Markov theta DPP;
- controlled theta-semigroup and theta-independence;
- sharp rough Wasserstein rate.

### Paper IV

Send the main files plus:

```text
paper-IV-filtering-games/technical-appendix-v4.pdf
paper-IV-filtering-games/technical-appendix-v4.tex
```

Ask for separate conclusions on:

- noncompact filter contraction and posterior moment ball;
- slow initial layer;
- constrained curvature-compensation VI;
- lower/upper scheme convergence;
- continuous-time pure feedback verification.

### Paper V

Send the main files plus:

```text
paper-V-representations/technical-appendix-v4.pdf
paper-V-representations/technical-appendix-v4.tex
```

Ask for separate conclusions on:

- parabolic terminal-map differentiability;
- static and dynamic tangent-law characterization;
- microscopic tangent-law convergence;
- Novikov/BMO Girsanov theorem;
- BSDE/PPDE/path-game branches;
- stable-volatility 2BSDE branch.

## 4. Cross-paper consistency questions

Every referee with access to more than one paper should check:

1. the branch widths and parameter interval in Papers I--III;
2. the equality between Paper II's pressure covariance and Paper III's
   predictable bracket;
3. the roof normalization and physical-clock theorem;
4. the common terminal PDE sign in Papers III--V;
5. the pure energy Hamiltonian in Papers IV--V;
6. the fact that Paper V's finite tangent laws tilt Paper III's exact finite
   collision recursion;
7. the absence of reverse dependencies from representations to HJB or from
   games to the one-player HJB.

## 5. Author metadata and disclosure

Before circulation, the human author must confirm:

- author name and order;
- affiliation and contact email;
- funding and conflict disclosures;
- final AI/LLM disclosure required by the chosen journal;
- every bibliography record and DOI;
- every companion-paper title and public preprint identifier.

The current metadata must not be assumed correct solely because it appears in
the repository.

## 6. Executed build gate

The clean-checkout gate has passed for:

```yaml
main_manuscripts: 5/5
normative_appendices: 6/6
fatal_errors: 0
undefined_citations: 0
undefined_references: 0
rerun_warnings: 0
overfull_boxes: 0
underfull_boxes: 0
```

Before external transmission, copy the PDFs from the verified build or rerun:

```bash
python3 tools/verify_referee_revision_v4_final.py
make -C papers/referee-ready all
```

## 7. Review-status language

Permitted before the new reports return:

```text
revised formal proof draft
clean-checkout structural verification passed
LaTeX build passed
prepared for second independent formal review
```

Not permitted:

```text
externally certified
referee accepted
journal-level correctness established
Annals/Inventiones/JAMS/Acta standard confirmed
accepted for publication
```

## 8. Minimum acceptable referee response metadata

Ask each referee to identify:

- exact manuscript hash or branch/commit reviewed;
- pages or theorem labels checked;
- specialist scope;
- whether the report is a full correctness review, partial specialist review,
  novelty/significance review, or exposition review;
- every remaining major, minor, or editorial issue;
- explicit recommendation for a fresh submission, not for the obsolete
  snapshot.
