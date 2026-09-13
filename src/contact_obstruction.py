"""Exact intrinsic lattice obstruction for a contained empty lattice simplex.

The geometric implication uses ACMS Lemma 5.1; this module certifies the
intrinsic first successive minimum of the integer contact difference body.
"""
from fractions import Fraction as F
from itertools import product
from math import gcd,prod
from .exact import Q,determinant,inverse,matvec,transpose,sub


def simplex_difference_minimum(vertices,max_points=2_000_000):
    if len(vertices)!=4 or any(len(p)!=3 for p in vertices):
        raise ValueError('Four points in dimension three required')
    if any(not Q.coerce(x).integer() for p in vertices for x in p):
        raise ValueError('Integer contact simplex required')
    B=transpose([list(sub(p,vertices[0])) for p in vertices[1:]])
    N=abs(determinant(B))
    if not N:raise ValueError('Full-dimensional simplex required')
    Bi=inverse(B)
    box=[int(max(p[j] for p in vertices)-min(p[j] for p in vertices)) for j in range(3)]
    if prod(2*b+1 for b in box)>max_points:raise RuntimeError('Exact search cap exceeded')
    minimum=Q(1);active=[];count=0
    for z in product(*(range(-b,b+1) for b in box)):
        if not any(z) or next(x for x in z if x)<0 or gcd(*z)!=1:continue
        count+=1;y=list(matvec(Bi,z));bary=[-sum(y,Q()),*y]
        gauge=sum((q for q in bary if q>0),Q())
        if gauge<minimum:minimum=gauge;active=[(z,bary)]
        elif gauge==minimum:active.append((z,bary))
    assert active and 0<minimum<=1 and not minimum.b
    return {'normalized_determinant':int(N.a),'lambda1':str(minimum.a),
        'primitive_minimizers_mod_sign':[list(z) for z,_ in active],
        'upper_witness':{'lattice_vector':list(active[0][0]),
            'difference_barycentrics':[str(x.a) for x in active[0][1]],
            'positive_sum':str(minimum.a)},
        'complete_search':{'difference_coordinate_bounds':box,'primitive_vectors_checked':count,
            'reason':'An integer edge gives lambda1<=1. Any vector with gauge<=1 lies in P-P and hence this coordinate box. Gauge=sum positive affine difference barycentrics. Nonprimitive vectors cannot improve the minimum.'}}


def width_upper_from_minimum(ell):
    ell=F(ell)
    if not 0<ell<=1:raise ValueError('Expected 0<lambda1<=1')
    if ell==1:return None
    return Q(1,F(2,3),3)/(1-ell)


def congruence_minimum(N,a):
    """First minimum for conv(0,(N,1,a),e2,e3), gcd(a,N)=1.

    The N=1 unimodular case is included separately. This formula is proved in
    proofs/CONTACT_OBSTRUCTION_REDUCTION.md, independently of box enumeration.
    """
    if not isinstance(N,int) or not isinstance(a,int) or N<1:
        raise ValueError('Positive integer determinant and integer residue required')
    if N==1:return F(1)
    if gcd(a,N)!=1:raise ValueError('Empty normal form requires coprime residue')
    return F(min(min(k,N-k)+min(a*k%N,N-a*k%N) for k in range(1,N)),N)


def below_candidate(upper):
    """Compare positive Q(sqrt3) upper with 2+sqrt2 via rational interval bounds.

    Intervals for both radicals are independently checked by squaring. This
    avoids silently mixing the two quadratic fields in the core Q class.
    """
    lo2,hi2=F(1414213562373095,10**15),F(1414213562373096,10**15)
    lo3,hi3=F(1732050807568877,10**15),F(1732050807568878,10**15)
    assert lo2*lo2<2<hi2*hi2 and lo3*lo3<3<hi3*hi3
    assert upper.d==3 and upper.b>0
    upper_hi=upper.a+upper.b*hi3
    lower_target=2+lo2
    if upper_hi<lower_target:return True
    if upper.a+upper.b*lo3>2+hi2:return False
    raise ArithmeticError('Comparison not separated by checked rational intervals')
