# Mathematical audit of the new 300-301 continuation

This is author-side proof checking, not another referee report or an independent expert certificate. Continuous proofs are in native LaTeX; diagnostic success is not their proof.

## 1. Physical input and exact interval coverage

The primitive-row construction of retained287 is re-read at b47 and preserved exactly. The four closed t-intervals cover [0,1/3] and their row vectors are primitive. The first width increases (derivative numerator 2-3t); each other positive numerator decreases with derivative 3/(2N)-s while its denominator increases. Their exact squared maxima are all strictly below (179/400)^2. The longitudinal projection is <H/2 at every direction, not merely almost every direction. Integrating real specular velocity jumps gives deviation <=2H sum c. A sum <1/4480 would put the real trajectory strictly inside an original disk because 179/400+1/400=9/20. The block endpoints are not extra reflections. 94*(3/50)>H, and the 93 interior collisions yield anchor cosine 1/(4480*93). This reconstructs the precise inherited294 input used here; it is not re-credited as novelty.

## 2. Full gap, endpoint signs and arbitrary sublevel points

The endpoint gradients are -v0 and v_last; interior gradients are v_prev-v_i=-2c_i n_i. Complete telescoping includes both endpoints once. Every flight gap is ell_i|vhat_i-v_i|^2/2; every contact gap is nonnegative on the full closed disk. At Q the contact sum is exactly E=R(2-c0-cm). A(Y)<=L therefore gives the same budget for ALL sublevel configurations, not merely a stationary or physical minimizer. Consecutive disks stay separated by3/50, so normalizations never divide by zero. Interior points and repeated nonconsecutive centers are allowed. The endpoint triangle bound is 2sqrt(2RE), not sqrt(2RE); both distances to the supporting point are included.

## 3. Main new telescoping identity

With delta_next-delta=(ell-tau)v+r, r=ell(vhat-v), projection on each varying transverse frame removes the longitudinal increment. Summing leaves the turning sum +(w_l-w_{l-1})*delta_l. Its sign and indexing are checked explicitly; dropping it is false and a rational negative control detects that mistake. Weighted Cauchy-Schwarz gives flight cost sqrt(2*N*T*E), T=H+4Rplus=187/25, N=94. Reflection gives |Delta w|=2c, and the already SUMMED contact budget gives turning cost <=2sqrt(N*Rplus*E). No artificial independence, curve smoothness or m-fold sum appears.

## 4. Constant and exponent audit

An anchor has |delta|<=sqrt(Rplus/c_anchor)*sqrt(E)<443sqrt(E). The last anchor before a nonanchor index, or the actual first endpoint, is fewer than94 edges away; otherwise the intervening complete block would contain an anchor. Flight and turning terms are <38sqrt(E), <14sqrt(E). The incoming-normal parallel component costs c_i|delta_i|<=sqrt(Rplus E)<sqrt(E), not sqrt(RE/c_i). Thus |n_i delta_i|<=496sqrt(E). Disk curvature yields delta_i^2<=2Rplus*496sqrt(E)=11656/25 sqrt(E)<484sqrt(E). This proves22 E^(1/4). At an anchor use delta<=2R and443sqrt(E) together, rather than misusing443sqrt(E) as22 E^(1/4) at arbitrary E. At the endpoints8RE<=4sqrt(E) because0<=E<1. E=0 is handled directly by positivity. The coefficient22 is in the fixed unit-lattice normalization; no scale-invariant dimensional claim or optimal exponent is made.

## 5. All-center clearance, existence, and physicality

Common affine parametrization proves BOTH directed Hausdorff bounds. Distance-to-set is1-Lipschitz in Hausdorff distance, simultaneously for every point of the plane. Taking infima over the same third-center set controls all lattice obstacles without enumerating a finite sample or assuming nearest-foot differentiability. The third-center set includes disks appearing elsewhere in the word.

A disk-product minimum exists by compactness. Each velocity error is <=sqrt(2E/tau_minus); actual interior c_i greater than that makes the minimizing gradient nonzero. Disk first-order optimality then supplies the correct inward normal. Equal unit speeds imply incoming and outgoing normal components -lambda/2,+lambda/2 and equality of tangential components. Endpoints have norm-one gradients, hence normal departure/arrival. Strict third-disk clearance and the exterior incident-disk quadratic identity prove first-hit physicality. Only AFTER this proof is the zero endpoint gap invoked to show uniqueness among all minimizers. No physical continuation across grazing is inserted.

## 6. Probability and normalization audit

The bad-word property is defined at fixed R and m on a countable word set, avoiding a measurable choice of a minimizer. The witness functions are measurable by countable infima and finite minima on regular charts. The new source consequence multiplies a pointwise inclusion by the SAME original exact event, nonnegative weight and actual roof selector, then integrates the original section measure once. There is no coarea Jacobian because no variable is changed. If the inherited collision measure is d(alpha)dp/(4pi) and section normalization c_*=91/(10000pi), these factors remain exactly where they were in dnu_R^*. They are not reinserted or squared. Countable marked sums are positive, so monotone convergence is valid without independence.

The result is a positive MEASURE inequality. Density ordering needs absolute continuity of the relevant pushforwards (or their absolutely continuous parts); no singular contribution or paired endpoint trace is silently dropped. There is no integration over R and no conversion of an R-integral to sup_R. It neither changes a microscopic window nor the B,m limit order. The final normalized estimate is still missing.

## 7. Execution boundary and negative controls

The local container and both Python entry points returned ServerError before any check could execute. Their attempted archive hash check is not a receipt. The new scoped GitHub workflow must be read at its exact commit before any execution success is asserted. The diagnostics intentionally include exact algebra arrays that are NOT claimed physical; explicitly parameterized actual one-flight/bounce records; real first-hit floating-point rays; and failed sufficient-clearance tests retained despite the known minimum being physical. No rejected ray is silently replaced by an easier sample. A build/diagnostic pass remains auxiliary error detection, not an independent reconstruction of the full historical analytic chain.
