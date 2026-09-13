"""Rational reconstruction of the best hollow four-cycle screening output."""
import json
import sys
from fractions import Fraction as F
from pathlib import Path
from src.exact import Q,inverse
from src.geometry import Polytope,certify_hollow,certify_width

def main():
    if sys.flags.optimize:
        raise SystemExit('Exact assertions required; do not use -O/-OO')
    data=json.loads(Path('results/det2_cycle_relaxation.json').read_text())
    row=max((r for r in data['rows'] if r['hollow_screen']['status']=='numeric_hollow'),key=lambda r:r['width_directional_numeric'])
    t=[F(str(x)).limit_denominator(10**6) for x in row['parameters'][:8]]
    A=[[Q() for j in range(4)] for i in range(4)]
    for i in range(4):
        x,y=t[2*i:2*i+2];a=(1+x)/2;r=1-a
        A[i][(i+1)%4]=Q(a);A[i][(i+2)%4]=Q(r*y);A[i][(i+3)%4]=Q(r*(1-y))
    assert all(A[i][i]==0 and sum(A[i],Q())==1 and all(A[i][j]>0 for j in range(4) if j!=i) for i in range(4))
    Ai=inverse(A);r=[sum((Ai[i][j] for i in range(4)),Q()) for j in range(4)]
    assert all(x>0 for x in r)
    contacts=[[0,0,0],[2,1,1],[0,1,0],[0,0,1]]
    vertices=[[sum((contacts[i][k]*Ai[i][j] for i in range(4)),Q())/r[j] for k in range(3)] for j in range(4)]
    K=Polytope(vertices);h=certify_hollow(K);w=certify_width(K)
    result={'status':'exact_rational_reconstruction','source_row':row['run'],
      'scope':'One reconstructed tetrahedron; not a global or local optimum certificate.',
      'parameters':[str(x) for x in t],'facet_matrix':[[str(x.a) for x in a] for a in A],
      'vertices':K.json(),'hollow':h,'width':w}
    Path('certificates/det2_cycle_rational.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'hollow':h,'width':w},indent=2))

if __name__=='__main__':main()
