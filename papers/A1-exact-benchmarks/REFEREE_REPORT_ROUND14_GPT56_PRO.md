# Independent Referee Report — Round 14

**Manuscript:** A1 — *Exact Benchmarks*  
**Reviewed branch:** `revision/round14-referee-positive-closure-11paper-2026-09-01`  
**Reviewed commit:** `dd9dbcb891076b7dbfe388bd8543d8342ba103c0`  
**Reviewed tree:** `c4492f8891e065201af70e68e6764ff5975f2137`  
**Controlling module:** `ROUND14_POSITIVE_CLOSURE.tex`  
**Registered module SHA-256:** `8f4d87768c9e8d31c237a72b719db51407a921b23401f14a9d17152bd79c1760`  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *JAMS*  
**Recommendation:** **Reject**

## Executive assessment

Round 14 makes two genuine repairs: it stops identifying the symbolic natural extension with a symplectic manifold, and it replaces the refinement-decaying seminorm from Round 13 by a geometric-mass construction. The coupled coding map is now the correct baker natural extension, and the mechanical work variable is at least placed in a canonical pair.

The new central theorem is nevertheless not correct. The exactness calculation used to glue the Hamiltonian channels contains an elementary one-form error; the purported regular section obtained by deleting the complete seam orbit is not a smooth two-dimensional section; and the flag-current norm is defined using parameter derivatives before a Banach bundle or derivative domain has been constructed. These are defects in the principal objects, not missing exposition.

## Decisive objections

### 1. The displayed primitive difference is wrong

On branch `i`, write `s=s_{i-1}` and `w=w_i`. The manuscript uses

\[
Q={q-s\over w},\qquad P=s+wp
\]

and the canonical one-form `p dq`. Direct calculation gives

\[
B_i^*(P\,dQ)-p\,dq
=(s+wp){dq\over w}-p\,dq
={s\over w}\,dq.
\]

Hence a primitive is

\[
G_i(q,p)={s\over w}(q-s)
\]

up to a constant. The manuscript instead writes

\[
G_i(q,p)={s\over w}(q-s)-sp,
\]

whose differential contains the spurious term `-s dp`. Therefore the asserted identity

\[
B_i^*(p\,dq)-p\,dq=dG_i
\]

is false under the manuscript's own coordinate convention.

This error is load bearing: the proof of exact face matching, the exact symplectic quotient, and the global primitive on the impact network all invoke this `G_i`.

### 2. The complete-seam-orbit complement is not the claimed smooth section

The paper defines

\[
S_a^\circ=(0,1)^2\setminus\mathcal S_a,
\]

where `S_a` contains every forward and backward iterate of all vertical and horizontal seams. For a full baker map these iterated boundaries form a countable, typically dense family. Their complement has full measure but is not an open two-dimensional manifold and is not an ordinary smooth Poincaré section.

If only the current seams are removed, one obtains open branch rectangles but some regular points later hit a seam. If the entire seam orbit is removed to make every iterate single valued, the resulting invariant set no longer has the local manifold structure asserted in the Hamiltonian-impact theorem. The manuscript cannot have both conclusions without introducing a graph-completed hybrid state space and proving its topology.

### 3. The channel quotient has not been shown to be a Hausdorff symplectic manifold

The outgoing face of channel `i` is the horizontal rectangle

\[
(0,1)\times I_i.
\]

It meets all four incoming vertical gates, with the next channel selected by the outgoing `q` coordinate. Thus the outgoing face must be subdivided along all target vertical seams before it is glued to the incoming channel faces. The proof merely says that regular faces are paired and that distinct gates remain separated. It does not define the quotient equivalence relation near the subdividing seams or provide compatible local charts.

Moreover, the open-gate quotient omits impact singularities but calls the resulting flow complete. Completeness on a nonclosed invariant full-measure subset is not automatic and is not proved.

### 4. The flag-current norm is circularly defined

The norm of `F_a^q` contains

\[
\sum_{j=0}^{q-k}\mathbf M(D_a^jT_F).
\]

But `D_a` is the material derivative that the proposition subsequently claims to construct as a bounded operator. At a fixed parameter `a`, an arbitrary finite current does not possess parameter derivatives. To make this meaningful one must first define a Banach bundle of `a`-dependent current jets, specify transport between fibers, and define the closed domains of every derivative.

As written, the space is defined using an operator that has not yet been defined, and the proposition then proves boundedness by appealing to membership in that same space. This is circular.

### 5. Material differentiation is not bounded on all finite-mass currents

Even after a jet-bundle repair, differentiation of a moving discontinuity sends a bulk measure to a face distribution. Differentiating an arbitrary finite face measure can produce derivatives that are not finite measures. The Reynolds formula is valid on a regular domain of sufficiently smooth densities; it does not give a bounded operator on the completion of all finite-mass currents merely because all codimensions have been listed.

The paper needs a precise anisotropic current domain, trace estimates, and a closability theorem. Componentwise completeness of finite measures does not supply these facts.

### 6. The all-order response formula is not established

The response proof is performed on finite cylinders and then passed to the completion by saying that refinement is an isometry. This does not address:

- the undefined parameter-jet norm above;
- uniform bounds for repeated material derivatives of seam velocities;
- compatibility of the future/past Poisson resolvents with the physical current completion; or
- convergence of mixed time-depth/flag insertions at arbitrary order.

The exact cancellation for a genuinely fixed physical observable is tautological because Lebesgue measure is fixed. It does not validate the proposed decomposition term by term.

### 7. Corrected scope and novelty

After removing the invalid exact-impact and all-order current claims, the sound material is an explicit Bernoulli baker coding, a canonical additive coordinate, and finite-order differentiation of moving rectangular partitions. This is useful benchmark material but not a contribution at the level of the four journals named above.

## Required reconstruction

A viable mathematical paper would have to:

1. correct the exact one-form calculation and rebuild the channel gluing;
2. choose an honest hybrid/impact section rather than call the complete seam-orbit complement a manifold;
3. define a parameterized current-jet bundle before using `D_a` in the norm;
4. prove closability and trace estimates on a regular current domain; and
5. sharply reduce the novelty claims.

## Recommendation

**Reject.** Round 14 repairs the symbolic topology, but the new exact Hamiltonian realization rests on a false primitive identity, and the all-order response space is circularly typed.