"""Stdlib exact interval review for arbitrary normalized U/Y extrema.

Exports independent bounds for the encoding audit. Universal validity rests
on the interval-product proof in DET5_COUPLED_FRAME_REVIEW.md; endpoint and
representative tests guard the implementation and all sign/reference cases.
"""
from fractions import Fraction as Q
from itertools import product,permutations
from math import gcd
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
BETA=Q(183,500);W=Q(17,5);R=Q(6,5)/BETA**3;BMIN=1/R;BMAX=1/W
P=((0,0,0),(5,1,2),(0,1,0),(0,0,1))

def need(c,m):
    if not c:raise ValueError(m)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def mul_iv(a,b):
    values=[x*y for x in a for y in b];return min(values),max(values)
def scale_iv(a,c):return mul_iv(a,(c,c))
def add_iv(*ivs):return sum(iv[0] for iv in ivs),sum(iv[1] for iv in ivs)
def intersect(*ivs):
    lo=max(iv[0] for iv in ivs);hi=min(iv[1] for iv in ivs)
    need(lo<=hi,'nonempty derived interval');return lo,hi

def normalized(ext,box):
    need(len(set(ext))==2 and all(i in range(4) for i in ext),'distinct extrema')
    out=[None]*4;out[ext[0]]=(Q(0),Q(0));out[ext[1]]=(Q(1),Q(1))
    for i,pair in zip([i for i in range(4) if i not in ext],box):
        lo,hi=map(Q,pair);need(0<=lo<=hi<=1,'closed normalized interval');out[i]=(lo,hi)
    need(all(iv is not None for iv in out),'two free intervals');return out

def per_vertex(P,ye,ue,box,i,u):
    q=normalized(ye,box[:2]);r=normalized(ue,box[2:]);L=ye[0]
    heights=[dot(u,p) for p in P];cap=R*(max(heights)-min(heights))
    if i==L:return {'implemented_static':(Q(0),Q(0)),'derived_static':(Q(0),Q(0)),'homogeneous':(Q(0),Q(0)),'cap':cap}
    difference=(r[i][0]-r[L][1],r[i][1]-r[L][0])
    Ustatic=mul_iv(difference,(W*BMIN,2*R*BMAX))
    Uphysical=mul_iv(difference,(W,2*R))
    global_static=(-cap*BMAX,cap*BMAX)
    current=global_static
    if tuple(u)==(0,1,0):current=q[i]
    elif tuple(u)==(1,-1,-2):current=intersect(current,Ustatic)
    elif tuple(u)==(1,-2,-2):current=intersect(current,add_iv(Ustatic,scale_iv(q[i],-1)))
    # u=a*U+c*Y+d*Z; the same per-vertex scalar intervals are shared.
    a,c,d=u[0],u[0]+u[1],2*u[0]+u[2]
    decomposition=add_iv(scale_iv(Ustatic,a),scale_iv(q[i],c),scale_iv((-2*R*BMAX,2*R*BMAX),d))
    derived=intersect(current,decomposition)
    Yphysical=(q[i][0]/BMAX,q[i][1]/BMIN)
    homogeneous=intersect((-cap,cap),add_iv(scale_iv(Uphysical,a),scale_iv(Yphysical,c),scale_iv((-2*R,2*R),d)))
    # Mutual consequences of b in [BMIN,BMAX], without assuming independence.
    derived=intersect(derived,mul_iv(homogeneous,(BMIN,BMAX)))
    homogeneous=intersect(homogeneous,mul_iv(derived,(1/BMAX,1/BMIN)))
    return {'implemented_static':current,'derived_static':derived,'homogeneous':homogeneous,'cap':cap}

def dirs():
    out=[]
    for u in product(range(-2,3),range(-3,4),range(-3,4)):
        if not any(u) or next(x for x in u if x)<0 or gcd(*u)!=1:continue
        h=[dot(u,p) for p in P]
        if max(h)-min(h)<=3:out.append(u)
    need(len(out)==15,'complete directions');return out

def main():
    need(0<BMIN<BMAX and W*BMIN<2*R*BMAX,'positive ordered gap/span bounds')
    boxes=[((0,1),(0,1)),((0,Q(1,2)),(0,Q(1,2))),((Q(1,2),1),(Q(1,2),1)),
           ((Q(1,4),Q(3,4)),(Q(1,4),Q(3,4))),((0,Q(1,2)),(Q(1,2),1)),((Q(3,4),1),(Q(3,4),1))]
    checks=0
    for ue in permutations(range(4),2):
        free=[i for i in range(4) if i not in ue]
        for box in boxes:
            rr=normalized(ue,box)
            for L in range(4):
                for endpoints in product((0,1),repeat=2):
                    r=[Q(0) if i==ue[0] else Q(1) if i==ue[1] else None for i in range(4)]
                    for i,k in zip(free,endpoints):r[i]=rr[i][k]
                    for s,b in product((W,2*R),(BMIN,BMAX)):
                        for i in range(4):
                            diff=(rr[i][0]-rr[L][1],rr[i][1]-rr[L][0])
                            static=mul_iv(diff,(W*BMIN,2*R*BMAX));hom=mul_iv(diff,(W,2*R))
                            actual=b*s*(r[i]-r[L]);need(static[0]<=actual<=static[1] and hom[0]<=actual/b<=hom[1],'all U reference/sign endpoint cases');checks+=1
    candidates=0;strict=0
    for ye in ((0,1),(0,3),(1,0)):
        for ue in permutations(range(4),2):
            for qb,rb in product(boxes[-2:],boxes):
                box=tuple(qb)+tuple(rb);q=normalized(ye,qb);r=normalized(ue,rb)
                qm=[sum(iv)/2 for iv in q];rm=[sum(iv)/2 for iv in r]
                b=(BMIN+BMAX)/2;s=(W+2*R)/2;L=ye[0]
                for i in range(4):
                    gU=b*s*(rm[i]-rm[L]);point=(gU+qm[i],qm[i],Q(0))
                    for u in dirs():
                        rec=per_vertex(P,ye,ue,box,i,u);g=dot(u,point)
                        if abs(g)<=rec['cap']*b:
                            need(rec['implemented_static'][0]<=g<=rec['implemented_static'][1],'current bound valid')
                            need(rec['derived_static'][0]<=g<=rec['derived_static'][1],'derived static valid')
                            need(rec['homogeneous'][0]<=g/b<=rec['homogeneous'][1],'derived homogeneous valid');candidates+=1
                        if rec['derived_static']!=rec['implemented_static'] or rec['homogeneous']!=(-rec['cap'],rec['cap']):strict+=1
    result={'status':'PASS','scope':'Exact endpoint/sign/reference tests supporting the continuous interval proof; no solver queries or full-model feasibility claims.',
            'U_endpoint_cases_checked':checks,'representative_directional_checks':candidates,'strictly_tighter_interval_records':strict,
            'Bmin':str(BMIN),'Bmax':str(BMAX),'U_scaled_span_closed_bounds':[str(W*BMIN),str(2*R*BMAX)],'solver_queries_run':0}
    (ROOT/'results/det5_coupled_interval_validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
