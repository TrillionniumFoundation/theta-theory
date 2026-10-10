# Exact-SHA qualification protocol — v73

Run `bash papers/A2-DYN-v73-referee-response/build.sh` from a checkout of this revision. No shell escape, remote source generation, skipped inherited proof, or assertion-only test is used.

`verify_v73.py` checks the reviewed v72 tree and report blob, exact provenance snapshots, every inherited core/Python/appendix/bibliography byte, status inheritance and the complete old input order. It deterministically generates the retained body and preceding opening under build/. It runs exact rational fixtures for threshold mixtures, paired flux, the compact primitive, preserved capacity, positive path error comparison and negative controls. Ordinary and optimized Python outputs must be byte-identical. Finite-only local mode is rejected in GitHub Actions.

The six inherited finite scripts run unchanged. Native pdflatex runs until the auxiliary file stabilizes, with a maximum of six passes. Warnings, undefined references, overfull boxes and missing characters fail qualification. The recorder must show all 163 core modules actually loaded. The renderer checks physical-page word bounds and creates preview PNGs for the new argument and the final page. These are rendering checks, not proof certification or an independent visual/human mathematical review.

The read-only Actions workflow binds checkout, PDF hash, source checks and recorder to the exact GITHUB_SHA. Artifacts contain the complete PDF, TeX log/aux/recorder, generated retained TeX, exact source tar, finite-check outputs, page geometry record and previews. A run result is authoritative only for its recorded SHA. Static prose in this folder does not certify a future run, and a successful run does not establish the missing Lorentz paired-flux decay.
