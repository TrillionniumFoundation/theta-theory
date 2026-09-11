# Historical derivation audit for A2 v15

## Frozen inputs and direct reading

The latest report and its scalar-linearization/width companion were read at `0c523413ef7ffa2dedd1ab471ce58b3275896a93`. The corresponding author source is `e136929b120912586266fb78e0ae7b3c9d43bfd6`. The complete native manuscript tree is `d516d2bc9230ea4a333f3d41ba2718485a307b27`. The earlier v13 report and v14 response/history establish the revision chain; they are not a substitute for the mathematical source reading.

The full abstract, input structure, introduction, analytic comparison, physical cocycle and width proofs, independent-contact inverse and bibliography were read. The six locally reproduced baseline files were matched exactly to their live Git blob identities. The original v4 half-line construction, relative determinant definition and complete two-boundary factorization proof were read through the start of its physical-law subsection. The v9 energy-profile, convolution, smooth uniqueness and stability arguments were read through the finite-jet discussion. The latest referee's source audit and original diagnostic script were read, and that script was reproduced exactly and rerun.

This is a targeted audit of the current requests and their historical dependencies. It is not a claim that every inherited appendix theorem, every global realization step or the entire statistical acquisition chain was newly checked line by line in this session.

## Use of historical derivations

The new scalar argument starts with the physical first-hit return already defined by the stationary half-line. Its general existence/uniqueness proof is classical. The physical product corollary depends on the retained v14 exact Schur identification, itself dependent on v4 relative factorization. It never divides an uncontrolled absolute action error by an exponentially small twist. The width converse is checked against the v9 normalized energy pushforward, including the factor at zero. The curvature/flight notation is checked against the original linear half-line orbit and the last-jet scaling in the independent-contact inverse.

## Preservation and verification boundary

The new native directory is a Git-tree extension of the entire frozen v14 directory, with explicit source/metadata overrides only. Original versions of overridden files are archived by their existing blob identities. All other active and inactive historical files are inherited unchanged. Earlier manuscript directories, review reports and repository settings are not altered. The initial temporary source-export workflow failed without useful execution logs and is omitted from the delivered tree.

The local workspace materialized the edited-source subset, not every inherited source file. The revised-section smoke build therefore does not certify a full-paper build. `VERIFICATION.json` records the actual edited-source and numerical checks, while `tools/verify_v15.py --scope full` is provided for the complete checkout. No assertion of a full formal proof audit is inferred from preservation or numerical success.
