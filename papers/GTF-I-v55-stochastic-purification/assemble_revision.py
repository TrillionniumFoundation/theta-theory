"""Materialize the frozen v55 native delta before qualification; no network."""
from pathlib import Path
import base64
import hashlib
import json
import lzma

HOME=Path(__file__).resolve().parent
BASE=HOME.parent/'GTF-I-v54-chebyshev-radius'
PAYLOAD='d8fbb22e626aa84503a5031b17d1509e1f5bed7d1f980eff0eeeb8c240783a9d'
INVENTORY='24a277754d99e289760a161bc3052444fc60c077d02aeb7f23d3f6278bbc385d'
REPORT='85a4bd2e1d4d6b02cb2360a66c25253148e8f2c1'

def require(ok,message):
    if not ok:raise RuntimeError(message)

def safe(name):
    path=Path(name)
    require(not path.is_absolute() and '..' not in path.parts,'Unsafe native path')
    return path

def main():
    parts=sorted((HOME/'assembly').glob('part-*.b64'))
    require(len(parts)==5,'Incomplete native delta')
    encoded=''.join(p.read_text().strip() for p in parts)
    require(len(encoded)==47632,'Native delta length mismatch')
    decoder=lzma.LZMADecompressor()
    data=decoder.decompress(base64.b64decode(encoded,validate=True),max_length=2000001)
    require(decoder.eof and not decoder.unused_data and len(data)<=2000000,'Invalid native delta archive')
    require(hashlib.sha256(data).hexdigest()==PAYLOAD,'Native delta digest mismatch')
    delta=json.loads(data)
    require(len(delta)==21,'Unexpected native delta file count')
    for name,entry in delta.items():
        target=HOME/safe(name)
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
        target.parent.mkdir(parents=True,exist_ok=True)
        target.write_text(text,encoding='utf-8')
    raw=(BASE/'evidence/SOURCE_HASHES.json').read_bytes()
    require(hashlib.sha256(raw).hexdigest()==INVENTORY,'Frozen predecessor inventory changed')
    files=json.loads(raw);require(len(files)==91,'Unexpected retained native count')
    for name,digest in files.items():
        source=BASE/safe(name);data=source.read_bytes()
        require(hashlib.sha256(data).hexdigest()==digest,'Predecessor source changed: '+name)
        target=HOME/'retained-v54'/safe(name);target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
    manifest={'predecessor_publication':'1eb16a3f857d17a91dc1c82906ef16a5965a47d2',
              'review_commit':'9c92a08458b92fd831010dca835de8e2239f82fc',
              'review_blob':REPORT,'files':files}
    (HOME/'PRESERVATION_MANIFEST.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
    report=(HOME/'FROZEN_R36_REPORT.md').read_bytes()
    require(hashlib.sha1(b'blob '+str(len(report)).encode()+b'\0'+report).hexdigest()==REPORT,'Controlling report changed')
    print(json.dumps({'status':'native-source-materialized','new_native_files':22,
                      'retained_native_files':91,'frozen_report':True,'qualification':'not yet run'}))

if __name__=='__main__':main()
