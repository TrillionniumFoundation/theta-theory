"""Materialize frozen v57 native sources before source-bound qualification."""
from pathlib import Path
import base64
import hashlib
import json
import lzma

HOME=Path(__file__).resolve().parent
BASE=HOME.parent/'GTF-I-v56-equivariant-boundary'
PAYLOAD='7f9df841b88df15132d2f7bda560995254c32846ee8b592b6d80bb3b1db49154'
INVENTORY='2101bdbe43b44171ebdb378c91f9fdfd031fbd04d070bd695bbd7bace2d9e58b'
REPORT='d9841d9b928800977e5965d5d6df52347fa64547'

def require(ok,message):
    if not ok:raise RuntimeError(message)

def safe(name):
    p=Path(name)
    require(not p.is_absolute() and '..' not in p.parts,'Unsafe native path')
    return p

def main():
    parts=[HOME/'assembly'/('part-'+str(i)+'.b64') for i in range(4)]
    require(all(p.is_file() for p in parts),'Incomplete native delta')
    encoded=''.join(p.read_text().strip() for p in parts)
    require(len(encoded)==37944,'Native delta length mismatch')
    decoder=lzma.LZMADecompressor()
    data=decoder.decompress(base64.b64decode(encoded,validate=True),max_length=2000001)
    require(decoder.eof and not decoder.unused_data and len(data)<=2000000,'Invalid delta archive')
    require(hashlib.sha256(data).hexdigest()==PAYLOAD,'Native delta digest mismatch')
    delta=json.loads(data);require(len(delta)==35,'Unexpected native delta file count')
    for name,entry in delta.items():
        target=HOME/safe(name)
        if isinstance(entry,str):text=entry
        else:
            raw=(BASE/safe(entry['base'])).read_bytes()
            require(hashlib.sha256(raw).hexdigest()==entry['sha256'],'Delta base changed: '+name)
            lines=raw.decode('utf-8').splitlines(keepends=True);chunks=[]
            for op in entry['ops']:
                if isinstance(op,str):chunks.append(op)
                else:
                    i,j=op
                    require(isinstance(i,int) and isinstance(j,int) and 0<=i<=j<=len(lines),'Invalid copy range')
                    chunks.append(''.join(lines[i:j]))
            text=''.join(chunks)
        target.parent.mkdir(parents=True,exist_ok=True)
        target.write_text(text,encoding='utf-8')
    raw=(BASE/'evidence/SOURCE_HASHES.json').read_bytes()
    require(hashlib.sha256(raw).hexdigest()==INVENTORY,'Frozen predecessor inventory changed')
    files=json.loads(raw);require(len(files)==145,'Unexpected retained native count')
    for name,digest in files.items():
        data=(BASE/safe(name)).read_bytes()
        require(hashlib.sha256(data).hexdigest()==digest,'Predecessor source changed: '+name)
        target=HOME/'retained-v56'/safe(name)
        target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
    manifest={'predecessor_publication':'5c3b3fb9ab878748f58462e065850d0a5cbbc2f6',
              'review_commit':'0b2226b43a10f10c4ed0c5f969c058cde8d59230',
              'review_blob':REPORT,'files':files}
    (HOME/'PRESERVATION_MANIFEST.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
    report=(HOME/'FROZEN_R37_REPORT.md').read_bytes()
    require(hashlib.sha1(b'blob '+str(len(report)).encode()+b'\0'+report).hexdigest()==REPORT,'Controlling report changed')
    print(json.dumps({'status':'native-source-materialized','new_native_files':36,
                      'retained_native_files':145,'frozen_report':True,'qualification':'not yet run'}))

if __name__=='__main__':main()
