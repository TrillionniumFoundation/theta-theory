#!/usr/bin/env python3
"""Reproduce the readable revision from frozen v115 and a checksum-bound patch."""
from __future__ import annotations
import base64,hashlib,json,shutil,subprocess,zlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PREFIX=Path('papers/A2-v17-boundary-information-coarsening/article')
OLD=ROOT/PREFIX/'v115';NEW=ROOT/PREFIX/'v116'
REVIEW='1cb4e00c86699247454d21dbec2dcce01a9c6b8b'
PATCH_SHA='d1c723f9b055f8fe7f988cffafce4015b62e49fea3774e8bf6c73e11d7cb9958'
EXPECTED={
 'AI_ASSISTANCE_AND_PROVENANCE.md':'2d809f80cadd32cbcaa448191b00de43112a14ccbb0513fd4319a1b65e5dec4d',
 'LITERATURE_AUDIT.md':'b9afdb76ab2b82e7a58617a157dd7a351293b9365c60661a16d923ebbf1c9f72',
 'PRESERVATION_AND_DEPENDENCIES.md':'ab2fe9221e5e35564652aafeef6dd9e95028be679002ad9ffa0bde8cd0034a69',
 'PROOF_AUDIT.md':'c7e8c988b943e46d9a8c3e691b37ef41ad2b28ed07d2c44f4be1cb01dfd5517e',
 'README.md':'e9f402d6d6bc3a019a7123ca82db16f01fb46e8a83d6576b08a195dd56574ef0',
 'RESPONSE_TO_R115.md':'d2362c02fb25329b72286f79c60070e4fceeaa2f34640b6191b9e01ea66a9bb2',
 'build.sh':'c33da7ddadc9cde27c1ab345d0ea413f42b93fee617918d78fabc37244175c27',
 'geometry.tex':'609937b4d7eb93c7b5bf83200bd25be585790cb7e5abcc96ef7cee1e8ae1b62a',
 'make_receipts.py':'3552a950ef8963afe4bf59557493fdc26f3e73cb35710848b8b3dab69682698c',
 'paper.tex':'cb7f24db09bb9e89ae6a8990525f3c6500535160074a6c2a1f5732ed58cc345d',
 'parts/00-introduction.tex':'82d3b6e68d0858c2a9bb32bcce1162b2ffffc24c59ab4f62cf17303a752d5da7',
 'parts/00b-intrinsic-residual-germs.tex':'f247d9164ea683e5846eebccf735c0b4fc64f1bac2bf3f879da1f99abf25501e',
 'parts/02j-higher-hyperplane-classification.tex':'927c80abdc489f68273dab821c07c0acdfe852198fab8102810f1e97c9fa2eae',
 'parts/02j-proof-details.tex':'21c9000b7550fc3014c6189c4460130724ce001a11fb02356016b6c52bb5df45',
 'parts/02k-quartic-primary.tex':'31d37af6ffcd2a0a110cb3c255a29051af29785c639c313f1d9732439955035e',
 'parts/02l-conductor-primary.tex':'46f5bafaa60e0fdd8abb0ae2e60df19cb102d05df6ad81400e2579591e779174',
 'parts/06-priority-and-application.tex':'cbf22f3690d9bd0f2cdb67efdb6eb0965208a95a3b171e43d5aa1b984341d451',
 'references.tex':'0b53f46c869f402534f55684d39f7b8d7044da50dd3861208eff00fb5709440a',
 'verify_v116.py':'0ee321a68a07d16de9472849f719b4bc2084cfca7312ec7cae6943d3a833181a',
}

def need(ok:bool,msg:str)->None:
    if not ok:raise RuntimeError(msg)
def digest(p:Path)->str:return hashlib.sha256(p.read_bytes()).hexdigest()
def main()->None:
    subprocess.run(['git','diff','--exit-code',REVIEW,'--',str(PREFIX/'v115')],cwd=ROOT,check=True)
    for p in sorted(OLD.rglob('*')):
        if not p.is_file():continue
        rel=p.relative_to(OLD)
        if rel.parts[0]=='crossrefs':continue
        if rel.parts[0]=='evidence' and rel.name!='V114_SOURCE_MANIFEST.json':continue
        if p.suffix not in ('.tex','.py','.sh','.md','.json'):continue
        target=NEW/rel;target.parent.mkdir(parents=True,exist_ok=True)
        if not target.exists():shutil.copy2(p,target)
    plain=ROOT/'.publication/a2-v116-source.patch'
    encoded=ROOT/'.publication/a2-v116-source.patch.zlib.b64'
    if encoded.exists():
        # Four known staging transcription insertions are removed before decoding.
        # The complete decoded patch must still equal its pre-recorded SHA-256.
        text=encoded.read_text().strip()
        for old,new in [('ibeqby8UL','ibeqbyUL'),('MCfNbVV0','MCfNbV0'),('Y9MpVJJTR','Y9MpVJTR'),('DSuZZUV0','DSuZUV0')]:
            text=text.replace(old,new)
        data=zlib.decompress(base64.b64decode(text,validate=True))
        need(hashlib.sha256(data).hexdigest()==PATCH_SHA,'patch digest mismatch')
        plain.write_bytes(data);encoded.unlink()
    need(plain.exists() and digest(plain)==PATCH_SHA,'missing or altered readable patch')
    for line in plain.read_text().splitlines():
        if line.startswith(('--- ','+++ ')):
            need(line[6:].startswith(str(PREFIX/'v116')+'/'),'patch escapes v116')
    check=subprocess.run(['git','apply','--check',str(plain)],cwd=ROOT,capture_output=True)
    if check.returncode==0:subprocess.run(['git','apply',str(plain)],cwd=ROOT,check=True)
    else:
        reverse=subprocess.run(['git','apply','--reverse','--check',str(plain)],cwd=ROOT,capture_output=True)
        need(reverse.returncode==0,'patch neither applicable nor already applied: '+check.stderr.decode())
    active=[]
    for p in sorted(OLD.rglob('*.tex')):
        rel=p.relative_to(OLD)
        if rel.parts[0] in ('history','evidence','crossrefs'):continue
        active.append(p)
        dest=NEW/'history/v115_source'/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest)
    need(len(active)==24,'unexpected active v115 source count')
    for name in ['README.md','RESPONSE_TO_R114.md','LITERATURE_AUDIT.md','PROOF_AUDIT.md','PRESERVATION_AND_DEPENDENCIES.md','AI_ASSISTANCE_AND_PROVENANCE.md','verify_revision.py','make_receipts.py']:
        shutil.copy2(OLD/name,NEW/'history'/('v115_'+name))
    manifest={'review_commit':REVIEW,'reviewed_head':'acfd3d57e0053e1b03df53020fd8e79e14599c03',
              'tex_sha256':{str(p.relative_to(OLD)):digest(p) for p in active}}
    (NEW/'evidence/V115_SOURCE_MANIFEST.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
    for name,expected in EXPECTED.items():
        got=digest(NEW/name);need(got==expected,'authored source mismatch '+name+' expected '+expected+' got '+got)
    (NEW/'evidence/AUTHORING_CHECK.json').write_text(json.dumps({'all_authored_hashes_match':True,'sha256':EXPECTED},indent=2,sort_keys=True)+'\n')
    (ROOT/'A2_REVISION_V116_INDEX.md').write_text('# A2 revision 116\n\nPrimary structure and residual geometry of multiplication failure schemes.\n\nBranch: `revision/a2-v116-higher-product-structure-2026-09-22`.\n\nRead [the v116 guide](papers/A2-v17-boundary-information-coarsening/article/v116/README.md), [the geometry article](papers/A2-v17-boundary-information-coarsening/article/v116/geometry.pdf), [the complete article](papers/A2-v17-boundary-information-coarsening/article/v116/paper.pdf), and [the response to R115](papers/A2-v17-boundary-information-coarsening/article/v116/RESPONSE_TO_R115.md).\n\nThe guide links the complete source, proof audit, source-bound build receipts and the explicitly unresolved full Ballico comparison. All older versions and review files are retained.\n')
    print('PASS: 19 authored file hashes; 24 frozen active sources; readable patch materialized')
if __name__=='__main__':main()
