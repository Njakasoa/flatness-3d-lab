from fractions import Fraction as F
import pytest
from src.exact import Q, inverse, matmul
from src.geometry import Polytope, certify_hollow, certify_width, simplex_automorphisms
from src.examples import codenotti_santos, standard_simplex


def test_exact_sign_near_cancellation():
    # Pell convergent: float evaluation rounds this strictly positive number to zero.
    x=Q(886731088897,-627013566048)
    assert x>0 and x.floor()==0 and x.ceil()==1
    assert Q(1,1)*Q(1,-1)==-1
    assert Q(2,1)/Q(2,1)==1
    assert Q(F(-7,3)).floor()==-3

def test_input_contracts():
    with pytest.raises(TypeError): Q(0.1)
    with pytest.raises(ValueError): Q(0,1,5)
    with pytest.raises(ValueError): Q(0,1,2)+Q(0,1,3)
    with pytest.raises(ValueError): Polytope([(0,0),(1,0),(2,0)])

def test_baseline():
    K=codenotti_santos(); w=certify_width(K); h=certify_hollow(K)
    assert Q.from_json(w['width'])==Q(2,1)
    assert len(w['minimizing_directions_mod_sign'])==7
    assert h['hollow'] and len(h['boundary_points'])==4
    assert all(len(f['relative_interior_contacts'])==1 for f in h['facets'])
    assert len(simplex_automorphisms(K))==4

def test_hollow_boundary_and_hidden_interior():
    assert certify_hollow(standard_simplex(3,3))['hollow']
    h=certify_hollow(standard_simplex(3,4))
    assert not h['hollow'] and (1,1,1) in h['interior_points']

def test_unimodular_shear_finds_nontrivial_minimizers():
    K=standard_simplex(2).transform([[1,13],[0,1]],[5,-3])
    c=certify_width(K)
    assert Q.from_json(c['width'])==1
    assert (1,-13) in c['minimizing_directions_mod_sign']
    assert certify_hollow(K)['hollow']

def test_non_simplex_facets():
    K=Polytope([(0,0),(1,0),(1,1),(0,1)])
    assert len(K.facets())==4
    assert certify_hollow(K)['hollow']
    assert Q.from_json(certify_width(K)['width'])==1
    with pytest.raises(NotImplementedError): K.volume()

def test_bad_transform_and_cap_fail_closed():
    K=standard_simplex()
    with pytest.raises(ValueError): K.transform([[2,0,0],[0,1,0],[0,0,1]],[0,0,0])
    with pytest.raises(ValueError): K.transform([[1,0,0],[0,1,0],[0,0,1]],[F(1,2),0,0])
    with pytest.raises(RuntimeError): certify_width(K,max_directions=1)
    with pytest.raises(RuntimeError): certify_hollow(K,max_points=1)
