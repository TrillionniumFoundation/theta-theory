# Mathematical audit of the new native proofs

## Conventions fixed before differentiation

The original radius interval is [9/20,47/100], unit speed is unchanged, and the minimum disk-to-disk flight is 3/50. Collision angles are outward-normal angles. For an actual oriented flight, v_i dot n_i = c_i and v_i dot n_{i+1} = -c_{i+1}. Thus both endpoint derivatives of its direction are negative: -R c_i/tau_i and -R c_{i+1}/tau_i. The reflection equation is 2 alpha_i - theta_{i-1} - theta_i = an odd multiple of pi on a fixed local lift. Displacement labels, true collision count, the initial counted section visit and terminal section event are unchanged.

## Inequalities checked in the native argument

1. The sign-conjugated Jacobian has COLUMN diagonal excess 2, not generally row diagonal dominance. N is normalized on the right by the diagonal D; A=(Id-N)D and A^-1=D^-1 sum N^k. Reversing these factors would be an error. Its column contraction is a*/(1+a*)=47/53.
2. For v-neighbor ratio at most lambda=50/47, the exact weighted column margin is 2-2(47/6)(3/47)=1. Multiplication by the nonnegative inverse is on the right. This yields both the weighted norm and the Green-column exponential decay. Missing end neighbors improve the inequalities. Zero incidences cause no division.
3. Boundary forcing for the first endpoint jet has l1 norm at most a*(|eta0|+|etam|); weighted forcing at most lambda times this. Adding the endpoints gives C1=59/6 and M1=56/3. The m=1 empty interior and m=2 shared boundary row are included.
4. Each direction derivative is the imaginary part of a complex-log derivative. Set partitions supply all mixed terms. The flight norm sums count each vertex at most twice. No physical word count or collision count is multiplied into the estimate. All higher jet recursions isolate precisely one one-block term and involve only previously bounded derivatives.
5. Every limiting physical flight still has length at least 3/50. A formal implicit continuation of reflection equations through a limiting grazing configuration is not an admissible orbit continuation through an unvisited disk or a section cut. Uniform derivative constants do not supply a uniform physical chart radius.
6. The Euclidean third norm derivative has three terms. Its fourth derivative has a norm bound 15/tau^3: 6 from the prefactor, 3 from v and 6 from P. The complete fourth composition counts are 1,7,6,1. Hence D4=R+7R^2/tau+18R^3/tau^2+15R^4/tau^3, not a coefficient guessed from a finite expansion.
7. Differentiating the exact third Schur identity produces S4[J1,J2,J3,J4] plus THREE S3 terms involving K14, K24 and K34. These terms generally do not vanish. Their equivalent negative H^-1 contractions check permutation symmetry but are not used to obtain a grazing bound. F4=2D4 C1^4+6D3 C2 C1^2 is uniform in m.
8. The 2x2 operator-norm conversion costs a factor 2. The scalar fourth Taylor integral contributes 1/24; the Hessian Taylor integral cancels that operator factor 2 through its integral 1/2. The entire interpolation segment must stay in the original physical branch.

## Normalization and limiting scope retained

The collision measure is d alpha d p/(4 pi). The original section normalization c*=91/(10000 pi), the one-copy clearance factor 1/(4 pi R), its section version 1/(4 pi R c*), and optical factor omega are not altered. No new derivative estimate multiplies by c* or removes it. The all-order jet estimates apply pointwise on every actual regular itinerary and hence to every exact-label/roof restriction without changing the restriction. They are not densities of the endpoint pairing source. Per-orbit optical decay cannot be summed without the appropriate physical pressure/source theorem.

The original m^2 L-infinity(dt) target topology and B-outermost order of limits are retained. A fixed-count grazing-limit corollary is not an interchange of m and grazing limits. No conclusion about the full normalized source follows from the constants in this audit.

## Independent computational diagnostics and limits

`check_reflection_resolvent.py` uses exact rational nonsymmetric tridiagonal solves, including simultaneous zeros and rows that are NOT diagonally dominant. These coefficient arrays are explicitly algebraic test cases, not asserted physical billiards. Independently, actual nearest-hit triangular-lattice rays generate physical collision words, all true intermediate collisions, physical roofs, clearances and exact labels. Reflection tensors are compared to the action Hessian and to independent Taylor-series arithmetic. Same-word endpoint finite differences are used only after checking the unchanged physical word.

The first execution passed 48 rational chains, 304 inverse columns, 33 zero-incidence arrays, and 77 non-row-dominant rows. It also checked 72 physical records/768 flights, six original section-to-section records, and 47 admissible finite-difference perturbations; 60 examples reject omission of the mixed fourth-order terms. These are diagnostics, not proof by sampling. The authoritative repeatable execution is recorded in `build/revision/current-validation.json`; no CI or formal-proof certification is inferred from it.

## Failed attempts retained

An initial inherited-source qualification was rejected when unrelated Python startup warmup text polluted its JSON output. The output and rejection are retained. Disabling that startup component, without changing mathematical checks, gave a complete repeated baseline qualification. The first new native LaTeX audit also rejected an overfull provenance SHA; explicit break opportunities repaired the layout, not the mathematical content. Failed/early run evidence and clean final receipts remain distinct.
