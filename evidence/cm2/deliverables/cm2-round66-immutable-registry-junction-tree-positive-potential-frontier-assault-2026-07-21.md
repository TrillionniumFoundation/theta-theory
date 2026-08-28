# CM2 Round 66 cross-gate assault: immutable registry gluing and positive potential

Date label: 2026-07-21

Strict verdict: **this append-only leaf certifies an exact standard-Borel
junction-tree gluing criterion and an exact obstruction to cyclic/pairwise
fragment assembly.  It does not construct the missing actual CM2 registry,
and it closes no gate.  CM2 remains `NO-GO_FOR_CLAIM`.**

## 1. Why the common registry is a mathematical hypothesis

Round 65 reduced the shortest route to one object carrying path/time/owner,
stable-plaque, material/face and sector/arrival records at once.  Having the
right marginal fragment in each gate is not yet such an object.  The records
must be coupled on the same immutable identifiers, and every overlap must
mean literal equality of the same physical coordinate rather than equality
in distribution after an unpinned relabelling.

Let `T=(A,E)` be a finite tree of fragment types.  Fragment `a` has a finite
key set `I_a`, standard-Borel coordinate spaces on those keys, and a
probability law `mu_a`.  Assume the running-intersection property:

```text
for every key k, {a : k in I_a} is a connected subtree of T.
```

For an edge `a--b`, put `S_ab=I_a intersection I_b`.  Then there is a global
law `Pi` on the union of all keys whose `I_a` marginal is `mu_a` for every
`a` if and only if

```text
(proj_Sab)# mu_a = (proj_Sab)# mu_b             for every edge a--b.
```

Necessity is immediate.  Sufficiency follows by rooting the tree,
disintegrating each child law over its separator, and successively attaching
the child-only coordinates by the corresponding regular conditional kernel.
Standard-Borel typing is what supplies those disintegrations.  The resulting
global coupling need not be unique.

This statement becomes a physical immutable join only when the separator
coordinates themselves are pinned physical IDs (or pinned Borel crosswalks
to such IDs).  Mere equality of anonymous marginal laws constructs at most
an abstract coupling; it does not prove same-orbit, same-collision,
same-plaque or same-material identity.

## 2. Sharp cyclic separator

Running intersection cannot be deleted.  Let `A,B,C` be bits and specify
three pair laws:

```text
mu_AB: uniform on (0,0),(1,1)       [A=B]
mu_BC: uniform on (0,0),(1,1)       [B=C]
mu_AC: uniform on (0,1),(1,0)       [A!=C]
```

Every one-bit marginal is the same uniform law, so every pair of fragments
passes its overlap-marginal test.  A global law would nevertheless force
`A=B=C` and `A!=C` almost surely, which is impossible.  Thus pairwise
compatibility of a cyclic collection does not certify a global registry.

The corresponding support-CSP replay has eight candidate atoms and accepts
zero.  In contrast, deleting any one of the three constraints leaves exactly
two atoms and a valid tree join.  This is a finite exact separator, not a
topological or numerical caveat.

## 3. Deterministic physical root versus abstract coupling

A sufficient physical interface stronger than the abstract theorem is a
pinned standard-Borel root `(Omega,nu)` with maps

```text
q_a: Omega -> product_(k in I_a) X_k,
```

such that `(q_a)#nu=mu_a` and the maps agree pointwise on every shared
immutable key.  Then `Pi=(q_a)_a#nu` is automatically supported on all
required equality graphs.  Conversely, a graph-supported global `Pi` can be
used as such a root.  Hence a physical common-root certificate is exactly a
graph-supported join certificate, not a list of same-law marginals.

For CM2 the minimum common record must cover, without changing
representative or gauge,

```text
path/time/owner/branch,
collision and stable-plaque/root IDs,
material/face/current-atlas IDs,
live versus one-shot-arrival status,
sector and positive-pair/Jordan labels.
```

The frozen Gate-1/3, Gate-2/4 and Gate-5 fragments do not provide a single
pinned root/crosswalk with exact separator marginals.  The actual immutable
registry therefore remains `NOT_CERTIFIED`.

## 4. Gluing is independent of the strong bound

Even after a lawful global `Pi` exists, Round 65's positive-path criterion
must be paid on that same root.  For typed nonnegative conditional charges
`W_j` and outer weight `w>1`, put

```text
H(omega)=sum_(j>=0) w^j P_(0:j)W_j(omega).
```

The all-time positive lift on `L1(nu)` is bounded exactly when
`H in L-infinity(nu)`, with operator norm `||H||_infinity`.  This condition
is neither created nor weakened by junction-tree gluing.

Indeed, take the already perfectly glued one-key root `Omega={1,2,...}` with

```text
nu{n}=3*4^(-n),       H(n)=2^n.
```

Every fragment can be the identity marginal on this same immutable key and
the global law is trivial, while `integral H dnu=3` is finite and
`H` is unbounded.  Unit `L1` atoms have lift norm `2^n`.  Thus

```text
exact common registry + finite actual positive moment
does not imply strong assembly.
```

A lawful sufficient route is therefore two-line and joint:

1. certify a graph-supported immutable junction-tree join (or deterministic
   common root); and
2. on that very root prove `sum_j w^j C_j<infinity` with the pointwise rows
   `P_(0:j)W_j<=C_j` almost everywhere.

Neither line can be replaced by averages taken on separately chosen laws.

## 5. Current technology boundary checked on 2026-07-21

Four official arXiv records were checked directly.

- `arXiv:2502.07765v2` proves a CLT with error bounds for sequential systems
  via complex projective cones and includes sequential dispersing billiards.
  It supplies a statistical memory-loss/CLT interface, not a parameter
  derivative, moving-boundary current/Piola remainder, or an all-depth
  collision-SRB stable trivialisation on CM2's immutable registry.
- `arXiv:2504.16532v3` proves optimal linear response for transitive
  `C^5` Anosov diffeomorphisms of the two-torus.  Its family assumes
  `T_delta=T_0+delta dot(T)+o_C5(delta)` and works on smooth
  Gouëzel--Liverani spaces.  The smooth torus model has no billiard collision
  singularity or moving boundary, so its operator derivative cannot be
  imported as CM2's strong Piola/current row.
- `arXiv:2402.02496v2` gives asymptotic local product structure for invariant
  measures of `C^(1+gamma)` diffeomorphisms of closed Riemannian manifolds.
  This is a closed smooth-manifold law and does not instantiate the actual
  singular collision atlas, stable tree, marker zero-defect or strong
  recipient.
- `arXiv:2504.17879v1` studies countable-state, uniformly lazy Markov chains
  killed by confining potentials under the direct-step property.  Those
  hypotheses and that countable-state process are not the frozen CM2 owner
  lineage or seven-sector kernel.

No external theorem is promoted.  Each candidate is retained only as a
precise technology boundary.

## 6. Strict frontier

```text
standard-Borel junction-tree gluing iff:            CERTIFIED_EXACT
cyclic parity separator:                            CERTIFIED_EXACT
graph-supported deterministic-root equivalence:     CERTIFIED_EXACT
glued finite-moment versus L-infinity separator:     CERTIFIED_EXACT
actual CM2 immutable global registry:                NOT_CERTIFIED
actual all-charge positive path potential in L-inf:  NOT_CERTIFIED

Gate 1: NOT_CERTIFIED
Gate 2: NOT_CERTIFIED; official fields 0/17
Gate 3: NOT_CERTIFIED
Gate 4: NOT_CERTIFIED; landing join 1/7
Gate 5: NOT_CERTIFIED; maturity 10/18, blocks 0
complete composite gates: 0/5
CM2: NO-GO_FOR_CLAIM
```

The shortest remaining common route is no longer “join the reports”.  It is
to emit one graph-supported actual root registry and certify both its exact
fragment marginals and its `L-infinity` all-time positive potential.
