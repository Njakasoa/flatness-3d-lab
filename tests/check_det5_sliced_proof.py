"""Check the CPC slice against both the original and its used assumptions.

No solver. Expands zero-argument term aliases to build a direct subset input.
Only a successful external replay makes the extracted input a certificate.
"""
from pathlib import Path
from functools import lru_cache
import argparse,gzip,json,sys,tempfile
import z3
from check_det5_scaled_leaf_cvc5 import reference,plain
from check_height_ethos import need,sha,sexps,emit,proof_body,checker,revision,ETHOS_REV,CVC5_REV
ROOT=Path(__file__).resolve().parents[1]

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--ethos',type=Path,required=True);ap.add_argument('--ethos-source',type=Path,required=True);ap.add_argument('--cvc5-source',type=Path,required=True);a=ap.parse_args()
 need(revision(a.ethos_source)==ETHOS_REV and revision(a.cvc5_source)==CVC5_REV,'pinned sources')
 record=json.loads((ROOT/'results/det5_cpc_dependency_slice.json').read_text());raw=gzip.decompress((ROOT/record['sliced_path']).read_bytes());need(sha(raw)==record['sliced_proof_sha256'],'slice bytes')
 cmds=sexps(raw.decode())[0];defs={c[1]:c[3]for c in cmds if c[0]=='define'}
 need(all(c[2]==[]for c in cmds if c[0]=='define'),'zero argument aliases')
 @lru_cache(None)
 def atom(x):
  if x in defs:return expand(defs[x])
  if '/'in x and all(a.isdigit()for a in x.split('/')):
   n,d=x.split('/');return ['/',n,d]
  return x
 def expand(e):return atom(e)if isinstance(e,str)else[expand(x)for x in e]
 declarations=[f'(declare-fun {c[1]} () Real)'for c in cmds if c[0]=='declare-const']
 formulas=[expand(c[2])for c in cmds if c[0]=='assume']
 smt='(set-logic QF_LRA)\n'+'\n'.join(declarations)+'\n'+'\n'.join('(assert '+emit(f)+')'for f in formulas)+'\n'
 # Directly compare scalar-normalized assertions with original public input.
 sys.path.insert(0,str(ROOT/'tests'));from audit_det5_scaled_frame_independent import canonical
 key=lambda e:canonical(z3.simplify(e))
 original=list(z3.parse_smt2_file(str(ROOT/'results/det5_scaled_leaf_contact_width_two.smt2')));subset=list(z3.parse_smt2_string(smt))
 need({key(e)for e in subset}<={key(e)for e in original},'subset of independently audited input')
 # Preserve the original input's concrete Real-numeral syntax for reference
 # binding: semantic rational expansion alone need not match CPC syntax.
 original_commands=sexps((ROOT/'results/det5_scaled_leaf_contact_width_two.smt2').read_text())
 original_asserts=[c for c in original_commands if c[0]=='assert']
 wanted={key(e)for e in subset};chosen=[];seen=set()
 for expr,command in zip(original,original_asserts):
  k=key(expr)
  if k in wanted and k not in seen:chosen.append(command);seen.add(k)
 need(seen==wanted,'all used assumptions have an original rendering')
 smt='(set-logic QF_LRA)\n'+'\n'.join(declarations)+'\n'+'\n'.join(emit(c)for c in chosen)+'\n'
 subset=list(z3.parse_smt2_string(smt))
 dest=ROOT/'certificates/det5_scaled_box_used_assumptions.smt2';dest.write_text(smt)
 ref,variables=reference(smt);body,counts=proof_body(raw,variables)
 report={'status':'INCOMPLETE','scope':'External proof check of the exact used-assumption subset; no new solver query and no automatic claim beyond mapped geometric hypotheses.','input_path':str(dest.relative_to(ROOT)),'input_sha256':sha(smt.encode()),'proof_path':record['sliced_path'],'proof_sha256':sha(raw),'input_assertions':len(subset),'retained_assumption_ids':record['retained_assumptions'],'reference_sha256':sha(ref.encode()),'ethos_revision':ETHOS_REV,'cvc5_signature_revision':CVC5_REV,'solver_queries_run':0}
 with tempfile.TemporaryDirectory(prefix='det5-sliced-')as tmp:
  p=Path(tmp)/'proof.cpc';q=Path(tmp)/'reference.smt2';p.write_text(body);q.write_text(ref)
  e=checker(a.ethos,a.cvc5_source,p,q);report['external_check']=e
  (ROOT/'results/det5_sliced_proof_validation.json').write_text(json.dumps(report,indent=2)+'\n')
  need(e['exit_code']==0 and e['stdout']=='correct'and not e['stderr'],'sliced external proof check')
  p.write_text(body+'\n(assume @not_in_input false)\n');bad=checker(a.ethos,a.cvc5_source,p,q)
  need(bad['exit_code']!=0 and'assumption'in(bad['stdout']+bad['stderr']).lower(),'new assumption rejected')
  report['unreferenced_assumption_rejected']=True
 report['status']='PASS';(ROOT/'results/det5_sliced_proof_validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:report[k]for k in('status','input_assertions','external_check')}))

if __name__=='__main__':main()
