"""Restore six exact height products on two newly reduced order branches.

This is a new nonlinear formulation of the remaining actual Y[0,3] chart.
SAT must still undergo independent exact body checks; UNKNOWN proves nothing.
"""
from pathlib import Path
import argparse,hashlib,json,time
import z3
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'results/det5_y_ordered_exact.json'

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--timeout-ms',type=int,default=15000);a=ap.parse_args()
 if OUT.exists():print('Exact ordered archive exists; unchanged queries skipped');return
 p=ROOT/'results/det5_y_ordered_root_difference.json';raw=p.read_bytes();prior=json.loads(raw)
 d={'scope':'Six exact height products restored on the two structurally ordered Y[0,3] residual branches. Recorded nonlinear outcomes require exact body/proof checking before any geometric conclusion.','source_archive_path':str(p.relative_to(ROOT)),'source_archive_sha256':hashlib.sha256(raw).hexdigest(),'queries':[]}
 for row in prior['queries']:
  inp=ROOT/row['input_path'];need=hashlib.sha256(inp.read_bytes()).hexdigest()==row['input_sha256']
  if not need:raise ValueError('source input changed')
  s=z3.SolverFor('QF_NRA');s.add(*z3.parse_smt2_file(str(inp)))
  for i in(1,2):
   for j in range(4):
    if i!=j:s.add(z3.Real(f'product_{i}_{j}')==z3.Real(f'q_{i}')*z3.Real(f'F_{i}_{j}'))
  s.set(timeout=a.timeout_ms);out=ROOT/f'results/det5_y_ordered_exact_{row["order"]}.smt2';out.write_text(s.to_smt2());t=time.monotonic();st=s.check()
  r={'order':row['order'],'source_path':row['input_path'],'source_sha256':row['input_sha256'],'input_path':str(out.relative_to(ROOT)),'input_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'status':str(st),'elapsed_seconds':time.monotonic()-t,'timeout_ms':a.timeout_ms,'z3_version':z3.get_version_string()}
  if st==z3.unknown:r['reason_unknown']=s.reason_unknown()
  if st==z3.sat:
   m=s.model();r['assignment']={str(v):m[v].sexpr()for v in m};r['rational_assignment']=all(z3.is_rational_value(m[v])for v in m);r['all_assertions_true']=all(z3.is_true(z3.simplify(m.eval(c,model_completion=True)))for c in s.assertions())
  d['queries'].append(r);OUT.write_text(json.dumps(d,indent=2)+'\n');print(json.dumps({k:r[k]for k in('order','status','elapsed_seconds')}),flush=True)
if __name__=='__main__':main()
