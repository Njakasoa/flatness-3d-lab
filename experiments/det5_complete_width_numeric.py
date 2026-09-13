"""Bounded full-width search on witness-selected linear guard/gauge branches.

Uses all fifteen complete width covectors, with fixed supporting vertex pairs
per numerical start. Restricted branches are exploratory, not global bounds.
"""
from pathlib import Path
from fractions import Fraction as Q
import json,numpy as np
from scipy.optimize import minimize,LinearConstraint,Bounds
from experiments.contact_contraction_trace_probe import ell
from experiments.det5_scaled_width_frame import inputs,EXTRA
from experiments.nonunimodular_complete_smt import width_directions
ROOT=Path(__file__).resolve().parents[1];ARCHIVE=ROOT/'results/det5_complete_width_numeric.json'

def main():
 if ARCHIVE.exists():print('Archive exists; unchanged experiment skipped');return
 C,S=inputs();P=np.array(C['contact_points'],float).T;dirs=np.array(width_directions(5,2),float);inds=[(i,j)for j in range(4)for i in range(4)if i!=j]
 vectors=sorted(set(map(tuple,C['primitive_contact_edge_directions']))|{tuple(r['vector'])for r in S['eligible_vectors']}|set(EXTRA))
 seeds=[]
 for name in ['det5_strong_fiber','det5_joint_volume_gaps','det5_joint_enriched_cover','det5_joint_short_gauges']:
  d=json.loads((ROOT/f'results/{name}.json').read_text());w=d if 'F'in d else d['retained_witness'];seeds.append((name,[[float(Q(x))for x in row]for row in w['F']]))
 d=json.loads((ROOT/'results/det5_scaled_width_frame.json').read_text())
 for row in d['queries']:
  if row.get('F')and row.get('actual_F',{}).get('invertible'):
   seeds.append((row['path'],[[float(Q(x))for x in r]for r in row['F']]))
  if len(seeds)>=12:break
 out={'scope':'Numerical lower-candidate search with all15directions on fixed guard/gauge/support-pair branches. No upper bound or exact witness inferred.','seeds':[]}
 for name,ff in seeds:
  F0=np.array(ff);A=[];lo=[];hi=[]
  def add(row,l,h):A.append(row);lo.append(l);hi.append(h)
  for j in range(4):add([float(j==jj)for i,jj in inds]+[0],1,1)
  for z in C['guards']:
   l=np.array(list(map(float,ell(z,5,2,True))));i=int(np.argmin(F0@l));add([l[j]if ii==i else 0 for ii,j in inds]+[0],-np.inf,0)
  for z in vectors:
   l=np.array(list(map(float,ell(z,5,2))));positive=F0@l>0;add([l[j]if positive[i]else 0 for i,j in inds]+[0],183/500+1e-8,np.inf)
  lc=LinearConstraint(np.array(A),np.array(lo),np.array(hi));bound=Bounds([1e-8]*12+[0],[1]*12+[3.972])
  def matrix(x):
   f=np.zeros((4,4))
   for t,(i,j)in enumerate(inds):f[i,j]=x[t]
   return f
  inv0=np.linalg.inv(F0);h0=dirs@P@inv0;pair=[(int(np.argmax(h)),int(np.argmin(h)))for h in h0];w0=min(np.ptp(h0,axis=1));x0=np.array([F0[i,j]for i,j in inds]+[w0*.999])
  def values(x,jac=False):
   f=matrix(x)
   try:iv=np.linalg.inv(f)
   except np.linalg.LinAlgError:return np.zeros((len(dirs),13))if jac else np.full(len(dirs),-1e8)
   h=dirs@P@iv
   if not jac:return np.array([h[t,p]-h[t,m]-x[-1]for t,(p,m)in enumerate(pair)])
   return np.array([[-h[t,i]*(iv[j,p]-iv[j,m])for i,j in inds]+[-1]for t,(p,m)in enumerate(pair)])
  res=minimize(lambda x:-x[-1],x0,jac=lambda x:np.array([0]*12+[-1.]),method='SLSQP',bounds=bound,constraints=[lc,{'type':'ineq','fun':values,'jac':lambda x:values(x,True)}],options={'maxiter':400,'ftol':1e-11})
  f=matrix(res.x);h=dirs@P@np.linalg.inv(f);av=np.array(A)@res.x;violation=max(0,float(np.max(np.array(lo)-av)),float(np.max(av-np.array(hi))),float(-np.min(values(res.x))))
  row={'source':name,'success':bool(res.success),'message':str(res.message),'iterations':int(res.nit),'width_15':float(np.min(np.ptp(h,axis=1))),'w_variable':float(res.x[-1]),'maximum_constraint_violation':violation,'F':f.tolist(),'fixed_width_pairs':pair,'widths':np.ptp(h,axis=1).tolist()}
  out['seeds'].append(row);ARCHIVE.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:row[k]for k in('source','success','width_15','maximum_constraint_violation','iterations')}),flush=True)

if __name__=='__main__':main()
