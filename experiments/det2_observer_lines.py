"""Complete determinant-two interior-point guards on twelve lattice lines.

Completeness uses the written minimal-observer argument and the width-one
classification for empty five-point 3-polytopes (Blanco--Santos Theorem1.2).
The finite list additionally assumes volume(K)<21. All enumeration is exact.
"""
import itertools
import json
from fractions import Fraction as Q
from math import ceil, floor, gcd
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
CONTACTS=((0,0,0),(2,1,1),(0,1,0),(0,0,1))
NORMALS=((0,0,1),(0,1,0),(1,-1,-1))
BOX=((-124,126),(-62,63),(-62,63))
SIGMA=(1,0,3,2)


def dot(x,y):return sum(a*b for a,b in zip(x,y))
def sub(x,y):return tuple(a-b for a,b in zip(x,y))
def cross(x,y):return (x[1]*y[2]-x[2]*y[1],x[2]*y[0]-x[0]*y[2],x[0]*y[1]-x[1]*y[0])
def need(x,msg):
    if not x:raise ValueError(msg)
def lam(z):
    x,y,z=map(Q,z)
    return (1+x/2-y-z,x/2,y-x/2,z-x/2)
def negative_mass(z):return sum(max(Q(0),-x) for x in lam(z))


def pair_profile(z):
    l=lam(z);possible=[]
    for i in range(4):
        other=[j for j in range(4) if j not in(i,SIGMA[i])]
        values=[l[SIGMA[i]],(l[SIGMA[i]]+l[other[0]])/2,(l[SIGMA[i]]+l[other[1]])/2]
        if max(values)<=0:return {'tautological':True,'blocking_row':i}
        if min(values)<=0:possible.append(i)
    need(possible,'an observer cannot be forced strictly interior for all pair matrices')
    return {'tautological':False,'possible_blocking_rows':possible}


def build():
    # Direct completeness of the three width-one normals: after sign choice
    # the values at p0,p1,p2,p3 lie in {0,1}, with p0 value0.
    reconstructed=[]
    for b1,b2,b3 in itertools.product((0,1),repeat=3):
        if (b1-b2-b3)%2 or not any((b1,b2,b3)):continue
        u=((b1-b2-b3)//2,b2,b3)
        if next(x for x in u if x)<0:u=tuple(-x for x in u)
        reconstructed.append(u)
    need(set(reconstructed)==set(NORMALS),'width-one normal list')
    # Independently verify the fixed contact tetrahedron is empty.
    Ppoints=[z for z in itertools.product(range(3),range(2),range(2)) if min(lam(z))>=0]
    need(set(Ppoints)==set(CONTACTS),'P is not empty')
    lines=[];guards=set()
    for u in NORMALS:
        levels=sorted(set(dot(u,p) for p in CONTACTS));need(levels[1]-levels[0]==1,'unit slab')
        for level in levels:
            ids=[i for i,p in enumerate(CONTACTS) if dot(u,p)==level]
            need(len(ids)==2,'each slab level must have two contacts')
            a,b=(CONTACTS[i] for i in ids);v=sub(b,a)
            need(gcd(*v)==1,'edge primitive')
            for sign in (-1,1):
                target=tuple(sign*x for x in u)
                options=[z for z in itertools.product(range(-3,4),repeat=3)
                         if dot(u,z)==level and cross(v,sub(z,a))==target]
                need(options,'no small particular lattice solution found')
                q0=min(options,key=lambda z:(sum(x*x for x in z),z))
                lows=[];highs=[]
                for q,vj,(lo,hi) in zip(q0,v,BOX):
                    if not vj:need(lo<=q<=hi,'line misses enclosing box');continue
                    ends=sorted((Q(lo-q,vj),Q(hi-q,vj)))
                    lows.append(ceil(ends[0]));highs.append(floor(ends[1]))
                lower,upper=max(lows),min(highs)
                included=[]
                for t in range(lower,upper+1):
                    z=tuple(q+t*d for q,d in zip(q0,v))
                    if negative_mass(z)<62:
                        included.append(t);guards.add(z)
                need(included==list(range(min(included),max(included)+1)),'convex mass interval')
                lines.append({'normal':u,'level':level,'contact_indices':ids,'cross_sign':sign,
                              'base_point':q0,'primitive_direction':v,
                              'enclosing_box_parameter_interval':[lower,upper],
                              'volume_below_21_parameter_interval':[min(included),max(included)],
                              'point_count':len(included)})
    need(len(lines)==12,'twelve lines')
    rows=[];pair=[]
    for z in sorted(guards):
        profile=pair_profile(z)
        rows.append({'point':z,'negative_barycentric_mass':str(negative_mass(z)),**profile})
        if not profile['tautological']:pair.append(z)
    return {'status':'exact_twelve_line_guard_enumeration',
            'hypotheses':['K compact full dimensional convex','P contained in K','all four contacts are on boundary of K','volume(K)<21 for the finite list'],
            'source':'https://arxiv.org/pdf/1409.6701 (v3), Theorem 1.2(1)',
            'width_one_normals':NORMALS,'contact_points':CONTACTS,'coordinate_box':BOX,
            'lines':lines,'finite_guard_count':len(guards),'guards':rows,
            'pair_nontrivial_count':len(pair),'pair_nontrivial_points':pair,
            'pair_tautological_count':len(guards)-len(pair),
            'scope':'Complete hollowness guards under the stated hypotheses, conditional on the cited classification theorem. Not a class width bound or an infeasibility result.'}


def main():
    data=build()
    (ROOT/'certificates/det2_observer_lines.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps({k:data[k] for k in ('status','finite_guard_count','pair_nontrivial_count','pair_tautological_count')}))
    for line in data['lines']:print(line['base_point'],line['primitive_direction'],line['volume_below_21_parameter_interval'])


if __name__=='__main__':main()
