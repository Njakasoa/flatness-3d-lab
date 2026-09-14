"""Fresh reference-bound kernel replay of three stored corner CPC proofs.

Standard library only; never invokes an SMT solver or overwrites proof receipts.
"""
from pathlib import Path
import argparse,gzip,json,tempfile
from check_height_ethos import need,sha,real_reference,proof_body,checker,revision,ETHOS_REV,CVC5_REV
ROOT=Path(__file__).resolve().parents[1]

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--ethos',type=Path,required=True);ap.add_argument('--ethos-source',type=Path,required=True);ap.add_argument('--cvc5-source',type=Path,required=True);ap.add_argument('--output',type=Path,default=ROOT/'results/det5_y_corner_supplement_ethos_validation.json');a=ap.parse_args()
 need(revision(a.ethos_source)==ETHOS_REV and revision(a.cvc5_source)==CVC5_REV,'pinned checker/signature sources')
 read=lambda p:json.loads((ROOT/p).read_text())
 rows=[read('results/det5_y_corner_gauge_sharp_probe.json')['queries'][0],read('results/det5_y_corner_enlarged.json'),read('results/det5_y_corner_enlarged_3_5.json')]
 out={'status':'INCOMPLETE','scope':'Fresh kernel replay of three archived partial corner refutations, not a geometric completeness theorem.','ethos_revision':ETHOS_REV,'cvc5_signature_revision':CVC5_REV,'proofs':[],'solver_queries_run':0}
 with tempfile.TemporaryDirectory(prefix='det5-corner-check-')as tmp:
  p=Path(tmp)/'proof.cpc';q=Path(tmp)/'reference.smt2'
  for r in rows:
   need(r['status']=='unsat','recorded refutation');smt=(ROOT/r['input_path']).read_bytes();packed=(ROOT/r['proof_path']).read_bytes();raw=gzip.decompress(packed)
   need(sha(smt)==r['input_sha256']and sha(raw)==r['proof_sha256']and sha(packed)==r['compressed_proof_sha256'],'input and proof hashes')
   ref,_,vs=real_reference(smt.decode());need(sha(ref.encode())==r['reference_sha256'],'reference binding');body,_=proof_body(raw,vs);p.write_text(body);q.write_text(ref)
   checked=checker(a.ethos,a.cvc5_source,p,q);need(checked['exit_code']==0 and checked['stdout']=='correct'and not checked['stderr'],'external kernel check')
   out['proofs'].append({'input_path':r['input_path'],'input_sha256':sha(smt),'proof_path':r['proof_path'],'proof_sha256':sha(raw),'reference_sha256':sha(ref.encode()),'ethos':checked});a.output.write_text(json.dumps(out,indent=2)+'\n')
  p.write_text(body+'\n(assume @unrelated false)\n');bad=checker(a.ethos,a.cvc5_source,p,q);need(bad['exit_code']!=0 and'assumption'in(bad['stdout']+bad['stderr']).lower(),'unreferenced assumption rejected')
  out['unreferenced_assumption_rejected']=True
 out['status']='PASS';a.output.write_text(json.dumps(out,indent=2)+'\n');print('Y_CORNER_SUPPLEMENT_ETHOS=PASS')
if __name__=='__main__':main()
