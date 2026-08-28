# Round213 report erratum: tail regions are a tagged strict-open subset

This erratum applies only to the narrative sentence at line 89 of the frozen
Round213 report:

- frozen report:
  `cm2_round213_source_g_round182_residual_dimensional_union_report.md`
- frozen report SHA256:
  `a55e4862e147c76b8e45c9b8125f9b8ba3aa7efb403ca35a47fb2a23d55f94f6`
- frozen six-entry manifest SHA256:
  `85fa3bb452c88e4c4aec12a3744fab1c206dd9ca7086ab64cee96448d24d9673`

The sentence “The `96` Round204 tail regions are not strict-open regions” is
incorrect.  The correct statement is:

> The `96` Round204 tail regions are a tagged subset of the `736` Round204
> strict-open 3D regions.  They are separately reported but non-additive.

The formal Round213 certificate, verifier, verification, and strict-open
union are already correct:

- Round204 contributes `736` strict-open 3D region rows in total, of which
  `96` carry the tail tag.
- Round208 contributes `36,040` strict-open 3D region rows.
- The disjoint strict-open union is therefore `736 + 36,040 = 36,776`.
- The verifier explicitly rejects an attack that adds the `96` tagged tail
  rows a second time.

No certificate field, verification result, credit, gate state, or frozen
Round213 artifact is changed by this erratum.  The original six-entry
manifest remains immutable; later artifacts must cite this correction when
describing the Round204 tail census.
