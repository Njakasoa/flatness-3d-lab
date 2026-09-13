"""Bounded numeric search on the linear guard/sign branch of strong witness.
Numerical outputs are guidance only; no theorem or exact witness is inferred.
"""
from pathlib import Path
from fractions import Fraction as Q
import json
import numpy as np
from scipy.optimize import minimize,linprog,LinearConstraint,Bounds
from experiments.contact_contraction_trace_probe import ell
ROOT=Path(__file__).resolve().parents[1]
R=json.loads((ROOT/'results/det5_strong_fiber.json').read_text())
C=next(c for c in json.loads((ROOT/'certificates/nonunimodular_observer_guards.json').read_text())['classes']if c['class_index']==5)
S=next(c for c in json.loads((ROOT/'results/two_vector_class_scan.json').read_text())['classes']if c['class_index']==5)
F0=np.array([[float(Q(x))for x in row]for row in R['F']]);inds=[(i,j)for i in range(4)for j in range(4)if i!=j];P=np.array(C['contact_points']).T
q=np.array([1,0,5/16,1/8]);A=[];lo=[];hi=[]
def add(row,l,h):A.append(row);lo.append(l);hi.append(h)
for j in range(4):
 row=np.zeros(14)
 for k,(i,jj)in enumerate(inds):row[k]=int(j==jj)
 add(row,1,1)
 row=np.zeros(14)
 for k,(i,jj)in enumerate(inds):row[k]=q[i]*int(j==jj)
 row[12]=-1;row[13]=-int(j in(1,2));add(row,0,0)
for z in C['guards']:
 l=np.array(list(map(float,ell(z,5,2,True))));i=int(np.argmin(F0@l));row=np.zeros(14)
 for k,(ii,j)in enumerate(inds):row[k]=l[j]*int(i==ii)
 add(row,-np.inf,0)
for z in sorted(set(map(tuple,C['primitive_contact_edge_directions']))|{tuple(r['vector'])for r in S['eligible_vectors']}):
 l=np.array(list(map(float,ell(z,5,2))));positive=F0@l>0;row=np.zeros(14)
 for k,(i,j)in enumerate(inds):row[k]=l[j]*positive[i]
 add(row,183/500+1e-7,np.inf)
row=np.zeros(14);row[-2:]=1;add(row,-np.inf,1)
A=np.array(A);lo=np.array(lo);hi=np.array(hi);lc=LinearConstraint(A,lo,hi);bounds=Bounds([1e-7]*12+[0,1e-7],[1]*13+[5/17-1e-7]);eq=lo==hi
ub=np.concatenate([A[np.isfinite(hi)&~eq],-A[np.isfinite(lo)&~eq]]);bv=np.concatenate([hi[np.isfinite(hi)&~eq],-lo[np.isfinite(lo)&~eq]])
def matrix(x):
 f=np.zeros((4,4))
 for k,(i,j)in enumerate(inds):f[i,j]=x[k]
 return f
def objective(x):
 try: v=P@np.linalg.inv(matrix(x));h=np.array([1,-1,-2])@v;w=np.ptp(h)
 except np.linalg.LinAlgError:return 1000
 return -min(w,100)
x0=np.array([F0[i,j]for i,j in inds]+[float(Q(R['offset'])),float(Q(R['gap']))]);rng=np.random.default_rng(5913);out=[]
for k in range(12):
 if k:
  lp=linprog(rng.normal(size=14),A_ub=ub,b_ub=bv,A_eq=A[eq],b_eq=lo[eq],bounds=list(zip(bounds.lb,bounds.ub)),method='highs')
  if not lp.success:break
  x0=.99*lp.x+.01*x0
 res=minimize(objective,x0,method='SLSQP',bounds=bounds,constraints=lc,options={'maxiter':300,'ftol':1e-10})
 violation=max(np.max(lo-A@res.x),np.max(A@res.x-hi),0)
 row=dict(index=k,success=bool(res.success),message=res.message,U_width=-res.fun,maximum_linear_violation=float(violation),F=matrix(res.x).tolist(),Y_offset=res.x[12],Y_gap=res.x[13])
 v=P@np.linalg.inv(matrix(res.x));h=np.array([1,-1,-2])@v;rn=(h-min(h))/np.ptp(h);row.update(U_extrema=[int(np.argmin(h)),int(np.argmax(h))],U_normalized=rn.tolist())
 out.append(row);(ROOT/'results/det5_retained_joint_probe_numeric.json').write_text(json.dumps({'scope':'Numerical branch guidance only','queries':out},indent=2)+'\n');print(k,res.success,-res.fun,violation,flush=True)
 if violation<1e-7 and -res.fun>3.405:break
