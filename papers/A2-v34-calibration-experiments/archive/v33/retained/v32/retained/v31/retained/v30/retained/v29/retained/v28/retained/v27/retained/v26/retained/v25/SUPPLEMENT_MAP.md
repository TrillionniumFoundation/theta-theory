# Submission volumes

`main.tex` is the active v25 primary article. Its proofs are self-contained at the displayed scope.

`retained/v24/main.tex` is the exact reviewed v24 article, Supplement P. Its whole tree includes its original verification history and its retained v23 Supplement Q. The latter contains the v22, v21 and v18 retained manuscripts and their earlier mathematical chain. These are included sources, not citations to independently accepted publications.

`complete/main.tex` and `complete/two_collision.tex` are the unchanged original smooth-theory supplement and auxiliary document. The same native tree is also preserved inside the inherited chain.

For current full-package qualification run `python3 tools/validate_v25.py --all-volumes --require-checkout` from an actual checkout. The v25 primary is built first. The preserved v24 driver then builds its primary and all six of its declared companions under the current commit. Its raw historical diagnostics and reversible staged-only layout insertions remain explicitly recorded. Historical wrappers do not touch tracked mathematics and are not silently described as warning-free raw builds.
