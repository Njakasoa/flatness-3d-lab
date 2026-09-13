"""At most24 new exact joint-height fibers, with fixed retained Y extrema.
Resumes only absent fibers, preserves raw rational SAT assignment before checks.
"""
from pathlib import Path
from fractions import Fraction as Q
from itertools import product
from math import floor,ceil,gcd,prod
import json,time,hashlib,z3
from experiments.det5_joint_height_interval import make,U
from experiments.det5_height_fiber_witness import inverse
from experiments.contact_contraction_trace_probe import certify,ell
ROOT=Path(__file__).resolve().parents[1]
PATH=ROOT/'results/det5_retained_joint_probe.json'

def main():
 sources=['results/det5_joint_fibers.json','results/det5_joint_height_interval.json','results/det5_strong_fiber.json']
 hashes={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()for p in sources}
 C=next(c for c in json.loads((ROOT/'certificates/nonunimodular_observer_guards.json').read_text())['classes']if c['class_index']==5)
 S=next(c for c in json.loads((ROOT/'results/two_vector_class_scan.json').read_text())['classes']if c['class_index']==5)
 previous=json.loads((ROOT/sources[0]).read_text())['queries']
 seen={(tuple(r['Y_extrema']),tuple(r['U_extrema']),tuple(map(Q,r['midpoint'])))for r in previous}
 data=json.loads(PATH.read_text())if PATH.exists()else dict(scope='Bounded exact fibers only; UNSAT cannot exclude an open neighborhood or chart.',sources_sha256=hashes,Y_extrema=[1,0],fixed_Y=['5/16','1/8'],maximum_queries=24,queries=[])
 assert data['sources_sha256']==hashes
 if any(r.get('invertible')for r in data['queries']):return
 proposals=[('1','1'),('15/16','63/64'),('7/8','15/16'),('63/64','63/64'),('1/2','1/2'),('3/4','1/2'),('1/2','7/8'),('7/8','1/2')]
 for pair in proposals:
  for high in(2,3,0):
   Uext=[1,high];mid=list(map(Q,['5/16','1/8',*pair]));key=((1,0),tuple(Uext),tuple(mid))
   assert key not in seen
   if any(r['U_extrema']==Uext and r['midpoint']==list(map(str,mid))for r in data['queries']):continue
   assert len(data['queries'])<24
   solver,F,q,r,a,b,offset,gap=make(C,S,[1,0],Uext,[[x,x]for x in mid]);solver.set(timeout=2000)
   n=len(data['queries']);path=f'results/det5_retained_joint_probe_{n:02d}.smt2';(ROOT/path).write_text(solver.to_smt2())
   started=time.monotonic();status=solver.check();row=dict(Y_extrema=[1,0],U_extrema=Uext,midpoint=list(map(str,mid)),status=str(status),elapsed_seconds=time.monotonic()-started,timeout_ms=2000,path=path);data['queries'].append(row)
   if status==z3.unknown:row['reason_unknown']=solver.reason_unknown()
   if status==z3.sat:
    model=solver.model();val=lambda x:model.eval(x,model_completion=True).as_fraction();matrix=[[val(x)for x in line]for line in F]
    row.update(F=[[str(x)for x in line]for line in matrix],Y_normalized=list(map(str,map(val,q))),U_normalized=list(map(str,map(val,r))),Y_offset=str(val(a)),Y_gap=str(val(b)),U_offset=str(val(offset)),U_gap=str(val(gap)))
    PATH.write_text(json.dumps(data,indent=2)+'\n')
    try:T=inverse(matrix)
    except ValueError:row['invertible']=False
    else:
     row['invertible']=True;P=C['contact_points'];V=[[sum(Q(P[i][k])*T[i][j]for i in range(4))for k in range(3)]for j in range(4)];row['vertices']=[[str(x)for x in v]for v in V]
     widths=[max(sum(Q(u[k])*v[k]for k in range(3))for v in V)-min(sum(Q(u[k])*v[k]for k in range(3))for v in V)for u in((0,1,0),U)]
     assert widths==[1/val(b),1/val(gap)]and min(widths)>Q(17,5);row['directional_widths']=list(map(str,widths));PATH.write_text(json.dumps(data,indent=2)+'\n')
     boxcount=prod(max(0,floor(max(v[k]for v in V))-ceil(min(v[k]for v in V))+1)for k in range(3));row['body_integer_box_count']=boxcount
     if boxcount<=50000:row['exact_body']=certify(matrix,P)
   PATH.write_text(json.dumps(data,indent=2)+'\n');print(n,Uext,list(map(str,mid[2:])),status,flush=True)
   if row.get('invertible'):return
 assert all(hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h for p,h in hashes.items())
if __name__=='__main__':main()
