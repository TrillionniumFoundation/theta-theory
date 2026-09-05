# Theta theory — active Round 53 revision

**Boundary Identification from Recurring Fast Probes: Energy-Robust Posteriors and Bound Observable Certificates**

Author: Qian Qi. Revision date: 5 September 2026.

Start with [the review index](ROUND53_REVIEW_INDEX.md), [the article source](ROUND53_REVISION.tex), and [the response to Round 52](AUTHOR_RESPONSE_ROUND52.md).

The new revision retains logarithmic labeled physical depth, strengthens the complete posterior to a controlled cumulative-energy discrepancy class, allows atomless exploration when short probes recur outside exploration, uses the actual clock remainder, and binds executable diameter decisions to the complete observable grid and model identity.

```sh
python tools/verify_round53.py --pdf
```

This checks the immutable source manifest, runs the historical and new regression suites, and performs three TeX passes. The active implementation is `tools/round53_certificates.py`; its certifying entry point is `certify_outer`. Supplied statistical bands still require their own coverage guarantee. Tests and builds do not constitute formal proof certification or journal acceptance.

All historical manuscript roots, derivations, referee reports and programs are preserved on this full-history revision branch. The new root explicitly inputs the unchanged moment/inverse and likelihood sources in `round51/`; they are part of its manifest, not optional external files.
