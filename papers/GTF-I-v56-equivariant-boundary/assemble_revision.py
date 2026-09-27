"""Materialize the frozen v56 delta and native preservation tree; no network."""
from pathlib import Path
import base64
import hashlib
import json
import lzma

HOME=Path(__file__).resolve().parent
BASE=HOME.parent/'GTF-I-v55-stochastic-purification'
PAYLOAD='a0f9bc0e17c46d9c2cd399ad7dc7e1c0724ceda90dded0c478132d374ee2131d'
INVENTORY='95b73b3553dd95d8c4308c37dfb2e87d11f4f48f186932a40e58e609013a1ec4'
FROZEN={'FROZEN_R37_REPORT.md':'d9841d9b928800977e5965d5d6df52347fa64547',
        'FROZEN_PIPELINE_LEDGER.md':'c1ef29a5bcab0e2d4729c7c6815ec11e95be5808',
        'FROZEN_PIPELINE_HISTORY.md':'6041ef8b9e5e76883e86d4009c0735869b51b7a6'}

def require(ok,message):
    if not ok:raise RuntimeError(message)

def safe(name):
    p=Path(name)
    require(not p.is_absolute() and '..' not in p.parts,'Unsafe native path')
    return p

def main():
    parts=sorted((HOME/'assembly').glob('part-*.b64'))
    require(len(parts)==5,'Incomplete native delta')
    encoded=''.join(p.read_text().strip() for p in parts)
    require(len(encoded)==56588,'Native delta length mismatch')
    decoder=lzma.LZMADecompressor()
    data=decoder.decompress(base64.b64decode(encoded,validate=True),max_length=2000001)
    require(decoder.eof and not decoder.unused_data and len(data)<=2000000,'Invalid native archive')
    require(hashlib.sha256(data).hexdigest()==PAYLOAD,'Native delta digest mismatch')
    delta=json.loads(data);require(len(delta)==27,'Unexpected native file count')
    for name,entry in delta.items():
        if isinstance(entry,str):text=entry
        else:
            prior=BASE/safe(entry['base']);raw=prior.read_bytes()
            require(hashlib.sha256(raw).hexdigest()==entry['sha256'],'Delta base changed: '+name)
            lines=raw.decode('utf-8').splitlines(keepends=True);chunks=[]
            for op in entry['ops']:
                if isinstance(op,str):chunks.append(op)
                else:
                    i,j=op
                    require(isinstance(i,int) and isinstance(j,int) and 0<=i<=j<=len(lines),'Invalid copy range')
                    chunks.append(''.join(lines[i:j]))
            text=''.join(chunks)
        target=HOME/safe(name);target.parent.mkdir(parents=True,exist_ok=True)
        target.write_text(text,encoding='utf-8')
    raw=(BASE/'evidence/SOURCE_HASHES.json').read_bytes()
    require(hashlib.sha256(raw).hexdigest()==INVENTORY,'Frozen predecessor inventory changed')
    files=json.loads(raw);require(len(files)==114,'Unexpected predecessor source count')
    for name,digest in files.items():
        data=(BASE/safe(name)).read_bytes()
        require(hashlib.sha256(data).hexdigest()==digest,'Predecessor changed: '+name)
        target=HOME/'retained-v55'/safe(name);target.parent.mkdir(parents=True,exist_ok=True)
        target.write_bytes(data)
    manifest={'predecessor_publication':'00a0864003790aa3efcdc7f88358b6fa27ffe868',
              'review_commit':'0b2226b43a10f10c4ed0c5f969c058cde8d59230',
              'review_blob':FROZEN['FROZEN_R37_REPORT.md'],'files':files}
    (HOME/'PRESERVATION_MANIFEST.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
    for name,blob in FROZEN.items():
        data=(HOME/name).read_bytes()
        require(hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==blob,'Frozen evidence changed: '+name)
    print(json.dumps({'status':'readable-native-source-materialized','new_native_files':31,
                      'retained_native_files':114,'qualification':'not yet run'}))

if __name__=='__main__':main()
