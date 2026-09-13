"""External Ethos check of the five-direction pending-box refutation.

No solver calls. Input/proof framing is shared with the reviewed adapter.
"""
from pathlib import Path
import argparse,gzip,json,tempfile
from check_det5_scaled_leaf_cvc5 import reference
from check_height_ethos import need,sha,proof_body,checker,revision,ETHOS_REV,CVC5_REV
ROOT=Path(__file__).resolve().parents[1]

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--ethos',type=Path,required=True);ap.add_argument('--ethos-source',type=Path,required=True);ap.add_argument('--cvc5-source',type=Path,required=True);ap.add_argument('--output',type=Path,default=ROOT/'results/det5_scaled_width_core_ethos_validation.json');a=ap.parse_args()
 out=a.output
 need(revision(a.ethos_source)==ETHOS_REV and revision(a.cvc5_source)==CVC5_REV,'pinned checker/signature sources')
 archive=ROOT/'results/det5_scaled_leaf_width_core.json';d=json.loads(archive.read_text());r=next(r for r in d['queries']if r['name']=='contact_width_two');need(r['status']=='unsat','refutation')
 smt=(ROOT/r['path']).read_bytes();packed=(ROOT/r['proof_path']).read_bytes();raw=gzip.decompress(packed)
 need(sha(smt)==r['input_sha256']and sha(raw)==r['proof_sha256'],'input/proof hashes')
 ref,variables=reference(smt.decode());body,counts=proof_body(raw,variables)
 report={'scope':'Externally checked refutation of one retained Y/U box with five width directions. No whole chart or class exclusion.','status':'INCOMPLETE','input_path':r['path'],'input_sha256':sha(smt),'proof_path':r['proof_path'],'proof_sha256':sha(raw),'compressed_proof_sha256':sha(packed),'reference_sha256':sha(ref.encode()),'archive_sha256':sha(archive.read_bytes()),'ethos_revision':ETHOS_REV,'cvc5_signature_revision':CVC5_REV,'proof_commands':counts,'solver_queries_run':0}
 with tempfile.TemporaryDirectory(prefix='det5-five-widths-')as tmp:
  p=Path(tmp)/'proof.cpc';q=Path(tmp)/'reference.smt2';p.write_text(body);q.write_text(ref)
  result=checker(a.ethos,a.cvc5_source,p,q);report['external_check']=result;out.write_text(json.dumps(report,indent=2)+'\n')
  need(result['exit_code']==0 and result['stdout']=='correct'and not result['stderr'],'external kernel check')
  p.write_text(body+'\n(assume @fresh_unrelated false)\n');bad=checker(a.ethos,a.cvc5_source,p,q)
  need(bad['exit_code']!=0 and'assumption'in(bad['stdout']+bad['stderr']).lower(),'unreferenced assumption rejected')
  report['unreferenced_assumption_rejected']=True
  # An empty proof cannot establish the required top-level false conclusion.
  try:proof_body(b'(\n\n)',variables)
  except ValueError:report['missing_refutation_rejected']=True
  else:raise ValueError('empty proof accepted')
 report['status']='PASS';out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))

if __name__=='__main__':main()
