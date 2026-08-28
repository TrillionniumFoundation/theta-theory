#!/usr/bin/env python3
"""Round306B1AF4K1 exact semantic checker foundation, with zero theorem credit.

The implemented algorithms check only finite exact certificates.  They do not
read construction data, construct normalized support, constitute formal B1A,
authorize B2, or mint any mathematical/CM2 credit.  Public print/self-test
modes are filesystem inert.  Only ``--verify-dependencies`` reads the two
frozen semantic sources.  Every other mode is silently refused before all
filesystem and output boundaries.
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from fractions import Fraction
import hashlib
from itertools import product
import json
from math import isqrt
import os
from pathlib import Path
import re
import stat
import sys
import tempfile
from typing import Any, Callable, Iterable, Mapping, NoReturn, Sequence
from unittest import mock


class CheckBlocked(ValueError): pass
class ModeBlocked(RuntimeError): pass
def need(ok: bool, label: str) -> None:
    if not ok: raise CheckBlocked(label)


SCHEMA = "cm2.round306b1af4k1.source-g-semantic-theorem-kernel.v1"
STATUS = "PASS_EXACT_EXECUTABLE_CHECKER_FOUNDATION__ZERO_FORMAL_THEOREM_CREDIT"
REFUSAL = "AF4K1 candidate/production unavailable before filesystem/output boundaries"
DEPENDENCY_DIRECTORY = Path(__file__).parent
DEPENDENCY_PINS = (
    {"label":"Round306B1AF4_SYMBOLIC_KERNEL_FINAL",
     "filename":"cm2_round306b1af4_source_g_normalized_support_symbolic_kernel.py",
     "exact_size":87237,
     "source_sha256":"c8bb9cf85aace782639859c33625732bf866a7fad34ff31cce58ab84af9f6a6f"},
    {"label":"Round306B1AF4D1_SEMANTIC_WIRE_DELTA_FINAL",
     "filename":"cm2_round306b1af4d1_source_g_semantic_wire_delta_contract.py",
     "exact_size":84392,
     "source_sha256":"5082df54ea4c514de906f4a923856adb20c6240c9be33401e784b2513a85f09f"},
)
NAME=re.compile(r"^[A-Za-z][A-Za-z0-9_.:-]{0,127}$")
IDENT=re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.:/+\-]{0,511}$")
HEX64=re.compile(r"^[0-9a-f]{64}$")
MAX_BITS=4096; MAX_DEPTH=256; MAX_NODES=200000; MAX_BOXES=4096; MAX_ATOMS=2000000
MAX_JSON_STRING_CHARS=1<<20; MAX_CANONICAL_JSON_BYTES=64<<20
SCALAR="SCALAR"; PREDICATE="PREDICATE"
OPS=("CONST_Q","VAR","NEG","ADD","SUB","MUL","DIV_NONZERO","SQUARE",
     "SQRT_POSITIVE","EQ_ZERO","LT_ZERO","GT_ZERO","LE_ZERO","GE_ZERO",
     "AND","OR_DISJOINT","RESTRICT")


def canonical_bytes(x: Any) -> bytes:
    return json.dumps(x,ensure_ascii=True,allow_nan=False,sort_keys=True,
                      separators=(",",":")).encode("ascii")
def digest(x: Any) -> str: return hashlib.sha256(canonical_bytes(x)).hexdigest()
def _snapshot_canonical_json_tree(x:Any,label:str)->Any:
    """Copy a bounded, acyclic, type-strict JSON tree away from caller state."""
    count=[0];budget=[0];active:set[int]=set()
    def charge(amount:int)->None:
        budget[0]+=amount;need(budget[0]<=MAX_CANONICAL_JSON_BYTES,label+" aggregate byte bound")
    def rec(value:Any,depth:int)->Any:
        need(depth<=MAX_DEPTH,label+" depth");count[0]+=1;need(count[0]<=MAX_NODES,label+" nodes")
        kind=type(value)
        charge(2)
        if value is None or kind is bool:charge(len(canonical_bytes(value)));return value
        if kind is int:
            need(value.bit_length()<=MAX_BITS,label+" integer bound");charge(len(canonical_bytes(value)));return value
        if kind is str:
            need(len(value)<=MAX_JSON_STRING_CHARS,label+" string bound");charge(len(canonical_bytes(value)));return value
        need(kind in {dict,list},label+" strict JSON type")
        marker=id(value);need(marker not in active,label+" cycle");active.add(marker)
        if kind is dict:
            need(count[0]+len(value)<=MAX_NODES,label+" key bound")
            out:Any={}
            for key,item in value.items():
                need(type(key) is str and len(key)<=MAX_JSON_STRING_CHARS,label+" string keys")
                count[0]+=1;charge(len(canonical_bytes(key))+1);out[key]=rec(item,depth+1)
        else:
            out=[]
            for item in value:out.append(rec(item,depth+1))
        active.remove(marker)
        return out
    try:snapshot=rec(x,0)
    except CheckBlocked:raise
    except (RuntimeError,TypeError,ValueError,OverflowError,RecursionError) as error:
        raise CheckBlocked(label+" snapshot failed") from error
    need(len(canonical_bytes(snapshot))<=MAX_CANONICAL_JSON_BYTES,label+" canonical byte bound")
    return snapshot
def _validate_canonical_json_tree(x:Any,label:str)->None:_snapshot_canonical_json_tree(x,label)
def _checked_result(kernel_id:str,canonical_input:Any,result_fields:Mapping[str,Any])->dict[str,Any]:
    """Bind a mechanical result digest to its complete canonical input wire."""
    need(isinstance(kernel_id,str) and IDENT.fullmatch(kernel_id) is not None,"result kernel id")
    need(isinstance(result_fields,Mapping) and
         "kernel_id" not in result_fields and
         "canonical_input_commitment_sha256" not in result_fields and
         "check_digest_sha256" not in result_fields,"result fields")
    canonical_input=_snapshot_canonical_json_tree(canonical_input,"canonical input")
    commitment_wire={"schema":SCHEMA+".canonical-check-input.v1",
                     "kernel_id":kernel_id,"input":deepcopy(canonical_input)}
    body={"kernel_id":kernel_id,**dict(result_fields),
          "canonical_input_commitment_sha256":digest(commitment_wire)}
    return {**body,"check_digest_sha256":digest(body)}
def ident(x: Any,label: str) -> str:
    need(isinstance(x,str) and IDENT.fullmatch(x) is not None,label); return x
def as_q(x: Any,label: str="rational") -> Fraction:
    need(isinstance(x,Mapping) and set(x)=={"numerator","denominator"},label+" wire")
    n,d=x["numerator"],x["denominator"]
    need(type(n) is int and type(d) is int and d>0,label+" integers")
    q=Fraction(n,d)
    need(q.numerator==n and q.denominator==d and n.bit_length()<=MAX_BITS and
         d.bit_length()<=MAX_BITS,label+" reduced/bounded")
    return q
def qw(x: int|Fraction) -> dict[str,int]:
    q=Fraction(x); need(q.numerator.bit_length()<=MAX_BITS and q.denominator.bit_length()<=MAX_BITS,"q bound")
    return {"numerator":q.numerator,"denominator":q.denominator}


@dataclass(frozen=True)
class Interval:
    lower: Fraction; upper: Fraction
    def __post_init__(self)->None:
        need(type(self.lower) is Fraction and type(self.upper) is Fraction and self.lower<=self.upper,"interval")
    @classmethod
    def point(cls,x: int|Fraction)->"Interval": q=Fraction(x); return cls(q,q)
    @classmethod
    def from_wire(cls,x:Any)->"Interval":
        need(isinstance(x,Mapping) and set(x)=={"lower","upper"},"interval wire")
        return cls(as_q(x["lower"]),as_q(x["upper"]))
    def wire(self)->dict[str,Any]: return {"lower":qw(self.lower),"upper":qw(self.upper)}
    def neg(self)->"Interval": return Interval(-self.upper,-self.lower)
    def add(self,o:"Interval")->"Interval": return Interval(self.lower+o.lower,self.upper+o.upper)
    def sub(self,o:"Interval")->"Interval": return self.add(o.neg())
    def mul(self,o:"Interval")->"Interval":
        p=(self.lower*o.lower,self.lower*o.upper,self.upper*o.lower,self.upper*o.upper)
        return Interval(min(p),max(p))
    def square(self)->"Interval":
        p=(self.lower*self.lower,self.upper*self.upper)
        return Interval(Fraction(0) if self.lower<=0<=self.upper else min(p),max(p))
    def div(self,o:"Interval")->"Interval":
        need(not o.lower<=0<=o.upper,"division excludes zero")
        r=Interval(min(Fraction(1,o.lower),Fraction(1,o.upper)),max(Fraction(1,o.lower),Fraction(1,o.upper)))
        return self.mul(r)
    def excludes_zero(self)->bool: return self.upper<0 or self.lower>0


def sqrt_iv(x:Interval)->Interval:
    need(x.lower>0,"sqrt positive")
    scale=1<<96
    def floor(q:Fraction)->Fraction: return Fraction(isqrt((q.numerator*scale*scale)//q.denominator),scale)
    lo,hi=floor(x.lower),floor(x.upper)
    if hi*hi!=x.upper: hi+=Fraction(1,scale)
    need(lo*lo<=x.lower and hi*hi>=x.upper,"sqrt outward")
    return Interval(lo,hi)
def c(x:int|Fraction)->dict[str,Any]: return {"op":"CONST_Q","value":qw(x)}
def v(name:str)->dict[str,Any]: need(NAME.fullmatch(name) is not None,"var"); return {"op":"VAR","name":name}
def _exact(x:Mapping[str,Any],keys:set[str],label:str)->None: need(set(x)==keys,label+" keys")


def infer_type(node:Any)->str:
    count=[0]
    def rec(x:Any,depth:int)->str:
        need(depth<=MAX_DEPTH,"AST depth"); count[0]+=1; need(count[0]<=MAX_NODES,"AST nodes")
        need(isinstance(x,Mapping) and x.get("op") in OPS,"supported AST")
        op=x["op"]
        if op=="CONST_Q": _exact(x,{"op","value"},op); as_q(x["value"]); return SCALAR
        if op=="VAR": _exact(x,{"op","name"},op); need(isinstance(x["name"],str) and NAME.fullmatch(x["name"]),"var"); return SCALAR
        if op in {"NEG","SQUARE","SQRT_POSITIVE"}:
            _exact(x,{"op","arg"},op); need(rec(x["arg"],depth+1)==SCALAR,op); return SCALAR
        if op in {"ADD","MUL"}:
            _exact(x,{"op","args"},op); need(isinstance(x["args"],list) and len(x["args"])>=2,op+" arity")
            need(all(rec(a,depth+1)==SCALAR for a in x["args"]),op); return SCALAR
        if op in {"SUB","DIV_NONZERO"}:
            _exact(x,{"op","left","right"},op); need(rec(x["left"],depth+1)==rec(x["right"],depth+1)==SCALAR,op); return SCALAR
        if op in {"EQ_ZERO","LT_ZERO","GT_ZERO","LE_ZERO","GE_ZERO"}:
            _exact(x,{"op","arg"},op); need(rec(x["arg"],depth+1)==SCALAR,op); return PREDICATE
        if op in {"AND","OR_DISJOINT"}:
            _exact(x,{"op","args"},op); need(isinstance(x["args"],list) and len(x["args"])>=2,op+" arity")
            need(all(rec(a,depth+1)==PREDICATE for a in x["args"]),op)
            if op=="OR_DISJOINT": need(len({canonical_bytes(a) for a in x["args"]})==len(x["args"]),"OR dup")
            return PREDICATE
        _exact(x,{"op","predicate","domain"},op)
        need(rec(x["predicate"],depth+1)==rec(x["domain"],depth+1)==PREDICATE,"restrict"); return PREDICATE
    return rec(node,0)
def _cv(x:Mapping[str,Any])->Fraction|None: return as_q(x["value"]) if x.get("op")=="CONST_Q" else None
def _perfect_sqrt(q:Fraction)->Fraction|None:
    if q<0:return None
    n,d=isqrt(q.numerator),isqrt(q.denominator)
    return Fraction(n,d) if n*n==q.numerator and d*d==q.denominator else None


def normalize(node:Any)->dict[str,Any]:
    infer_type(node)
    def rec(x:Mapping[str,Any])->dict[str,Any]:
        op=x["op"]
        if op=="CONST_Q":return c(as_q(x["value"]))
        if op=="VAR":return v(x["name"])
        if op=="NEG":
            a=rec(x["arg"]); q=_cv(a)
            return c(-q) if q is not None else (a["arg"] if a["op"]=="NEG" else {"op":op,"arg":a})
        if op in {"ADD","MUL"}:
            flat=[]
            for raw in x["args"]:
                a=rec(raw); flat.extend(a["args"] if a["op"]==op else [a])
            sy=[]; qs=[]
            for a in flat:
                q=_cv(a); (qs if q is not None else sy).append(q if q is not None else a)
            if op=="ADD":
                q=sum(qs,Fraction(0))
                if q or not sy:sy.append(c(q))
            else:
                q=Fraction(1)
                for z in qs:q*=z
                if q==0:return c(0)
                if q!=1 or not sy:sy.append(c(q))
            sy.sort(key=canonical_bytes); return sy[0] if len(sy)==1 else {"op":op,"args":sy}
        if op=="SUB":
            l,r=rec(x["left"]),rec(x["right"]); lq,rq=_cv(l),_cv(r)
            return c(lq-rq) if lq is not None and rq is not None else (l if rq==0 else {"op":op,"left":l,"right":r})
        if op=="DIV_NONZERO":
            l,r=rec(x["left"]),rec(x["right"]); lq,rq=_cv(l),_cv(r); need(rq!=0,"division zero")
            if lq is not None and rq is not None:return c(lq/rq)
            if lq==0:return c(0)
            return l if rq==1 else {"op":op,"left":l,"right":r}
        if op=="SQUARE":
            a=rec(x["arg"]); q=_cv(a)
            if q is not None:return c(q*q)
            return {"op":op,"arg":a["arg"] if a["op"]=="NEG" else a}
        if op=="SQRT_POSITIVE":
            a=rec(x["arg"]); q=_cv(a)
            if q is not None:
                need(q>0,"sqrt constant"); z=_perfect_sqrt(q)
                if z is not None:return c(z)
            return {"op":op,"arg":a}
        if op in {"EQ_ZERO","LT_ZERO","GT_ZERO","LE_ZERO","GE_ZERO"}:return {"op":op,"arg":rec(x["arg"])}
        if op in {"AND","OR_DISJOINT"}:
            flat=[]
            for raw in x["args"]:
                a=rec(raw); flat.extend(a["args"] if a["op"]==op else [a])
            keyed=sorted((canonical_bytes(a),a) for a in flat)
            if op=="AND":
                out=[]
                for key,a in keyed:
                    if not out or key!=canonical_bytes(out[-1]):out.append(a)
                return out[0] if len(out)==1 else {"op":op,"args":out}
            need(len(keyed)==len({k for k,_ in keyed}),"OR normalized dup"); return {"op":op,"args":[a for _,a in keyed]}
        return {"op":op,"predicate":rec(x["predicate"]),"domain":rec(x["domain"])}
    out=rec(node); infer_type(out); return out


def differentiate(node:Any,variable:str)->dict[str,Any]:
    need(isinstance(variable,str) and NAME.fullmatch(variable),"derivative variable")
    ast=normalize(node); need(infer_type(ast)==SCALAR,"derivative scalar")
    def d(x:Mapping[str,Any])->dict[str,Any]:
        op=x["op"]
        if op=="CONST_Q":return c(0)
        if op=="VAR":return c(x["name"]==variable)
        if op=="NEG":return {"op":"NEG","arg":d(x["arg"])}
        if op=="ADD":return {"op":"ADD","args":[d(a) for a in x["args"]]}
        if op=="SUB":return {"op":"SUB","left":d(x["left"]),"right":d(x["right"])}
        if op=="MUL":
            return {"op":"ADD","args":[{"op":"MUL","args":[d(a) if i==j else deepcopy(a) for j,a in enumerate(x["args"])]} for i in range(len(x["args"]))]}
        if op=="DIV_NONZERO":
            num={"op":"SUB","left":{"op":"MUL","args":[d(x["left"]),deepcopy(x["right"])]},"right":{"op":"MUL","args":[deepcopy(x["left"]),d(x["right"])]}}
            return {"op":"DIV_NONZERO","left":num,"right":{"op":"SQUARE","arg":deepcopy(x["right"])}}
        if op=="SQUARE":return {"op":"MUL","args":[c(2),deepcopy(x["arg"]),d(x["arg"])]}
        if op=="SQRT_POSITIVE":return {"op":"DIV_NONZERO","left":d(x["arg"]),"right":{"op":"MUL","args":[c(2),deepcopy(x)]}}
        raise CheckBlocked("unsupported derivative:"+op)
    return normalize(d(ast))


def substitute(node:Any,replacements:Mapping[str,Any])->dict[str,Any]:
    ast=normalize(node); repl={}
    for name,expr in replacements.items():
        need(NAME.fullmatch(name) is not None,"sub var"); expr=normalize(expr); need(infer_type(expr)==SCALAR,"sub scalar"); repl[name]=expr
    def rec(x:Mapping[str,Any])->dict[str,Any]:
        op=x["op"]
        if op=="VAR" and x["name"] in repl:return deepcopy(repl[x["name"]])
        if op in {"CONST_Q","VAR"}:return dict(x)
        if op in {"NEG","SQUARE","SQRT_POSITIVE","EQ_ZERO","LT_ZERO","GT_ZERO","LE_ZERO","GE_ZERO"}:return {"op":op,"arg":rec(x["arg"])}
        if op in {"ADD","MUL","AND","OR_DISJOINT"}:return {"op":op,"args":[rec(a) for a in x["args"]]}
        if op in {"SUB","DIV_NONZERO"}:return {"op":op,"left":rec(x["left"]),"right":rec(x["right"])}
        return {"op":op,"predicate":rec(x["predicate"]),"domain":rec(x["domain"])}
    return normalize(rec(ast))


def ast_variables(node:Any)->set[str]:
    """Return the exact free-variable set of this binder-free AST."""
    ast=normalize(node);out:set[str]=set()
    def rec(x:Mapping[str,Any])->None:
        op=x["op"]
        if op=="VAR":out.add(x["name"]);return
        if op=="CONST_Q":return
        if op in {"NEG","SQUARE","SQRT_POSITIVE","EQ_ZERO","LT_ZERO","GT_ZERO","LE_ZERO","GE_ZERO"}:rec(x["arg"]);return
        if op in {"ADD","MUL","AND","OR_DISJOINT"}:
            for a in x["args"]:rec(a)
            return
        if op in {"SUB","DIV_NONZERO"}:rec(x["left"]);rec(x["right"]);return
        rec(x["predicate"]);rec(x["domain"])
    rec(ast);return out


def ast_operator_set(node:Any)->set[str]:
    """Return operators without normalizing away domain restrictions."""
    infer_type(node);out:set[str]=set()
    def rec(x:Mapping[str,Any])->None:
        op=x["op"];out.add(op)
        if op in {"CONST_Q","VAR"}:return
        if op in {"NEG","SQUARE","SQRT_POSITIVE","EQ_ZERO","LT_ZERO","GT_ZERO","LE_ZERO","GE_ZERO"}:rec(x["arg"]);return
        if op in {"ADD","MUL","AND","OR_DISJOINT"}:
            for a in x["args"]:rec(a)
            return
        if op in {"SUB","DIV_NONZERO"}:rec(x["left"]);rec(x["right"]);return
        rec(x["predicate"]);rec(x["domain"])
    rec(node);return out


def eval_interval(node:Any,env:Mapping[str,Interval])->Interval|str:
    # Deliberately evaluate the validated *raw* tree.  Normalizing first could
    # erase a domain restriction such as 0 / g at a cell where g contains 0.
    ast=deepcopy(node);infer_type(ast);need(all(isinstance(k,str) and NAME.fullmatch(k) and isinstance(z,Interval) for k,z in env.items()),"env")
    def scalar(x:Mapping[str,Any])->Interval:
        op=x["op"]
        if op=="CONST_Q":return Interval.point(as_q(x["value"]))
        if op=="VAR":need(x["name"] in env,"bound var");return env[x["name"]]
        if op=="NEG":return scalar(x["arg"]).neg()
        if op=="ADD":
            out=Interval.point(0)
            for a in x["args"]:out=out.add(scalar(a))
            return out
        if op=="SUB":return scalar(x["left"]).sub(scalar(x["right"]))
        if op=="MUL":
            out=Interval.point(1)
            for a in x["args"]:out=out.mul(scalar(a))
            return out
        if op=="DIV_NONZERO":return scalar(x["left"]).div(scalar(x["right"]))
        if op=="SQUARE":return scalar(x["arg"]).square()
        if op=="SQRT_POSITIVE":return sqrt_iv(scalar(x["arg"]))
        raise CheckBlocked("predicate as scalar")
    def pred(x:Mapping[str,Any])->str:
        op=x["op"]
        if op in {"EQ_ZERO","LT_ZERO","GT_ZERO","LE_ZERO","GE_ZERO"}:
            z=scalar(x["arg"])
            if op=="EQ_ZERO":return "TRUE" if z.lower==z.upper==0 else ("FALSE" if z.excludes_zero() else "UNKNOWN")
            if op=="LT_ZERO":return "TRUE" if z.upper<0 else ("FALSE" if z.lower>=0 else "UNKNOWN")
            if op=="GT_ZERO":return "TRUE" if z.lower>0 else ("FALSE" if z.upper<=0 else "UNKNOWN")
            if op=="LE_ZERO":return "TRUE" if z.upper<=0 else ("FALSE" if z.lower>0 else "UNKNOWN")
            return "TRUE" if z.lower>=0 else ("FALSE" if z.upper<0 else "UNKNOWN")
        if op in {"AND","OR_DISJOINT"}:
            vals=[pred(a) for a in x["args"]]
            if op=="AND":return "FALSE" if "FALSE" in vals else ("TRUE" if all(a=="TRUE" for a in vals) else "UNKNOWN")
            return "TRUE" if "TRUE" in vals else ("FALSE" if all(a=="FALSE" for a in vals) else "UNKNOWN")
        vals=[pred(x["predicate"]),pred(x["domain"])]
        return "FALSE" if "FALSE" in vals else ("TRUE" if all(a=="TRUE" for a in vals) else "UNKNOWN")
    return scalar(ast) if infer_type(ast)==SCALAR else pred(ast)


@dataclass(frozen=True)
class Axis:
    name:str; lower:Fraction; lower_closed:bool; upper:Fraction; upper_closed:bool
@dataclass(frozen=True)
class Box:
    coordinate_parameter:str; axes:tuple[Axis,...]
    @classmethod
    def from_wire(cls,x:Any)->"Box":
        need(isinstance(x,Mapping) and set(x)=={"wire_id","coordinate_parameter","axes"},"box fields")
        need(x["wire_id"]=="RATIONAL_INTERVAL_BOX_V1","box id"); coordinate=ident(x["coordinate_parameter"],"coordinate")
        rows=x["axes"]; need(isinstance(rows,list) and 1<=len(rows)<=16,"axes")
        out=[]
        for row in rows:
            need(isinstance(row,Mapping) and set(row)=={"axis","lower","lower_closed","upper","upper_closed"},"axis fields")
            name=row["axis"]; need(isinstance(name,str) and NAME.fullmatch(name),"axis name")
            lo,hi=as_q(row["lower"]),as_q(row["upper"])
            need(type(row["lower_closed"]) is bool and type(row["upper_closed"]) is bool and lo<hi,"axis interval")
            out.append(Axis(name,lo,row["lower_closed"],hi,row["upper_closed"]))
        names=[a.name for a in out]
        expected=["t","p","s"] if coordinate=="TPS" else sorted(names,key=lambda z:z.encode("ascii"))
        need(names==expected and len(names)==len(set(names)),"canonical axes")
        return cls(coordinate,tuple(out))
    def environment(self)->dict[str,Interval]:return {a.name:Interval(a.lower,a.upper) for a in self.axes}


def _contains(a:Axis,kind:str,lo:Fraction,hi:Fraction|None)->bool:
    if kind=="POINT":
        return (a.lower<lo or (a.lower==lo and a.lower_closed)) and (lo<a.upper or (lo==a.upper and a.upper_closed))
    need(hi is not None and lo<hi,"atom"); return a.lower<=lo and hi<=a.upper
def _atoms(parent:Box,children:Sequence[Box],face:tuple[str,Fraction]|None)->Iterable[Any]:
    names=tuple(a.name for a in parent.axes)
    need(all(z.coordinate_parameter==parent.coordinate_parameter and tuple(a.name for a in z.axes)==names for z in children),"same coordinate/axes")
    per=[]; total=1
    for i,a in enumerate(parent.axes):
        ends={a.lower,a.upper}
        for z in children:ends.update((z.axes[i].lower,z.axes[i].upper))
        if face is not None and a.name==face[0]: atoms=[("POINT",face[1],None)]
        else:
            order=sorted(ends); atoms=[]
            for j,q in enumerate(order):
                atoms.append(("POINT",q,None))
                if j+1<len(order):atoms.append(("OPEN",q,order[j+1]))
        per.append(atoms);total*=len(atoms);need(total<=MAX_ATOMS,"atom bound")
    return product(*per)


def check_box_partition(parent_wire:Any,child_wires:Any,face:tuple[str,Fraction]|None=None)->dict[str,Any]:
    if face is not None:
        need(type(face) is tuple and len(face)==2 and type(face[0]) is str and
             NAME.fullmatch(face[0]) is not None and type(face[1]) is Fraction,"face exact typed wire")
    entry_input=_snapshot_canonical_json_tree(
      {"parent_box":parent_wire,"child_boxes":child_wires,
       "face":None if face is None else {"axis":face[0],"endpoint":qw(face[1])}},"box partition input")
    parent_wire=entry_input["parent_box"];child_wires=entry_input["child_boxes"]
    face_wire=entry_input["face"]
    face=None if face_wire is None else (face_wire["axis"],as_q(face_wire["endpoint"],"face endpoint"))
    parent=Box.from_wire(parent_wire)
    need(isinstance(child_wires,list) and 1<=len(child_wires)<=MAX_BOXES,"child boxes")
    children=[Box.from_wire(x) for x in child_wires]
    for child in children:
        need(len(child.axes)==len(parent.axes),"child dimension")
        for pa,ca in zip(parent.axes,child.axes):
            need(pa.name==ca.name and pa.lower<=ca.lower<ca.upper<=pa.upper,"child subset bounds")
            need(not (ca.lower==pa.lower and ca.lower_closed and not pa.lower_closed),"child lower outside parent")
            need(not (ca.upper==pa.upper and ca.upper_closed and not pa.upper_closed),"child upper outside parent")
    if face is not None:
        axis=next((a for a in parent.axes if a.name==face[0]),None)
        need(axis is not None and face[1] in {axis.lower,axis.upper} and _contains(axis,"POINT",face[1],None),"included parent face")
        index=next(i for i,a in enumerate(parent.axes) if a.name==face[0])
        need(all(_contains(child.axes[index],"POINT",face[1],None) for child in children),
             "every face child intersects selected face")
    count=0
    for atom in _atoms(parent,children,face):
        if not all(_contains(a,*piece) for a,piece in zip(parent.axes,atom)):continue
        count+=1;hits=sum(all(_contains(a,*piece) for a,piece in zip(z.axes,atom)) for z in children)
        need(hits==1,"box partition gap or overlap")
    need(count>0,"nonempty partition")
    return _checked_result("RATIONAL_BOX_PARTITION_V1",entry_input,
      {"mechanically_checked":True,"child_count":len(children),"atom_count":count,
       "scope":"FACE" if face else "FULL_BOX","formal_credit":0})


def check_regular_trace(cert:Any)->dict[str,Any]:
    cert=_snapshot_canonical_json_tree(cert,"regular trace certificate")
    keys={"wire_id","factor_ast","derivative_ast","graph_variable","side_sign",
          "ambient_box","cells","claimed_approach_face_by_cell"}
    need(isinstance(cert,Mapping) and set(cert)==keys,"trace fields")
    need(cert["wire_id"]=="REGULAR_LEVELSET_ONE_SIDED_TRACE_CERT_V1","trace id")
    graph=cert["graph_variable"];need(isinstance(graph,str) and NAME.fullmatch(graph),"graph var")
    need(type(cert["side_sign"]) is int and cert["side_sign"] in (-1,1),"side sign")
    raw_factor,raw_derivative=cert["factor_ast"],cert["derivative_ast"]
    factor=normalize(raw_factor);derivative=normalize(raw_derivative)
    need(infer_type(factor)==SCALAR and derivative==differentiate(factor,graph),"exact derivative")
    ambient=Box.from_wire(cert["ambient_box"]);need(graph in [a.name for a in ambient.axes],"graph axis")
    check_box_partition(cert["ambient_box"],cert["cells"])
    cells=[Box.from_wire(x) for x in cert["cells"]]
    graph_index=next(i for i,a in enumerate(ambient.axes) if a.name==graph)
    ambient_graph_axis=ambient.axes[graph_index]
    need(all(box.axes[graph_index]==ambient_graph_axis for box in cells),
         "trace cells may partition base axes but not graph axis")
    claims=cert["claimed_approach_face_by_cell"]
    need(isinstance(claims,list) and len(claims)==len(cells),"trace claims")
    expected=[]
    for i,box in enumerate(cells):
        env=box.environment(); di=eval_interval(raw_derivative,env)
        need(isinstance(di,Interval) and di.excludes_zero(),"strict derivative")
        ds=1 if di.lower>0 else -1;axis=next(a for a in box.axes if a.name==graph)
        lo,hi=dict(env),dict(env);lo[graph]=Interval.point(axis.lower);hi[graph]=Interval.point(axis.upper)
        # Full-cell evaluation checks every raw DIV_NONZERO/SQRT_POSITIVE
        # domain before endpoint signs are used.
        eval_interval(raw_factor,env)
        flo,fhi=eval_interval(raw_factor,lo),eval_interval(raw_factor,hi)
        need(isinstance(flo,Interval) and isinstance(fhi,Interval),"endpoint intervals")
        if ds==1:need(flo.upper<0 and fhi.lower>0,"increasing bracket")
        else:need(flo.lower>0 and fhi.upper<0,"decreasing bracket")
        expected.append({"cell_index":i,"approach_face":"UPPER" if cert["side_sign"]*ds==1 else "LOWER"})
    need(_type_strict_equal(claims,expected),"trace sign/face exact typed wire")
    return _checked_result("REGULAR_LEVELSET_ONE_SIDED_TRACE_V1",cert,
      {"mechanically_checked_sufficient_certificate":True,"cell_count":len(cells),
       "does_not_mint_physical_incidence":True,"formal_theorem_credit":0})


def check_codim2_empty(cert:Any)->dict[str,Any]:
    cert=_snapshot_canonical_json_tree(cert,"codim2 certificate")
    keys={"wire_id","disposition","domain_box","cover_cells","source_factor_ast",
          "target_factor_ast","per_cell_excluded_factor"}
    need(isinstance(cert,Mapping) and set(cert)==keys,"codim2 fields")
    need(cert["wire_id"]=="CODIM2_INTERSECTION_DISPOSITION_CERT_V1","codim id")
    need(cert["disposition"] in {"EMPTY","MATERIALIZED_REGULAR","BLOCKED_SINGULAR"},"explicit disposition")
    if cert["disposition"]!="EMPTY":raise CheckBlocked("unsupported codim2 disposition:"+cert["disposition"])
    raw_source,raw_target=cert["source_factor_ast"],cert["target_factor_ast"]
    source,target=normalize(raw_source),normalize(raw_target)
    need(infer_type(source)==infer_type(target)==SCALAR,"codim scalar")
    check_box_partition(cert["domain_box"],cert["cover_cells"])
    cells=[Box.from_wire(x) for x in cert["cover_cells"]];labels=cert["per_cell_excluded_factor"]
    need(isinstance(labels,list) and len(labels)==len(cells),"exclusion labels")
    for i,box in enumerate(cells):
        si,ti=eval_interval(raw_source,box.environment()),eval_interval(raw_target,box.environment())
        need(isinstance(si,Interval) and isinstance(ti,Interval),"codim intervals")
        allowed=[]
        if si.excludes_zero():allowed.append("SOURCE")
        if ti.excludes_zero():allowed.append("TARGET")
        need(allowed and labels[i] in allowed,"per-cell zero exclusion")
    return _checked_result("CODIM2_INTERSECTION_DISPOSITION_V1",cert,
      {"disposition":"EMPTY","cover_cell_count":len(cells),"mechanically_checked":True,
       "formal_theorem_credit":0})


def check_mixed_face_partition(cert:Any)->dict[str,Any]:
    cert=_snapshot_canonical_json_tree(cert,"mixed-face certificate")
    need(isinstance(cert,Mapping) and set(cert)=={"wire_id","parent_box","face_axis","face_side","child_rows"},"mixed fields")
    need(cert["wire_id"]=="MIXED_BOUNDARY_FACE_PARTITION_CERT_V1","mixed id")
    parent=Box.from_wire(cert["parent_box"]);axis=next((a for a in parent.axes if a.name==cert["face_axis"]),None)
    need(axis is not None and cert["face_side"] in {"LOWER","UPPER"},"face selector")
    endpoint=axis.lower if cert["face_side"]=="LOWER" else axis.upper
    rows=cert["child_rows"];need(isinstance(rows,list) and rows,"face rows")
    ids=[];boxes=[]
    for row in rows:
        need(isinstance(row,Mapping) and set(row)=={"child_box","owner_member_id","row_id"},"face row")
        ids.append(ident(row["row_id"],"row id"));ident(row["owner_member_id"],"owner");boxes.append(row["child_box"])
    need(len(ids)==len(set(ids)),"duplicate face row")
    result=check_box_partition(cert["parent_box"],boxes,(cert["face_axis"],endpoint))
    return _checked_result("MIXED_BOUNDARY_FACE_PARTITION_V1",cert,
      {"child_count":len(rows),"mechanically_checked":True,
       "partition_digest_sha256":result["check_digest_sha256"],"formal_theorem_credit":0})


def check_chart_map(chart:Any)->dict[str,Any]:
    chart=_snapshot_canonical_json_tree(chart,"ChartMap certificate")
    need(isinstance(chart,Mapping) and set(chart)=={"wire_id","source_variables","target_variables","forward_components","inverse_branches"},"chart fields")
    need(chart["wire_id"]=="CHART_MAP_AST_V1","chart id")
    sources,targets=chart["source_variables"],chart["target_variables"]
    need(isinstance(sources,list) and isinstance(targets,list) and sources and targets,"chart vars")
    need(all(isinstance(x,str) and NAME.fullmatch(x) for x in sources+targets),"chart names")
    need(len(sources)==len(set(sources)) and len(targets)==len(set(targets)) and set(sources).isdisjoint(targets),"chart unique")
    need(len(sources)==len(targets),"ChartMap equal dimension")
    fw=chart["forward_components"]
    need(isinstance(fw,list) and [x.get("target_variable") for x in fw]==targets,"forward order")
    fmap={}
    chart_safe_ops={"CONST_Q","VAR","NEG","ADD","SUB","MUL","SQUARE"}
    for row in fw:
        need(isinstance(row,Mapping) and set(row)=={"target_variable","expression_ast"},"forward row")
        need(ast_operator_set(row["expression_ast"])<=chart_safe_ops,"forward ChartMap polynomial subset")
        expr=normalize(row["expression_ast"]);need(infer_type(expr)==SCALAR and ast_variables(expr)<=set(sources),"forward scalar/source variables");fmap[row["target_variable"]]=expr
    branches=chart["inverse_branches"];need(isinstance(branches,list) and branches,"inverse branches")
    ids=[x.get("branch_id") for x in branches]
    need(all(isinstance(x,str) and IDENT.fullmatch(x) for x in ids) and ids==sorted(ids,key=lambda x:x.encode("ascii")) and len(ids)==len(set(ids)),"branch ids")
    for branch in branches:
        need(isinstance(branch,Mapping) and set(branch)=={"branch_id","source_components"},"branch row")
        rows=branch["source_components"];need(isinstance(rows,list) and [x.get("source_variable") for x in rows]==sources,"inverse order")
        imap={}
        for row in rows:
            need(isinstance(row,Mapping) and set(row)=={"source_variable","expression_ast"},"inverse row")
            need(ast_operator_set(row["expression_ast"])<=chart_safe_ops,"inverse ChartMap polynomial subset")
            expr=normalize(row["expression_ast"]);need(infer_type(expr)==SCALAR and ast_variables(expr)<=set(targets),"inverse scalar/target variables");imap[row["source_variable"]]=expr
        for t in targets:need(substitute(fmap[t],imap)==v(t),"forward after inverse identity")
        for s in sources:need(substitute(imap[s],fmap)==v(s),"inverse after forward identity")
    return _checked_result("CHART_MAP_BIJECTION_V1",chart,
      {"branch_count":len(branches),"exact_compositions_checked":2*len(sources)*len(branches),
       "mechanically_checked":True,"branch_domain_cover_theorem_credit":0,
       "formal_theorem_credit":0})


def check_representation_owners(payload:Any)->dict[str,Any]:
    payload=_snapshot_canonical_json_tree(payload,"representation-owner certificate")
    need(isinstance(payload,Mapping) and set(payload)=={"wire_id","member_ids","representation_rows","member_cover_groups"},"owner fields")
    need(payload["wire_id"]=="REPRESENTATION_OWNER_BOOKKEEPING_V1","owner id")
    members=payload["member_ids"]
    need(isinstance(members,list) and members and all(isinstance(x,str) and IDENT.fullmatch(x) for x in members),"members")
    need(members==sorted(members,key=lambda x:x.encode("ascii")) and len(members)==len(set(members)),"member canonical")
    rows=payload["representation_rows"];need(isinstance(rows,list) and rows,"representations")
    need([x.get("representation_row_id") for x in rows]==sorted([x.get("representation_row_id") for x in rows],key=lambda x:x.encode("ascii") if isinstance(x,str) else b""),"canonical representation order")
    owners={};partial=set()
    for row in rows:
        need(isinstance(row,Mapping) and set(row)=={"representation_row_id","owner_member_id","coverage_semantics","cover_group_id"},"representation row")
        rid,owner=ident(row["representation_row_id"],"rep id"),ident(row["owner_member_id"],"rep owner")
        need(rid not in owners and owner in members,"unique rep/existing owner")
        semantics=row["coverage_semantics"];need(semantics in {"FULL_SET_EQUALITY","PARTIAL_INCLUSION"},"coverage semantics")
        group=row["cover_group_id"]
        if semantics=="PARTIAL_INCLUSION":ident(group,"partial group");partial.add(rid)
        else:need(group is None,"full group null")
        owners[rid]=(owner,group)
    groups=payload["member_cover_groups"];need(isinstance(groups,list),"groups")
    need([x.get("cover_group_id") for x in groups]==sorted([x.get("cover_group_id") for x in groups],key=lambda x:x.encode("ascii") if isinstance(x,str) else b""),"canonical group order")
    seen_groups=set();grouped=set();group_owners=set()
    for row in groups:
        need(isinstance(row,Mapping) and set(row)=={"cover_group_id","owner_member_id","representation_row_ids"},"group row")
        gid,owner=ident(row["cover_group_id"],"group id"),ident(row["owner_member_id"],"group owner")
        need(gid not in seen_groups and owner in members and owner not in group_owners,"group unique owner");seen_groups.add(gid);group_owners.add(owner)
        ids=row["representation_row_ids"]
        need(isinstance(ids,list) and ids and ids==sorted(ids,key=lambda x:x.encode("ascii")) and len(ids)==len(set(ids)),"group ids")
        for rid in ids:
            need(rid in owners and owners[rid]==(owner,gid) and rid not in grouped,"group owner binding");grouped.add(rid)
    need(grouped==partial,"partial exactly grouped once")
    need({owner for owner,_group in owners.values()}==set(members),"every member has representation")
    return _checked_result("MEMBER_REPRESENTATION_UNION_COVER_V1",payload,
      {"member_count":len(members),"representation_count":len(rows),
       "partial_representation_count":len(partial),"cover_group_count":len(groups),
       "owner_bookkeeping_mechanically_checked":True,
       "support_inclusion_or_union_theorem_credit":0,"formal_theorem_credit":0})


ROLE_RANK={"AST_NORMALIZATION":0,"INTERVAL_SIGNS":1,"REGULAR_LEVELSET_ONE_SIDED_TRACE":2,
           "MIXED_BOUNDARY_FACE_PARTITION":3,"CHART_MAP_BIJECTION":4,
           "REPRESENTATION_OWNER_BACKBINDING":5,"MEMBER_REPRESENTATION_UNION_COVER":6}
def check_proof_bundle(bundle:Any,required_roles:Sequence[str])->dict[str,Any]:
    need(type(required_roles) in {list,tuple},"required roles container")
    entry_input=_snapshot_canonical_json_tree(
      {"bundle":bundle,"required_roles":list(required_roles)},"proof bundle input")
    bundle=entry_input["bundle"];required_roles=entry_input["required_roles"]
    keys={"wire_id","subject_row_id","claims","dependency_edges","root_claim_ids","bundle_sha256","formal_credit"}
    need(isinstance(bundle,Mapping) and set(bundle)==keys,"bundle fields")
    need(bundle["wire_id"]=="PROOF_BUNDLE_DAG_V1" and type(bundle["formal_credit"]) is int and bundle["formal_credit"]==0,"bundle id/exact integer zero credit");ident(bundle["subject_row_id"],"subject")
    need(type(required_roles) is list and required_roles and
         all(type(x) is str and x in ROLE_RANK for x in required_roles) and len(required_roles)==len(set(required_roles)) and
         list(required_roles)==sorted(required_roles,key=lambda x:ROLE_RANK[x]),"required roles exact canonical set")
    claims=bundle["claims"];need(isinstance(claims,list) and claims,"claims")
    ids=[];roles=[]
    for row in claims:
        need(isinstance(row,Mapping) and set(row)=={"role","claim_id","kernel_id","payload","payload_sha256"},"claim row")
        role=row["role"];need(role in ROLE_RANK,"role");cid=ident(row["claim_id"],"claim id");ident(row["kernel_id"],"kernel id")
        _validate_canonical_json_tree(row["payload"],"claim payload")
        need(isinstance(row["payload_sha256"],str) and HEX64.fullmatch(row["payload_sha256"]) and row["payload_sha256"]==digest(row["payload"]),"payload hash")
        ids.append(cid);roles.append(role)
    need(len(ids)==len(set(ids)),"duplicate claim")
    order=[(ROLE_RANK[x["role"]],x["kernel_id"].encode("ascii"),x["claim_id"].encode("ascii")) for x in claims]
    need(order==sorted(order) and roles==list(required_roles),"claim order/roles")
    edges=bundle["dependency_edges"];need(type(edges) is list,"dependency edges canonical list")
    pairs=[]
    for edge in edges:
        need(isinstance(edge,Mapping) and set(edge)=={"claim_id","depends_on_claim_id"},"edge row")
        pair=(ident(edge["claim_id"],"edge claim"),ident(edge["depends_on_claim_id"],"edge dep"))
        need(pair[0] in ids and pair[1] in ids and pair[0]!=pair[1],"edge local");pairs.append(pair)
    need(len(pairs)==len(set(pairs)) and pairs==sorted(pairs,key=lambda x:(x[0].encode("ascii"),x[1].encode("ascii"))),"edges canonical")
    deps={x:[] for x in ids};consumers={x:0 for x in ids}
    for a,b in pairs:deps[a].append(b);consumers[b]+=1
    visiting=set();done=set()
    def walk(x:str)->None:
        need(x not in visiting,"DAG cycle")
        if x in done:return
        visiting.add(x)
        for y in deps[x]:walk(y)
        visiting.remove(x);done.add(x)
    for x in ids:walk(x)
    roots=sorted([x for x in ids if consumers[x]==0],key=lambda x:x.encode("ascii"))
    need(bundle["root_claim_ids"]==roots,"exact roots")
    hashed={k:deepcopy(bundle[k]) for k in ("wire_id","subject_row_id","claims","dependency_edges","root_claim_ids","formal_credit")}
    need(bundle["bundle_sha256"]==digest(hashed),"bundle hash")
    return _checked_result("PROOF_BUNDLE_DAG_VALIDATION_V1",entry_input,
      {"claim_count":len(claims),"edge_count":len(pairs),"mechanically_checked":True,
       "formal_theorem_credit":0})


def _contract_document()->dict[str,Any]:
    return {
      "schema":SCHEMA,"status":STATUS,"sealed_exact":True,
      "scope":{"executable_checker_foundation":True,"construction_data_read":False,
        "producer":False,"formal_B1A":False,"mechanically_checked_is_not_theorem_credit":True,
        "formal_credit_minted":False,"CM2_credit_minted":False},
      "dependency_seal":{"pins":[dict(x) for x in DEPENDENCY_PINS],"pin_count":2,
        "pin_set_sha256":digest(DEPENDENCY_PINS),"held_dirfd":True,"O_NOFOLLOW":True,
        "nlink_one":True,"two_pass_same_fd":True,"pre_post_fstat":True,
        "path_replacement_fail_closed":True,"final_all_pin_path_revalidation_before_any_fd_close":True,
        "full_directory_fingerprint_stable":True,"dependencies_imported_or_executed":False},
      "implemented_exact_subset":{"AST_operators":list(OPS),"exact_rational_interval_wire":True,
        "interval_evaluation_preserves_raw_DIV_and_SQRT_domain_checks":True,
        "TPS_axis_order":["t","p","s"],"all_other_axis_orders":"ASCII_ASCENDING",
        "symbolic_exact_derivative":True,"finite_box_cover_disjoint_face_partition":True,
        "partition_children_must_be_subsets_and_face_children_must_intersect_face":True,
        "regular_levelset_trace_sufficient_interval_certificate":True,
        "R236_codim2_EMPTY_exhaustive_zero_exclusion":True,"mixed_boundary_face_partition":True,
        "ChartMap_exact_substitution_compositions":True,"representation_owner_group_bookkeeping":True,
        "proof_bundle_DAG_integrity":True},
      "explicit_fail_closed_limits":{
        "codim2_MATERIALIZED_REGULAR":"UNSUPPORTED_WITHOUT_COMPLETE_NONEMPTY_RANK_FACE_RECOMPUTATION",
        "codim2_BLOCKED_SINGULAR":"UNSUPPORTED_AS_PASSING_CERTIFICATE",
        "ChartMap_branch_domain_cover":"NOT_PROVED_BY_SYMBOLIC_COMPOSITION_ALONE",
        "ChartMap_DIV_or_SQRT":"FAIL_CLOSED_UNTIL_EXACT_BRANCH_DOMAIN_CERTIFICATE_EXISTS",
        "representation_set_inclusion_or_union":"NOT_PROVED_BY_OWNER_BOOKKEEPING",
        "trace_global_source_authority":"NOT_READ_OR_ESTABLISHED",
        "arbitrary_nonlinear_identity":"REJECTED_UNLESS_EXACT_NORMALIZATION_REDUCES_TO_IDENTITY"},
      "security":{"exact_recursive_contract_equality":True,"extra_or_missing_fields_rejected":True,
        "unsupported_AST_or_theorem_rejected":True,"candidate_production_unknown_modes_silent_rc1":True,
        "refusal_before_path_open_temp_write_stdout_stderr":True,
        "check_result_digest_binds_complete_canonical_input_commitment":True,
        "all_public_checkers_use_entry_plain_JSON_snapshot":True,
        "DAG_result_input_binds_bundle_and_required_roles":True,
        "canonical_inputs_and_claim_payloads_are_bounded_strict_JSON_trees":True,
        "face_endpoint_requires_exact_Fraction_not_bool_or_int_alias":True,
        "trace_and_bundle_bool_int_aliases_rejected":True},
      "formal_credit":{"normalized_support":0,"representation_cover":0,"physical_incidence":0,
        "transition":0,"pair_routing":0,"maximality":0,"CM2":0},
      "downstream_state":{"B1A":"BLOCKED","B2":"NOT_AUTHORIZED","D02":"BLOCKED","CM2":"NO-GO_FOR_CLAIM"}}
def _type_strict_equal(left:Any,right:Any)->bool:
    """JSON-tree equality that rejects Python's bool/int value aliasing."""
    if type(left) is not type(right):return False
    if isinstance(left,dict):
        return (left.keys()==right.keys() and
                all(_type_strict_equal(left[key],right[key]) for key in left))
    if isinstance(left,list):
        return len(left)==len(right) and all(_type_strict_equal(a,b) for a,b in zip(left,right))
    return left==right
def validate_contract(document:Any)->None: need(_type_strict_equal(document,_contract_document()),"exact type-strict entire contract")
def contract_envelope()->dict[str,Any]:
    doc=_contract_document();validate_contract(doc);return {"contract":doc,"canonical_contract_digest_sha256":digest(doc)}


def _fp(x:os.stat_result)->tuple[int,...]:
    return (x.st_dev,x.st_ino,x.st_mode,x.st_nlink,x.st_size,x.st_mtime_ns,x.st_ctime_ns)
def _did(x:os.stat_result)->tuple[int,int,int]:return (x.st_dev,x.st_ino,x.st_mode)
def _hash_fd(fd:int)->tuple[int,str]:
    os.lseek(fd,0,os.SEEK_SET);total=0;h=hashlib.sha256()
    while True:
        block=os.read(fd,1<<20)
        if not block:break
        total+=len(block);h.update(block)
    return total,h.hexdigest()
def verify_dependencies()->dict[str,Any]:
    directory=os.fspath(DEPENDENCY_DIRECTORY);path_dir=os.stat(directory,follow_symlinks=False)
    need(stat.S_ISDIR(path_dir.st_mode),"dep dir")
    dflags=os.O_RDONLY|getattr(os,"O_DIRECTORY",0)|getattr(os,"O_CLOEXEC",0)|getattr(os,"O_NOFOLLOW",0)
    dfd=os.open(directory,dflags);opened=[];rows=[]
    try:
        held_dir=os.fstat(dfd);need(_fp(path_dir)==_fp(held_dir),"dir race")
        try:
            for pin in DEPENDENCY_PINS:
                name=pin["filename"];need(name==os.path.basename(name) and name not in {"",".",".."},"basename")
                before=os.stat(name,dir_fd=dfd,follow_symlinks=False)
                need(stat.S_ISREG(before.st_mode) and before.st_nlink==1 and before.st_size==pin["exact_size"],"dep metadata")
                fd=os.open(name,os.O_RDONLY|getattr(os,"O_CLOEXEC",0)|getattr(os,"O_NOFOLLOW",0),dir_fd=dfd)
                held=os.fstat(fd);need(_fp(before)==_fp(held),"open race");opened.append((pin,fd,held))
            for pin,fd,held in opened:
                s1,h1=_hash_fd(fd);need(_fp(os.fstat(fd))==_fp(held),"pass1 race")
                s2,h2=_hash_fd(fd);need(_fp(os.fstat(fd))==_fp(held),"pass2 race")
                need(_fp(os.stat(pin["filename"],dir_fd=dfd,follow_symlinks=False))==_fp(held),"path replacement")
                need(s1==s2==pin["exact_size"] and h1==h2==pin["source_sha256"],"dep bytes")
                rows.append({"label":pin["label"],"filename":pin["filename"],"size":s1,"sha256":h1,"held_fd_stable":True})
            # A path checked after its own hash can still be replaced while a
            # later pin is being hashed.  Revalidate the complete path set,
            # while every original fd remains held, before closing any fd.
            for pin,fd,held in opened:
                need(_fp(os.fstat(fd))==_fp(held),"final held-fd replacement")
                final_path=os.stat(pin["filename"],dir_fd=dfd,follow_symlinks=False)
                need(_fp(final_path)==_fp(held),"late dependency path replacement")
        finally:
            for _,fd,_ in reversed(opened):os.close(fd)
        need(_fp(held_dir)==_fp(os.fstat(dfd))==_fp(os.stat(directory,follow_symlinks=False)),"dir replaced")
    finally:os.close(dfd)
    body={"schema":SCHEMA+".dependency-verification.v1","status":"PASS","pin_count":2,
          "pin_set_sha256":digest(DEPENDENCY_PINS),"raw_bytes_only":True,
          "all_file_fds_open_before_first_hash":True,
          "final_all_pin_path_revalidation_before_any_fd_close":True,
          "full_directory_fingerprint_stable":True,"files":rows,"formal_credit":0}
    return {**body,"verification_digest_sha256":digest(body)}


def _box(rows:Sequence[tuple[str,int|Fraction,bool,int|Fraction,bool]])->dict[str,Any]:
    return {"wire_id":"RATIONAL_INTERVAL_BOX_V1","coordinate_parameter":"TEST",
            "axes":[{"axis":n,"lower":qw(lo),"lower_closed":lc,"upper":qw(hi),"upper_closed":uc}
                    for n,lo,lc,hi,uc in rows]}
def _blocked(action:Callable[[],Any])->None:
    try:action()
    except CheckBlocked:return
    raise AssertionError("attack accepted")
def _bundle()->dict[str,Any]:
    p0,p1={"normalized":True},{"interval":"strict"}
    claims=[{"role":"AST_NORMALIZATION","claim_id":"c0","kernel_id":"K0","payload":p0,"payload_sha256":digest(p0)},
            {"role":"INTERVAL_SIGNS","claim_id":"c1","kernel_id":"K1","payload":p1,"payload_sha256":digest(p1)}]
    body={"wire_id":"PROOF_BUNDLE_DAG_V1","subject_row_id":"subject","claims":claims,
          "dependency_edges":[{"claim_id":"c1","depends_on_claim_id":"c0"}],"root_claim_ids":["c1"],"formal_credit":0}
    return {**body,"bundle_sha256":digest(body)}


def _positive_tests()->dict[str,int]:
    x,y=v("x"),v("y")
    poly={"op":"ADD","args":[{"op":"SQUARE","arg":x},{"op":"MUL","args":[c(3),x,y]},c(2)]}
    expected=normalize({"op":"ADD","args":[{"op":"MUL","args":[c(2),x]},{"op":"MUL","args":[c(3),y]}]})
    need(differentiate(poly,"x")==expected,"derivative sample")
    need(eval_interval({"op":"LE_ZERO","arg":{"op":"SUB","left":x,"right":c(1)}},{"x":Interval(Fraction(0),Fraction(1))})=="TRUE","LE")
    need(eval_interval({"op":"GE_ZERO","arg":x},{"x":Interval(Fraction(0),Fraction(1))})=="TRUE","GE")
    parent=_box([("x",0,True,2,True)]);children=[_box([("x",0,True,1,False)]),_box([("x",1,True,2,True)])]
    box_result=check_box_partition(parent,children)
    alternate_children=[_box([("x",0,True,Fraction(1,2),False)]),
                        _box([("x",Fraction(1,2),True,2,True)])]
    alternate_box_result=check_box_partition(parent,alternate_children)
    need(_type_strict_equal(
           {key:value for key,value in box_result.items() if key not in {"canonical_input_commitment_sha256","check_digest_sha256"}},
           {key:value for key,value in alternate_box_result.items() if key not in {"canonical_input_commitment_sha256","check_digest_sha256"}}),
         "box digest-separation regression must retain identical result summary")
    need(box_result["canonical_input_commitment_sha256"]!=alternate_box_result["canonical_input_commitment_sha256"] and
         box_result["check_digest_sha256"]!=alternate_box_result["check_digest_sha256"],
         "distinct box certificates require distinct result digests")
    factor={"op":"SUB","left":v("t"),"right":c(Fraction(1,2))};tb=_box([("t",0,True,1,True)])
    trace_cert={"wire_id":"REGULAR_LEVELSET_ONE_SIDED_TRACE_CERT_V1","factor_ast":factor,
      "derivative_ast":c(1),"graph_variable":"t","side_sign":1,"ambient_box":tb,"cells":[tb],
      "claimed_approach_face_by_cell":[{"cell_index":0,"approach_face":"UPPER"}]}
    trace_result=check_regular_trace(trace_cert)
    codim_cert={"wire_id":"CODIM2_INTERSECTION_DISPOSITION_CERT_V1","disposition":"EMPTY",
      "domain_box":parent,"cover_cells":[parent],"source_factor_ast":{"op":"ADD","args":[x,c(1)]},
      "target_factor_ast":{"op":"SUB","left":x,"right":c(1)},"per_cell_excluded_factor":["SOURCE"]}
    codim_result=check_codim2_empty(codim_cert)
    face_parent=_box([("x",0,True,1,True),("y",0,True,2,True)])
    rows=[{"row_id":"r0","owner_member_id":"m0","child_box":_box([("x",0,True,1,True),("y",0,True,1,False)])},
          {"row_id":"r1","owner_member_id":"m1","child_box":_box([("x",0,True,1,True),("y",1,True,2,True)])}]
    mixed_cert={"wire_id":"MIXED_BOUNDARY_FACE_PARTITION_CERT_V1","parent_box":face_parent,
      "face_axis":"x","face_side":"LOWER","child_rows":rows}
    mixed_result=check_mixed_face_partition(mixed_cert)
    chart={"wire_id":"CHART_MAP_AST_V1","source_variables":["x"],"target_variables":["u"],
      "forward_components":[{"target_variable":"u","expression_ast":x}],
      "inverse_branches":[{"branch_id":"b0","source_components":[{"source_variable":"x",
        "expression_ast":v("u") }]}]}
    chart_result=check_chart_map(chart)
    owners={"wire_id":"REPRESENTATION_OWNER_BOOKKEEPING_V1","member_ids":["m0"],
      "representation_rows":[{"representation_row_id":"a","owner_member_id":"m0","coverage_semantics":"FULL_SET_EQUALITY","cover_group_id":None},
        {"representation_row_id":"p","owner_member_id":"m0","coverage_semantics":"PARTIAL_INCLUSION","cover_group_id":"g"}],
      "member_cover_groups":[{"cover_group_id":"g","owner_member_id":"m0","representation_row_ids":["p"]}]}
    owner_result=check_representation_owners(owners)
    alternate_owners=deepcopy(owners);alternate_owners["member_ids"]=["m1"]
    for row in alternate_owners["representation_rows"]:row["owner_member_id"]="m1"
    for row in alternate_owners["member_cover_groups"]:row["owner_member_id"]="m1"
    alternate_owner_result=check_representation_owners(alternate_owners)
    need(_type_strict_equal(
           {key:value for key,value in owner_result.items() if key not in {"canonical_input_commitment_sha256","check_digest_sha256"}},
           {key:value for key,value in alternate_owner_result.items() if key not in {"canonical_input_commitment_sha256","check_digest_sha256"}}),
         "owner digest-separation regression must retain identical result summary")
    need(owner_result["canonical_input_commitment_sha256"]!=alternate_owner_result["canonical_input_commitment_sha256"] and
         owner_result["check_digest_sha256"]!=alternate_owner_result["check_digest_sha256"],
         "distinct owner certificates require distinct result digests")
    bundle=_bundle();dag_result=check_proof_bundle(bundle,["AST_NORMALIZATION","INTERVAL_SIGNS"])
    _box_entry_snapshot_mutation_probe();_trace_entry_snapshot_mutation_probe()
    results=(box_result,alternate_box_result,trace_result,codim_result,mixed_result,chart_result,
             owner_result,alternate_owner_result,dag_result)
    for result in results:
        need(isinstance(result.get("canonical_input_commitment_sha256"),str) and
             HEX64.fullmatch(result["canonical_input_commitment_sha256"]) is not None,
             "canonical input commitment present")
        body={key:deepcopy(value) for key,value in result.items() if key!="check_digest_sha256"}
        need(result["check_digest_sha256"]==digest(body),"result digest covers input commitment")
    return {"derivative":1,"closed_predicates":2,"box_partition":2,"trace":1,"codim2_empty":1,
            "mixed_face":1,"ChartMap":1,"owner_bookkeeping":2,"proof_DAG":1,
            "canonical_input_bound_results":len(results),"distinct_certificate_digest_pairs":2,
            "entry_snapshot_mutation_regressions":2}


def _box_entry_snapshot_mutation_probe()->None:
    """Mutate caller boxes after atom traversal; result must bind entry bytes."""
    parent=_box([("x",0,True,2,True)])
    children=[_box([("x",0,True,1,False)]),_box([("x",1,True,2,True)])]
    expected=check_box_partition(deepcopy(parent),deepcopy(children));raw_atoms=_atoms;mutated=[False]
    def mutating_atoms(*args:Any,**kwargs:Any)->Iterable[Any]:
        yield from raw_atoms(*args,**kwargs)
        children[0]["axes"][0]["upper"]=qw(3);mutated[0]=True
    module=sys.modules[__name__]
    with mock.patch.object(module,"_atoms",new=mutating_atoms):
        actual=check_box_partition(parent,children)
    need(mutated[0] and _type_strict_equal(actual,expected),"box entry snapshot mutation isolation")
    _blocked(lambda:check_box_partition(parent,children))


def _trace_entry_snapshot_mutation_probe()->None:
    """Mutate caller derivative after semantic comparison; commitment stays at entry."""
    tb=_box([("t",0,True,1,True)])
    cert={"wire_id":"REGULAR_LEVELSET_ONE_SIDED_TRACE_CERT_V1",
      "factor_ast":{"op":"SUB","left":v("t"),"right":c(Fraction(1,2))},
      "derivative_ast":c(1),"graph_variable":"t","side_sign":1,"ambient_box":tb,"cells":[tb],
      "claimed_approach_face_by_cell":[{"cell_index":0,"approach_face":"UPPER"}]}
    expected=check_regular_trace(deepcopy(cert));raw_equal=_type_strict_equal;mutated=[False]
    def mutating_equal(left:Any,right:Any)->bool:
        out=raw_equal(left,right)
        cert["derivative_ast"]=c(999);mutated[0]=True
        return out
    module=sys.modules[__name__]
    with mock.patch.object(module,"_type_strict_equal",new=mutating_equal):
        actual=check_regular_trace(cert)
    need(mutated[0] and raw_equal(actual,expected),"trace entry snapshot mutation isolation")
    _blocked(lambda:check_regular_trace(cert))


def _late_dependency_replacement_probe()->None:
    """Model replacement of pin 0 while pin 1 hashes; it must be rejected."""
    def fake(mode:int,ino:int,size:int,stamp:int)->os.stat_result:
        return os.stat_result((mode,ino,7,1,1000,1000,size,stamp,stamp,stamp))
    directory=fake(stat.S_IFDIR|0o700,90,4096,10)
    files={100:fake(stat.S_IFREG|0o600,100,DEPENDENCY_PINS[0]["exact_size"],20),
           101:fake(stat.S_IFREG|0o600,101,DEPENDENCY_PINS[1]["exact_size"],21)}
    replaced=fake(stat.S_IFREG|0o600,999,DEPENDENCY_PINS[0]["exact_size"],99)
    by_name={DEPENDENCY_PINS[0]["filename"]:files[100],DEPENDENCY_PINS[1]["filename"]:files[101]}
    calls={name:0 for name in by_name}
    def fake_stat(path:Any,*_a:Any,**_kw:Any)->os.stat_result:
        if os.fspath(path)==os.fspath(DEPENDENCY_DIRECTORY):return directory
        calls[path]+=1
        return replaced if path==DEPENDENCY_PINS[0]["filename"] and calls[path]>=3 else by_name[path]
    opens=[90,100,101]
    def fake_open(*_a:Any,**_kw:Any)->int:return opens.pop(0)
    def fake_fstat(fd:int)->os.stat_result:return directory if fd==90 else files[fd]
    hashes={100:(DEPENDENCY_PINS[0]["exact_size"],DEPENDENCY_PINS[0]["source_sha256"]),
            101:(DEPENDENCY_PINS[1]["exact_size"],DEPENDENCY_PINS[1]["source_sha256"])}
    module=sys.modules[__name__]
    with (mock.patch.object(os,"stat",side_effect=fake_stat),mock.patch.object(os,"open",side_effect=fake_open),
          mock.patch.object(os,"fstat",side_effect=fake_fstat),mock.patch.object(os,"close",return_value=None),
          mock.patch.object(module,"_hash_fd",side_effect=lambda fd:hashes[fd])):
        verify_dependencies()


def _attacks()->list[tuple[str,Callable[[],Any]]]:
    parent=_box([("x",0,True,2,True)])
    face_alias_parent=_box([("x",0,True,1,True)])
    overlap=[_box([("x",0,True,1,True)]),_box([("x",1,True,2,True)])]
    gap=[_box([("x",0,True,1,False)]),_box([("x",1,False,2,True)])]
    outside=[_box([("x",-1,True,1,False)]),_box([("x",1,True,2,True)])]
    factor={"op":"SUB","left":v("t"),"right":c(Fraction(1,2))};tb=_box([("t",0,True,1,True)])
    trace={"wire_id":"REGULAR_LEVELSET_ONE_SIDED_TRACE_CERT_V1","factor_ast":factor,"derivative_ast":c(2),
      "graph_variable":"t","side_sign":1,"ambient_box":tb,"cells":[tb],
      "claimed_approach_face_by_cell":[{"cell_index":0,"approach_face":"UPPER"}]}
    sign=deepcopy(trace);sign["derivative_ast"]=c(1);sign["claimed_approach_face_by_cell"][0]["approach_face"]="LOWER"
    bool_index=deepcopy(sign);bool_index["claimed_approach_face_by_cell"][0]={"cell_index":False,"approach_face":"UPPER"}
    hidden=deepcopy(sign);hidden["claimed_approach_face_by_cell"][0]["approach_face"]="UPPER"
    hidden["factor_ast"]={"op":"ADD","args":[
      {"op":"DIV_NONZERO","left":c(0),"right":{"op":"SUB","left":v("t"),"right":c(Fraction(1,2))}},factor]}
    codim={"wire_id":"CODIM2_INTERSECTION_DISPOSITION_CERT_V1","disposition":"MATERIALIZED_REGULAR",
      "domain_box":parent,"cover_cells":[parent],"source_factor_ast":v("x"),"target_factor_ast":v("x"),
      "per_cell_excluded_factor":["SOURCE"]}
    chart={"wire_id":"CHART_MAP_AST_V1","source_variables":["x"],"target_variables":["u"],
      "forward_components":[{"target_variable":"u","expression_ast":v("x")}],
      "inverse_branches":[{"branch_id":"b","source_components":[{"source_variable":"x",
        "expression_ast":{"op":"ADD","args":[v("u"),c(1)]}}]}]}
    freevar_chart={"wire_id":"CHART_MAP_AST_V1","source_variables":["x"],"target_variables":["u"],
      "forward_components":[{"target_variable":"u","expression_ast":v("u")}],
      "inverse_branches":[{"branch_id":"b","source_components":[{"source_variable":"x","expression_ast":v("x")}]}]}
    singular_chart={"wire_id":"CHART_MAP_AST_V1","source_variables":["x"],"target_variables":["u"],
      "forward_components":[{"target_variable":"u","expression_ast":{"op":"ADD","args":[v("x"),
        {"op":"DIV_NONZERO","left":c(0),"right":v("x")} ]}}],
      "inverse_branches":[{"branch_id":"b","source_components":[{"source_variable":"x","expression_ast":v("u")}]}]}
    owner={"wire_id":"REPRESENTATION_OWNER_BOOKKEEPING_V1","member_ids":["m"],
      "representation_rows":[{"representation_row_id":"r","owner_member_id":"m","coverage_semantics":"PARTIAL_INCLUSION","cover_group_id":"g"},
        {"representation_row_id":"r","owner_member_id":"m","coverage_semantics":"PARTIAL_INCLUSION","cover_group_id":"g"}],"member_cover_groups":[]}
    def with_payload(payload:Any)->dict[str,Any]:
        candidate=_bundle();candidate["claims"][0]["payload"]=payload
        candidate["claims"][0]["payload_sha256"]=digest(payload)
        hashed={k:deepcopy(candidate[k]) for k in ("wire_id","subject_row_id","claims","dependency_edges","root_claim_ids","formal_credit")}
        candidate["bundle_sha256"]=digest(hashed);return candidate
    need(digest({1:"v"})==digest({"1":"v"}),"non-string JSON key collision regression premise")
    need(digest(("v",))==digest(["v"]),"tuple/list JSON collision regression premise")
    non_string_key_bundle=with_payload({1:"v"});tuple_payload_bundle=with_payload(("v",))
    float_payload_bundle=with_payload(1.0);oversized_integer_bundle=with_payload(1<<MAX_BITS)
    oversized_string_bundle=with_payload("x"*(MAX_JSON_STRING_CHARS+1))
    tuple_edges_bundle=_bundle();tuple_edges_bundle["dependency_edges"]=()
    tuple_edges_bundle["root_claim_ids"]=["c0","c1"]
    hashed={k:deepcopy(tuple_edges_bundle[k]) for k in ("wire_id","subject_row_id","claims","dependency_edges","root_claim_ids","formal_credit")}
    tuple_edges_bundle["bundle_sha256"]=digest(hashed)
    cycle=_bundle();cycle["dependency_edges"]=[{"claim_id":"c0","depends_on_claim_id":"c1"},{"claim_id":"c1","depends_on_claim_id":"c0"}];cycle["root_claim_ids"]=[]
    hashed={k:deepcopy(cycle[k]) for k in ("wire_id","subject_row_id","claims","dependency_edges","root_claim_ids","formal_credit")};cycle["bundle_sha256"]=digest(hashed)
    false_credit_bundle=_bundle();false_credit_bundle["formal_credit"]=False
    hashed={k:deepcopy(false_credit_bundle[k]) for k in ("wire_id","subject_row_id","claims","dependency_edges","root_claim_ids","formal_credit")}
    false_credit_bundle["bundle_sha256"]=digest(hashed)
    extra_trace=deepcopy(trace);extra_trace["evidence_string"]="PASS"
    return [("box overlap",lambda:check_box_partition(parent,overlap)),("box gap",lambda:check_box_partition(parent,gap)),
      ("box child outside parent",lambda:check_box_partition(parent,outside)),
      ("face bool endpoint alias",lambda:check_box_partition(face_alias_parent,[face_alias_parent],("x",True))),
      ("face int endpoint noncanonical",lambda:check_box_partition(face_alias_parent,[face_alias_parent],("x",1))),
      ("wrong derivative",lambda:check_regular_trace(trace)),("wrong trace sign",lambda:check_regular_trace(sign)),
      ("trace false cell-index alias",lambda:check_regular_trace(bool_index)),
      ("hidden trace singularity",lambda:check_regular_trace(hidden)),
      ("extra evidence string",lambda:check_regular_trace(extra_trace)),
      ("codim default",lambda:check_codim2_empty(codim)),("ChartMap pseudo identity",lambda:check_chart_map(chart)),
      ("ChartMap illicit free variables",lambda:check_chart_map(freevar_chart)),
      ("ChartMap hidden singularity",lambda:check_chart_map(singular_chart)),
      ("owner duplicate",lambda:check_representation_owners(owner)),
      ("DAG non-string payload key",lambda:check_proof_bundle(non_string_key_bundle,["AST_NORMALIZATION","INTERVAL_SIGNS"])),
      ("DAG tuple payload alias",lambda:check_proof_bundle(tuple_payload_bundle,["AST_NORMALIZATION","INTERVAL_SIGNS"])),
      ("DAG float payload noncanonical",lambda:check_proof_bundle(float_payload_bundle,["AST_NORMALIZATION","INTERVAL_SIGNS"])),
      ("DAG oversized integer payload",lambda:check_proof_bundle(oversized_integer_bundle,["AST_NORMALIZATION","INTERVAL_SIGNS"])),
      ("DAG oversized string payload",lambda:check_proof_bundle(oversized_string_bundle,["AST_NORMALIZATION","INTERVAL_SIGNS"])),
      ("DAG tuple dependency-edges alias",lambda:check_proof_bundle(tuple_edges_bundle,["AST_NORMALIZATION","INTERVAL_SIGNS"])),
      ("DAG cycle",lambda:check_proof_bundle(cycle,["AST_NORMALIZATION","INTERVAL_SIGNS"])),
      ("bundle false zero-credit alias",lambda:check_proof_bundle(false_credit_bundle,["AST_NORMALIZATION","INTERVAL_SIGNS"])),
      ("unsupported AST",lambda:differentiate({"op":"SIN","arg":v("x")},"x")),
      ("late first-pin path replacement",_late_dependency_replacement_probe)]
def _mutations()->list[tuple[str,Callable[[dict[str,Any]],None]]]:
    return [("extra",lambda x:x.__setitem__("extra",True)),("missing",lambda x:x.pop("security")),
      ("bool-int sealed alias",lambda x:x.__setitem__("sealed_exact",1)),
      ("zero-false credit alias",lambda x:x["formal_credit"].__setitem__("CM2",False)),
      ("credit",lambda x:x["formal_credit"].__setitem__("CM2",1)),("scope credit",lambda x:x["scope"].__setitem__("CM2_credit_minted",True)),
      ("unsupported theorem",lambda x:x["implemented_exact_subset"].__setitem__("R236_MATERIALIZED",True)),
      ("weaken pin",lambda x:x["dependency_seal"].__setitem__("O_NOFOLLOW",False)),
      ("erase limit",lambda x:x["explicit_fail_closed_limits"].pop("ChartMap_branch_domain_cover")),
      ("B1A pass",lambda x:x["downstream_state"].__setitem__("B1A","PASS")),
      ("pin hash",lambda x:x["dependency_seal"]["pins"][0].__setitem__("source_sha256","0"*64)),
      ("coherent fake GO",lambda x:(x["scope"].__setitem__("CM2_credit_minted",True),x["formal_credit"].__setitem__("CM2",1),x["downstream_state"].__setitem__("CM2","GO"))),
      ("candidate enabled",lambda x:x["security"].__setitem__("candidate_production_unknown_modes_silent_rc1",False))]


def _refuse(_path:Any=None)->NoReturn:raise ModeBlocked(REFUSAL)
def _boundary_probe()->dict[str,int]:
    names=("builtins_open","os_open","os_stat","os_lstat","path_lstat","path_open","path_write_bytes","path_write_text","mkstemp","named_temp","stdout","stderr")
    counters={x:0 for x in names}
    def trip(name:str)->Callable[...,Any]:
        def inner(*_a:Any,**_kw:Any)->Any:counters[name]+=1;raise AssertionError("boundary:"+name)
        return inner
    class Out:
        def write(self,*_a:Any,**_kw:Any)->Any:return trip("stdout")()
        def flush(self)->None:pass
    class Err:
        def write(self,*_a:Any,**_kw:Any)->Any:return trip("stderr")()
        def flush(self)->None:pass
    with (mock.patch("builtins.open",side_effect=trip("builtins_open")),mock.patch("os.open",side_effect=trip("os_open")),
      mock.patch("os.stat",side_effect=trip("os_stat")),mock.patch("os.lstat",side_effect=trip("os_lstat")),
      mock.patch.object(Path,"lstat",side_effect=trip("path_lstat")),mock.patch.object(Path,"open",side_effect=trip("path_open")),
      mock.patch.object(Path,"write_bytes",side_effect=trip("path_write_bytes")),mock.patch.object(Path,"write_text",side_effect=trip("path_write_text")),
      mock.patch("tempfile.mkstemp",side_effect=trip("mkstemp")),mock.patch("tempfile.NamedTemporaryFile",side_effect=trip("named_temp")),
      mock.patch.object(sys,"stdout",Out()),mock.patch.object(sys,"stderr",Err())):
        for argv in (["--candidate-output","/must/not/inspect"],["--produce"],["--unknown"],[],["--candidate-output"]):need(main(argv)==1,"rc1")
    need(all(x==0 for x in counters.values()),"zero boundaries");return counters


def self_test()->dict[str,Any]:
    doc=_contract_document();validate_contract(doc);positive=_positive_tests();att=[];muts=[]
    for label,fn in _attacks():_blocked(fn);att.append(label)
    for label,mut in _mutations():
        candidate=deepcopy(doc);mut(candidate);_blocked(lambda candidate=candidate:validate_contract(candidate));muts.append(label)
    boundary=_boundary_probe()
    return {"schema":SCHEMA+".self-test.v1","status":"PASS","canonical_contract_digest_sha256":digest(doc),
      "positive_mechanical_checks":positive,"adversarial_certificate_count":len(att),"adversarial_certificates_rejected":len(att),
      "contract_mutation_count":len(muts),"contract_mutations_rejected":len(muts),
      "filesystem_and_output_boundary_call_counts":boundary,"formal_credit":0}


def main(argv:Sequence[str]|None=None)->int:
    args=list(sys.argv[1:] if argv is None else argv)
    if args==["--print-contract"]:print(canonical_bytes(contract_envelope()).decode("ascii"));return 0
    if args==["--self-test"]:print(canonical_bytes(self_test()).decode("ascii"));return 0
    if args==["--verify-dependencies"]:print(canonical_bytes(verify_dependencies()).decode("ascii"));return 0
    try:_refuse()
    except ModeBlocked:return 1
    raise AssertionError("unreachable")
if __name__=="__main__":raise SystemExit(main())
