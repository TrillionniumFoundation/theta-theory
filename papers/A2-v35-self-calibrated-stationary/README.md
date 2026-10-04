# A2 v35 — self-calibrated stationary collision experiments

**Qian Qi · 4 October 2026**

Primary article: *Scalar collision laws and recognition of periodic dispersing billiards*, `main.tex`. This revision responds to the **v34** referee report at `e8ad32bfd0a8641c239c67e9776ba08d3aaab72a`, reviewing author commit `ed3876b8a82e2c46bc1533457978c15fea1a2114`. It does not use the different v34 package previously prepared in a conversation as its baseline.

## Mathematical revision

The new Section 10 proves joint recovery of the unknown convex launch footprint and the periodic table from two fixed, known homothetic scales. A positive inball gives a cross-scale nesting margin, so component correspondence is recovered without labels, distinct shapes or asymmetry. Two support equations then separate the original body and the unknown footprint. The finite theorem retains the one-scale stationary upper exponent while eliminating every footprint-support and density-evaluation oracle. Exact homothety, the scale factors and dilation origin, uniform geometric bounds, boundary-mass constants and fine nominal positioning remain explicit controls or priors. The noise density itself is not reconstructed.

The new Section 11 proves a noise-specific expected-stopping lower power `nu^(-(s+1)/(s-2))`, `s=6+beta`, under one fixed known uniform-disk law used for every competing table. Uniform short-command mean contraction on a physical packing is combined with a binary-channel range inequality valid after every adaptive history. The lower bound also permits direction-specific commands and any scale in a fixed interval bounded away from zero. It is not the earlier table-dependent adversarial calibration coupling. A gap remains to the stationary upper exponent; neither exponent matching nor sharp confidence dependence is claimed.

The two explicit proof clarifications requested by the report are in Section 9: erosions are bounded below the uniform rolling radii at their point of use; the high-order approximation kernel is explicitly signed, with four displayed rational coefficients.

## Preservation and reading route

Read the additional main theorem in Section 1, then Sections 10 and 11. The article is self-contained. All **28** reviewed theorem/lemma/proposition/corollary blocks remain verbatim, **24 of 26** reviewed proofs remain verbatim, and the other two receive only the stated clarifications. There are **33** proof blocks in the current article. Ten of the twelve inherited core files are byte-identical. All 86 reviewed labels remain reachable. The title and active collision-law topic are unchanged.

The existing `papers/A2-v34-calibration-experiments/` directory and its `archive/v33/` remain untouched at their existing repository paths. They are preservation/history, not newly required journal supplements. The proposed patch adds only the new paper directory and its read-only verification workflow.

## Reproduction

The current finite diagnostics use Python's standard library; rebuilding the article requires `latexmk`, `pdflatex` with the packages used in `main.tex`, and Poppler `pdfinfo`. Rerunning the pinned v34 diagnostics also needs `mpmath`.

```sh
python3 tools/validate_v35.py
python3 tools/validate_v35.py --baseline ../A2-v34-calibration-experiments --run-retained
python3 tools/validate_v35.py --require-checkout --expected-commit "$(git rev-parse HEAD)" \
  --baseline ../A2-v34-calibration-experiments --run-retained
```

The actual local run built a **36-page** primary with no final TeX warnings, undefined references or overfull/underfull diagnostics. It passed **4,254** current finite diagnostics and **19** current validation-contract checks, and independently reran **5,886** v34 diagnostics and **21** v34 contract checks in ordinary and optimized Python with pairwise identical output. These are finite reproducibility evidence, not formal proof certification or physical-sensor execution.
