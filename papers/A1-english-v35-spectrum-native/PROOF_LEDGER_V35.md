# A1 v35 — mathematical dependency and preservation ledger

The controlling submission is the v34 report at `a177077ede2b64e11af1efb016eaa6bb5ddf2a13`, on manuscript `03a4788efb3cf643bc2cd60257c5ed290bb0570d`. This revision preserves its principal theorem and general finite-cell realization theory. All paths below are relative to the new native directory.

## Principal theorem: unchanged complete proof chain

`core/02_experiments.tex`, `text/operational_model.tex` and `risk_criteria.tex` specify executable tests, prescribed acquisition, future-only queries, charged per-report labels and the distinct risk criteria. `text/exact_information.tex` and `core/03_transversality.tex` identify operational moments, construct the acquired binomial tangent and prove the exact one-rank normalization loss. `text/analytic_inputs.tex` supplies positive pairings and bounded-format real covering inputs. `text/collision_flags.tex` proves complete confluent-flag attainment and actual acquisition-law minorization. `text/collision_direct.tex` proves whole-image anisotropic covering, checkpoint lower bounds and one reachable raw-moment causal realization. `text/main_classification.tex` states the unchanged joint calibration-and-budget theorem. `text/collision_consequences.tex` proves persistent bits, the finite-power collision tree and the two-parameter arrangement.

The historical proof route remains present rather than being replaced by a spectral analogy. The Fourier matrix in the new section is auxiliary; it changes neither the physical reports nor the charged memory resource. Fixed prior, detector, horizon and compact chamber remain in the constants. A full-support prior may be singular. No growing-horizon or calibration-blind conclusion is inferred.

## New comparison arguments

**Proposition 13.1**, `prop:v35-exterior-spectrum`: for fixed `q` and `L >= q−1`, alternating minors factor by a Vandermonde polynomial. Their quotient polynomials are bounded on the compact unit torus. Exterior operator norm bounds and one consecutive-row minor compare every leading singular-value product with the maximal real-node determinant volume. Exact repeated labels are included. The constants depend on fixed size and bandwidth, so this does not replace the stronger varying-bandwidth estimates in the cited literature.

**Corollary 13.2**, `cor:v35-spectral-envelope`: apply Proposition 13.1 to the formal future nodes and retain the acquired cutoff of the principal theorem. Maximize over the finite index and checkpoint sets. The causal conclusion is inherited from the complete acquired-geometry proof, not established by the matrix comparison alone.

**Corollary 13.3**, `cor:v35-fixed-future`: use the six separated groups and three within-group gaps in the existing two-parameter proof. Their maximal-volume profile gives six order-one singular scales, two scales of order rho and one of order tau. Apply the existing checkpoint theorem at acquisition lengths one, two and three, keeping future length two. The total horizons differ explicitly. Zero spectral scales are handled by rank rather than division by zero.

**Remark 13.4**, `rem:v35-flat-path`: substitute the displayed smooth flat path directly in the retained determinant law and balance adjacent terms. This distinguishes the full determinant theorem from the additional finite-power hypothesis of the collision-tree computation.

The comparison reads BDGGY2021, Theorems 2.2–2.3, against these fixed-size exterior products, and BDGY2020, Definition 3.13 and Theorem 3.14, against the experiment's distinct loss and memory resource. The primary-source locators and DOI metadata are in the bibliography. No exhaustive originality theorem is claimed.

## Finite-cell and companion preservation

`v35/moment_controllers.tex` keeps every v34 statement and all finite-cell hypotheses, including zero evidence, zero occupancy, atomic command ties, deterministic realization under atomless commands and scalarized polyhedral optimality. Only the proofs of one-step implementability and the overlap corollary remove duplicated calculations by explicit reference to the complete preceding Blackwell proof. `v33/finite_compatibility.tex`, `v33/precision.tex` and `v33/exact_instance.tex` remain active and unchanged.

`companions.tex` and all its mathematical sources remain byte-identical. Their structural, exact-kernel, uncertainty, effective, graph, occupation, regenerative and delayed-use results retain their individual assumptions. None is silently imported as a premise with stronger simultaneous quantifiers in the main experiment.

The preservation scan finds 218 unchanged inherited theorem-like statement blocks and 207 inherited proof blocks, with precisely the two editorial integrations described above. It compares the complete declared native source closures, not only modified modules. The Git publication is based on the entire v34 native subtree, preserving inactive sources and historical records as well. Old entrypoint, README and build-wrapper objects are retained under `history/`.

## Reproduction and limits

`v35/build_native.py` compiles the complete native pair with actual reference exports and verifies the active input closure using the TeX recorder. `verification-v35/NATIVE_BUILD_V34_CURRENT.json` and `NATIVE_BUILD_V35.json` distinguish current v34 and v35 executions. Current v35 has 42 main and 159 companion pages. `PRESERVATION.json`, `VALIDATION_SUMMARY.json` and `VISUAL_INSPECTION.json` state what was compared, executed and visually inspected.

The new comparison diagnostics and the two unchanged inherited exact checkers execute under ordinary and optimized Python with identical outputs. Such executions do not establish continuum compactness, uniform acquired mass, semialgebraic entropy bounds or every possible global optimum. Those conclusions rest on the printed analytical arguments, not on check counts.
