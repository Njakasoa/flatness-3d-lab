"""Exact first minimum of the difference body of a two-layer integer polytope."""
from fractions import Fraction as F
from itertools import product
from math import gcd

def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(o,a,b):return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])

def convex_hull(points):
    points=sorted(set(points));lower=[];upper=[]
    for p in points:
        while len(lower)>=2 and cross(lower[-2],lower[-1],p)<=0:lower.pop()
        lower.append(p)
    for p in reversed(points):
        while len(upper)>=2 and cross(upper[-2],upper[-1],p)<=0:upper.pop()
        upper.append(p)
    return lower[:-1]+upper[:-1]

def certify_minimum(vertices,height):
    """Requires binary height with an entry +1, as in normalized frame charts.

    Deleting that pivot coordinate while recording height is unimodular.
    Between layers, P_t=(1-t)P_0+tP_1. Thus the zero-height difference
    section is conv(P_0-P_0,P_1-P_1). At scale<1, all lattice vectors of
    P-P have height zero. A lattice edge always witnesses a minimum <=1.
    """
    p=tuple(tuple(v) for v in vertices);h=tuple(height)
    if len(h)!=3 or any(x not in (0,1) for x in h) or not any(h):raise ValueError('Binary nonzero height required')
    if any(len(v)!=3 or any(type(x)!=int for x in v) or dot(h,v) not in (0,1) for v in p):raise ValueError('Integer points in layers zero and one required')
    pivot=h.index(1);keep=[j for j in range(3) if j!=pivot]
    layers=[[tuple(v[j] for j in keep) for v in p if dot(h,v)==t] for t in (0,1)]
    if not all(layers):raise ValueError('Both layers required')
    differences=[(a[0]-b[0],a[1]-b[1]) for layer in layers for a in layer for b in layer]
    polygon=convex_hull(differences)
    if len(polygon)<3:raise ValueError('Full dimensional polytope required')
    edges=[]
    for a,b in zip(polygon,polygon[1:]+polygon[:1]):
        normal=(b[1]-a[1],a[0]-b[0]);offset=dot(normal,a)
        assert offset>0 and all(dot(normal,q)<=offset for q in differences)
        edges.append((normal,offset))
    bounds=[max(abs(v[j]) for v in polygon) for j in range(2)]
    ell=F(1);active=[];count=0
    for z in product(*(range(-m,m+1) for m in bounds)):
        if not any(z) or next(x for x in z if x)<0 or gcd(*z)!=1:continue
        count+=1;gauge=max(F(dot(n,z),b) for n,b in edges)
        if gauge<ell:ell=gauge;active=[z]
        elif gauge==ell:active.append(z)
    def lift(z):
        v=[0]*3
        for j,c in zip(keep,z):v[j]=c
        v[pivot]=-dot(h,v)
        return v
    return {'lambda1':str(ell),'height_direction':list(h),'deleted_coordinate':pivot,
            'section_vertices':[list(v) for v in polygon],
            'section_facets':[{'normal':list(n),'offset':b} for n,b in edges],
            'section_search_bounds':bounds,'primitive_section_vectors_checked':count,
            'section_minimizers_mod_sign':[lift(z) for z in active],
            'scope':'Section minimizers listed; at lambda1=1 nonplanar minimizers may also exist.'}
