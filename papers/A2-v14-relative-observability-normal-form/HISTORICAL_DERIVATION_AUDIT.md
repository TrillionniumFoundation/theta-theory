# A2 v14 historical derivation audit

## Frozen chain

The controlling author source is `0e54099f079232df233316ae6fe7986fc51b7ea1`,
`papers/A2-v13-two-flight-relative-invariants`, native tree
`ee946ef91770778839f15c8c35416d401e99ea1c`. The latest review is
`a02d58d2b77e3337f001cf13676c5ff70e1ba97c` (28 September 2026). The earlier v13
review and analytic comparator are at `b3f0ad5843782c221651c9189fc156d20865cab1`
(10 September 2026). The canonical September 28 source alias resolves to the
same September 10 author commit, so it was not treated as a mathematical revision.

## Derivations consulted for the new arguments

The v13 two-flight section supplies the full action, twist, ellipse-moment and
triangular-block calculation and the supplied-family finite-window proof. The
physical-image section supplies the support-function construction, its area
compensator and the triangular support-to-contact Jacobian. The v4 boundary-layer
section supplies the half-line Green operator, trace-class determinant amplitude,
normalization, and smooth geometric relative theorem. The v13 introduction and
operator comparison distinguish the smooth physical theorem and its integral
from finite-flight and global spectral inverses. The existing source-history
ledger records the retained v3–v12 derivation chain; that ledger is preserved in
the exact native snapshot rather than being silently recast as a new audit.

The September 10 companion normal-form memorandum supplies the restricted
analytic comparator, including the physical projection identity and the
identification by uniqueness. The September 28 report supplies the explicit
quantifier and normalization objections. The local normal-form input was checked
against the primary arXiv text of De Simoi–Kaloshin–Leguil, v4, printed pp. 10 and
13. The new text credits the referee calculation separately from that publication.

## Preservation rule

The v14 native tree starts from the exact v13 tree. Its complete source snapshot
is also retained at `history/v13-reviewed`. Existing mathematical input files are
reused as Git objects; new arguments are additional active inputs. The main
abstract, date, roadmap and acknowledgments are updated. Root response, status,
source-pin and verification documents describe v14 rather than reproducing v13
success claims. Their originals are in the snapshot. The build and checker are
read-only with respect to tracked source.

`tools/verify_v14.py` compares all old active result and proof environments and
checks that the old input set remains reachable. In a Git checkout it verifies
the snapshot's exact tree identity before relying on that baseline. An isolated
new-section compile or finite algebra run is not reported as a full revalidation
of every inherited appendix. No previous paper, author branch or review file is
rewritten by this revision.
