# A2 v11 revision entry point

**Manuscript:** Qian Qi, *Nonlinear boundary laws and stable energy invariants in dispersing billiards*, 10 September 2026.

**Revision directory:** `papers/A2-v11-abel-stable-boundary-profiles`.

The complete native English source is `main.tex` in that directory. The unchanged original companion is `two_collision.tex`. `RESPONSE_TO_REFEREES.md` answers the completed-v10 report at review commit `2b893b931a894dfc9e7730b853f575124ffb5c55`. `PROOF_LEDGER.md` and `HISTORICAL_DERIVATION_AUDIT.md` identify the new proof chain and historical inputs. `VERIFICATION.json` records actual local builds, selected rendered-page inspection, finite diagnostics and their limits.

The revision adds a nonlinear weighted Abel-flux stability theorem, a fully charged integrated-flux acquisition theorem, and a smooth-physical-class calibration procedure estimating the unknown gap, area and multiplier. The physical nonlinear invariant is the central target. Labels, common smoothness/convergence bounds and coarse parameter boxes remain supplied. The new preparation bounds are sufficient and certificate-dependent, not full-profile minimax assertions.

All 176 reviewed active formal environments are retained byte-identically; the new manuscript contains 192. The complete local builds have 107 main pages and 7 companion pages. Successful tests are not formal proof certification, a remote CI result, an exhaustive novelty clearance, or a journal decision.

From the manuscript directory:

```sh
python tools/build.py
python tools/run_all_checks.py
```

See its README for requirements and authenticated historical diagnostic inputs. The native Git tree does not duplicate the compiled PDFs; those and full build/test logs are supplied in the revision packet. This branch adds a separate revision directory and this entry point on top of the review commit. Every pre-existing repository path, manuscript, derivation and review is preserved. It is ready for the next independent referee examination, not merged into the default branch.
