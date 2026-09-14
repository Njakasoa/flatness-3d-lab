"""Fresh CPC checking for fiber, anchor and height-box inputs; no new searches.

Expand SMT lets with the Z3 parser, keep every assertion, and type numeric
leaves as Real for Ethos. Inert set-info metadata is not a proof premise.
"""
from pathlib import Path
import argparse,gzip,json,re,tempfile
import z3
from check_height_ethos import need,sha,sexps,emit,proof_body,checker,revision,ETHOS_REV,CVC5_REV
from check_det5_scaled_leaf_cvc5 import plain

ROOT=Path(__file__).resolve().parents[1]


def boolean_plain(expr):
    if z3.is_true(expr):return 'true'
    if z3.is_false(expr):return 'false'
    if z3.is_rational_value(expr) or z3.is_const(expr):return plain(expr)
    ops={z3.Z3_OP_ADD:'+',z3.Z3_OP_MUL:'*',z3.Z3_OP_SUB:'-',z3.Z3_OP_UMINUS:'-',
         z3.Z3_OP_DIV:'/',z3.Z3_OP_EQ:'=',z3.Z3_OP_LT:'<',z3.Z3_OP_LE:'<=',
         z3.Z3_OP_GT:'>',z3.Z3_OP_GE:'>=',z3.Z3_OP_OR:'or',z3.Z3_OP_AND:'and',z3.Z3_OP_NOT:'not'}
    need(expr.decl().kind() in ops,'supported linear operation')
    return '('+ops[expr.decl().kind()]+' '+' '.join(boolean_plain(x) for x in expr.children())+')'


def reference(text):
    commands=sexps(text)
    need(commands[0]==['set-logic','QF_LRA'],'linear logic')
    declarations=[c for c in commands if c[0]=='declare-fun']
    need(all(c[2:]==[[],'Real'] for c in declarations),'nullary Real declarations')
    variables={c[1] for c in declarations}
    need(len(variables)==len(declarations) and len(variables) in (3,6,22),'fiber/anchor/height-box dimension')
    need(all(c[0] in ('set-logic','set-info','declare-fun','assert')for c in commands),'input commands')
    metadata=[c for c in commands if c[0]=='set-info']
    need(all(c==['set-info',':status','unknown'] for c in metadata),'inert metadata only')
    original=list(z3.parse_smt2_string(text))
    flat='(set-logic QF_LRA)\n'+'\n'.join(emit(c)for c in declarations)+'\n'+''.join('(assert '+boolean_plain(a)+')\n'for a in original)
    parsed=list(z3.parse_smt2_string(flat))
    need(len(original)==len(parsed) and all(z3.eq(z3.simplify(a),z3.simplify(b)) for a,b in zip(original,parsed)),'let expansion retains assertions')
    def convert(e):
        if isinstance(e,str):
            if re.fullmatch(r'[0-9]+',e):return e+'/1'
            need(e in variables or e in ('true','false'),'typed symbol or Boolean constant')
            return e
        need(e[0] in ('+','-','*','/','=','<','<=','>','>=','or','and','not'),'linear assertion operation')
        return [e[0],*[convert(c) for c in e[1:]]]
    out=[]
    for command in sexps(flat):
        out.append(['assert',convert(command[1])]if command[0]=='assert'else command)
    return '\n'.join(emit(c)for c in out)+'\n',variables,len(original)


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--archive',default='results/det5_fiber_anchor.json')
    ap.add_argument('--output',default='results/det5_fiber_anchor_ethos_validation.json')
    ap.add_argument('--ethos',type=Path,required=True)
    ap.add_argument('--ethos-source',type=Path,required=True)
    ap.add_argument('--cvc5-source',type=Path,required=True)
    a=ap.parse_args();row=json.loads((ROOT/a.archive).read_text())
    need(row['status']=='unsat','stored refutation')
    raw=(ROOT/row['input_path']).read_bytes();proof=gzip.decompress((ROOT/row['proof_path']).read_bytes())
    need(sha(raw)==row['input_sha256'] and sha(proof)==row['proof_sha256'],'archived bindings')
    ref,vs,count=reference(raw.decode());body,_=proof_body(proof,vs)
    need(revision(a.ethos_source)==ETHOS_REV and revision(a.cvc5_source)==CVC5_REV,'pinned sources')
    with tempfile.TemporaryDirectory(prefix='det5-fiber-proof-')as tmp:
        p=Path(tmp)/'proof.cpc';q=Path(tmp)/'reference.smt2';p.write_text(body);q.write_text(ref)
        check=checker(a.ethos,a.cvc5_source,p,q)
        need(check['exit_code']==0 and check['stdout']=='correct' and not check['stderr'],'external proof check')
        p.write_text(body+'\n(assume @unrelated false)\n');bad=checker(a.ethos,a.cvc5_source,p,q)
        need(bad['exit_code']!=0 and'assumption'in(bad['stdout']+bad['stderr']).lower(),'unrelated assumption rejected')
    result={'status':'PASS','scope':'Reference-bound proof check for the exact archived LRA statement; geometric region coverage requires the separate input/geometry audit.',
            'input_path':row['input_path'],'input_sha256':sha(raw),'proof_path':row['proof_path'],'proof_sha256':sha(proof),
            'reference_sha256':sha(ref.encode()),'assertions_preserved':count,'variables':sorted(vs),'ethos':check,
            'ethos_revision':ETHOS_REV,'cvc5_signature_revision':CVC5_REV,'unrelated_assumption_rejected':True,'solver_queries_run':0}
    (ROOT/a.output).write_text(json.dumps(result,indent=2)+'\n');print('FIBER_PROOF_ETHOS=PASS')


if __name__=='__main__':main()
