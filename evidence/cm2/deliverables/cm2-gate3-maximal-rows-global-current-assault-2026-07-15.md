# CM2 Gate 3 maximal-row and global-current assault

Date: 2026-07-15  
Verdict: **maximal connected event rows, the global finite-Borel event current, and global signed scalar coarea matching are certified; full transfer difference-quotient convergence and CM2 norm typing remain open**

## 1. What this pass closes

The sixth assault proved that the active label atlas has zero remaining
two-dimensional unresolved parameter area.  It did not glue the rectangular
and analytic pieces into maximal rows.  This pass performs that gluing in the
global source-normal circle, so the four dominant-coordinate charts and all
diagonal seam duplicates are quotiented before connectivity is computed.

The exact output is:

```text
128 parameter-active global signed sheets,
328 exhaustive candidate transition curves,
88 state-changing physical boundaries,
64 maximal connected physical event rows,
64 unique complete hit/miss/polarity labels,
16 exact Jx/Jy four-row orbits.
```

Every maximal row carries one positive coarea law, one signed hit-minus-miss
current and one exact `Jx` partner.  Their finite sum is a signed Borel measure
that pairs with every bounded Borel test.

## 2. Exhaustive global curve arrangement

For every active global sheet `(source,target,epsilon)`, the only possible
label-changing curves are:

| analytic family | candidates |
|---|---:|
| source grazing `cp=0` | 256 |
| forward horizontal tangent `u_y=0` | 24 |
| active earlier first-visibility switch | 16 |
| active later miss-owner switch | 32 |
| **total** | **328** |

The first two families are evaluated directly from the exact two-circle
geometry.  The latter two are the cross-colour part of the exhaustive 82,048
target-target descriptor registry closed in the sixth assault.

There are 320 same-sheet candidate pairs.  Arb proves 304 pairs strictly
separated on the whole parameter interval.  The remaining 16 are separated
after one bisection of `s in [-1/400,1/400]`.  Thus:

```text
all same-sheet candidate curves are pairwise disjoint,
maximum separation depth = 1,
strict separation leaves = 336,
cyclic curve order is constant on the full parameter window.
```

A certified strict witness in every open cyclic band determines its complete
state.  Adjacent equal states are merged.  Exactly 88 candidates change the
physical state:

| physical boundary | count | side pattern |
|---|---:|---|
| source grazing | 32 | empty / physical |
| first visibility | 16 | empty / physical |
| miss owner | 32 | physical / physical with different miss targets |
| parameter polarity | 8 | physical / physical with opposite polarity |

The endpoint-incidence identity is exact:

\[
32+16+2(32+8)=128=2\cdot64.
\]

Hence every physical row has exactly two boundary incidences.  Because the
transition universe is exhaustive, all candidate curves are disjoint, and
every retained boundary has distinct strict side states, the 64 connected
open bands are maximal.

The distribution of maximal rows among the 128 active sheets is:

```text
104 sheets carry 0 rows,
8 sheets carry 1 row,
4 sheets each carry 2, 3, 4 or 5 rows.
```

The weighted total is `64`.  No chart identifier remains in the global row
label, and the exact symmetry audit gives 16 four-row `Jx/Jy` orbits.

## 3. Global finite-Borel coarea current

At the reference table `s=0`, use the source-normal angle `theta` on a maximal
row.  Up to the fixed collision-flux normalization `Z_N^{-1}`, the positive
coefficient law is

\[
 dm_e
 =R_{\rm source}\,c_p
   \left|\eta\epsilon\frac{c_pu_y}{\ell_T}\right|d\theta
 =R_{\rm source}\frac{c_p^2|u_y|}{\ell_T}\,d\theta.
\]

The signed event current is

\[
 J_e(\Phi)=\sigma_e\int_{A_e}
 \{\Phi(z_T(\theta))-\Phi(y_M(\theta))\}\,dm_e(\theta).
\]

Here `z_T` is the target grazing trace and `y_M` is the first strict
non-grazing miss collision.  The same `(+1,-1)` mark is retained on every
occurrence.

### 3.1 Exact finite-mass envelope

For all 64 active source-target pairs, exact affine-centre arithmetic gives

\[
 |C(s)|^2\le \frac{1362001}{160000}<36.
\]

The already certified circle-separation margin is

\[
 |C|^2-(R_S+R_T)^2\ge \frac{36337}{160000},
 \qquad R_S+R_T=\frac{13}{25}.
\]

Using `|C|<6` and `R_T>=4/25` gives

\[
 \ell_T^2
 \ge \frac{36337}{3260000}
 >\frac1{100},
 \qquad \ell_T>\frac1{10}.
\]

Consequently the unnormalised density satisfies

\[
 R_S\frac{c_p^2|u_y|}{\ell_T}
 \le \frac{18}{5}.
\]

With `2*pi<7`, one row has positive mass at most `126/5`, all 64 laws have
total mass at most `8064/5`, and the global hit-minus-miss current has

\[
 \|J\|_{TV}\le \frac{16128}{5}Z_N^{-1}.
\]

Thus `J` is a finite signed Borel measure and

\[
 |J(\Phi)|\le\frac{16128}{5}Z_N^{-1}\|\Phi\|_\infty
\]

for every bounded Borel test.

### 3.2 No hidden endpoint atoms

- Source-grazing endpoints have zero density because `cp=0`.
- Polarity endpoints have zero density because `u_y=0`.
- First-visibility and miss-switch endpoints are isolated points of the
  one-dimensional base and have zero absolutely continuous base mass.

Therefore the assembled order-zero current has no additional endpoint atoms.

## 4. Exact global scalar pairing

The 64 maximal rows form 32 exact `Jx` pairs.  Under `Jx`,

```text
s -> -s, so the reference s=0 is fixed;
(n_x,n_y) -> (-n_x,n_y);
(u_x,u_y) -> (-u_x,u_y);
epsilon -> -epsilon;
cp, ell_T, |u_y|, R_source and dtheta are invariant.
```

Hence `(Jx)_*m_e=m_{Jx(e)}` exactly, while parameter-coarea polarity reverses.
The complete maximal-row scalar coefficient sum is therefore zero:

\[
 \sum_e\sigma_e m_e(1)=0.
\]

The event current itself also annihilates the constant test rowwise because
its mark is `(+1,-1)`.  Neither statement says that arbitrary reflection-odd
tests cancel.

## 5. Gate-4/5 structural consequence

The universal same-occurrence theorem can now be instantiated on the true
maximal partition rather than on rectangular subrows.  The global ledger has:

```text
64 maximal physical occurrences,
64 common positive laws m_e,
64 pre-recovery expressions q_e=max(C_fw(e),C_rev(e),2)m_e,
128 singular Kac coordinates,
64 shared (+1,-1) coordinate pairs,
32 exact Jx scalar pairs.
```

The finite-Borel endpoint adjoint, Kac tower, prefix/suffix pairing and
four-term centered algebra therefore apply to all 64 maximal rows.  Counting
one charge per singular coordinate would incorrectly charge 128 times and is
explicitly rejected.

This is still a symbolic pre-recovery `q` ledger.  The global Borel TV bound
`16128/5` is not a forward standard-family cost `C_fw`, a reverse flux cost
`C_rev`, or a stopped-parent recovery estimate.

## 6. Latest-theory audit

The 2026 paper *Linear response for Sinai billiards with small holes*
(`arXiv:2604.19671v2`) proves differentiability for a shrinking boundary hole
by establishing conditional invariance and exponential relaxation of suitable
standard families.  It is the closest current result found in the audit, but
it does not directly close CM2:

- its perturbation is a shrinking hole, not a moving-scatterer event atlas;
- its source geometry is chosen so the image of the hole can be foliated by
  sufficiently long standard pairs;
- it does not provide the rowwise bidirectional same-occurrence recovery or
  the frozen `C_fw,C_rev` required here;
- it explicitly notes that currently available Banach spaces for general
  piecewise hyperbolic systems do not contain standard pairs.

The result strongly supports the controlled interval/standard-family route,
but it is not an honest drop-in theorem for the missing CM2 norm layer.  The
2026 contracting-fibre response theorem (`arXiv:2602.02317v2`) and the 2025
cusp theorem (`arXiv:2505.17462v1`) likewise require structures absent from
this billiard instance.

## 7. Exact remaining boundary

Certified in this pass:

1. the maximal chart-quotiented connected event-row registry;
2. one exact hit/miss/polarity label on every maximal row;
3. one positive physical coarea law and signed Borel current per row;
4. a global finite TV envelope and arbitrary bounded-Borel test pairing;
5. exact `Jx` positive-law pairing and global signed scalar matching;
6. the all-maximal-row symbolic single-charge and finite-Borel Kac ledger.

Still not certified:

1. convergence of the full transfer difference quotient, including the
   smooth fixed-core derivative and boundary tightness;
2. dynamic-`C^1` test pullback and any CM2 current norm;
3. a homogeneity-cut growth ledger and numeric `C_fw,C_rev` on all rows;
4. controlled interval/cylinder stopped-parent recovery under one frozen `q`;
5. physical prefix/suffix distortion sums and the three CM2 norm lifts.

Thus Gate 3, Gate 4, Gate 5 and unconditional CM2 remain open.

## 8. Reproduction

```bash
PYTHONPATH=deliverables /tmp/cm2-flint-venv/bin/python \
  deliverables/cm2_gate3_maximal_global_row_registry_verifier.py \
  --replay --integrity-only

PYTHONPATH=deliverables /tmp/cm2-flint-venv/bin/python \
  deliverables/cm2_gate3_global_borel_current_assembly_verifier.py \
  --replay --integrity-only

PYTHONPATH=deliverables /tmp/cm2-flint-venv/bin/python \
  deliverables/cm2_gate45_maximal_row_single_charge_ledger_verifier.py \
  --replay --integrity-only
```

Each verifier's live default mode deliberately exits `2` while full transfer
DQ convergence, stopped recovery and CM2 norm lifts remain open.
