# Paper 1 Compile Status

- Updated: 2026-07-11 CST
- Scope: collision-map conormal modules, source-specific recovery, obstructions,
  a conditional abstract calculus, and a fixed-table continuous-time boundary
- Build: `latexmk -pdf -jobname=response-theory -interaction=nonstopmode -halt-on-error main.tex`
- Result: pass
- Pages: 67
- PDF: `response-theory.pdf`
- Bytes: 838753
- SHA256: `6a03005d74a27f2fc521c39a26ca9984fc22dfe32de12c50018a03b6b3dffa82`

## Active posture

- The positive standard-family route is now recorded at its exact proved
  boundary.  A compactly supported physical bump is prescribed before its
  Poisson primitive and has an explicit nonzero periodic-orbit certificate,
  hence is not a continuous coboundary.  An unnumbered conditional theorem
  proves differentiability of its infinite susceptibility from a uniform
  two-time singular-profile estimate, with the derivative written as an
  absolutely convergent double series.  The text proves that ordinary
  standard-family coupling supplies only the future-time factor.  The
  required past-time conditional-mixing factor remains a genuine open input;
  it is not inferred from the Demers--Zhang gap or from the weighted graph
  domain.  Second shape response remains outside this route because it creates
  curve derivatives and point atoms.

- All unconditional spectral and resolvent arguments now live on the
  transported Demers--Zhang dynamical strong space `B_U`.  The positive
  flux-seed scale `D_U` remains a parameter-trace domain; no `D_U` invariance
  or spectral gap is claimed.  Proposition 3.5, the positive-waiting theorem,
  the correlation primitive/remainder results, the reset interface, and the
  main theorem use the proved `B_U` gap consistently.
- The moving-face section now uses an actual `L^infinity`-anchored weighted
  primitive domain.  Its targets use canonical backward-singularity and
  homogeneity labels, actual one-step `C^r` pullback cocycle weights, and an
  isometric direct limit over artificial refinements.  The weighted iterated
  trace estimate, closability proof, and separate tubular-extension orbit
  bound are explicit.  No bounded `L`-invariance is claimed.  Radial
  invariant-density jets, fixed-length assembled currents/primitives, and the
  corresponding exact-current sources have proved membership.
- The radial reset is now R3-free.  A bounded triangular physical-cutoff
  multiplier is defined on every coefficient sector; it intertwines with
  realization, preserves the realization kernel, descends to the quotient,
  and passes from finite support to the countable completion.  Thus a common
  grazing cutoff may be applied labelwise to the completed historical block,
  and physical assembly commutes exactly with that cutoff.  The assembled identity
  `(I-L^N)rho_j`, bounded radial flux jets, and the `u^3 du` flux then give
  a uniform `O(2^{-4M})` scalar reset tail.  No convergence of raw historical
  labels is claimed.
- The block-flux construction is only a fixed-atlas graph-norm remark.
  It records the two desired one-event estimates and embeds at the correct
  `D_U^(3)=N_5^flux` level, but claims no chart/refinement independence,
  completed operator map, transfer invariance, next-event return, or S1.
- A nonzero prescribed physical correlation density is given for common rigid
  translation with `a(q,v)=omega dot v`.  The source is fixed before its Poisson
  primitive.  In the exact conjugacy trivialization the transfer operator,
  source, and primitive are constant, so `q_1=q_2=0`, the terminal coordinate
  and strong remainder vanish identically, and the susceptibility is `C^J`.
  This is explicitly a consistency proposition, not a moving-face theorem or
  a general strong transport-domain result.
- On that actual weighted primitive/Poisson-pullback domain, the localized gluing map
  for a genuinely moving isolated face is
  surjective onto arbitrary smooth trace profiles.  Its admissible
  source kernel has infinite codimension and, on every compact trace subarc,
  admits a bounded complement.  This rules out generic
  finite-coefficient tuning as a construction of the missing nonconjugate
  source; a structural identity is necessary.  After first recovery, the
  localized q2 face test cuts out an affine infinite-codimension set of first
  source jets, and the same mechanism recurs at every finite order.
- On the same actual interface, because `rho_0=1` at the base table, the defect
  map is first split surjective on a Poisson-independent weighted
  local-potential class.  It is also split surjective on the pullback
  correlation graph class.  The
  observables passing first gluing form a closed complemented
  infinite-codimension subspace with open dense complement in that graph
  topology; every next graph-domain observable jet meets the corresponding
  affine constraint.
- The correlation graph is intersected with an `L^infinity`-anchored rooted
  weighted source space.  Its depth-`d` presentations use the same jet cocycle
  `W_r`; the observable right inverse has the explicit two-root form
  `E phi-L E phi`, so no unweighted high-strip branch estimate is used.
  Regular periodic evaluation extends continuously from this source core.
- On that trace domain, on a free orbit of face subarcs under any
  finite geometric symmetry group,
  applying the central idempotent for any irreducible representation to the
  local right inverse gives a right inverse inside the corresponding isotypic
  source/observable subspace.  Thus parity and finite symmetry do
  not reduce the obstruction; only an additional pointwise stabilizer Ward
  identity could do so.
- A separate geometric proposition rules out that remaining exception for
  physical finite torus isometries: no nonidentity symmetry fixes an open
  regular grazing-face subarc pointwise in a corner-free table of separated
  strictly convex scatterers.
- A local Noether/Ward primitive must also have zero source sum on every
  regular periodic orbit.  Orbit-sum evaluation is onto `R^N` for every finite
  family of `N` disjoint regular periodic orbits, giving an independent
  infinite-codimension constraint.  An invariant local charge yields zero;
  its noninvariant increment is the exact-current benchmark.
- On the augmented primitive domain, face profiles and finitely many
  primitive-orbit values are jointly split by disjoint tubular and orbit-bump
  extensions.  The earlier source-level joint-surjection claim was removed:
  for `g=(I-L)h` with a single-valued primitive, every periodic source sum
  vanishes identically by telescoping.
- On every finite strongly connected regular itinerary subsystem, a
  finite-label finite-memory rule with zero sum on every periodic word is a
  cylinder coboundary by an elementary directed-graph potential argument.
  Hence finite-memory symbolic Ward rules do not produce a new class beyond
  exact currents.
- The actual source-specific radial theorem now appears before the appendix.
  Auxiliary symmetry/cohomology no-go results are in Appendix A; the base
  quotient construction and the conditional S1--S3 calculus are in Appendix B,
  with the conditional propagation subsection explicitly not used
  by the radial theorem.  Fixed-table BDL input and the three moving-flow
  obstructions have been compressed and moved to the final logical-boundary
  section.
- Finite-group representation, physical-stabilizer, periodic/Noether,
  joint-defect, and finite-memory arguments are now auxiliary appendix
  material; the main line keeps the radial package and split
  obstruction.
- Uniform Demers--Zhang input remains matched explicitly to 2013 Theorems 2.2,
  2.5, 2.6, 2.3/Corollary 2.4, and 2.11.

## QA

- Numbered environments: 79 total across the main source and integrated proof
  ledger (24 theorems, 29 propositions, 9 lemmas, 1 corollary,
  11 definitions, 5 assumptions).
- No fatal compile error, undefined reference/citation, rerun warning,
  overfull box, duplicate label, or visible `??`.
- Only non-blocking underfull warnings remain.
