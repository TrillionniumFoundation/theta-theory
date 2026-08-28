# CM2 Gate 5: actual physical phase-graph assault

Date: 2026-07-15  
Model: centred rational two-disk pilot  
Sections: `M=G sqcup C_clean`, `M*=M sqcup W`, `N=G sqcup W`  
Verdict: **the actual component phase graphs are strongly connected with
weighted cycle gcd one; the complete return-word/operator matrix and Gate 5
remain `NOT_CERTIFIED`**

## 1. What was audited

The bounded-depth statement `K_N<=9` was not used as an aperiodicity
argument.  Instead this audit replays physical first-hit branches in the
declared billiard and assigns a weight only after counting the intervening
common-refinement returns.

Two related graphs are distinguished:

1. the exact height-two block-support graph of
   `M*=M sqcup W`, corresponding to the block matrix
   `[[A,B],[C,0]]`;
2. the solid-component return graph on `N=G sqcup W`, with edge weight equal
   to the number of `M*` steps before the next solid collision.

The second object is presently a certified physical **spanning subgraph**,
not the missing complete return-word partition.

This graph audit is also rebound to the corrected Gate-3 owner frontier.  The
old 320 apparent endpoint descriptors and 16 apparent transition vertices
have been retracted by the missing forward-time check; the corrected count is
zero physical transition vertices and four nonphysical `tau=3` collars.  None
of those raw descriptors is used as a phase edge below.  Every displayed edge
instead has an independent physical first-hit witness.

## 2. Exact physical witnesses

### 2.1 A direct gray-to-gray branch

Work in `[-1/2,1/2]^2`, with gray centres at the corners.  From the lower-left
gray disk use the rational outward unit direction

```text
u=(99/101,20/101).
```

For radius `R_G=9/25`, the source point is exactly

```text
q=(-743/5050,-433/1010).
```

Against the lower-right gray target, the ray-circle quadratic has

```text
linear       = -1566/2525,
offset       = 743/2525,
discriminant = 576281/6375625 > 0,
arrival cosine > 3/4.
```

The selected near root is strictly forward.  It occurs before the closest
point

```text
(9401/20402,-6241/20402),
```

which lies in `x<1/2`, `y<-3/10`.  Hence the entire flight stays in the open
square, crosses no transparent wall, and remains vertically farther than
`3/10>R_W` from the central white row.  Independently, throughout
`|s|<=1/400`, its supporting line has white clearance

```text
789/2020 - 4/25 > 0.
```

All other gray/white rows are excluded by the same open flight rectangle.
Thus this is a strict positive-open physical branch:

```text
M -> M  through A,                 weight 1 in M*,
G -> G  on N with no M* event,     return weight 1.
```

### 2.2 The wall--white--wall block branch

At the centre of the explicit cylinder use

```text
q=(-1/2,0),  u=(1,0),  |s|<=1/400.
```

The first white flight and its time reverse both lie in

```text
[27/80,137/400] subset (1/4,1/2).
```

The ray stays exactly `1/2` from every gray corner centre, giving gray
clearance `7/50`.  This is the physical positive-width `C/B` pair

```text
M -> W,   W -> M,
```

each of height one in `M*`.  The independent fixed-section impact certificate
replays the stronger uniform cylinder bounds
`|n.u|>99/100` and `n.e_1<-49/50`.

### 2.3 The solid gray--white--gray tube

The exact diagonal centre distance satisfies

```text
d^2=1/2,
1/2-(R_G+R_W)^2=287/1250>0.
```

The companion 400-bit Arb certificate covers a positive tube and proves the
physical word

```text
G(0,0) -> W(0,0) -> G(0,0),
```

with incidence, discriminant and unintended-obstacle margins and zero
transparent-wall crossings.  Therefore the two solid component edges are

```text
G -> W,   W -> G,
```

both with common-refinement return weight one.

The independent 400-bit connector certificate was also replayed.  Its
14-collision word contains consecutive gray collisions, has clearance
`>1/5`, incidence `>3/5`, and zero transparent-wall crossings, independently
confirming the `G->G` solid self-loop.

## 3. The two actual graphs

The height-two support graph is exactly

```text
states: M,W
edges : M->M (A,1), M->W (C,1), W->M (B,1).
```

The certified standard-`N` physical spanning graph is

```text
states: G,W
edges : G->G (clean,1), G->W (QNL,1), W->G (reverse QNL,1).
```

Both are strongly connected.  Each contains the physical cycles

```text
odd  cycle: M->M or G->G,       total weight 1,
even cycle: M->W->M or G->W->G, total weight 2.
```

The exact weighted-graph checker therefore returns

```text
cycle gcd = gcd(1,2) = 1.
```

For the standard-`N` graph this conclusion is stable under adding every
still-unregistered physical return word: the displayed subgraph already
spans both states and is strongly connected, while the full cycle-weight gcd
must divide the weight-one self-loop.  Thus the actual pilot is not subject
to the constant-roof-two phase obstruction at the component level.

## 4. What this closes—and what it does not

This closes the previously open **finite combinatorial phase-period layer**:

```text
ACTUAL PHYSICAL SPANNING GRAPH: CERTIFIED
STRONG CONNECTIVITY: CERTIFIED
EXPLICIT ODD/EVEN CYCLES: CERTIFIED
COMPONENT CYCLE GCD ONE: CERTIFIED
```

It does not turn the graph into the operator identity required by the
fixed-to-full Wiener theorem.  The present files still lack:

1. the complete Borel partition into every standard-`N` return word;
2. source/target lift, homogeneity subbranch and exact weight on every cell;
3. the immutable operator block associated with every word;
4. global return-boundary DQ and occurrence/source matching;
5. an operator proof that `D(z)` has no unit-circle kernel after all blocks
   are assembled;
6. the singular source/test and CM2 norm intertwiners.

A component graph with gcd one is a necessary combinatorial witness, not a
substitute for those operator and norm fields.  In the currently preferred
`direct_standard_N` route no separate phase tower is used at all; its target
standard-`N` spectral layer was already certified.  The new graph is relevant
to the optional fixed-to-full common-refinement route and removes only its
period-two combinatorial obstruction.

## 5. Reproduction and verdict

All physical predecessor certificates were replayed with the pinned
Flint/Arb environment.  The new executable uses exact rational arithmetic and
the existing fail-closed weighted-graph checker.

```text
HEIGHT_TWO_MSTAR_ACTUAL_SUPPORT_GRAPH: CERTIFIED
STANDARD_N_ACTUAL_PHYSICAL_SPANNING_GRAPH: CERTIFIED
PHASE_GRAPH_STRONG_CONNECTIVITY: CERTIFIED
PHYSICAL_WEIGHT_ONE_AND_WEIGHT_TWO_CYCLES: CERTIFIED
COMPONENT_WEIGHTED_CYCLE_GCD_ONE: CERTIFIED

COMPLETE_STANDARD_N_RETURN_WORD_MANIFEST: NOT_CERTIFIED
OPERATOR_WIENER_APERIODICITY_FOR_FIXED_TO_FULL_ROUTE: NOT_CERTIFIED
PHASE_TEST_NORM_LIFT: NOT_CERTIFIED
GATE 5: NOT_CERTIFIED
```
