# Independent author reconstruction of native module 322

## Exact inspected sources and conclusion

This audit independently reconstructs the mathematical argument in the root author's complete `core/322_positive_critical_marked_source.tex`. It is an author proof check, not a referee report or an independent external expert certification.

| Source | SHA-256 inspected |
|---|---|
| Root native module 322 | `5c1e539958c3296f389eecbee3986bd6dfc7a5ce613943c6149e745c5bc269c1` |
| Independent draft `math-boundary/322_positive_physical_critical_fans.tex` | `bbbd02362e5f233527f37f63db8afe06c0d2f9a67d851f56ee02ce906a895e5f` |
| Native module 319, actual one-sided branch suprema | `ea974d39e39822598fb38ba78083702900559e04615ff00a59decbea73b25845` |
| Native module 285, critical Hessian and fan normalization | `ce75a732b7e6a1ad6ad6ded5083b83b0163b6c929d1842b996c39eb38955cc71` |
| Native module 286, exact radial coarea and Borel critical bands | `a9941b7bb977c527b3db20be9afd43de196ebda87a1a4347c5b298657fbff442` |
| Native module 317, physical half-ray determinant | `1d29cdf129519cdabedf8356de86b164e2f5576c57c99b1451e3db55c7857187` |

**Conclusion:** no substantive mathematical gap was found within the stated stratum: the original zero-clearance unvisited mark, normal record endpoints, every limiting visited incidence positive, and the actual finite analytic physical/section/record/roof tests. The proof supplies a complete bound for the leading incoming fan, including collapsed zero-clearance angular slices and every marked index. It does not claim a visited-grazing trace, a collision-uniform sum of nonleading local remainders, or completion of the raw pointwise LLT.

## Reconstructed proof chain

1. **Finite actual analytic conditions, including degenerate differentials.** Positive visited incidences make the fixed strict reflection word analytic in local endpoint coordinates by its invertible internal Hessian. Only finitely many lattice disks can meet the finitely many nearby bounded segments. All other disks have a uniform margin in this fixed local neighborhood. The actual first-hit and no-extra-collision conditions are finite analytic sign tests, with perpendicular-foot and endpoint cases retained. The original section is a finite union of coordinate rectangles (native 303); its finite-time occupation and endpoint tests remain a finite Boolean formula under the regular auxiliary maps. The actual roof is the analytic flight-length sum. No arbitrary Borel selector is assigned this analyticity.

   If an active analytic function has zero linear part, its first **nonzero homogeneous Taylor polynomial**, of any finite order, is used. On the circle that polynomial has finitely many zeros; away from them its sign determines the function's sign along all sufficiently short radial points, uniformly on compact angular subintervals. Identically zero functions have their actual constant truth values evaluated in the Boolean formula. Thus a positive limiting sector has an open interval of admitted generic rays. This reasoning covers critical roof inequalities whose first nonzero term is quadratic.

2. **The limiting angular fraction is the actual coarea fraction.** The momentum chart `z=(p_0,p_m)` has derivative `R^-1 diag(-1,1)G` from endpoint coordinates and is invertible. Its first-order change from `y=G^(1/2)(q-q_x)` is the exact invertible map in native 285, so positivity of angular measure is preserved. For completeness, the inherited radial coarea formula in native 286 has a continuous and locally bounded optical coefficient at each fixed positive-visited germ. The just-proved angular indicator limit exists except on finitely many rays. Dominated convergence therefore identifies the leading physical coefficient with `mathfrak J(x)*beta_y(x)`, including a zero leading coefficient when `beta_y=0`. This does not use bulk singular-nullness and does not require a uniform local radius in the collision count. An explicit sentence making this inherited dominated-convergence step visible in the native proof was recommended to the author.

3. **Positive clearance is a true local coordinate.** Native 317's determinant is

   \[
   |\det D_{(\vartheta,u)}(p_0,p_m)|
      =A_-^pA_+^p(h_-+h_+)>0.
   \]

   The backward and forward clearance columns have opposite signs, yielding the positive sum `h_-+h_+`, not a cancellable difference. The identity continues along each fixed strict positive-incidence word. Hence `D_z u(0)` is a nonzero linear form. A positive admitted angular sector containing only `u>0` has a generic ray with `D_z u(0)e>0`, after the two zero directions are removed. On that ray `u(re)=d r+O(r^2)` and `d u(re)/dr=d+O(r)>0`. This gives representatives at **every** sufficiently small positive clearance, not merely along a germ-dependent sequence.

4. **Representatives can satisfy both genuine partitions.** Each admitted generic radial point is interior to the actual strict-word source and its nonconstant original tests. At fixed positive clearance, the local `(vartheta,u)` coordinates therefore provide a nonempty open angular interval of actual records. Removing the two partitions' angular-null cuts still leaves representatives, chosen arbitrarily close to the radial point. They remain inside an interval of each physical partition and approach the original germ. For finitely many germs the minimum of their local positive-clearance ranges is positive. This construction requires neither a common range over all words nor a global exchange of a null set with a limit.

5. **Marked-state uniqueness includes periodic normalization.** Translate the marked disk to the origin and retain its impact sign. A limiting direction and sign determine the oriented marked tangent line. Starting at its foot, the first strictly met disk in either direction is unique; every earlier limiting contact is tangent and cannot serve as a positive-incidence visited collision. Its reflection fixes the next ray, and iteration determines the two complete strict half-words, including any later genuine visit to the marked disk. At fixed `m,j`, the two collision counts determine the initial disk. Translating that disk to the original fundamental cell is unique. Thus a second periodic lift is not a second marked copy. Distinct side sectors at this same marked state are united before assigning a fraction.

6. **Distinct germs eventually occupy distinct half-intervals.** In a finite family, different same-sign limiting directions have a positive separation after a common seam is chosen away from them. The physical branch derivative satisfies

   \[
   |\partial_\vartheta p_0|,\ |\partial_\vartheta p_m|
       \ge k_-a_\circ
   \]

   on their respective one-sided intervals, by native 319. If two representatives were in the same interval, monotonicity and the fundamental theorem of calculus would force their momentum difference to exceed `k_-a_circle` times their separated angular difference. Their endpoint momenta both converge to zero, contradicting that bound. The argument is applied separately to the backward and forward partitions. No shared nonzero target momentum or independent sampling of the two halves is assumed.

7. **Branch suprema transfer to the full positive germ sum.** At each common positive clearance, each selected reciprocal half derivative is bounded by its interval supremum. Distinctness permits their finite sum to be paid by `H_nm`. All limiting visited incidences are positive, so the finitely many optical matrix entries, positive momentum derivatives and ratios converge on each fixed word. The positive-clearance limit can therefore be taken in that finite sum. Only then is the supremum over all finite germ subfamilies taken. This proves the complete half sums, each at most `H_nm`. It also establishes countability of the positive-weight family. A collapsed angular slice at clearance zero is never assumed populated.

8. **Optical decay, exact counts and coefficient.** The true half counts are `j+1` and `m-j`. The optical incoming endpoint has no added reflection kick. Native 319 gives reciprocal bounds `E_*sigma^j` and `E_*sigma^(m-1-j)`, with `sigma=47/59`. Native 317 gives

   \[
   u_x\le C_{\rm foot}(A_-^p)^{-1}(A_+^p)^{-1},\quad
   C_{\rm foot}=607/90.
   \]

   Summing with either individual bound and the opposite full half sum gives two inequalities; their minimum is exactly `Q_mb*sigma^max(j,m-1-j)`. Both impact signs are already included in `H_nm`; no additional sign or word multiplicity is required.

   Independently rederiving the original fan normalization gives

   \[
   \mathfrak J=\frac{\omega}{2c_*\sqrt{\det G}}
      =\frac{\sqrt{\det G}}{2R^2c_*}u_x.
   \]

   Native 285 proves `sqrt(det G)/R^2<=170/9`. Since the united physical fraction is at most one, the coefficient is exactly `C_pc=(170/(18c_*))*Q_mb`. One original conditioning factor is present. The angular normalization uses the normalized `y` fraction, and no factor from a different endpoint angle has been substituted.

9. **Every marked index and the original limit order.** For every `0<=j<m`, `max(j,m-1-j)>=(m-1)/2`, including the two shallow endpoints. The complete leading-fan sum over all `m` indices is at most `C_pc*m*sigma^((m-1)/2)`. Multiplication by the unchanged `m^2` leaves `C_pc*m^3*sigma^((m-1)/2)`, which tends to zero. These bounds are independent of radius and any chosen original exact-label or roof-value restriction, so the corresponding suprema are taken after the full positive sums. The local clearance limit was used only at fixed radius/count and finite family. No outer guard width or original order of limits is exchanged.

## Comparison of the independent proof drafts

The root and independent draft use the same actual geometric mechanism and exact optical factors. The independent draft splits the analytic sign and representative construction into two lemmas and states the bounded-coarea dominated-convergence identification more explicitly. The root draft is shorter and gives the same finite-family transfer and all-index decay. The inspected root hash already corrects “avoid the partitions” to “avoid their cuts and exceptional angular sets”, and limits the outstanding multiplier language to the separate boundary measures; it does not reopen native 315's proved bulk integrability theorem.

No finite checker or floating-point run was used to justify sector persistence, physical uniqueness, full family exhaustion, or interchange of limits in this reconstruction. These are proved by the finite analytic sign argument, the actual first-strict-hit dynamics, the exact determinant, monotone branch separation, and positive finite-subfamily exhaustion.

## Remaining scope, kept explicit

The theorem pays the leading positive incoming fan of the specified zero-clearance marked stratum. A visited grazing limit does not have the positive finite optical products used here. Nonleading critical coarea remainders can have germ-dependent neighborhoods and require their own uniform sum. Other section/pairing traces and same-roof positive-source shortages retain their original obligations. A general Borel pairing selector may restrict an already defined fan measure; its angular trace cannot be invented by the analytic sign argument. None of those remaining tasks changes the valid all-index leading-fan conclusion established by module 322.
