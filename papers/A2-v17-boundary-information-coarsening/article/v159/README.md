# A2 revision 159 — complete referee reading entry

Branch: `revision/a2-v159-intrinsic-boundary-modular-completion-2026-09-25`.

The controlling report is the complete v157 report at `b81ba4a2fac700f17b26163079bd17ef54947509`. The complete reviewed baseline is v157 at `a6d34cd2bb2075c64015f3667dbf3f391665cefd`. We additionally preserve and integrate the v158 derivation sources locked at `61c7a13fa1ce2c65777b9ca7a8e5f6c17dd6ca48`; that tip did not yet contain materialized v158 PDFs. No earlier revision or review branch is overwritten.

## Complete reading objects

| Object | PDF | Independent full source |
|---|---|---|
| I. Finite failure schemes and the reconstruction of quadratic pencils | [reconstruction.pdf](reconstruction.pdf) | [reconstruction.tex](reconstruction.tex) |
| II. Intrinsic power geometry and the boundary of quadratic pencils | [divisor-geometry.pdf](divisor-geometry.pdf) | [divisor-geometry.tex](divisor-geometry.tex) |
| Unified preservation master, not a third submission | [geometry.pdf](geometry.pdf) | [geometry.tex](geometry.tex) |

The root `CURRENT_REVIEW_ENTRY.md` pins the source and publication state. The [build receipt](BUILD_RECEIPT_V159.json) supplies actual source/PDF hashes and page counts. Cross-paper references are embedded in the focused sources; neither requires an external companion `.aux` file.

The [point-by-point response](RESPONSE_TO_V157_REPORT.md) addresses all 24 specific requests. The [literature record](LITERATURE_AUDIT_V159.md) identifies inspected primary statements and the historical comparison which remains unavailable.

## Mathematical reading route

Paper I, Theorem 10.1 and Proposition 11.1, constructs the native source-normalized algebra bundle from the first relation and first jets, before the pencil coefficient line is recovered. Scalar twists cancel; the universal property specifies the rank-one nilpotence quotient. At `h=1` there is no exponent choice. This is a canonical functorial bundle and projective diagram, not an unproved preferred linear subquotient of the failure algebra.

Paper II, Theorems 6.1 and 7.2, realizes every rank graph by relative complete quadrics and recovers both elementary divisors and minimal indices for arbitrary symmetric pencils, together with their global degree conservation law.

Paper II, Theorem 11.3, computes simultaneous ordinary transverse collisions of arbitrary multiplicities, including higher-order perturbations. The graph on the total surface is the blow-up of the collision points. Its fibre is a reduced nodal tree without embedded components. Every tail map is a complete Veronese system of degree

`delta_(a,p) = (p-h(n-c_a))_+ - c_a (p-h(n-1))_+`.

The exact power ideal is `(z_a,tau)^delta_(a,p) (det S_a)^((p-h(n-1))_+)`. In particular one power selects each point centre.

Theorem 11.4 constructs a flat modular family of distinct limits over a fixed semisimple pencil and proves

`dim rho^(-1)(R_0) >= sum_a [binom(c_a+1,2)-2]`.

A triple collision gives a four-dimensional family. The proof uses the finite preimage under normalization, not an invalid lifting claim for a nondominant normal source. These are specified families in an incidence fibre, not a classification of the entire fibre or a proper quotient-stack theorem.

## Preservation and verification

The [preservation record](NONDELETION_V159.json) retains all 352 v157 labels and all 236 v157 mathematical blocks, as well as the entire locked v158 mathematical additions. The v158 intermediate master has 390 labels and 257 blocks. Every body block is allocated exactly once across the focused manuscripts; [PAPER_MAP_V159.json](PAPER_MAP_V159.json) gives that allocation. Replaced front matter is archived in `PREVIOUS_FRONTMATTER_V158.tex`.

[EXACT_CHECKS_V159.json](EXACT_CHECKS_V159.json) records 28 distinct-factor coefficient-space tests, 135 arbitrary-corank tail coefficient-space tests, 21 independent determinant-apolar ideal comparisons, six higher-order Artin-base comparisons and 480 simultaneous-cluster degree profiles. The inherited v158 suite and the earlier suites it invokes are actually executed; the current inherited receipt is [INHERITED_V158_CHECKS_RERUN.json](INHERITED_V158_CHECKS_RERUN.json). The distinct historical 28-check suite is not claimed as rerun. Computations are finite audits, not certificates of the general proofs.

## Reproduce

In this directory in the checked-out branch, with Python 3, SymPy 1.14.0, TeX Live and Poppler:

```sh
python3 check_v159.py
python3 assemble_v159.py --build
```

The assembler verifies all seven locked v158 source hashes, regenerates an intermediate predecessor master from v157 without changing its inputs, and checks that master against its pinned SHA-256. It then emits all three complete sources, compiles the PDFs, stabilizes the companion references and rejects missing labels, undefined references/citations, duplicated labels and horizontal overflows. Only the v159 outputs and root reading entry are published by the branch-specific workflow.

## Documentary scope

The first-jet envelope is an algebra bundle on the intrinsic source, not an untwisted coefficient representation at a point. The ordinary-collision theorem has explicit transverse and semisimplicity hypotheses; the independent all-pencil invariant theorem includes singular pencils. Complete quadrics, invariant-ideal classification, congruence canonical forms and the general multiplier-ideal formulas are credited as classical inputs. The theorem/proof-level Ballico 1993 comparison remains unavailable in both submitted papers. No nonanticipation, formal proof certification or editorial acceptance is inferred from that limitation or from passing finite checks.
