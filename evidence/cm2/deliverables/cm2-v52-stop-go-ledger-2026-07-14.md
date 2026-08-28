# CM2 v52 stop–go ledger

Date: 2026-07-14  
Status: working research milestone; not a submission manuscript

## Frozen artifacts

- Baseline v51 is frozen and unchanged from the referee copy.
  - `cm2-bridge-note-v51.tex`
  - SHA256: `da0f4ac7a6a914bef07d4e3b05d844803b251cc60f2486f943aca3abed4736bc`
- Working v52 contains the corrections and new lemmas listed below.
  - `cm2-bridge-note-v52.tex`
  - SHA256: `e4fd6c74c4be53ec97287b747e792ec8c32f9cd184cff05047189472481c5daa`
  - Compiled PDF: `cm2-bridge-note-v52.pdf`, 168 pages
  - PDF SHA256: `d570137f20d062f03bf742d2c0c20bce332fd6bc2183b3a5d135f1fdbc315b69`
- Exact certificates:
  - `cm2_fixed_section_geometry_cert.py`
  - `cm2_fixed_section_impact_cert.py`
  - `cm2_fixed_section_qnl_cert.py`
  - `cm2_fixed_section_projective_cert.py`
  - `cm2_fixed_section_common_vertex_cert.py` (`python-flint==0.9.0`)

The first four scripts run without error under the system interpreter.  The
Arb candidate script runs without error in the recorded python-flint
environment and reports `ORBIT_ROOT`, `PHYSICAL_WORD`, and
`TRIVIALIZED_MATRIX_NONDEGENERACY` as certified, while printing
`COMMON_MAGNET` and `GIBBS_PHYSICAL_ID` as not certified.  The projective
script deliberately ends
with `DYNAMICAL COMMON-VERTEX CONNECTOR: NOT CERTIFIED`; its theorem is an
artificial Bernoulli benchmark, not physical PPE.

## What v52 now proves or repairs

### Correctness repairs

1. The scaled-density estimate now has the correct exponential dependence on
   log-density distortion.  Positive amplitude pieces are normalized and their
   masses are absorbed into the coefficient mass before later density bounds.
2. The observable-multiplier recovery clock now pays both the observable
   Hölder norm and the logarithmic density mark.
3. The mixed-cylinder expansion explicitly assumes commuting, exhaustive
   filtrations and projective-norm convergence.
4. The Fourier reduction explicitly assumes the low-frequency centered
   cylinder-mixing estimate used in its proof.
5. Previously schematic notation such as `U_0` and `Y_+` is either defined or
   explicitly demoted from a completed Banach construction.

### Paper 1: moving-singularity current calculus

1. On a compact regular branch, the order-one transport current admits an
   explicit order-zero divergence density, with the boundary current shown
   when the source does not vanish at the boundary.
2. Across a regular radical face, the common-atlas difference quotient
   converges in `(C^{1,alpha})*`; coefficient measures converge in total
   variation on the occurrence atlas.
3. Equal physical traces cancel the switching-face atom before absolute
   values.  The remaining radical envelope is integrable and has
   `O(rho^{1/2})` collar mass.
4. Two distinct regular analytic event germs have a locally integrable
   double-radical envelope even at finite-order tangential contact:
   `O(rho(1+log rho^{-1}))`.  Hence no determinant lower bound is needed for
   such verified vertices.

These results do **not** yet prove global one-return first variation for the
entire fixed-section map.  Coincident genuine factors, critical event germs,
unresolved corner/grazing normal forms, and higher uncancelled multiplicity
remain in the event inventory.

### Paper 2: PPE/nonconcentration

1. The exact local QNL witness remains `-325/72`.
2. In the current context decomposition one can take affine context degree
   `d_Z=1`, so the required terminal finite-type order is two.
3. A real local, parameter-uniform, amplitude-weighted affine escape estimate
   is obtained once the amplitude is normalized in `L^p`.
4. The two exact pilot matrices yield a fully certified separated Bernoulli
   projective system and a finite-time/stationary Frostman bound.
5. Two counterexamples are now explicit:
   - untransported periodic matrices do not certify common-vertex twisting;
   - a nonzero terminal jet seed can be cancelled by later analytic
     continuation.
6. A 400-bit Arb/Krawczyk certificate proves existence and uniqueness of a
   symmetric period-eight fixed-section connector orbit with a 14-collision
   physical word.  It certifies incidence cosine `>3/5`, unintended-obstacle
   clearance `>1/5`, no transparent-wall crossing, its common-coordinate derivative,
   and four nonzero twisting determinants (the smallest is `>3/100`).

The Bernoulli result is a benchmark only.  Actual-SRB, all-parent,
prescribed-depth PPE requires a common Markov vertex, physical connector,
endpoint-slope identification, stopped-parent projective law, and normalized
amplitude moments.

The new candidate closes the periodic-orbit and coordinate-trivialized
four-determinant nondegeneracy layers, but not the common-vertex theorem.
Full-cross source strips in one
magnet, cone/singularity margins, a conditional Gibbs-weight lower bound, and
the physical endpoint-projective identity remain explicitly uncertified.

### Recovery and face time

1. Rare-cell normalized `Z` moments are no longer required.  A global `L^p`
   weight, an unnormalized levelwise `Z` numerator, and a level-mass tail imply
   aggregate shallow/deep recovery bounds with explicit exponent
   `gamma_chi = c_0(1/p' - chi) - a_Z chi`.
2. The local positive entry box has pointwise bounded shape/recovery marks, so
   every outer restriction there inherits all finite moments without dividing
   by rare-cell mass.
3. A same-occurrence bidirectional recovery proposition converts exact
   alternative factorizations plus exponential recovery moments into
   `FACE_TIME_REC`.

The missing primitive is geometric, not a moment inequality: the **same
physical occurrence and coefficient** must admit forward/reverse order-zero
proper-family factorizations, with exact propagated `q` matching.  Separate
entry and exit tags do not suffice.

## Stop–go decisions

| Workstream | Decision | Current boundary |
|---|---|---|
| Paper 1, general/local current calculus | GO | A complete paper can be written, but its pilot application is a verified regular subatlas plus positive core. |
| Paper 1, top-field global pilot theorem | CONDITIONAL GO | Requires a complete one-return radical event inventory and a nonempty open parameter neighbourhood. |
| Projective PPE route | GO TO MAGNET CERTIFICATE | A physical periodic orbit and coordinate-trivialized nondegeneracy are certified; actual connector transport, full-cross strips, weight margins, and endpoint identification remain the kill test. |
| Terminal invariant-jet route | HOLD | A local seed does not survive automatically; no invariant cone is proved. |
| Aggregate recovery moments | GO | The rare-cell normalization obstruction has been removed. |
| Global face-time theorem | CONDITIONAL GO | Same-occurrence bidirectional order reduction and exact `q` matching remain open. |
| Fixed-section unconditional CM2 | NO-GO FOR CLAIM | PPE, global DQ/matching, and global face-time are not closed. |
| Standard full-boundary CM2/susceptibility | NO-GO FOR CLAIM | In addition, the section-to-full transfer remains unproved. |

## Next two falsifiable certificates

### Certificate A: complete one-return radical event inventory

For every primary/secondary event and finite torus lift:

1. enumerate the fixed common source charts and physical words;
2. square-free factor every event equation;
3. certify submersion on every admissible zero set;
4. classify each common factor as artificial/duplicate with exact trace
   cancellation, or supply a joint radical normal form;
5. enumerate triple and higher incidences;
6. certify corner, grazing, target-transversality, and parameter-continuation
   margins by exact or interval arithmetic.

Stop if a genuine coincident unequal-trace factor or an untreated critical
germ appears.  Do not discard it as a measure-zero set.

### Certificate B: physical common-vertex projective connector

Within one clean fixed-section magnet rectangle, certify two complete return
words, their transported loop derivatives, and:

1. the exact collision/transparent-wall/lift itineraries;
2. uniform non-grazing and non-target-obstacle clearance;
3. full crossing of the same rectangle and parameter continuation;
4. pinching and all Perron-line twisting wedges with strict margins;
5. positive conditional branch-weight lower bounds;
6. pointwise identification of projective slope with the physical endpoint
   derivative ratio.

Only after these six items may the common-vertex result feed an actual
stopped-parent Frostman/PPE theorem.

## Reproducibility commands

```bash
python3 deliverables/cm2_fixed_section_geometry_cert.py
python3 deliverables/cm2_fixed_section_impact_cert.py
python3 deliverables/cm2_fixed_section_qnl_cert.py
python3 deliverables/cm2_fixed_section_projective_cert.py
python3 -m venv /tmp/cm2-flint-venv
/tmp/cm2-flint-venv/bin/python -m pip install 'python-flint==0.9.0'
/tmp/cm2-flint-venv/bin/python \
  deliverables/cm2_fixed_section_common_vertex_cert.py
latexmk -pdf -interaction=nonstopmode -halt-on-error \
  -outdir=/tmp/cm2-v52-build deliverables/cm2-bridge-note-v52.tex
```

Acceptance criterion for this milestone: all five scripts exit zero, LaTeX
has no unresolved or multiply-defined references, and v51 retains its frozen
SHA256.
