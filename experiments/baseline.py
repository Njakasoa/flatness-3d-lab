"""Run from the project root: python -m experiments.baseline."""
import json
from pathlib import Path
from src.examples import codenotti_santos
from src.geometry import certify_width, certify_hollow, simplex_automorphisms
from src.exact import Q


def main():
    K=codenotti_santos()
    width=certify_width(K); hollow=certify_hollow(K)
    assert Q.from_json(width['width'])==Q(2,1)
    assert hollow['hollow']
    result={'body':'Codenotti-Santos in Z^3','vertices':K.json(),
        'volume':K.volume().json(),'width_certificate':width,
        'hollow_certificate':hollow,'lattice_automorphisms':simplex_automorphisms(K)}
    Path('certificates/codenotti_santos.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'width':str(Q.from_json(width['width'])),'volume':str(K.volume()),
          'directions':width['minimizing_directions_mod_sign'],
          'box':width['search_bound']['coordinate_bounds'],
          'contacts':hollow['boundary_points'],'symmetry_order':len(result['lattice_automorphisms'])},indent=2))
if __name__=='__main__': main()
