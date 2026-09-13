"""Independent-engine proof for one new scaled pending-leaf exclusion.

Parses the archived linear input, removes only exact syntactic simplifications,
and emits a let-free Real formula for cvc5/CPC and optional Ethos checking.
This verifies one leaf, not the inherited frontier or a whole contact class.
"""
from pathlib import Path
import argparse,gzip,hashlib,json,re,subprocess,tempfile
import z3,cvc5
from replay_height_cover_cvc5 import run
from check_height_ethos import need,sha,sexps,emit,proof_body,checker,revision,ETHOS_REV,CVC5_REV
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'results/det5_scaled_leaf_cvc5_validation.json'

def plain(e):
 if z3.is_rational_value(e):
  q=e.as_fraction();v=str(abs(q.numerator))if q.denominator==1 else f'(/ {abs(q.numerator)} {q.denominator})'
  return f'(- {v})'if q<0 else v
 if z3.is_const(e)and e.num_args()==0:return str(e)
 ops={z3.Z3_OP_ADD:'+',z3.Z3_OP_MUL:'*',z3.Z3_OP_SUB:'-',z3.Z3_OP_UMINUS:'-',z3.Z3_OP_DIV:'/',z3.Z3_OP_EQ:'=',z3.Z3_OP_LT:'<',z3.Z3_OP_LE:'<=',z3.Z3_OP_GT:'>',z3.Z3_OP_GE:'>=',z3.Z3_OP_OR:'or',z3.Z3_OP_AND:'and',z3.Z3_OP_NOT:'not'}
 return '('+ops[e.decl().kind()]+' '+' '.join(plain(x)for x in e.children())+')'

def reference(smt):
 cmds=sexps(smt);variables={c[1]for c in cmds if c[0]=='declare-fun'}
 def convert(e):
  if isinstance(e,str):
   if re.fullmatch(r'[0-9]+',e):return e+'/1'
   need(e in variables,'Real reference symbol');return e
  need(e[0]in('+','-','*','/','=','<','<=','>','>=','or','and','not'),'reference operation')
  return [e[0],*[convert(x)for x in e[1:]]]
 out=[]
 for c in cmds:
  if c[0]=='assert':out.append(['assert',convert(c[1])])
  else:need(c[0]in('set-logic','declare-fun'),'reference command');out.append(c)
 return '\n'.join(emit(c)for c in out)+'\n',variables

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--ethos',type=Path);ap.add_argument('--ethos-source',type=Path);ap.add_argument('--cvc5-source',type=Path);a=ap.parse_args()
 if OUT.exists():print('Recorded proof attempt exists; unchanged run skipped');return
 data=json.loads((ROOT/'results/det5_scaled_pending_transfer.json').read_text());rows=[r for r in data['queries']if r['status']=='unsat'];need(len(rows)==1,'unique new pending leaf')
 row=rows[0];raw=(ROOT/row['path']).read_bytes();need(sha(raw)==row['input_sha256'],'source binding')
 assertions=[z3.simplify(c)for c in z3.parse_smt2_string(raw.decode())];assertions=[c for c in assertions if not z3.is_true(c)]
 variables={}
 def visit(e):
  if z3.is_const(e)and e.decl().kind()==z3.Z3_OP_UNINTERPRETED:need(e.sort()==z3.RealSort(),'Real variable');variables[str(e)]=e
  for x in e.children():visit(x)
 for c in assertions:visit(c)
 text='(set-logic QF_LRA)\n'+''.join(f'(declare-fun {n} () Real)\n'for n in sorted(variables))+''.join('(assert '+plain(c)+')\n'for c in assertions)
 # Exact equality of AST assertion multisets after simplification.
 need(sorted(c.sexpr()for c in assertions)==sorted(z3.simplify(c).sexpr()for c in z3.parse_smt2_string(text)),'let-free transfer')
 dest=ROOT/'certificates/det5_scaled_pending_leaf';dest.mkdir(exist_ok=True);(dest/'input.smt2').write_text(text)
 result,proof=run(text)
 result.update(scope='One new pending-leaf refutation only. No complete chart or contact-class exclusion.',source_path=row['path'],source_sha256=sha(raw),input_sha256=sha(text.encode()),Y_extrema=row['Y_extrema'],U_extrema=row['U_extrema'],node=row['node'],box=row['box'],cvc5_version=cvc5.__version__)
 if proof is not None:
  need(not any('TRUST'in r or'SORRY'in r for r in result['proof_rules']),'no trusted rules')
  pr=proof.encode()if isinstance(proof,str)else proof;(dest/'proof.cpc.gz').write_bytes(gzip.compress(pr,mtime=0));result['proof_sha256']=sha(pr)
  if a.ethos:
   need(a.ethos_source and a.cvc5_source,'both pinned sources');need(revision(a.ethos_source)==ETHOS_REV and revision(a.cvc5_source)==CVC5_REV,'pinned sources')
   ref,vs=reference(text);body,counts=proof_body(pr,vs)
   with tempfile.TemporaryDirectory(prefix='det5-scaled-proof-')as tmp:
    tmp=Path(tmp);pp=tmp/'proof.cpc';rr=tmp/'reference.smt2';pp.write_text(body);rr.write_text(ref)
    check=checker(a.ethos,a.cvc5_source,pp,rr);result['ethos']=check
    need(check['exit_code']==0 and check['stdout']=='correct'and not check['stderr'],'external proof check')
    pp.write_text(body+'\n(assume @fresh_unrelated false)\n');bad=checker(a.ethos,a.cvc5_source,pp,rr)
    need(bad['exit_code']!=0 and'assumption'in(bad['stdout']+bad['stderr']).lower(),'reference corruption rejected')
    result['reference_corruption_rejected']=True;result['reference_sha256']=sha(ref.encode());result['proof_commands']=counts;result['ethos_revision']=ETHOS_REV;result['cvc5_signature_revision']=CVC5_REV
 OUT.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))

if __name__=='__main__':main()
