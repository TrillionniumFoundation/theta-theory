# Proof and resource ledger — A1 v10

## Principal chain

`lem:binomial-tangent` + strict mixed pairing -> `thm:rank` -> exact history dimension. Complete Hermite positivity + every-prefix Newton attainment -> an attained, minorized flag. The separate bounded-format cover controls the entire reachable image. These yield `thm:intrinsic-checkpoint`, and positive raw updates yield `thm:intrinsic-streaming`.

`prop:exterior-profile` explains the classical finite spectral content; it is not used as a substitute for the attained history law. `lem:prefix-hermite` isolates a classical interpolation fact. Both are attributed to the v9 referee note.

The new chain is `lem:finite-greedy` -> `thm:compact-compiler` -> `lem:finite-moments` -> `thm:digital-intrinsic`. The first step is a classical farthest-first argument with an explicit numerical allowance. The compact-state theorem enumerates feasible grid histories and compiles the transitions, with error accumulated after every update. The finite-moment lemma verifies evaluation from finite data without gap inversion. The intrinsic attainable cover supplies the sharp rate, and its l=1 floor absorbs numerical and command errors.

## Runtime and offline data

Runtime mutable state: one representative index, at most M values with a supplied stage clock. Current command code, current report and an independently revealed query are inputs. No history, raw state vector or oracle is retained. An autonomous clock enlarges the state space by a fixed horizon factor.

Offline data: grid candidate histories, finitely accurate state and output evaluations, and chosen representative histories. These are used only to construct integer transition and dyadic output tables. Approximate state vectors are never treated as reachable posteriors for an online rational update; appended feasible histories supply offline transition evaluations instead.

Read-only program: O(M^(J+1) log(M+1)) bits for fixed J,N. Input precision: log2(M+1)+O(1) places. Oracle running time is not bounded. A supplied finite approximation is distinct from an algorithm that produces approximations for a noncomputable prior.

## Quantifiers

The upper bound holds on every admitted continuous-command/report history and every sufficiently accurate current input name. The lower comparison uses a fixed memoryless input-coding interface and the original independent continuous exploration law. A history-dependent naming rule would be an extra communication channel and is excluded.

The calibration is known; separate tables may be compiled for each calibration and M. The comparison constants are uniform on the fixed compact positive chamber. There is no calibration-blind codebook claim, no uniformity over all priors and no fixed total-program-size claim.

## Preservation

Ten v9 body source files are pinned by their Git blob hashes in `build.py`. The principal retains 42 predecessor named results and all 40 predecessor complete proof blocks. The new document has 49 complete proof blocks. These inventory numbers are not counts of independent new advances.
