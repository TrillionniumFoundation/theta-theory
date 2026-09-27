"""Materialize the frozen v59 native revision before qualification; no network."""
from pathlib import Path
import base64
import hashlib
import json
import lzma

HOME=Path(__file__).resolve().parent
BASE=HOME.parent/'GTF-I-v58-finite-input'
PAYLOAD='91fe753757219ca517e6559a20fb30251b35e438474091b070807ba64774b4c2'
INVENTORY='b24cb0618ff15980acb6165c227d7ff5db8b09312277d8750da72e12d0809fd3'
PINS={'FROZEN_R39_REPORT.md':'5ba98081a61e12f11a0858e696bf79492c106ae9',
      'FROZEN_R39_PIPELINE_AUDIT.md':'6f36057b0f12c0a1d71798b6b9f0fe9fc0f592a9'}

def require(ok,message):
    if not ok:raise RuntimeError(message)

def safe(name):
    p=Path(name)
    require(not p.is_absolute() and '..' not in p.parts,'Unsafe native path')
    return p

def main():
    parts=sorted((HOME/'assembly').glob('part-*.b64'))
    require(len(parts)==6,'Incomplete native payload')
    encoded=''.join(p.read_text().strip() for p in parts)
    require(len(encoded)==53688,'Native payload length mismatch')
    dec=lzma.LZMADecompressor()
    raw=dec.decompress(base64.b64decode(encoded,validate=True),max_length=2000001)
    require(dec.eof and not dec.unused_data and len(raw)<=2000000,'Invalid native archive')
    require(hashlib.sha256(raw).hexdigest()==PAYLOAD,'Native payload digest mismatch')
    overrides=json.loads(raw);require(len(overrides)==21,'Native override count mismatch')
    inventory=(BASE/'evidence/SOURCE_HASHES.json').read_bytes()
    require(hashlib.sha256(inventory).hexdigest()==INVENTORY,'Predecessor inventory changed')
    files=json.loads(inventory);require(len(files)==230,'Predecessor file count changed')
    for name,digest in files.items():
        data=(BASE/safe(name)).read_bytes()
        require(hashlib.sha256(data).hexdigest()==digest,'Predecessor bytes changed: '+name)
        target=HOME/'retained-v58'/safe(name);target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
        if not name.startswith('retained-v57/') and name not in overrides and name!='PRESERVATION_MANIFEST.json':
            target=HOME/safe(name);target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
    for name,text in overrides.items():
        require(isinstance(text,str),'Invalid native source')
        target=HOME/safe(name);target.parent.mkdir(parents=True,exist_ok=True);target.write_text(text,encoding='utf-8')
    manifest={'predecessor_publication':'27be4b236b9336bbfa2fa855dec3a346d63b8be7',
              'review_commit':'6daa50db42873a4a32cd3c1610f19630f5739b51',
              'review_blob':PINS['FROZEN_R39_REPORT.md'],
              'audit_commit':'849cbc2fb4d589d8fd13d8c7d34492af191e0f75',
              'audit_blob':PINS['FROZEN_R39_PIPELINE_AUDIT.md'],'files':files}
    (HOME/'PRESERVATION_MANIFEST.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
    for name,blob in PINS.items():
        raw=(HOME/name).read_bytes()
        require(hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==blob,'Frozen r39 record changed: '+name)
    print(json.dumps({'status':'native-source-materialized','retained_files':230,'native_overrides':21,
                      'both_r39_records_verified':True,'qualification':'not yet executed'}))
if __name__=='__main__':main()
