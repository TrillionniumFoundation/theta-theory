#!/usr/bin/env python3
"""Verify preservation and declared cross-document roles, with finite controls.

Role declarations encode a human/author reading of hypotheses, not a semantic
proof decision computed from TeX delimiters. Historical checkers remain frozen.
"""
from __future__ import annotations
from collections import Counter
import hashlib
import json
import re
from pathlib import Path
from source_provenance import require, blob_id, graph
from materialize_revision_v57 import (P, ARCHIVE, CHANGES, INTRO, CHANNEL,
    ROUTES, DEPENDENCY, APPLICATION, REF, BLOCK, revised, dependency_map)
from check_revision_v56 import coordinate_controls
from check_revision_v55 import reduction_controls


def references_by_unit(text):
    out={}; owner=None
    for match in BLOCK.finditer(text):
        labels=re.findall(r'\\label\{([^}]+)\}',match.group())
        if match.group(1)!='proof':owner=labels[0] if labels else None
        if owner:out.setdefault(owner,set()).update(REF.findall(match.group()))
    return out


def validate_roles(units,roles):
    for owner,refs in units.items():
        for label in refs & set(roles):
            require(owner==APPLICATION and label==DEPENDENCY and
                    roles[label]=='external_theorem_input',
                    'Undeclared external theorem dependency: '+str((owner,label)))


def preservation():
    baseline=json.loads((ARCHIVE/'active-source-manifest.json').read_text())
    old={n:i for d in baseline.values() for n,i in d.items()}
    require(len(old)==120,'Wrong inherited union')
    changed=[];count=0;retained=0;proofs=0;before_env=Counter();after_env=Counter()
    for name,info in old.items():
        data=(ARCHIVE/name if name in CHANGES else P/name).read_bytes()
        require(len(data)==info['bytes'] and hashlib.sha256(data).hexdigest()==info['sha256']
          and blob_id(data)==info['git_blob'],'Baseline identity: '+name)
        original=data.decode();current=(P/name).read_text()
        require(current==(revised(name,original) if name in CHANGES else original),'Unprescribed edit: '+name)
        a=list(BLOCK.finditer(original));b=list(BLOCK.finditer(current))
        require(len(a)==len(b),'Statement/proof inventory changed: '+name)
        for ordinal,(x,y) in enumerate(zip(a,b)):
            count+=1;proofs+=x.group(1)=='proof';before_env[x.group(1)]+=1;after_env[y.group(1)]+=1
            if x.group()==y.group():retained+=1
            else:changed.append({'path':name,'ordinal':ordinal,'environment':x.group(1),
                      'old_block_sha256':hashlib.sha256(x.group().encode()).hexdigest(),
                      'new_block_sha256':hashlib.sha256(y.group().encode()).hexdigest()})
        require(set(re.findall(r'\\label\{([^}]+)\}',original)) <=
                set(re.findall(r'\\label\{([^}]+)\}',current)),'Inherited label lost: '+name)
    require([(x['path'],x['environment']) for x in changed]==[
        (CHANNEL,'corollary'),(CHANNEL,'proof'),(INTRO,'theorem')],
        'Changed blocks exceed the declared correction set')
    require(before_env==after_env,'Environment inventory changed')
    unions=set();entry_counts={}
    for entry,group in baseline.items():
        files=graph(P,entry+'.tex');require(files==set(group),'Active graph changed: '+entry)
        entry_counts[entry]=len(files);unions|=files
        text='\n'.join((P/n).read_text() for n in sorted(files))
        labels=re.findall(r'\\label\{([^}]+)\}',text)
        require(len(labels)==len(set(labels)),'Duplicate labels: '+entry)
        refs=set(REF.findall(text));external=set()
        if entry=='rigidity':external=set(dependency_map()['external_reference_roles'])
        if entry=='main':external={x for x in refs if x.startswith('TC-')}
        require(refs<=set(labels)|external,'Unresolved source reference: '+entry)
        cites={k.strip() for c in re.findall(r'\\cite(?:\[[^\]]*\])?\{([^}]+)\}',text) for k in c.split(',')}
        bib=set(re.findall(r'\\bibitem(?:\[[^\]]*\])?\{([^}]+)\}',text))
        require(cites<=bib,'Unresolved bibliography: '+entry)
    require(unions==set(old),'Union changed')
    return {'inherited_unique_active_inputs':len(old),'byte_identical_in_place':len(old)-len(CHANGES),
       'archived_amended_inputs':list(CHANGES),'entry_source_counts':entry_counts,
       'inherited_statement_proof_blocks':count,'verbatim_blocks':retained,
       'amended_blocks':changed,'inherited_proof_blocks':proofs,
       'environment_inventory':dict(sorted(before_env.items())),
       'new_theorems':0,'scope':'Per-source-path block retention; shared display copies are counted as source blocks, not independent theorems.'}


def dependency_controls():
    declared=json.loads((P/'journal/DEPENDENCY_MAP_V57.json').read_text())
    require(declared==dependency_map(),'Dependency ledger differs from declared roles/occurrences')
    roles=declared['external_reference_roles'];units={}
    for name in graph(P,'rigidity.tex'):
        units.update(references_by_unit((P/name).read_text()))
    validate_roles(units,roles)
    require(DEPENDENCY in units[APPLICATION],'Acquisition dependency lost')
    # Regression case: moving a theorem reference into a statement cannot remove it.
    fixture=(r'\begin{corollary}\label{'+APPLICATION+r'}Assume Theorem~\ref{'+DEPENDENCY+
             r'}.\end{corollary}\begin{proof}Apply its conclusions.\end{proof}')
    fu=references_by_unit(fixture);require(DEPENDENCY in fu[APPLICATION],'Statement-only import not detected')
    validate_roles(fu,roles)
    wrong=dict(roles);wrong[DEPENDENCY]='background_comparison'
    rejected=False
    try:validate_roles(fu,wrong)
    except RuntimeError:rejected=True
    require(rejected,'Misclassified hypothesis-level import passed')
    rogue=fixture.replace(APPLICATION,'thm:undeclared-import')
    rejected=False
    try:validate_roles(references_by_unit(rogue),roles)
    except RuntimeError:rejected=True
    require(rejected,'Undeclared imported theorem passed')
    # The literal graph is a regression aid only; it does not prove semantic independence.
    for headline in declared['headline_source_labels']:
        seen=set();pending=[headline]
        while pending:
            label=pending.pop()
            if label in seen:continue
            seen.add(label);pending.extend(units.get(label,set())-seen)
        require(APPLICATION not in seen and DEPENDENCY not in seen,
                'New literal edge from a headline theorem to the acquisition application')
    return {'external_reference_roles':roles,'external_reference_occurrences':len(declared['occurrences']),
      'statement_only_import_detected':True,'misclassification_rejected':True,
      'undeclared_theorem_import_rejected':True,
      'headline_literal_reference_regression':'passed; not semantic proof certification',
      'role_source':'Explicit reading-derived declaration, not proof-environment exclusion.'}


if __name__=='__main__':
    print(json.dumps({'status':'passed','mathematical_certification':False,
      'preservation':preservation(),'dependency_controls':dependency_controls(),
      'retained_graph_support_and_signed_controls':coordinate_controls(),
      'retained_v55_stopped_experiment_controls':reduction_controls()},indent=2,sort_keys=True))
