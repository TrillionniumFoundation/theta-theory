# Appendix S — Actual nonconjugate radial specular U3

This appendix is normative for the export `P1-SINAI-RADIAL-U3`.  The full proof
is maintained in

```text
../../maximal-strengthening/SPECULAR_SINAI_RADIAL_U3.md
```

## S.1 Actual family

One circular scatterer in a periodic finite-horizon dispersing table is
inflated radially while all other scatterers remain fixed.  In normalized
collision coordinates the invariant density is

\[
\rho_a(s,\varphi)
=
\frac{\ell_i(a)\cos\varphi}
{2\sum_j\ell_j(a)}.
\]

A period-two monodromy has parameter-dependent trace; hence the family is not
smoothly conjugate to the base table.

## S.2 Complete differentiated-invariance source

For distributional parameter letters `L_0^[k]`, differentiating
`L_a rho_a=rho_a` gives

\[
S_j
=\sum_{k=1}^j\binom jkL_0^{[k]}\rho_0^{(j-k)}
=(I-L_0)\rho_0^{(j)}.
\]

The right-hand side is a centered strong density.  Therefore all singular
letters on the left cancel after complete physical assembly, and

\[
R_0S_j=\rho_0^{(j)}.
\]

This proves actual order three and arbitrary finite order for the invariant
projector.

## S.3 Exact-coboundary twist

For `kappa_a=g_a-g_a o T_a`,

\[
L_{a,q}=M_{e^{-qg_a}}L_aM_{e^{qg_a}},
\]

so the twisted projector and reduced resolvent have all mixed finite-order
`(a,q)` derivatives.

## S.4 Scope

This appendix does not export generic centered noncoboundary pressure U3 from
geometry alone.  The split-surjective face-defect theorem rules out that
upgrade.  A general noncoboundary channel must submit the bilateral
third-source packet of the main paper.
