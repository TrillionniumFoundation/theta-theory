# Proof audit of the proposed nonabelian section

This is an author-side mathematical audit. It is not an independent human referee report, a proof-assistant certificate, or an editorial assessment. The proposed source is `42-nonabelian-memory.tex`; the controlling source SHA-256 is recorded in `DEPENDENCY_MAP_R75_NONABELIAN.json` and the executed diagnostic report.

## 1. Multiplicity and positive synthesis

The Fourier transform convention is `hat f(rho)=|G|^-1 sum_g f(g)rho(g^-1)`. Left translation of the function by `h` therefore acts by **right** multiplication of its Fourier block by `rho(h)`. All output blocks must be stacked vertically before taking rank; looking at only the maximum individual output rank would be insufficient in general. The cyclic multiplicity is the rank of the whole stack.

The group-algebra decomposition allows arbitrary matrix blocks independently. If the stacked matrix has rank `r`, its right matrix ideal is isomorphic to `r` rows of length `d_rho`. This proves the multiplicity statement, rather than merely a one-sided rank bound.

Complex multiplicity inequalities do not by themselves describe a probability factorization. There are two separate steps. First, a complex injection `F=A+iB` has a full-size minor whose real polynomial in `A+zB` is nonzero at `z=i`; an integer `z` outside its roots gives a real injection. Second, the retained R74 construction embeds the zero-average real response module, adds a sufficiently small real zero-mass preparation perturbation to the uniform row, and adjusts the decoder around its positive mean. Zero-mean output columns are identically zero and can be restored after construction. This covers real, complex and quaternionic irreducible types without a hidden exclusion.

The trivial Fourier multiplicity is exactly one because the output mean is a nonzero probability vector. Thus the integer cover cannot choose the empty action, and the restricted-copy minimum cannot be zero. Constant tables require one orbit copy and unrestricted core one. The contrast parameter is explicitly restricted to `[0,1]`; all positive-contrast multiplicity conclusions exclude `t=0`.

The fixed-orbit resource `q_H` and unrestricted resource `kappa_G` are kept distinct. The integer cover determines the unrestricted module minimum. Its conversion into positive memory is local in contrast and has a constructive positive endpoint; it does not solve arbitrary full-contrast bilinear positivity.

## 2. Exact normality boundary and robust witness

For normal `H`, preparation absorption produces the full left-`H`-invariant probability polytope. For nonnormal `H`, the averaging idempotent in every irreducible cannot have only zero/full ranks: otherwise every block would be zero or identity, making the group-algebra idempotent central and its support `H` conjugation invariant. This argument establishes a partial irreducible multiplicity for **every** nonnormal subgroup.

The witness is real and probability valued: `chi_X(g)/|X|` is the average of deterministic return indicators. Its active Fourier blocks are scalar identities. They have full rank, exceeding the partial multiplicity available on one orbit. No separate real-type construction is needed for this lower bound. Mixing every return decoder with the same constant shows that the nonconvexity persists arbitrarily close to a strictly interior binary probability table.

For the quantitative margin, any candidate single-orbit block has a kernel vector. The witness block acts as `alpha I` on that vector, giving operator-norm separation at least `alpha=t*m/(d*d_rho)`. Normalized Fourier transformation is contractive from the scalar sup norm to matrix operator norm because the representations are unitary. The resulting bound ranges over all probability preparations and bounded decoders on the orbit. Its constant is not asserted optimal.

The theorem characterizes convexity of this fixed transitive response set. It does not assert that no other linear formulation is possible for any nonnormal group or any specially structured response.

## 3. Full-contrast rigidity

At identity response one, every positive mixture component has identity response one. A `[0,1]` decoder must therefore equal one throughout its preparation support. On a transitive orbit of size `d`, averaging the response over the group gives `sum(D)/d`, hence at least `1/d`. Equality of the mixture mean with `1/d` forces equality in each component and leaves a singleton support and its indicator decoder.

This lemma is applied only after the unrestricted symmetric-group proof has excluded all other positive-mass orbit types. Imposing natural orbits as an initial ansatz would not establish the unrestricted lower bound.

## 4. The all-n symmetric-group lower bound

The standard module is irreducible and faithful by the explicit transposition argument in the text. The character response has a full standard Fourier block, so the observable module has `n-1` copies of the standard module; its dimension is `1+(n-1)^2`, its group is `S_n`, and all `n!` residuals are distinct.

For any subgroup `K`, the standard fixed-space dimension is the number of **natural** `K`-orbits minus one. The product-of-symmetric-groups bound on `|K|` yields the subgroup-index estimates. If there are at least three natural orbits, the multinomial coefficient is bounded below by the concentrated partition value. With two natural orbits, the only degree-`n` standard-carrying case is the full point stabilizer; a proper subgroup costs at least `2n`, and two non-singleton parts cost at least `C(n,2)>=2n`. This last inequality is why `n>=5` is stated.

The proof does not classify all low-index subgroups and does not assume that every index-`n` subgroup is a natural point stabilizer. In particular, it remains valid for `S6`: an exceptional subgroup that is transitive in the specified natural action has standard multiplicity zero. Under a hypothetical core smaller than `n^2`, the multiplicity sum and extra-`n` cost force exactly `n-1` natural carriers; all remaining orbit degrees together are below `n`. Those remaining orbits would raise the group mean strictly above `1/n` at identity response one, so they carry no positive preparation mass. Rigidity then reduces to `n-1` return indicators, while the transposition equations force positive weight at each of the `n` points. This is the contradiction.

The original rational low-contrast decoder on `n-1` natural orbits is retained, including its complete response identity. The full-contrast upper uses `n` natural orbits. For every positive contrast, any factorization below `n^2` again has exactly `n-1` natural carriers. The extra-orbit aggregate has no standard Fourier block, while subtraction from the target shows it has no other nontrivial blocks either. It is a constant nonnegative vector `v_E` of mass `w_E`. Normalizing the natural preparation by `w_N=1-w_E>0` and replacing its decoder by `w_N D+1 v_E` absorbs all extras without adding a label. Thus no intermediate core value occurs. The sharp matrix argument below now computes the transition explicitly as `(sqrt(n)-1)/(sqrt(n)+1)`, with the smaller memory attained at equality. This closes the formerly open threshold; it does not report an executed quantifier-elimination calculation.

The pure-start value follows from the inherited theorem with the computed `N=n!`. For every `n>=5`, `n^2+1<n!`, so the initializer is genuinely charged. The physical realization uses `P_g^T` on column state vectors to match row/chronological multiplication.

## 5. Sharp positivity threshold and equality rigidity

The singular-coefficient lemma is stated for every entrywise nonnegative real matrix `A` with rank below `n`, total entry sum one, and `PAP=(t/n)P`, where `P=I-J/n` and `t>0`. It does not assume that `A` is symmetric, positive semidefinite, or already equipped with a stochastic factorization. The bound is therefore a relaxation valid for every coefficient matrix arising from `n-1` natural orbit copies.

The centered identity implies a scalar identity plus row and column terms. A nonzero left null vector cannot have coordinate sum zero, since multiplying by `P` would then contradict the positive scalar centered block. It can consequently be normalized to sum one. This gives the exact normal form `A=(t/n)(I+c1^T-1v^T)`, with `v dot c=0` and `1=t sum(c)`. The proof separates all nonnegative `v`, including the strictly positive possibility, from vectors with a negative minimum; it does not inadvertently restrict the first case to `min(v)=0`.

For a negative minimum `-m`, the nonnegative entries force `c_1>=max(L,M-1)` and `c_i>=M` for the remaining coordinates, where `M` and `L` are the largest and second-largest coordinates of `v`. The slack's dot product is bounded below by `-m` times its total mass. The normalization of `v` gives `M>=(1+m)/(n-1)` and `L>=(1-M+m)/(n-2)`. Substitution produces a concave quadratic on the resulting interval. Its lower endpoint is `(1+m)(n+1/m)/(n-1)`; its upper endpoint is `n-1+n*m/(n-1)>n-1`. AM–GM gives the sharp constant `(sqrt(n)+1)/(sqrt(n)-1)`. The strict comparison with `n-1` requires `n>4`, matching the theorem's hypothesis.

Equality forces `m=1/sqrt(n)`, the lower concavity endpoint, `n-1` equal positive null-vector entries, and exactly one negative entry. Equality in the slack bound puts all slack at that negative coordinate. These conditions determine the entire coefficient matrix, up to simultaneous coordinate permutation. The resulting matrix is `A*=(n-1)^-1 sum ell_i^T ell_i`, where `ell_i=(1-1/sqrt(n))e_i+(1/sqrt(n))e_n`. Its symmetry is derived rather than assumed. The centered rows `ell_i-1/n` form an orthogonal basis, giving the matching sharp construction directly.

For a hypothetical smaller controller, the unrestricted action argument first reduces it to `n-1` natural orbits. The resulting nonnegative coefficient matrix has rank at most `n-1`. Its entry sum follows from the group mean. Its centered identity follows from comparing permutation sums that interchange two assigned columns; no Fourier orientation ambiguity is hidden in this step. Thus the matrix lemma yields the universal smaller-core exclusion for every `t>tau_n`, and decoder mixing gives every `0<=t<=tau_n`.

At the threshold, the positive diagonal leading block of the unique coefficient matrix forces each of the `n-1` nonnegative rank-one orbit terms to cover exactly one diagonal position. Its zero cross entries force support on `{i,n}`. The two off-diagonal ratios then determine each probability preparation and decoder up to its orbit weight: `lambda_i=ell_i`, `D_i=ell_i/((n-1)w_i)`, `sum(w_i)=1`, `w_i>=(1-1/sqrt(n))/(n-1)`. These weight conditions are necessary and sufficient. In particular, uniform weights are not forced. The classification concerns minimum **permutation-core factorizations**. It does not identify every original stochastic transition realization with that form, nor classify all optimum cores at full contrast.

## 6. Validation and limits

The canonical diagnostic has 95,999 exact rational, integer, algebraic and symbolic identity checks and zero floating checks. The threshold closure added 111 aggregated checks, counted per matrix identity, full specified response table, or parameter sample rather than per matrix entry. The normal and `-O` reports are byte identical, and AST inspection found no removable assertion statements. The pinned execution uses Python 3.12.14 and SymPy 1.14.0.

The retained checks cover explicitly specified finite groups, partition inequalities through `n=30`, controllers, Fourier matrices, residuals, a finite margin grid, constant-extra absorption, and a three-output negative control for using individual ranks instead of the vertical stack. The new checks verify the lower-bound algebra exactly, radical equality matrices for `n=5,6,9,16`, full response tables for `S5` and `S6`, four specified permutations for `S9` and `S16`, uniform and nonuniform equality factorizations, an invalid-weight negative control, and nonsymmetric singular matrices satisfying the relaxed lemma's hypotheses. The diagnostic does not enumerate every larger symmetric-group subgroup or arbitrary controller, and its symbolic simplifications are not proof-assistant certification. The universal assertions depend on the displayed proofs.

Two native `pdflatex` passes of the standalone syntax wrapper completed, producing a ten-page PDF. That wrapper uses explicit placeholders for inherited theorem references; the full manuscript and supplement must be compiled after integration to validate their actual numbering, bibliography and layout. There are no undefined references in the wrapper; a source-local 1.59311pt overfull line remains in its article layout. No full-manuscript build, GitHub CI run, independent specialist approval or publication decision is asserted by this subtask.
