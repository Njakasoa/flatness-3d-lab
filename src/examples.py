"""Reconstruction in standard Z^d, with explicit original lattice conversion."""
from .exact import Q, inverse, matvec, sub, transpose
from .geometry import Polytope


def codenotti_santos():
    r=Q(0,1)
    raw=[(2+r,r,2+r),(-r,2+r,-2-r),(-2-r,-r,2+r),(r,-2-r,-2-r)]
    contacts=[(-1,-1,-1),(1,-1,1),(1,1,-1),(-1,1,1)]
    B=transpose([list(sub(p,contacts[0])) for p in contacts[1:]])
    Bi=inverse(B)
    # x=p0+Bz identifies Z^3 with the affine lattice of ACMS (1).
    return Polytope([matvec(Bi,sub(v,contacts[0])) for v in raw])


def standard_simplex(d=3,scale=1):
    return Polytope([(0,)*d]+[tuple(scale if j==i else 0 for j in range(d)) for i in range(d)])
