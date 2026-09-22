# Independent harsh top-four referee report — A2 nominal revision v119 (Round 2)

**Manuscript family:** A2, last materialized title: *Conductor strata and nonreduced multiplication failure schemes*  
**Author:** Qian Qi  
**Repository:** TrillionniumFoundation/theta-theory  
**Nominal revision branch reviewed:** `revision/a2-v119-full-failure-embedded-conductor-2026-09-22`  
**Nominal v119 branch HEAD found in repository history:** `d4254d9b01405ad02c64d2ff591503d4cc7a6aa7`  
**Last actual A2 mathematical product HEAD:** `44bfc648ead008896a6981a7302a6d5ab8b21bb8`  
**Last actual mathematical revision:** `revision/a2-v118-higher-defect-nonreduced-generators-2026-09-22`  
**Frozen v118 mathematical source identified by the prior v118 review:** `c87bfdad8d97e68637d269e656b46c4cce85551e`  
**Date:** 22 September 2026

## Referee status

This is an owner-requested, AI-assisted external-referee-style report. It was not commissioned by *Annals of Mathematics*, *Inventiones Mathematicae*, *Journal of the American Mathematical Society*, *Acta Mathematica*, or any other journal, and it must not be represented as a journal-issued report or editorial decision.

I have deliberately reviewed two logically distinct objects:

1. the **nominal v119 revision branch**, to determine whether there is actually a new mathematical revision to referee; and
2. the **latest materialized mathematics**, which remains v118, in order to give a scientifically meaningful top-four assessment rather than merely stopping at a repository/provenance objection.

That distinction is essential here.

# Recommendation

## 1. Nominal revision v119: return without scientific re-review

The branch named

`revision/a2-v119-full-failure-embedded-conductor-2026-09-22`

is **not a mathematical revision**.

Direct comparison with

`revision/a2-v118-higher-defect-nonreduced-generators-2026-09-22`

shows that v119 is ahead by exactly one commit and that the **only changed path** is

`reviews/a2-v118-independent-harsh-top4-2026-09-22/REFEREE_REPORT.md`.

No manuscript source, theorem statement, proof source, response-to-referee document, revision index, source identity, build receipt, or v119 article directory is added by the nominal v119 delta.

Therefore the advertised mathematical content “full-failure-embedded-conductor” is not present at the branch HEAD.

This is a fatal revision-workflow defect. A branch label is not a theorem.

## 2. Latest actual mathematics, v118: reject in present form for a general top-four journal

I do not base this recommendation on a discovered contradiction in the headline v118 theorems. The main new mechanisms remain mathematically plausible and, in several places, technically elegant.

The top-four assessment remains negative because the paper still lacks a theorem of sufficient breadth and conceptual force connecting the new conductor formalism to the **full multiplication-failure scheme**. The central gap is still the same one the manuscript itself exposes: the higher-defect structure naturally controls an extreme-corank / higher-Fitting locus, not the full zeroth-Fitting failure geometry.

The nonreduced multigenerator flagship theorem is exact but geometrically too rigid: its entire stable scheme is a pure power of one determinant Cartier divisor. The codimension-two conductor theorem is clean but remains a low-rank representation-theoretic classification of quotient data, not a classification of the ambient failure scheme. The two mechanisms remain parallel rather than unified.

A genuine v119 could change this assessment if it actually proves the “full-failure / embedded-conductor” theorem suggested by the branch name. The present branch does not.

# I. Repository and provenance audit

## I.1 The nominal v119 branch contains review history, not new mathematics

The repository comparison is unambiguous.

Relative to v118 product HEAD `44bfc648...`, the nominal v119 line adds one review file and no mathematical source.

This means the following basic questions have no v119 answer:

- Which theorem changed?
- Which proof changed?
- Which v118 referee objection is claimed to be closed?
- Where is the v119 source tree?
- What exact commit is the mathematical source?
- What PDF, if any, is the v119 journal object?
- What response document maps referee objections to mathematical changes?
- What is the theorem-level delta relative to v118?

A serious revision workflow must answer these from the branch itself.

## I.2 The v119 branch name overstates what exists

The words “full-failure-embedded-conductor” are mathematically substantive. They suggest at least one of the following:

- a theorem identifying the full (operatorname{Fitt}_0) failure scheme in a higher-defect family;
- an embedded-component theorem;
- a conductor-controlled primary decomposition;
- a theorem connecting conductor strata to associated primes of the full failure scheme.

No such v119 theorem is materialized in the nominal branch.

The mismatch between branch name and branch content is not cosmetic. It risks confusing future authors, reviewers and automated provenance tools about what has actually been proved.

## I.3 Required repair before calling anything v119

A real v119 should contain, at minimum:

- a v119 mathematical source tree;
- an explicit identity/manifest file;
- a theorem/proof delta from v118;
- a response to both extant v118 referee reports;
- a source pin identifying the last mathematical-change commit;
- a product/build receipt if PDFs are committed;
- and a branch HEAD that points to the mathematical/product revision rather than to a referee-report commit.

Until then, v119 should not be described as a scientific revision.

# II. What v118 genuinely achieves

A harsh referee report should still distinguish real advances from insufficient advances.

## II.1 Stable generated algebra and conductor/action stratification

After local unit normalization, the manuscript stabilizes powers of the universal subspace and extracts a generated subalgebra bundle (E). On exact-rank strata of the stable multiplication map, (E) is locally free and acts on

[
M=B/E.
]

The kernel

[
J=ker(E	ooperatorname{End}(M))
]

is the conductor, and the quotient data

[
C=E/Jsubset Q=B/J
]

gives a faithful action on (Q/C).

This is a genuine relative structure theorem. The manuscript correctly restricts base-change claims to exact-rank strata rather than pretending conductor formation commutes with arbitrary specialization.

That is mathematically responsible and worth preserving.

## II.2 The nonreduced rank-jump example is useful

The example

[
E=langle 1,,s z^2+z^3,,z^4anglesubset mathbb C[s][z]/(z^5)
]

produces a nonreduced action-rank locus with scheme structure (s^2=0).

This is a good example because it shows why the exact-rank stratification is not pedantry: the relative conductor data genuinely changes scheme-theoretically at the boundary.

The paper would benefit from using this example more centrally to motivate what a future full primary theorem should detect.

## II.3 The codimension-two quotient theorem is conceptually clean

When (B/E) has rank two, the commuting trace-zero endomorphism argument gives a rank-at-most-two action. The resulting exact-rank dichotomy produces:

- a rank-three quotient with scalar subalgebra, or
- a rank-four quotient (Q) which is rank two over a rank-two algebra (C).

This is one of the best results in v118.

It is a complete theorem in a genuinely nontrivial low-rank case.

## II.4 The fat-point determinant theorem is exact

For

[
B_{e,h}=mathbb C[z_1,ldots,z_e]/(z_1,ldots,z_e)^h,
]

the manuscript identifies the stable failure ideal on the ((e+1))-plane parameter space as

[
mathcal I_Delta^N,
qquad
N=inom{e+h-1}{e+1}.
]

After unit normalization, the key endomorphism is substitution

[
T_x:z_imapsto x_i.
]

The (mathfrak m)-adic filtration gives graded blocks (operatorname{Sym}^j M), so

[
det T_x
=
prod_{j=1}^{h-1}det(operatorname{Sym}^j M)
=
(det M)^N.
]

This is a clean and useful calculation.

## II.5 The global fat-point transport theorem is also real

The projective-space theorem for an order-(h) fat point and (nge2h-1) is not merely a local-algebra restatement. The triangular monomial argument supplies an actual global saturation/cokernel comparison.

The theorem is stronger than a toy example and deserves to remain in the paper.

# III. The central top-four obstruction: the paper still does not control the full higher-defect failure scheme

This is the decisive mathematical issue.

The higher-defect conductor theorem works by passing to a stable generated subalgebra and then stratifying the action on the quotient.

That is excellent structure on selected strata.

It is not a classification of the full multiplication failure locus.

For codimension (r>1), the manuscript itself identifies the unital-subalgebra locus with an extreme-corank Fitting condition of the form

[
V!left(
operatorname{Fitt}_{r-1}
operatorname{coker}(operatorname{Sym}^mW	o B)
ight),
]

whereas the ordinary nonsurjectivity scheme is governed by

[
operatorname{Fitt}_0.
]

These are different schemes.

For a top-four paper, the conductor flag should become a tool for proving a theorem about (operatorname{Fitt}_0), not the endpoint of the theory.

The missing theorem should answer questions such as:

- What are the irreducible components of the full failure scheme?
- Which conductor/action strata dominate which components?
- What are their generic coranks?
- What are the closure relations between exact-rank strata?
- Where do embedded components occur?
- What are the local normal forms near stratum collisions?
- How do primary exponents depend on conductor data?
- Which singularities occur generically?

v118 does not yet provide this.

# IV. Codimension two is a strong model case, but it has not yet been turned into failure geometry

The rank-two quotient-module theorem is elegant precisely because (operatorname{End}(M)) is so small.

For rank-two (M), commuting trace-zero matrices are highly constrained. This produces the rank-three/rank-four quotient dichotomy.

That mechanism is special.

The paper presently stops after classifying quotient/conductor data.

A much stronger theorem would identify how the two mechanisms occur inside the **actual codimension-two (operatorname{Fitt}_0) failure scheme**.

For example:

- Are the two quotient mechanisms generic points of different components?
- Can one specialize to the other?
- What is the local scheme at their meeting locus?
- Does the (s^2=0) rank-jump model appear systematically as a transversal local structure?
- Are there embedded associated points along the transition?
- What is the normalization of the relevant component(s)?
- What equations cut out the closures?

This is the most natural route to a genuinely strong v119.

# V. The flagship nonreduced family is exact but geometrically too easy

The fat-point theorem gives a nonreduced family in arbitrary embedding dimension and nilpotence order.

However, its entire stable scheme is

[
NDelta
]

for one irreducible Cartier determinant divisor (Delta).

Once this is known, many advertised primary statements become formal:

- there is one associated prime;
- every positive power is primary;
- there are no embedded primes;
- the transverse multiplicity is (N);
- nilpotence is controlled by the single exponent (N).

This is legitimate nonreduced geometry, but it is the simplest possible nonreduced geometry.

The family does not exhibit:

- multiple primary components;
- embedded primes;
- non-Cartier support;
- higher-jet-dependent support;
- collisions of different conductor strata;
- or a nontrivial conductor-to-primary correspondence.

For a specialist paper this may be a satisfying rigidity theorem.

For a top-four paper it is not enough by itself.

# VI. The tangent determinant controls everything; higher jets disappear

A revealing aspect of the proof is that the stable determinant depends only on the linear coefficient matrix

[
M:K	omathfrak m/mathfrak m^2.
]

All higher-order coefficients of the generators disappear from the determinant.

This is a strong theorem.

It also shows exactly where the significance ceiling lies.

Increasing (h) changes only the power (N). It does not create new support, new components, new associated primes or new local singularity types beyond those inherited from a determinant hypersurface.

Thus the “arbitrary embedding dimension and nilpotence order” generality is quantitative more than qualitative.

A genuinely stronger family would be one in which higher jets alter the primary geometry.

# VII. The paper already contains evidence of harder embedded behavior, but only as isolated local material

Elsewhere in the manuscript family there are local examples of the form

[
(ab,b^2)=(b)cap(a,b)^2,
]

which exhibit an embedded or mixed primary phenomenon qualitatively richer than a pure power of one prime divisor.

This raises the right question:

Can the paper produce a **systematic multigenerator family** where such embedded structure is unavoidable and computable?

If yes, that would justify the “embedded conductor” language and materially improve the paper.

At present, no v119 theorem doing so is committed.

# VIII. The global fat-point theorem is a transport theorem, not a classification theorem

The global theorem for a single homogeneous fat point in (mathbb P^e) is useful.

Its proof is nevertheless driven by monomial degree intervals and triangular basis arguments.

The support is one maximally symmetric local model.

A broader theorem would need to survive for classes such as:

- unions of fat points;
- mixed multiplicity schemes;
- local complete intersections;
- nonmonomial Artin quotients;
- families with varying Hilbert function;
- or local algebras whose associated graded structure varies in moduli.

Until then, the projective-space theorem should be described as a sharp transport mechanism for one tractable family, not as a general higher-dimensional classification.

# IX. The two flagship mechanisms are still parallel rather than unified

The conductor mechanism produces

[
E,quad J,quad Csubset Q,quad 	ext{action-rank strata}.
]

The fat-point mechanism produces

[
M,quad T_x,quad det T_x,quad mathcal I_Delta^N.
]

The paper does not yet prove that the conductor data predicts the primary exponent (N), associated primes, or the full local equation.

Nor does the fat-point determinant illuminate a nontrivial interaction between different conductor strata.

This is the architectural weakness of the current A2.

The paper has two good pieces of exact mathematics.

It does not yet have the theorem that makes them one theory.

# X. Terminology and statement-level issues that should be fixed

Even independently of venue, the next actual mathematical revision should address several clarity issues.

## X.1 Distinguish unit-generation from algebra-generation

In the fat-point parameter space, “generating” can mean different things.

The relevant open first guarantees a local unit / augmentation surjectivity. Off the determinant divisor, the tangent classes span (mathfrak m/mathfrak m^2), and only then does Nakayama imply algebra generation.

The manuscript should use terminology such as:

- unit-generating / augmentation-generating open;
- algebra-generating subopen.

Then (Delta) is exactly the boundary between them.

## X.2 Define (Delta) intrinsically

Rather than treating (Delta) primarily through frame coordinates, define it globally as the determinant divisor of

[
Klongrightarrow (mathfrak m/mathfrak m^2)otimesmathcal O_X.
]

Compute its determinant line bundle / divisor class.

This would make the geometry cleaner.

## X.3 Isolate the relative cyclic-vector lemma

The codimension-two rank-two action argument should include a standalone relative lemma proving:

- openness of the cyclic-vector condition;
- local freeness of (Q) over (C);
- compatibility with base change.

The argument is plausible but currently too compressed relative to its conceptual role.

## X.4 State the scheme-theoretic meaning of (operatorname{Fitt}_0=0)

Below the stable threshold, if the zeroth Fitting ideal is zero, the failure scheme is the whole parameter space.

Say this explicitly.

## X.5 Separate mathematical-source provenance from workflow provenance

The repository should maintain distinct fields for:

- `mathematical_source_commit`;
- `last_math_change_commit`;
- `product_commit`;
- `workflow_commit`;
- `controlling_review_commits`.

The present v119 accident is exactly what happens when these identities are conflated.

# XI. What a real v119 should contain

The branch name already suggests the correct ambition. A real v119 should materialize one of the following types of theorem.

## XI.1 Full codimension-two (operatorname{Fitt}_0) classification

Use the quotient/conductor dichotomy to determine the actual nonsurjectivity scheme, including:

- components;
- dimensions;
- generic coranks;
- closure relations;
- singular/embedded structure at the transition.

This is the most direct upgrade.

## XI.2 A systematic embedded-primary theorem

Construct a natural multigenerator family whose stable failure scheme has:

- multiple associated primes;
- an embedded associated component;
- or non-Cartier primary support,

and prove its primary decomposition.

This would finally make “embedded conductor” a mathematical theorem rather than a branch label.

## XI.3 Conductor-to-primary theorem

Prove that conductor/action invariants determine primary exponents or associated-prime structure in a nontrivial class.

That would unify the two current pillars of the manuscript.

## XI.4 Higher-rank quotient geometry

For (operatorname{rank}(B/E)ge3), go beyond mere action-rank stratification and derive equations or moduli structure for the relevant commutative subalgebras of (operatorname{End}(B/E)) that arise from multiplication.

A rank stratification alone is not enough.

## XI.5 A family with genuine higher-jet dependence

Find an Artin family in which higher-order coefficients of the generators change:

- support;
- associated primes;
- embedded structure;
- or singularity type.

This would demonstrate that the theory is not merely tangent-determinant rigidity.

# XII. Final assessment

The mathematical trajectory is improving.

v118 is not empty work. It adds a serious conductor/action formalism, a clean codimension-two quotient theorem, a nonreduced rank-jump example, an exact truncated-local-algebra determinant formula, and a global fat-point transport theorem.

But a top-four paper needs more than an accumulation of correct exact mechanisms.

It needs a theorem that reorganizes the subject.

The current A2 still stops one step before that point.

The strongest candidate for such a theorem is already visible from the manuscript's own architecture:

> **show that conductor quotient data controls the full higher-defect zeroth-Fitting failure scheme, including its components and nonreduced/embedded primary structure.**

That is what a genuine “full-failure-embedded-conductor” revision should prove.

The nominal v119 branch currently proves none of this because it contains no new mathematics at all.

## Decision summary

- **Nominal v119 as a revision:** not scientifically reviewable; return without re-review.
- **Latest actual mathematical content (v118):** substantial but below general top-four threshold in present form.
- **Fatal proof contradiction found in v118 headline theorems:** no.
- **Fatal provenance/revision-identity defect in nominal v119:** yes.
- **Primary mathematical blocker:** conductor stratification still does not classify the full (operatorname{Fitt}_0) failure geometry.
- **Most promising next theorem:** full codimension-two failure scheme with embedded/primary conductor structure.

