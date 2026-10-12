# Build and verification guide

Required: Python 3, NumPy, pypdf, pdflatex with standard AMS/lmodern/microtype/geometry/hyperref packages, pdfinfo and pdftotext. The hosted workflow pins pypdf and NumPy and records the actual TeX engine.

Run `python verify.py`, `python regression.py`, and `python -O regression.py` from this directory. Regression stdout must be byte-identical. These are source and finite checks, not proof certificates.

`python native_build.py --output /tmp/r38-native --receipt /tmp/r38-native.json` performs two isolated copies, three TeX passes each, active-input recorder checks, label/citation/box audit, and within-environment byte comparison. Without `--source-sha` the receipt correctly says local uncommitted preflight.

`python build.py --source-sha <ordinary-source-SHA> --expected-tree <ordinary-projection-tree> --output <output> --receipt <receipt>` rebuilds the native article and the full unchanged retained R37 chain. Companion J is the complete R37 native article; I/H and older companions are retained, not replaced by excerpts. Each nested build verifies its pinned source projection. Artifacts/evidence/review inputs are excluded from the ordinary mathematical projection by an explicit rule; the actual Git directory tree is separately recorded.

Independent reconstruction must start from a downloaded remote ordinary-source or artifact packet. Snapshot all input bytes before and after. Record actual environments, PDF hashes, page counts, normalized text and rendering comparison; do not promise cross-TeX byte equality. Final verification adds only evidence files. The full repo contains papers outside this build scope; their existence is not a claim that this command rebuilds them all.
