"""Exact V-polytopes in dimensions two and three; exhaustive bounded certificates."""
from itertools import combinations, permutations, product
from math import gcd, prod, factorial
from .exact import Q, dot, sub, transpose, determinant, inverse, matvec, matmul


class Polytope:
    def __init__(self,vertices):
        self.vertices=tuple(dict.fromkeys(tuple(Q.coerce(x) for x in v) for v in vertices))
        if not self.vertices: raise ValueError('No vertices')
        self.d=len(self.vertices[0])
        if self.d not in (2,3) or any(len(v)!=self.d for v in self.vertices):
            raise ValueError('Dimension must be uniformly 2 or 3')
        # In this implementation V may contain redundant generators; full dimension required.
        self.basis=None
        largest=Q()
        for ids in combinations(range(1,len(self.vertices)),self.d):
            rows=[list(sub(self.vertices[i],self.vertices[0])) for i in ids]
            magnitude=abs(determinant(rows))
            if magnitude>largest: self.basis=(ids,rows);largest=magnitude
        if self.basis is None: raise ValueError('Body must be full dimensional')
        self._facets=None

    def directional_width(self,u):
        vals=[dot(v,u) for v in self.vertices]
        return max(vals)-min(vals)

    def facets(self):
        if self._facets is not None: return self._facets
        faces={}
        for ids in combinations(range(len(self.vertices)),self.d):
            v=self.vertices[ids[0]]
            rows=[list(sub(self.vertices[i],v)) for i in ids[1:]]
            n=tuple((-1)**j*determinant([r[:j]+r[j+1:] for r in rows]) for j in range(self.d))
            if not any(n): continue
            b=dot(n,v); signs=[(dot(n,w)-b).sign() for w in self.vertices]
            if max(signs)>0 and min(signs)<0: continue
            if max(signs)>0: n=tuple(-x for x in n); b=-b
            on=tuple(i for i,w in enumerate(self.vertices) if dot(n,w)==b)
            faces[on]=(n,b,on)
        self._facets=list(faces.values())
        return self._facets

    def classify(self,p):
        signs=[(dot(n,p)-b).sign() for n,b,_ in self.facets()]
        return 'outside' if max(signs)>0 else ('boundary' if 0 in signs else 'interior')

    def volume(self):
        if len(self.vertices)!=self.d+1:
            raise NotImplementedError('Exact volume currently supports simplices only')
        return abs(determinant(self.basis[1]))/factorial(self.d)

    def transform(self,U,t):
        if len(U)!=self.d or any(len(r)!=self.d for r in U) or len(t)!=self.d:
            raise ValueError('Dimension mismatch')
        if any(not Q.coerce(x).integer() for r in U for x in r) or abs(determinant(U))!=1:
            raise ValueError('U must belong to GL(d,Z)')
        if any(not Q.coerce(x).integer() for x in t): raise ValueError('Translation must be integral')
        return Polytope([tuple(a+b for a,b in zip(matvec(U,v),t)) for v in self.vertices])

    def json(self): return [[x.json() for x in v] for v in self.vertices]


def primitive_directions(bounds):
    for u in product(*(range(-b,b+1) for b in bounds)):
        nonzero=[x for x in u if x]
        if nonzero and nonzero[0]>0 and gcd(*u)==1: yield u


def certify_width(K,max_directions=2_000_000):
    d=K.d
    trial=[tuple(int(i==j) for i in range(d)) for j in range(d)]
    W=min(K.directional_width(u) for u in trial)
    ids,D=K.basis
    inv=inverse(D)  # D rows are vertex differences; q=D u.
    bounds=[(W*sum(map(abs,r),Q())).floor() for r in inv]
    if prod(2*b+1 for b in bounds)>max_directions:
        raise RuntimeError('Certified box exceeds configured work cap; no certificate returned')
    best=W; active=[]; count=0
    for u in primitive_directions(bounds):
        count+=1; w=K.directional_width(u)
        if w<best: best=w; active=[u]
        elif w==best: active.append(u)
    assert active
    return {'status':'certified_lattice_width','width':best.json(),
            'minimizing_directions_mod_sign':active,'direction_count':count,
            'upper_certificate':{'direction':active[0],'value':best.json()},
            'lower_certificate':{'checked_minimum':best.json(),'all_box_directions_checked':True},
            'search_bound':{'initial_upper':W.json(),'basis_vertex_ids':[0,*ids],
              'D_inverse':[[x.json() for x in r] for r in inv],'coordinate_bounds':bounds,
              'proof':'q_i=<u,v_i-v_0>, |q_i|<=w(K,u)<=W; u=D^-1 q implies |u_j|<=W sum_i |D^-1_ji|. Outside this box width>W.'}}


def certify_hollow(K,max_points=2_000_000):
    box=[(min(v[i] for v in K.vertices).ceil(),max(v[i] for v in K.vertices).floor()) for i in range(K.d)]
    if prod(max(0,b-a+1) for a,b in box)>max_points:
        raise RuntimeError('Exact bounding box exceeds work cap; no certificate returned')
    boundary=[]; interior=[]; count=0
    for p in product(*(range(a,b+1) for a,b in box)):
        count+=1; loc=K.classify(p)
        if loc=='boundary': boundary.append(p)
        elif loc=='interior': interior.append(p)
    faces=[]
    for n,b,on in K.facets():
        contacts=[p for p in boundary if dot(n,p)==b]
        rel=[p for p in contacts if sum(dot(nn,p)==bb for nn,bb,_ in K.facets())==1]
        faces.append({'normal':[x.json() for x in n],'offset':b.json(),'vertex_ids':on,
                      'lattice_contacts':contacts,'relative_interior_contacts':rel})
    return {'status':'certified_hollow' if not interior else 'certified_nonhollow',
            'hollow':not interior,'integer_box':box,'points_checked':count,
            'interior_points':interior,'boundary_points':boundary,'facets':faces}


def simplex_automorphisms(K):
    if len(K.vertices)!=K.d+1: raise ValueError('Simplex required')
    base=K.vertices[0]; E=transpose([list(sub(v,base)) for v in K.vertices[1:]])
    Ei=inverse(E); answer=[]
    for perm in permutations(range(K.d+1)):
        p0=K.vertices[perm[0]]
        F=transpose([list(sub(K.vertices[i],p0)) for i in perm[1:]])
        U=matmul(F,Ei); t=sub(p0,matvec(U,base))
        if abs(determinant(U))==1 and all(x.integer() for r in U for x in r) and all(x.integer() for x in t):
            answer.append({'permutation':perm,'U':[[int(x.a) for x in r] for r in U],'t':[int(x.a) for x in t]})
    return answer
