# Author proof audit: explicit physical optical comparison

This is an author-side derivation and dependency check of native module 313. It is not a referee report, a claim of an independent human reconstruction, or a certificate produced by finite computation. Historical module 238 and its qualitative proof are preserved. The new result makes the original norm, coordinate conversion and uniform constants completely explicit.

## Exact statement and scope

For the actual triangular Lorentz gas with unit speed, radius \(R\in[9/20,47/100]\), true first-collision map \(T_R\), and the invariant lines at points regular in both time directions, Theorem **thm:eo-optical** proves
\[
 \frac{c_mj_m}{30000}\le\omega\le30000c_mj_m,
 \qquad j_1/c_0\le6400.
\]
Here \(j_m=J^sT_R^m\) is Euclidean stable arclength in the actual coordinates \((s,\varphi)\), \(s=R\alpha\), and \(\omega=|\partial_{p_0}\alpha_m|^{-1}\) is the original endpoint optical weight, with \(p=\sin\varphi\). The bounds hold before insertion of any original return, displacement, collision-count, section or roof test. No endpoint cap is needed beyond regularity. No collision-dependent adapted metric is used.

The optical statement is for \(m\ge1\). For the empty block only \(j_0=1\) is asserted; the optical inverse derivative is not defined at \(m=0\). Original physical flight bounds \(\tau_-=3/50\) and the true radius interval are retained. The probability stays \(\nu=d\alpha\,dp/(4\pi)\), with exactly the original \(c_*^{-1}\) section conditioning.

## Differential, sign and invariant lines

1. With counterclockwise tangent \(t\), the actual departure and arrival directions are \(v=cn+pt=-c'n'+p't'\). Differentiating the physical flight and arrival angle gives
   \[
   -c'\delta s'-c\delta s=\tau(\delta\varphi+\varkappa\delta s),
   \qquad
   \delta\varphi'=\varkappa'\delta s'-\varkappa\delta s-\delta\varphi.
   \]
   These produce \(DT_R=-M\), not an unsigned assertion about the physical derivative. Its determinant is \(c/c'\). Scalar signs disappear only when slopes, absolute areas and norms are taken.

2. The actual positive slope map is
   \[
   f(v)=\varkappa'+\frac{c'(\varkappa+v)}
                                  {\tau(\varkappa+v)+c}.
   \]
   On \([a,K]\), with \(a=100/47\), \(K=170/9\), it maps into the same interval and has derivative at most \(47/48\). This follows from \((b+c)^2-4bc=(b-c)^2\); it does not require a positive lower incidence. Nested transported intervals construct the measurable invariant unstable line. True time reversal \(I(s,\varphi)=(s,-\varphi)\) constructs the stable line.

3. Their angle sine lies in \([2a/19^2,1]\). Weighted horizontal growth is \(c_m|\delta s_m|\ge(59/47)^m c_0|\delta s_0|\). Taking areas of the two actual invariant unit vectors gives exactly
   \[
   u_mj_m e_m/e_0=c_0/c_m.
   \]
   Consequently \(j_m\le19\,e_{\min}^{-1}(47/59)^m\). Reversal gives backward contraction of the unstable line. This proves that the constructed lines are the true contracting directions, without importing an ergodic or pressure theorem.

## Comparison of columns and the optical cocycle

For the columns of the first positive matrix, both component ratios lie in \([a,K]\). Left multiplication by every later positive matrix preserves \(aC_2\le C_1\le KC_2\). The last column lies in the same slope cone. Thus the complete product has
\[
 (2a/19)b_m\le u_m\le2K(19)b_m.
\]
There is one initial comparison and one terminal norm conversion. There is no factor \(C^m\).

At fixed \(\alpha_0\), the original coordinate changes give \(d\varphi_0=dp_0/c_0\) and \(d\alpha_m=ds_m/R\), hence \(\omega=Rc_0/b_m\). The exact conjugacy
\[
 B_{i+1}M_iB_i^{-1}=C_{i+1}S_i,\quad
 B_i=\begin{pmatrix}c_i&0\\\varkappa_i&1\end{pmatrix},\quad
 C_i=\begin{pmatrix}1&0\\2\varkappa_i/c_i&1\end{pmatrix}
\]
telescopes all intermediate coordinate changes and gives \(b_m=\mathfrak b_m/c_m\). This is the original optical denominator with its internal collision factors. For one flight \(\mathfrak b_1=\tau_0\). Exactly one radius factor remains.

The area identity now gives
\[
 \frac{\omega}{c_mj_m}
       =R\,\frac{u_m}{b_m}\frac{e_m}{e_0}.
\]
The rational enclosures actually checked are
\[
 \frac{19^3}{4R_-a^2}=\frac{15151531}{18000}<30000,\quad
 \frac{R_+K19^3}{a}=\frac{257576027}{9000}<30000,
\]
\[
 \frac{19^3}{4\tau_-a^2}=\frac{15151531}{2400}<6400.
\]
The one-flight lower bound on \(c_1u_1\) cancels the remaining inverse incidence in \(j_1/c_0\).

## Null sets and the pressure interface

At each fixed radius the regular first-collision partition has null singular curves. Nonzero local Jacobians and countable regular charts preserve nullity under forward and backward iterates. Thus the two-sided regular set has full collision measure. Its removal changes no positive finite-record bulk pushforward. This does not erase a singular paired endpoint trace. No common null set over uncountably many radii is required by the actual order \(\sup_R\operatorname*{ess\,sup}_t\).

Module 313 completes the two optical assertions of Input **input:v112-geometric-pressure**, with \(C_0=30000\), \(C_1=6400\). The separate whole-cylinder bound
\[
 \sup_{R,l}\sum_{w\in\mathcal W_l(R)}
                     \sup_{[w]_R\cap M_R'}j_l\le Q_*
\]
is still a premise. Historical 238 is not called a newly discovered growth theorem. The new guarded pressure corollary in module 312 uses the reverse optical inequality and the proved tube-volume bound; it retains its guard and endpoint cap.

## Actual finite verification

The exact checker uses rational arithmetic and symbolic identities, and raises exceptions rather than relying on assertions. Its 12 matrix-product stress cases include incidences as small as \(10^{-20}\), but are coefficient algebra, not claimed physical trajectory samples. It checks determinants, cone maps, derivative identities, original-coordinate conjugacy, telescope identities and nonaccumulating column bounds. The proof of the infinite-time and full-word statements remains the native proof above.

Actual normal and optimized Python executions are recorded in **optical-verification/RUN_RECEIPT.json**, with command, interpreter, times, exit status and actual output hashes. Both runs completed successfully, with identical standard output and identical detail files. The detailed output records the exact native-source SHA-256. The earlier CHECK_EXPLICIT_OPTICAL.normal.json is a retained earlier-draft run; the final executed source identity is the one in the paired optical-verification files.
