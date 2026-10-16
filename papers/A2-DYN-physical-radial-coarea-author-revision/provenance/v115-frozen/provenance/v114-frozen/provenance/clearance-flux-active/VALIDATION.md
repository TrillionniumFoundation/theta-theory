# Validation record

The baseline active source was independently rebuilt in this runtime using its original build script. That build produced 31 pages with no unresolved references, multiply defined labels or overfull boxes. The source was recovered from completed run 38561460974 at author SHA `45015de51c652bcdaca13123bf65627bf199b2ab`; the downloaded ZIP digest matched the GitHub artifact digest.

The revised build is executed by the supplied `build.sh`. Machine outputs in `evidence/current-validation.json` and the build logs are the authoritative final result, including page count and normal/optimized comparisons. No new GitHub Actions run is presented as executed.

## New mathematical program

`tools/check_clearance.py` checks the signed line-coordinate Jacobians and strip derivative symbolically, the gap and transversality constants by exact rational arithmetic, 1,024 depth-sum cases and 3,081 interpolation cases. It also runs 180,000 deterministic actual physical flight samples (60,000 each at radii .45, .46, .47), and 6,000 inverse line-to-collision reconstructions. The finite lattice scan's completeness for each sampled flight is checked using a geometric distance margin; it is not asserted as a proof of the global finite-horizon constant.

For clearance width .015, observed mean near-miss counts per sampled collision are .0324, .0318 and .0325333333, against exact-flux predictions .0333333333, .0326086957 and .0319148936. Standardized differences are approximately -1.25, -1.09 and .81. These samples are diagnostic consistency checks of the explicit implementation, not evidence replacing the continuous change-of-variables proof. The inverse reconstruction's maximum clearance discrepancy is about 2.97e-16; no new collision at the marked disk is inserted.

## Proof-relevant checks not reducible to scripts

The manuscript's full proofs explicitly check: local and global multiplicity; Borel branch construction; monotone nonnegative exhaustion; preservation of original segment endpoints; signed boundary/direction derivative; grazing-uniform lower bound; no uncontrolled continuity-component count; time reversal at the preceding flight; growth input and bounded representatives; empty future blocks; all-depth positive union bound; the strict endpoint `a<1`; actual joint-record conditioning; exactly one `c*^-1`; angular kernels first defined as measures; and the long-time roof derivative chain rule without an unproved lower bound.

What is not verified: a full source-independent reconstruction of historical pressure/spectral/pairing/inversion inputs; the target-roof `m^-2` clearance bridge; comparison capacity abundance; remaining shallow-incidence/boundary payments; the full original raw pointwise theorem; new remote CI; remote push. No finite diagnostic or successful compile is labeled a proof of these statements.

## Failure retention

The first revised build stopped at the original v112 manifest checker because the new main file was correctly different from the frozen v112 main blob. That failure is retained in `evidence/initial-revised-build-failure.txt`. The corrected new-revision checker verifies the new active manifest and independently checks the unchanged baseline copy; it does not disable the baseline hash checks. This source-identity failure was not a mathematical test failure and is not concealed by a false CI claim.

A second build correctly failed the typesetting gate because the new audit appendix cited two external keys not present in the original active bibliography. Both full bibliography entries were added; the failed log is preserved as `evidence/second-build-main.log` and the failure console as `evidence/second-revised-build-failure.txt`. The gate was not weakened.
