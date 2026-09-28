"""Materialize pinned native sources before qualification; no network or hidden dependency."""
from pathlib import Path
import base64, hashlib, json, lzma
HOME=Path(__file__).resolve().parent
BASE=HOME.parent/'GTF-I-v62-referee-response'
def require(ok,message):
    if not ok:raise RuntimeError(message)
def safe(name):
    p=Path(name);require(not p.is_absolute() and '..' not in p.parts,'Unsafe source path');return p
def main():
    config=json.loads((HOME/'assembly/config.json').read_text())
    parts=sorted((HOME/'assembly').glob('part-*.b64'))
    require(len(parts)==config['part_count'],'Incomplete assembly')
    encoded=''.join(p.read_text().strip() for p in parts)
    require(len(encoded)==config['encoded_length'],'Assembly length mismatch')
    decoder=lzma.LZMADecompressor();raw=decoder.decompress(base64.b64decode(encoded,validate=True),max_length=2000001)
    require(decoder.eof and not decoder.unused_data and len(raw)<=2000000,'Invalid assembly archive')
    require(hashlib.sha256(raw).hexdigest()==config['payload_sha256'],'Assembly digest mismatch')
    delta=json.loads(raw);require(len(delta)==config['new_delta_files'],'Native delta count mismatch')
    for name,entry in delta.items():
        if isinstance(entry,str):text=entry
        else:
            data=(BASE/safe(entry['base'])).read_bytes()
            require(hashlib.sha256(data).hexdigest()==entry['sha256'],'Changed source base: '+name)
            lines=data.decode().splitlines(keepends=True);chunks=[]
            for op in entry['ops']:
                if isinstance(op,str):chunks.append(op)
                else:
                    i,j=op;require(isinstance(i,int) and isinstance(j,int) and 0<=i<=j<=len(lines),'Invalid source range')
                    chunks.append(''.join(lines[i:j]))
            text=''.join(chunks)
        target=HOME/safe(name);target.parent.mkdir(parents=True,exist_ok=True);target.write_text(text,encoding='utf-8')
    raw=(BASE/'evidence/SOURCE_HASHES.json').read_bytes()
    require(hashlib.sha256(raw).hexdigest()==config['inventory_sha256'],'Changed v62 inventory')
    files=json.loads(raw);require(len(files)==410,'Changed predecessor count')
    for name,digest in files.items():
        data=(BASE/safe(name)).read_bytes()
        require(hashlib.sha256(data).hexdigest()==digest,'Changed predecessor source: '+name)
        target=HOME/'retained-v62'/safe(name);target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
    manifest={**config['manifest_metadata'],'files':files}
    (HOME/'PRESERVATION_MANIFEST.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'readable-native-source-materialized','retained':410,'new_files':len(delta)+1,'qualification':'not yet run'}))
if __name__=='__main__':main()
