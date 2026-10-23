# R77 author research: unrestricted stopped-law memory certificates

## Integratable files

- `51-unrestricted-approximation.tex`: four numbered statements, complete proofs, and scope discussion. Suggested placement: immediately after current section 48, before the inherited actual-history theorem.
- `bibliography-addition.tex`: one verified primary bibliography entry. Existing `GPT13` is also cited.
- `diagnostics_r77_unrestricted.py`: exact rational finite diagnostic; output path is an optional first positional argument. It deliberately uses explicit failures rather than Python `assert`.
- `diagnostics-normal.json` and `diagnostics-optimized.json`: actual normal and optimized runs; each has 39,087 completed checks and source/script SHA-256 identities. These are author finite diagnostics, not a formal proof or external referee.
- `probe.pdf`, `probe.log`, `probe-build.stdout`: a standalone syntax/layout smoke compile with unresolved references to the surrounding paper. This is not the final manuscript build. The source and bibliography compiled without an error.

## Mathematical advance

The R76 exact obstruction applied to arbitrary classical machines, but its quantitative stopped-law lower was limited to physical hidden dictionaries with Born terminal decoders, and its matching logarithmic phase analysis did not supply a Diophantine lower for the original rational-superoperator phase. The new theorem supplies a quantitative lower for arbitrary classical decoder tables. It is weaker than the physical lower, and the gap is explicitly retained.

Let `a(J)` be the least integer `m` with `binom(m,floor(m/2)) >= J`. A finite family of `J` delayed terminal tests with zero target self-rejection, cross-rejection at least `s`, and herald probabilities at least `p*`, forces at least `a(J)` classical labels at error `delta <= p* s^2/(32 J^2)`. This is an operational theorem for any classical or quantum causal experiment satisfying the observable probability hypotheses. Its proof converts joint stopped-event errors into a normalized nonnegative factorization with a strict diagonal/off-diagonal margin, then uses robust thresholded supports and Sperner's bound.

At the original `z=(3+4i)/5` Bloch phase, the rare prefixes `1 0^n` have probability `zeta 8^{-(n+1)}` and cost at most `B`, where `zeta=min(1,7B/8)`. The exact arithmetic inequality `sin^2(q theta/2) >= 1/(2*5^q)` yields the explicit finite certificate

`delta <= 25*zeta / (128 * 200^J * J^2)  =>  N_cl(delta;B) >= a(J)`.

Consequently the unrestricted minimum is at least logarithmic in `log(1/delta)` for fixed positive `B`. The known physical upper is logarithmic in `1/delta`, with `L+6` mixed or `L+7` pure labels at this original phase. We do not close that remaining asymptotic gap, and do not infer an extra pure-start label in the unrestricted approximation lower.

The all-non-root-algebraic-phase corollary uses an elementary field norm estimate, supplying the same lower order with effective exponential separation constants. It makes no badly-approximable claim. The supplied badly-approximable case uses the stronger polynomial pairwise separation but still only the unrestricted support lower.

## Proof audit

1. The off-diagonal and diagonal estimates use *joint* events. The proof does not divide an unconditional error by an unknown rare probability before bounding that probability.
2. The herald distribution is shared across all delayed terminal choices. A decoder receiving an uncounted full history is explicitly excluded because it changes the memory definition.
3. Arbitrary `[0,1]` decoder columns are permitted; no Born representation, additivity across POVMs, measurement noncontextuality, or hidden quantum states are imposed.
4. The approximation guarantee applies to full records of finitely many preparation--test procedures. Tests use terminal projectors; the new rate is not a report-only quantitative lower.
5. The budget is evaluated in the target. Nontermination or simulator expected cost is not inferred from total variation.
6. Every factor in the robust support argument is at most one. The strict inequality in the lemma survives equality at the final error cutoff because the operational diagonal margin is half the permitted threshold.
7. The power `z^q` is the Bloch rotation, not the half-angle unitary. Exact rational arithmetic checks this convention.
8. General algebraic separation uses the nonzero algebraic integer `(Az)^q-A^q`; root-of-unity phases are excluded before its norm is used.
9. The ordinary factorization antichain cardinality is sharp via equal-size subsets, but this is not an upper construction for the qubit chronological dynamics.
10. New author contribution is the quantitative operational transfer and application to unrestricted stopped simulations. No claim of priority is made for Sperner theory, nonnegative rank support bounds, or elementary algebraic norm separation.

## Integration notes

The diagnostic currently expects its section file beside the script. When moving it into the final source root, either preserve that relative layout or change its source lookup to `sections/51-unrestricted-approximation.tex` and reseal/re-execute; do not reuse its old hash receipt after editing.

The main abstract/overview should distinguish three quantities: the arbitrary-decoder lower `Omega(log log(1/delta))`; the existing general upper `O(log(1/delta))` at one fixed angle; and the matching `~log_8(1/delta)` result only within the physical/Born class under a badly-approximable hypothesis. A finite lower certificate now exists at the original algebraic phase; a matching logarithmic lower there remains unproved even for the physical class unless an independent arithmetic estimate is supplied.

## Primary literature actually inspected

1. Gouveia, Parrilo, Thomas, *Lifts of convex sets and cone factorizations*, Math. Oper. Res. 38 (2013), 248--264, arXiv:1111.3164v2. https://arxiv.org/pdf/1111.3164 . Inspected Section 4.1's zero-diagonal/nonnegative-rank antichain argument, and Corollary 4.13's face-antichain bound. This directly establishes that the exact antichain ingredient is classical. Web retrieval references `turn4view0`, `turn7view1`.
2. Vandaele, Gillis, Glineur, *On the linear extension complexity of regular n-gons*, Linear Algebra Appl. 521 (2017), 217--239, DOI 10.1016/j.laa.2016.12.023, arXiv:1505.08031v2. https://arxiv.org/abs/1505.08031 and https://arxiv.org/pdf/1505.08031 . Inspected Section 3.1, theorem on antichains, and explicit discussion that the exact support bound for hollow Euclidean distance matrices was already known. Journal metadata and DOI verified on official arXiv abstract. Web references `turn4view1`, `turn7view2`, `turn12view0`.
3. Hrubes, *On the nonnegative rank of distance matrices*, Information Processing Letters 112 (2012), 457--461. Author-hosted preprint https://users.math.cas.cz/~hrubes/PDFs/mrank.pdf and bibliography page https://users.math.cas.cz/~hrubes/papers.html . This is context for why low ordinary rank does not imply large unrestricted nonnegative rank, and why a physical dictionary packing lower cannot simply be asserted for arbitrary decoders. No theorem of this paper is required in the new proof. Web references `turn7view0`, `turn4view2`.

These source checks identify classical ingredients and relevant comparisons. They are not an exhaustive priority clearance, expert endorsement, or editorial assessment. The publisher page for Vandaele et al. returned HTTP 403; full text and journal metadata were available from the authors' arXiv deposit.
