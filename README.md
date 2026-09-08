# Theta theory — current review entry

The current submission on this branch is **Round 35**. Start with
[ROUND35_REVIEW_INDEX.md](ROUND35_REVIEW_INDEX.md) and
[AUTHOR_RESPONSE_ROUND34.md](AUTHOR_RESPONSE_ROUND34.md).

The focused manuscript is `ROUND35_REVISION.tex`: *Constructive Adaptive
Identification of Local Damping and Stiffness in an Infinite Mechanical Lattice*.
It contains a specified infinite coupled mechanical model, a four-word
identification construction, posterior and filter-jet proofs, an exact bath
memory kernel, and corrected supporting statements. Its exact rational
embedding certificate is reproducible from the included code.

The original eleven-part Sinai/hard-sphere programme is preserved. This branch
does not declare all of its original applications solved. The proof ledger
separates the new mechanical model from those remaining targets.

```bash
python3 -m pip install -r round35/requirements.txt
python3 tools/verify_round35.py
```

The verifier also needs `pdflatex` and `pdfinfo`. It writes only under `build/`;
it never patches manuscript sources or publishes commits. Historical Round 33
sources and records remain historical rather than being relabelled as Round 35
verification.
