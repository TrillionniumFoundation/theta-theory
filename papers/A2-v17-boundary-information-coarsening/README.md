# A2 v17 — boundary information and observation coarsening

**Nonlinear boundary laws and two-contact rigidity in dispersing billiards**  
Qian Qi · English manuscript · September 11, 2026

Revision branch: `revision/a2-v17-boundary-information-coarsening-2026-09-11`.

[Complete article entry point](main.tex) · [Original companion](two_collision.tex) · [Response to the v16 report](RESPONSE_TO_REFEREES.md) · [Proof ledger](PROOF_LEDGER.md) · [Verification status](VERIFICATION.json) · [Source identities](SOURCE_PINS.json).

## Mathematical change

The complete v16 source tree is retained. The active main has 60 direct inputs, including all 56 old inputs. The new main-text theorem identifies the boundary information of linearly vanishing densities and proves the endpoint-only normal critical experiment for the physical finite/boundary comparison. At the same preparation scale, complete records, endpoint records and success bits have three different limiting testing distances. The exact endpoint success scale is `exp(2 j gamma)/(j gamma)`, with every failure charged in its raw version. The general smooth physical transfer and the stronger even-contact transfer are stated separately, with explicit nonempty positive-offset regimes.

The nonshrinking relative law, full boundary profiles, independent-contact inverse, two-flight benchmark, all calibration and minimax appendices, and the original companion remain included. Classical scalar linearization and classical nonregular likelihood phenomena are attributed rather than counted as new mechanisms. An attributed random-hazard clarification is added to the adaptive appendix.

The new core proofs are `article/18_boundary_information.tex` and `article/19_endpoint_critical.tex`. Their introduction is `article/01b_observation_hierarchy.tex`. The optional adaptive clarification is `article/32_random_hazard.tex`.

## Reproduction and build scope

From a complete checkout, run the full native build, not an abbreviated entry point:

```sh
python3 tools/build_submission.py --output-dir /absolute/path/outside/this/directory
python3 tools/check_boundary_information.py
python3 -O tools/check_boundary_information.py
```

The build driver compiles `two_collision.tex` before `main.tex`, follows every active native input, records source hashes, retains logs, and rejects unresolved references/citations, duplicate labels and missing glyphs. The verification record states what was actually executed; a script or a failed Actions job is not presented as a successful complete build.

The 143 new finite checks passed in ordinary and optimized mode with byte-identical output. These checks are not formal proof certification. See `VERIFICATION.json` for the separately recorded full-main build status and evidence.

## Preservation

This revision begins from review commit `c5fed5340df3147f64cb3479cf1837357f73e7a8` and copies the reviewed v16 native tree by Git object identity. The overwritten entry point, bibliography and submission metadata are preserved in `history/v16/`. Prior revision directories and every referee report remain unchanged. Creating this branch does not merge it into `main`.

The manuscript is offered for renewed independent review, not represented as accepted by a journal.
