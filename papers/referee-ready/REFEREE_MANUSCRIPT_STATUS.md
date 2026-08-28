# θ-Theory referee-manuscript status

**Date:** 2026-08-28  
**Branch:** `theta-referee-manuscripts-2026-08-28`  
**Base:** `theta-maximal-strengthening-closure-2026-08-28`  
**Scope:** θ-Theory only

## Deliverable status

```yaml
standalone_paper_folders: 5
standalone_main_tex_files: 5
paper_specific_bibliographies: 5
paper_specific_referee_guides: 5
paper_specific_build_notes: 5
series_manifest: COMPLETE
series_referee_guide: COMPLETE
structural_verifier: COMMITTED
latex_workflow: COMMITTED

main_tex_sizes_bytes:
  paper_I: 30110
  paper_II: 26045
  paper_III: 28574
  paper_IV: 28879
  paper_V: 28759
  total: 142367

internal_packet_language_in_main_tex: REMOVED_BY_DESIGN
companion_dependency_order: ACYCLIC_BY_DESIGN
reverse_representation_dependencies: FORBIDDEN
external_peer_review: NOT_PERFORMED
mathematical_correctness_certified_externally: false
formal_credit: 0
```

## Manuscript content

### Paper I

A self-contained response paper containing the bilateral product-tail theorem,
finite-DQ convergence in the complete two-time topology, CM2-to-U3
totalization, the open four-branch moving-seam realization, the nonconjugate
radial specular projector/source response, and maximality/no-go results.

### Paper II

A self-contained physical-response paper containing finite-atlas Banach-bundle
stabilization, joint pressure response, the physical-time pressure root,
oriented suspension renewal, the pressure/Green--Kubo/martingale covariance
identity, coefficient lift, ellipticity, actual positive diffusion, uniform
high-frequency BDL bounds, and exact similarity-family response.

### Paper III

A self-contained rough-homogenization paper containing causal Doob selection,
the martingale--rough package, the qualitative-versus-quantitative distinction,
full-scale nonautonomous homogenization, an actual selected four-branch model,
a sharp Gaussian fractional-Sobolev rough-path Wasserstein rate, HJB
convergence, the theta-semigroup, and a non-subadditive example.

### Paper IV

A self-contained filtering/game paper containing bounded and weighted filter
stability, the vanishing slow initial layer, strategy-tree estimates,
sequential lower/upper limits, mixed relaxed Isaacs, the exact pure-saddle
criterion, a noncompact strong concave--convex theorem, the actual four-branch
game, and an actual Gaussian noncompact filter.

### Paper V

A self-contained representation paper containing the single-law obstruction,
exact jet calibration, Feynman--Kac, FBSDE/control/game/2BSDE typing, PPDEs, an
actual entropic pure path game with completed-square verification and quadratic
BSDE, and an actual volatility-control PPDE/2BSDE branch.

## Build attempt

The repository workflow created six jobs: one structural job and five LaTeX
matrix jobs.  GitHub returned every job with `runner_id=0`, an empty step list,
and failure before checkout or any command execution.  Therefore:

```yaml
github_runner_allocated: false
structural_script_executed_in_actions: false
latex_compilation_executed_in_actions: false
failure_classification: INFRASTRUCTURE_BEFORE_STEPS
```

No compilation success or failure is inferred from those workflow records.  A
clean checkout with TeX Live should run:

```bash
python3 tools/verify_referee_manuscripts.py
make -C papers/referee-ready all
```

## Review boundary

The manuscripts are ready to be handed to external specialists as formal proof
drafts.  They are not represented as accepted, externally certified, or
journal-ready without changes.  Human authors remain responsible for
line-by-line proof verification, novelty assessment, bibliography validation,
authorship metadata, and journal-specific disclosure.
