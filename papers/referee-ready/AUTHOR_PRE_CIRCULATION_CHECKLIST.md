# Human-author checklist before external circulation

This checklist is mandatory before any manuscript is sent as a claimed theorem
or submitted to a journal.

## Identity and disclosure

- [ ] Confirm every author name, order, affiliation, email, and corresponding
  author designation.
- [ ] Replace placeholder acknowledgements with accurate funding and conflict
  disclosures.
- [ ] Review the AI/computational-assistance disclosure against the current
  policy of the target journal.
- [ ] Confirm that every listed author has read and approved the full paper.

## Mathematical audit

- [ ] Assign at least one internal reader who did not write the proof to each
  manuscript.
- [ ] Check every definition for nonempty examples and every normed space for
  completeness.
- [ ] Verify all parameter-uniform constants and the order in which suprema,
  limits, sums, and derivatives are interchanged.
- [ ] Check every use of compactness for a prior strict local witness.
- [ ] Audit all regularity losses and operator domains in every resolvent word.
- [ ] Confirm that every comparison theorem is stated in the exact growth and
  topology class used by the value functions.
- [ ] Check all stochastic integrability, aggregation, measurable-selection,
  and concatenation hypotheses.
- [ ] Test every actual model against every field of its theorem statement.
- [ ] Confirm that each no-go result excludes precisely the stronger claim
  stated, and no more.

## Cross-paper audit

- [ ] Give each companion theorem a stable public theorem number and preprint
  citation.
- [ ] Verify the direction of every companion import.
- [ ] Confirm the covariance and `1/2` conventions across Papers II--V.
- [ ] Confirm the maximizing/minimizing player convention across Papers IV--V.
- [ ] Confirm that Paper V is never cited upstream as a proof of HJB,
  homogenization, filtering, or game convergence.

## Bibliography and novelty

- [ ] Verify every BibTeX record against the publisher or original paper.
- [ ] Add a precise comparison paragraph for the closest prior results in each
  introduction.
- [ ] Ask a field specialist to check whether any central theorem overlaps an
  unpublished or recently posted result.
- [ ] Remove uncited or nonessential references from the circulated version.

## Typesetting and archival checks

- [ ] Run `python3 tools/verify_referee_manuscripts.py` in a full checkout.
- [ ] Run `make -C papers/referee-ready all` in a clean TeX Live environment.
- [ ] Resolve every warning about undefined citations, references, overfull
  boxes, duplicate labels, and PDF strings.
- [ ] Inspect every displayed formula and page break in the generated PDFs.
- [ ] Archive the exact referee version with a commit SHA and checksums.

## External review packet

- [ ] Include the paper-specific `REFEREE_GUIDE.md`.
- [ ] State which companion papers are assumed and provide them to the referee.
- [ ] Ask the referee to distinguish correctness, novelty, exposition, and
  journal-level significance.
- [ ] Record all referee objections in an issue or revision ledger and answer
  them with exact theorem/line references.
