# Independent A2 v13 review — 10 September 2026

Start with [REFEREE_REPORT.md](REFEREE_REPORT.md). This is an author-requested AI-assisted independent referee-style assessment, not a journal decision or proof certificate.

**Reviewed author commit:** `0e54099f079232df233316ae6fe7986fc51b7ea1`.

**Recommendation under the requested four-journal benchmark:** reject in the present form on significance grounds. No fatal defect was found in the principal proof chain examined. All three concrete v12 revision requests are closed; the remaining negative judgment is evaluative, not a claim that the two-flight proof or the general relative law is missing or false.

The report distinguishes the exact two-flight inverse, the function-valued relative law, and the finite-family versus full-profile experiments. It includes the actual smooth-class pilot audit. [SOURCE_AUDIT.json](SOURCE_AUDIT.json) records pinned blobs, reading coverage, external verification and limitations.

The independent [verify_review.py](verify_review.py) ran **2,757 exact rational checks** successfully in ordinary and optimized Python. The two committed outputs are identical. No author test routine is imported.

```sh
python3 verify_review.py --output checks.normal.json
python3 -O verify_review.py --output checks.optimized.json
cmp checks.normal.json checks.optimized.json
```

These checks are not formal proof certification, a native TeX/PDF build, nonlinear billiard simulation or remote CI. The author's reported build, page and preservation counts were not independently verified here.

This review is added in a new directory on a new review branch based on the pinned author source. It does not edit the manuscript, delete old reviews, merge branches or change permissions.
