# General Theta Foundations I — revision 24

**Statistical Resource Duality and Two-Preparation Physical Certification**  
Qian Qi · 24 September 2026

This package responds to the seventh external report on v23, frozen at
`e34f5eb4fe1b1f03018c6baec2e594ab22766dfb`. The branch descends from that
report and preserves the predecessor manuscript, review and repository paths.

## Reading order

The canonical journal article is [paper.pdf](paper.pdf), from
[main.tex](main.tex). It contains the complete new proof chain, not merely
an outline. The paired [complete mathematical manuscript](complete-manuscript.pdf)
contains that article and the entire unchanged 96-page v23 article.
The [complete development](complete-development.pdf) contains the new
article and the entire unchanged 649-page v23 development. Each combined
volume includes one clearly marked divider page. No predecessor proof is
removed from the repository or the full volumes.

Read [the point-by-point response](RESPONSE_TO_REFEREE.md) for the mapping
of requests 24.1–24.10, and [the resource ledger](RESOURCE_LEDGER.md) for
all preparation, register, mark and clock costs. The generated
[theorem locations](evidence/THEOREM_LOCATIONS.json) give exact numbers
and pages. [Proof status](PROOF_STATUS.json), [pipeline status](PIPELINE_STATUS.json),
[historical audit](HISTORY_AUDIT.md), and [literature crosswalk](LITERATURE_CROSSWALK.md)
separate established claims from the remaining comparisons and targets.

## Principal theorem

For the original reset row-event physical task, let
`u1=4035777/10240000`, `m2=(12-3*sqrt(3))/16`, and `TV(Q,Q*)<=beta`.
Then `N_c^phys(W,Q)=2` for every `W>=12` and
`u1+beta<=c<m2-beta`. In particular this applies to the positive-noise
collision family at `beta=1/300`, `c=2/5`.

The converse permits unlimited memory and all declared adaptive feedback
schedules with at most one candidate training preparation. The matching
audit has two training preparations and two fresh validations, hence
four preparations in total. Its deterministic full profile is
`(1,2,3,3,4,5,5,10,12,10,10,7,3)`. Its decision alphabet has five labels,
not three. Its peak is twelve; peak optimality is not claimed. A fully
phase-tagged autonomous implementation has at most 75 states.

The new statistical dual is uniform over architectures under the
dominating-row assumption. The separate finite-architecture subdivision
certificate has an explicit `HS/m` interval gap and row-block degrees
`d_r`; it is not a uniform global SOS-degree theorem. The autonomous
stationary binary optimum is attributed to Hellman–Cover, with explicit
finite-time and dyadic implementation costs added to the ledger.

## Reproduction

Use Python 3.11 or newer, `sympy==1.14.0`, `PyMuPDF==1.26.7`, and a TeX
installation providing `pdflatex`, AMS, Latin Modern, microtype and geometry.
From the repository root run:

```sh
python -m pip install sympy==1.14.0 PyMuPDF==1.26.7
python papers/GTF-I-v24-structural-resources/verify.py
python -O papers/GTF-I-v24-structural-resources/verify.py
python papers/GTF-I-v24-structural-resources/build.py
```

The predecessor directory `papers/GTF-I-v23-compatible-frontiers` must
be present. An alternate location can be supplied with `GTF_V23_DIR`.
The [portable source archive](evidence/SUBMISSION_SOURCES.zip) includes
the new source, all predecessor source files needed here and the two
frozen predecessor PDFs. Extract its two sibling directories and invoke
the new build script. The bibliography correction to R. A. Flower and
the paragraph-layout preflight are idempotent and recorded explicitly.

The build checks the exact prior table, polynomial identity and
4096-word residual machine; reruns the inherited v20–v23 diagnostics;
requires normal/optimized agreement; detects deliberately incorrect
controls in both modes; compiles three times; and checks every appended
predecessor page for identical text and raster samples. Read the actual
[build receipt](evidence/BUILD_RECEIPT.json), rather than inferring
execution success from the existence of this README.

## Scope of the completed revision

The preparation boundary for `W>=12` is proved. The complete boundary
for peak widths 3 through 11, the least peak at two preparations and the
best score among all two-preparation selectors are not determined. The
old minimum decision alphabet of three remains a different resource
statement, achieved with longer training. Independent A2 results and
historical B4/C2 aggregate targets are preserved without a claim of
closure. The original Norberg proof-level comparison remains incomplete.
Finite checks, PDF preservation and compilation do not certify novelty,
independent mathematical correctness or journal acceptance.
