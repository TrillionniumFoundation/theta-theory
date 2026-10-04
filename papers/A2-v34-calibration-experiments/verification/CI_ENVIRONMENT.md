# Hosted environment correction

The first v34 run, `37173615154`, checked out source commit `477cbff26270b6a04af2c09b9a82d5e804345c46`. Its 5,886 new diagnostics and 21 contract tests passed in both ordinary and optimized modes. Qualification stopped when the unchanged v33 suite imported `scipy.integrate` because SciPy was missing from the runner. The receipt correctly reports failure, not a manuscript build or a full pass.

Artifact `11292157892` preserves the failed execution with outer SHA-256 `08277f10bc39cf2567501abab90619f3b3d8b6c01808847eeca329e5ec69deb8`. The downloaded `retained-v33-normal.log` records `ModuleNotFoundError: No module named 'scipy'`.

The follow-up commit adds the omitted Ubuntu NumPy/SciPy packages and documents these retained-suite dependencies. It changes no mathematical source, verification script, source pin, archived manuscript or actual local receipt. The next run must check out and qualify the new commit; neither the first run nor the prior v33 pass is relabelled as its success.

## Complete dependency inventory

Run `37173820908` at `6a13c13aa4b663ad590c63d8e8a328976e1ed2df` again passed the new diagnostics and contract tests, then found the further missing `shapely.geometry` import in the retained physical-geometry check. Artifact `11292392515`, SHA-256 `75e4f319a972eb1bb53fcab4797b8c4ab6c7963f97f7b72b4af47d0d14f68323`, preserves this failure.

An AST import inventory of every participating current/v33/v32 tool and imported local validator identifies four external numerical packages: mpmath, NumPy, SciPy and Shapely. The final environment installs all four and imports them in a preflight step that prints their actual versions. The local qualified versions were respectively 1.3.0, 2.3.5, 1.17.0 and 2.1.2; the hosted run reports its own versions rather than claiming identical numerical libraries. No historical script is changed or skipped.
