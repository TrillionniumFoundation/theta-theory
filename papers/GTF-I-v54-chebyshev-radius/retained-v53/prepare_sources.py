"""Materialize the frozen supplement and revision records before source qualification."""
from __future__ import annotations
import hashlib
import json
import re
import subprocess
from pathlib import Path

HOME=Path(__file__).resolve().parent
BASE='7641901c2ef957542aa50d9918f272ac7a72ca1c'
REVIEW='4b1eb39eacdb741354e8c4faaedb1c3aabb3a14c'
REVIEW_BLOB='eabcb8404c98d5094f6e2d9113c67214bce75c91'
OLD='papers/GTF-I-v52-quantitative-lifts'
REPORT='reviews/general-theta-foundations-i-v52-quantitative-noisy-rigidity-harsh-top4-r34-2026-09-27/REFEREE_REPORT.md'

def gitbytes(ref: str, path: str) -> bytes:
    return subprocess.check_output(['git','show',ref+':'+path],cwd=HOME)

def save(name: str, obj) -> None:
    (HOME/name).write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')

def active(root: Path, name: str, seen: set[str]) -> list[str]:
    if name in seen:
        raise RuntimeError('Repeated or circular input: '+name)
    seen.add(name)
    path=root/name
    out=[name]
    for child in re.findall(r'\\input\{([^}]+)\}',path.read_text()):
        if not child.endswith('.tex'):child+='.tex'
        if Path(child).is_absolute() or '..' in Path(child).parts:
            raise RuntimeError('Input escapes retained source root')
        out.extend(active(root,child,seen))
    return out

def main() -> None:
    manifest=json.loads(gitbytes(BASE,OLD+'/evidence/SOURCE_HASHES.json'))
    target=HOME/'retained-v52';target.mkdir(exist_ok=True)
    for name,digest in manifest.items():
        if Path(name).is_absolute() or '..' in Path(name).parts:
            raise RuntimeError('Invalid frozen source name')
        data=gitbytes(BASE,OLD+'/'+name)
        if hashlib.sha256(data).hexdigest()!=digest:
            raise RuntimeError('Frozen source digest mismatch: '+name)
        dest=target/name;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data)
    inputs=active(target,'main.tex',set())
    labels=[]
    for name in inputs:
        labels.extend(re.findall(r'\\label\{([^}]+)\}',(target/name).read_text()))
    if len(inputs)!=33 or len(set(labels))!=242 or len(labels)!=len(set(labels)):
        raise RuntimeError('Unexpected v52 active input/label inventory')
    report=gitbytes(REVIEW,REPORT)
    blob=hashlib.sha1(b'blob '+str(len(report)).encode()+b'\0'+report).hexdigest()
    if blob!=REVIEW_BLOB:
        raise RuntimeError('Controlling report blob mismatch')
    (HOME/'FROZEN_R34_REPORT.md').write_bytes(report)
    ledger=gitbytes(BASE,'ROUND17_PROOF_DEPENDENCY_LEDGER.md')
    (HOME/'FROZEN_PIPELINE_LEDGER.md').write_bytes(ledger)
    save('PRESERVATION_MANIFEST.json',{
        'schema':'gtf53.preservation/1','predecessor_publication':BASE,
        'review_commit':REVIEW,'review_blob':REVIEW_BLOB,
        'files':manifest,'active_inputs':inputs,'loaded_labels':sorted(labels),
        'policy':'All 59 predecessor native source files retained byte-for-byte; all 33 active inputs and 242 labels recompiled. Original repository paths are unchanged.'})
    save('PROOF_STATUS.json',{
        'schema':'gtf53.proof-status/1','predecessor':BASE,'review':REVIEW,
        'written_proofs':{
            'thm:classification53':'Complete written proof, including continuous readouts, critical equality, and unrestricted narrow-cut occupation.',
            'thm:observable53':'Complete written proof on reachable modulo invisible space; no spanning assumption.',
            'cor:circle53':'Matching critical noise rho/2 with a fair decoder at equality.',
            'prop:torus53':'Exact formula under independent angles in the actual compact closure.',
            'prop:similarity53':'Complete invariant-metric proof for a uniformly bounded group, including inverses.',
            'thm:algebraic53':'Explicit resultant-based finite horizon and occupation bound throughout epsilon<rho/2.',
            'prop:salem53':'Explicit nonrational algebraic unit-circle example and non-torsion proof.',
            'note:conditioning53':'Attained basis-minimal conditioning, exact finite LP computation, and singular-value bound.'},
        'classical_inputs':['closed matrix subgroup theorem','Haar averaging','real Stone-Weierstrass','integer resultant identity','finite linear optimization'],
        'not_claimed':[
            'independent formal proof verification or editorial acceptance',
            'sharp asymptotic width rate for algebraic irrational rotations',
            'effective word-net complexity for arbitrary real compact-group input',
            'execution of the unconditional six-state noise search at N=9216009',
            'general SOS certificate discovery or efficient global width optimization',
            'closure of unrelated model-specific analytic pipeline gates'],
        'qualification':'See source-bound evidence/BUILD_RECEIPT.json; this ledger alone is not a passing test receipt.'})
    (HOME/'README.md').write_text('''# General Theta Foundations I — Revision 53

## Referee reading order

1. `paper.pdf` / `main.tex`: the independently complete main article, **Sharp Noise Thresholds for Stochastic Realizations of Compact Group Experiments**.
2. `RESPONSE_TO_REFEREE.md`: responses to the major r34 requests and all thirty local comments.
3. `COMPANION_NOTES.pdf` / `supplement-notes.tex`: local proof refinements, support-cone geometry, and intrinsic reachable-basis conditioning.
4. `COMPLETE_SUPPLEMENT.pdf` / `retained-v52/main.tex`: the complete preceding mathematical theory, not a selected excerpt.
5. `evidence/BUILD_RECEIPT.json`, `evidence/SOURCE_HASHES.json`, and `evidence/REFEREE_PACKAGE.zip`: actual qualification, source identity, and the portable referee package.

## Central result

For finite continuous binary-mean interfaces on a compact matrix-group closure H with an executable identity command, the critical total-variation error is

`epsilon_c = (1/4) max_{seed,query,component} (maximum mean - minimum mean)`.

Uniformly bounded horizon-specific clocked stochastic width exists **if and only if epsilon >= epsilon_c**, including equality. A single stationary permutation machine attains the boundary. Below it every fixed width has a horizon-independent occupation budget. No spanning, reachability-rank, positive-mass, or conditioning assumption is imposed.

Consequences include the intrinsic observable-quotient exact criterion, the sharp planar threshold rho/2, continuous nonlinear and measure-once unitary readouts, compact similarity, and explicit algebraic-circle width bounds for the whole interval epsilon<rho/2. The rational example rho=1/10, epsilon=1/25 has r=5, Delta=1/150, and A=23364.

## Frozen sources and preservation

Parent publication: `7641901c2ef957542aa50d9918f272ac7a72ca1c` (v52).  
Controlling r34: `4b1eb39eacdb741354e8c4faaedb1c3aabb3a14c`.  
Working branch: `revision/general-theta-foundations-i-v53-component-oscillation-2026-09-27`.  
Publication branch: `revision/general-theta-foundations-i-v53-referee-ready-2026-09-27` (created only after actual qualification).

The complete 59-file validated predecessor source inventory is retained byte-for-byte under `retained-v52/`. Its 33 active LaTeX inputs and all 242 loaded labels are rebuilt. The original v52 paths and all previous revision/review branches remain unchanged. Historical introductions and secondary estimates remain in the complete supplement rather than being silently removed from the deliverable.

## Reproduce

With Python 3.11, SymPy 1.14.0, PyMuPDF 1.26.7, and TeX Live with AMS, Latin Modern, microtype, and TikZ installed, run `python build.py --check-isolated` from this directory. The portable native source archive requires no GitHub access to rebuild. `prepare_sources.py` is only the repository-side materializer for frozen predecessor and report bytes; it is not needed in the already materialized archive.

The proof is written in the manuscript. Exact finite tests and PDF reproducibility do not replace independent mathematical review. The detailed resource and analytic-dependency boundaries are in the article, response, and audit; neither practical six-state noise-search execution nor a general SOS discovery engine is claimed.
''')
    (HOME/'HISTORY_AND_PIPELINE_AUDIT.md').write_text('''# History and pipeline audit — Revision 53

## Frozen evidence

The complete r34 referee report was read in contiguous ranges, including the correctness discussion, novelty/breadth assessment, publication recommendation, required extensions, and all thirty local comments. Its commit is `4b1eb39eacdb741354e8c4faaedb1c3aabb3a14c` and its exact copied blob is checked during source materialization.

The predecessor publication is `7641901c2ef957542aa50d9918f272ac7a72ca1c`. Its source-bound v52 workflow `36298407771`, validated artifact `10924348954`, and native source commit `eb73ed400b3b77aaee8bf52a06a587f8d207d011` supplied the complete predecessor artifact consulted for this revision. The publication tree, not an unpinned branch tip, supplies the retained bytes.

Directly consulted mathematical sources include the active main program, machine model, common-row/Hankel compatibility, word profiles and endpoint contraction, arithmetic scales, reachable lifts, all-width exact rigidity, noisy finite-orbit reduction, effective one-surplus bounds, stable conditioned sections, global certificates, and the rational uniform compiler. The predecessor history, resource, priority, pipeline, and build records were compared with the root Round-Seventeen dependency ledger. The source inventory covers the whole active predecessor article; this does not assert a fresh line-by-line referee audit of every earlier branch or every unrelated analytic manuscript.

## Finite-dimensional derivation chain

```
common stochastic-row compatibility
  -> actual reachable spans and positive sections
  -> exact all-width occupation and finite-group stationarization
  -> finite-orbit/moving-space reduction and executable word contraction (v52)
  -> identity component and finite component quotient (v53)
  -> conditional tensor-polynomial moments (v53)
  -> nonnegative localization at both output extremes (v53)
  -> exact component-oscillation noise boundary and narrow-cut occupation (v53)
```

The new argument reuses and reproves the endpoint mechanism; it does not treat a cutwise nonnegative factorization as a common-row realization. The conditional polynomial step is what allows one query and a partial interface to replace the old full-coordinate calibration. The finite-orbit subspace is identified with the fixed space of the identity component in the companion notes.

The effective branch is

```
explicit harmonic localization
  -> nonzero integer resultant / Gaussian-integer power separation
  -> separated harmonic orbit points
  -> finite executable block defect
  -> explicit full-subcritical algebraic-circle width inequality.
```

The retained geometric and certificate branches remain intact: trace asymmetry -> support cone -> one-surplus expansion; reachable-basis conditioning -> whole-suffix stability; finite exact separation -> terminating algebraic noise search; complete projector residual -> classical global SOS certificates; finite rational group -> priced rational sampling. They are not mislabeled as steps in the new unconditional proof.

## Broader repository DAG

`FROZEN_PIPELINE_LEDGER.md` retains the root ledger as read-only historical evidence. Its chains are

```
A2 -> A3 -> A4 -> C2 -> D1
B2-GC -> B1 -> B2-MC -> B3 -> B4 -> C1 -> C2 -> D1
A1 independent
```

The ledger requires model-derived raw Fourier/density local limits, entropy-controlled stopped LDP, a global past kernel, canonical coefficients and shell conditioning, process CLT and Mosco recovery, nonlinear Nisio/resolvent and graph-core identities, regular filtering and QMD/LAN, strict/form response and changing-filtration projection, and labelled posterior contraction. None is imported as a proved premise of the compact-group article. This revision supplies a finite-dimensional realization result, and assigns no unearned completion credit to those separate analytic gates. No unrelated manuscript or main-branch file is edited.

## Preservation and validation

`PRESERVATION_MANIFEST.json` records all 59 source hashes, the 33 active inputs, and all 242 predecessor labels. The new main article is genuinely independent, while the full earlier theory remains buildable. Validation reruns inherited checks in both normal and optimized Python, checks new exact arithmetic and boundary examples, builds all three PDFs, and compares every text/raster page after a native-source-only isolated rebuild. The actual receipt is authoritative; plans and written proof-status entries are not test passes.
''')
    (HOME/'LITERATURE_AUDIT.md').write_text('''# Targeted literature audit — Revision 53

Primary sources checked on 27 September 2026:

- Alex Brodsky and Nicholas Pippenger, *Characterizations of 1-Way Quantum Finite Automata*, SIAM Journal on Computing 31(5), 1456–1478 (2002), DOI 10.1137/S0097539799353443; author preprint arXiv:quant-ph/9903014. Theorem 3.3 is the bounded-error measure-once/group-language equivalence. Theorem 3.6 preserves cutpoint-language acceptance with a possibly changed cutpoint, not uniform additive preservation of each numerical output probability. The publisher page and primary preprint statements were inspected. The PDF screenshot service failed to render the requested pages; the primary parsed theorem text was available and used, not a visual claim about an unavailable image.
- Vincent D. Blondel, Emmanuel Jeandel, Pascal Koiran, and Natacha Portier, *Decidable and undecidable problems about quantum automata*, SIAM Journal on Computing 34(6), 1464–1473 (2005); primary preprint arXiv:quant-ph/0304082. Section 3 and Theorem 3.1 give the compact semigroup closure/algebraic-invariant route to strict-threshold decision. This is credited as an antecedent, not claimed as a new algorithm.
- Brian C. Hall, *Lie Groups, Lie Algebras, and Representations*, second edition (2015), publisher/author edition record. Used for the standard closed-matrix-subgroup structure; compact Lie groups have finite component groups.
- Gerald B. Folland, *A Course in Abstract Harmonic Analysis*, second edition, Chapman & Hall/CRC (2016 edition citation; publisher copyright listing also says 2015). Used for standard Haar averaging and compact representations.

The retained primary positive-realization literature, including Benvenuti–Farina's 2004 tutorial, and Paz's probabilistic-automata framework remain in the bibliography and complete supplement. The comparison in the main article explicitly separates stationary language recognition, numerical threshold decision, positive realization, and horizon-dependent stochastic numerical approximation. No exhaustive first-in-literature claim is certified by this audit.

External reference locations:

- https://epubs.siam.org/doi/10.1137/S0097539799353443
- https://arxiv.org/abs/quant-ph/9903014
- https://arxiv.org/abs/quant-ph/0304082
- https://sites.nd.edu/brian-hall/lie-groups-lie-algebras-and-representations/
- https://www.routledge.com/A-Course-in-Abstract-Harmonic-Analysis/Folland/p/book/9781032922218

The finite regression suite is not a priority search. Classical results in the supplement (Farkas, Putinar, Lasserre, compactness, and finite algebraic elimination) remain explicitly attributed. The mathematical contribution submitted for independent assessment is the stated component-oscillation theorem with its model quantifiers and the explicit full-subcritical arithmetic consequence.
''')
    notes=HOME/'supplement-notes.tex'
    text=notes.read_text()
    text=text.replace('This corrects only notation: $\\norm\\alpha_1$ means the $\\ell^1$ norm of $\\alpha$, not a row index.',
                      'Here $\\norm\\alpha_1$ denotes the $\\ell^1$ norm of the coefficient row.')
    notes.write_text(text)
    print(json.dumps({'status':'materialized','retained_files':len(manifest),'active_inputs':len(inputs),'retained_labels':len(labels),'review':REVIEW}))

if __name__=='__main__':
    main()
