"""Explicit affine-lattice embeddings of all63 hull types into nine templates."""
from fractions import Fraction as F
from itertools import combinations,permutations
from pathlib import Path
import json
from enumeration.contact_extensions import det,adj,matrix,dot,sub,canonical

def affine_image(U,t,points):
    return tuple(sorted(tuple(dot(row,p)+t[i] for i,row in enumerate(U)) for p in points))

def find_full_frame_map(source,target):
    """Map some ordered source frame to the first target four-frame, exactly."""
    target=tuple(map(tuple,target))
    targetframe=next(f for f in combinations(target,4) if det(matrix(f)))
    B=matrix(targetframe);N=det(B)
    for f in permutations(source,4):
        A=matrix(f);d=det(A)
        if abs(d)!=abs(N):continue
        Ai=adj(A)
        U=tuple(tuple(F(sum(B[i][k]*Ai[k][j] for k in range(3)),d) for j in range(3)) for i in range(3))
        if any(x.denominator!=1 for row in U for x in row):continue
        U=tuple(tuple(int(x) for x in row) for row in U)
        t=tuple(targetframe[0][i]-dot(U[i],f[0]) for i in range(3))
        if affine_image(U,t,source)==tuple(sorted(target)):
            assert abs(det(U))==1
            return {'matrix':[list(r) for r in U],'translation':list(t)}
    return None

def main():
    ext=json.loads(Path('results/contact_extensions.json').read_text())['classes']
    tet=[c for c in json.loads(Path('certificates/contact_obstructions.json').read_text())['cases'] if c['survives_threshold_11A_over_7']]
    templates=[c['vertices'] for c in ext if len(c['vertices'])==8]
    targets=[c['vertices'] for c in tet]+[c['vertices'] for c in ext]
    rows=[]
    for i,P in enumerate(targets):
        found=None
        for j,R in enumerate(templates):
            for inds in combinations(range(8),len(P)):
                subset=tuple(tuple(R[k]) for k in inds)
                if len(P)>=5 and canonical(subset)!=tuple(map(tuple,P)):continue
                m=find_full_frame_map(subset,P)
                if m is not None:
                    found={'class_index':i,'vertices':P,'template_index':j,'subset_indices':list(inds),'map_subset_to_class':m};break
            if found is not None:break
        if found is None:raise AssertionError(('No template embedding',i,P))
        rows.append(found)
    # The last template has a square in the z=0 layer, written explicitly.
    R=templates[-1];S=[(0,0,0),(1,0,0),(-1,1,0),(0,1,0)]
    U=((1,1,0),(0,1,0),(0,0,1));t=(0,0,0)
    square=((0,0,0),(0,1,0),(1,0,0),(1,1,0))
    assert affine_image(U,t,S)==square and det(U)==1
    rows.append({'class_index':62,'vertices':[list(p) for p in square],
      'template_index':len(templates)-1,'subset_indices':[R.index(list(p)) for p in S],
      'map_subset_to_class':{'matrix':[list(r) for r in U],'translation':list(t)}})
    result={'status':'exact_template_embeddings_pending_independent_replay',
       'scope':'Each necessary contact hull is a subset of a template up to affine lattice equivalence. The template need not lie in the surrounding hollow body.',
       'templates':templates,'template_count':len(templates),'configuration_count':len(rows),'embeddings':rows}
    Path('certificates/contact_templates.json').write_text(json.dumps(result,indent=2)+'\n')
    print('Exact affine embeddings:',len(rows),'configurations into',len(templates),'templates')

if __name__=='__main__':main()
