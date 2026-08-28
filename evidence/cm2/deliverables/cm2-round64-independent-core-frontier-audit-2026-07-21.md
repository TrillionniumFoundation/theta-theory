# CM2 Round 64 — independent core-frontier audit

Date: 2026-07-21

Verdict: **PASS; no frozen leaf correction is required.  Gate
1/2/3/4/5 remain NOT_CERTIFIED, Gate 2 remains 0/17, Gate 4's landing join
remains 1/7 with fields 1, 4 and 7 partial, Gate-5 maturity remains 10/18
with zero complete blocks, complete composite gates remain 0/5, and CM2
remains NO-GO_FOR_CLAIM.**

## 1. Independence and frozen scope

All five Round-64 leaf manifests were frozen before this audit read them:

1. Gate 1/3 one-cross-term and dyadic-clock primary leaf;
2. Gate 1/3 resonant-tail and BL-transport supplementary leaf;
3. Gate 2/4 weighted-tree and actual-join primary leaf;
4. Gate 2/4 Jacobian/tag-lift supplementary leaf;
5. Gate 5 lineage-kernel/flux-bridge leaf.

The audit authored none of those leaves and modified none of them.  It pins
their five manifest roots, five SHA ledgers, the shared Round-64 helper and
the complete Round-63 recursive root.  The five leaf SHA ledgers replay
4+5+4+5+5=23 artifact rows exactly.

## 2. Gate 1/3 audit

The primary Gate-1 algebra was recomputed:

    D_y D_x^(-1)
      =[[1+v_y du, dv-v_y du v_x],
        [du,       1-du v_x]].

The two frozen one-sided Green theorems pay every old entry; the only new
combined-gauge quantity is

    T_n=R_n^(-1)v_y(u_y-u_x)v_x.

The four exact regimes replay: q=1/2 decays, q=1 has both a nonzero constant
and an alternating nonlimit, and q=2 diverges.  Thus q<1 is sufficient for
automatic decay but not necessary for class-H convergence.

The supplementary leaf correctly records the related logical boundary:
zero renormalized tails can pass Hölder regularity but cannot create
twisting from a zero canonical loop.  Its critical loop

    (I-E_21)(I+E_12)=[[1,1],[-1,0]]

has determinant one and both axis wedges -1.  The two leaves are compatible:
an actual nonzero uniformly Hölder limit and the selected immutable twisting
token remain missing.

For Gate 3, the exact safe-clock closed form was replayed over M=0,...,500:

    Dbar(M)=0 for M<=310,       Dbar(M)=M-309 for M>=311.

The primary leaf correctly removes any false factor proportional to the
1392/696 collision-time span from endpoint TV, compressing the debt to one
dyadic level-trace ledger.  Its six separators show that weak TV, base F13
and weak cemetery do not bound that ledger.  The supplementary BL estimate
is also correct: endpoint transport may be summable while raw endpoint TV
diverges.  BL transport does not pay the physical strong dyadic trace,
cemetery or Piola rows.

## 3. Gate 2/4 audit

The weighted-tree replay has

    delta_T=3/20,       P=19/200,

and satisfies P<=delta_T<=2P.  Source and landing values agree under the
commuting tree.  The tree-edge lower and upper bounds, root-path distortion
budget, 5/5 actual fragment join and 0/7 physical stable-tree
materialization were independently checked.

The supplementary three-plaque replay has delta=6/5 and P=3/4, also inside
the sharp sandwich.  Its density/RN/arclength substitution is algebraically
equivalent to Round 63's m-squared budget.  Its deterministic tag model has
one-vector moment 3 but unbounded W_D=2^n, so no bounded L1-to-weighted-graph
operator follows.

The primary smooth four-plaque separator independently reinforces that
boundary: zero edge defects, commuting squares and the strict scalar
properness budget coexist with BV variation N tending to infinity.  Neither
leaf constructs the actual collision-SRB stable tree or physical strong
recipient.

## 4. Gate 5 audit

For label marginals beta_j, the exact standard-Borel criterion was verified:
a label-preserving sub-Markov kernel with mass bound c exists exactly when
beta_(j+1)<=c beta_j, and the minimum c is the essential supremum of the RN
ratio.  The strict, stationary and singular-label finite rows replay with
c_*=1/2, 1 and infinity.

Using the pinned exact rho and w_Z, the independent calculation gives

    q_trace^*=2.0008601538... > 2,
    w_Z sqrt(rho)=1.0000003696... > 1.

Thus q<=2 cannot pay the trace threshold, and q_col=806.02... remains a
different owner-Orlicz exponent.

The two harmonic separators, all six remaining exact-cut codes, extended
N_acc definition, one-shot cemetery typing, signed-plus-common Jordan
bridge, bounded-RN domination tier and all 32 suffix atoms were replayed.
The leaf correctly keeps the unified positive slice, cross-j marginal
contraction, same-law small-gap charge, physical common carrier and all five
suffix values open.

## 5. Cross-leaf red team

No legal cross-leaf substitution closes a gate:

1. a convergent scalar T_n is not the immutable all-plaque twisting token;
2. BL endpoint transport is not the physical strong dyadic-clock ledger;
3. a weighted-median quotient theorem is not an actual stable tree;
4. scalar properness and one finite tag moment do not imply strong assembly;
5. stable-tree covariance does not imply insertion-time lineage contraction;
6. signed current cancellation does not pay positive Jordan common mode;
7. MME product structure, shrinking-hole response and reviews use the wrong
   law or perturbation and were not promoted.

## 6. Acceptance

    Python syntax including shared helper:           11/11
    dependency pin rows across leaves:               69/69
    leaf SHA artifact rows:                          23/23
    leaf integrity/replay:                           5/5
    leaf deterministic re-emission:                  5/5 byte-identical
    hostile semantic mutations:                     1590/1590 rejected
    hostile strict-JSON payloads:                     31/31 rejected
    default producer/verifier entry points:          10/10 exit 2

The audit producer/verifier additionally replay their own canonical manifest,
source arithmetic, semantic mutation set, strict JSON and default exit-2
guard.
