"""Exact adversarial control against the assertion 'large width forces tetrahedral'."""
import json
from pathlib import Path
from fractions import Fraction as F
from src.examples import codenotti_santos
from src.geometry import Polytope, certify_width, certify_hollow
from src.exact import Q


def main():
    K=codenotti_santos();delta=F(1,1000);v0=K.vertices[0]
    cuts=[tuple((1-delta)*a+delta*b for a,b in zip(v0,v)) for v in K.vertices[1:]]
    T=Polytope(list(K.vertices[1:])+cuts)
    w=certify_width(T);h=certify_hollow(T)
    assert h['hollow'] and len(T.facets())==5 and len(T.vertices)==6
    assert Q.from_json(w['width'])>F(17,5)
    result={'body':'one-vertex truncation of Delta','delta':str(delta),'vertices':T.json(),
       'facet_count':5,'vertex_count':6,'width_certificate':w,'hollow_certificate':h,
       'scope':'nonmaximal hollow body; does not refute any maximal-body conjecture'}
    Path('certificates/truncated_delta.json').write_text(json.dumps(result,indent=2)+'\n')
    print('truncated width',Q.from_json(w['width']))
if __name__=='__main__':main()
