"""Bounded exploration of the four-cycle half-sum exclusion relaxation.

This is a necessary finite lattice-point relaxation, not a hollow certificate.
The row-stochastic facet matrix has a dominant successor coefficient >=1/2.
"""
import json,itertools,time
from pathlib import Path
import numpy as np
from scipy.optimize import minimize

P=np.array([[0,0,0],[2,1,1],[0,1,0],[0,0,1]],float)
# u.lambda is integer-valued on ambient Z3 when sum(u) is even. Anchor u0=0.
DUAL=np.array([(0,*u) for u in itertools.product(range(-3,4),repeat=3)
               if any(u) and sum(u)%2==0 and max(0,*u)-min(0,*u)<=3],float)

def facet_matrix(t):
    A=np.zeros((4,4))
    for i in range(4):
        x,y=t[2*i:2*i+2];a=.5+.5*x;r=1-a
        A[i,(i+1)%4]=a;A[i,(i+2)%4]=r*y;A[i,(i+3)%4]=r*(1-y)
    return A

def geometry(t):
    A=facet_matrix(t)
    try:Q=np.linalg.inv(A)
    except np.linalg.LinAlgError:return None
    r=Q.sum(axis=0)
    if np.min(r)<=1e-9:return None
    V=Q/r
    widths=np.ptp(DUAL@V,axis=1)
    return A,V,r,widths

def constraint(t):
    g=geometry(t)
    if g is None:return np.full(len(DUAL)+4,-1e3)
    return np.r_[g[3]-t[8],g[2]-1e-7]

def inspect_hollow(V):
    verts=(P.T@V).T
    lo=np.ceil(verts.min(axis=0)-1e-8).astype(int);hi=np.floor(verts.max(axis=0)+1e-8).astype(int)
    count=int(np.prod(np.maximum(hi-lo+1,0)))
    if count>200000:return {'status':'box_cap','box_size':count}
    aug=np.c_[verts,np.ones(4)];inv=np.linalg.inv(aug.T)
    pts=np.array(list(itertools.product(*(range(a,b+1) for a,b in zip(lo,hi)))))
    vals=np.c_[pts,np.ones(len(pts))]@inv.T
    inside=pts[np.all(vals>1e-8,axis=1)]
    return {'status':'numeric_hollow' if len(inside)==0 else 'numeric_nonhollow',
      'integer_box_size':count,'interior_points':inside.tolist(),'vertices':verts.tolist()}

def main():
    rng=np.random.default_rng(20260914);rows=[];start=time.monotonic()
    for k in range(24):
        x=rng.uniform(.03,.9,8) if k else np.tile([.02,2/3],4)
        g=geometry(x)
        if g is None:continue
        t=np.r_[x,min(g[3])]
        out=minimize(lambda z:-z[8],t,method='SLSQP',bounds=[(0,1-1e-7),(1e-7,1-1e-7)]*4+[(0,5)],
                     constraints={'type':'ineq','fun':constraint},options={'maxiter':350,'ftol':1e-10})
        g=geometry(out.x)
        if g is None:continue
        row={'run':k,'solver_success':bool(out.success),'parameters':out.x.tolist(),
             'width_directional_numeric':float(min(g[3])),'facet_matrix':g[0].tolist(),
             'hollow_screen':inspect_hollow(g[1])}
        rows.append(row);print(k,row['width_directional_numeric'],row['hollow_screen']['status'],flush=True)
    result={'status':'bounded_numeric_relaxation','seed':20260914,'directions':DUAL.tolist(),
      'scope':'Only four half-sum lattice points enforced in optimization; post-screen checks full numerical box.',
      'elapsed_seconds':time.monotonic()-start,'rows':rows}
    Path('results/det2_cycle_relaxation.json').write_text(json.dumps(result,indent=2)+'\n')

if __name__=='__main__':main()
