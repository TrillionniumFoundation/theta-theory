#!/usr/bin/env python3
"""Rebuild the R75 author dependency maps from the actual native index.

This reads THEOREM_INDEX.json; it neither compiles TeX nor proves mathematics.
The 197 R74 proof records remain unchanged except for their current locators
and the descriptive locator identity. Author-declared logical premises are
kept separate from mechanically extracted LaTeX references.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
from verify import active_tex, without_comments

ROOT = Path(__file__).resolve().parent
OLD_LEDGER = "inputs/r74/THEOREM_DEPENDENCIES.json"
OLD_LEDGER_SHA256 = "cad130e049156e6c77dc4b447e915ff2d0f38549e6e89456ef51f637a8bae6b9"
BASE_SOURCE = "29b999abf11c43709e64be58765aa1984d13ac91"
BASE_PUBLICATION = "c2c05ee3dccd23588790cd92d2aa2b0b3dac00e0"
REVIEW_COMMIT = "358481b21ceeeedb1205ebd30f86982e32a2cb04"
EXPECTED_INHERITED, EXPECTED_NEW, EXPECTED_CURRENT = 197, 12, 209
NEW_SOURCES = ["sections/42-nonabelian-memory.tex",
               "sections/43-stationary-initialization.tex",
               "sections/44-noisy-instruments.tex",
               "supplement-r75-conditional.tex"]

DECLARATIONS = [
    {
        "label": "lem:r75-fourier-multiplicity", "kind": "lemma",
        "title": "Fourier multiplicity and real descent",
        "source": NEW_SOURCES[0], "document": "main",
        "hypotheses": [
            "A finite group G, a finite nonempty output set C, and a probability table b:G->Delta(C); the action on the table need not be faithful.",
            "All output Fourier matrices are stacked vertically, and V_b is the real cyclic span of the left translates.",
            "For the descent assertion, U and V are arbitrary finite-dimensional real G-modules."
        ],
        "conclusion": "The multiplicity of rho in V_b complexified is rank A_rho(b); the trivial multiplicity is one. A real equivariant injection exists exactly when all complex irreducible multiplicities are dominated, including complex and quaternionic real types.",
        "direct_dependencies": [],
        "inherited_mechanisms": [],
        "supporting_definition_labels": ["eq:r75-fourier-block"],
        "internal_load_bearing_facts": [],
        "proof": "Classical Fourier decomposition identifies the rho cyclic block with {A_rho M}, which has rank(A_rho) row copies. A complex injection A+iB descends because a nonzero maximal minor of A+zB is a real polynomial nonzero at i and therefore at some real z; the degree bound gives a finite candidate list.",
        "classical_ingredients": ["Complete reducibility and finite group-algebra decomposition", "Matrix-coefficient orthogonality", "A nonzero polynomial has finitely many roots"],
        "priority_keys": ["Serre77"],
        "claim_class": "Classical representation-theoretic mechanism stated and proved in the precise multi-output conventions required here; not a claim to invent Fourier decomposition or real descent.",
        "limits": "A linear multiplicity criterion alone is not a positive factorization. The next theorem separately proves stochastic positivity."
    },
    {
        "label": "thm:r75-orbit-multiplicity", "kind": "theorem",
        "title": "Exact orbit multiplicity at small contrast",
        "source": NEW_SOURCES[0], "document": "main",
        "hypotheses": [
            "Finite G and C, b:G->Delta(C), group mean pi, and b_t=pi+t(b-pi), 0<=t<=1.",
            "For the restricted count, a prescribed subgroup H and disjoint copies of H\\G; missing active irreducible types give infinite copy number.",
            "For the unrestricted cover, one representative of every subgroup conjugacy class; the pure-start formula is applied only when G is the observable group."
        ],
        "conclusion": "For every positive contrast, q_H(b_t)>=max_rho ceil(r_rho/m_rho(H)); this is attained on an explicit positive interval whenever finite. The integer multiplicity cover gives the exact permutation-module minimum and the unrestricted positive core at sufficiently small positive contrast.",
        "direct_dependencies": ["lem:r75-fourier-multiplicity", "thm:r73-memory-formula"],
        "inherited_mechanisms": ["thm:r74-low-contrast", "eq:r73-module-bounds"],
        "supporting_definition_labels": ["eq:r75-copy-number", "eq:r75-multiplicity-cover"],
        "internal_load_bearing_facts": [],
        "proof": "Semisimplicity embeds the response subquotient in every realizing permutation module. Frobenius reciprocity counts each coset orbit. A real embedding of the centered response, invariant orthogonal projection, a uniform preparation perturbation, and a bounded decoder perturbation give the matching positive factorization on any prescribed adequate action. Zero-mean output columns are restored as zero columns.",
        "classical_ingredients": ["Frobenius reciprocity", "Invariant inner products and complete reducibility", "Finite integer covering", "Positivity by mixing with a strictly positive average"],
        "priority_keys": ["Serre77", "GPT13", "KPT10", "BocciCarliniRapallo11"],
        "claim_class": "Exact action-restricted resource count and its unrestricted multiplicity-cover form. The positivity mechanism extends the retained R74 construction and is reproduced explicitly.",
        "limits": "Small positive contrast only for matching general synthesis; q_H is not kappa/[G:H] in general. At t=0 one copy suffices. No arbitrary full-contrast nonnormal-group LP is asserted."
    },
    {
        "label": "thm:r75-normality-convexity", "kind": "theorem",
        "title": "Normality is the exact single-orbit convexity boundary",
        "source": NEW_SOURCES[0], "document": "main",
        "hypotheses": ["A finite group G, subgroup H, and transitive right action X=H\\G of degree d.", "Binary terminal responses on exactly this one orbit, with arbitrary probability preparation and stochastic decoder; no additional hidden orbit or mixture label is supplied."],
        "conclusion": "The binary single-orbit response set is convex exactly when H is normal. In the nonnormal case the averaged return character witnesses failure at every positive contrast; an irreducible block with 0<m_rho(H)<d_rho gives sup-norm distance at least t*m_rho(H)/(d*d_rho).",
        "direct_dependencies": ["lem:r75-fourier-multiplicity"],
        "inherited_mechanisms": ["lem:r74-normal-orbits"],
        "supporting_definition_labels": [],
        "internal_load_bearing_facts": ["eq:r75-nonconvexity-margin"],
        "proof": "Normal H gives exactly all H-invariant probability tables by a point preparation. If H is nonnormal, its group-algebra averaging projection is noncentral, so some irreducible fixed-space rank is strictly between zero and full degree. The normalized permutation character has a full scalar Fourier block there, which a single orbit cannot carry. A kernel vector of every competing rank-deficient block yields the quantitative margin.",
        "classical_ingredients": ["Centrality of the subgroup average iff the subgroup is normal", "Permutation characters and Frobenius reciprocity", "Operator-norm separation from rank-deficient matrices"],
        "priority_keys": ["Serre77"],
        "claim_class": "Necessary and sufficient convexity classification for a fixed transitive probability-response action, with an explicit positive-contrast obstruction.",
        "limits": "The displayed distance is a rigorous lower bound, not a claimed sharp distance for all actions. The result concerns the specified action and does not preclude other formulations or larger positive cores."
    },
    {
        "label": "lem:r75-return-rigidity", "kind": "lemma",
        "title": "Full-contrast return-law rigidity",
        "source": NEW_SOURCES[0], "document": "main",
        "hypotheses": ["A finite mixture of positive-weight components on copies of one fixed transitive d-point G-action X, with probability preparations and scalar decoders in [0,1].", "The mixed response has value one at the identity and uniform group average 1/d."],
        "conclusion": "Each active component has a point preparation and the matching point-indicator decoder, hence is a pure return law.",
        "direct_dependencies": [], "inherited_mechanisms": [],
        "supporting_definition_labels": [], "internal_load_bearing_facts": [],
        "proof": "Identity value one forces each decoder to equal one throughout its preparation support. Transitivity makes its group average the decoder average, at least 1/d. Equality of the mixture average forces support size one and zeros off that point in each active component.",
        "classical_ingredients": ["Equality in a convex combination of numbers bounded by one", "Uniform averaging on a transitive action"],
        "priority_keys": [],
        "claim_class": "Elementary equality lemma used to certify the full-contrast endpoint; no separate broad novelty claim.",
        "limits": "The common orbit degree and positive mixture weights are essential. The symmetric-group theorem separately excludes other orbit types before applying it."
    },
    {
        "label": "lem:r75-singular-coefficient", "kind": "lemma",
        "title": "A sharp singular-coefficient bound and its equality case",
        "source": NEW_SOURCES[0], "document": "main",
        "hypotheses": ["n>=5, t>0, and P=I-11^T/n.", "A is a real entrywise nonnegative n by n matrix with rank(A)<n, total entry sum one, and PAP=(t/n)P.", "No symmetry or positive-semidefiniteness of A is assumed."],
        "conclusion": "t<=(sqrt(n)-1)/(sqrt(n)+1). Equality holds precisely, up to simultaneous row/column permutation, for A_*=(n-1)^(-1) sum_{i<n} ell_i^T ell_i, ell_i=(1-1/sqrt(n))e_i+(1/sqrt(n))e_n; extremal symmetry is forced.",
        "direct_dependencies": [], "inherited_mechanisms": [],
        "supporting_definition_labels": [],
        "internal_load_bearing_facts": ["eq:r75-null-vector-form", "eq:r75-null-sum-bound", "eq:r75-extremal-coefficient"],
        "proof": "A normalized left null vector gives A=(t/n)(I+c1^T-1v^T), v.c=0 and sum(c)=1/t. Entrywise positivity yields lower bounds controlled by the largest, second largest and most negative v coordinates. A strictly concave one-variable bound reduces to two endpoints; AM-GM gives the sharp constant. Equality forces one negative null coordinate and a unique slack support, hence A_*. Orthogonal centered probability rows prove attainment.",
        "classical_ingredients": ["Rank-one row/column decomposition under centering", "Left null vectors", "A concave quadratic attains its minimum at an endpoint", "Arithmetic-geometric mean inequality"],
        "priority_keys": [],
        "claim_class": "Sharp inequality and complete equality classification proved in this revision for a nonsymmetric nonnegative singular-matrix class. This is an author claim with a full elementary proof, not an exhaustive priority certificate.",
        "limits": "The stated dimension restriction n>=5 is used in strict equality separation; no extension of this uniqueness assertion to n<=4 is claimed. The lemma does not assume or classify a chosen hidden implementation."
    },
    {
        "label": "thm:r75-symmetric-return", "kind": "theorem",
        "title": "The exact two-level nonabelian memory law",
        "source": NEW_SOURCES[0], "document": "main",
        "hypotheses": ["n>=5 and binary S_n response beta_t(g)=(1-t)/n+t*chi_n(g)/n for 0<=t<=1.", "For positive contrast, arbitrary finite exact stochastic controllers under the retained prepared-response interface; all finite G-set orbit types are permitted in the positive-core reduction.", "The equality classification concerns minimum permutation cores at the attained threshold, not all unreduced stochastic implementations."],
        "conclusion": "For t>0, observable group S_n, residual count n!, dimension 1+(n-1)^2 and module bound n(n-1). With tau=(sqrt(n)-1)/(sqrt(n)+1), kappa is n(n-1) on 0<t<=tau and n^2 above; pure memory adds one. At tau every minimum core has n-1 natural orbits and precisely the stated ell_i preparations and D_i=ell_i/((n-1)w_i), with sum(w_i)=1 and w_i>=(1-1/sqrt(n))/(n-1). At t=0 both minima are one.",
        "direct_dependencies": ["lem:r75-fourier-multiplicity", "lem:r75-return-rigidity", "lem:r75-singular-coefficient", "thm:r73-memory-formula"],
        "inherited_mechanisms": ["thm:r73-normal-form", "thm:r74-contrast-thresholds"],
        "supporting_definition_labels": ["eq:r75-symmetric-return"],
        "internal_load_bearing_facts": ["eq:r75-index-estimate", "eq:r75-index-extra", "eq:r75-threshold-factorizations"],
        "proof": "The full standard Fourier block fixes the observable invariants. Counting natural point-orbits of every subgroup gives the unrestricted index lower and a strict penalty for nonnatural standard carriers. Any core below n^2 therefore has exactly n-1 natural carriers; all extra-orbit contributions are constant and can be absorbed into their decoders. Its coefficient matrix is nonnegative singular with PAP=(t/n)P, so the sharp lemma gives the exact lower. A_* gives the threshold controller and decoder mixing all smaller contrasts; n natural return orbits give the upper above threshold. Nonnegative rank-one support/ratio rigidity classifies every minimum threshold factorization. The retained pure-start formula completes the count.",
        "classical_ingredients": ["Standard representation of S_n and character orthogonality", "Subgroup index and factorial-product bounds", "Nonnegative rank-one factorization support", "Permutation-sum row/column swaps"],
        "priority_keys": ["Serre77", "BocciCarliniRapallo11"],
        "claim_class": "Exact all-contrast resource law, matching constructions and endpoint rigidity for an unbounded nonabelian family. The rational low-contrast and full-contrast arguments are retained as additional explicit results.",
        "limits": "The equality classification stops at the permutation-core level. The two-command prepared quantum realization proves physical availability, not minimal Hilbert dimension or a common-resource quantum advantage. The relative gap tends to one. No A1/A2 or full Theta-pipeline completion follows."
    },
    {
        "label": "thm:r75-stationary-initializer", "kind": "theorem",
        "title": "Stationary initialization law",
        "source": NEW_SOURCES[1], "document": "main",
        "hypotheses": ["A nonempty finite command alphabet with finite report sets and an observable response predictively stationary under a full-support command mixture.", "All future-word stationarity equalities are required; when terminal decoders are part of the experiment, all word/readout identities include the empty word.", "Mixed and pure minima use arbitrary real nonnegative edge-emitting tables, with a prescribed pure initial label counted; no irreducibility or minimal linear-state assumption."],
        "conclusion": "The minima are both one for a one-label response, and otherwise n_pure=n_mix+1, with infinity+1=infinity. A stationary hidden row for the averaged command can be chosen without enlarging a mixed realization.",
        "direct_dependencies": [], "inherited_mechanisms": [],
        "supporting_definition_labels": ["eq:r75-predictive-stationarity", "eq:r75-terminal-stationarity"],
        "internal_load_bearing_facts": ["eq:r75-initial-functional-identity", "eq:r75-elimination-tables"],
        "proof": "Predictive stationarity writes the initial future function as a convex combination of hidden future functions. Unless the one-label exception holds, eliminate the initial label and redirect every transition into it using the same normalized coefficients; induction includes zero-length terminal readout. Conversely one counted initializer executes the first actual command into any mixed core. Cesaro averaging preserves every future response and supplies a stationary averaged-command hidden row.",
        "classical_ingredients": ["Positive realizations and future-response functions", "Convex elimination", "Cesaro averaging of finite stochastic matrices"],
        "priority_keys": ["Heller65", "MonrasWinter14", "MonrasWinter16"],
        "claim_class": "A general exact relation between two initialization conventions in the classical positive-realization framework; neither that framework nor stationarity itself is newly claimed.",
        "limits": "Full-support observable stationarity and all terminal quantifiers are material. This is an edge-emitting process theorem. External policy memory, coefficient bit length and exact sampling cost are separate."
    },
    {
        "label": "cor:r75-stationary-process", "kind": "corollary",
        "title": "Stationary processes",
        "source": NEW_SOURCES[1], "document": "main",
        "hypotheses": ["An ordinary stationary finite-alphabet process that is not i.i.d.", "Edge-emitting HMM realizations, with freely mixed initialization compared to a counted prescribed pure label."],
        "conclusion": "The minimum pure-start HMM has exactly one more label than the minimum mixed-start HMM, with the infinite-value convention.",
        "direct_dependencies": ["thm:r75-stationary-initializer"],
        "inherited_mechanisms": ["thm:r74-depolarizing-obstruction"],
        "supporting_definition_labels": [], "internal_load_bearing_facts": [],
        "proof": "Specialize the general controlled initialization theorem to one command. The same-source Cesaro argument identifies the freely mixed convention with a stationary hidden-row convention.",
        "classical_ingredients": ["One-command specialization of observable stationarity"],
        "priority_keys": ["Heller65", "MonrasWinter16"],
        "claim_class": "A corollary of the general R75 initialization theorem; the previous q/q+1 example is an application, not a premise needed for this proof.",
        "limits": "Not a new solution of the unrestricted minimum positive-state realization problem, and not a claim for a different state-emitting model convention."
    },
    {
        "label": "lem:r75-noisy-physical", "kind": "lemma",
        "title": "Physical margins and predictive rank",
        "source": NEW_SOURCES[2], "document": "main",
        "hypotheses": ["The displayed complete three-report qubit instrument, retention parameter 0<=alpha<=1 and any real angle theta; initial state I/2.", "For rank three, alpha>0 and sin(theta)!=0; the zero-retention endpoint is handled separately."],
        "conclusion": "All branches are completely positive with the displayed report floors, sum exactly to depolarization, and give fixed-command stationarity and one-dependence. The explicit cylinder has three independent modes and predictive rank three at nonreal positive retention, and rank two at zero retention; the response is never one-label.",
        "direct_dependencies": [],
        "inherited_mechanisms": ["thm:r74-depolarizing-obstruction"],
        "supporting_definition_labels": ["eq:r75-noisy-instrument"],
        "internal_load_bearing_facts": ["eq:r75-noisy-cylinder"],
        "proof": "Choi-matrix norm bounds give a positive I/16 margin for the complement branch. The rank-one report resets to tau, allowing direct iteration of the damped rotation and the cylinder formula. A nonzero Vandermonde minor gives rank three; the zero-retention two-by-two Hankel minor gives rank two, with a matching two-dimensional reachable diagonal space.",
        "classical_ingredients": ["Choi positivity", "Vandermonde independence", "Finite response/Hankel rank"],
        "priority_keys": ["Fanizza24", "MonrasWinter16"],
        "claim_class": "Physical and rank verification for this complete damped family, extending the retained undamped example. Low-rank non-HMM phase mechanisms and one-dependent examples have prior antecedents.",
        "limits": "Fixed-command stationarity and one-dependence are not claims about feedback-controlled records. The pure-reset branch violates the R68 every-posterior interior hypothesis at every block length, so that theorem is not being applied here."
    },
    {
        "label": "lem:r75-full-instrument-bounds", "kind": "lemma",
        "title": "Relative cylinder obstruction and polygon realization",
        "source": NEW_SOURCES[2], "document": "main",
        "hypotheses": ["The complete instrument of the preceding lemma; alpha>0 and sin(theta)!=0 for the arbitrary-HMM lower.", "For the upper, a regular q-gon of actual pure qubit states, q>=3, with a reset vertex and alpha*exp(i*theta) in that polygon; the same condition may hold for a whole command family."],
        "conclusion": "Every M-label mixed realization forces alpha*exp(i*theta) into the M-state stochastic eigenvalue region. Conversely the polygon supplies an exact q-label realization of all report branches, word states, terminal POVMs and common adaptive policies, using one dictionary for all eligible commands.",
        "direct_dependencies": ["lem:r75-noisy-physical", "prop:r70-relative-spectrum"],
        "inherited_mechanisms": ["lem:r70-core"],
        "supporting_definition_labels": ["eq:r75-noisy-instrument", "eq:r75-noisy-cylinder"],
        "internal_load_bearing_facts": ["eq:r75-cylinder-spectrum"],
        "proof": "Positive entrance/exit paths bound the productive zero-report core by C*8^(-n). Cayley-Hamilton forces the observed nonreal eigenvalue into a productive irreducible block; Perron normalization there and a stationary-row contraction yield the exact normalized stochastic eigenvalue. For the upper, branch zero preserves the polygon, branch one resets to its vertex and branch two has normalized Bloch norm at most 5/11, inside every eligible polygon. Barycentric branch interpolation proves the full subnormalized-state identities.",
        "classical_ingredients": ["Perron-Frobenius normalization on one irreducible block", "Cayley-Hamilton", "Invariant physical-state dictionaries and barycentric interpolation"],
        "priority_keys": ["Fanizza24", "MonrasWinter16"],
        "claim_class": "A matched necessary spectral obstruction and sufficient complete-instrument construction; the relative-spectrum mechanism is inherited and its reducible-core proof is explicitly carried through here.",
        "limits": "The entire stochastic eigenvalue region is only a necessary condition, not proved sufficient for arbitrary full instruments. The upper is restricted to the actual invariant polygon and its qualifying angle family."
    },
    {
        "label": "thm:r75-noisy-memory", "kind": "theorem",
        "title": "Sharp noisy-instrument memory",
        "source": NEW_SOURCES[2], "document": "main",
        "hypotheses": ["The displayed complete noisy qubit instrument; first sector M>=3, 0<theta<=2*pi/M, 0<alpha<=1.", "For the common all-angle count, 0<alpha<1; a finite alphabet has the same upper and a matching lower when it contains a worst phase.", "Pure-start counts use the stationary-response theorem; zero-retention and undamped endpoints are stated separately."],
        "conclusion": "Exact first-sector mixed feasibility alpha<=1/(cos(theta)+sin(theta)tan(pi/M)), with exact M/M+1 counts and zero-report lazy-cycle Perron rigidity at equality. The simultaneous all-angle mixed optimum is K=max(3,ceil(pi/arccos(alpha))), with pure optimum K+1. At alpha=0 the counts are 2/3; at alpha=1 the full family is infinite, with inherited fixed-phase finite/infinite alternatives.",
        "direct_dependencies": ["lem:r75-noisy-physical", "lem:r75-full-instrument-bounds", "lem:r69-sector", "thm:r75-stationary-initializer", "thm:r74-depolarizing-obstruction"],
        "inherited_mechanisms": ["thm:r69-sector-phase", "thm:r69-worst-phase"],
        "supporting_definition_labels": ["eq:r75-noisy-instrument"],
        "internal_load_bearing_facts": ["eq:r75-first-sector", "eq:r75-universal-count", "eq:r75-zero-damping-tables"],
        "proof": "The necessary spectrum and actual polygon upper meet on the classical first-sector chord. Strict smaller-size sector exclusion forces the full carrying block, and applying the sector bound before radial contraction fixes its Perron root at 1/8 and the normalized lazy cycle. A polygon containing the whole radius-alpha disk gives one all-command dictionary; one critical phase gives its matching lower. Explicit two-state rational branch tables settle zero retention. The general initializer theorem gives every pure charge.",
        "classical_ingredients": ["Classical stochastic sector inequality and boundary equality case", "Regular-polygon inradius", "Perron normalization"],
        "priority_keys": ["DmitrievDynkin46", "JohnsonPaparella17", "KirklandSmigoc22", "Fanizza24"],
        "claim_class": "Exact complete-instrument and simultaneous-command realization results using inherited spectral geometry. The sector curve and inverse-square-root worst-phase exponent are not claimed as new classical spectral discoveries.",
        "limits": "Rigidity is for the zero-report matrix up to diagonal similarity, cyclic relabeling and orientation; the other branches are not uniquely classified. No full fixed-angle formula outside the proved regimes is claimed. The R71 arithmetic lift is inherited reasoning, not a new number-theoretic theorem."
    },
    {
        "label": "thm:r75-stopped-approximation", "kind": "theorem",
        "title": "Stopped-law approximation from conditional damping",
        "source": NEW_SOURCES[3], "document": "supplement",
        "hypotheses": ["A finite angle command alphabet, initial qubit I/2 and target retention alpha=1.", "One class of common randomized command/stopping/terminal-POVM policies, each with target expected calls E_1^pi(tau)<=B<infinity; no external quantum register entangled with the qubit.", "One approximate model with retention 1-epsilon, 0<epsilon<1, is chosen independently of the policy; the epsilon=1 and B=0 cases are explicit."],
        "conclusion": "Uniform complete stopped-law total variation, including the nontermination atom, is at most epsilon*B/8. The stronger terminal classical-quantum trace-distance estimate holds with a scalar nontermination block. Pure memory at tolerance delta is at most 1+max(3,ceil(pi/arccos(1-8*delta/B)))=(pi/4)*sqrt(B/delta)+O(1) in the stated regime; an L-label policy adds the explicit product-core account.",
        "direct_dependencies": ["thm:r75-noisy-memory", "lem:r75-full-instrument-bounds"],
        "inherited_mechanisms": [],
        "supporting_definition_labels": ["eq:r75-noisy-instrument"],
        "internal_load_bearing_facts": ["eq:r75-instrument-distance", "eq:r75-capped-distance"],
        "proof": "The two opposite branch perturbations have one-call flagged trace distance at most epsilon*tr(X)/8 for a positive single-qubit input. Finite-horizon telescoping keeps every changed-call prefix entirely target, weighting error by target survival probabilities. Common positive trace-preserving tails contract the difference. Retaining all finite stopped blocks and merging unfinished histories into a scalar block yields the infinite-horizon limit, including nontermination. The exact noisy dictionary and initializer provide the memory upper.",
        "classical_ingredients": ["Trace-norm contraction of positive trace-preserving maps on Hermitian inputs", "Hybrid telescoping", "Tail-sum formula for expected stopping time", "Monotone limits of stopped blocks"],
        "priority_keys": [],
        "claim_class": "A uniform bounded-target-cost implementation upper for the complete controlled stopped experiment, with a counted memory construction; not a new generic telescoping principle.",
        "limits": "The budget is under the target, not the approximation. The latter may have nontermination mass and unbounded expected cost. No matching approximation lower or optimal exponent is proved, and the one-call constant excludes an entangled external quantum register."
    }
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical(value: object) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode()


def native_statements(files: list[str]) -> tuple[dict, dict]:
    origins, statements = {}, {}
    pattern = re.compile(r"\\begin\{(theorem|lemma|proposition|corollary|example)\}"
                         r"(?:\[([^\]]*)\])?(.*?)\\end\{\1\}", re.S)
    for relative in files:
        text = without_comments((ROOT / relative).read_text(encoding="utf-8"))
        for label in re.findall(r"\\label\{([^}]+)\}", text):
            require(label not in origins or origins[label] == relative,
                    "Duplicated active label: " + label)
            origins[label] = relative
        for match in pattern.finditer(text):
            labels = re.findall(r"\\label\{((?:thm|lem|prop|cor|ex):[^}]+)\}", match.group(3))
            if not labels:
                continue
            require(len(labels) == 1, "Ambiguous statement labels in " + relative)
            label = labels[0]
            block = match.group(0)
            following = text[match.end():]
            proof = re.match(r"\s*\\begin\{proof\}(?:\[[^\]]*\])?.*?\\end\{proof\}", following, re.S)
            if proof:
                block += proof.group(0)
            references = set()
            for items in re.findall(r"\\(?:eqref|ref|cref|Cref|autoref|nameref)\{([^}]+)\}", block):
                references.update(item.strip() for item in items.split(","))
            statements[label] = {"kind": match.group(1), "title": (match.group(2) or "").strip(),
                                 "source": relative, "references": sorted(references)}
    return origins, statements


def linked_labels(labels: list[str]) -> str:
    return ", ".join("`" + label + "`" for label in labels) or "None; the proof is given directly from the listed hypotheses and classical ingredients."


def build() -> dict[str, bytes]:
    old_bytes = (ROOT / OLD_LEDGER).read_bytes()
    require(sha(old_bytes) == OLD_LEDGER_SHA256, "The exact retained R74 dependency authority changed")
    old = json.loads(old_bytes)
    old_rows = {row["label"]: row for row in old["statements"]}
    require(len(old_rows) == len(old["statements"]) == EXPECTED_INHERITED,
            "Expected all 197 unique R74 records")
    index_bytes = (ROOT / "THEOREM_INDEX.json").read_bytes()
    index = json.loads(index_bytes)
    require(index["schema"] == "theta.r75.compiled-theorem-index.v1", "Need the actual R75 native index")
    rows = {row["label"]: row for row in index["statements"]}
    require(len(rows) == len(index["statements"]) == EXPECTED_CURRENT, "Expected 209 compiled labels")
    require(index["inherited_statement_count"] == EXPECTED_INHERITED and
            index["new_statement_count"] == EXPECTED_NEW, "Wrong compiled inherited/current counts")
    declarations = {row["label"]: copy.deepcopy(row) for row in DECLARATIONS}
    require(len(declarations) == len(DECLARATIONS) == EXPECTED_NEW, "Expected twelve unique declarations")
    require(set(rows) == set(old_rows) | set(declarations) and not set(old_rows) & set(declarations),
            "Compiled current set differs from the 197+12 declared set")
    files = list(dict.fromkeys(active_tex("main") + active_tex("supplement")))
    origins, native = native_statements(files)
    require(set(rows) <= set(native), "A compiled statement has no parsed native body")
    bibkeys = set(re.findall(r"\\bibitem(?:\[[^\]]*\])?\{([^}]+)\}", (ROOT / "references.tex").read_text()))
    new_rows, catalog = [], []
    inherited_hashes = {}
    excluded_locator_fields = {"source", "document", "number", "page", "identity"}
    for locator in index["statements"]:
        label = locator["label"]
        require(origins[label] == locator["source"], "Current source locator mismatch: " + label)
        require(locator["document"] in ("main", "supplement") and locator["page"] > 0 and locator["number"],
                "Invalid actual compiled locator: " + label)
        if label in old_rows:
            record = copy.deepcopy(old_rows[label])
            inherited_hashes[label] = sha(canonical(old_rows[label]))
            for key in ("source", "document", "number", "page"):
                record[key] = locator[key]
            record["identity"] = "Current native R75 compiled locator; exact R74 proof-authority record is retained at inputs/r74/THEOREM_DEPENDENCIES.json."
            record["inherited_from_r74"] = True
            record["retained_r74_record_sha256"] = inherited_hashes[label]
            record["retained_proof_authority"] = {"path": OLD_LEDGER, "label": label, "commit": BASE_SOURCE}
            for key, value in old_rows[label].items():
                if key not in excluded_locator_fields:
                    require(record[key] == value, "An inherited proof-authority field changed: " + label + ":" + key)
        else:
            record = declarations[label]
            require(record["source"] == locator["source"] and record["document"] == locator["document"],
                    "Declared source/document mismatch: " + label)
            for field in ("kind", "title", "source"):
                require(record[field] == native[label][field], "Declared/native " + field + " mismatch: " + label)
            record.update({key: locator[key] for key in ("number", "page")})
            record["inherited_from_r74"] = False
            record["identity"] = "R75 numbered addition; count does not imply mathematical novelty or journal endorsement."
            record["explicit_statement_or_immediate_proof_references"] = [ref for ref in native[label]["references"] if ref in rows]
            record["other_explicit_references"] = [ref for ref in native[label]["references"] if ref not in rows]
            record["reference_extraction_scope"] = "Numbered statement and immediately following proof only; references are not automatically logical premises."
            require(set(record["priority_keys"]) <= bibkeys, "Undefined bibliography priority key: " + label)
            new_rows.append(record)
        for field in ("direct_dependencies", "inherited_mechanisms", "supporting_definition_labels", "internal_load_bearing_facts",
                      "explicit_statement_or_immediate_proof_references", "other_explicit_references"):
            for dependency in record.get(field, []):
                require(dependency in origins, "Undefined active label in " + field + ": " + label + " -> " + dependency)
        catalog.append(record)
    require(sum(row["document"] == "main" for row in new_rows) == 11 and
            sum(row["document"] == "supplement" for row in new_rows) == 1, "Expected eleven main and one supplement additions")
    # Acyclicity is checked for the newly declared logical premises, not for
    # syntactic citations or embedded historical-label ledgers.
    done, visiting = set(), set()
    def visit(label: str) -> None:
        require(label not in visiting, "Cycle among new logical dependencies: " + label)
        if label in done or label not in declarations:
            return
        visiting.add(label)
        for dependency in declarations[label]["direct_dependencies"]:
            visit(dependency)
        visiting.remove(label)
        done.add(label)
    for label in declarations:
        visit(label)
    source_hashes = {name: sha((ROOT / name).read_bytes()) for name in NEW_SOURCES}
    inherited_dependencies = {dependency for row in new_rows
                              for field in ("direct_dependencies", "inherited_mechanisms")
                              for dependency in row[field] if dependency not in declarations}
    authority_hashes = {origins[label]: sha((ROOT / origins[label]).read_bytes()) for label in sorted(inherited_dependencies)}
    checks = {
        "current_compiled_statement_count": EXPECTED_CURRENT,
        "all_inherited_records_retained": EXPECTED_INHERITED,
        "new_declared_statement_count": EXPECTED_NEW,
        "all_inherited_nondisplay_proof_fields_unchanged": True,
        "all_current_label_references_resolve": True,
        "new_logical_dependency_graph_acyclic": True,
        "new_native_titles_kinds_sources_match": True,
        "all_declared_priority_keys_in_bibliography": True,
        "active_tex_file_count": len(files), "active_label_count": len(origins),
        "scope": "Identity, catalog, label and declared dependency consistency; not a proof checker, native build or priority clearance."
    }
    addendum = {
        "schema": "theta.r75.author-dependency-addendum.v1",
        "paper": "General Theta Foundations I",
        "scope": "Twelve current numbered additions: six finite-group/matrix statements, five main controlled-process statements and one supplement approximation theorem. This is an inventory, not twelve claims of new classical theory.",
        "inherited_source_commit": BASE_SOURCE, "inherited_publication_commit": BASE_PUBLICATION,
        "controlling_referee_commit": REVIEW_COMMIT,
        "current_source_identity": "The source hashes below and actual compiled index identify this map. The final source commit is assigned by the publication handshake, not guessed here.",
        "numbered_statement_count": EXPECTED_NEW, "main_statement_count": 11, "supplement_statement_count": 1,
        "retained_dependency_authority": OLD_LEDGER, "retained_dependency_authority_sha256": OLD_LEDGER_SHA256,
        "compiled_index_sha256": sha(index_bytes), "source_sha256": source_hashes,
        "inherited_dependency_source_sha256": authority_hashes,
        "reference_semantics": "direct_dependencies are author-declared logical prerequisites; inherited_mechanisms record reused constructions or contextual authorities, including a proof supplied again in full. Definition and internal-fact labels are distinct. Extracted LaTeX references are syntax only.",
        "statements": new_rows,
        "source_verification": checks,
        "verification_limits": [
            "All proofs are ordinary author mathematics, not proof-assistant certification.",
            "Finite exact and floating diagnostics do not prove universal optimality, infinite-horizon limits or novelty.",
            "The R65 deposited report is not a review or endorsement of R75.",
            "No independent human expert assessment or editorial decision is claimed.",
            "A1, A2 and the wider Theta pipeline are not assumptions silently discharged by these results."
        ]
    }
    full = {
        "schema": "theta.r75.author-dependencies.v1", "paper": "General Theta Foundations I",
        "controlling_predecessor_source_commit": BASE_SOURCE, "base_publication_commit": BASE_PUBLICATION,
        "inherited_statement_count": EXPECTED_INHERITED, "added_statement_count": EXPECTED_NEW,
        "expected_current_statement_count": EXPECTED_CURRENT,
        "compiled_locator": "Actual paired native main/supplement output in THEOREM_INDEX.json; the strict source-bound build must reproduce every locator.",
        "compiled_index_sha256": sha(index_bytes),
        "declared_current_proof_addendum": "provenance/R75_PROOF_DEPENDENCIES.json",
        "retained_dependency_authority": OLD_LEDGER,
        "retained_dependency_authority_sha256": OLD_LEDGER_SHA256,
        "reference_semantics": addendum["reference_semantics"],
        "statements": catalog,
        "inherited_proof_record_sha256": inherited_hashes,
        "historical_dependency_ledgers": copy.deepcopy(old["historical_dependency_ledgers"]),
        "superseded_duplicate_drafts": copy.deepcopy(old["superseded_duplicate_drafts"]),
        "inherited_instrument_authorities": copy.deepcopy(old["inherited_instrument_authorities"]),
        "historical_label_boundary": "Embedded earlier ledgers are preserved historical objects and can contain renamed labels; they are not silently promoted to current graph edges. All current catalog references and all twelve current declarations resolve in active source.",
        "source_verification": checks,
        "research_status": "RESEARCH_STATUS.md",
        "limitations": "Author dependency map, not formal proof checking, independent human assessment, editorial approval or a novelty certificate."
    }
    lines = ["# Theorem and dependency map — General Theta Foundations I, R75", "",
             "The actual paired native index contains **209 statement labels**: all **197 inherited R74 labels** and **12 current additions**, of which eleven are in the main article and one is in the supplement. These include supporting classical and elementary lemmas; the count is not a novelty count. The independent R58 companion retains its separate source and numbering.", "",
             "## Main proof chains and scope", "",
             "| Chain | Mathematical content and boundary |", "|---|---|",
             "| Predictive response → compact reversibility → finite group → stochastic normal form | Inherited R72/R73 structure for arbitrary finite-dimensional compactly reversible responses. The full normal-form proof and pure-start alternatives remain active. |",
             "| Stacked Fourier rank → real descent → orbit multiplicities → positive synthesis | Any finite group and finite output set; exact prescribed-orbit copy counts and integer multiplicity cover at small positive contrast. Classical representation theory is credited. |",
             "| Subgroup averaging → permutation character → rank obstruction | Normality is necessary and sufficient for convexity on one transitive binary-response action; nonnormality has an explicit positive-contrast distance witness. |",
             "| Arbitrary subgroup indices → absorption of extra orbits → singular nonnegative coefficient bound | For every n≥5, the S_n character family has the exact threshold (√n−1)/(√n+1), no intermediate core sizes, matching implementations and complete minimum-core equality classification. |",
             "| Complete future-response stationarity → initial-label elimination | The general exact mixed/pure initialization difference, including terminal readout before any call and the one-label exception. This chain does not assume reversible group dynamics. |",
             "| Complete qubit branches → productive cylinder → block Perron normalization → physical polygon | Arbitrary-controller lower and one simultaneous physical upper meet in the first sector and worst phase; exact boundary and zero-retention counts are stated separately. |",
             "| Single-call trace distance → target-prefix telescoping → stopped-block limit | One finite simulator works uniformly over common adaptive policies with bounded target expected calls, including a nontermination symbol. This is an upper bound with no asserted optimal approximation exponent. |",
             "| R74 contrast / normal-subgroup LP / dual / algebraic synthesis | Retained general and special-model results with their original hypotheses and proof authority. The new nonnormal theory does not mislabel the old restricted LP as unrestricted. |",
             "| Actual-history / performed-law / minimax / reset / rank / geometric chains | All valid historical bodies remain compiled or in their explicitly identified independent companion. They are not all premises of the new core theorems, and none closes A1/A2 or the full Theta pipeline. |", "",
             "[THEOREM_DEPENDENCIES_R75.md](THEOREM_DEPENDENCIES_R75.md) supplies the twelve explicit hypotheses, logical prerequisites, proof mechanisms and limits. `provenance/R75_PROOF_DEPENDENCIES.json` is its structured counterpart. `THEOREM_DEPENDENCIES.json` contains all 209 current catalog entries; `inputs/r74/THEOREM_DEPENDENCIES.json` is the byte-exact 197-entry predecessor authority. The older R74 addendum and embedded historical ledgers remain retained unchanged.", "",
             "Logical prerequisites, reused mechanisms, internal proof facts and syntactically extracted references are separate fields. In particular, a LaTeX citation is not automatically a proof premise. Current catalog references are checked against all active labels, including equations; historical renamed-label objects remain historical.", "",
             "## Actual compiled locators", "",
             "The following document, number, page and source locations are copied from the actual `THEOREM_INDEX.json`, not guessed from source order. `M` means the main article and `S` the current supplement. Moving a retained body changes its locator, not its mathematical authority.", "",
             "| Document | Number | Page | Label | Source | Role |", "|---|---|---:|---|---|---|"]
    for row in catalog:
        role = "Inherited R74 proof authority" if row["inherited_from_r74"] else "R75 numbered addition"
        lines.append(f"| {'M' if row['document']=='main' else 'S'} | {row['number']} | {row['page']} | `{row['label']}` | `{row['source']}` | {role} |")
    lines += ["", "## Identity and validation boundary", "",
              f"The compiled index SHA-256 is `{sha(index_bytes)}`. The retained predecessor dependency-ledger SHA-256 is `{OLD_LEDGER_SHA256}`. The generator checks 197 unchanged inherited proof-authority records, twelve native title/kind/source matches, all current referenced labels, and acyclicity of the new logical dependency graph. It does not perform mathematical proof checking or confer independent referee approval.", "",
              "Reproduce these four maps from the sealed actual index with `python build_theorem_map.py`; check byte identity without writing with `python build_theorem_map.py --check`. A changed native index requires regeneration and a subsequent source seal.", ""]
    detail = ["# R75 theorem dependencies, hypotheses and claim boundaries", "",
              "This is an author dependency addendum for General Theta Foundations I. It keeps the full 197-entry predecessor catalog and its proof authority at `inputs/r74/THEOREM_DEPENDENCIES.json`; the current complete catalog has 209 entries. Eleven of the twelve current additions are in the main article, and the stopped-approximation theorem is in the supplement. A supporting classical lemma is counted as a statement without being claimed as a new classical theorem.", "",
              "## How to read the map", "",
              "**Direct logical prerequisites** are results actually used as premises in the current proof. **Inherited mechanisms and contextual authorities** identify a reused construction, a special case or a related retained theorem, including a mechanism proved again here. Definition labels and internal proof facts are recorded separately. Automatically extracted statement/immediate-proof references in the JSON are syntactic evidence, not a substitute for this mathematical analysis.", "",
              "The compiled locations below are taken from the actual paired native index. The index and current source hashes are pinned in `provenance/R75_PROOF_DEPENDENCIES.json`. The final Git identity is assigned by the source/publication handshake. No unexecuted computation, human review or editorial decision is asserted by this map.", ""]
    for i, row in enumerate(new_rows, 1):
        detail += [f"## {i}. {row['title']}", "",
                   f"**Native locator:** {row['document']}, {row['kind']} {row['number']}, page {row['page']}; `{row['label']}` in `{row['source']}`.", "",
                   "**Hypotheses.** " + " ".join(row["hypotheses"]), "",
                   "**Conclusion.** " + row["conclusion"], "",
                   "**Direct logical prerequisites.** " + linked_labels(row["direct_dependencies"]), "",
                   "**Inherited mechanisms and contextual authorities.** " + (linked_labels(row["inherited_mechanisms"]) if row["inherited_mechanisms"] else "None beyond the classical framework credited below."), "",
                   "**Proof mechanism.** " + row["proof"], "",
                   "**Classical ingredients and priority boundary.** " + "; ".join(row["classical_ingredients"]) + ". " + row["claim_class"], "",
                   "**Limits.** " + row["limits"], ""]
    detail += ["## Retained mathematics and unresolved scope", "",
               "The old R74 dependency records, including the normal-subgroup LP, dual certificates, algebraic synthesis, fixed four-bit model, constructive contraction theorem and undamped instrument theorem, remain unaltered as mathematical authorities. Their actual compiled document/number/page fields are updated in the complete catalog. Every one of the 197 inherited labels remains present. The exact symmetric-group threshold is now proved in closed form; the earlier interim statement that only an attained algebraic threshold was known is superseded by the sharp coefficient lemma, not left as a current open problem.", "",
               "The general full-contrast nonnormal-group synthesis problem, optimal fixed-angle complete-instrument memory outside the proved regimes, sharp approximation lower bounds, common-resource quantum/classical comparisons, unknown-model identification, A1/A2 and the broader Theta pipeline are not solved by these statements. The R71 arithmetic envelope and exponents transferred to the complete instrument are inherited reasoning, not additional new numbered arithmetic theorems.", "",
               "## Evidence categories", "",
               "The written proofs are ordinary author arguments. The author-team AI challenge is a separate source-hashed reading, not independent human refereeing. Finite exact and floating diagnostics test named fixtures and identities; native LaTeX checks source closure and locators. None of these is a formal proof certificate, a priority clearance or an editorial decision. The controlling deposited R65 report has not been reclassified as a review of R75.", "",
               "Regenerate with `python build_theorem_map.py` and check with `python build_theorem_map.py --check`. The process requires the actual 209-entry compiled index, validates every current named dependency, preserves each predecessor proof record, and refuses missing or duplicate labels.", ""]
    return {"THEOREM_DEPENDENCIES.json": canonical(full),
            "provenance/R75_PROOF_DEPENDENCIES.json": canonical(addendum),
            "THEOREM_MAP.md": "\n".join(lines).encode(),
            "THEOREM_DEPENDENCIES_R75.md": "\n".join(detail).encode()}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Require byte-identical generated maps without writing")
    args = parser.parse_args()
    generated = build()
    for name, data in generated.items():
        path = ROOT / name
        if args.check:
            require(path.is_file() and path.read_bytes() == data, "Generated map differs: " + name)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
    print(json.dumps({"status": "PASS", "mode": "check" if args.check else "write",
                      "scope": "Dependency-map identity and consistency, not mathematical proof verification",
                      "inherited": EXPECTED_INHERITED, "added": EXPECTED_NEW, "current": EXPECTED_CURRENT,
                      "outputs": {name: sha(data) for name, data in generated.items()}}, sort_keys=True))


if __name__ == "__main__":
    main()
