"""Exhaustive twelve-way Z-extrema pilot on one new coupled residual formula.

Every actual tetrahedron attains a distinct minimum/maximum pair in Z.
Closed ordering inequalities include ties; this branch cover is exhaustive.
No whole box is certified unless every branch has checked refutations.
"""
from pathlib import Path
from itertools import permutations
import argparse,hashlib,json,time
import z3
from experiments.det5_scaled_width_frame import ROOT,TARGET,rat
OUT=ROOT/'results/det5_coupled_z_extrema.json'

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--timeout-ms',type=int,default=3000);a=ap.parse_args()
 raw=(ROOT/'results/det5_coupled_scaled_frame.json').read_bytes();archive=json.loads(raw);row=archive['queries'][0]
 base=ROOT/row['path'];formula=base.read_bytes()
 if hashlib.sha256(formula).hexdigest()!=row['input_sha256']:raise ValueError('input binding')
 d=json.loads(OUT.read_text())if OUT.exists()else{'scope':'Exhaustive Z-extrema split of one coupled residual outer model. Status-only UNSAT is not a checked exclusion.','source_archive_sha256':hashlib.sha256(raw).hexdigest(),'source_path':row['path'],'source_sha256':row['input_sha256'],'Y_extrema':row['Y_extrema'],'U_extrema':row['U_extrema'],'node':row['node'],'box':row['box'],'queries':[]}
 if d['source_sha256']!=row['input_sha256']:raise ValueError('source changed')
 done={tuple(r['Z_extrema'])for r in d['queries']};L=row['Y_extrema'][0]
 z=[rat(0)if i==L else z3.Real(f't{i}_2')for i in range(4)];b=z3.Real('scaled_b')
 for low,high in permutations(range(4),2):
  if(low,high)in done:continue
  s=z3.SolverFor('QF_LRA');s.add(*z3.parse_smt2_string(formula.decode()));s.add(*[v>=z[low]for v in z],*[v<=z[high]for v in z],z[high]-z[low]>rat(TARGET)*b);s.set(timeout=a.timeout_ms)
  p=ROOT/f'results/det5_coupled_z_{low}_{high}.smt2'
  if p.exists():raise ValueError('unrecorded input exists')
  p.write_text(s.to_smt2());t=time.monotonic();st=s.check();r={'Z_extrema':[low,high],'path':str(p.relative_to(ROOT)),'input_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'status':str(st),'elapsed_seconds':time.monotonic()-t,'timeout_ms':a.timeout_ms}
  if st==z3.unknown:r['reason_unknown']=s.reason_unknown()
  if st==z3.sat:
   m=s.model();r['assignment']={str(v):str(m[v])for v in m};r['all_assertions_true']=all(z3.is_true(m.eval(c,model_completion=True))for c in s.assertions())
  d['queries'].append(r);OUT.write_text(json.dumps(d,indent=2)+'\n');print(json.dumps({k:r[k]for k in('Z_extrema','status','elapsed_seconds')}),flush=True)

if __name__=='__main__':main()
