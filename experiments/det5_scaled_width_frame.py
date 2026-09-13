"""Complete d5a2 scaled vertex frame and shared-product outer relaxations.

All fifteen width tests are linear in T_i=b(v_i-v_L). The exact contact
reconstruction is bilinear. Linear relaxations use proved finite bounds;
SAT relaxations and solver UNKNOWN never imply a high-width body or exclusion.
"""
from fractions import Fraction as Q
from itertools import combinations
from pathlib import Path
import argparse,hashlib,json,time
import z3
from experiments.contact_contraction_trace_probe import build,ell
from experiments.det5_complete_vertex_lift import gauges
from experiments.nonunimodular_complete_smt import width_directions
from experiments.det5_height_fiber_witness import inverse

ROOT=Path(__file__).resolve().parents[1]
ARCHIVE=ROOT/'results/det5_scaled_width_frame.json'
BETA=Q(183,500);TARGET=Q(17,5);R=Q(6,5)/BETA**3
GAP_MIN=Q(1,1)/R;GAP_MAX=1/TARGET
EXTRA=((1,-1,1),(2,1,1),(3,1,0),(6,1,2),(1,1,0),(2,1,0),(3,1,1),(4,1,1))
REPS=((0,1),(0,3),(1,0))

def rat(q):return z3.RealVal(str(q))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def inputs():
 C=next(c for c in json.loads((ROOT/'certificates/nonunimodular_observer_guards.json').read_text())['classes']if c['class_index']==5)
 S=next(c for c in json.loads((ROOT/'results/two_vector_class_scan.json').read_text())['classes']if c['class_index']==5)
 return C,S

def make(C,S,ext,box=None,relax=False):
 base,F,vectors=build(C,S,include_trace=False)
 repl=[];free=[];intervals={};box=box or [[Q(0),Q(1)]for _ in range(8)]
 for j in range(4):
  ids=[i for i in range(4)if i!=j];f,g=F[ids[0]][j],F[ids[1]][j]
  repl.append((F[ids[2]][j],1-f-g));free.extend((f,g))
  for k,i in enumerate(ids[:2]):intervals[i,j]=tuple(box[2*j+k])
  intervals[ids[2],j]=(max(Q(0),1-box[2*j][1]-box[2*j+1][1]),min(Q(1),1-box[2*j][0]-box[2*j+1][0]))
 F=[[z3.simplify(z3.substitute(x,*repl))for x in row]for row in F]
 s=z3.SolverFor('QF_LRA'if relax else'QF_NRA')
 s.add(*[z3.simplify(z3.substitute(x,*repl))for x in base.assertions()])
 gauges(s,F,sorted(set(vectors)|set(EXTRA)))
 for v,(lo,hi)in zip(free,box):s.add(v>=rat(lo),v<=rat(hi))
 L,H=ext;b=z3.Real('scaled_b')
 s.add(b>rat(GAP_MIN),b<rat(GAP_MAX))
 T=[[rat(0)if i==L else rat(1)if k==1 and i==H else z3.Real(f't{i}_{k}')for k in range(3)]for i in range(4)]
 for i in range(4):s.add(T[i][1]>=0,T[i][1]<=1)
 for i,j in combinations(range(4),2):
  for k,m in ((0,5),(2,2)):
   s.add(T[i][k]-T[j][k]<rat(m*R)*b,T[j][k]-T[i][k]<rat(m*R)*b)
 W={};products=[]
 for i in range(4):
  for j in range(4):
   for k in range(3):
    f,t=F[i][j],T[i][k]
    if i==j or i==L:W[i,j,k]=rat(0)
    elif k==1 and i==H:W[i,j,k]=f
    elif not relax:W[i,j,k]=f*t
    else:
     fl,fh=intervals[i,j];tl,th=(Q(0),Q(1))if k==1 else(-((5,1,2)[k])*R*GAP_MAX,((5,1,2)[k])*R*GAP_MAX)
     w=z3.Real(f'w{i}_{j}_{k}');W[i,j,k]=w
     s.add(t>=rat(tl),t<=rat(th),f>=rat(fl),f<=rat(fh))
     s.add(w>=rat(fl)*t+rat(tl)*f-rat(fl*tl),w>=rat(fh)*t+rat(th)*f-rat(fh*th),
           w<=rat(fh)*t+rat(tl)*f-rat(fh*tl),w<=rat(fl)*t+rat(th)*f-rat(fl*th))
     products.append((i,j,k,w))
 for j in range(1,4):
  for k in range(3):s.add(sum(W[i,j,k]-W[i,0,k]for i in range(4))==b*(C['contact_points'][j][k]-C['contact_points'][0][k]))
 dirs=width_directions(5,2)
 for u in dirs:
  h=[sum(u[k]*v[k]for k in range(3))for v in T]
  s.add(z3.Or(*[sign*(h[i]-h[j])>rat(TARGET)*b for i,j in combinations(range(4),2)for sign in(-1,1)]))
 return s,F,T,b,free,products,dirs

def inspect(F,C):
 try:A=inverse(F)
 except (StopIteration,ZeroDivisionError,ValueError):return {'invertible':False}
 V=[[sum(Q(C['contact_points'][i][k])*A[i][j]for i in range(4))for k in range(3)]for j in range(4)]
 ws={tuple(u):max(sum(u[k]*v[k]for k in range(3))for v in V)-min(sum(u[k]*v[k]for k in range(3))for v in V)for u in width_directions(5,2)}
 u=min(ws,key=ws.get)
 return {'invertible':True,'minimum_of_complete_15':str(ws[u]),'minimizing_list_direction':list(u),'all_15_above_target':min(ws.values())>TARGET}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--new-relaxations-per-chart',type=int,default=9);ap.add_argument('--timeout-ms',type=int,default=3000);ap.add_argument('--exact-timeout-ms',type=int,default=7000);args=ap.parse_args()
 if min(args.new_relaxations_per_chart,args.timeout_ms,args.exact_timeout_ms)<=0:raise ValueError('positive bounds')
 C,S=inputs()
 data=json.loads(ARCHIVE.read_text())if ARCHIVE.exists()else{'scope':'Complete15width scaled frame, three Y representatives. Bilinear equivalence is exact; McCormick SAT is only outer feasibility. Status-closed leaves need proof checking before any exclusion claim.','class_index':5,'target':str(TARGET),'beta':str(BETA),'R':str(R),'gap_bounds':[str(GAP_MIN),str(GAP_MAX)],'z3_version':z3.get_version_string(),'queries':[],'charts':[]}
 def save():ARCHIVE.write_text(json.dumps(data,indent=2)+'\n')
 for ext in REPS:
  if not any(r['kind']=='exact'and r['Y_extrema']==list(ext)for r in data['queries']):
   s,F,T,b,*_=make(C,S,ext);s.set(timeout=args.exact_timeout_ms)
   path=ROOT/f'results/det5_scaled_exact_{ext[0]}_{ext[1]}.smt2';path.write_text(s.to_smt2());start=time.monotonic();st=s.check()
   row={'kind':'exact','Y_extrema':list(ext),'path':str(path.relative_to(ROOT)),'input_sha256':sha(path),'timeout_ms':args.exact_timeout_ms,'status':str(st),'elapsed_seconds':time.monotonic()-start}
   if st==z3.unknown:row['reason_unknown']=s.reason_unknown()
   if st==z3.sat:row['assignment']={str(v):str(s.model()[v])for v in s.model()}
   data['queries'].append(row);save();print(json.dumps(row),flush=True)
  chart=next((c for c in data['charts']if c['Y_extrema']==list(ext)),None)
  if chart is None:
   chart={'Y_extrema':list(ext),'closed':[],'pending':[{'node':'r','box':[['0','1']for _ in range(8)]}]};data['charts'].append(chart)
  for _ in range(args.new_relaxations_per_chart):
   if not chart['pending']:break
   leaf=chart['pending'].pop(0);box=[[Q(x)for x in pair]for pair in leaf['box']];tag=leaf['node']
   if any(r['kind']=='relaxation'and r['Y_extrema']==list(ext)and r['node']==tag for r in data['queries']):raise ValueError('repeat node')
   s,F,T,b,free,products,dirs=make(C,S,ext,box,True);s.set(timeout=args.timeout_ms)
   path=ROOT/f'results/det5_scaled_relax_{ext[0]}_{ext[1]}_{tag}.smt2';path.write_text(s.to_smt2());start=time.monotonic();st=s.check()
   row={'kind':'relaxation','Y_extrema':list(ext),**leaf,'path':str(path.relative_to(ROOT)),'input_sha256':sha(path),'timeout_ms':args.timeout_ms,'status':str(st),'elapsed_seconds':time.monotonic()-start}
   axis=max(range(8),key=lambda i:box[i][1]-box[i][0])
   if st==z3.unsat:chart['closed'].append(leaf)
   else:
    if st==z3.unknown:row['reason_unknown']=s.reason_unknown()
    if st==z3.sat:
     model=s.model();fm=[[model.eval(x).as_fraction()for x in r]for r in F];tm=[[model.eval(x).as_fraction()for x in r]for r in T];bm=model.eval(b).as_fraction()
     row['F']=[[str(x)for x in r]for r in fm];row['T']=[[str(x)for x in r]for r in tm];row['b']=str(bm)
     residual=[abs(model.eval(w).as_fraction()-fm[i][j]*tm[i][k])for i,j,k,w in products]
     row['maximum_product_residual']=str(max(residual,default=Q(0)));row['actual_F']=inspect(fm,C)
     if row['actual_F'].get('all_15_above_target'):row['requires_exact_body_certification']=True
    # Longest-edge cyclic split gives a complete finite-tree partition.
    lo,hi=box[axis];mid=(lo+hi)/2
    for suffix,iv in [('0',(lo,mid)),('1',(mid,hi))]:
     child=[list(x)for x in box];child[axis]=list(iv);chart['pending'].append({'node':tag+suffix,'box':[[str(x)for x in pair]for pair in child]})
    row['split_axis']=axis
   data['queries'].append(row);save();print(json.dumps({k:row[k]for k in('kind','Y_extrema','node','status','elapsed_seconds')}),flush=True)
   if row.get('requires_exact_body_certification'):return
  print(json.dumps({'Y':ext,'closed':len(chart['closed']),'pending':len(chart['pending'])}),flush=True)

if __name__=='__main__':main()
