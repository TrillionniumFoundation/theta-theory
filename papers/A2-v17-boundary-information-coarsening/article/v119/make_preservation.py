#!/usr/bin/env python3
"""Record exact preservation against the frozen v118 source artifact."""
from pathlib import Path
import hashlib,json,re
here=Path(__file__).resolve().parent
base=here.parent/'v118'
if not base.is_dir():
    raise SystemExit('For regeneration, supply the pinned v118 sibling; existing manifest is portable.')
old_labels=set(); new_labels=set(); entries=[]
for source in base.rglob('*.tex'):
    if 'evidence' in source.parts: continue
    rel=source.relative_to(base); dest=here/rel
    old_labels.update(re.findall(r'\\label\{([^}]+)\}',source.read_text()))
    entries.append({'path':str(rel),'old_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
                    'new_sha256':hashlib.sha256(dest.read_bytes()).hexdigest() if dest.exists() else None,
                    'unchanged':dest.exists() and source.read_bytes()==dest.read_bytes()})
for source in list(here.glob('*.tex'))+list((here/'parts').glob('*.tex')):
    new_labels.update(re.findall(r'\\label\{([^}]+)\}',source.read_text()))
missing=sorted(old_labels-new_labels)
assert not missing,missing
out={'base_mathematical_source':'c87bfdad8d97e68637d269e656b46c4cce85551e',
     'base_product_head':'44bfc648ead008896a6981a7302a6d5ab8b21bb8',
     'controlling_review':'d4254d9b01405ad02c64d2ff591503d4cc7a6aa7',
     'old_labels':sorted(old_labels),'old_label_count':len(old_labels),
     'new_label_count':len(new_labels),'missing_old_labels':missing,
     'new_labels':sorted(new_labels-old_labels),'source_files':entries,
     'unchanged_old_tex_files':sum(x['unchanged'] for x in entries),
     'missing_old_tex_files':[x['path'] for x in entries if x['new_sha256'] is None],
     'v118_directory_modified':False}
(here/'evidence/PRESERVATION.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ['old_labels','source_files','new_labels']},indent=2))
