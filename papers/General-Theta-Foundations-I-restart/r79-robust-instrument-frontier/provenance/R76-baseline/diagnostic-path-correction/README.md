# R76 formal-source diagnostic path correction

The first pushed source commit `4f61c7a5173416c3532e1b6b967bed8e2a559f08` was actually subjected to strict verification. The run stopped when the new structure diagnostic tried to hash its mathematical source at a development-relative path. Its preceding finite checks had run, but no completed report or strict PASS existed.

Only the default path in `diagnostics_r76_structure.py` is corrected to `sections/46-mean-contrast.tex`. No mathematical statement, proof, finite-check logic or inherited diagnostic is changed. `CORRECTION.json` binds the old/new script hashes, while `BUILD_FAILURE.json` and the stderr file preserve the actual failure. The initial commit remains in the new branch ancestry; its full partial run is kept in the publication validation archive. The following source commit must be independently sealed and pass the entire strict verification at its own real Git HEAD. The source cannot declare that future result in advance.
