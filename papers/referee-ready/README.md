# θ-Theory five-paper series — referee revision v4

This directory contains the five controlling manuscripts revised in response to
the 2026-08-29 referee reports.

## Controlling branch

```text
theta-referee-revision-v4-full-positive-2026-08-29
```

The controlling source in each paper folder is `main.tex`, and the controlling
bibliography is `references.bib`.  Both are promoted copies of the corresponding
round-four files.

## Papers

1. **Paper I — response**  
   *Bilateral Response, Symbolic Desingularization, and All-Order Spectral Jets
   for Nonconjugate Moving Collision Dynamics*

2. **Paper II — pressure and suspension**  
   *Pressure, Physical Diffusion, and Uniform Full-Frequency Suspension
   Response for Moving Collision Systems*

3. **Paper III — homogenization and theta**  
   *Exact-Innovation Rough Homogenization and Microscopic Construction of
   Theta-Semigroups from Nonconjugate Collision Dynamics*

4. **Paper IV — filtering and games**  
   *Noncompact Filtering, Curvature-Compensated Pure Isaacs Games, and
   Deterministic Multiscale Limits*

5. **Paper V — representations**  
   *Tangent-Law Characterization and Stochastic Representations of
   Theta-Semigroups*

## Common actual chain

The same nonconjugate symplectic moving collision map carries:

```text
all-order response
 -> pressure / symmetric physical covariance / full-frequency suspension
 -> exact-innovation rough homogenization
 -> pointwise microscopic HJB / controlled theta-semigroup
 -> noncompact filtering / pure Isaacs game
 -> microscopic tangent laws / Girsanov / BSDE / PPDE.
```

An independent analytic no-eclipse open-billiard branch provides a genuine
moving specular all-order response and Dolgopyat strengthening.

See:

- `COMMON_ACTUAL_PLATFORM_V4.md`;
- `REVISION_V4_RESPONSE_TO_REFEREES.md`;
- `REVISION_V4_THEOREM_MANIFEST.yaml`;
- `REVISION_V4_HOSTILE_PROOF_AUDIT.md`;
- `REFEREE_REVISION_V4_STATUS.md`.

## Verification

From the repository root:

```bash
python3 tools/verify_referee_revision_v4.py --write-receipt
make -C papers/referee-ready all
```

The verifier checks structure, citations, labels, promoted controlling files,
dependency anchors, and finite-dimensional formulas.  LaTeX compilation and
formula checks do not certify the analytical proofs.

## External-review package

For each specialist referee, provide:

- that paper's `main.pdf`, `main.tex`, and `references.bib`;
- that paper's `REFEREE_GUIDE.md`;
- the immediately required companion preprint;
- `REVISION_V4_RESPONSE_TO_REFEREES.md`;
- the formal report template.

The revision has not yet received its second independent formal report, and no
journal acceptance or external correctness certification is claimed.
