# Dependency acyclicity of the native physical-word pressure theorem

## Source and conclusion

This is a read-only author consistency reconstruction for `ps:pressure` and `ps:input-complete`, not a new referee report or an external expert certification. The inspected article is `papers/A2-DYN-physical-roof-variation-author-revision` at the supplied source commit `6708e30d1e8511e6ed2f4e3a6247c09628bd3ea9`. Local Git objects were compared with the working files for the 27 items in `ACYCLICITY_SOURCE_MANIFEST_326.json`; every comparison was byte-identical. No repository source, ref, remote application or CI state was changed by this check.

The inspected native 326 has SHA-256 `4be3dc9d6ffcc038e507c34ba6248e0157c2bc32cf5b040df151238cedb80508`.

**Conclusion: no circular use of the original complete physical-word pressure input was found in the dependencies of the new pressure theorem.** The old full-word pressure input is a consequence of 326, not an ancestor. The three substantive incoming branches are the deterministic same-word comparison in 318, the marked positive-clearance interval budget in 319, and the canonical horizontal interval budget in 324. Their required sub-results are independently upstream of the old pressure premise.

This conclusion concerns dependency acyclicity. It preserves the narrower external dependency on the qualified Demers–Zhang curve-growth lemma and does not reclassify a citation audit, internal reconstruction, finite check or successful execution as external mathematical certification.

## The two sums are different mathematical quantities

The old complete physical-word pressure is

\[
P_N(R)=\sum_{w\in\mathcal W_N(R)}
       \sup_{x\in[w]_R\cap M_R'}J^sT_R^N(x).
\]

It is the first clause of `input:v112-geometric-pressure` in native 266. A full two-dimensional word domain is involved in each supremum.

The curve-growth quantity is instead, for one already specified short homogeneous curve C,

\[
\sum_{V\in\mathcal G_l^+(C)}\sup_V J_V(T_R^{-l})\le C_g.
\]

It is `eq:ag-growth` in 280 and `eq:uc-growth-conclusion` in 283. Every inverse branch in this sum comes from that one original curve and carries its own physical inverse. The same constant works for the allowed initial curves, but the statement does not add a sum over all those curves or over all physical-word domains. This distinction is essential: 326 needs the new stopping/assignment argument to convert the available source sums into the original word-pressure bound.

## First incoming branch: qualified curve growth and canonical sources

| Native file and locator | Actual incoming facts | Result used downstream |
|---|---|---|
| 281, `lem:uc-transform`, `thm:uc-curvature` | True circular reflection differential, flight lower bound and explicit cone bounds | Invariance of the geometric-curvature class, including arbitrarily small positive incidences. No pressure estimate enters the proof. |
| 282, `lem:uc-central`, `thm:uc-expansion`, `thm:uc-distortion` | Actual finite-horizon geometry, monotone impact parameter, the preceding graph transform | One-step adapted contraction sum below one, weakened exponent threshold 1/2, and distortion along one physical homogeneous curve. The finite candidate count concerns one next collision, not long-word pressure. |
| 283, `thm:uc-growth` | The preceding native (H2)–(H4) verifications plus the qualified curve-sum statement in Demers–Zhang Lemma 3.2(b) | The uniform one-initial-curve inverse-Jacobian sum; countable actual source-cut coverage; discharge of `input:ag-growth`. The current dependency notes correct the page locator for the inspected external version. |
| 284, `lem:mc-first`, `eq:mc-class`, `lem:mc-family` | True first image of a fixed physical momentum fibre; the same native curvature/complexity arguments | A fixed enlarged curvature allowance with its own `hat k0`, `hat ell*`, `hat Cg`; a summable, source-labelled first-image density family. The smaller marked-foot class's growth constant is not silently reused. |
| 284, `eq:mc-last-cancellation` in `thm:mc-kernel` | Exact one-collision graph differential | `abs(dp_next/dell) >= k_- tau_-`, before terminal homogeneity subdivision; the terminal incidence cancels algebraically. |
| 324, `thm:cs-half-sup` | The qualified first-image family, its own growth constant, the exact last-collision cancellation, finitely many terminal first-hit branches | Complete interval-supremum sums for canonical sources, with no endpoint cap and no terminal homogeneity cut. The proof redoes the chain-rule sum; it does not turn an endpoint root-density bound into a branch-supremum sum by assertion. |
| 324, `lem:cs-determinant`, `cor:cs-overlap` | Finite physical optical matrices, collision-area invariance and the purely combinatorial interval-overlay lemma `lem:mb-overlay` | The horizontal factor `c_i` and the complete two-half interval budget used by 326. |

The optical convention in 324 is verified by its exact conjugacy: l actual flights and l−1 internal reflection kicks. The source constants and the overlap bound used by 326 precede, and do not require, the later Gauss-angle variation/charge theorems in 324. Thus the latter's references to 320 are not an incoming dependency of the pressure proof. Modules 323 and 325 are likewise not ancestors of `ps:pressure`.

In particular, the `C_*` in 284's enlarged-class requirement is the explicit curvature-forcing constant `64061/8100` from 281, `eq:uc-affine`. It is not the pressure-dependent roof constant `C_star = C0 Q*/(2 c_* lambda_circle)` from 266. Likewise A_* is the geometric density-family budget in 279, and C_g or its enlarged-class version is the one-curve growth constant in 283. None of these source constants contains the old Q_*.

The stage-280 statement `input:ag-growth` was an explicit input at that stage. Native 283 discharges it for the stated class. Calling that stage-280 statement an input is not evidence of a surviving full-word pressure premise in 283 or 324.

## Second incoming branch: marked positive-clearance source

1. Native 279, `thm:ag-density`, `lem:ag-branches` and `thm:ag-family`, differentiates the true first collision from the marked foot, counts its finite actual first-hit branches, and sums the grazing pieces with their exact incidence-weighted densities. It uses neither growth nor full-word pressure. Its opening explicitly separates this route from the pressure-dependent summation in 278.
2. Native 316 defines `H_nm` in `eq:nm-H` using only this source family, native 283's C_g, the finite terminal next-hit count and native 284's last-collision cancellation. `thm:nm-kernel` is a momentum kernel on the actual angular source; it is not the original physical-word pressure.
3. Native 319, `thm:mb-branch-sup`, proves the stronger interval-supremum budget directly: first-image density supremum, l−2 applications of actual curve propagation, then the final physical collision. It does not infer the interval sum from a common-target root sum in 316. The l=1 case is treated by the finite first-hit partition.
4. Native 317, `thm:bf-foot-determinant` and the first identity in `cor:bf-wronskian`, supply the exact two-sided root weight. These are finite-trajectory optical identities from the reflection matrices in 277, `thm:xf-jacobian`, the actual line measure and collision-area change of variables. The endpoint measure identity is also recorded in 286, `thm:rc-coarea`; this local identity needs no global pressure bound. The words “pressure input” in the opening of 277 refer to the separate summation in 278, not to its finite Jacobi identity.
5. Native 319's own `lem:mb-overlay` combines the two actual interval partitions. This proves `thm:mb-two-sided-sum` with the displayed Q_mb. The last paragraph expressly distinguishes that marked-source sum from `input:v112-geometric-pressure`.

Native 326 uses this result only at **positive clearance levels**. Its proof does not need the stronger zero-clearance trace statement in 316/319, a critical zero-offset cancellation, or any roof-height theorem. Consequently none of the independent critical or global roof conclusions is fed backwards into its marked-source budget.

## Third incoming branch: same-word comparison

Native 318, `cor:xd-backward-curves`, follows from `thm:xd-cross-distortion`. The proof uses the exact physical differential in **313**, `lem:eo-differential`, and two deterministic comparisons established within 318: `lem:xd-paired-records` and `lem:xd-log-incidence`.

The only substantive localization input to `lem:xd-paired-records` is native 308, `cor:ae-geometric`. Its position bound follows from:

- The real 94-flight anchor geometry, explicitly reconstructed in `retained-geometric-input.tex`, `lem:sc-buffer` and `lem:sc-anchor`.
- The direct positive disk-product gap in 300, `lem:sc-gap`; full-record quartic coercivity in 302, `thm:ss-quartic`; and the deterministic interior inequalities in 304, `lem:bl-caccioppoli`, `lem:bl-interior`.
- Native 308's hard-interval work identity and anchor-layer contraction, `lem:ae-hard-interval` and `thm:ae-layer`. These compare one real record with a global disk-product minimum and do not sum words or physical probabilities. The companion transverse budget in 307 is also deterministic.

There is a genuinely pressure-conditional side consequence in **299**, `eq:gv-localized-pressure`, within `prop:gv-source`. It is explicitly conditional on `input:v112-geometric-pressure`. That roof-density consequence is **not** used by 300/302/304/307/308 or by 318's comparison proof. The positive gap and endpoint-deficit identities used by the deterministic branch are separately proved geometric identities. Treating every statement in a shared file or nearby numbered module as one indivisible dependency would create a spurious cycle here.

The true stable/unstable lines used in 326 are themselves constructed in 313, `lem:eo-differential`, by the explicit slope contraction and its time reversal. Their existence and norm conventions do not invoke a pressure or mixing theorem. Native 318 is therefore a uniform comparison for two actual records of one word, not a premise that has already paid the sum over words.

## Pressure-named material in 314–319

| Module | Status relevant to this audit |
|---|---|
| 314 | Its weak-roof and physical-margin results are not used by `ps:pressure`, 319's branch-supremum proof, or 324's canonical branch-supremum proof. Its concluding reference to unrestricted pressure states that pressure is not inferred from those roof spaces. |
| 315 | `thm:sm-full-multiplier` uses intersections of the actual momentum kernels proved in 284 and layer-cake bounds. It explicitly makes no marked-word pressure assumption. Neither this multiplier theorem nor its later weak-roof consequences are ancestors of `ps:pressure`. |
| 316 | The all-time angular kernel uses 279, 283 and the local terminal cancellation in 284. H_nm has that explicit formula, without Q_*. |
| 317 | Only the finite marked-foot optical determinant and local root-weight identity are needed by 319. Its other boundary-flux/critical results are not required to obtain those identities. |
| 318 | The cross-curve theorem uses deterministic anchor localization. References to a “preserved pressure candidate” describe its eventual application; the final scope remark explicitly leaves the complete word sum unpaid at that source stage. |
| 319 | The marked interval-supremum sum is proved from one-curve growth and positive optical products. Its mention of the original pressure input explicitly distinguishes the two statements; it is not an assumption. |

Native 321 enters 326 through the definition of the intrinsic affine fibres `tc:fibers` and the identification of the former pressure interface. The capacity-moment theorem `tc:all-classes` is not used to supply the missing pressure bound. The new stopping argument supplies that bound directly.

## Direction of the completed input

The logical order is: the upstream physical geometry, qualified single-curve growth and deterministic same-word comparison; then complete one-dimensional source supremum budgets; then the new physical boundary stopping and one-word assignment in 326; then the completed three-clause geometric input in `ps:input-complete`; finally the inherited consequences in 266–269.

The two optical clauses of that completed input come from native 313, `thm:eo-optical`, with constants 30000 and 6400. Its `cor:eo-pressure-scope` distinguishes those already proved optical estimates from the formerly separate full-word sum. The occurrence of the input label in this corollary is an output/status statement, not an assumption in the optical proof.

One locator precision emerged: the current ledger's phrase “Native 260 differential” is less exact than the actual cited label, `lem:eo-differential`, which is in **313**. The underlying finite-flight optical structure is inherited, and there is no mathematical cycle; the label-resolved source trace above gives the precise origin. No native proof edit is required for the acyclicity conclusion.

The original single-unvisited-clearance same-roof m^-2 issue, conditioned comparison-pool abundance, normalized low-load shortage, and joint spectral/arithmetic/conditional interfaces remain distinct. Acyclicity of the new geometric pressure proof does not assert their completion.
