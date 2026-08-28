# CM2 Gate 3/4 round 27 — arbitrary-n C24 path and component schema

Date: 2026-07-18  
Status: append-only strict leaf; no aggregate, root, or prior artifact modified

## Frozen conclusion

This leaf closes an exact **existence and bookkeeping interface** that was
still missing between four already frozen objects:

1. the full-measure two-dimensional regular collision-step key grammar;
2. the 24 positive-area physical C24 source cores;
3. the collision-SRB Kac return levels and uniform unweighted exponential
   return tail;
4. the round-26 limiting physical `R1/Q1` partition and finite `Q2` anchors.

For every fixed parameter `|s|<=1/400` and every finite `n`, it defines
full-dimensional candidate fibres for `R_n` and `Q_n`, proves that they cover
C24 modulo the singular/core-boundary collision-null set, and supplies a
canonical countable connected-component refinement schema.

The conclusion is deliberately nonconstructive at component level.  It does
**not** enumerate the nonempty path words or components and does not attach
numeric component masses, margins, unstable Jacobians, distortion, common
forward/reverse restriction IDs, or strong `q_n` payloads.  Thus this is not
a materialized raw arbitrary-`n` branch table and it does not certify Gates
3--5.

## Full-dimensional arbitrary-n candidate path join

The frozen regular collision-step alphabet has size

```text
|K| = 441280.
```

With 24 physical source-core tags, the depth-`n` candidate universe is

```text
c24-path:(source_core_id,n,k_1,...,k_n),
|candidate universe at depth n| = 24 * 441280^n.
```

Empty fibres are allowed.  This distinction is essential: the formula counts
candidate words, not certified nonempty physical branches.  The frozen
depth-one through depth-nine counts are replayed exactly, including
`10,590,720` source-tagged candidates at `n=1` and
`4,673,472,921,600` at `n=2`.

The upstream Gate-5 domain contract is now joined directly: every regular
collision step has exactly one frozen key owner, using the dominant-chart tie
order and one-sided trace/cemetery typing.  Hence every finite regular
collision orbit segment has exactly one frozen step-key word.
The complement is contained in the countable grazing/corner/homogeneity
singularity cemetery and therefore has collision-SRB mass zero.  Joining the
step words to the 24 source cores consequently gives C24 coverage modulo this
null set.  The carrier remains two-dimensional at fixed parameter; no
occurrence curve is substituted for physical area.

## Exact Rn/Qn levels and mass ledger

For the physical return clock

```text
tau_C_s^+(x) = inf{n>=1 : T_s^n(x) in C_s},
```

define

```text
Q_0 = C_s,
Q_n = C_s intersection intersection_{j=1}^n T_s^{-j}(C_s^c),
R_n = C_s intersection intersection_{j=1}^{n-1} T_s^{-j}(C_s^c)
      intersection T_s^{-n}(C_s),  n>=1.
```

Modulo the singular and core-face cemetery,

```text
Q_(n-1) = R_n disjoint_union Q_n,
C_s = (disjoint_union_{j=1}^N R_j) disjoint_union Q_N.
```

The Kac nonreturning mass is zero, hence

```text
C_s = disjoint_union_{n>=1} R_n   modulo collision-SRB null sets.
```

For a path word `k`, the symbolic physical loads are now typed as

```text
m_s,n,k     = mu_s(R_n intersection fibre(k)),
qmass_s,n,k = mu_s(Q_n intersection fibre(k)).
```

Their exact sum identities are certified.  In particular,

```text
sum_k m_s,n,k       = mu_s(R_n),
sum_k qmass_s,n,k   = mu_s(Q_n),
sum_n sum_k m_s,n,k = mu_s(C_s).
```

Using the frozen C24 open-hole result gives the uniform unweighted tail

```text
mu_s(Q_n)/mu_s(C_s)
  < (550000/147)
    * (111718729/111718750)^floor(n/N_open),
```

where the common `N_open>=1` is theorem-supplied and still not numerically
materialized.  No strong-`q` weighted tail is inferred from this identity.

## Canonical regular connected components

At fixed `s` and finite `n`, a regular path fibre is a finite intersection of
strict collision-owner, chart, homogeneity, core-avoidance, and terminal-core
inequalities along analytic billiard branches.  It is open relative to the
source-core interior.  Its finite-depth boundary is carried by grazing/corner
and homogeneity singularities, equal-root owner-change curves, chart seams,
and preimages of the 24 core faces; this is a countable union of piecewise
analytic collision-null curves.

Every nonempty open connected component contains a rational dyadic basis
element whose closure lies inside that component.  Fix once and for all a
bijective enumeration of these basis elements by the natural numbers and
take the least admissible index.  The natural-number order is a well-order,
so this minimum exists.  Therefore the components are at most countable and
admit the canonical existence label

```text
c24-component:(source_core_id,n,path_key,least_dyadic_basis_index).
```

The billiard map on each such component is a real-analytic local
diffeomorphism with a regular inverse.  Its full invariant collision-area
Jacobian is `1`; this is not converted into an unstable Jacobian or a
distortion bound.  No uniform joint-parameter component atlas is claimed.

## Round-26 constructive anchors

The schema is checked against the constructive facts already frozen:

- the limiting physical step-one `R1/Q1` partition modulo collision-null
  boundary is certified;
- the fair one-step unresolved tube is `O(2^(-d/3))`;
- 114,006 strict finite `Q2` inner atoms of mass
  `5257799/5120000000` exist;
- the remaining time-two outer mass is `106721/204800000`;
- the finite time-two anchor is not yet a complete `R2/Q2` partition.

The arbitrary-`n` schema does not erase or silently fill the unresolved
time-two components.

## Latest technique audit

The source of arXiv:2604.19671v2 was rechecked, including its standard-family
invariance and conditional exponential-mixing results.  Those results are
for a small boundary-position hole whose images can be foliated by long
standard pairs.  The paper explicitly says that the argument relies
significantly on hole geometry and that even a circular phase-space hole is
out of reach.  C24 is a parameter-uniform union of phase-space rectangles,
and the missing CM2 interface requires numeric branchwise strong payloads.
Consequently the paper remains a useful recovery blueprint but cannot be
substituted for the missing C24 admissibility, component enumeration, or
strong Lasota--Yorke proof.

Reference: <https://arxiv.org/abs/2604.19671v2>.

## Exact advancement and nonpromotion

Newly certified:

- arbitrary finite-depth C24 candidate-path coverage modulo singular null;
- the measurable `R_n/Q_n` level, telescope, and physical mass-sum schema;
- the already frozen uniform unweighted exponential `Q_n` mass tail in this
  path ledger;
- existence and canonical countable IDs for regular connected components.

Still not certified:

- exact nonempty path-key and component enumeration;
- numeric branchwise collision-SRB masses and owner/core margins;
- unstable Jacobian and distortion payloads;
- common forward/reverse strong restriction IDs;
- strong `q_n` payload and weighted excursion/cemetery tail;
- a finite complete raw arbitrary-`n` branch table;
- an induced strong Lasota--Yorke coefficient;
- Gates 3, 4, 5, or CM2.

The strict global status remains `CM2 NO-GO FOR CLAIM`.

## Frozen artifacts and replay

- `cm2_gate34_round27_arbitrary_n_path_schema_cert.py`
- `cm2_gate34_round27_arbitrary_n_path_schema_verifier.py`
- `cm2-gate34-round27-arbitrary-n-path-schema-manifest-2026-07-18.json`
- `cm2-gate34-round27-arbitrary-n-path-schema-manifest-2026-07-18.sha256`

```bash
.venv-neurips/bin/python \
  deliverables/cm2_gate34_round27_arbitrary_n_path_schema_verifier.py \
  --manifest deliverables/cm2-gate34-round27-arbitrary-n-path-schema-manifest-2026-07-18.json \
  --integrity-only

.venv-neurips/bin/python \
  deliverables/cm2_gate34_round27_arbitrary_n_path_schema_verifier.py \
  --manifest deliverables/cm2-gate34-round27-arbitrary-n-path-schema-manifest-2026-07-18.json \
  --replay

.venv-neurips/bin/python \
  deliverables/cm2_gate34_round27_arbitrary_n_path_schema_verifier.py \
  --manifest deliverables/cm2-gate34-round27-arbitrary-n-path-schema-manifest-2026-07-18.json \
  --self-test
```

Integrity, independent replay, and `75/75` hostile tests pass.  Default live
mode exits `2` because component enumeration and all strong gates remain open.
