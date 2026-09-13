"""Complete GL⋉Z body invariant on the explicitly supported contact-frame domain."""
import json
from itertools import permutations
from .exact import Q, determinant, inverse, matvec, transpose, sub
from .geometry import certify_hollow


def canonicalize(K,contacts=None):
    actual=tuple(sorted(tuple(p) for p in certify_hollow(K)['boundary_points']))
    if contacts is None: contacts=actual
    contacts=tuple(sorted(set(tuple(p) for p in contacts)))
    if any(len(p)!=K.d or any(not Q.coerce(x).integer() for x in p) for p in contacts):
        raise ValueError('Contacts must be integral points of matching dimension')
    if contacts!=actual:
        raise ValueError('Explicit contacts must equal the entire boundary lattice set')
    if len(contacts)>8:raise RuntimeError('Canonicalization cap: at most 8 contacts')
    # Canonicalize actual extreme vertices, ignoring redundant V-generators.
    extremes=[]
    for v in K.vertices:
        normals=[list(n) for n,b,_ in K.facets() if sum(x*y for x,y in zip(n,v))==b]
        from itertools import combinations
        if any(determinant(list(rows)) for rows in combinations(normals,K.d)):
            extremes.append(v)
    best=None;frames=0
    for frame in permutations(contacts,K.d+1):
        B=transpose([list(sub(p,frame[0])) for p in frame[1:]])
        if abs(determinant(B))!=1:continue
        frames+=1;Bi=inverse(B)
        rows=[json.dumps([x.json() for x in matvec(Bi,sub(v,frame[0]))],sort_keys=True) for v in extremes]
        key='\n'.join(sorted(rows))
        if best is None or key<best:best=key
    if best is None:
        return {'status':'unsupported_no_unimodular_contact_frame','canonical_key':None}
    return {'status':'complete_on_unimodular_contact_frame_domain','canonical_key':best,'frames_checked':frames}
