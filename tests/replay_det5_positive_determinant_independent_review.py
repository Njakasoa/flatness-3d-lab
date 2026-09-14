"""Independent stdlib replay of the positive-determinant convexity review."""
from fractions import Fraction as Q
from hashlib import sha256
from itertools import product
from pathlib import Path
import argparse
import json

ROOT=Path(__file__).resolve().parents[1]


def norm(v):
    assert sum(v)==0
    return sum(abs(a) for a in v)/2


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--skip-primary-text", action="store_true", help="Replay arithmetic and local bindings without the unredistributed article")
    args=ap.parse_args()
    contacts=((0,0,0),(5,1,2),(0,1,0),(0,0,1))
    ell=(-Q(1,5),Q(2,5),-Q(2,5),Q(1,5))
    assert sum(ell)==0
    assert tuple(sum(ell[j]*contacts[j][i] for j in range(4)) for i in range(3))==(2,0,1)
    swapped=(ell[0],ell[2],ell[1],ell[3])
    assert swapped==(-Q(1,5),-Q(2,5),Q(2,5),Q(1,5))
    grid=(Q(0),Q(1,9),Q(1,2),Q(9,10),Q(99,100))
    weights=(Q(0),Q(1,4),Q(1,2),Q(3,4),Q(1))
    shapes=vertices=interior=endpoint_shapes=0
    for p,q in product(grid,repeat=2):
      L=1-p*q
      y=(1-q)/L;x=p*y
      assert 0<=x<y<=1
      for C,E in ((Q(1,7),Q(1,5)),(Q(2,5),Q(1,2)),(Q(1,3),Q(1,3))):
        A=C+p*E;B=q*C+E;S=C+E
        al=(1-p)*E;om=(1-q)*C
        assert min(A,B,al,om)>0 and S<1
        assert (1-x)*B-(1-y)*A==al
        assert x*B-y*A==-om
        assert al-(1-x)*B==-(1-y)*A
        assert om+x*B==y*A
        Z=(al,-B,A,-om)
        assert norm(Z)==S
        shapes+=1
        endpoint_shapes+=int(x==0 or y==1)
        for k,sign,bound in ((3,1,S/3),(2,-1,S/5)):
          def image(u,r):
            V=((1-x)*u-(1-y)*r,-u,r,x*u-y*r)
            return tuple((z+sign*2*v)/5 for z,v in zip(Z,V))
          triangle=((Q(0),Q(0)),(B/k,Q(0)),(B/k,A/k))
          values=[image(*v) for v in triangle]
          assert all(norm(v)<=bound for v in values)
          assert norm(values[0])==S/5
          if k==3:
            assert norm(values[2])==S/3
          else:
            assert norm(values[1])==A/5 and norm(values[2])==0
          vertices+=3
          for w1,w2 in product(weights,repeat=2):
            if w1+w2>1:continue
            w0=1-w1-w2
            u=(w1+w2)*B/k;r=w2*A/k
            assert u*A-r*B>=0 and k*u<=B
            assert (1-k*u/B,k*(u/B-r/A),k*r/A)==(w0,w1,w2)
            v=image(u,r)
            assert v==tuple(w0*a+w1*b+w2*c for a,b,c in zip(*values))
            assert norm(v)<=sum(w*norm(z) for w,z in zip((w0,w1,w2),values))<=bound
            assert norm(v)<(Q(1,3) if k==3 else Q(1,5))
            interior+=1
    # For c*A0<17/5, isolate2/sqrt3 and square positive rationals.
    for c in (Q(3,2),Q(5,4)):
        radical_upper=Q(17,5)/c-1
        assert radical_upper>0 and Q(4,3)<radical_upper**2
    assert Q(183,500)>Q(1,3)>Q(1,5)
    paths=('proofs/DET5_POSITIVE_HORIZONTAL_DETERMINANT.md',
           'proofs/DET5_POSITIVE_DETERMINANT_INDEPENDENT_REVIEW.md',
           'proofs/DET5_COMPACT_SHAPE_CHART_REVIEW.md',
           'papers/ACMS-1907.06199.txt')
    retained_paths=paths[:-1] if args.skip_primary_text else paths
    sources=[{'path':p,'sha256':sha256((ROOT/p).read_bytes()).hexdigest()} for p in retained_paths]
    if not args.skip_primary_text:
        text=(ROOT/paths[-1]).read_text()
        fragment=text[text.index('Lemma 5.1.'):text.index('5.2. Bounds on volume and width.')]
        assert 'hollow convex body in dimension three' in fragment and 'λ1(K−K)(14)' in fragment
    result={'status':'PASS','primary_text_check':'SKIPPED_UNREDISTRIBUTED' if args.skip_primary_text else 'PASS','sources':sources,'independent_compact_shapes':shapes,
            'endpoint_shapes':endpoint_shapes,'exact_vertex_gauges':vertices,
            'exact_convex_combination_checks':interior,
            'forward_universal_gauge_bound':'S/3 < 1/3',
            'reverse_universal_gauge_bound':'S/5 < 1/5',
            'forward_conditional_width_bound':'3*A0/2',
            'reverse_conditional_width_bound':'5*A0/4',
            'both_width_constants_below_17_5':True,
            'necessary_target_determinant_sign':'D<0',
            'corrections_required':[],'solver_queries_run':0,
            'scope':'Independent analytic review supported by exact arithmetic; no negative-branch exclusion, other-height-chart theorem, priority claim, or global flatness improvement.'}
    (ROOT/'results/det5_positive_determinant_independent_review.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
