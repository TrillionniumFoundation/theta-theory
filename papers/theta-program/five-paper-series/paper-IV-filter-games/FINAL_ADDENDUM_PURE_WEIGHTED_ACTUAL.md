# Final addendum: maximal pure Isaacs theorem and weighted noncompact actual filter

## 1. Pure saddle

For compact metric control sets and continuous `F(z,u,v)`, define

\[
H^-(z)=\max_u\min_vF(z,u,v),
\qquad
H^+(z)=\min_v\max_uF(z,u,v).
\]

### Theorem P4-PURE-ISAACS-MAXIMAL

A pure saddle exists at `z` if and only if

\[
H^-(z)=H^+(z).
\]

The reverse direction follows by choosing a maximin optimizer and a minimax optimizer.  Matching pennies shows that equality is not automatic.

For noncompact Euclidean controls, the quadratic-bilinear class

\[
F=f+a\cdot u+b\cdot v
-\frac\mu2|u|^2+rac\nu2|v|^2+u^TKv,
\qquad \mu,\nu>0,
\]

has a unique pure saddle.  The saddle operator `G=(-D_uF,D_vF)` obeys

\[
\langle G(w)-G(w'),w-w'\rangle
=\mu|u-u'|^2+\nu|v-v'|^2,
\]

because the mixed terms cancel.

## 2. Weighted noncompact actual filter

Let the hidden state be the Gaussian coordinate of a deterministic product shift and let

\[
W(y)=1+y^2.
\]

Use observations `o in {-1,+1}` with

\[
g_o(y)=\frac{1+o\epsilon_o\tanh y}{2},
\qquad 0<\epsilon_o<1.
\]

The hidden transition replaces the current coordinate by the next independent Gaussian coordinate.  Thus every prior is sent to the same Gaussian prediction in one step.  The posterior is

\[
\pi^o(dy)
=\frac{g_o(y)\gamma(dy)}{\int g_o\,d\gamma}.
\]

All posterior `W` moments are uniformly finite and the filter forgets its initial belief exactly after one prediction-update cycle.

## Exports

```text
P4-PURE-ISAACS-MAXIMAL
P4-WEIGHTED-NONCOMPACT-ACTUAL
```
