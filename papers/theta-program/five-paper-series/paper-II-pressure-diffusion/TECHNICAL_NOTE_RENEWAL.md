# Normative clarification: suspension renewal operators

This note is part of Paper II's proof draft and gives the precise reading of
Section 5.  It supersedes any reading in which the two roof-cell transforms in
the displayed renewal pairing are assumed to be the same elementary integral.

Let `F,G` be flow observables and let

\[
L_{a,z}=L_a(e^{-z\tau_a}\,\cdot).
\]

Return decomposition produces three bounded objects:

1. an entry vector
   \[
   \mathcal I_{a,z}G\in B_a;
   \]
2. an exit functional
   \[
   \mathcal O_{a,z}F\in B_a^*;
   \]
3. a finite same/adjacent-cell term
   \[
   H^{\rm cell}_{a,z}(F,G).
   \]

They are obtained by integrating over the incomplete initial and terminal roof
segments with their correct time orientation.  Their exact formulas depend on
the suspension convention, but contain only finite roof-cell integrals and
endpoint terms.  The long-return identity is

\[
\boxed{
\widehat C_{F,G}(a,z)
=
H^{\rm cell}_{a,z}(F,G)
+
\mathcal O_{a,z}F
\left[(I-L_{a,z})^{-1}\mathcal I_{a,z}G\right].
}
\tag{R.1}
\]

The notation `widehat F`, `widehat G` in the manuscript is shorthand for these
exit and entry objects, respectively; it does not assert that they are the
same transform.

Near zero,

\[
(I-L_{a,z})^{-1}
=
\frac{\Pi_{a,z}}{1-\lambda(a,0,z)}
+R_{a,z}^{\perp}.
\tag{R.2}
\]

For centered correlations, the rank-one contribution in (R.2) cancels with the
product-of-means term in the definition of `C`.  Since

\[
\partial_z\lambda(a,0,0)=-\bar\tau_a\ne0,
\]

the remaining reduced expression is regular at zero.  All parameter and
low-frequency derivatives through total order three are finite combinations
of:

- derivatives of `H^{cell}`;
- derivatives of `I` and `O`;
- the Paper-I/Paper-II reduced-resolvent words.

Thus the low-frequency suspension theorem uses no unproved high-frequency
moving-flow graph-domain assertion.
