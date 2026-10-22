# Independent author reconstruction of native module 326

This is an internal author proof reconstruction, not an external referee report or independent expert certification. It reconstructs the new mathematical argument rather than inferring it from compilation, finite tests, or CI. No repository source was edited in this reconstruction.

## Exact scope and source identities

The inspected draft is `new-round-pressure/326_physical_boundary_stopping_pressure.tex`, SHA256 `b5fa48632c71bc6cb15e53bcf511da88f83b723ddef4bf3a0aac963aa4b918c1`. The last change inspected adds the precise distinction between the original stopped homogeneity partition and the auxiliary enlarged source-growth partition; it changes no formula.

The canonical source input inspected here is `new-round-provenance/math-section-boundary/324_canonical_collision_boundary_budgets.tex`, SHA256 `59b827efe313cd8f71c172f18c14cfa193a4d1e44f66d1532958831338f3c9bb`. Its source-supremum and determinant statements are uncapped; the endpoint cap is introduced only for its later Gauss-angle turning and charge statements. This distinction is essential for module 326.

The inherited native statements used here are modules 318, 319, 321, 284, the native curve-growth theorem, and the original optical comparison in module 313. This reconstruction checks their interface and the new reasoning that combines them. It does not represent a new external validation of every earlier proof in their dependency closure. The companion audit manifest records the inspected local files and hashes.

The conclusion reconstructed is the original unweighted complete physical-word pressure bound

\[
 \sum_{w\in\mathcal W_N(R)}\sup_{x\in[w]_R\cap M'_R}j_N(x)
 \le Q_{\rm stop},\qquad R\in[9/20,47/100],\quad N\ge0.
\]

All words, the original collision map, the true stable Euclidean arclength cocycle, and the original radius family are retained. The proof does not impose endpoint caps, discard small-capacity cells, or replace the original word supremum by a source average. It closes the pressure component of the original geometric input if the cited native inputs are used with their stated hypotheses. It does not by itself close the raw pointwise local limit, conditional return normalization, or joint spectral and arithmetic obligations.

## 1. The native cross-curve theorem has the exact required indices

Native 318, Corollary `cor:xd-backward-curves`, compares the backward arclength Jacobians of two actual regular histories of length N when their complete lifted words and homogeneity strips at exactly the times −1,…,−N agree. It imposes no current-strip condition. Its tangent directions may be arbitrary vectors in the stable cone; the two points need not belong to the same connected component of the physical word domain. It is a pointwise comparison and does not require a smooth physical path between the two points.

This is stronger than ordinary distortion on one short homogeneous curve and is the precise statement needed by module 326. A version requiring current homogeneity, only matching times −1,…,−N+1, or a connected planar class would not justify the proposed transfer. The written inherited corollary has none of those mismatches.

Time reversal converts the backward terminal angle into the original forward initial angle. Thus the inclusion of −N among the fixed past strips pays the last incidence logarithm in native 318. The current incidence is not divided out in the distortion comparison. The same corollary can compare the true stable direction and the affine direction at the same current point, without an assertion that the invariant direction extends continuously to a singular boundary.

## 2. Exact affine-to-momentum comparison

Let the positive physical differential product in coordinates `(s,phi)` be

\[
 D T_R^N=(-1)^N\begin{pmatrix}A&B\\ C&D\end{pmatrix},
 \qquad AD-BC=c_0/c_N.
\]

For the current affine unit tangent
\(e_R=(1,-\kappa_R)/\sqrt{1+\kappa_R^2}\), direct matrix inversion gives

\[
 \frac1{|D T_R^{-N}e_R|}
 =\frac{c_0\sqrt{1+\kappa_R^2}}
 {c_N\sqrt{(D+\kappa_RB)^2+(C+\kappa_RA)^2}}.
\]

On a horizontal initial source, varying alpha while keeping p fixed means `delta s = R delta alpha` and `delta phi = 0`; at the terminal collision `delta p_N = c_N delta phi_N`. Consequently

\[
 u_x=|\partial_{\alpha_0}p_N|^{-1}=\frac1{R c_N C}.
\]

Dividing the first displayed expression by `c_0 u_x` yields

\[
 \frac{R\sqrt{1+\kappa_R^2}C}
 {\sqrt{(D+\kappa_RB)^2+(C+\kappa_RA)^2}}
 \le R_+\Gamma.
\]

The terminal incidence cancels exactly; it is not estimated by a false positive lower bound. There is exactly one radius factor. The use of `R_+ Gamma`, although conservative, is valid uniformly in R.

Stable invariance and native 318 at the same point give `j_N(x) <= C_cross w_N(T^N x)`. The second use of native 318, between two representatives in one matching class, gives a second factor `C_cross`. Thus the final constant really contains `C_cross^2`.

The terminal-source identity is also exact. In `(alpha,p)` the collision map preserves area, so a regular N-step Jacobian has determinant one. If its lower-left entry is `partial_alpha0 p_N`, the lower-left entry of its inverse is its negative. Therefore

\[
 |\partial_{\alpha_N}p_0|^{-1}=u_x.
\]

This justifies the horizontal terminal source without altering physical time or using a roof identity under reversal.

## 3. Why the affine fiber has no omitted geometric exit

The intrinsic source of native 321 is the outgoing-direction fiber

\[
 \alpha_N+\varphi_N=\vartheta\pmod{2\pi},
 \quad -\pi/2<\varphi_N<\pi/2.
\]

It is one injectively parameterized arc. A numerical alpha seam is not an endpoint and must not be counted as a physical exit. Intersect this arc with the open set having one complete past word and one specified open homogeneity strip at each of −1,…,−N. Each connected component is an open interval in the displayed phi parameter and therefore has endpoints in the closed parameter interval.

There are finitely many prescribed past strips for a fixed class. Each individual strip closure lies strictly between the grazing angles, including the central strip closure. Hence all forward incidences `c_0,...,c_{N-1}` remain bounded below by positive constants along that class interval. These lower bounds depend on its strip labels; no uniform lower bound over the full homogeneity partition is asserted or needed.

The prescribed centers are fixed. Contact positions lie on finitely many compact circles; all flight lengths lie between the already proved physical positive gap and finite-horizon bounds. Limits of an approaching actual interval therefore exist subsequentially. They are unique: starting with the unique limiting current state, each backward intersection with its prescribed previous circle is a simple entry root, because that previous collision has positive limiting incidence. The prescribed root continues uniquely step by step. This only defines the limiting prescribed word, not a physical continuation through an obstructing unvisited disk.

If the current incidence remains positive, no past strip boundary is reached, and every unvisited disk remains clear, the finite record is a regular physical first-hit record in an open neighborhood of the endpoint. Only finitely many disks can intersect the bounded neighborhoods of these finite flight segments. Thus strict clearances have a common positive margin locally. The original homogeneity inequalities are also strict. The class interval would extend, contradicting maximality.

An unvisited contact cannot occur at a listed collision endpoint because distinct radius-R disks have a strictly positive gap. A segment that avoids an open disk can meet its boundary at an interior point only tangentially. This leaves exactly the stated alternatives:

1. current/terminal grazing;
2. a past strip boundary;
3. a genuine interior unvisited tangency.

No section or occupation boundary is added here because the original pressure sum is over all physical words without those event restrictions. Their later use in a roof theorem is separate.

## 4. Common positive source levels are actual, not formal boundary states

For any chosen exit, its defining interior distance is strictly positive and continuous on an approaching interval tail and tends to zero:

- terminal signed angular distance to grazing;
- the signed angular distance to the chosen original strip level;
- the true clearance of the chosen unvisited disk, after restricting to a tail with fixed side and an interior foot.

The continuous image of the connected tail contains an interval `(0,eta)`. This is sufficient; no monotonicity of that distance or nonzero derivative along the affine fiber is required. For a finite group of selected words, take the minimum of their positive eta values. Every sufficiently small common level is then represented by an actual regular point in each selected original open class.

The representatives initially produced by the intermediate-value theorem need not avoid the artificial source cuts. The next local argument repairs this without leaving the same class. At a regular horizontal source, `T^i` is a local diffeomorphism and its fixed phi level cuts an open collision neighborhood in an open alpha interval. At a marked flight, the physical coordinates satisfy

\[
 \det\frac{\partial(\vartheta,b)}{\partial(s_j,\varphi_j)}
 =\det\begin{pmatrix}\kappa_R&1\\-c_j-\kappa_Rt&-t\end{pmatrix}
 =c_j>0.
\]

The signed clearance differs from b by a fixed sign and a constant, so fixing positive clearance again leaves a nonempty open source-angle interval. The foot condition, actual word, and all the original open strip tests persist there.

The one-sided source cuts are countable/null in their own actual source parameter, not merely null for a two-dimensional collision measure. Their union cannot exhaust this open interval. A representative can therefore be selected in the genuine interiors of the required one-sided intervals. The source-growth partition from native 324 may use an enlarged curvature allowance and a different fixed cutoff from the stopped original partition. No matching of those two partitions is used: the selected point remains in the original open class while avoiding the source cuts.

This method never evaluates a derivative at zero clearance, a grazing state, or a homogeneity boundary. Every source estimate is used at a strictly positive interior level. The only later limit is of an explicit continuous cosine coefficient, with the selected supremum on the other side of the inequality fixed.

## 5. Word injectivity, and the absence of an unvisited-center count

On a fixed canonical collision source, the disk at that source is translated to the origin. The forward and backward source intervals each carry their actual lifted half-word. Their overlap therefore determines the whole lifted word. Translating its initial disk back to the original fundamental copy recovers exactly one original forward word.

For a marked source the chosen unvisited disk is translated to the origin, while the source angle and signed mark determine the line. Following its actual collisions backwards fixes the initial disk; translating that disk to the original fundamental copy recovers one marked copy of one original word. A single source overlap cannot produce two distinct original complete words. Different assignments of a mark to the same word would be irrelevant because the pressure proof selects and assigns each word only once.

Thus distinct selected original words occupy distinct complete source intervals within each common-level group. They need not have distinct homogeneity tuples, positive capacities, or macroscopically long intervals. A word may have many physical components; selecting a near-maximizer in one component is legitimate because the pressure asks for one supremum per word. The proof does not sum the suprema of all classes belonging to that word.

The already combined marked-source bound includes both signs and all physically recovered copies. An additional factor counting the centers of near obstacles would double-count an index already encoded by this one-copy construction. No such factor is needed or omitted.

## 6. Exact source budgets

The horizontal branch-supremum input from native 324 is a sum of whole-interval suprema, not an almost-everywhere pointwise root bound. For a half-length l,

\[
 \sum_I a_I\le H_{\rm H},\qquad a_I\le E_{\rm H}\sigma^{l-1},
 \quad E_{\rm H}=47/6,\quad\sigma=47/59.
\]

Its optical proof has the first displacement at least the true flight gap `3/50`, no virtual physical flight, and each subsequent kick-flight increases the positive displacement by at least `59/47`. Its first-image density and middle growth estimate use the qualified enlarged class and its own growth constant. No terminal homogeneity subdivision or incidence cap enters this statement.

At an internal horizontal source, the exact determinant is

\[
 u_x=\frac{c_i}{A_-A_+(d_-+d_+)},
 \quad d_\pm\ge\frac{\tau_-}{\tau_-+R_+}.
\]

The source-incidence factor `c_i` is retained from the actual collision area `d alpha_i dp_i = c_i d alpha_i d phi_i`. Hence `C_H=53/12` and the interval overlay gives

\[
 \sum_O\sup_Ou_x\le
 \cos h\,C_H H_H E_H
 (\sigma^{i-1}+\sigma^{N-i-1}).
\]

This is the factor needed to sum infinitely many original homogeneity boundaries. Uniformity without the cosine would not suffice.

The four families of assigned words have the following total budgets for their representative values `c_0 u_x`:

| Assigned exit | Exact payment |
|---|---:|
| Terminal grazing, both signs | `2 H_H` |
| Initial homogeneity boundaries, both sides of every level | `2 S_H H_H` |
| Internal homogeneity boundaries, both sides, all levels and indices | `4 S_H C_H H_H E_H / (1-sigma)` |
| Unvisited tangencies, all flight indices, original two signs and copies | `2 Q_mb / (1-sigma)` |

For the initial group `c_0=cos(h+epsilon delta)` exactly. For internal groups use `c_0<=1` and the two-sided source cosine. At each finite group the left side is independent of delta; letting delta decrease to zero only replaces the displayed cosine by `cos h`. With

\[
 S_H=2\sum_{k\ge k_0}\sin(k^{-2})\le2/(k_0-1),
\]

all levels are paid. There are two sides per original level and two signed families of levels; the latter are already included in `S_H`. This gives exactly the factors two and four shown above, without an extra missing sign factor.

The internal depth sum is at most `2/(1-sigma)`, and so is the sum of all marked-flight depth factors. Both are independent of N, including shallow marks. At N=1 the internal source family is empty, while terminal, initial, and marked-source payments remain valid.

## 7. Recovering the original supremum and order of limits

Let `S_w` be the supremum of the continuous affine inverse weight on the full finite regular domain of the current-normalized word. Finite cone expansion makes each such supremum finite. True stable states in the original cylinder map into this domain, so their original stable-word supremum is at most `C_cross S_w`.

For a finite word family and `epsilon>0`, select a point with affine weight at least `(1-epsilon)S_w`. The past homogeneity boundaries form a locally finite union of smooth coordinate level sets near a finite regular point, so the point can be selected off those boundaries. Continuity of the affine weight justifies this even if the original supremum was approached only through boundary points.

For every selected common-source representative z in its matching class, native 318 gives

\[
 (1-\epsilon)S_w\le C_\times w_N(z)
 \le C_\times R_+\Gamma c_0(z)u_x(z).
\]

Summing by the finite groups and applying the budgets above proves a bound independent of the finite family. Nonnegative exhaustion then pays the full word set. In this finite-horizon geometry that set is already finite for fixed N, but the exhaustion argument does not rely on its cardinality. Finally let epsilon decrease to zero and include the first comparison to the true stable cocycle. This gives exactly

\[
 Q_{\rm stop}=max\{1,R_+\Gamma C_\times^2\mathcal B_*\}.
\]

All common-level choices and limits occur at fixed R, fixed N and a fixed finite family. There is no exchange involving a collision-count limit, roof essential supremum, return normalization, or the outer microscopic-window parameter.

## Reconstruction outcome

No defect was found in this new boundary-stopping implication after the checks above. In particular, the proof genuinely pays the original complete-word supremum and not a weaker capacity moment. Its substantive new ingredient is the exhaustive stopping assignment and the finite-group positive-level transfer to the already quantified physical source budgets.

The qualified statement is a successful internal author reconstruction of the written implication from its identified native hypotheses. Finite auxiliary calculations, source hashes, and later compilation records are separate evidence and do not prove this continuous geometric argument. No claim of a completed raw pointwise local limit, external favorable review, or independent expert verification is made here.
