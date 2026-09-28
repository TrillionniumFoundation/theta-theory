#!/usr/bin/env python3
"""Materialize the full analytic-contact revision with exact baseline archives."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
from source_provenance import blob_id, require, write_json
from materialize_revision_v58 import dependency_map as prior_dependency_map

P=Path(__file__).resolve().parents[1]
BASE='92a6d946c98e19c33ebff15997c0116ac158b89d'
REVIEW='464209b66aad6ff48b63f054711396fbfd759b64'
ARCHIVE=P/'history/v58-review-baseline'
NEW='article/23a2_analytic_contact_inverse_v59.tex'
INTRO='journal/00_principal_introduction_v56.tex'
FULL_INTRO='article/00_structural_introduction_v48.tex'
SIGNED='article/23a_signed_endpoint_rigidity_v27.tex'
ROUTES='journal/full_reference_routes_v56.tex'
CHANGES=('main.tex','rigidity.tex',INTRO,FULL_INTRO,SIGNED,ROUTES)

OVERVIEW=r'''The analytic germ problem admits a further conclusion for the complete
nonlinear map, not just its diagonal blocks.  In
Theorem~\ref{thm:v59-analytic-contact-inverse}, the half-line actions
are local analytic coordinates for anchored analytic contact pairs in a
bounded-holomorphic norm on one small fixed disc.  The derivative is
\[
 (D\mathscr S(\psi)\eta)_b(u)
 =\alpha_b(u)\eta_b(u)+
       \sum_{i\ge1}v_{b,i}(u)\eta_{b+i}(x_{b,i}(u)),
       \qquad |x_{b,i}(u)|\le\rho^i|u|,\quad \inf|\alpha_b|>0.
\]
This identity follows from the actual stationary envelope, including its
vanishing terminal term.  The first term is an invertible multiplier;
the remaining evaluations contract high-order vanishing functions.
One finite low-jet system and a norm-convergent tail inverse therefore
control all lower-degree couplings.  A local contraction gives the
nonlinear inverse.  In the induced analytic quotient norms, its complete
linearized finite-jet inverses have bounds independent of the truncation
order.  The analytic norm is an additional hypothesis: it is not inferred
from finitely many density derivatives, total variation, or a finite
sample.  No continuation to an entire obstacle or uniform acquisition
rate is part of this local analytic estimate.
'''


def once(text: str, before: str, after: str) -> str:
    require(text.count(before)==1,'Unexpected edit anchor: '+before)
    return text.replace(before,after,1)


def revised(name: str,text: str)->str:
    if name=='main.tex':
        text=text.replace('A2 revision 58','A2 revision 59')
        return once(text,
            'are bounded uniformly in order at a positive hyperbolic margin.',
            'are bounded uniformly in order at a positive hyperbolic margin.\n'
            'For analytic contact germs, the complete action map is locally\n'
            'biholomorphic in a bounded-holomorphic norm on a small fixed disc;\n'
            'an envelope representation controls its lower-degree couplings.')
    if name=='rigidity.tex':
        text=once(once(text,'A2 v58.','A2 v59.'),'A2 revision 58','A2 revision 59')
        text=once(text, r'\maketitle', r'\maketitle'+'\n'+r'\enlargethispage{2pt}')
        return once(text,
            'identity exponentially under geometric admissibility.',
            'identity exponentially under geometric admissibility.\n'
            'For analytic contact germs, an envelope representation yields a local\n'
            'analytic inverse for the complete action map in a fixed-disc\n'
            'bounded-holomorphic norm, including all lower-degree couplings.')
    if name==INTRO:
        return once(text,'diagonal bounds.\n\nThe density algebra',
                    'diagonal bounds.\n\n'+OVERVIEW+'\nThe density algebra')
    if name==FULL_INTRO:
        return once(text,'\n\\subsection{The observation and the main theorem}',
                    '\n'+OVERVIEW+'\n\\subsection{The observation and the main theorem}')
    if name==SIGNED:
        return text+'\n\\input{article/23a2_analytic_contact_inverse_v59}\n'
    if name==ROUTES:
        return once(once(text,'DEPENDENCY_MAP_V58.json','DEPENDENCY_MAP_V59.json'),'{A2-v58}','{A2-v59}')
    raise RuntimeError('Unprescribed amendment: '+name)


def dependency_map(root: Path=P)->dict:
    out=prior_dependency_map(root)
    out.update(revision=59,baseline_source=BASE,review_head=REVIEW,
               supersedes='journal/DEPENDENCY_MAP_V58.json')
    return out


def materialize()->dict:
    require((P/NEW).is_file(),'Missing analytic-contact proof')
    ARCHIVE.mkdir(parents=True,exist_ok=True)
    mp=ARCHIVE/'active-source-manifest.json'
    if not mp.exists():
        native=P.parents[1]/'deliveries/a2-v58'/BASE/'active-source-manifest.json'
        require(native.is_file(),'Missing source-matched baseline manifest')
        mp.write_bytes(native.read_bytes())
    manifest=json.loads(mp.read_text())
    old={n:i for g in manifest.values() for n,i in g.items()}
    require(len(old)==121,'Unexpected baseline active union')
    for name,info in old.items():
        archived=ARCHIVE/name
        target=archived if name in CHANGES and archived.exists() else P/name
        data=target.read_bytes()
        require(len(data)==info['bytes'] and hashlib.sha256(data).hexdigest()==info['sha256']
                and blob_id(data)==info['git_blob'],'Baseline identity: '+name)
        if name in CHANGES:
            archived.parent.mkdir(parents=True,exist_ok=True)
            if not archived.exists():archived.write_bytes(data)
            expected=revised(name,data.decode())
            require((P/name).read_text() in (data.decode(),expected),'Unexpected active edit: '+name)
            (P/name).write_text(expected)
    write_json(P/'journal/DEPENDENCY_MAP_V59.json',dependency_map())
    return {'status':'materialized','baseline_source':BASE,'review_head':REVIEW,
            'inherited_active_sources':len(old),'new_input':NEW,'amended_inputs':list(CHANGES),
            'mathematical_certification':False}

if __name__=='__main__':print(json.dumps(materialize(),indent=2,sort_keys=True))
