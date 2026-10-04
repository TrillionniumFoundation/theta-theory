# A2-DYN v1 — physical collision records and raw local inversion

**Qian Qi, Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas**

This research manuscript executes the A2-DYN workstream after the final A2-GEOM
v43 review. It is not another revision of the geometric inverse. The raw
mixed lattice--roof density local limit remains the long-time target. The
present mechanical, periodic, and edge results are proved directly; the
long-time theorem has explicitly printed analytical hypotheses whose full
billiard realization is not claimed complete.

## Source freeze

A2-GEOM author: `4557df22f5c72bc80943690ecd6c2e39de3734ab`.
Controlling final review/base: `af2390e3073acf8ccd90b10d7566e30cbf18c425`.
Research branch: `research/a2-dyn-v1-raw-local-limits-2026-10-04`.
Paper directory: `papers/A2-DYN-v1-raw-local-limits`.
All older papers and reports remain unchanged. The workflow checks the entire
path diff from the frozen base, not merely a claim of preservation.

## Results to read

`main.tex` contains the complete native article. It gives an exact marked
suspension formula including initial and terminal residual flights; an explicit
physical inducing section; true winding four-cycles certified by rational
interval arithmetic over the whole radius interval; and a unimodular augmented
periodic-record matrix at zero roof frequency.

The normal alternating word has right density jump
`J_N(R) = 1 / (2 R sinh(N acosh(1+(1-2R)/R))))`.
More generally, a regular critical word is normal at its endpoints, has at
most one critical point for its center sequence, and has a jump bounded by
`C_* (47/53)^(N-2)`. This is a uniform individual-word bound, not a sum over
all branches. For the explicitly specified inducing section, one component
has a nonzero jump for every return count; its raw joint characteristic
function is therefore not globally L1. An exact subtraction isolates the
edge without smoothing or discarding any physical record.

The actual finite induced records have mixed coarea densities, also with bounded
insertions. This is an absolute-continuity result, not a uniform asymptotic bound.

The residual-inversion theorem proves the raw central density LLT under its
printed small-frequency, summable-edge, and integrable-residual hypotheses.
Central density conditioning, physical-clock transfer, covariance continuity,
and geometry-to-Gaussian prediction have their own explicit inputs. An
unconditional application transfers radius error to equilibrium collision-rate
error with constant 110 and needs no reconstruction of the unknown launch law.

`P0_P5_STATUS.md` and `STATUS.json` distinguish these proved statements from
unrealized analytic inputs. `PROOF_LEDGER.md`, `SOURCE_AUDIT.md`, and
`LITERATURE_AUDIT.md` explain dependencies, repairs, and prior work.
`SPECIALIST_REVIEW_BRIEF.md` is a handoff, not an invented independent review.

## Reproduction

A standalone source copy can be built with `sh build.sh`. In the repository,
run `python3 tools/qualify.py --expected-head "$(git rev-parse HEAD)"` from this
directory. The latter verifies committed source bytes and preservation, checks
the declared status, runs the rational winding certificate and independent
finite diagnostics in normal and optimized Python, builds the PDF without
shell escape, and binds source archives and evidence to the exact head.

The finite suite has 686 checks, separated into exact algebra and floating
mechanical/model diagnostics. The winding certificate uses 32 rational
parameter intervals, integer square-root enclosures, and explicit Taylor
remainders. Neither suite is a continuum proof assistant or a human review.
No full-billiard LLT certificate, A3 dependency release, journal acceptance,
or independent human confirmation is asserted by a successful build.
