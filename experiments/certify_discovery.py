"""Convert selected exploratory bodies to exact rational contact models and replay."""
import json,itertools
from fractions import Fraction as F
from pathlib import Path
import numpy as np
from src.exact import Q,inverse,matmul,dot,determinant,matvec
from src.geometry import Polytope,certify_width,certify_hollow,simplex_automorphisms
from src.canonical import canonicalize
from .discovery import vertices_from_parameters


def rationalize(row):
    if row['parameters'] is not None:
        _,C=vertices_from_parameters(row['parameters']);R=[[Q() for _ in range(4)] for _ in range(4)]
        for j in range(4):
            ids=[i for i in range(4) if i!=j]
            vals=[F(str(float(C[i,j]))).limit_denominator(10**7) for i in ids[:2]]
            vals.append(1-sum(vals))
            if min(vals)<=0:raise ValueError('Rationalization left contact simplex')
            for i,a in zip(ids,vals):R[i][j]=Q(a)
        P=[[Q(0),Q(1),Q(0),Q(0)],[Q(0),Q(0),Q(1),Q(0)],[Q(0),Q(0),Q(0),Q(1)], [Q(1)]*4]
        V=matmul(P,inverse(R))
        return Polytope(list(zip(*V[:3])))
    planes=[]
    for f in row['facets']:
        c=min(row['lattice_contacts_numeric'],key=lambda p:abs(np.dot(f[:3],p)+f[3]))
        if abs(np.dot(f[:3],c)+f[3])>1e-6:raise ValueError('Facet lacks identified contact')
        n=tuple(Q(F(str(float(x))).limit_denominator(10**6)) for x in f[:3])
        planes.append((n,dot(n,c)))
    vs=[]
    for ids in itertools.combinations(range(len(planes)),3):
        A=[list(planes[i][0]) for i in ids]
        if not determinant(A):continue
        v=matvec(inverse(A),[planes[i][1] for i in ids])
        if all(dot(n,v)<=b for n,b in planes):vs.append(v)
    return Polytope(vs)


def main():
    rows=[json.loads(s) for s in Path('results/near_extremizers.jsonl').read_text().splitlines()]
    ranked=sorted(rows,key=lambda r:-r['width_directional_upper_estimate'])
    selected=ranked[:4]
    for family in sorted(set(r['family'] for r in rows)):
        best=max((r for r in rows if r['family']==family),key=lambda r:r['width_directional_upper_estimate'])
        if best not in selected:selected.append(best)
    summary=[]
    for row in selected:
        K=rationalize(row);h=certify_hollow(K);w=certify_width(K)
        val=Q.from_json(w['width'])
        result={'source_id':row['id'],'source_family':row['family'],'rationalization_changes_body':True,
          'vertices':K.json(),'hollow_certificate':h,'width_certificate':w,
          'volume':K.volume().json() if len(K.vertices)==4 else None,
          'automorphisms':simplex_automorphisms(K) if len(K.vertices)==4 else None,
          'canonicalization':canonicalize(K),'counterexample':h['hollow'] and val>Q(2,1)}
        path=f'certificates/discovery_{row["id"]}.json'
        Path(path).write_text(json.dumps(result,indent=2)+'\n')
        summary.append({'id':row['id'],'family':row['family'],'hollow':h['hollow'],
           'width_exact':str(val),'width_decimal_display':float(val),'facets':len(K.facets()),
           'counterexample':result['counterexample'],'certificate':path})
        print(row['id'],h['hollow'],float(val),'counterexample',result['counterexample'],flush=True)
    Path('results/certified_discovery_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
if __name__=='__main__':main()
