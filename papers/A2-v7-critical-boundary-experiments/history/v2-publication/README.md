# A2 v2 — geometric stability and curvature identification

**Geometric stability and curvature identification for uniform collision thresholds**  
Qian Qi — September 9, 2026.

Branch: `revision/a2-geometric-thresholds-curvature-2026-09-09`.  
Controlling review: `14aaea8937f8b2d373bc642f3568d7280dcbbbd7`.  
Reviewed manuscript: `500cf06faccb6eadd6c122abeb63c60a0cb7522e`.

## Read the current submission

`main.tex` is the complete **25-page English article**. `two_collision.tex` is the unchanged **seven-page companion**. Start with Theorems 1.1–1.2 for the geometric result, Theorem 12.1 for curvature identification, and Propositions 13.1–13.2 for the differentiated record and moving-cut results. The complete circular hierarchy and proofs remain in Sections 2–8.

The revision proves the threshold law for compact smooth families in an open C4 neighborhood of circular scatterers, without reflection or rotational symmetry. It includes unequal contact curvatures, non-even boundary jets and competition between shortest channels. An explicit three-parameter isogap family separates threshold locations from contact curvatures, which its amplitudes identify. The retained resource is full physical phase-volume preparation; no artificial local ensemble replaces it.

`RESPONSE_TO_REFEREE_V2.md` answers UCT-R1 through UCT-R4 and the sharper source-domain observation. `PROOF_LEDGER_V2.md` identifies the new proof chain and retained historical inputs. `SUBMISSION_INDEX.md` separates the current geometric theorem, the circular specialization, the companion and the original long-time programme.

All 18 inherited statement blocks and 17 proof blocks remain verbatim. Every original section file remains unchanged, including the historical comparison. The complete former native subtree and review/verification material are preserved in this directory by the Git base. Old entrypoints and index files are additionally available under `history/v1/`. The current comparison and new proofs are in `v2/`; the latest controlling report is copied under `review-basis-uniform-thresholds/`.

## Reproduce

From this directory with Python 3.10 or later, TeX Live, NumPy, SciPy and SymPy:

```sh
python build.py
python v2/verify_geometry.py > /tmp/a2-v2-checks.json
python -O v2/verify_geometry.py > /tmp/a2-v2-checks-O.json
cmp /tmp/a2-v2-checks.json /tmp/a2-v2-checks-O.json
python tools/verify_thresholds.py > /tmp/a2-circle-checks.json
python -O tools/verify_thresholds.py > /tmp/a2-circle-checks-O.json
cmp /tmp/a2-circle-checks.json /tmp/a2-circle-checks-O.json
```

The build compiles both real entrypoints and checks reference convergence, recorder input identity and overfull boxes. `verification-v2/` records the current source hashes, six successful compiler passes, 328 new checks and 411 rerun circular checks. The ordinary and optimized outputs agree byte for byte. These are finite diagnostics, not formal proofs of continuum uniformity.

The current build is content-addressed because it precedes the publication commit. PDF binaries and full compiler logs are supplied in the accompanying native review package; all needed native TeX inputs, builder and compact receipts are in the repository. Old `verification/` files refer only to their historical edition.

No remote CI run, exhaustive priority search, formal proof-assistant certification, noisy inverse stability theorem or unrestricted long-time local-limit theorem is claimed. The new analytical proof is submitted for independent review; a diagnostic count does not decide mathematical significance or journal acceptance.
