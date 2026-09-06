# Independent A1 v11 referee review

**Reviewed submission:** `f2f7bd3cf2544c3c57f09d015cb10bf0efe6c1c0`  
**Revision branch:** `revision/a1-english-v11-referee-response-2026-09-06`  
**Review branch:** `review/a1-english-v11-harsh-referee-2026-09-06`  
**Recommendation:** Reject at the requested Annals / Inventiones / JAMS / Acta level in the present form.

This owner-requested AI-assisted assessment is not commissioned by those journals. It distinguishes the principal theorem's examined validity, the new implementation evidence, and the editorial significance judgment.

The [referee report](REFEREE_REPORT.md) closes the old zero-decoder objection and records a different, executed transition-sensitivity failure: both the original suite and a version with every transition sent to index zero pass 8,207 checks, although 775 transition entries change. This is not a counterexample to the original compiler or its continuum theorem. The [technical note](TECHNICAL_NOTE.md) proves an exact interval witness explaining how collapsed transitions destroy covering order, and distinguishes exact rational bit lengths from sufficient rounded precision.

The [mathematical audit](MATHEMATICAL_AUDIT.md) gives the principal proof checks. The [source index](SOURCE_INDEX.md) pins read ranges, references, version-specific citation concerns, source hashes and work not performed. The [execution record](EXECUTION.json) contains independently generated results, not copied author validation claims.

Reproduce from the repository root:

```sh
python3 reviews/a1-english-v11-certified-memory-2026-09-06/reproduce_review.py \
  --source papers/A1-english-v11 \
  --out a1-v11-referee-reproduction
```

The [script](reproduce_review.py) checks the three author source hashes, reruns the original suite and mutation, and runs the independent rational diagnostics without modifying manuscript sources. Its output directory is separate from the author's validation directory. Numerical reproduction does not certify a continuum proof or a journal decision.

All review additions are confined to this new directory on the new review branch. The original revision, earlier reviews and main branch are left unchanged.
