"""Transfer frozen Y/U pending boxes into the complete scaled width frame.

Normalized U boxes become linear ratio bounds because its span is positive.
The model adds all-direction volume spans and shared barycentric volume cuts.
Inherited UNSAT labels are provenance, not checked proof kernels.
"""
from fractions import Fraction as Q
from itertools import combinations
from pathlib import Path
import argparse,hashlib,json,time
import z3
from experiments.det5_scaled_width_frame import make,inputs,rat,R,TARGET,inspect,ROOT
SOURCE=ROOT/'results/det5_joint_short_gauges.json'
ARCHIVE=ROOT/'results/det5_scaled_pending_transfer.json'
U=(1,-1,-2)

def strengthened(C,S,chart,leaf):
 ext=chart['Y_extrema'];ue=chart['U_extrema'];box=[[Q(x)for x in pair]for pair in leaf['box']]
 s,F,T,b,free,products,dirs=make(C,S,ext,relax=True)
 for i,(lo,hi)in zip([i for i in range(4)if i not in ext],box[:2]):
  t=T[i][1];s.add(t>=rat(lo),t<=rat(hi))
  for j in range(4):
   if i==j:continue
   w=z3.Real(f'w{i}_{j}_1');f=F[i][j]
   s.add(w>=rat(lo)*f,w<=rat(hi)*f,w>=t+rat(hi)*f-rat(hi),w<=t+rat(lo)*f-rat(lo))
 h=[sum(U[k]*v[k]for k in range(3))for v in T];D=h[ue[1]]-h[ue[0]]
 s.add(D>rat(TARGET)*b)
 for v in h:s.add(v>=h[ue[0]],v<=h[ue[1]])
 for i,(lo,hi)in zip([i for i in range(4)if i not in ue],box[2:]):s.add(h[i]-h[ue[0]]>=rat(lo)*D,h[i]-h[ue[0]]<=rat(hi)*D)
 for u in dirs:
  ph=[sum(u[k]*p[k]for k in range(3))for p in C['contact_points']];cap=R*(max(ph)-min(ph))
  th=[sum(u[k]*v[k]for k in range(3))for v in T]
  for i,j in combinations(range(4),2):s.add(th[i]-th[j]<rat(cap)*b,th[j]-th[i]<rat(cap)*b)
 # Reuse exactly the lifted contact-zero products from the reconstruction.
 L,H=ext
 def w(i,j,k):
  if i==j or i==L:return rat(0)
  if k==1 and i==H:return F[i][j]
  return z3.Real(f'w{i}_{j}_{k}')
 center=[sum(w(i,0,k)for i in range(4))for k in range(3)]
 for i in range(4):
  x,y,z=[T[i][k]-center[k]for k in range(3)]
  bary=[b+rat(Q(2,5))*x-y-z,x/5,y-x/5,z-rat(Q(2,5))*x]
  for mask in range(1,16):s.add(sum(bary[j]for j in range(4)if mask&(1<<j))<rat(R)*b)
 return s,F,T,b,products

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--max-new',type=int,default=36);ap.add_argument('--timeout-ms',type=int,default=3000);args=ap.parse_args()
 if min(args.max_new,args.timeout_ms)<=0:raise ValueError('positive bounds')
 C,S=inputs();raw=SOURCE.read_bytes();source=json.loads(raw)
 data=json.loads(ARCHIVE.read_text())if ARCHIVE.exists()else{'scope':'Complete15direction scaled outer models on immutable pending Y/U leaves, with sharper spans and shared volume cuts. Partial recorded outcomes establish no class exclusion.','source':{'path':str(SOURCE.relative_to(ROOT)),'sha256':hashlib.sha256(raw).hexdigest(),'query_count':len(source['queries'])},'queries':[]}
 if data['source']['sha256']!=hashlib.sha256(raw).hexdigest():raise ValueError('source changed')
 done={(tuple(r['Y_extrema']),tuple(r['U_extrema']),r['node'])for r in data['queries']}
 charts=[c for c in source['charts']if c['pending_leaves']];todo=[]
 for n in range(max(len(c['pending_leaves'])for c in charts)):
  for c in charts:
   if n<len(c['pending_leaves']):
    leaf=c['pending_leaves'][n];key=(tuple(c['Y_extrema']),tuple(c['U_extrema']),leaf['node'])
    if key not in done:todo.append((c,leaf))
 for c,leaf in todo[:args.max_new]:
  s,F,T,b,products=strengthened(C,S,c,leaf);s.set(timeout=args.timeout_ms)
  ye,ue=c['Y_extrema'],c['U_extrema'];path=ROOT/f'results/det5_scaled_pending_{ye[0]}_{ye[1]}_{ue[0]}_{ue[1]}_{leaf["node"]}.smt2';path.write_text(s.to_smt2());start=time.monotonic();st=s.check()
  row={'Y_extrema':ye,'U_extrema':ue,**leaf,'path':str(path.relative_to(ROOT)),'input_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'timeout_ms':args.timeout_ms,'status':str(st),'elapsed_seconds':time.monotonic()-start}
  if st==z3.unknown:row['reason_unknown']=s.reason_unknown()
  if st==z3.sat:
   m=s.model();fm=[[m.eval(x).as_fraction()for x in r]for r in F]
   row['assignment']={str(x):str(m[x])for x in m};row['F']=[[str(x)for x in r]for r in fm];row['actual_F']=inspect(fm,C)
  data['queries'].append(row);ARCHIVE.write_text(json.dumps(data,indent=2)+'\n');print(json.dumps({k:row[k]for k in('Y_extrema','U_extrema','node','status','elapsed_seconds')}),flush=True)
  if row.get('actual_F',{}).get('all_15_above_target'):return

if __name__=='__main__':main()
