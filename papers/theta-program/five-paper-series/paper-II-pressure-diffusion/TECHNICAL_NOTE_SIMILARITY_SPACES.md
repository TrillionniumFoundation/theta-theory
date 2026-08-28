# Technical note: transported anisotropic spaces for the similarity family

Let `B_0` be any fixed-table anisotropic space on which the flow generator `A_0` and its BDL resolvent are defined.  For the scaled table set

\[
B_a=C_aB_0,
\qquad
\|C_af\|_{B_a}:=\|f\|_{B_0}.
\]

Thus `C_a:B_0->B_a` is an isometry by definition.  Pulling every object back to `B_0` gives

\[
\widetilde A_a
=C_a^{-1}A_aC_a=s(a)^{-1}A_0
\]

and

\[
(z-\widetilde A_a)^{-1}
=s(a)(s(a)z-A_0)^{-1}.
\]

Hence no differentiability of the geometric transport on a pre-existing fixed anisotropic norm is required.  On the transported bundle the parameter dependence is entirely the scalar map `s(a)`.  For every integer `k`, derivatives of the resolvent are finite sums of fixed-table resolvent powers multiplied by derivatives of `s`.

The high-frequency region also transports exactly: if `w=s(a)z`, then a fixed-table resonance-free strip or cone for `w` becomes its scalar pullback for `z`.  Compact bounds `s_-<=s(a)<=s_+` make all constants uniform.

This note is the normative functional-analytic interpretation of `P2-BDL-HF-SIMILARITY`; it prevents the exact scaling example from being read as a proof that arbitrary geometric pullbacks are differentiable on one fixed BDL space.
