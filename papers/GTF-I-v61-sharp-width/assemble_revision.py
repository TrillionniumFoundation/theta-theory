"""Materialize and verify readable v61 native source before qualification; no network."""
from pathlib import Path
import base64,hashlib,json,lzma
HOME=Path(__file__).resolve().parent
BASE=HOME.parent/'GTF-I-v59-causal-realization'
PARTS=5
ENCODED=53772
PAYLOAD='ecd4971867e35c10df519358f9ec4c6df9f6ffff410f62d5caebf85d207a1879'
INVENTORY='d69678fd67a76617e20e42916e5be963970692c889cfe5d197a88f62837c5ecf'
OWN='096992bcbe7ac88caa6a81e957215f442003de897814535acaf488b2d7ab7a57'

def require(ok,msg):
    if not ok:raise RuntimeError(msg)
def safe(name):
    p=Path(name)
    require(not p.is_absolute() and '..' not in p.parts,'Unsafe native path')
    return p

def main():
    raw=(BASE/'evidence/SOURCE_HASHES.json').read_bytes()
    require(hashlib.sha256(raw).hexdigest()==INVENTORY,'Frozen source inventory changed')
    inventory=json.loads(raw);require(len(inventory)==285,'Wrong predecessor count')
    for name,digest in inventory.items():
        data=(BASE/safe(name)).read_bytes()
        require(hashlib.sha256(data).hexdigest()==digest,'Frozen source changed: '+name)
        retained=HOME/'retained-v59'/safe(name)
        retained.parent.mkdir(parents=True,exist_ok=True);retained.write_bytes(data)
        if 'retained-v58' not in Path(name).parts:
            target=HOME/safe(name);target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
    parts=sorted((HOME/'assembly').glob('part-*.b64'))
    require(len(parts)==PARTS,'Incomplete delta')
    encoded=''.join(p.read_text().strip() for p in parts)
    require(len(encoded)==ENCODED,'Wrong encoded length')
    decoder=lzma.LZMADecompressor()
    raw=decoder.decompress(base64.b64decode(encoded,validate=True),max_length=2000001)
    require(decoder.eof and not decoder.unused_data and len(raw)<=2000000,'Invalid delta archive')
    require(hashlib.sha256(raw).hexdigest()==PAYLOAD,'Native delta digest mismatch')
    for name,entry in json.loads(raw).items():
        target=HOME/safe(name)
        if isinstance(entry,str):text=entry
        else:
            original=(BASE/safe(entry['base'])).read_bytes()
            require(hashlib.sha256(original).hexdigest()==entry['sha256'],'Wrong delta base: '+name)
            lines=original.decode().splitlines(keepends=True);out=[]
            for op in entry['ops']:
                if isinstance(op,str):out.append(op)
                else:
                    i,j=op
                    require(isinstance(i,int) and isinstance(j,int) and 0<=i<=j<=len(lines),'Bad copy range')
                    out.append(''.join(lines[i:j]))
            text=''.join(out)
        target.parent.mkdir(parents=True,exist_ok=True);target.write_text(text,encoding='utf-8')
    own={str(p.relative_to(HOME)):hashlib.sha256(p.read_bytes()).hexdigest() for p in HOME.rglob('*') if p.is_file()
         and not {'retained-v59','evidence','assembly','__pycache__'}.intersection(p.relative_to(HOME).parts)
         and p.suffix in {'.tex','.py','.md','.json'} and p.name!='assemble_revision.py'}
    digest=hashlib.sha256(json.dumps(own,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    require(digest==OWN,'Native output inventory mismatch')
    print(json.dumps({'status':'readable-native-source-materialized','own_files':len(own),'retained_files':285,'qualification':'not yet run'}))

if __name__=='__main__':main()
