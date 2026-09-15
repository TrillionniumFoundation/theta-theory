#!/usr/bin/env python3
"""Apply the bounded v56-referee corrections and archive the exact prior inputs.

Reference roles are declared by the author after reading statements, proofs and
hypotheses. The collected occurrences are syntax evidence, not a proof oracle.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import re
from source_provenance import blob_id, graph, require, write_json, strip_comments

P=Path(__file__).resolve().parents[1]
ARCHIVE=P/'history/v56-review-baseline'
BASE='ae0eea2a3368b01a72ab6eaf50bad0cfb50ec8de'
REVIEW='4d2916b6963404d65966626196c3da5da04f8756'
INTRO='journal/00_principal_introduction_v56.tex'
CHANNEL='article/23j_generic_finite_channel_rigidity_v45.tex'
DIFFERENTIAL='article/23m_differential_rigidity_v48.tex'
ROUTES='journal/full_reference_routes_v56.tex'
CHANGES=('main.tex','rigidity.tex',INTRO,CHANNEL,DIFFERENTIAL,ROUTES)
DEPENDENCY='thm:v25-global-physical-reconstruction'
APPLICATION='cor:v45-physical-chart'
REF=re.compile(r'\\(?:ref|eqref|autoref|pageref)\{([^}]+)\}')
BLOCK=re.compile(r'\\begin\{(structuraltheorem|theorem|lemma|proposition|corollary|definition|remark|proof)\}.*?\\end\{\1\}',re.S)


def once(text,before,after):
    require(text.count(before)==1,'Unexpected edit anchor: '+before)
    return text.replace(before,after,1)


def revised(name,text):
    if name=='main.tex':
        require(text.count('A2 revision 56')==2,'Unexpected full-entry version fields')
        return text.replace('A2 revision 56','A2 revision 57')
    if name=='rigidity.tex':
        return once(once(text,'A2 v56.','A2 v57.'),'A2 revision 56','A2 revision 57')
    if name==ROUTES:
        text=once(text,'% Explicit external labels; internal proof labels are never redirected.',
          '% Full-manuscript aliases; their semantic roles are declared in DEPENDENCY_MAP_V57.json.\n'
          '% The acquisition theorem is an explicit input to a principal corollary, not a comparison.')
        return once(text,'{A2-v56}','{A2-v57}')
    if name==DIFFERENTIAL:
        return once(text,'The full-class finite-histogram reconstruction below uses increasing',
          'The full-class finite-histogram reconstruction in the complete technical\nmanuscript uses increasing')
    if name==INTRO:
        text=once(text,
          'orders.  More precisely, for $M\\ge2$ and two pairs with the same gap agreeing through order $M$ on a\ncommon sufficiently small collar with the required functional smooth\nbounds, their actions satisfy',
          'orders.  More precisely, let $M\\ge2$ and let two anchored graph pairs\nhave the same gap and equal graph jets through order $M$ at their\nrespective anchored contacts.  Under common functional smooth bounds\non a sufficiently small collar, their actions satisfy')
        text=once(text,
          'The finite-dimensional scalar-coordinate conclusion is a consequence\nof this geometric kernel theorem on a stipulated immersed model.',
          'The finite-dimensional scalar-coordinate conclusion is a consequence\nof this geometric kernel theorem on a stipulated immersed model.\n\nThe nonlinear content is not encoded by the rarity of preparation alone.\nThe analytic family in Theorem~\\ref{thm:v4-jet-fiber} fixes the gap,\nfree area, contact curvatures and every leading endpoint covariance and\ncount amplitude, while its fourth contact jet is $3-24s$.  The signed\nblock inverse and Theorem~\\ref{thm:v26-density-inverse} therefore\nseparate its conditional laws at a fixed sufficiently small positive\noffset.  Thus the full law distinguishes geometries that its leading\nquadratic record does not.  The relative estimate supplies that nonlinear\nrecord at long flight number; the smooth remainder factorization licenses\nits geometric inversion.  These two analytic steps, rather than the\nsubsequent finite congruence bookkeeping or finite-dimensional coordinate\nselection, are the mechanism of the inverse.')
        text=once(text,
          'They are explicit references to that companion, not missing internal\nnumbers.  The companion\'s quantified acquisition theory uses additional',
          'They are explicit references to that companion, not missing internal\nnumbers.  One has a further logical role:\nCorollary~\\ref{cor:v45-physical-chart} is an application of\nTheorem~\\ref{thm:v25-global-physical-reconstruction} of the complete\ntechnical manuscript.  It uses that theorem\'s acquisition and risk\nestimates in addition to the geometric results proved here.  Its proof\nverifies the persistent-design hypotheses; it does not reprove the\nphysical pilot or capped estimation theorem.  This application is not\na premise of Theorem~\\ref{thm:v56-local-mechanism} or\nTheorems~\\ref{thm:v48-main} and~\\ref{thm:v51-main}.\nThe companion\'s quantified acquisition theory uses additional')
        return text
    if name==CHANNEL:
        a=text.index(r'\begin{corollary}[Persistent finite-design physical reconstruction]')
        b=text.index(r'\end{proof}',a)+len(r'\end{proof}')
        replacement=r'''\paragraph{Additional acquisition input.}
The following application uses
Theorem~\ref{thm:v25-global-physical-reconstruction} of the complete
technical manuscript, including its uniform-family assumptions and its
physical observation space.  In particular its calibration stage records
planar endpoint positions in a common frame for the two types of each
channel, uses the physical clock, and charges all independent preparations,
including failures.  These are additional acquisition assumptions, not
conclusions of the exact law-valued inverse.  The present corollary is not
used in the proofs of the geometric reconstruction or its differential.

\begin{corollary}[Persistent finite-design physical reconstruction]
\label{cor:v45-physical-chart}
Let $\mathfrak K$ be a compact analytic subfamily contained in one of the
persistent skeleton neighborhoods of
Theorem~\ref{thm:v45-generic-determination}.  Assume the uniform analytic,
chart and physical-record hypotheses of
Theorem~\ref{thm:v25-global-physical-reconstruction}, with the marked
$N+1$-channel design supplied by that neighborhood.  Then the acquisition
and uniform reconstruction conclusions of that theorem hold for this
design, with one common positive offset and all preparation failures
charged.  In particular its finite capped policies recover the complete
labelled table, including the unknown marked lattice, modulo one common
proper Euclidean motion.  The minimum even flight number may tend to
infinity as in its prescribed-budget protocol.
\end{corollary}

\begin{proof}
We apply Theorem~\ref{thm:v25-global-physical-reconstruction}; the task
here is to verify its geometric design hypotheses, not to reconstruct
its acquisition estimates from exact injectivity.
The persistent skeleton fixes connected incidence, a signature-rigid
spanning tree, and two independent marked cycle gains.  The transition
matches are unique on this properly asymmetric neighborhood.  The finite
list of channels has fixed gates and positive clearance; the stipulated
compact-family smooth bounds give common local laws by
Lemma~\ref{lem:v45-selected-locality}.  The integer gain matrix $M$ is
fixed.  Since $L$ is nonsingular throughout the compact class, the smallest
singular value of the recovered holonomy matrix $LM$ has a positive
minimum.  No Euclidean lattice vector is supplied by this argument.

Theorem~\ref{thm:v45-generic-determination} gives injectivity on this
class.  The finite analytic signature and compact-inverse results of
Section~\ref{sec:v25-signature-stability} provide the geometric inverse
hypotheses used by the cited acquisition theorem.  Its remaining uniform
analytic, chart and physical-record hypotheses are precisely those
assumed in the statement.  Theorem~\ref{thm:v25-global-physical-reconstruction}
therefore supplies the charged same-final-flight pilot, capped fresh-stage
estimator, and increasing-order prescribed-budget construction.  Applying
those conclusions gives the assertion.  The design is fixed before
acquisition; no new sensor, uncharged selection stage, or common design
across unrelated skeleton neighborhoods is introduced.
\end{proof}'''
        return text[:a]+replacement+text[b:]
    raise RuntimeError('Unknown amended file: '+name)


def occurrences(root,external):
    """Assign literal references to statement/proof/prose locations.

Pairing a proof with the preceding labelled statement is a syntactic aid.
It is not a claim that unlabelled reasoning or imported hypotheses vanish.
"""
    found=[]
    for name in sorted(graph(root,'rigidity.tex')):
        if name==ROUTES:continue
        text=strip_comments((root/name).read_text());spans=[];owner=None
        for match in BLOCK.finditer(text):
            labels=re.findall(r'\\label\{([^}]+)\}',match.group())
            kind=match.group(1)
            if kind!='proof':owner=labels[0] if labels else None
            spans.append((match.start(),match.end(),kind,owner))
        for match in REF.finditer(text):
            if match.group(1) not in external:continue
            kind,unit='prose',None
            for a,b,k,o in spans:
                if a<=match.start()<b:kind,unit=k,o;break
            found.append({'path':name,'line':text[:match.start()].count('\n')+1,
              'label':match.group(1),'location':kind,'statement_label':unit})
    return found


def dependency_map(root=P):
    previous=json.loads((root/'journal/DEPENDENCY_MAP_V56.json').read_text())
    labels=set(previous['external_comparison_labels'])
    found=occurrences(root,labels)
    roles={x:('external_theorem_input' if x==DEPENDENCY else 'background_comparison') for x in sorted(labels)}
    return {'revision':57,'baseline_source':BASE,'review_head':REVIEW,
      'supersedes':'journal/DEPENDENCY_MAP_V56.json',
      'principal_entry':'rigidity.tex','full_entry':'main.tex',
      'external_reference_roles':roles,'occurrences':found,
      'external_theorem_applications':[{
        'statement_label':APPLICATION,'path':CHANNEL,
        'input_label':DEPENDENCY,'input_source':'article/25b_augmented_global_reconstruction_v26.tex',
        'input_title':'Uniform global reconstruction from long same-type records',
        'role':'The theorem supplies the acquisition, risk and capped-budget conclusions.',
        'additional_hypotheses':['compact marked analytic class and uniform geometric/analytic margins',
          'common physical record spaces and fixed marked design',
          'both planar endpoint components in per-channel oriented physical frames',
          'physical clock, independent phase-volume preparations and charged failures'],
        'internal_design_checks':['persistent signature-rigid tree','two independent marked gains',
          'uniform selected-channel laws','holonomy nonsingularity margin','exact inverse on the compact class'],
        'core_status':'Downstream application, not a premise of the three headline geometric theorems.'}],
      'headline_source_labels':['thm:v56-local-mechanism','thm:v48-main','thm:v51-main'],
      'principal_inputs':sorted(graph(root,'rigidity.tex')),
      'role_assignment':'Author-declared after statement, hypothesis and proof reading; not inferred from delimiter position.',
      'syntax_scope':'Literal references in statements, associated proofs and prose; no inference of semantic independence.',
      'mathematical_certification':False}


def materialize():
    ARCHIVE.mkdir(parents=True,exist_ok=True)
    manifest=ARCHIVE/'active-source-manifest.json'
    if not manifest.exists():
        origin=P.parents[1]/'deliveries/a2-v56'/BASE/'active-source-manifest.json'
        require(origin.is_file(),'Supply the source-matched v56 manifest before editing')
        manifest.write_bytes(origin.read_bytes())
    old={n:i for group in json.loads(manifest.read_text()).values() for n,i in group.items()}
    require(len(old)==120,'Unexpected baseline union')
    for name,info in old.items():
        archived=ARCHIVE/name;path=archived if name in CHANGES and archived.exists() else P/name
        data=path.read_bytes()
        require(len(data)==info['bytes'] and hashlib.sha256(data).hexdigest()==info['sha256']
          and blob_id(data)==info['git_blob'],'Unexpected baseline bytes: '+name)
        if name in CHANGES:
            archived.parent.mkdir(parents=True,exist_ok=True)
            if not archived.exists():archived.write_bytes(data)
            after=revised(name,data.decode())
            require((P/name).read_text() in (data.decode(),after),'Unexpected current edit: '+name)
            (P/name).write_text(after)
    write_json(P/'journal/DEPENDENCY_MAP_V57.json',dependency_map())
    return {'status':'materialized','review_head':REVIEW,'baseline_source':BASE,
      'amended_inputs':list(CHANGES),'inherited_active_inputs':len(old),
      'external_theorem_application':APPLICATION,'new_mathematical_theorems':0,
      'mathematical_certification':False}

if __name__=='__main__':print(json.dumps(materialize(),indent=2,sort_keys=True))
