# General Theta Foundations I — Revision 51

**Compatible Lifts, Finite-Group Rigidity, and Stable Stochastic Width**  
Qian Qi · 27 September 2026

[Article](paper.pdf) · [Native source](main.tex) · [Response to r32](RESPONSE_TO_REFEREE.md) · [Build receipt](evidence/BUILD_RECEIPT.json) · [Referee package](evidence/REFEREE_PACKAGE.zip)

The new proofs give reachable sections at arbitrary width, a local cubic real-algebraic characterization of prescribed profiles, an all-width finite-group criterion for bounded exact clocked width, an eventual exact six-state frontier in dimension three, and an explicit positive-error four-state frontier in dimension two. The precise seed, command and error hypotheses are stated in each theorem. The variational six-state gap is not assigned an unproved numerical value. The real-algebraic criterion is not an implemented general optimizer.

For planar signed-permutation alphabets containing I and −I, signal 1/10, horizon at least 16 and binary-TV error at most 1/200000, the optimal width is exactly four. The zero-error horizon-14 sufficient bound remains in the article. Neither first horizon is claimed sharp.

Build with Python 3.11, SymPy 1.14.0, PyMuPDF 1.26.7 and TeX Live with AMS, Latin Modern, microtype, mathtools, geometry, booktabs and hyperref:

```sh
python check_revision.py
python -O check_revision.py
python build.py --check-core
```

Extract `evidence/CORE_SOURCES.zip` and run `python GTF-I-v51-compatible-lifts/build.py --core-only` for an isolated build. No earlier revision is needed for that command. `prepare.py` is the repository-only assembly step and is not required in the isolated core.

The old paper and all historical branches remain unchanged. Every original active mathematical module is retained; copied-file editorial edits and hashes are listed in the preservation manifest. The actual input graph is checked, not an unloaded archive. All sources are readable native text, not an opaque payload. The final receipt records executed checks, not an advance assertion of success.
