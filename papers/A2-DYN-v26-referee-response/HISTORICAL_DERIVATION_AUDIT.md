# Historical audit — revision 26

The current branch set was read before revision. The latest substantive report is on v25, not the v16 source last discussed in the conversation. The new revision starts at review SHA b9d11ff3bc2c08bb7410d93d3128d847e277cc08 and inherits the frozen v25 author source 4c07267338175932688a20a6021dae1b602074a0.

The v25 exact artifact 11443489844 from run 37530699923 was downloaded. Its archive SHA-256 is 5d06be36ffd606b2c8522edcfe0284a66f6cca0ddf0b7e2fa2d3b83dfd730a1c. The source archive supplies the earlier A2-DYN derivation chain. The detailed new dependency audit covers modules 40--41 (finite extraction and observed-count localization), 46--49 (fixed-order damping and unsmoothing), 50--51 (fourth-root stopping and retained isotropic rate), 52--53 (all fixed residual orders and separate-width boxes), and 54 (dependency guide), with their earlier marked/BV/covariance conventions. The existing regular-critical coefficient bound in module 04 is retained, not reintroduced as a new result.

The new estimate uses the already proved weighted stopping cost, but integrates it over a shape whose entire first radial moment has the required growth. It does not infer long-time raw derivatives from collision BV or call a finite union of boxes the full isotropic complement. The new signed correction identity uses exactly the finite-count measures already present in module 41. The physical law, weight, count and mark are fixed while only the analysis cutoff changes.

All inherited mathematical sources and scripts are checked byte-for-byte. The new proof adds two modules and an introductory/dependency bridge, not a replacement manuscript assembled by deleting old results.
