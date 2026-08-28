# CM2 Round 58 three-leaf independent core-frontier audit

Date: 2026-07-20  
Audit verdict: **PASS — no claimed-scope blocker and no cross-leaf status
contradiction.  All five composite gates remain open and CM2 remains
`NO-GO_FOR_CLAIM`.**

This append-only audit freezes all five artifacts (certificate, verifier,
manifest, report and SHA ledger) from each Round-58 core leaf:

```text
Gate 4 manifest:   d335ea6b9bfdc68c13fa0c44f5f2893af7399546f5951d0cfc156be8b5236ffb
Gate 5 manifest:   27c5d2e9a6ac9ed8eeb3d42dc96aa1c0a8faa8e50e006811efea22b45c86b859
Gate 1/2/3 manifest:
                   42a035e38687acb4ae1a3ce43a1459c49ba08a1406083c811f919823ecc8d526
```

In total, `15/15` frozen artifacts and all `12/12` entries in their three SHA
ledgers were independently rehashed.  No audited file was edited.

## 1. Gate 4: maximal-component minimum and its exact scope

Fix one

```text
(y, physical landing chart, immutable physical restriction ID).
```

Every exact positive standard-pair carrier has a strictly positive regular
density on a connected interval.  It therefore cannot cross a true
positive-length zero-law gap or an omitted singular/cemetery puncture and
must lie in one maximal positive component `C`.  Since its length is at most
`ell(C)`, every exact representation of the mass on `C` pays

```text
sum_(W subset C) p_W/ell(W) >= kappa_y(C)/ell(C).
```

Restricting the inherited positive density once to each maximal component
attains equality.  The audit independently replayed three nontrivial exact
rational cut ledgers and recovered the same inequality.  Hence

```text
J_land,min(y)=sum_C kappa_y(C)/ell(C)
```

is the exact minimum within the frozen registry, and the same-time same-ID
physical landing is proper iff

```text
J_land,min(y)<C_p h(y)
```

on almost every positive fibre.  Allowing countably many positive candidate
families does not weaken the iff: their normalized boundary ratios form a
mass-weighted average, and a countable sum of positive strict deficits is
still positive.

The Borel and zero-fibre details are correctly typed.  Round 57's
least-rational component owners give Borel endpoints, masses and lengths;
the monotone component sum is Borel.  When `h=0`, the component registry is
empty, `J_land,min=z_land=0`, and no normalization is performed.

The theorem does **not** exhaust cross-`y` or cross-chart physical Rokhlin
redistribution.  Such a construction would require the new Gate-2 physical
stable-holonomy interface.  Thus the main leaf's phrase “exhausted” is
correct only with its explicit fixed-`(y,chart,ID)` qualifier.

Round 57's finite physical landing representation implies
`J_land,min,total<infinity`.  With the strict definition

```text
D_land=0,                                      z_land<C_p,
D_land=min{d>=1:2^-d z_land<C_p/2},            z_land>=C_p,
```

minimality gives `2^D_land<=4 z_land/C_p` on the defect and therefore

```text
integral h 2^D_land <= H+(4/C_p)J_land,min,total < infinity.
```

The strict boundary was replayed: `z_land=C_p` gives `D_land=2`, not one.
`D_land` is unshifted physical landing geometry; `D_cap` is stopped
two-view/reference geometry.  They cannot be interchanged or appended to
the original first-return time.

The finite separator is exact.  For `N=floor(C_p)+1`, `N` retained intervals
of total mass `999/1000` separated by positive gaps have physical normalized
minimum `N/(999/1000)>C_p`, while a stopped reference reassembler has
`J_cap=2`, normalized value `2/(999/1000)<C_p`, and `D_cap=0`.  It is a
logical standard-family nonimplication model, not a billiard-realization
claim.  Reinducing the identity model repeats the same improper landing, so
finite `Z` and once coverage do not force properness at any finite
occurrence.

Gate-4 audit result:

```text
maximal-component minimum / properness iff: PASS
J_land,min,total and full dyadic D_land moment: PASS
fixed-registry scope, Borel and zero-fibre policy: PASS
D_land versus D_cap typing and separator: PASS
physical proper same-ID first-return kernel: NOT_CERTIFIED
Gate 4: NOT_CERTIFIED
```

## 2. Gate 5: owner ledger, density typing, H/J and positive transport

Round 50/54 supplies an actual finite Borel owner/root law restricted to
`A_col`; the Borel selector `K` and deterministic integer clock `r_K` thus
define a genuine extended-valued same-law ledger.  For
`a_k=w_Z^r_k`, pointwise telescoping and Tonelli give

```text
sum_k a_k m_k
=a_0 nu(A_col)+sum_(j>=0)(a_(j+1)-a_j)nu{K>j}.
```

The audit replayed the identity over a six-level nonuniform rational law.
This proves a well-typed necessary-and-sufficient tail series, not its
finiteness.  `A_col` coverage and restricted-moment finiteness are separate
axes; neither follows from the other.

The root/density distinction is correct.  The frozen physical trace selects
one root atom per parent and integrates those atoms over the outer parent
law.  It is not an along-collar absolutely continuous conditional.  The
Round-54 artificial uniform extension has density `ell^-1`, whose aggregate
is exactly the missing raw `Z_col`.  Treating it as a free physical density
would be circular.

The positive recovery carrier minimally needs the joint marks

```text
K = clearance level,
H = compatible 9148-block horizon,
J = exact labelled operator/domain join.
```

The same-`K` two-completion separator is exact.  The audit checked directly
that the frozen constants imply `gamma<1/2`, hence `beta<1` and
`r_(2n)<=2n+1`, and also `w_Z^2/2<1`.  Therefore the aligned completion has a
finite recovered moment, while the short/misaligned completion pays
`sum_n 2^n=infinity`.  No theorem reading only the frozen clearance marginal
can infer the missing hybrid suffix.

For every nonnegative Borel charge and every coupling,

```text
integral [a(y+)+a(y-)] dpi
=integral a dmu+ + integral a dmu-.
```

An independent non-diagonal `3x3` rational coupling replay confirmed the
identity.  The cost is coupling-independent.  Consequently signed OT and
signed-current cancellation cannot create a positive F10 or strong cemetery
moment.  The equal-Jordan-marginal separator has signed OT zero but positive
clearance terms `2^(alpha_opt n^2-n)`, which diverge.

Gate-5 audit result:

```text
same-owner Borel extended ledger / Abel identity: PASS
same-owner ledger finite: NOT_CERTIFIED
root atom versus collar density typing: PASS
physical H/J joint law and same-operator join: NOT_CERTIFIED
signed OT => positive F10/strong cemetery: FALSE_BY_SEPARATOR
Gate 5 maturity / complete blocks: 10/18 / 0
Gate 5: NOT_CERTIFIED
```

## 3. Gates 1/2/3 and the cross-gate landing join

The Gate-1 Dini theorem is a valid conditional Cauchy criterion: summable
common weighted-projective increments telescope to a uniform Holder tail.
The audit replayed `C_n=1-2^-n` exactly.  The `10^-29` twisting radius is
valid only in the same physical QNL fibre and normalized eigenbasis.  The
physical all-plaque increment rows and combined-gauge loop enclosure remain
absent.

Gate 2 correctly measures projected singularity shadows, not collision
area.  If `Leb(B_j)<=b_j`, `sum b_j<|I|`, and surviving graph transforms have
common compactness/contraction bounds, a positive all-depth base follows by
the union bound and graph-transform compactness.  A zero-area transverse
line can project to the full fibre base, so area nullity does not provide
this input.  The physical projected-shadow rows remain zero.

The Gate-2 to Gate-4 join is consistent with the Gate-4 minimum theorem.
Pushing to a long quotient interval produces only a latent reference lift.
Same-time redistribution on the same physical graph is possible only after
installing all seven listed physical product-rectangle, holonomy,
fragmentation, unstable-conditional, boundary-charge, branch-inverse and
strong-assembly fields.  It is therefore `CONDITIONAL_JOIN_ONLY`, not a
current landing-kernel promotion.

The Gate-3 CAD recurrence is a legitimate computable majorant **for a branch
formula separately proved to fit the declared encoding envelope**.  The
audit independently recomputed the first three projection/lifting rows for
depths one, two and three.  The physical circular-pilot formula has not been
machine-enumerated into that envelope, so no unconditional physical
component bound follows.  The `p_d=2^-d`, `G(d)=d^d` example proves only that
an exponential clock moment does not integrate an arbitrary
superexponential majorant; it asserts no physical component lower bound.
The determinant-one diagonal replay correctly separates area control from a
directional Piola bound.

Gate-1/2/3 audit result:

```text
weighted-projective Dini and projected-shadow bridges: CONDITIONAL PASS
same-time Gate-2 to Gate-4 physical redistribution: CONDITIONAL_JOIN_ONLY
CAD recurrence: CERTIFIED_FOR_DECLARED_ENCODING_BUDGET_ONLY
physical CAD budget / strong R_s,Q_s / Piola / MT_DQ: NOT_CERTIFIED
Gates 1/2/3: NOT_CERTIFIED
```

## 4. Cross-leaf consistency and strict verdict

No state collision was found:

- Gate 4's fixed-registry iff leaves exactly the cross-registry Gate-2 route
  conditional;
- physical `D_land` is not the stopped/reference `D_cap`;
- Gate 5's signed objects remain signed and do not pay positive tower debt;
- Gate 3's CAD claim is explicitly conditional on a declared formula budget.

The strict aggregate state is therefore:

```text
Gate 1: NOT_CERTIFIED
Gate 2: NOT_CERTIFIED
Gate 3: NOT_CERTIFIED
Gate 4: NOT_CERTIFIED
Gate 5: NOT_CERTIFIED (10/18, complete blocks 0)
complete composite gates: 0/5
CM2: NO-GO_FOR_CLAIM
```

## 5. Executable acceptance

The three audited leaves were re-run before freezing this package:

```text
leaf syntax:                       6/6 PASS
leaf dependency pins:             24/24 PASS
leaf hostile mutations:           246/246 rejected (82+97+67)
leaf replay / reemit:              3/3 / 3/3 PASS
leaf SHA ledger entries:          12/12 PASS
leaf default entries:              6/6 exit exactly 2
```

This independent audit package adds:

```text
syntax:                             2/2 PASS
frozen artifact pins:             15/15 PASS
parsed frozen SHA-ledger entries: 12/12 PASS
independent semantic replay:       PASS
hostile semantic mutations:       96/96 rejected
deterministic manifest reemit:     byte-identical PASS
artifact SHA ledger:               4/4 PASS
default cert/verifier:              2/2 exit exactly 2
```

The audit SHA ledger uses workspace-root-relative `deliverables/...` paths
only and is intended to be checked from the workspace root.

Artifacts:

- `cm2_round58_independent_core_frontier_audit_cert.py`
- `cm2_round58_independent_core_frontier_audit_verifier.py`
- `cm2-round58-independent-core-frontier-audit-manifest-2026-07-20.json`
- `cm2-round58-independent-core-frontier-audit-2026-07-20.md`
- `cm2-round58-independent-core-frontier-audit-manifest-2026-07-20.sha256`
