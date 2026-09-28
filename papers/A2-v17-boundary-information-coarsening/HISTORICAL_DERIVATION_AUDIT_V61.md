# A2 v61 — historical derivation and revision audit

The report is pinned at `396bb28e17ba9944af5ff89a2db601412eeb95ee`, and the reviewed mathematical source at `1a55bfb1102c3eab9cdcd6a292c5ef9070ea14a5`. The native v60 artifact was obtained from run `35039952221`, attempt 1, artifact `10424981887`. Its outer SHA-256 is `cc1d87a5454d2dd2637a8f3f741ee00cdb7e379f1b2138a02fb20649ecdcafc8`. Before editing, all 739 frozen source files were checked for length, SHA-256 and Git blob identity against the native manifest.

## Read and used in this revision

| Historical source | Mathematical role examined | Treatment |
|---|---|---|
| `v4/10_boundary_layers.tex` | Weighted half-lines; physical action; exact finite cofactor normalization; two-ended trace-class comparison; common-domain integration; fixed-offset law. | Entire file retained unchanged. The new introduction exposes this as the forward mechanism. |
| `article/23a_signed_endpoint_rigidity_v27.tex` | Interpolation of actual smooth graphs; finite envelope; decaying terminal remainder; finite-jet factorization; signed last-jet blocks. | Retained unchanged. Exposition puts factorization before coefficient algebra. |
| `article/23a2_analytic_contact_inverse_v59.tex` | Protected argument domain, holomorphic half-lines, complete envelope, low quotient/high tail inverse and variable-leading-coordinate extension. | Retained unchanged. Complete lower couplings are not replaced by diagonal estimates. |
| `article/23a3_conditional_observation_inverse_v60.tex` | Contracted-evaluation criterion; Chebyshev restriction estimate; compatible two-radius inverse; real law extraction; weak norms and mesh bias. | Retained unchanged. No new general continuation claim. |
| `article/23f_single_offset_law_inverse_v42.tex` | Four-density identity, scalar anchor, signed action recovery, fixed-order stability and finite-flight inverse. | The relevant inverse and finite-flight proof were checked; entire file retained unchanged. |
| `v4/20_nonlinear_information.tex` | Action and determinant contributions to the quartic response; area-preserving support family; fixed leading data with nonzero nonlinear response. | Retained unchanged. The actual values and the scope of the comparison are brought into the introduction. |
| `journal/00_principal_introduction_v56.tex`, `journal/01_structural_statements_v56.tex` | Local headline, observation design, global finite alternatives, asymmetry, differential and immersed-model conclusions. | Original introduction retained; all its mathematical statement/proof environments remain verbatim in the new introduction. Structural theorem file unchanged. |
| `journal/DEPENDENCY_LEDGER_V60.md` and the v60 historical audit | Existing acquisition theorem input, comparison references and scope of prior work. | Read as dependency declarations, not substitutes for the proofs. Their roles are retained. |
| `main.tex`, `rigidity.tex` and the reference routes | Principal/full separation and cross-document compilation. | Version metadata and abstracts adjusted; principal selects the new introduction. Exact original entries archived. |

The local and global routes remain

`physical full-phase bridge -> relative normalized law -> signed actions -> actual smooth contact jets -> analytic contact germs -> complete analytic obstacle images -> finite incidence registration -> marked lattice`.

The analytic-norm route and its conditional real-data consequence remain part of this chain. The complete acquisition theorem is downstream and has additional hypotheses. The new exposition is not a proof of unmarked channel discovery or equality with a marked length spectrum.

## What changed, and what did not

The new introduction is an expository reorganization with additional explanation of already proved formulas and comparisons. It introduces no mathematical statement environment beyond those inherited verbatim. The principal abstract is rewritten around the relative/action mechanism. The full abstract adds an organizing sentence; its full list of conclusions is retained. The original introduction remains available in place; exact original entry files are archived under `history/v60-review-baseline/`.

All theorem/proof modules, including the v59 and v60 additions, remain unchanged. No A1 file, prior referee report or default-branch ref is modified. The new source and native-product branches are separate. Repository index/readme changes and their archived originals are delivery navigation, not mathematical scope changes.

The preservation checker compares the inherited Git subtree against the pinned mathematical source. It permits only the two entry files and the paper readme to differ, requires every inherited path to remain, requires the old principal introduction to remain byte-identical, and requires all its mathematical environments to occur in the new introduction. It also compares the active TeX graph with the original graph after the one explicit introduction replacement. These mechanical statements do not establish semantic independence or mathematical correctness.

## Coverage limits

This round concentrated on the relative/action proof chain, the new v60 inverse and the realized comparison needed to answer R60-E1. It is not a fresh line-by-line certification of every historical finite-action/full-phase prerequisite, every global matching proof, the complete acquisition/calibration catalogue, all statistical experiments or the companion theorem. The complete corpus is retained and rebuilt. The primary-source check is a scope and attribution check, not an exhaustive originality search. No placement conclusion is deduced from these preservation or build checks.
