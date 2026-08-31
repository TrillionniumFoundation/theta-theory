# Independent Referee Report — Round Eleven

**Manuscript:** A1 — Exact Benchmarks  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *JAMS*  
**Recommendation:** **Reject**  
**Reviewed branch:** `revision/round11-referee-positive-closure-11paper-2026-08-31@e81cbf57624d21be23ee9d982a1255c076363761`  
**Reviewed source:** `revision/round11-referee-final/A1_COUPLED_EXTENSION_SMOOTH_SUSPENSION.tex` (Git blob `e4bec81413db37a5a14a0bbf7d11223bc4f88524`)

## Executive assessment

Round eleven correctly replaces the nonexistent inverse of a one-sided past shift by the coupled natural-extension map

\[
(x,y)\mapsto(\sigma x,x_0y),
\]

and it no longer assigns a spectral gap to the bilateral Koopman shift. Those are genuine corrections. The new Hamiltonian and current constructions, however, are not defined on the spaces stated in the manuscript. The principal obstruction is elementary: one connected source sheet maps across several target sheets, so the proposed disjoint-sheet return cannot be a continuous first-return map unless the source is refined by the target label. The claimed higher-order current calculus likewise generates corner and flag currents that are absent from the declared Banach space.

## Major mathematical objections

### 1. The four-sheet Poincaré return is not a map into a disjoint four-sheet section

On source strip \(i\), the baker branch maps the vertical strip onto a horizontal strip spanning all four target vertical strips. Hence the target sheet label changes along the internal curves

\[
Q_i(q)=s_j(a).
\]

The manuscript keeps only four source sheets and says that the target label is retained. A continuous map from the connected sheet \(i\) to a disjoint union of target sheets cannot change component without the source being split along those preimages. The required section is at least the \(16\)-cell refinement \(C_{ij}\), together with all boundary germs. It is not the four-sheet section used in the theorem.

Consequently the asserted smooth mapping torus and its Poincaré return are not constructed.

### 2. The collar-isotopy lemma is incompatible with the advertised branch map

The affine branch sends the entire boundary of a vertical rectangle to the boundary of a differently placed horizontal rectangle. An isotopy that is constant in a collar of the rounded source boundary cannot simultaneously agree with that affine map up to the boundary. Multiplying a generating Hamiltonian by a cutoff changes the time-one map; “exactness permits the cutoff error to be removed” is not a theorem and no correction equation, support condition, or endpoint matching is supplied.

This is especially serious because the mapping-torus gluing requires a globally defined exact symplectomorphism of the actual incoming and outgoing section components, not merely a local interior approximation.

### 3. Autonomization does not repair the missing component map

A periodic time-dependent Hamiltonian on a fixed disjoint union produces a symplectic self-map of each connected component unless the topology already specifies a legitimate cross-component gluing. The proof simply declares that retaining the sheet label makes the quotient smooth. It does not define the target component map on the internal target seams, prove Hausdorffness, or construct compatible collars. The conclusion “ordinary smooth manifold, not a branched quotient” therefore assumes the point at issue.

### 4. The declared current space does not contain its iterated derivatives

The norm contains only bulk \(C^1\) densities and codimension-one face traces. A second material derivative of a moving polyhedral partition produces codimension-two corner terms; higher derivatives produce flag currents of every codimension. The proof mentions “compatible flag currents” but supplies neither coordinates nor norms for them. They are not elements of the displayed completion.

Thus the proposition can at most type one derivative. It cannot support the theorem's unspecified finite-order response or repeated resolvent/current words.

### 5. Refinement boundedness is asserted, not proved

The estimate \(4^n\varpi^n<1\) controls only cell count. Face multiplicities, trace norms under anisotropic affine pullback, endpoint derivatives, and repeated common refinements also enter. No uniform operator bound is given for the refinement maps, and the assertion that the orientation relations form a closed subspace is unsupported.

### 6. The response theorem is not a theorem at the stated level

The manuscript does not define the present-symbol coupling operator, the mixed-cylinder tensor norm, or the source/target spaces of the reduced resolvents when a Hadamard current is inserted. The final statement that the three terms cancel for a fixed physical observable is a change-of-variables tautology; it does not validate the separate infinite series used to represent them.

## Status of earlier objections

The natural-extension typing and the rejection of a bilateral spectral gap are repaired. The conditional nature of the valuation coefficient is also stated honestly. The physical Hamiltonian realization and all-order current response remain open.

## Minimum reconstruction

A viable benchmark paper would need to:

1. refine the section by both source and target labels;
2. construct an actual exact symplectic gluing with compatible collars;
3. prove the resulting quotient is a Hausdorff smooth symplectic manifold with boundary/corners;
4. define a graded current complex containing all flag strata; and
5. prove a bounded response theorem on that graded complex.

Even after such repairs, the manuscript would remain a benchmark rather than a top-four-journal contribution unless a genuinely new general theorem emerges.

## Recommendation

**Reject.** The coupled symbolic correction is sound, but the advertised smooth suspension and higher-order response calculus are not mathematically constructed.