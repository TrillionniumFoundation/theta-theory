# Author-team challenge record: finite search for any finite number of locations

## Scope and source identity

The complete draft is `59-finite-search-saturation.tex`.

Current source SHA-256:

`ad5e939156204c372d76bc587a36b6c2169f705012133ba89a43f6aaf6653dbd`

The declaration record is `R80_FINITE_SEARCH_DECLARED_STATEMENTS.json`
and contains seven declarations with hypotheses, conclusions, direct
dependencies, proof mechanisms, priority keys, and explicit limits.

This is an author-team record produced by collaborating automated
agents. It is neither an independent human expert assessment nor a
formal proof certificate. The universal assertions are supported by
the manuscript's written proofs. The separate exact-arithmetic
diagnostic suite checks finite identities and examples only.

## Development and retained alternatives

The initial question was whether the two-location arithmetic
classification could extend to every finite number of imperfect
search locations with arbitrary positive deterministic command costs.
The eventual result retains the two-location section, including its
sharper normalized quantitative constants, and adds a general section.

The first proposed sufficiency route used a finite posterior-state
occupation measure and stationary realization. It was not needed.
The delivered proof instead reproduces the classical consistent-tie
mixture result using linear functionals of the risk vector, then
implements its at most n deterministic words with a counted pure
initializer. No occupation-measure assertion is used as an unproved
bridge.

A necessity argument based only on individual deterministic words
would not cover arbitrary stochastic controllers. A second argument
based only on pairwise irrationality would omit mixed families in
which some logarithmic increments are commensurable. The delivered
proof addresses both points: it projects the word onto rational
commensurability classes, proves a common deterministic suffix for
every optimal greedy word, and applies a finite support-set evolution
argument to all stochastic kernels. Within-class command mixing is
allowed throughout.

Primitive-data constants were added only after the structural proof.
The key estimate is a uniform strict improvement on every other
model when all calls to one model's command are deleted. This leads
to an explicit least-favourable-prior floor, which removes the
unknown prior from both the exponential approximation bound and the
rational-data finite label cap. The cap is an effectivity result;
its magnitude is not presented as computationally practical.

## Priority boundaries

The greedy search rule, existence of an interior least-favourable
prior, equalized risk, and at most n consistent-priority word mixture
are classical search theory and are explicitly credited. Common-power
eventual cycles for arbitrary finite n are likewise credited to
Clarkson--Lin--Glazebrook, Section 6.1 and Appendix C, including its
earlier attribution to Matula. These components are reproduced in
full for transparent dependencies and are not presented as new.

The added resource statements concern the all-stochastic counted-memory
necessity argument through partial commensurability classes, the
explicit primitive-data prior floor and memory approximation rate,
and the resulting computable label cap. The written claims remain
scoped to the displayed scalar search family. No literature search
is represented as an exhaustive certification of novelty.

## Adversarial checks made in the written proof

1. **Properness and word laws.** Each finite-risk word uses every
   command infinitely often. Planned-word conditioning does not
   reveal the hidden model, because prefix likelihood cancels between
   private realizations with the same command prefix.
2. **Boundary priors.** Deleting zero-prior commands gives a strict
   improvement only in the retained support. The proof completes
   finite prefixes with a common proper fallback before using this
   competitor in the all-model separation argument.
3. **Infinite reorderings.** Uniform geometric tails justify both
   continuity of the greedy risk map and the limit of infinitely many
   tie-block reorderings.
4. **Finite mixtures.** A common order of decreasing lambda_i/pi_i
   minimizes every tied block for a given linear functional. Convex
   separation and affine elimination, not an unsupported finite
   mixture assumption, yield the at most n words.
5. **Partial commensurability.** Distinct classes share only finitely
   many tied item pairs. Class-frequency ratios are irrational even
   when a class contains several rationally related increments.
6. **Stochastic memory.** The union of positive command/update
   supports gives a deterministic map on nonempty label subsets.
   A deterministic class suffix therefore must eventually repeat.
7. **Counted initialization.** One prescribed initial label samples
   the first command, and only after failure is a compatible branch
   chosen and stored in counted tail labels. There is no free mixed
   initial state or persistent random seed.
8. **Prior constants.** Markov's inequality is applied to the number
   of paid calls. The deletion event has planned probability at least
   one half, and its deleted call has survival at least r_min^T0 in
   every other model. The restricted problem genuinely omits the
   deleted command. The simplification to delta=g/(2K) uses
   V >= c_min > g/2.
9. **Memory constants.** For T >= 1, the initializer, at most
   n(T-1) continuation labels, and one fallback use at most nT labels
   because n >= 2.
10. **Exact rational cap.** A primitive signed prime-exponent vector
    gives an integer common-power representation by Bezout's
    identity. A bounded interval of length 2N0 lattice units contains
    at most 2N0+1 points of every offset coset. The sufficient memory
    bound therefore does not require knowing the optimal prior.

## Assumption sensitivity and limits

The proof uses 0 < r_i < 1. At r_i=0, positive failure likelihoods
and the requirement of infinitely many attempts fail; at r_i=1,
the corresponding model is infeasible. Strictly positive call costs
are required for call-count and compactness arguments. Model-independent
costs are used in the exact adjacent-exchange vector. An uncounted
external clock or persistent infinite seed would alter the finite
autonomous-memory problem and is not allowed.

The estimates give an upper approximation rate. Irrationality alone
is not converted into a numerical lower bound on a given finite-M
gap. Algebraicity and computability of the history value are asserted
only in the rational saturating case, via its explicit finite budget.
No arithmetic classification is claimed for arbitrary noncommuting
quantum instruments or for the larger Theta research program.

## Review status

The drafting agent checked all proof steps and constants. The
separate `math_challenge` agent completed an adversarial read of the
entire mathematical source at the pre-clarification hash
`8e48af95faf9f8ce8c563b3d9b9d51c8fce408881ece30eee68e8ba74c31b053`
and reported no substantive gap,
including the fixed finite cross-class tie cutoff, the affine
mixture reduction, and all primitive-data constant and label-cap
steps. The parent author-integration agent retains responsibility
for the controlling integrated source hash, native LaTeX compilation,
repository-wide dependency checking, and publication provenance.

The independent diagnostic source is
`/tmp/theta-math-challenge/diagnostics_r80_general_search.py`, SHA-256
`e176adba2c2a4906e530908fe6db3b662468baf9ce12f4a0d6194d8c4dbc9425`.
Its normal and Python `-O` runs both completed 24,254 exact rational
checks and produced byte-identical reports. These include 22 complete
periodic-mixture product chains, in addition to prefix/fallback
implementations and arithmetic and tail identities. The independent
source-pinned mathematical audit is
`/tmp/theta-math-challenge/R80_GENERAL_SEARCH_INTERNAL_AUDIT.md`.
These are finite independent diagnostic and internal reasoning
records; they do not constitute formal verification or external
human endorsement.

A final full reread by the drafting and parent integration agents found
no substantive gap in quantifiers, strict parameter boundaries, or
conditional first-command mixture. Relative to the independently
reviewed 8e48af95-prefixed source, the final source changes only the
theorem title to "for any finite number of locations", explicitly
defines the unreachable initial update rows when p_a=0, and splits
two long displays across lines. The p_a>0 conditional-mixture formula
and all mathematical conclusions are unchanged. These final
clarifications are being repinned in the independent audit.

Canonical declaration JSON SHA-256: `78cd0d6085dcecb307921179af05969bc7c8e068f196bc82acd85c0952106af7`.

## Native production clarification after the final author read

The integrated source is SHA-256 `3220cac3bd7ab6220d96eb3115e006ff040959098cc4171513a9b1aa9f70cd9d`. Native draft 02 exposed a LaTeX alignment error: the prior-constant display used multiple alignment pairs inside `split`. Both `split` display environments were changed to `aligned`, without editing any formula. Draft 03 completed the paired native compile. The separate final-hash audit in `R80_GENERAL_SEARCH_INTERNAL_AUDIT.md` authenticates this exact clarification boundary. Draft compilation is not strict committed-source verification.
