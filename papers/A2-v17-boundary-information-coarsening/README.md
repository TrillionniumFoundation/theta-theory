# A2 revision 74 — smooth contact rigidity and moment reconstruction

Qian Qi · September 17, 2026

**Boundary laws and smooth contact rigidity of periodic dispersing billiards**

This complete English revision responds to the A2 v73 report committed at `9c69f03f97dea57e83061af96aeb9bfe4dcc80d3` on `review/a2-v73-independent-harsh-top4-2026-09-17`. The historical directory name is not the manuscript version. Begin at the repository-root [A2_REVISION_V74_REVIEW_READY.md](../../A2_REVISION_V74_REVIEW_READY.md), which distinguishes source and native-product references.

The principal journal article is `rigidity.tex`; `main.tex` contains the full technical manuscript; `two_collision.tex` is the unchanged companion. They overlap and are not three independent papers or three disjoint page counts.

## Reading the revision

The shared introduction presents the relative rare-event law, signed global contact inverse and actual smooth flat-tail argument before the one-law and charged-invariant consequences. The new overview is `article/00p_moment_overview_v74.tex`; its complete proofs are in `article/10i_moment_reconstruction_v74.tex`.

The new theorem reconstructs each oblique limiting density from four one-dimensional first-moment profiles and a two-by-two moment matrix. Its determinant floor follows from the opposite marked action slopes. The finite reconstruction retains the exponentially small rank defect and fits the compressed image of actual table–offset pairs. One-dimensional weighted smoothing improves the exponents to `s/[2(m+s)+1]` and `s/(m+s+2)`, while the area estimate retains its flight-length amplification. The accepted data are still paired endpoints; the theorem does not replace them by unpaired marginals.

Charged area recovery uses independent normalized unit-speed Liouville preparations and exact acceptance tags. “No supplied local flux amplitude” does not mean an unknown reset distribution or unknown detection efficiency. This convention now appears in the unified abstract, experiment definition, charged overview and conclusion.

## Referee response and preservation

[RESPONSE_TO_REFEREE_V74.md](RESPONSE_TO_REFEREE_V74.md) maps the concrete handoff and wording corrections, the retained mathematical findings, the new theorem and the significance argument. [COVER_LETTER_V74.md](COVER_LETTER_V74.md) states the mathematical case without claiming editorial acceptance. [HISTORICAL_DERIVATION_AUDIT_V74.md](HISTORICAL_DERIVATION_AUDIT_V74.md) records which inherited mechanisms were used and which claims were not newly independently re-audited in full.

Every one of the 969 inherited manuscript paths remains. The nine modified originals are retained byte-for-byte with modes in `history/v73-review-baseline/`. Replacing four active abstract fragments by a unified abstract does not remove their files or any active mathematical proof input. The normal-incidence two-offset inverse, symmetric and unequal-action routes, actual smooth proofs, analytic and global companions, information catalogue, and prior referee records are retained.

## Native verification

Run `python3 -B tools/verify_preservation_v74.py` against the pinned Git source tree, then `python3 -B tools/build_revision_v74.py --output-dir <outside-source-directory>`. The latter builds all three complete entries from immutable Git objects, checks the recorder inputs and imported external auxiliaries, and runs the inherited and new diagnostics in normal and optimized Python modes. Historical checkers run with their original active source bytes restored in an isolated temporary tree.

The root review-ready entry and versioned delivery manifest identify the actual source commit, native PDFs, source ZIP and performed checks. A successful build and finite symbolic diagnostics are not mathematical proof certificates. Visual inspection coverage is reported separately; no unperformed all-page inspection or blanket independent recertification is claimed.
